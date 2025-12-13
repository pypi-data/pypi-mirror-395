"""
数据库模块

提供统一的数据库模型定义、操作接口和连接管理
"""

from .base import Base, get_engine, get_session, init_db
from .connector import (
    # 连接池函数
    get_sync_redis_pool,
    get_async_redis_pool,
    get_async_redis_pool_for_pubsub,
    get_pg_engine_and_factory,
    get_asyncpg_pool,
    # 客户端实例函数
    get_sync_redis_client,
    get_async_redis_client,
    get_dual_mode_async_redis_client,
    # 缓存清理
    clear_all_cache,
    # 配置解析
    DBConfig,
    # 连接器类
    SyncRedisConnector,
    RedisConnector,
    PostgreSQLConnector,
    ConnectionManager,
    # 便捷函数
    create_redis_client,
    create_pg_session,
)

__all__ = [
    # SQLAlchemy 基础
    'Base',
    'get_engine',
    'get_session',
    'init_db',

    # 连接池函数
    'get_sync_redis_pool',
    'get_async_redis_pool',
    'get_async_redis_pool_for_pubsub',
    'get_pg_engine_and_factory',
    'get_asyncpg_pool',

    # 客户端实例函数
    'get_sync_redis_client',
    'get_async_redis_client',
    'get_dual_mode_async_redis_client',

    # 缓存清理
    'clear_all_cache',

    # 配置解析
    'DBConfig',

    # 连接器类
    'SyncRedisConnector',
    'RedisConnector',
    'PostgreSQLConnector',
    'ConnectionManager',

    # 便捷函数
    'create_redis_client',
    'create_pg_session',
]
