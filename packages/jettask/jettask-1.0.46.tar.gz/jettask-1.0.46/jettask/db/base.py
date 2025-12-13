"""
数据库基础配置

使用 SQLAlchemy 2.0 的异步API
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
import logging

logger = logging.getLogger(__name__)

# 创建基类
Base = declarative_base()

# 全局引擎和会话工厂
_engine = None
_async_session_factory = None


def get_engine(database_url: str, **kwargs):
    """
    获取或创建数据库引擎

    Args:
        database_url: 数据库连接URL（如 postgresql+asyncpg://user:pass@host/db）
        **kwargs: 其他引擎参数

    Returns:
        AsyncEngine: 异步数据库引擎
    """
    global _engine

    if _engine is None:
        # 确保使用正确的异步驱动
        if database_url and 'postgresql://' in database_url:
            database_url = database_url.replace('postgresql://', 'postgresql+asyncpg://')

        # 默认配置
        engine_kwargs = {
            'echo': kwargs.pop('echo', False),
            'pool_pre_ping': kwargs.pop('pool_pre_ping', True),
            'poolclass': kwargs.pop('poolclass', NullPool),  # 使用NullPool避免连接池问题
        }
        engine_kwargs.update(kwargs)

        _engine = create_async_engine(database_url, **engine_kwargs)
        logger.info(f"数据库引擎已创建: {database_url.split('@')[-1]}")

    return _engine


def get_session_factory(database_url: str = None, **kwargs):
    """
    获取或创建会话工厂

    Args:
        database_url: 数据库连接URL
        **kwargs: 其他引擎参数

    Returns:
        async_sessionmaker: 异步会话工厂
    """
    global _async_session_factory

    if _async_session_factory is None:
        if database_url is None:
            raise ValueError("数据库URL未提供")

        engine = get_engine(database_url, **kwargs)
        _async_session_factory = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    return _async_session_factory


def get_session(database_url: str = None, **kwargs):
    """
    获取数据库会话（上下文管理器）

    Args:
        database_url: 数据库连接URL
        **kwargs: 其他引擎参数

    Returns:
        AsyncSession: 异步数据库会话上下文管理器

    Example:
        async with get_session(db_url) as session:
            result = await session.execute(select(Task))
            tasks = result.scalars().all()
    """
    factory = get_session_factory(database_url, **kwargs)
    return factory()


async def init_db(database_url: str, **kwargs):
    """
    初始化数据库（创建所有表）

    Args:
        database_url: 数据库连接URL
        **kwargs: 其他引擎参数

    Example:
        await init_db('postgresql+asyncpg://user:pass@localhost/jettask')
    """
    # 导入所有模型以注册到 Base.metadata
    from .models import Task, ScheduledTask, TaskExecutionHistory  # noqa: F401

    engine = get_engine(database_url, **kwargs)

    async with engine.begin() as conn:
        # 创建所有表
        await conn.run_sync(Base.metadata.create_all)
        logger.info("数据库表已创建/更新")


async def drop_all(database_url: str, **kwargs):
    """
    删除所有表（谨慎使用！）

    Args:
        database_url: 数据库连接URL
        **kwargs: 其他引擎参数
    """
    # 导入所有模型以注册到 Base.metadata
    from .models import Task, ScheduledTask, TaskExecutionHistory  # noqa: F401

    engine = get_engine(database_url, **kwargs)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        logger.warning("所有数据库表已删除")
