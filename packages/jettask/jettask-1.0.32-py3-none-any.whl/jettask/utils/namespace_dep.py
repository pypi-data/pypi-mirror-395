"""
命名空间依赖注入工具
提供统一的命名空间参数处理和数据库连接管理
"""
import logging
from typing import Optional
from fastapi import Depends, HTTPException, Path, Request
from jettask.namespace import NamespaceConnection, NamespaceDataAccessManager

logger = logging.getLogger(__name__)


class NamespaceContext:
    """
    命名空间上下文对象
    封装命名空间的所有信息和数据库连接
    """

    def __init__(
        self,
        namespace_name: str,
        connection: NamespaceConnection,
        manager: NamespaceDataAccessManager
    ):
        self.namespace_name = namespace_name
        self.connection = connection
        self.manager = manager

    async def get_redis_client(self, decode: bool = True):
        """获取 Redis 客户端"""
        return await self.connection.get_redis_client(decode=decode)

    async def get_pg_session(self):
        """获取 PostgreSQL 会话"""
        return await self.connection.get_pg_session()

    @property
    def redis_prefix(self) -> str:
        """获取 Redis 键前缀"""
        return self.connection.redis_prefix

    @property
    def redis_config(self) -> dict:
        """获取 Redis 配置"""
        return self.connection.redis_config

    @property
    def pg_config(self) -> dict:
        """获取 PostgreSQL 配置"""
        return self.connection.pg_config


def get_namespace_manager(request: Request) -> NamespaceDataAccessManager:
    """
    获取命名空间数据访问管理器
    从 app.state 中获取全局实例
    """
    if not hasattr(request.app.state, 'namespace_data_access'):
        raise HTTPException(
            status_code=500,
            detail="Namespace data access not initialized"
        )

    # namespace_data_access 是 NamespaceJetTaskDataAccess 实例
    # 它包含一个 manager 属性
    return request.app.state.namespace_data_access.manager


async def get_namespace_context(
    namespace: str = Path(..., description="命名空间名称", example="default"),
    manager: NamespaceDataAccessManager = Depends(get_namespace_manager)
) -> NamespaceContext:
    """
    获取命名空间上下文（依赖注入函数）

    这个函数会：
    1. 从路径参数中提取 namespace 名称
    2. 从任务中心API或Nacos获取命名空间配置
    3. 建立数据库连接（Redis + PostgreSQL）
    4. 返回封装好的命名空间上下文对象

    使用示例：
    ```python
    @router.get("/{namespace}/queues")
    async def get_queues(
        ns: NamespaceContext = Depends(get_namespace_context)
    ):
        # 直接使用 ns 对象访问数据库
        redis_client = await ns.get_redis_client()
        # ... 执行操作
        return {"namespace": ns.namespace_name}
    ```

    Args:
        namespace: 从路径参数中提取的命名空间名称
        manager: 命名空间数据访问管理器（自动注入）

    Returns:
        NamespaceContext: 命名空间上下文对象

    Raises:
        HTTPException: 当命名空间不存在或配置错误时
    """
    try:
        # 获取命名空间的数据库连接
        connection = await manager.get_connection(namespace)

        # 创建并返回上下文对象
        return NamespaceContext(
            namespace_name=namespace,
            connection=connection,
            manager=manager
        )

    except ValueError as e:
        logger.error(f"命名空间 '{namespace}' 配置错误: {e}")
        raise HTTPException(
            status_code=404,
            detail=f"命名空间 '{namespace}' 不存在或配置错误"
        )
    except Exception as e:
        logger.error(f"获取命名空间 '{namespace}' 上下文失败: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"获取命名空间连接失败: {str(e)}"
        )


# 为了向后兼容，提供一个简化的依赖函数
async def get_namespace_connection(
    namespace: str = Path(..., description="命名空间名称", example="default"),
    manager: NamespaceDataAccessManager = Depends(get_namespace_manager)
) -> NamespaceConnection:
    """
    获取命名空间数据库连接（简化版本）

    直接返回 NamespaceConnection 对象，适用于简单场景

    Args:
        namespace: 命名空间名称
        manager: 命名空间数据访问管理器

    Returns:
        NamespaceConnection: 数据库连接对象
    """
    try:
        return await manager.get_connection(namespace)
    except ValueError as e:
        logger.error(f"命名空间 '{namespace}' 配置错误: {e}")
        raise HTTPException(
            status_code=404,
            detail=f"命名空间 '{namespace}' 不存在或配置错误"
        )
    except Exception as e:
        logger.error(f"获取命名空间 '{namespace}' 连接失败: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"获取命名空间连接失败: {str(e)}"
        )


__all__ = [
    'NamespaceContext',
    'get_namespace_context',
    'get_namespace_connection',
    'get_namespace_manager'
]
