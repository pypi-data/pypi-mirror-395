"""
命名空间上下文 - 简洁的命名空间管理类
"""
import asyncio
import logging
import os
import sys
from typing import Optional, Dict, Any, List, TYPE_CHECKING
from datetime import datetime
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker
from jettask.core.center_client import TaskCenterClient
from jettask.db.connector import (
    get_dual_mode_async_redis_client,
    get_pg_engine_and_factory
)
from jettask.config.nacos_config import config as nacos_config

if TYPE_CHECKING:
    from jettask.webui.services.namespace_service import NamespaceService


# 配置日志格式 - 根据环境变量 JETTASK_LOG_FORMAT 决定
log_format = os.environ.get('JETTASK_LOG_FORMAT', 'text').lower()
log_level = logging.INFO

logger = logging.getLogger(__name__)

# 配置日志handler（与 webui/app.py 保持一致）
from jettask.utils.task_logger import JSONFormatter, ExtendedTextFormatter, TaskContextFilter

# 清除已有的handler，避免重复
logger.handlers.clear()
logger.setLevel(log_level)

handler = logging.StreamHandler(sys.stderr)
handler.addFilter(TaskContextFilter())

if log_format == 'json':
    handler.setFormatter(JSONFormatter())
else:
    handler.setFormatter(ExtendedTextFormatter(
        '%(asctime)s - %(levelname)s - [%(task_id)s] - %(name)s - %(message)s'
    ))

logger.addHandler(handler)
logger.propagate = False  # 不传播到父logger


