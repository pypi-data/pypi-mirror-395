"""
Namespace 中间件 - 自动注入命名空间上下文

这个中间件会自动检测路由中的 {namespace} 参数，并将 NamespaceContext 注入到 request.state.ns
这样所有路由都无需手动使用 Depends(get_namespace_context)，直接访问 request.state.ns 即可
"""
import asyncio
import logging
import re
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from typing import Callable

from jettask.core.namespace import NamespaceManagerDB

logger = logging.getLogger(__name__)


class NamespaceMiddleware(BaseHTTPMiddleware):
    """
    Namespace 自动注入中间件

    功能：
    1. 自动检测路由路径中的 {namespace} 参数
    2. 使用 NamespaceManagerDB 查询命名空间配置
    3. 将 NamespaceContext 注入到 request.state.ns
    4. 统一处理命名空间不存在等错误

    使用方式：
    ```python
    # 在 app.py 中注册
    app.add_middleware(NamespaceMiddleware)

    # 在路由中使用
    @router.get("/{namespace}/queues")
    async def get_queues(request: Request):
        ns = request.state.ns  # 已自动注入 NamespaceContext
        redis_client = await ns.get_redis_client()
        # ... 业务逻辑
    ```
    """

    # 预编译的正则表达式（性能优化）
    NAMESPACE_PATTERN = re.compile(r'/api/task/v1/([^/]+)')

    # 需要排除的路径前缀（这些路径不需要 namespace）
    # 使用元组而非列表，性能更好
    EXCLUDED_PATHS = (
        '/api/task/v1/namespaces',  # 命名空间管理自身（全局路由）
        '/docs',               # API 文档
        '/openapi.json',       # OpenAPI schema
        '/redoc',              # ReDoc 文档
        '/health',             # 健康检查
    )

    # 不是命名空间的资源名称（性能优化：使用集合）
    NON_NAMESPACE_RESOURCES = frozenset(['namespaces', 'auth'])

    def __init__(self, app):
        """
        初始化中间件

        Args:
            app: FastAPI 应用实例
        """
        super().__init__(app)
        # 创建命名空间管理器（基于数据库，默认启用自动刷新，间隔60秒）
        self._manager = NamespaceManagerDB(auto_refresh=True, refresh_interval=60)
        logger.info("NamespaceMiddleware 初始化完成，使用 NamespaceManagerDB（自动刷新已启用，间隔60秒）")

        # 在后台触发一次加载，这样自动刷新会立即启动
        # 注意：这里使用 asyncio.create_task 在后台执行，不阻塞中间件初始化
        asyncio.create_task(self._preload_namespaces())

    async def _preload_namespaces(self):
        """
        预加载命名空间列表

        这个方法在后台执行，会触发命名空间列表的首次加载，
        从而启动自动刷新任务。
        """
        try:
            logger.info("开始预加载命名空间列表...")
            namespaces = await self._manager.list_namespaces()
            logger.info(f"命名空间预加载完成，共 {len(namespaces)} 个命名空间，自动刷新已启动")
        except Exception as e:
            logger.warning(f"命名空间预加载失败: {e}，将在第一次请求时重试")

    async def dispatch(self, request: Request, call_next: Callable):
        """
        中间件处理逻辑（性能优化版本）

        Args:
            request: HTTP 请求对象
            call_next: 下一个中间件或路由处理器

        Returns:
            HTTP 响应
        """
        path = request.url.path

        # 1. 快速路径：检查是否是排除路径
        # 使用 path.startswith 的元组参数一次性检查所有前缀（Python 优化）
        if path.startswith(self.EXCLUDED_PATHS):
            return await call_next(request)

        # 2. 使用预编译的正则表达式提取 namespace
        namespace_match = self.NAMESPACE_PATTERN.search(path)

        if not namespace_match:
            # 没有 namespace 参数，直接放行
            return await call_next(request)

        namespace = namespace_match.group(1)

        # 3. 快速检查：是否是非命名空间的资源名称
        # 使用 frozenset 的 O(1) 查找
        if namespace in self.NON_NAMESPACE_RESOURCES:
            return await call_next(request)

        # 4. 使用 NamespaceManagerDB 获取命名空间上下文并注入
        try:
            # 从管理器获取 NamespaceContext（懒加载：第一次会从数据库加载所有命名空间）
            namespace_context = await self._manager.get_namespace(namespace)

            # 注入到 request.state，供路由使用
            request.state.ns = namespace_context

            logger.debug(f"已为请求 {path} 注入命名空间上下文: {namespace}")

        except ValueError as e:
            # 命名空间不存在
            logger.warning(f"命名空间 '{namespace}' 不存在: {e}")
            return JSONResponse(
                status_code=404,
                content={"detail": f"命名空间 '{namespace}' 不存在"}
            )
        except Exception as e:
            # 其他错误（数据库查询失败等）
            logger.error(f"获取命名空间 '{namespace}' 失败: {e}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={"detail": f"获取命名空间失败: {str(e)}"}
            )

        # 5. 调用下一个处理器
        response = await call_next(request)
        return response
