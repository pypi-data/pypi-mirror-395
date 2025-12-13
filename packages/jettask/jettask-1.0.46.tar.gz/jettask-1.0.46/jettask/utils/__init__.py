from .helpers import get_hostname, gen_task_name, is_async_function
from .task_logger import get_task_logger

# 为了向后兼容，从 jettask.db 重新导出数据库连接函数
from jettask.db.connector import (
    # 全局连接池函数
    get_sync_redis_pool,
    get_async_redis_pool,
    get_pg_engine_and_factory,
    # 客户端实例函数
    get_sync_redis_client,
    get_async_redis_client,
    get_dual_mode_async_redis_client,
    # 配置解析
    DBConfig,
)

__all__ = [
    "get_hostname",
    "gen_task_name",
    "is_async_function",
    # 全局连接池函数（向后兼容）
    "get_sync_redis_pool",
    "get_async_redis_pool",
    "get_pg_engine_and_factory",
    # 客户端实例函数
    "get_sync_redis_client",
    "get_async_redis_client",
    "get_dual_mode_async_redis_client",
    # 数据库连接工具
    "DBConfig",
    "get_task_logger",
]