class NamespaceContext:
    """
    命名空间上下文 - 管理命名空间的数据库连接和相关信息

    简洁的设计，专注于连接管理和基本信息维护
    """

    def __init__(
        self,
        pg_info: Dict[str, Any],
        redis_info: Dict[str, Any],
        name: Optional[str] = None,
        description: Optional[str] = None,
        version: Optional[int] = None,
        enabled: bool = True,
        connection_url: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        **kwargs
    ):
        """
        初始化命名空间上下文

        Args:
            pg_info: PostgreSQL配置信息
            redis_info: Redis配置信息
            name: 命名空间名称
            description: 描述
            version: 配置版本号
            enabled: 是否启用
            connection_url: API连接URL
            created_at: 创建时间
            updated_at: 更新时间
            **kwargs: 其他扩展信息
        """
        # 基本信息
        self.name = name
        self.description = description
        self.version = version
        self.enabled = enabled
        self.connection_url = connection_url
        self.created_at = created_at
        self.updated_at = updated_at

        # 配置信息
        self.pg_info = pg_info
        self.redis_info = redis_info

        # 扩展信息
        self.extra_info = kwargs

        # 连接资源
        self._redis_text_client: Optional[redis.Redis] = None
        self._redis_binary_client: Optional[redis.Redis] = None
        self._pg_engine: Optional[AsyncEngine] = None
        self._pg_session_factory: Optional[async_sessionmaker] = None

        # Jettask 应用实例（用于任务发送）
        self._jettask_app: Optional['Jettask'] = None

        # QueueRegistry 实例（用于队列管理）
        self._queue_registry: Optional['QueueRegistry'] = None

        # 独立的初始化标志
        self._redis_initialized = False
        self._pg_initialized = False
        self._jettask_initialized = False
        self._queue_registry_initialized = False

    @classmethod
    def from_flat_dict(cls, data: Dict[str, Any]) -> 'NamespaceContext':
        """从扁平化的字典创建 NamespaceContext 实例"""
        # 提取 PostgreSQL 信息
        pg_info = {
            'url': data.get('pg_url'),
            'config_mode': data.get('pg_config_mode', 'direct'),
            'nacos_key': data.get('pg_nacos_key')
        }

        # 提取 Redis 信息
        redis_info = {
            'url': data.get('redis_url'),
            'config_mode': data.get('redis_config_mode', 'direct'),
            'nacos_key': data.get('redis_nacos_key'),
            'prefix': data.get('redis_prefix')  # 支持显式的 redis_prefix
        }

        # 提取其他字段
        return cls(
            pg_info=pg_info,
            redis_info=redis_info,
            name=data.get('name'),
            description=data.get('description'),
            version=data.get('version'),
            enabled=data.get('enabled', True),
            connection_url=data.get('connection_url'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

    def _resolve_config_url(self, config_info: Dict[str, Any], config_type: str) -> Optional[str]:
        """
        解析配置URL，根据 config_mode 决定是直接使用还是从 Nacos 获取

        Args:
            config_info: 配置信息字典，包含 url/config_mode/nacos_key
            config_type: 配置类型，用于日志输出（'Redis' 或 'PostgreSQL'）

        Returns:
            解析后的真实连接URL，如果无法解析则返回 None
        """
        if not config_info:
            logger.debug(f"Namespace {self.name} has no {config_type} configuration")
            return None

        config_mode = config_info.get('config_mode', 'direct')

        if config_mode == 'direct':
            # Direct 模式：直接使用提供的 URL
            url = config_info.get('url')
            if url:
                logger.debug(f"Namespace {self.name} {config_type} using direct mode: {url}")
                return url
            else:
                logger.warning(f"Namespace {self.name} {config_type} config_mode is 'direct' but no URL provided")
                return None

        elif config_mode == 'nacos':
            # Nacos 模式：从 Nacos 获取真实 URL
            nacos_key = config_info.get('nacos_key')
            if not nacos_key:
                logger.warning(f"Namespace {self.name} {config_type} config_mode is 'nacos' but no nacos_key provided")
                return None

            try:
                logger.debug(f"Namespace {self.name} {config_type} fetching URL from Nacos with key: {nacos_key}")
                url = nacos_config.get(nacos_key)
                if url:
                    logger.info(f"Namespace {self.name} {config_type} successfully fetched from Nacos: {nacos_key}")
                    return url
                else:
                    logger.warning(f"Namespace {self.name} {config_type} Nacos key '{nacos_key}' returned empty value")
                    return None
            except Exception as e:
                logger.error(f"Namespace {self.name} failed to fetch {config_type} URL from Nacos (key: {nacos_key}): {e}", exc_info=True)
                return None

        else:
            logger.error(f"Namespace {self.name} {config_type} unknown config_mode: {config_mode}")
            return None

    async def _initialize_redis(self):
        """懒加载：初始化 Redis 连接（仅在第一次使用时调用）"""
        if self._redis_initialized:
            logger.debug(f"Namespace {self.name} Redis already initialized, skipping")
            return

        try:
            redis_url = self._resolve_config_url(self.redis_info, 'Redis')
            if redis_url:
                logger.debug(f"Lazy-loading Redis connection for namespace {self.name}")
                self._redis_text_client, self._redis_binary_client = get_dual_mode_async_redis_client(
                    redis_url=redis_url,
                    max_connections=50
                )
                logger.info(f"Namespace {self.name} Redis connection initialized successfully")
            else:
                logger.debug(f"Namespace {self.name} has no valid Redis configuration")

            self._redis_initialized = True

        except Exception as e:
            logger.error(f"Failed to initialize Redis for namespace {self.name}: {e}", exc_info=True)
            raise

    async def _initialize_pg(self):
        """懒加载：初始化 PostgreSQL 连接（仅在第一次使用时调用）"""
        if self._pg_initialized:
            logger.debug(f"Namespace {self.name} PostgreSQL already initialized, skipping")
            return

        try:
            pg_url = self._resolve_config_url(self.pg_info, 'PostgreSQL')
            if pg_url:
                # 确保使用 asyncpg 驱动
                if pg_url.startswith('postgresql://'):
                    pg_url = pg_url.replace('postgresql://', 'postgresql+asyncpg://', 1)

                logger.debug(f"Lazy-loading PostgreSQL connection for namespace {self.name}")
                self._pg_engine, self._pg_session_factory = get_pg_engine_and_factory(
                    dsn=pg_url,
                    pool_size=10,
                    max_overflow=5,
                    pool_recycle=3600,
                    echo=False
                )
                logger.info(f"Namespace {self.name} PostgreSQL connection initialized successfully")
            else:
                logger.debug(f"Namespace {self.name} has no valid PostgreSQL configuration")

            self._pg_initialized = True

        except Exception as e:
            logger.error(f"Failed to initialize PostgreSQL for namespace {self.name}: {e}", exc_info=True)
            raise

    async def get_redis_client(self, decode: bool = True) -> redis.Redis:
        """
        获取 Redis 客户端（懒加载：第一次调用时自动初始化）

        Args:
            decode: 是否解码为字符串，默认 True（使用文本模式）

        Returns:
            Redis 客户端实例

        Raises:
            ValueError: 如果 Redis 未配置
        """
        # 懒加载：第一次使用时自动初始化
        if not self._redis_initialized:
            await self._initialize_redis()

        # 根据 decode 参数选择文本或二进制客户端
        client = self._redis_text_client if decode else self._redis_binary_client
        if not client:
            raise ValueError(f"Namespace {self.name} has no Redis configuration")

        return client

    async def get_pg_session(self) -> AsyncSession:
        """
        获取 PostgreSQL 会话（懒加载：第一次调用时自动初始化）

        Returns:
            PostgreSQL 异步会话

        Raises:
            ValueError: 如果 PostgreSQL 未配置
        """
        # 懒加载：第一次使用时自动初始化
        if not self._pg_initialized:
            await self._initialize_pg()

        if not self._pg_session_factory:
            raise ValueError(f"Namespace {self.name} has no PostgreSQL configuration")

        return self._pg_session_factory()

    @property
    def redis_prefix(self) -> str:
        """
        获取 Redis 键前缀

        从 redis_info 中提取 prefix，如果未配置则使用命名空间名称

        Returns:
            Redis 键前缀字符串
        """
        # 优先使用 redis_info 中配置的 prefix
        prefix = self.redis_info.get('prefix') if self.redis_info else None
        # 如果没有配置，使用命名空间名称作为前缀
        return prefix or self.name or 'jettask'

    @property
    def redis_config(self) -> Dict[str, Any]:
        """
        获取 Redis 配置信息（用于兼容旧代码）

        Returns:
            包含 url 和 prefix 的字典
        """
        return {
            'url': self._resolve_config_url(self.redis_info, 'Redis'),
            'prefix': self.redis_prefix
        }

    @property
    def pg_config(self) -> Dict[str, Any]:
        """
        获取 PostgreSQL 配置信息（用于兼容旧代码）

        Returns:
            包含 url 的字典
        """
        return {
            'url': self._resolve_config_url(self.pg_info, 'PostgreSQL')
        }

    async def get_jettask_app(self) -> 'Jettask':
        """
        获取 Jettask 应用实例（懒加载：第一次调用时自动创建）

        这个方法会创建并缓存 Jettask 实例，用于任务发送等操作。

        Returns:
            Jettask 应用实例

        Raises:
            ValueError: 如果 Redis 或 PostgreSQL 未配置
        """
        # 如果已经初始化过，直接返回缓存的实例
        if self._jettask_initialized and self._jettask_app:
            logger.debug(f"Namespace {self.name} Jettask already initialized, reusing instance")
            return self._jettask_app

        try:
            # 解析配置 URL
            redis_url = self._resolve_config_url(self.redis_info, 'Redis')
            pg_url = self._resolve_config_url(self.pg_info, 'PostgreSQL')

            if not redis_url:
                raise ValueError(f"Namespace {self.name} has no Redis configuration")
            if not pg_url:
                raise ValueError(f"Namespace {self.name} has no PostgreSQL configuration")

            # 导入 Jettask（延迟导入避免循环依赖）
            from jettask import Jettask

            logger.info(f"Creating Jettask instance for namespace {self.name}")
            logger.debug(f"  Redis URL: {redis_url}")
            logger.debug(f"  Redis Prefix: {self.redis_prefix}")
            logger.debug(f"  PG URL: {pg_url[:50]}...")

            # 创建 Jettask 实例
            self._jettask_app = Jettask(
                redis_url=redis_url,
                redis_prefix=self.redis_prefix,
                pg_url=pg_url
            )

            self._jettask_initialized = True
            logger.info(f"Namespace {self.name} Jettask instance created successfully")

            return self._jettask_app

        except Exception as e:
            logger.error(f"Failed to create Jettask instance for namespace {self.name}: {e}", exc_info=True)
            raise

    async def get_queue_registry(self) -> 'QueueRegistry':
        """
        获取 QueueRegistry 实例（懒加载：第一次调用时自动创建）

        这个方法会创建并缓存 QueueRegistry 实例，用于队列注册和查询操作。

        Returns:
            QueueRegistry 实例

        Raises:
            ValueError: 如果 Redis 未配置
        """
        # 如果已经初始化过，直接返回缓存的实例
        if self._queue_registry_initialized and self._queue_registry:
            logger.debug(f"Namespace {self.name} QueueRegistry already initialized, reusing instance")
            return self._queue_registry

        try:
            # 确保 Redis 已初始化
            if not self._redis_initialized:
                await self._initialize_redis()

            # 检查 Redis 客户端是否可用
            if not self._redis_binary_client or not self._redis_text_client:
                raise ValueError(f"Namespace {self.name} has no Redis configuration")

            # 导入 QueueRegistry（延迟导入避免循环依赖）
            from jettask.messaging.registry import QueueRegistry

            logger.info(f"Creating QueueRegistry instance for namespace {self.name}")
            logger.debug(f"  Redis Prefix: {self.redis_prefix}")

            # 创建 QueueRegistry 实例
            self._queue_registry = QueueRegistry(
                redis_client=self._redis_binary_client,  # 同步客户端（兼容旧代码）
                async_redis_client=self._redis_text_client,  # 异步客户端
                redis_prefix=self.redis_prefix
            )

            self._queue_registry_initialized = True
            logger.info(f"Namespace {self.name} QueueRegistry instance created successfully")

            return self._queue_registry

        except Exception as e:
            logger.error(f"Failed to create QueueRegistry instance for namespace {self.name}: {e}", exc_info=True)
            raise

    @property
    def is_initialized(self) -> bool:
        """检查是否已初始化（Redis 或 PostgreSQL 任一初始化即为 True）"""
        return self._redis_initialized or self._pg_initialized

    @property
    def has_redis(self) -> bool:
        """检查是否配置了 Redis（支持 direct 和 nacos 模式）"""
        if not self.redis_info:
            return False
        # Direct 模式：检查是否有 url
        if self.redis_info.get('config_mode') == 'direct':
            return bool(self.redis_info.get('url'))
        # Nacos 模式：检查是否有 nacos_key
        elif self.redis_info.get('config_mode') == 'nacos':
            return bool(self.redis_info.get('nacos_key'))
        return False

    @property
    def has_pg(self) -> bool:
        """检查是否配置了 PostgreSQL（支持 direct 和 nacos 模式）"""
        if not self.pg_info:
            return False
        # Direct 模式：检查是否有 url
        if self.pg_info.get('config_mode') == 'direct':
            return bool(self.pg_info.get('url'))
        # Nacos 模式：检查是否有 nacos_key
        elif self.pg_info.get('config_mode') == 'nacos':
            return bool(self.pg_info.get('nacos_key'))
        return False

    async def close(self):
        """关闭连接（清理引用，实际连接由全局单例管理）"""
        if not self.is_initialized:
            return

        logger.debug(f"Closing namespace {self.name} connections")

        # 清理引用（实际连接由全局单例池管理）
        self._redis_text_client = None
        self._redis_binary_client = None
        self._pg_engine = None
        self._pg_session_factory = None
        self._jettask_app = None
        self._queue_registry = None

        # 重置初始化标志
        self._redis_initialized = False
        self._pg_initialized = False
        self._jettask_initialized = False
        self._queue_registry_initialized = False

        logger.info(f"Namespace {self.name} closed")

    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典格式

        Returns:
            包含所有信息的字典
        """
        return {
            'name': self.name,
            'description': self.description,
            'version': self.version,
            'enabled': self.enabled,
            'connection_url': self.connection_url,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'pg_info': self.pg_info,
            'redis_info': self.redis_info,
            'redis_prefix': self.redis_prefix,
            'is_initialized': self.is_initialized,
            'redis_initialized': self._redis_initialized,
            'pg_initialized': self._pg_initialized,
            'jettask_initialized': self._jettask_initialized,
            'queue_registry_initialized': self._queue_registry_initialized,
            'has_redis': self.has_redis,
            'has_pg': self.has_pg,
            **self.extra_info
        }

    def __repr__(self) -> str:
        redis_mark = 'YES' if self.has_redis else 'NO'
        pg_mark = 'YES' if self.has_pg else 'NO'
        redis_init = 'INIT' if self._redis_initialized else 'LAZY'
        pg_init = 'INIT' if self._pg_initialized else 'LAZY'
        return (
            f"<NamespaceContext "
            f"name='{self.name}' "
            f"version={self.version} "
            f"redis={redis_mark}({redis_init}) "
            f"pg={pg_mark}({pg_init}) "
            f"enabled={self.enabled}>"
        )

class BaseNamespaceManager:
    """
    命名空间管理器基类

    提供命名空间管理的通用功能，子类只需实现数据加载逻辑。
    """

    def __init__(self, auto_refresh: bool = True, refresh_interval: int = 60):
        """
        初始化基础管理器

        Args:
            auto_refresh: 是否自动启动定时刷新，默认为 True
            refresh_interval: 刷新间隔（秒），默认为 60 秒
        """
        self._contexts: Dict[str, NamespaceContext] = {}
        self._initialized = False
        self._refresh_interval = refresh_interval
        self._refresh_task: Optional[asyncio.Task] = None
        self._auto_refresh_enabled = auto_refresh
        self._closed = False

    async def _ensure_loaded(self):
        """确保已加载命名空间列表（懒加载）"""
        if not self._initialized:
            await self.refresh()
            # 如果启用了自动刷新且还未启动刷新任务，则启动定时刷新
            if self._auto_refresh_enabled and self._refresh_task is None:
                self.start_auto_refresh()

    async def refresh(self):
        """
        刷新命名空间列表

        子类必须实现此方法以从不同的数据源加载命名空间。
        """
        raise NotImplementedError("子类必须实现 refresh() 方法")

    async def get_namespace(self, name: str) -> NamespaceContext:
        """
        获取指定名称的命名空间上下文（懒加载）

        Args:
            name: 命名空间名称

        Returns:
            NamespaceContext 实例

        Raises:
            ValueError: 命名空间不存在
        """
        await self._ensure_loaded()

        if name not in self._contexts:
            logger.error(f"命名空间 '{name}' 不存在")
            raise ValueError(f"命名空间 '{name}' 不存在")

        return self._contexts[name]

    async def list_namespaces(self, enabled_only: bool = False) -> List[NamespaceContext]:
        """
        列出所有命名空间上下文

        Args:
            enabled_only: 是否只返回已启用的命名空间

        Returns:
            NamespaceContext 列表
        """
        await self._ensure_loaded()

        contexts = list(self._contexts.values())

        if enabled_only:
            contexts = [ctx for ctx in contexts if ctx.enabled]

        logger.debug(f"列出 {len(contexts)} 个命名空间（enabled_only={enabled_only}）")
        return contexts

    async def get_namespace_names(self, enabled_only: bool = False) -> List[str]:
        """
        获取所有命名空间名称列表

        Args:
            enabled_only: 是否只返回已启用的命名空间

        Returns:
            命名空间名称列表
        """
        await self._ensure_loaded()

        if enabled_only:
            names = [name for name, ctx in self._contexts.items() if ctx.enabled]
        else:
            names = list(self._contexts.keys())

        logger.debug(f"获取 {len(names)} 个命名空间名称（enabled_only={enabled_only}）")
        return names

    def start_auto_refresh(self):
        """
        启动定时刷新任务

        在后台创建一个异步任务，定期调用 refresh() 方法刷新命名空间列表。
        """
        if self._refresh_task is not None:
            logger.warning("定时刷新任务已在运行，跳过启动")
            return

        if self._closed:
            logger.warning("管理器已关闭，无法启动定时刷新")
            return

        logger.info(f"启动命名空间定时刷新任务，间隔: {self._refresh_interval}秒")
        self._refresh_task = asyncio.create_task(self._auto_refresh_loop())

    def stop_auto_refresh(self):
        """
        停止定时刷新任务
        """
        if self._refresh_task is not None:
            logger.info("停止命名空间定时刷新任务")
            self._refresh_task.cancel()
            self._refresh_task = None

    async def _auto_refresh_loop(self):
        """
        定时刷新循环

        这个方法会在后台持续运行，每隔指定的时间间隔刷新一次命名空间列表。
        如果刷新失败，会记录错误日志但不会中断循环。
        """
        logger.info(f"定时刷新循环已启动，刷新间隔: {self._refresh_interval}秒")

        try:
            while not self._closed:
                # 等待指定的时间间隔
                await asyncio.sleep(self._refresh_interval)

                # 如果已经关闭，退出循环
                if self._closed:
                    break

                # 执行刷新
                try:
                    logger.debug("执行定时刷新命名空间列表...")
                    await self.refresh()
                    logger.debug("定时刷新命名空间列表完成")
                except Exception as e:
                    logger.error(f"定时刷新命名空间失败: {e}", exc_info=True)
                    # 继续循环，不中断定时刷新

        except asyncio.CancelledError:
            logger.info("定时刷新任务被取消")
        except Exception as e:
            logger.error(f"定时刷新循环异常退出: {e}", exc_info=True)
        finally:
            logger.info("定时刷新循环已结束")

    def _clear_contexts(self):
        """清理所有上下文（同步方法）"""
        self._contexts.clear()
        self._initialized = False

    async def _close_contexts(self):
        """关闭所有已初始化的上下文"""
        for ctx in self._contexts.values():
            if ctx.is_initialized:
                await ctx.close()

    async def close(self):
        """关闭所有命名空间上下文"""
        logger.info(f"关闭命名空间管理器: {len(self._contexts)} 个命名空间")

        # 标记为已关闭
        self._closed = True

        # 停止定时刷新任务
        self.stop_auto_refresh()

        # 如果任务存在，等待其完成
        if self._refresh_task is not None:
            try:
                await asyncio.wait_for(self._refresh_task, timeout=5.0)
            except (asyncio.TimeoutError, asyncio.CancelledError):
                logger.debug("定时刷新任务已取消或超时")

        await self._close_contexts()
        self._clear_contexts()

        logger.info("命名空间管理器已关闭")

    async def __aenter__(self):
        """支持异步上下文管理器"""
        return self

    async def __aexit__(self, _exc_type, _exc_val, _exc_tb):
        """退出上下文时自动关闭"""
        await self.close()


class NamespaceManagerAPI(BaseNamespaceManager):
    """
    基于 API 的多命名空间管理器

    通过 TaskCenterClient 从 API 获取命名空间数据，并管理多个 NamespaceContext 实例。
    适合客户端或远程调用场景。

    特点：
    - 通过 HTTP API 获取命名空间配置
    - 自动创建和缓存 NamespaceContext 实例
    - 支持懒加载：只有在访问时才创建上下文
    - 支持刷新：可以重新从 API 加载最新配置
    """

    def __init__(self, base_url: str, api_key: Optional[str] = None, auto_refresh: bool = True, refresh_interval: int = 60):
        """
        初始化基于 API 的命名空间管理器

        Args:
            base_url: TaskCenter 的基础 URL，例如 "http://localhost:8001"
            api_key: API密钥（用于请求鉴权）
            auto_refresh: 是否自动启动定时刷新，默认为 True
            refresh_interval: 刷新间隔（秒），默认为 60 秒
        """
        super().__init__(auto_refresh=auto_refresh, refresh_interval=refresh_interval)


        self.base_url = base_url
        self._client = TaskCenterClient(base_url, api_key=api_key)

        logger.info(f"NamespaceManagerAPI 初始化: base_url={base_url}")
        if api_key:
            logger.info("API 密钥已配置")

    async def refresh(self):
        """
        从 API 刷新命名空间列表

        重新从 TaskCenter API 获取所有命名空间配置，并更新缓存。
        """
        # logger.info(f"从 API 刷新命名空间列表: {self.base_url}")

        try:
            # 获取所有命名空间
            namespace_list = await self._client.get_namespace_list(page_size=100)

            # 保存旧的上下文以便后续关闭
            old_contexts = self._contexts
            self._contexts = {}

            # 为每个命名空间创建 NamespaceContext
            for ns_data in namespace_list:
                name = ns_data.get('name')
                if name:
                    # 创建新的上下文
                    ctx = NamespaceContext.from_flat_dict(ns_data)
                    self._contexts[name] = ctx
                    logger.debug(f"创建命名空间上下文: {name}")

            # 关闭旧的上下文
            for old_ctx in old_contexts.values():
                if old_ctx.is_initialized:
                    await old_ctx.close()

            self._initialized = True
            logger.debug(f"成功从 API 刷新 {len(self._contexts)} 个命名空间")

        except Exception as e:
            logger.error(f"从 API 刷新命名空间失败: {e}", exc_info=True)
            raise

    async def close(self):
        """关闭所有命名空间上下文和 API 客户端"""
        logger.info(f"关闭 NamespaceManagerAPI: {len(self._contexts)} 个命名空间")

        # 调用基类方法关闭所有上下文
        await self._close_contexts()

        # 关闭 API 客户端
        await self._client.close()

        # 清理状态
        self._clear_contexts()

        logger.info("NamespaceManagerAPI 已关闭")

    def __repr__(self) -> str:
        return (
            f"<NamespaceManagerAPI "
            f"base_url='{self.base_url}' "
            f"namespaces={len(self._contexts)} "
            f"initialized={self._initialized}>"
        )


class NamespaceManagerDB(BaseNamespaceManager):
    """
    基于数据库的多命名空间管理器

    通过 NamespaceService 直接从数据库读取命名空间数据，并管理多个 NamespaceContext 实例。
    适合服务端或有直接数据库访问权限的场景。

    特点：
    - 直接从数据库读取命名空间配置（不经过 API）
    - 自动创建和缓存 NamespaceContext 实例
    - 支持懒加载：只有在访问时才创建上下文
    - 支持刷新：可以重新从数据库加载最新配置
    """

    def __init__(self, auto_refresh: bool = True, refresh_interval: int = 60):
        """
        初始化基于数据库的命名空间管理器

        Args:
            auto_refresh: 是否自动启动定时刷新，默认为 True
            refresh_interval: 刷新间隔（秒），默认为 60 秒
        """
        super().__init__(auto_refresh=auto_refresh, refresh_interval=refresh_interval)
        logger.info("NamespaceManagerDB 初始化")

    async def refresh(self):
        """
        从数据库刷新命名空间列表

        重新从数据库获取所有命名空间配置，并更新缓存。
        """
        logger.info("从数据库刷新命名空间列表")

        try:
            # 懒加载 NamespaceService 和数据库连接
            from jettask.webui.services.namespace_service import NamespaceService
            from jettask.webui.config import webui_config
            from jettask.db.connector import get_pg_engine_and_factory

            # 获取元数据库会话工厂
            _, session_factory = get_pg_engine_and_factory(webui_config.meta_database_url)

            # 获取所有命名空间（分页获取所有）
            async with session_factory() as session:
                namespace_list = await NamespaceService.list_namespaces(session, page=1, page_size=1000)

            # 保存旧的上下文以便后续关闭
            old_contexts = self._contexts
            self._contexts = {}

            # 为每个命名空间创建 NamespaceContext
            for ns in namespace_list:
                name = ns.name
                if name:
                    # 将 NamespaceResponse 转换为 dict
                    ns_data = {
                        'name': ns.name,
                        'description': ns.description,
                        'redis_url': ns.redis_url,
                        'redis_config_mode': ns.redis_config_mode,
                        'redis_nacos_key': ns.redis_nacos_key,
                        'pg_url': ns.pg_url,
                        'pg_config_mode': ns.pg_config_mode,
                        'pg_nacos_key': ns.pg_nacos_key,
                        'connection_url': ns.connection_url,
                        'version': ns.version,
                        'enabled': ns.enabled,
                        'created_at': ns.created_at,
                        'updated_at': ns.updated_at
                    }

                    # 创建新的上下文
                    ctx = NamespaceContext.from_flat_dict(ns_data)
                    self._contexts[name] = ctx
                    logger.debug(f"创建命名空间上下文: {name}")

            # 关闭旧的上下文
            for old_ctx in old_contexts.values():
                if old_ctx.is_initialized:
                    await old_ctx.close()

            self._initialized = True
            logger.info(f"成功从数据库刷新 {len(self._contexts)} 个命名空间")

        except Exception as e:
            logger.error(f"从数据库刷新命名空间失败: {e}", exc_info=True)
            raise

    def __repr__(self) -> str:
        return (
            f"<NamespaceManagerDB "
            f"namespaces={len(self._contexts)} "
            f"initialized={self._initialized}>"
        )


