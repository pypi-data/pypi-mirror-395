"""
TaskCenter API 客户端

这个类是一个纯粹的 API 客户端，用于与 TaskCenter API 进行通信。
所有方法都是异步的，支持实时查询。
"""
import logging
from typing import Optional, Dict, Any, List
import aiohttp

logger = logging.getLogger(__name__)


class TaskCenterClient:
    """
    TaskCenter API 客户端

    这是一个轻量级的 HTTP 客户端，专门用于与 TaskCenter API 进行通信。

    特点：
    - 纯异步接口，所有方法都返回协程
    - 无状态设计，每次调用都是实时查询
    - 自动管理 HTTP 会话
    - 完整的错误处理和日志记录

    使用示例：
        ```python
        # 初始化客户端
        client = TaskCenterClient(task_center_url="http://localhost:8001")

        # 获取命名空间列表
        namespaces = await client.get_namespace_list()

        # 获取特定命名空间
        namespace = await client.get_namespace("default")

        # 获取统计信息
        stats = await client.get_namespace_statistics("default")

        # 使用完毕后关闭
        await client.close()
        ```

    或使用上下文管理器：
        ```python
        async with TaskCenterClient("http://localhost:8001") as client:
            namespaces = await client.get_namespace_list()
        ```
    """

    def __init__(self, task_center_url: str, api_key: Optional[str] = None):
        """
        初始化 TaskCenter API 客户端

        Args:
            task_center_url: TaskCenter 的基础 URL，例如 "http://localhost:8001"
                           不需要包含 /api/task/v1 路径，客户端会自动添加
            api_key: API密钥，用于请求鉴权（可选）

        示例：
            client = TaskCenterClient("http://localhost:8001")
            client = TaskCenterClient("https://taskcenter.example.com", api_key="your-api-key")
        """
        # 移除末尾的斜杠
        self.task_center_url = task_center_url.rstrip('/')
        self._base_api_url = f"{self.task_center_url}/api/task/v1"
        self._session: Optional[aiohttp.ClientSession] = None
        self._api_key = api_key

        logger.info(f"TaskCenter 客户端初始化: {self.task_center_url}")
        if api_key:
            logger.info("API 密钥已配置，将使用鉴权模式")

    async def _get_session(self) -> aiohttp.ClientSession:
        """获取或创建 HTTP 会话"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
            logger.debug("创建新的 HTTP 会话")
        return self._session

    def _get_headers(self) -> Dict[str, str]:
        """获取请求头（包含 API Key）"""
        headers = {}
        if self._api_key:
            headers['X-API-Key'] = self._api_key
        return headers

    async def get_namespace_list(
        self,
        page: int = 1,
        page_size: int = 100,
        is_active: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        获取命名空间列表

        Args:
            page: 页码，从 1 开始，默认为 1
            page_size: 每页数量，范围 1-100，默认为 100
            is_active: 是否只返回激活的命名空间，None 表示返回所有

        Returns:
            命名空间列表，每个元素是一个包含命名空间完整信息的字典

        Raises:
            aiohttp.ClientError: 网络请求失败
            ValueError: API 返回错误状态码

        示例：
            # 获取所有命名空间
            all_namespaces = await client.get_namespace_list()

            # 只获取激活的命名空间
            active_namespaces = await client.get_namespace_list(is_active=True)

            # 分页获取
            first_page = await client.get_namespace_list(page=1, page_size=20)
        """
        url = f"{self._base_api_url}/namespaces/"
        params = {
            'page': page,
            'page_size': page_size
        }
        if is_active is not None:
            params['is_active'] = is_active

        logger.debug(f"获取命名空间列表: page={page}, page_size={page_size}, is_active={is_active}")

        try:
            session = await self._get_session()
            headers = self._get_headers()
            async with session.get(url, params=params, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    logger.debug(f"成功获取 {len(data)} 个命名空间")
                    return data
                else:
                    error_text = await resp.text()
                    logger.error(f"获取命名空间列表失败: HTTP {resp.status}, {error_text}")
                    raise ValueError(f"获取命名空间列表失败: HTTP {resp.status}")
        except aiohttp.ClientError as e:
            logger.error(f"网络请求失败: {e}")
            raise
        except Exception as e:
            logger.error(f"获取命名空间列表失败: {e}")
            raise

    async def get_namespace(self, namespace_name: str) -> Dict[str, Any]:
        """
        获取特定命名空间的详细信息

        Args:
            namespace_name: 命名空间名称

        Returns:
            命名空间的完整配置信息，包括：
            - name: 命名空间名称
            - description: 描述
            - enabled: 是否启用
            - redis_config: Redis 配置
            - pg_config: PostgreSQL 配置
            - redis_url: Redis 连接 URL
            - pg_url: PostgreSQL 连接 URL
            - version: 配置版本号
            - created_at: 创建时间
            - updated_at: 更新时间

        Raises:
            ValueError: 命名空间不存在或 API 返回错误
            aiohttp.ClientError: 网络请求失败

        示例：
            namespace = await client.get_namespace("default")
            print(f"命名空间: {namespace['name']}")
            print(f"Redis URL: {namespace['redis_url']}")
            print(f"PG URL: {namespace['pg_url']}")
        """
        url = f"{self._base_api_url}/{namespace_name}/"

        logger.debug(f"获取命名空间详情: {namespace_name}")

        try:
            session = await self._get_session()
            headers = self._get_headers()
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    logger.info(f"成功获取命名空间 '{namespace_name}' 的详细信息")
                    return data
                elif resp.status == 404:
                    logger.error(f"命名空间 '{namespace_name}' 不存在")
                    raise ValueError(f"命名空间 '{namespace_name}' 不存在")
                else:
                    error_text = await resp.text()
                    logger.error(f"获取命名空间失败: HTTP {resp.status}, {error_text}")
                    raise ValueError(f"获取命名空间失败: HTTP {resp.status}")
        except aiohttp.ClientError as e:
            logger.error(f"网络请求失败: {e}")
            raise
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"获取命名空间失败: {e}")
            raise

    async def get_namespace_statistics(self, namespace_name: str) -> Dict[str, Any]:
        """
        获取命名空间的统计信息

        Args:
            namespace_name: 命名空间名称

        Returns:
            统计信息字典，包含：
            - total_queues: 队列总数
            - total_tasks: 任务总数
            - active_workers: 活跃 Worker 数
            - redis_memory_usage: Redis 内存使用（字节）
            - db_connections: 数据库连接数

        Raises:
            ValueError: 命名空间不存在或 API 返回错误
            aiohttp.ClientError: 网络请求失败

        示例：
            stats = await client.get_namespace_statistics("default")
            print(f"队列数: {stats['total_queues']}")
            print(f"任务数: {stats['total_tasks']}")
            print(f"Worker 数: {stats['active_workers']}")
        """
        url = f"{self._base_api_url}/{namespace_name}/statistics"

        logger.debug(f"获取命名空间统计信息: {namespace_name}")

        try:
            session = await self._get_session()
            headers = self._get_headers()
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    logger.info(f"成功获取命名空间 '{namespace_name}' 的统计信息")
                    return data
                elif resp.status == 404:
                    logger.error(f"命名空间 '{namespace_name}' 不存在")
                    raise ValueError(f"命名空间 '{namespace_name}' 不存在")
                else:
                    error_text = await resp.text()
                    logger.error(f"获取统计信息失败: HTTP {resp.status}, {error_text}")
                    raise ValueError(f"获取统计信息失败: HTTP {resp.status}")
        except aiohttp.ClientError as e:
            logger.error(f"网络请求失败: {e}")
            raise
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"获取统计信息失败: {e}")
            raise

    async def create_namespace(self, namespace_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建新的命名空间

        Args:
            namespace_data: 命名空间配置数据，包含：
                - name: 命名空间名称（必需）
                - description: 描述（可选）
                - config_mode: 配置模式，"direct" 或 "nacos"（必需）
                - redis_url: Redis 连接 URL（direct 模式必需）
                - pg_url: PostgreSQL 连接 URL（direct 模式必需）
                - redis_nacos_key: Redis Nacos 配置键（nacos 模式必需）
                - pg_nacos_key: PostgreSQL Nacos 配置键（nacos 模式必需）

        Returns:
            创建成功的命名空间信息

        Raises:
            ValueError: 创建失败（如名称已存在、参数错误等）
            aiohttp.ClientError: 网络请求失败

        示例：
            # 使用 direct 模式创建
            namespace = await client.create_namespace({
                "name": "production",
                "description": "生产环境",
                "config_mode": "direct",
                "redis_url": "redis://:password@localhost:6379/0",
                "pg_url": "postgresql://user:password@localhost:5432/jettask"
            })
        """
        url = f"{self._base_api_url}/namespaces/"

        logger.debug(f"创建命名空间: {namespace_data.get('name')}")

        try:
            session = await self._get_session()
            headers = self._get_headers()
            async with session.post(url, json=namespace_data, headers=headers) as resp:
                if resp.status == 201:
                    data = await resp.json()
                    logger.info(f"成功创建命名空间 '{namespace_data.get('name')}'")
                    return data
                elif resp.status == 400:
                    error_text = await resp.text()
                    logger.error(f"创建命名空间失败: {error_text}")
                    raise ValueError(f"创建命名空间失败: {error_text}")
                else:
                    error_text = await resp.text()
                    logger.error(f"创建命名空间失败: HTTP {resp.status}, {error_text}")
                    raise ValueError(f"创建命名空间失败: HTTP {resp.status}")
        except aiohttp.ClientError as e:
            logger.error(f"网络请求失败: {e}")
            raise
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"创建命名空间失败: {e}")
            raise

    async def update_namespace(
        self,
        namespace_name: str,
        update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        更新命名空间配置

        Args:
            namespace_name: 命名空间名称
            update_data: 要更新的字段，所有字段都是可选的：
                - description: 描述
                - enabled: 是否启用
                - config_mode: 配置模式
                - redis_url: Redis 连接 URL
                - pg_url: PostgreSQL 连接 URL
                - redis_nacos_key: Redis Nacos 配置键
                - pg_nacos_key: PostgreSQL Nacos 配置键

        Returns:
            更新后的命名空间信息

        Raises:
            ValueError: 更新失败（如命名空间不存在、参数错误等）
            aiohttp.ClientError: 网络请求失败

        示例：
            # 更新描述和状态
            namespace = await client.update_namespace("default", {
                "description": "默认命名空间（已更新）",
                "enabled": True
            })
        """
        url = f"{self._base_api_url}/{namespace_name}/"

        logger.debug(f"更新命名空间: {namespace_name}")

        try:
            session = await self._get_session()
            headers = self._get_headers()
            async with session.put(url, json=update_data, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    logger.info(f"成功更新命名空间 '{namespace_name}'")
                    return data
                elif resp.status == 404:
                    logger.error(f"命名空间 '{namespace_name}' 不存在")
                    raise ValueError(f"命名空间 '{namespace_name}' 不存在")
                elif resp.status == 400:
                    error_text = await resp.text()
                    logger.error(f"更新命名空间失败: {error_text}")
                    raise ValueError(f"更新命名空间失败: {error_text}")
                else:
                    error_text = await resp.text()
                    logger.error(f"更新命名空间失败: HTTP {resp.status}, {error_text}")
                    raise ValueError(f"更新命名空间失败: HTTP {resp.status}")
        except aiohttp.ClientError as e:
            logger.error(f"网络请求失败: {e}")
            raise
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"更新命名空间失败: {e}")
            raise

    async def delete_namespace(self, namespace_name: str) -> Dict[str, Any]:
        """
        删除命名空间

        Args:
            namespace_name: 命名空间名称

        Returns:
            删除结果，包含 success 和 message 字段

        Raises:
            ValueError: 删除失败（如命名空间不存在、默认命名空间不能删除等）
            aiohttp.ClientError: 网络请求失败

        示例：
            result = await client.delete_namespace("staging")
            print(result['message'])  # "命名空间已删除"

        注意:
            - 默认命名空间（default）不能删除
            - 删除操作不可逆
        """
        url = f"{self._base_api_url}/{namespace_name}/"

        logger.debug(f"删除命名空间: {namespace_name}")

        try:
            session = await self._get_session()
            headers = self._get_headers()
            async with session.delete(url, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    logger.info(f"成功删除命名空间 '{namespace_name}'")
                    return data
                elif resp.status == 404:
                    logger.error(f"命名空间 '{namespace_name}' 不存在")
                    raise ValueError(f"命名空间 '{namespace_name}' 不存在")
                elif resp.status == 400:
                    error_text = await resp.text()
                    logger.error(f"删除命名空间失败: {error_text}")
                    raise ValueError(f"删除命名空间失败: {error_text}")
                else:
                    error_text = await resp.text()
                    logger.error(f"删除命名空间失败: HTTP {resp.status}, {error_text}")
                    raise ValueError(f"删除命名空间失败: HTTP {resp.status}")
        except aiohttp.ClientError as e:
            logger.error(f"网络请求失败: {e}")
            raise
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"删除命名空间失败: {e}")
            raise

    async def close(self):
        """
        关闭 HTTP 会话，释放资源

        在不再使用客户端时应该调用此方法。
        如果使用上下文管理器（async with），会自动调用。

        示例：
            client = TaskCenterClient("http://localhost:8001")
            try:
                # 使用客户端
                namespaces = await client.get_namespace_list()
            finally:
                # 关闭客户端
                await client.close()
        """
        if self._session and not self._session.closed:
            await self._session.close()
            logger.debug("HTTP 会话已关闭")

    async def __aenter__(self):
        """支持异步上下文管理器"""
        return self

    async def __aexit__(self, _exc_type, _exc_val, _exc_tb):
        """退出上下文时自动关闭会话"""
        await self.close()

    def __repr__(self) -> str:
        """字符串表示"""
        return f"<TaskCenterClient url='{self.task_center_url}'>"




__all__ = ['TaskCenterClient']
