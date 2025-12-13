import os

import time
from datetime import datetime
from ..utils.serializer import dumps, loads, dumps_str, loads_str
import signal

import asyncio
import logging
import contextlib
import importlib
import time 

from typing import List


# 导入TaskMessage
from .message import TaskMessage
from .task import Task
from .enums import TaskStatus
from jettask.messaging.event_pool import EventPool
from ..executor.orchestrator import ProcessOrchestrator
from ..utils import gen_task_name
from ..scheduler import TaskScheduler
from ..exceptions import TaskTimeoutError, TaskExecutionError, TaskNotFoundError
# 导入统一的数据库连接管理
from jettask.db.connector import get_sync_redis_client, get_async_redis_client

# 尝试导入 uvloop,如果可用则使用它以获得更好的性能
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    UVLOOP_AVAILABLE = True
except ImportError:
    UVLOOP_AVAILABLE = False

logger = logging.getLogger('app')

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

if UVLOOP_AVAILABLE:
    logger.debug("Using uvloop for better performance")
else:
    logger.debug("uvloop not available, using default asyncio event loop")


class Jettask(object):
    # Lua脚本从config模块导入，统一管理

    def __init__(self, redis_url: str = None, include: list = None, max_connections: int = None,
                 consumer_config: dict = None, tasks=None,
                 redis_prefix: str = None, scheduler_config: dict = None, pg_url: str = None,
                 task_center=None, 
                 heartbeat_interval: float = 5.0, heartbeat_timeout: float = 15.0,
                 scanner_interval: float = 2) -> None:
        self._tasks = tasks or {}
        self._task_queues = {}  # 记录任务名称到队列的映射 (task_name -> queue_name)
        self.asyncio = False
        self.include = include or []

        # 任务中心相关属性
        self.task_center = None  # 将通过mount_task_center方法挂载或初始化时指定
        self._task_center_config = None
        self._original_redis_url = redis_url
        self._original_pg_url = pg_url

        # 优先使用传入参数，其次使用环境变量
        self.redis_url = redis_url or os.environ.get('JETTASK_REDIS_URL')
        self.pg_url = pg_url or os.environ.get('JETTASK_PG_URL')
        self.max_connections = max_connections if max_connections is not None else int(os.environ.get('JETTASK_MAX_CONNECTIONS', '500'))
        self.redis_prefix = redis_prefix or os.environ.get('JETTASK_REDIS_PREFIX', 'jettask')

        # 检查必需参数：redis_url
        if not self.redis_url:
            raise ValueError(
                "必须提供 redis_url 参数！\n\n"
                "请通过以下任一方式配置:\n"
                "  1. 初始化时传参:\n"
                "     app = Jettask(redis_url='redis://localhost:6379/0')\n\n"
                "  2. 设置环境变量:\n"
                "     export JETTASK_REDIS_URL='redis://localhost:6379/0'\n\n"
                "  3. 在 .env 文件中配置:\n"
                "     JETTASK_REDIS_URL=redis://localhost:6379/0\n"
            )

        self.consumer_config = consumer_config or {}
        self.scheduler_config = scheduler_config or {}

        # 心跳配置
        # 校验：heartbeat_timeout 必须大于 heartbeat_interval 的 2 倍
        # 否则会导致 worker 在正常心跳期间就被判定为超时
        if heartbeat_timeout <= heartbeat_interval * 2:
            raise ValueError(
                f"heartbeat_timeout ({heartbeat_timeout}s) 必须大于 heartbeat_interval ({heartbeat_interval}s) 的 2 倍！\n\n"
                f"当前配置会导致 worker 在正常心跳间隔内就被判定为超时。\n"
                f"建议配置：heartbeat_timeout >= heartbeat_interval * 3\n"
                f"例如：heartbeat_interval=5.0, heartbeat_timeout=15.0"
            )
        self.heartbeat_interval = heartbeat_interval  # 心跳发送间隔
        self.heartbeat_timeout = heartbeat_timeout    # 心跳超时时间（必须 > interval * 2）
        self.scanner_interval = scanner_interval      # Scanner 扫描间隔

        # 如果初始化时提供了task_center，直接挂载
        if task_center:
            self.mount_task_center(task_center)

        # Update prefixes with the configured prefix using colon namespace
        self.STATUS_PREFIX = f"{self.redis_prefix}:STATUS:"
        self.RESULT_PREFIX = f"{self.redis_prefix}:RESULT:"
        
        # 预编译常用操作，减少运行时开销
        self._loads = loads
        self._dumps = dumps
        
        # 调度器相关
        self.scheduler = None
        self._scheduler_db_url = None

        self._status_prefix = self.STATUS_PREFIX
        self._result_prefix = self.RESULT_PREFIX

        # Worker 状态管理器（延迟初始化）
        self.worker_state_manager = None

        # Worker 状态查询器（延迟初始化 - 需要 Redis 客户端）
        self._worker_state = None


        # 初始化清理状态，但不注册处理器
        self._cleanup_done = False
        self._should_exit = False
        self._worker_started = False
        self._handlers_registered = False

        # 队列注册表（懒加载）
        self._registry = None
        self._registry_initialized = False

        # 存储待注册的限流配置，延迟到start()方法中注册
        self._pending_rate_limits = {}
   
    
    def _load_config_from_task_center(self):
        """从任务中心加载配置"""
        try:
            import asyncio
            # 检查是否已经在事件循环中
            try:
                loop = asyncio.get_running_loop()
                # 已在事件循环中，无法同步加载
                return False
            except RuntimeError:
                # 不在事件循环中，可以创建新的
                loop = asyncio.new_event_loop()
                if self.task_center:
                    # 如果已经初始化，直接获取配置
                    if self.task_center._initialized:
                        config = self.task_center._config
                    else:
                        # 使用异步模式连接
                        success = loop.run_until_complete(self.task_center.connect(asyncio=True))
                        if success:
                            config = self.task_center._config
                        else:
                            config = None
                else:
                    config = None
                loop.close()
            
            if config:
                # 任务中心配置优先级高于手动配置
                redis_config = config.get('redis_config', {})
                pg_config = config.get('pg_config', {})
                # 构建Redis URL
                if redis_config:
                    redis_host = redis_config.get('host', 'localhost')
                    redis_port = redis_config.get('port', 6379)
                    redis_password = redis_config.get('password')
                    redis_db = redis_config.get('db', 0)
                    
                    if redis_password:
                        self.redis_url = f"redis://:{redis_password}@{redis_host}:{redis_port}/{redis_db}"
                    else:
                        self.redis_url = f"redis://{redis_host}:{redis_port}/{redis_db}"
                    
                    logger.debug(f"从任务中心加载Redis配置: {redis_host}:{redis_port}/{redis_db}")
                
                # 构建PostgreSQL URL
                if pg_config:
                    pg_host = pg_config.get('host', 'localhost')
                    pg_port = pg_config.get('port', 5432)
                    pg_user = pg_config.get('user', 'postgres')
                    pg_password = pg_config.get('password', '')
                    pg_database = pg_config.get('database', 'jettask')
                    
                    self.pg_url = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}"
                    logger.debug(f"从任务中心加载PostgreSQL配置: {pg_host}:{pg_port}/{pg_database}")
                
                # 保存配置供后续使用
                self._task_center_config = config
                
                # 更新Redis前缀为命名空间名称
                if self.task_center and self.task_center.redis_prefix != "jettask":
                    self.redis_prefix = self.task_center.redis_prefix
                    # 更新相关前缀
                    self.STATUS_PREFIX = f"{self.redis_prefix}:STATUS:"
                    self.RESULT_PREFIX = f"{self.redis_prefix}:RESULT:"
                
                # 清理已缓存的Redis连接，强制重新创建
                if hasattr(self, '_redis'):
                    delattr(self, '_redis')
                if hasattr(self, '_async_redis'):
                    delattr(self, '_async_redis')
                if hasattr(self, '_ep'):
                    delattr(self, '_ep')
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.warning(f"从任务中心加载配置失败，使用手动配置: {e}")
            # 恢复原始配置
            self.redis_url = self._original_redis_url
            self.pg_url = self._original_pg_url
    
    def mount_task_center(self, task_center):
        """
        挂载任务中心到Jettask应用
        
        如果task_center已经连接，会自动应用配置到当前app。
        
        Args:
            task_center: TaskCenter实例
            
        使用示例：
            from jettask.core.center_client import TaskCenterClient

            # 创建任务中心客户端（可复用）
            task_center = TaskCenterClient("http://localhost:8001")
            await task_center.connect()  # 只需连接一次
            
            # 创建多个app实例，共享同一个task_center
            app1 = Jettask()
            app1.mount_task_center(task_center)  # 自动应用配置
            
            app2 = Jettask()
            app2.mount_task_center(task_center)  # 复用配置
        """
        self.task_center = task_center
        
        # 如果任务中心已连接，立即应用所有配置
        if task_center and task_center._initialized:
            # 应用Redis配置
            if task_center.redis_config:
                redis_url = task_center.get_redis_url()
                if redis_url:
                    self.redis_url = redis_url
                    
            # 应用PostgreSQL配置
            if task_center.pg_config:
                pg_url = task_center.get_pg_url()
                if pg_url:
                    self.pg_url = pg_url
            
            # 更新Redis前缀
            self.redis_prefix = task_center.redis_prefix
            # 更新相关前缀
            self.STATUS_PREFIX = f"{self.redis_prefix}:STATUS:"
            self.RESULT_PREFIX = f"{self.redis_prefix}:RESULT:"
            self.QUEUE_PREFIX = f"{self.redis_prefix}:QUEUE:"
            self.STREAM_PREFIX = f"{self.redis_prefix}:STREAM:"
            self.TASK_PREFIX = f"{self.redis_prefix}:TASK:"
            self.SCHEDULER_PREFIX = f"{self.redis_prefix}:SCHEDULED:"
            self.LOCK_PREFIX = f"{self.redis_prefix}:LOCK:"
            
            # 标记配置已加载
            self._task_center_config = {
                'redis_config': task_center.redis_config,
                'pg_config': task_center.pg_config,
                'namespace_name': task_center.namespace_name,
                'version': task_center.version
            }
    
    
    def _setup_cleanup_handlers(self):
        """设置清理处理器"""
        # 避免重复注册
        if self._handlers_registered:
            return
        
        self._handlers_registered = True
        
        def signal_cleanup_handler(signum=None, frame=None):
            """信号处理器"""
            if self._cleanup_done:
                return
            # 只有启动过worker才需要打印清理信息
            if self._worker_started:
                logger.debug("Received shutdown signal, cleaning up...")
            self.cleanup()
            if signum:
                # 设置标记表示需要退出
                self._should_exit = True
                # 对于多进程环境，不直接操作事件循环
                # 让执行器自己检测退出标志并优雅关闭
        
        def atexit_cleanup_handler():
            """atexit处理器"""
            if self._cleanup_done:
                return
            # atexit时不重复打印日志，静默清理
            self.cleanup()
        
        # 注册信号处理器
        if hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, signal_cleanup_handler)
        if hasattr(signal, 'SIGINT'):
            signal.signal(signal.SIGINT, signal_cleanup_handler)
        
        # 注册atexit处理器
        import atexit
        atexit.register(atexit_cleanup_handler)
    
    def cleanup(self):
        """清理应用资源"""
        if self._cleanup_done:
            return
        self._cleanup_done = True
        
        # 只有真正启动过worker才打印日志
        if self._worker_started:
   
            
            # 清理EventPool
            if hasattr(self, 'ep') and self.ep:
                self.ep.cleanup()
            

        else:
            # 如果只是实例化但没有启动，静默清理
            if hasattr(self, 'ep') and self.ep:
                self.ep.cleanup()


    @property
    def async_redis(self):
        """获取异步Redis客户端（全局单例）"""
        # 如果配置了任务中心且还未加载配置，先加载配置
        if self.task_center and self.task_center.is_enabled and not self._task_center_config:
            self._load_config_from_task_center()

        # logger.debug(f"Creating async_redis client with socket_timeout=None for redis_url={self.redis_url}")
        return get_async_redis_client(
            redis_url=self.redis_url,
            decode_responses=True,
            max_connections=self.max_connections,
            socket_timeout=None  # 无限等待，不超时
        )

    @property
    def redis(self):
        """获取同步Redis客户端（全局单例）"""
        # 如果配置了任务中心且还未加载配置，先加载配置
        # if self.task_center and self.task_center.is_enabled and not self._task_center_config:
        #     self._load_config_from_task_center()

        return get_sync_redis_client(
            redis_url=self.redis_url,
            decode_responses=True,
            max_connections=self.max_connections
        )

    @property
    def binary_redis(self):
        """获取同步二进制Redis客户端（不自动解码，用于获取msgpack数据）"""
        return get_sync_redis_client(
            redis_url=self.redis_url,
            decode_responses=False,
            max_connections=self.max_connections
        )

    @property
    def async_binary_redis(self):
        """获取异步二进制Redis客户端（不自动解码，用于获取msgpack数据）"""
        return get_async_redis_client(
            redis_url=self.redis_url,
            decode_responses=False,
            max_connections=self.max_connections,
            socket_timeout=None
        )

    @property
    def worker_state(self):
        """
        获取 WorkerState 实例（单例，延迟初始化）

        WorkerManager 负责 Worker 状态的查询和管理
        """
        if self._worker_state is None:
            from jettask.worker.lifecycle import WorkerManager
            self._worker_state = WorkerManager(
                redis_client=self.redis,
                async_redis_client=self.async_redis,
                redis_prefix=self.redis_prefix
            )
            logger.debug("Initialized WorkerManager for app")
        return self._worker_state

    @property
    def ep(self):
        name = "_ep"
        if hasattr(self, name):
            ep = getattr(self, name)
        else:
            # 传递redis_prefix到consumer_config
            consumer_config = self.consumer_config.copy() if self.consumer_config else {}
            consumer_config['redis_prefix'] = self.redis_prefix

            # 创建必需的依赖
            # 注意：不传入 async_redis_client，让 EventPool 自己懒加载创建
            # 避免在子线程中触发异步客户端的创建

            # 对于只用于发送消息的 EventPool，不需要真正的 task_event_queues
            # 但为了满足接口要求，传递空字典
            task_event_queues = {}

            ep = EventPool(
                redis_client=self.redis,
                async_redis_client=None,  # 懒加载，避免子线程创建
                task_event_queues=task_event_queues,
                tasks=self._tasks,
                queue_registry=None,  # 使用懒加载的 registry 属性
                offline_recovery=self.worker_state_manager,  # offline_recovery - 使用 App 的 WorkerManager
                redis_url=self.redis_url,
                consumer_config=consumer_config,
                redis_prefix=self.redis_prefix,
                app=self
            )
            setattr(self, name, ep)
        return ep

    @property
    def registry(self):
        """获取 QueueRegistry 实例（懒加载）"""
        if self._registry_initialized and self._registry:
            return self._registry

        # 懒加载创建 QueueRegistry
        from ..messaging.registry import QueueRegistry

        self._registry = QueueRegistry(
            redis_client=self.redis,  # 传入同步客户端
            async_redis_client=self.async_redis,  # 传入异步客户端
            redis_prefix=self.redis_prefix
        )

        self._registry_initialized = True
        return self._registry

    def clear(self):
        if hasattr(self, "process"):
            delattr(self, "process")
        if hasattr(self, "_ep"):
            delattr(self, "_ep")
        if hasattr(self, "_registry"):
            self._registry = None
            self._registry_initialized = False

    def get_task_by_name(self, name: str) -> Task:
        # 1. 直接查找完整名称
        task = self._tasks.get(name)
        if task:
            return task
        
        # 2. 如果是简单名称（不含.），尝试匹配所有以该名称结尾的任务
        if '.' not in name:
            for task_key, task_obj in self._tasks.items():
                # 匹配 "module.function_name" 形式，提取函数名部分
                if '.' in task_key:
                    _, func_name = task_key.rsplit('.', 1)
                    if func_name == name:
                        return task_obj
                elif task_key == name:
                    # 完全匹配（可能没有模块前缀）
                    return task_obj
        
        return None

    def get_task_config(self, task_name: str) -> dict:
        """
        获取任务配置

        Args:
            task_name: 任务名称

        Returns:
            任务配置字典，如果任务不存在则返回None
        """
        # 获取任务对象
        task = self.get_task_by_name(task_name)
        if not task:
            return None

        # 返回任务的配置（从Task对象的属性中提取）
        return {
            'auto_ack': getattr(task, 'auto_ack', True),
            'queue': getattr(task, 'queue', None),
            'timeout': getattr(task, 'timeout', None),
            'max_retries': getattr(task, 'max_retries', 0),
            'retry_delay': getattr(task, 'retry_delay', None),
        }

    def include_module(self, modules: list):
        self.include += modules

    def _task_from_fun(
        self, fun, name=None, base=None, queue=None, bind=False, retry_config=None, rate_limit=None, auto_ack=True, **options
    ) -> Task:
        name = name or gen_task_name(fun.__name__, fun.__module__)
        base = base or Task

        # 不再限制队列模式，因为每个task都有独立的consumer group

        if name not in self._tasks:
            run = staticmethod(fun)
            task: Task = type(
                fun.__name__,
                (base,),
                dict(
                    {
                        "app": self,
                        "name": name,
                        "run": run,
                        "queue": queue,
                        "retry_config": retry_config,  # 存储重试配置
                        "rate_limit": rate_limit,  # 存储限流配置
                        "auto_ack": auto_ack,  # 存储自动ACK配置
                        "_decorated": True,
                        "__doc__": fun.__doc__,
                        "__module__": fun.__module__,
                        "__annotations__": fun.__annotations__,
                        "__wrapped__": run,
                    },
                    **options,
                ),
            )()
            task.bind_app(self)
            with contextlib.suppress(AttributeError):
                task.__qualname__ = fun.__qualname__
            self._tasks[task.name] = task

            # 记录任务到队列的映射 (task -> queue)
            if queue:
                self._task_queues[name] = queue

            # 如果任务配置了限流，注册到Redis；否则删除旧配置
            if rate_limit:
                # 支持 int (QPS) 和 ConcurrencyLimit/QPSLimit 对象
                if isinstance(rate_limit, int) and rate_limit > 0:
                    # 简单的 int 值作为 QPS 限制
                    self._register_rate_limit(name, rate_limit)
                elif hasattr(rate_limit, 'to_dict'):
                    # RateLimitConfig 对象（ConcurrencyLimit 或 QPSLimit）
                    self._register_rate_limit_config(name, rate_limit)
            else:
                # 没有限流配置，删除 Redis 中的旧配置（如果存在）
                from jettask.utils.rate_limit.limiter import RateLimiterManager

                RateLimiterManager.unregister_rate_limit_config(
                    redis_client=self.redis,
                    task_name=name,
                    redis_prefix=self.redis_prefix
                )
        else:
            task = self._tasks[name]
        return task

    def _register_rate_limit(self, task_name: str, qps_limit: int):
        """存储任务的 QPS 限流规则，延迟到 start() 时注册到 Redis"""
        from jettask.utils.rate_limit.config import QPSLimit

        # 转换为 QPSLimit 配置对象并存储
        config = QPSLimit(qps=qps_limit)
        self._pending_rate_limits[task_name] = config
        logger.debug(f"存储任务 {task_name} 的 QPS 限流配置，将在 start() 时注册")

    def _register_rate_limit_config(self, task_name: str, config):
        """存储任务的限流配置对象，延迟到 start() 时注册到 Redis

        Args:
            task_name: 任务名称
            config: RateLimitConfig 对象（ConcurrencyLimit 或 QPSLimit）
        """
        # 存储配置，延迟注册
        self._pending_rate_limits[task_name] = config
        logger.debug(f"存储任务 {task_name} 的限流配置，将在 start() 时注册")

    def _apply_pending_rate_limits(self):
        """将所有待注册的限流配置注册到 Redis（在 start() 时调用）"""
        if not self._pending_rate_limits:
            return

        from jettask.utils.rate_limit.limiter import RateLimiterManager

        for task_name, config in self._pending_rate_limits.items():
            try:
                RateLimiterManager.register_rate_limit_config(
                    redis_client=self.redis,
                    task_name=task_name,
                    config=config,
                    redis_prefix=self.redis_prefix
                )
                logger.debug(f"已注册任务 {task_name} 的限流配置")
            except Exception as e:
                logger.error(f"注册任务 {task_name} 的限流配置失败: {e}")

        logger.debug(f"已注册 {len(self._pending_rate_limits)} 个任务的限流配置")

    def _get_queues_from_tasks(self, task_names: List[str]) -> List[str]:
        """从任务名称列表获取对应的队列列表（使用 task -> queue 映射）

        Args:
            task_names: 任务名称列表

        Returns:
            队列名称列表（去重，保持顺序）

        Raises:
            ValueError: 如果某个任务不存在或没有指定队列
        """
        queues = []
        for task_name in task_names:
            # 检查任务是否存在
            if task_name not in self._task_queues:
                # 提供更友好的错误信息
                available_tasks = list(self._task_queues.keys())
                raise ValueError(
                    f"任务 '{task_name}' 不存在或未配置队列。\n"
                    f"已注册的任务: {', '.join(available_tasks) if available_tasks else '(无)'}"
                )

            # 从映射中获取队列
            queue = self._task_queues[task_name]

            # 去重
            if queue not in queues:
                queues.append(queue)

        logger.debug(f"从 {len(task_names)} 个任务获取到 {len(queues)} 个队列: {queues}")
        return queues

    def get_tasks_by_queue(self, queue_name: str) -> List[str]:
        """从队列名称获取关联的任务列表（反向查询）

        Args:
            queue_name: 队列名称

        Returns:
            任务名称列表
        """
        return [task_name for task_name, queue in self._task_queues.items() if queue == queue_name]

    def task(
        self,
        name: str = None,
        queue: str = None,
        base: Task = None,
        # 重试相关参数
        max_retries: int = 0,
        retry_backoff: bool = True,  # 是否使用指数退避
        retry_backoff_max: float = 60,  # 最大退避时间（秒）
        retry_on_exceptions: tuple = None,  # 可重试的异常类型
        # 限流相关参数
        rate_limit: int = None,  # QPS 限制（每秒允许执行的任务数）
        # ACK相关参数
        auto_ack: bool = True,  # 是否自动ACK（默认True）
        *args,
        **kwargs,
    ):
        """
        任务装饰器 - 统一使用 TaskRouter 内部实现

        Args:
            name: 任务名称
            queue: 队列名称
            base: 基类
            max_retries: 最大重试次数
            retry_backoff: 是否使用指数退避
            retry_backoff_max: 最大退避时间
            retry_on_exceptions: 可重试的异常类型
            rate_limit: 限流配置（QPS或RateLimitConfig对象）
            auto_ack: 是否自动ACK（默认True）
        """
        def _create_task_cls(fun):
            # 将重试配置传递给_task_from_fun
            retry_config = None
            if max_retries > 0:
                retry_config = {
                    'max_retries': max_retries,
                    'retry_backoff': retry_backoff,
                    'retry_backoff_max': retry_backoff_max,
                }
                # 将异常类转换为类名字符串，以便序列化
                if retry_on_exceptions:
                    retry_config['retry_on_exceptions'] = [
                        exc if isinstance(exc, str) else exc.__name__
                        for exc in retry_on_exceptions
                    ]

            # 统一通过 _task_from_fun 创建任务，包含 auto_ack 参数
            return self._task_from_fun(
                fun,
                name,
                base,
                queue,
                retry_config=retry_config,
                rate_limit=rate_limit,
                auto_ack=auto_ack,  # 传递 auto_ack
                *args,
                **kwargs
            )

        return _create_task_cls
    
    def include_router(self, router, prefix: str = None):
        """
        包含一个TaskRouter，将其所有任务注册到app中
        
        Args:
            router: TaskRouter实例
            prefix: 额外的前缀（可选）
        """
        from ..task.router import TaskRouter
        
        if not isinstance(router, TaskRouter):
            raise TypeError(f"Expected TaskRouter, got {type(router)}")
        
        # 获取router中的所有任务
        tasks = router.get_tasks()
        
        for task_name, task_config in tasks.items():
            # 复制配置，避免修改原始数据
            config = task_config.copy()
            
            # 如果指定了额外前缀，添加到任务名前面
            if prefix:
                if config.get('name'):
                    config['name'] = f"{prefix}.{config['name']}"
                else:
                    config['name'] = f"{prefix}.{task_name}"
            
            # 获取任务函数和配置
            func = config.pop('func')
            name = config.pop('name', task_name)
            queue = config.pop('queue', None)
            
            # 提取重试相关参数
            retry_config = {}
            if 'max_retries' in config:
                retry_config['max_retries'] = config.pop('max_retries', 0)
            if 'retry_delay' in config:
                retry_config['retry_backoff_max'] = config.pop('retry_delay', 60)
            
            # 注册任务到app
            self._task_from_fun(
                func,
                name=name,
                queue=queue,
                retry_config=retry_config if retry_config else None,
                **config
            )
    
    def send_tasks(self, messages: list, asyncio: bool = False):
        """
        统一的任务发送接口 - 支持同步和异步

        Args:
            messages: TaskMessage对象列表（或字典列表）
            asyncio: 是否使用异步模式（默认False）

        Returns:
            同步模式: List[str] - 任务ID列表
            异步模式: 返回协程，需要使用 await

        使用示例:
            from jettask.core.message import TaskMessage

            # 同步发送
            msg = TaskMessage(
                queue="order_processing",
                args=(12345,),
                kwargs={"customer_id": "C001", "amount": 99.99}
            )
            task_ids = app.send_tasks([msg])

            # 异步发送
            task_ids = await app.send_tasks([msg], asyncio=True)

            # 批量发送
            messages = [
                TaskMessage(queue="email", kwargs={"to": "user1@example.com"}),
                TaskMessage(queue="email", kwargs={"to": "user2@example.com"}),
                TaskMessage(queue="sms", kwargs={"phone": "123456789"}),
            ]
            task_ids = app.send_tasks(messages)

            # 跨项目发送（不需要task定义）
            messages = [
                TaskMessage(queue="remote_queue", kwargs={"data": "value"})
            ]
            task_ids = await app.send_tasks(messages, asyncio=True)
        """
        if asyncio:
            return self._send_tasks_async(messages)
        else:
            return self._send_tasks_sync(messages)

    def ack(self, ack_items: list):
        """
        批量确认消息（ACK）

        用于 auto_ack=False 的任务，手动批量确认消息。
        这是同步方法，会在后台异步执行ACK操作。

        Args:
            ack_items: ACK项列表，每项可以是：
                - (queue, event_id): 简单形式
                - (queue, event_id, group_name): 带消费者组名
                - (queue, event_id, group_name, offset): 完整形式
                - dict: {'queue': ..., 'event_id': ..., 'group_name': ..., 'offset': ...}

        Example:
            from jettask import TaskRouter

            router = TaskRouter()

            @router.task(queue="batch_queue", auto_ack=False)
            async def process_batch(ctx, items):
                # 批量处理
                results = []
                ack_list = []

                for item in items:
                    try:
                        result = await process_item(item)
                        results.append(result)

                        # 收集需要ACK的消息
                        ack_list.append((
                            ctx.queue,
                            item['event_id'],
                            ctx.group_name,
                            item.get('offset')
                        ))
                    except Exception as e:
                        logger.error(f"Failed to process {item}: {e}")

                # 批量确认成功处理的消息
                ctx.app.ack(ack_list)

                return results
        """
        if not ack_items:
            return

        # 检查是否有 executor_core（Worker运行时才有）
        if not hasattr(self, '_executor_core') or not self._executor_core:
            logger.warning("ACK can only be called in worker context")
            return

        # 将ACK项添加到executor_core的pending_acks
        for item in ack_items:
            if isinstance(item, dict):
                queue = item['queue']
                event_id = item['event_id']
                group_name = item.get('group_name')
                offset = item.get('offset')
            elif isinstance(item, (tuple, list)):
                if len(item) >= 3:
                    queue, event_id, group_name = item[0], item[1], item[2]
                    offset = item[3] if len(item) > 3 else None
                elif len(item) == 2:
                    # 🔧 不再支持只有 (queue, event_id) 的简化形式
                    logger.error(
                        f"Invalid ACK item format: {item}. "
                        f"group_name is required. Use (queue, event_id, group_name) or ctx.acks([event_ids])"
                    )
                    continue
                else:
                    logger.error(f"Invalid ACK item format: {item}")
                    continue
            else:
                logger.error(f"Invalid ACK item type: {type(item)}")
                continue

            # 🔧 检查 group_name 是否提供
            if not group_name:
                logger.error(
                    f"group_name is required for ACK. item={item}. "
                    f"Use ctx.acks([event_ids]) for automatic group_name injection."
                )
                continue

            # 添加到pending_acks
            self._executor_core.pending_acks.append((queue, event_id, group_name, offset))
            logger.debug(f"Added to pending_acks: queue={queue}, event_id={event_id}, group_name={group_name}")

        # 检查是否需要立即刷新
        # 检查是否需要立即刷新
        if len(self._executor_core.pending_acks) >= 100:
            # 创建异步任务刷新
            import asyncio
            try:
                loop = asyncio.get_running_loop()
                asyncio.create_task(self._executor_core._flush_all_buffers())
            except RuntimeError:
                # 不在事件循环中，稍后会自动刷新
                pass

    def _send_tasks_sync(self, messages: list):
        """同步发送任务"""
        if not messages:
            return []

        results = []

        # 按队列分组消息，以便批量处理
        queue_messages = {}
        for msg in messages:
            # 支持TaskMessage对象或字典
            if isinstance(msg, dict):
                msg = TaskMessage.from_dict(msg)
            elif not isinstance(msg, TaskMessage):
                raise ValueError(f"Invalid message type: {type(msg)}. Expected TaskMessage or dict")

            # 验证消息
            msg.validate()

            # 确定实际的队列名（考虑优先级）
            actual_queue = msg.queue
            if msg.priority is not None:
                # 将优先级拼接到队列名后面
                actual_queue = f"{msg.queue}:{msg.priority}"
                # 更新消息体中的queue字段，确保与实际发送的stream key一致
                msg.queue = actual_queue

            # 按队列分组
            if actual_queue not in queue_messages:
                queue_messages[actual_queue] = []
            queue_messages[actual_queue].append(msg)

        # 处理每个队列的消息
        for queue, queue_msgs in queue_messages.items():
            batch_results = self._send_batch_messages_sync(queue, queue_msgs)
            results.extend(batch_results)

        return results

    async def _send_tasks_async(self, messages: list):
        """异步发送任务"""
        if not messages:
            return []

        results = []

        # 按队列分组消息，以便批量处理
        queue_messages = {}
        for msg in messages:
            # 支持TaskMessage对象或字典
            if isinstance(msg, dict):
                msg = TaskMessage.from_dict(msg)
            elif not isinstance(msg, TaskMessage):
                raise ValueError(f"Invalid message type: {type(msg)}. Expected TaskMessage or dict")

            # 验证消息
            msg.validate()

            # 确定实际的队列名（考虑优先级）
            actual_queue = msg.queue
            if msg.priority is not None:
                # 将优先级拼接到队列名后面
                actual_queue = f"{msg.queue}:{msg.priority}"
                # 更新消息体中的queue字段，确保与实际发送的stream key一致
                msg.queue = actual_queue

            # 按队列分组
            if actual_queue not in queue_messages:
                queue_messages[actual_queue] = []
            queue_messages[actual_queue].append(msg)

        # 处理每个队列的消息
        for queue, queue_msgs in queue_messages.items():
            batch_results = await self._send_batch_messages_async(queue, queue_msgs)
            results.extend(batch_results)

        return results
    
    def _send_batch_messages_sync(self, queue: str, messages: list) -> list:
        """批量发送任务（同步）

        注意：延迟任务现在也直接发送到普通队列，由TaskExecutor中的AsyncDelayQueue处理延迟
        """
        from ..utils.serializer import dumps_str

        # 所有消息（包括延迟任务）都发送到普通队列
        all_messages = []

        for msg in messages:
            msg_dict = msg.to_dict()

            # 处理延迟任务：添加 execute_at 标记，但不写入 DELAYED_QUEUE
            if msg.delay and msg.delay > 0:
                current_time = time.time()
                msg_dict['execute_at'] = current_time + msg.delay
                msg_dict['is_delayed'] = 1

            all_messages.append(msg_dict)

        results = []

        # 批量发送所有任务到普通队列（包括延迟任务）
        if all_messages:
            batch_results = self.ep._batch_send_event_sync(
                self.ep.get_prefixed_queue_name(queue),
                [{'data': dumps_str(msg)} for msg in all_messages],
                self.ep.get_redis_client(asyncio=False, binary=True).pipeline()
            )
            results.extend(batch_results)

        return results

    async def _send_batch_messages_async(self, queue: str, messages: list) -> list:
        """批量发送任务（异步）

        注意：延迟任务现在也直接发送到普通队列，由TaskExecutor中的AsyncDelayQueue处理延迟
        """
        from ..utils.serializer import dumps_str

        # 所有消息（包括延迟任务）都发送到普通队列
        all_messages = []

        for msg in messages:
            msg_dict = msg.to_dict()

            # 处理延迟任务：添加 execute_at 标记，但不写入 DELAYED_QUEUE
            if msg.delay and msg.delay > 0:
                current_time = time.time()
                msg_dict['execute_at'] = current_time + msg.delay
                msg_dict['is_delayed'] = 1

            all_messages.append(msg_dict)

        results = []
        # 批量发送所有任务到普通队列（包括延迟任务）
        if all_messages:
            batch_results = await self.ep._batch_send_event(
                self.ep.get_prefixed_queue_name(queue),
                [{'data': dumps_str(msg)} for msg in all_messages],
                self.ep.get_redis_client(asyncio=True, binary=True).pipeline()
            )
            results.extend(batch_results)

        return results

    def _get_task_names_from_queue(self, queue: str, task_name: str = None) -> list:
        """获取队列的任务名列表

        Args:
            queue: 队列名称（可能包含优先级后缀）
            task_name: 可选的任务名，如果提供则直接返回 [task_name]

        Returns:
            任务名列表，如果 task_name 提供则返回 [task_name]，否则返回队列的所有任务名
        """
        if task_name is not None:
            return [task_name]

        # 从 base_queue 中提取基础队列名（去掉优先级）
        base_queue = queue.split(':')[0] if ':' in queue else queue

        # 使用异步方法获取任务名
        import asyncio
        try:
            # 尝试在当前事件循环中运行
            loop = asyncio.get_running_loop()
            # 如果已经在事件循环中，创建一个任务
            task_names = asyncio.create_task(self.registry.get_task_names_by_queue(base_queue))
            # 注意：这里无法等待，需要调用者处理
            # 这种情况不应该发生，因为这是同步方法
            raise RuntimeError("Cannot call sync method from async context")
        except RuntimeError:
            # 没有运行中的事件循环，创建新的
            task_names = asyncio.run(self.registry.get_task_names_by_queue(base_queue))

        return list(task_names) if task_names else []

    def get_result(self, event_id: str, queue: str, task_name: str = None,
                   delete: bool = False, asyncio: bool = False,
                   delayed_deletion_ex: int = None, wait: bool = False,
                   timeout: int = 300, poll_interval: float = 0.5):
        """获取任务执行结果

        在任务组架构下，每个任务都有独立的执行结果存储。
        结果存储格式: {redis_prefix}:TASK:{event_id}:{group_name}

        这个方法支持完全解耦的生产者-消费者模式，生产者只需要知道：
        - event_id: 发送任务时返回的事件ID
        - queue: 队列名称
        - task_name: 任务名称（可选，不提供时会获取该队列所有任务的结果）

        Args:
            event_id: 任务事件ID（发送任务时返回的消息ID）
            queue: 队列名称
            task_name: 任务名称（可选）。如果不提供，会获取该队列所有任务的结果，返回列表
            delete: 是否删除结果（默认False）
            asyncio: 是否使用异步模式（默认False）
            delayed_deletion_ex: 延迟删除时间（秒），设置后会在指定时间后自动删除
            wait: 是否阻塞等待直到任务完成（默认False）
            timeout: 等待超时时间（秒），默认300秒
            poll_interval: 轮询间隔（秒），默认0.5秒

        Returns:
            当指定task_name时:
                同步模式: 任务结果（字符串或字节），如果任务未完成返回None
                异步模式: 返回协程，需要使用 await
            当不指定task_name时:
                返回列表，每个元素是字典: [{"task_name": "xxx", "result": ..., "status": ...}, ...]

        Raises:
            TaskTimeoutError: 等待超时
            TaskExecutionError: 任务执行失败
            TaskNotFoundError: 任务不存在

        Examples:
            # 获取单个任务结果
            result = app.get_result("1234567890-0", "my_queue", task_name="my_task")

            # 获取队列中所有任务的结果
            results = app.get_result("1234567890-0", "my_queue")
            # 返回: [{"task_name": "task1", "result": ..., "status": ...}, {"task_name": "task2", ...}]

            # 异步获取所有任务结果
            results = await app.get_result("1234567890-0", "my_queue", asyncio=True)
        """
        # 判断是否指定了 task_name，决定最终返回格式
        return_single = task_name is not None

        # 获取需要查询的任务名列表
        task_names = self._get_task_names_from_queue(queue, task_name)

        # 如果没有任务，直接返回空列表
        if not task_names:
            if asyncio:
                async def _return_empty_list():
                    return []
                return _return_empty_list()
            else:
                return []

        # 统一处理：遍历所有任务获取结果
        if asyncio:
            return self._get_results_async(event_id, queue, task_names, delete,
                                          delayed_deletion_ex, wait, timeout, poll_interval, return_single)
        else:
            return self._get_results_sync(event_id, queue, task_names, delete,
                                         delayed_deletion_ex, wait, timeout, poll_interval, return_single)

    def get_queue_position(self, event_id: str, queue: str, task_name: str = None, asyncio: bool = False):
        """获取任务在队列中的排队情况

        通过 event_id 查询任务在队列中的排队位置，包括：
        - 距离被读取还差多少任务
        - 距离被消费还差多少任务

        Args:
            event_id: 任务事件ID（发送任务时返回的消息ID）
            queue: 队列名称
            task_name: 任务名称（可选）。如果不提供，会获取该队列所有任务的排队情况
            asyncio: 是否使用异步模式（默认False）

        Returns:
            当指定task_name时:
                返回字典: {
                    "task_name": "xxx",
                    "task_offset": 12,
                    "read_offset": 14,
                    "task_ack_offset": 10,
                    "pending_read": 2,      # 距离被读取还差2个任务
                    "pending_consume": -2   # 已经被消费了（负数表示已完成）
                }
            当不指定task_name时:
                返回列表，每个元素是上述格式的字典

        Note:
            排名信息反映的是任务的发送顺序（offset），而不是执行顺序。
            在并发执行的场景下，排名靠后的任务可能先执行完成，而排名靠前的任务可能还在执行中。

            例如：
            - 任务A (offset=10) 和任务B (offset=15) 同时被读取
            - 如果任务B执行得快，可能会先完成
            - 此时任务A的 pending_consume 可能仍为正数（还未消费确认）
            - 而任务B的 pending_consume 已经变为负数（已完成）

            因此：
            - pending_read 表示有多少任务在你之前被发送到队列
            - pending_consume 表示有多少任务在你之前被消费确认（不代表执行顺序）
            - 负数的 pending_consume 只表示该任务已被确认，不表示所有前面的任务都已完成

        Examples:
            # 获取单个任务的排队情况
            position = app.get_queue_position("1234567890-0", "my_queue", task_name="my_task")

            # 获取队列中所有任务的排队情况
            positions = app.get_queue_position("1234567890-0", "my_queue")

            # 异步获取
            position = await app.get_queue_position("1234567890-0", "my_queue", asyncio=True)
        """
        # 判断是否指定了 task_name，决定最终返回格式
        return_single = task_name is not None

        # 获取需要查询的任务名列表
        task_names = self._get_task_names_from_queue(queue, task_name)

        # 如果没有任务，直接返回空列表
        if not task_names:
            if asyncio:
                async def _return_empty_list():
                    return []
                return _return_empty_list()
            else:
                return []

        # 统一处理：遍历所有任务获取排队情况
        if asyncio:
            return self._get_queue_positions_async(event_id, queue, task_names, return_single)
        else:
            return self._get_queue_positions_sync(event_id, queue, task_names, return_single)

    def _get_queue_positions_sync(self, event_id: str, queue: str, task_names: list, return_single: bool):
        """同步获取任务排队情况"""
        results = []

        # 构建 stream key
        prefixed_queue = f"{self.redis_prefix}:QUEUE:{queue}"

        # 从 stream 中获取任务数据
        try:
            # XRANGE 获取指定 event_id 的消息
            stream_data = self.binary_redis.xrange(prefixed_queue, min=event_id, max=event_id, count=1)

            if not stream_data:
                # 任务不存在于 stream 中
                for task_name in task_names:
                    results.append({
                        "task_name": task_name,
                        "error": "Task not found in stream"
                    })
                if return_single:
                    return results[0] if results else None
                return results

            # 解析 stream 数据
            message_id, message_data = stream_data[0]

            # 解码字段
            task_offset = None
            for key, value in message_data.items():
                if isinstance(key, bytes):
                    key = key.decode('utf-8')
                if key == 'offset':
                    if isinstance(value, bytes):
                        task_offset = int(value.decode('utf-8'))
                    else:
                        task_offset = int(value)
                    break

            if task_offset is None:
                for task_name in task_names:
                    results.append({
                        "task_name": task_name,
                        "error": "Offset not found in task data"
                    })
                if return_single:
                    return results[0] if results else None
                return results

        except Exception as e:
            for task_name in task_names:
                results.append({
                    "task_name": task_name,
                    "error": f"Failed to read from stream: {str(e)}"
                })
            if return_single:
                return results[0] if results else None
            return results

        # 获取 READ_OFFSETS 和 TASK_OFFSETS（使用 pipeline + HMGET 优化）
        read_offsets_key = f"{self.redis_prefix}:READ_OFFSETS"
        task_offsets_key = f"{self.redis_prefix}:TASK_OFFSETS"

        # 提取基础队列名（去掉优先级）
        base_queue = queue.split(':')[0] if ':' in queue else queue

        # 构建需要查询的字段列表
        offset_keys = [f"{base_queue}:{task_name}" for task_name in task_names]

        try:
            # 使用 pipeline 批量获取所有需要的字段
            pipeline = self.redis.pipeline()
            pipeline.hmget(read_offsets_key, offset_keys)
            pipeline.hmget(task_offsets_key, offset_keys)
            read_offsets_list, task_offsets_list = pipeline.execute()
        except Exception as e:
            for task_name in task_names:
                results.append({
                    "task_name": task_name,
                    "error": f"Failed to read offsets: {str(e)}"
                })
            if return_single:
                return results[0] if results else None
            return results

        # 对每个任务计算排队情况
        for idx, task_name in enumerate(task_names):
            # 获取 read_offset
            read_offset = read_offsets_list[idx]
            if read_offset is not None:
                read_offset = int(read_offset)

            # 获取 task_ack_offset
            task_ack_offset = task_offsets_list[idx]
            if task_ack_offset is not None:
                task_ack_offset = int(task_ack_offset)

            # 计算排队情况
            # pending_read: 正数表示还差多少个任务才能被读取，0表示刚好被读取，负数表示已被读取
            pending_read = (task_offset - read_offset) if read_offset is not None else None
            # pending_consume: 正数表示还差多少个任务才能被消费，0表示刚好被消费，负数表示已被消费
            pending_consume = (task_offset - task_ack_offset) if task_ack_offset is not None else None

            results.append({
                "task_name": task_name,
                "task_offset": task_offset,
                "read_offset": read_offset,
                "task_ack_offset": task_ack_offset,
                "pending_read": pending_read,
                "pending_consume": pending_consume
            })

        # 根据 return_single 决定返回格式
        if return_single:
            return results[0] if results else None
        return results

    async def _get_queue_positions_async(self, event_id: str, queue: str, task_names: list, return_single: bool):
        """异步获取任务排队情况"""
        results = []

        # 构建 stream key
        prefixed_queue = f"{self.redis_prefix}:QUEUE:{queue}"

        # 从 stream 中获取任务数据
        try:
            # XRANGE 获取指定 event_id 的消息
            stream_data = await self.async_binary_redis.xrange(prefixed_queue, min=event_id, max=event_id, count=1)

            if not stream_data:
                # 任务不存在于 stream 中
                for task_name in task_names:
                    results.append({
                        "task_name": task_name,
                        "error": "Task not found in stream"
                    })
                if return_single:
                    return results[0] if results else None
                return results

            # 解析 stream 数据
            message_id, message_data = stream_data[0]

            # 解码字段
            task_offset = None
            for key, value in message_data.items():
                if isinstance(key, bytes):
                    key = key.decode('utf-8')
                if key == 'offset':
                    if isinstance(value, bytes):
                        task_offset = int(value.decode('utf-8'))
                    else:
                        task_offset = int(value)
                    break

            if task_offset is None:
                for task_name in task_names:
                    results.append({
                        "task_name": task_name,
                        "error": "Offset not found in task data"
                    })
                if return_single:
                    return results[0] if results else None
                return results

        except Exception as e:
            for task_name in task_names:
                results.append({
                    "task_name": task_name,
                    "error": f"Failed to read from stream: {str(e)}"
                })
            if return_single:
                return results[0] if results else None
            return results

        # 获取 READ_OFFSETS 和 TASK_OFFSETS（使用 pipeline + HMGET 优化）
        read_offsets_key = f"{self.redis_prefix}:READ_OFFSETS"
        task_offsets_key = f"{self.redis_prefix}:TASK_OFFSETS"

        # 提取基础队列名（去掉优先级）
        base_queue = queue.split(':')[0] if ':' in queue else queue

        # 构建需要查询的字段列表
        offset_keys = [f"{base_queue}:{task_name}" for task_name in task_names]

        try:
            # 使用 pipeline 批量获取所有需要的字段
            pipeline = self.async_redis.pipeline()
            pipeline.hmget(read_offsets_key, offset_keys)
            pipeline.hmget(task_offsets_key, offset_keys)
            read_offsets_list, task_offsets_list = await pipeline.execute()
        except Exception as e:
            for task_name in task_names:
                results.append({
                    "task_name": task_name,
                    "error": f"Failed to read offsets: {str(e)}"
                })
            if return_single:
                return results[0] if results else None
            return results

        # 对每个任务计算排队情况
        for idx, task_name in enumerate(task_names):
            # 获取 read_offset
            read_offset = read_offsets_list[idx]
            if read_offset is not None:
                read_offset = int(read_offset)

            # 获取 task_ack_offset
            task_ack_offset = task_offsets_list[idx]
            if task_ack_offset is not None:
                task_ack_offset = int(task_ack_offset)

            # 计算排队情况
            # pending_read: 正数表示还差多少个任务才能被读取，0表示刚好被读取，负数表示已被读取
            pending_read = (task_offset - read_offset) if read_offset is not None else None
            # pending_consume: 正数表示还差多少个任务才能被消费，0表示刚好被消费，负数表示已被消费
            pending_consume = (task_offset - task_ack_offset) if task_ack_offset is not None else None

            results.append({
                "task_name": task_name,
                "task_offset": task_offset,
                "read_offset": read_offset,
                "task_ack_offset": task_ack_offset,
                "pending_read": pending_read,
                "pending_consume": pending_consume
            })

        # 根据 return_single 决定返回格式
        if return_single:
            return results[0] if results else None
        return results

    def _build_task_key(self, task_name: str, queue: str, event_id: str):
        """构建任务的 key 信息

        Returns:
            tuple: (group_name, full_key)
        """
        prefixed_queue = f"{self.redis_prefix}:QUEUE:{queue}"
        group_name = f"{prefixed_queue}:{task_name}"
        status_key = f"{event_id}:{group_name}"
        full_key = f"{self.redis_prefix}:TASK:{status_key}"
        return group_name, full_key

    @staticmethod
    def _decode_bytes(value):
        """解码字节为字符串"""
        if value and isinstance(value, bytes):
            return value.decode('utf-8')
        return value

    @staticmethod
    def _is_task_completed(status):
        """检查任务是否已完成（成功）"""
        return status in [TaskStatus.COMPLETED.value, TaskStatus.SUCCESS.value]

    @staticmethod
    def _is_task_failed(status):
        """检查任务是否失败"""
        return status in [TaskStatus.ERROR.value, TaskStatus.FAILED.value, "ERROR", "FAILED", "error", "failed"]

    def _get_results_sync(self, event_id: str, queue: str, task_names: list,
                         delete: bool, delayed_deletion_ex: int, wait: bool,
                         timeout: int, poll_interval: float, return_single: bool):
        """同步获取任务结果（支持单个或批量）"""
        results = []

        for task_name in task_names:
            try:
                _, full_key = self._build_task_key(task_name, queue, event_id)

                # 统一调用 _get_result_sync，通过 wait 参数控制行为
                task_info = self._get_result_sync(full_key, event_id, delete, delayed_deletion_ex,
                                                  wait, timeout, poll_interval)

                # 如果任务不存在
                if not task_info:
                    results.append({
                        "task_name": task_name,
                        "status": None,
                        "result": None
                    })
                else:
                    # 添加 task_name 到结果中
                    task_info["task_name"] = task_name
                    results.append(task_info)

            except Exception as e:
                results.append({
                    "task_name": task_name,
                    "status": "ERROR",
                    "result": None,
                    "error_msg": str(e)
                })

        # 根据 return_single 决定返回格式
        if return_single:
            return results[0] if results else None
        return results

    async def _get_results_async(self, event_id: str, queue: str, task_names: list,
                                 delete: bool, delayed_deletion_ex: int, wait: bool,
                                 timeout: int, poll_interval: float, return_single: bool):
        """异步获取任务结果（支持单个或批量）"""
        results = []

        for task_name in task_names:
            try:
                _, full_key = self._build_task_key(task_name, queue, event_id)

                # 统一调用 _get_result_async，通过 wait 参数控制行为
                task_info = await self._get_result_async(full_key, event_id, delete, delayed_deletion_ex,
                                                         wait, timeout, poll_interval)

                # 如果任务不存在
                if not task_info:
                    results.append({
                        "task_name": task_name,
                        "status": TaskStatus.PENDING.value,
                        "result": None
                    })
                else:
                    # 添加 task_name 到结果中
                    task_info["task_name"] = task_name
                    results.append(task_info)

            except Exception as e:
                results.append({
                    "task_name": task_name,
                    "status": "ERROR",
                    "result": None,
                    "error_msg": str(e)
                })

        # 根据 return_single 决定返回格式
        if return_single:
            return results[0] if results else None
        return results

    def _get_result_sync(self, full_key: str, event_id: str, delete: bool, delayed_deletion_ex: int,
                         wait: bool = False, timeout: int = 300, poll_interval: float = 0.5):
        """同步获取任务结果（支持等待模式）"""
        from ..exceptions import TaskTimeoutError, TaskExecutionError, TaskNotFoundError

        # 使用二进制客户端，不自动解码（因为 result 是 msgpack 序列化的）
        client = self.binary_redis
        start_time = time.time()

        while True:
            # 获取整个 hash 的所有字段
            task_data = client.hgetall(full_key)

            if not task_data:
                if wait:
                    raise TaskNotFoundError(f"Task {event_id} not found")
                return None

            # 解码字节字段
            decoded_data = {}
            for key, value in task_data.items():
                # 解码 key
                if isinstance(key, bytes):
                    key = key.decode('utf-8')

                # 跳过内部标记字段
                if key.startswith('__'):
                    continue

                # 解码 value - 只有 result 字段需要 loads_str
                if isinstance(value, bytes):
                    if key == 'result':
                        try:
                            decoded_data[key] = loads_str(value)
                        except Exception:
                            decoded_data[key] = value
                    else:
                        # 其他字段尝试 UTF-8 解码
                        try:
                            decoded_data[key] = value.decode('utf-8')
                        except Exception:
                            decoded_data[key] = value
                else:
                    decoded_data[key] = value

            # 如果不需要等待，处理删除逻辑后直接返回
            if not wait:
                if delayed_deletion_ex is not None:
                    client.expire(full_key, delayed_deletion_ex)
                elif delete:
                    if self.task_center and self.task_center.is_enabled:
                        client.hset(full_key, "__pending_delete", "1")
                    else:
                        client.delete(full_key)
                return decoded_data

            # 需要等待：检查任务状态
            status = decoded_data.get('status')

            # 检查任务是否完成
            if self._is_task_completed(status):
                # 任务成功完成，处理删除逻辑后返回
                if delayed_deletion_ex is not None:
                    client.expire(full_key, delayed_deletion_ex)
                elif delete:
                    if self.task_center and self.task_center.is_enabled:
                        client.hset(full_key, "__pending_delete", "1")
                    else:
                        client.delete(full_key)
                return decoded_data

            elif self._is_task_failed(status):
                # 任务失败，抛出异常
                error_msg = decoded_data.get('error_msg', 'Task execution failed')
                raise TaskExecutionError(event_id, error_msg)

            # 检查超时
            if time.time() - start_time > timeout:
                raise TaskTimeoutError(f"Task {event_id} timed out after {timeout} seconds")

            # 任务仍在执行中，等待后重试
            time.sleep(poll_interval)

    async def _get_result_async(self, full_key: str, event_id: str, delete: bool, delayed_deletion_ex: int,
                                wait: bool = False, timeout: int = 300, poll_interval: float = 0.5):
        """异步获取任务结果（支持等待模式）"""

        # 使用二进制客户端，不自动解码（因为 result 是 msgpack 序列化的）
        client = self.async_binary_redis
        start_time = time.time()

        while True:
            # 获取整个 hash 的所有字段
            task_data = await client.hgetall(full_key)

            if not task_data:
                if wait:
                    raise TaskNotFoundError(f"Task {event_id} not found")
                return None

            # 解码字节字段
            decoded_data = {}
            for key, value in task_data.items():
                # 解码 key
                if isinstance(key, bytes):
                    key = key.decode('utf-8')

                # 跳过内部标记字段
                if key.startswith('__'):
                    continue

                # 解码 value - 只有 result 字段需要 loads_str
                if isinstance(value, bytes):
                    if key == 'result':
                        try:
                            decoded_data[key] = loads_str(value)
                        except Exception:
                            decoded_data[key] = value
                    else:
                        # 其他字段尝试 UTF-8 解码
                        try:
                            decoded_data[key] = value.decode('utf-8')
                        except Exception:
                            decoded_data[key] = value
                else:
                    decoded_data[key] = value

            # 如果不需要等待，处理删除逻辑后直接返回
            if not wait:
                if delayed_deletion_ex is not None:
                    await client.expire(full_key, delayed_deletion_ex)
                elif delete:
                    if self.task_center and self.task_center.is_enabled:
                        await client.hset(full_key, "__pending_delete", "1")
                    else:
                        await client.delete(full_key)
                return decoded_data

            # 需要等待：检查任务状态
            status = decoded_data.get('status')

            # 检查任务是否完成
            if self._is_task_completed(status):
                # 任务成功完成，处理删除逻辑后返回
                if delayed_deletion_ex is not None:
                    await client.expire(full_key, delayed_deletion_ex)
                elif delete:
                    if self.task_center and self.task_center.is_enabled:
                        await client.hset(full_key, "__pending_delete", "1")
                    else:
                        await client.delete(full_key)
                return decoded_data

            elif self._is_task_failed(status):
                # 任务失败，抛出异常
                error_msg = decoded_data.get('error_msg', 'Task execution failed')
                raise TaskExecutionError(event_id, error_msg)

            # 检查超时
            if time.time() - start_time > timeout:
                raise TaskTimeoutError(f"Task {event_id} timed out after {timeout} seconds")

            # 等待后重试
            await asyncio.sleep(poll_interval)

    def register_router(self, router, prefix: str = None):
        """
        注册任务路由器
        
        Args:
            router: TaskRouter实例
            prefix: 额外的前缀（可选）
        
        使用示例：
            from jettask import Jettask, TaskRouter
            
            # 创建路由器
            email_router = TaskRouter(prefix="email", queue="emails")
            
            @email_router.task()
            async def send_email(to: str):
                pass
            
            # 注册到主应用
            app = Jettask(redis_url="redis://localhost:6379/0")
            app.register_router(email_router)
        """
        from ..task.router import TaskRouter
        
        if not isinstance(router, TaskRouter):
            raise TypeError("router must be a TaskRouter instance")
        
        # 注册所有任务
        for task_name, task_config in router.get_tasks().items():
            # 如果指定了额外前缀，添加到任务名
            if prefix:
                if task_config.get('name'):
                    task_config['name'] = f"{prefix}.{task_config['name']}"
                task_name = f"{prefix}.{task_name}"
            
            # 获取任务函数
            func = task_config.pop('func')
            name = task_config.pop('name', task_name)
            queue = task_config.pop('queue', None)
            
            # 注册任务
            task = self._task_from_fun(func, name, None, queue, **task_config)
            logger.debug(f"Registered task: {name} (queue: {queue or self.redis_prefix})")
        
        return self

    def _mount_module(self):
        for module in self.include:
            module = importlib.import_module(module)
            for attr_name in dir(module):
                obj = getattr(module, attr_name)
                if hasattr(obj, "app"):
                    self._tasks.update(getattr(obj, "app")._tasks)

    def _validate_tasks_for_executor(self, execute_type: str, queues: List[str]):
        """验证任务类型是否与执行器兼容"""
        if execute_type in ["asyncio", "multi_asyncio"]:
            return  # AsyncIO和MultiAsyncio可以处理异步任务
        
        # 只有Thread执行器不能处理异步任务
        incompatible_tasks = []
        for task_name, task in self._tasks.items():
            # 检查任务是否属于指定队列
            if task.queue not in queues:
                continue
                
            # 检查是否是异步任务
            if asyncio.iscoroutinefunction(task.run):
                incompatible_tasks.append({
                    'name': task_name,
                    'queue': task.queue,
                    'type': 'async'
                })
        
        if incompatible_tasks:
            error_msg = f"\n错误：{execute_type} 执行器不能处理异步任务！\n"
            error_msg += "发现以下异步任务：\n"
            for task in incompatible_tasks:
                error_msg += f"  - {task['name']} (队列: {task['queue']})\n"
            error_msg += f"\n解决方案：\n"
            error_msg += f"1. 使用 asyncio 或 process 执行器\n"
            error_msg += f"2. 或者将这些任务改为同步函数（去掉 async/await）\n"
            error_msg += f"3. 或者将这些任务的队列从监听列表中移除\n"
            raise ValueError(error_msg)



    def _create_executor(self, concurrency: int):
        """
        创建进程编排器实例

        Returns:
            ProcessOrchestrator 实例
        """
        # 创建 ProcessOrchestrator（多进程管理器）
        orchestrator = ProcessOrchestrator(self, concurrency)

        # 保存 orchestrator 引用
        self._current_executor = orchestrator

        # 设置信号处理器
        def signal_handler(signum, frame):
            logger.debug(f"Main process received signal {signum}, initiating shutdown...")
            self._should_exit = True
            orchestrator.shutdown_event.set()
            raise KeyboardInterrupt()

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        return orchestrator

    async def _cleanup_worker_v3(self, heartbeat_managers: list, executor, worker_ids: list):
        """
        清理 Worker 资源（新版本，支持多个心跳协程）
        """
        logger.debug("Shutting down workers...")

        # 1. 停止 Worker 超时扫描器
        # try:
        #     logger.debug("Stopping worker scanner...")
        #     self.worker_state.stop_timeout_scanner(timeout=3.0)
        # except Exception as e:
        #     logger.error(f"Error stopping worker scanner: {e}", exc_info=True)

        # 2. 停止所有心跳协程
        if heartbeat_managers:
            logger.debug(f"Stopping {len(heartbeat_managers)} heartbeat tasks...")
            for i, heartbeat in enumerate(heartbeat_managers):
                try:
                    worker_id = worker_ids[i][0] if i < len(worker_ids) else f"worker_{i}"
                    logger.debug(f"Stopping heartbeat task for {worker_id}...")
                    await heartbeat.stop()
                except Exception as e:
                    logger.error(f"Error stopping heartbeat #{i}: {e}", exc_info=True)

        # 3. 关闭执行器
        if executor:
            try:
                logger.debug("Shutting down executor...")
                executor.shutdown()
            except Exception as e:
                logger.error(f"Error shutting down executor: {e}", exc_info=True)

        # 5. 调用通用清理
        # try:
        #     self.cleanup()
        # except Exception as e:
        #     logger.error(f"Error in cleanup: {e}", exc_info=True)

        logger.debug(f"All {len(worker_ids)} workers shutdown complete")

    async def _start(self, tasks: List[str], concurrency: int = 1, prefetch_multiplier: int = 1):
        """
        启动 Worker 主逻辑（多进程模式，主进程调用）

        新架构流程：
        1. 从任务名称获取队列列表
        2. 确保 queue_registry 的 redis 客户端已初始化
        3. 为每个子进程生成独立的 Worker ID
        4. 在主进程为每个子进程启动独立的心跳线程
        5. 创建执行器
        6. Fork 并启动子进程，传递对应的 worker_id
        7. 等待退出信号（阻塞）
        8. 清理资源

        Args:
            tasks: 任务名称列表
            concurrency: 并发执行器进程数（子进程数量）
            prefetch_multiplier: 预取倍数
        """
        heartbeat_managers = []
        executor = None
        worker_ids = []

        # 1. 从任务名称获取队列列表
        queues = self._get_queues_from_tasks(tasks)
        logger.debug(f"Tasks {tasks} -> Queues {queues}")

        try:
            # 2. 为每个子进程生成独立的 Worker ID 并启动心跳协程
            # logger.debug(f"Generating {concurrency} worker IDs and starting heartbeat tasks...")
            from jettask.worker.heartbeat import HeartbeatManager

            for i in range(concurrency):
                # 使用新方法：生成 worker_id 并启动心跳，等待首次心跳成功
                heartbeat = await HeartbeatManager.create_and_start(
                    queue_registry=self.registry,  # 传递 queue_registry 用于发现新队列
                    worker_manager=self.worker_state,  # 传递 worker_manager 用于更新 worker 状态
                    async_redis_client=self.async_redis,
                    redis_prefix=self.redis_prefix,
                    interval=self.heartbeat_interval,
                    heartbeat_timeout=self.heartbeat_timeout,
                    worker_state=self.worker_state
                )
                # 从心跳管理器对象中获取 worker_id 和 worker_key
                worker_ids.append((heartbeat.worker_id, heartbeat.worker_key))
                heartbeat_managers.append(heartbeat)
                # logger.debug(f"  Process #{i}: worker_id={heartbeat.worker_id} (heartbeat started)")

            # 3. 创建执行器（在启动 scanner 之前，避免 fork 复制协程资源）
            executor = self._create_executor(concurrency)

            # 4. 启动全局 Worker 超时扫描器（在 fork 之后启动，避免资源复制到子进程）
            # Scanner 会使用每个 worker 自己存储的 heartbeat_timeout 进行超时判断
            # logger.debug("Starting global worker timeout scanner...")
            # 启动 scanner，使用配置的扫描间隔
            HeartbeatManager.start_global_timeout_scanner(
                scan_interval=self.scanner_interval,
                worker_manager=self.worker_state
            )
            # logger.debug("Global worker timeout scanner started")
         

            # 5. 启动 ProcessOrchestrator
            # 传递 worker_ids 列表，每个子进程使用对应的 worker_id
            # 注意：executor.start() 是同步阻塞调用，但必须在主线程中运行（因为需要设置信号处理器）
            # 它内部使用 time.sleep() 会阻塞事件循环，但心跳和队列发现任务已经在事件循环中启动
            # logger.debug(f"Starting {concurrency} executor processes...")

            # 在线程池中运行，避免阻塞事件循环
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,  # 使用默认线程池
                executor.start,
                queues,
                tasks,
                prefetch_multiplier,
                worker_ids
            )
        

        except KeyboardInterrupt:
            logger.debug("Worker interrupted by keyboard")
        except Exception as e:
            logger.error(f"Error in worker main loop: {e}", exc_info=True)
        finally:
            # 停止全局 scanner
            logger.debug("Stopping global worker timeout scanner...")
            await HeartbeatManager.stop_global_timeout_scanner()

            # 清理资源
            await self._cleanup_worker_v3(heartbeat_managers, executor, worker_ids)

    def start(
        self,
        tasks: List[str],
        concurrency: int = 1,
        prefetch_multiplier: int = 1,
    ):
        """启动 Worker（仅支持 multi_asyncio）

        Args:
            tasks: 任务名称列表（必需参数）
            concurrency: 并发数
            prefetch_multiplier: 预取倍数
        """

        # 检查必需参数
        if not tasks:
            raise ValueError(
                "必须指定 tasks 参数！\n"
                "示例: app.start(tasks=['task1', 'task2'], concurrency=4)"
            )

        # 标记worker已启动
        self._worker_started = True

        # 如果配置了任务中心且配置尚未加载，从任务中心获取配置
        if self.task_center and self.task_center.is_enabled and not self._task_center_config:
            self._load_config_from_task_center()

        # 注册所有待注册的限流配置到 Redis
        logger.debug("正在注册待注册的限流配置...")
        self._apply_pending_rate_limits()

        # 注册清理处理器（只在启动worker时注册）
        self._setup_cleanup_handlers()


        # 使用 asyncio.run 启动异步的 _start() 方法
        asyncio.run(self._start(
            tasks=tasks,
            concurrency=concurrency,
            prefetch_multiplier=prefetch_multiplier,
        ))


    def get_task_info(self, event_id: str, asyncio: bool = False):
        """获取任务信息（从TASK:hash）"""
        client = self.get_redis_client(asyncio)
        key = f"{self.redis_prefix}:TASK:{event_id}"
        if asyncio:
            return client.hgetall(key)
        else:
            return client.hgetall(key)
    
    def get_task_status(self, event_id: str, asyncio: bool = False):
        """获取任务状态（从TASK:hash的status字段）

        注意：这个方法使用简化的 key 格式 TASK:{event_id}
        如果需要获取带 group_name 的任务状态，请使用 _get_task_status_sync 或 _get_task_status_async
        """
        if asyncio:
            return self._get_task_status_simple_async(event_id)
        else:
            client = self.redis
            key = f"{self.redis_prefix}:TASK:{event_id}"
            return client.hget(key, "status")

    async def _get_task_status_simple_async(self, event_id: str):
        """异步获取任务状态（简化版本，不需要 task_name 和 queue）"""
        key = f"{self.redis_prefix}:TASK:{event_id}"
        return await self.async_redis.hget(key, "status")

    def set_task_status(self, event_id: str, status: str, asyncio: bool = False):
        """设置任务状态（写入TASK:hash的status字段）"""
        if asyncio:
            return self._set_task_status_async(event_id, status)
        else:
            client = self.redis
            key = f"{self.redis_prefix}:TASK:{event_id}"
            return client.hset(key, "status", status)
    
    async def _set_task_status_async(self, event_id: str, status: str):
        """异步设置任务状态"""
        key = f"{self.redis_prefix}:TASK:{event_id}"
        return await self.async_redis.hset(key, "status", status)

    def set_task_status_by_batch(self, mapping: dict, asyncio: bool = False):
        """批量设置任务状态（写入TASK:hash）"""
        if asyncio:
            return self._set_task_status_by_batch_async(mapping)
        else:
            pipeline = self.redis.pipeline()
            for event_id, status in mapping.items():
                key = f"{self.redis_prefix}:TASK:{event_id}"
                pipeline.hset(key, "status", status)
            return pipeline.execute()
    
    async def _set_task_status_by_batch_async(self, mapping: dict):
        """异步批量设置任务状态"""
        pipeline = self.async_redis.pipeline()
        for event_id, status in mapping.items():
            key = f"{self.redis_prefix}:TASK:{event_id}"
            pipeline.hset(key, "status", status)
        return await pipeline.execute()

    def del_task_status(self, event_id: str, asyncio: bool = False):
        """删除任务状态（删除整个TASK:hash）"""
        client = self.get_redis_client(asyncio)
        key = f"{self.redis_prefix}:TASK:{event_id}"
        return client.delete(key)

    def get_redis_client(self, asyncio: bool = False):
        return self.async_redis if asyncio else self.redis

    async def get_and_delayed_deletion(self, key: str, ex: int):
        """获取结果并延迟删除（从hash中）"""
        result = await self.async_redis.hget(key, "result")
        await self.async_redis.expire(key, ex)
        return result

    # ==================== 定时任务调度相关 ====================
    
    async def _ensure_scheduler_initialized(self, db_url: str = None):
        """确保调度器已初始化（内部方法）"""
        if not self.scheduler:
            logger.debug("Auto-initializing scheduler...")
            # 优先使用传入的db_url，然后是实例化时的pg_url，最后是环境变量
            if not db_url:
                db_url = self.pg_url or os.environ.get('JETTASK_PG_URL')
            if not db_url:
                raise ValueError(
                    "Database URL not provided. Please provide pg_url when initializing Jettask, "
                    "or set JETTASK_PG_URL environment variable\n"
                    "Example: app = Jettask(redis_url='...', pg_url='postgresql://...')\n"
                    "Or: export JETTASK_PG_URL='postgresql://user:password@localhost:5432/jettask'"
                )

            self._scheduler_db_url = db_url

            # 创建调度器
            scheduler_config = self.scheduler_config.copy()
            scheduler_config.setdefault('scan_interval', 1.0)  # 默认30秒扫描一次
            scheduler_config.setdefault('batch_size', 100)
            scheduler_config.setdefault('lookahead_seconds', 3600)  # 默认提前1小时

            self.scheduler = TaskScheduler(
                app=self,
                db_url=db_url,
                **scheduler_config
            )

            logger.debug("Scheduler initialized")
    
    async def start_scheduler(self):
        """启动定时任务调度器（自动初始化，阻塞式）"""
        # 自动初始化调度器
        await self._ensure_scheduler_initialized()

        try:
            # wait=True 表示阻塞等待调度器完成
            await self.scheduler.start(wait=True)
        except Exception as e:
            logger.error(f"Scheduler error: {e}", exc_info=True)
            raise
    
    async def register_schedules(self, schedules):
        """
        注册定时任务（支持单个或批量）

        这是新的统一注册方法，类似 TaskMessage 的设计模式。

        Args:
            schedules: ScheduledMessage 对象或列表

        Returns:
            注册的任务数量

        Example:
            from jettask import Schedule

            # 1. 定义定时任务
            schedule1 = Schedule(
                scheduler_id="notify_every_30s",
                queue="notification_queue",
                interval_seconds=30,
                kwargs={"user_id": "user_123", "message": "定时提醒"}
            )

            schedule2 = Schedule(
                scheduler_id="report_cron",
                queue="report_queue",
                cron_expression="0 9 * * *",
                description="每天生成报告"
            )

            # 2. 批量注册
            count = await app.register_schedules([schedule1, schedule2])
            print(f"注册了 {count} 个定时任务")
        """
        from ..scheduler.definition import Schedule
        from ..db.models import ScheduledTask, TaskType

        # 自动初始化
        await self._ensure_scheduler_initialized()

        # 支持单个或列表
        if isinstance(schedules, Schedule):
            schedules = [schedules]

        if not schedules:
            return 0

        # 获取当前命名空间
        namespace = 'default'
        if self.task_center and hasattr(self.task_center, 'namespace_name'):
            namespace = self.task_center.namespace_name
        elif self.redis_prefix and self.redis_prefix != 'jettask':
            namespace = self.redis_prefix

        # 转换为 ScheduledTask 对象
        tasks = []
        for schedule in schedules:
            if not isinstance(schedule, Schedule):
                raise ValueError(f"Expected Schedule, got {type(schedule)}")

            data = schedule.to_dict()
            task = ScheduledTask(
                scheduler_id=data['scheduler_id'],
                task_type=data['task_type'],  # 直接使用字符串值
                queue_name=data['queue'],
                namespace=namespace,
                task_args=data['task_args'],
                task_kwargs=data['task_kwargs'],
                interval_seconds=data.get('interval_seconds'),
                cron_expression=data.get('cron_expression'),
                next_run_time=data.get('next_run_time'),
                enabled=data['enabled'],
                priority=data['priority'],
                timeout=data['timeout'],
                max_retries=data['max_retries'],
                retry_delay=data['retry_delay'],
                description=data['description'],
                tags=data['tags'],
                metadata=data['metadata']
            )
            # 保存 skip_if_exists 选项
            task._skip_if_exists = schedule.skip_if_exists
            tasks.append(task)

        # 批量注册到数据库
        from ..db.connector import get_pg_engine_and_factory

        _, session_factory = get_pg_engine_and_factory(
            dsn=self._scheduler_db_url,
            pool_size=10,
            max_overflow=20,
            pool_recycle=3600,
            echo=False
        )
        session = session_factory()
        try:
            registered_count = 0
            for task in tasks:
                skip_if_exists = getattr(task, '_skip_if_exists', True)

                # 检查任务是否已存在
                existing_task = await ScheduledTask.get_by_scheduler_id(session, task.scheduler_id)

                if existing_task:
                    if not skip_if_exists:
                        # 更新现有任务
                        task.id = existing_task.id
                        await ScheduledTask.update_task(session, task)
                        await session.commit()
                        logger.debug(f"已更新定时任务: {task.scheduler_id} -> {task.queue_name}")
                    else:
                        logger.debug(f"定时任务已存在: {task.scheduler_id}")
                else:
                    # 创建新任务
                    await ScheduledTask.create(session, task)
                    await session.commit()
                    registered_count += 1
                    logger.debug(f"已注册定时任务: {task.scheduler_id} -> {task.queue_name}")

            return registered_count
        finally:
            await session.close()

    async def list_schedules(self, **filters):
        """
        列出定时任务

        Args:
            **filters: 过滤条件（enabled, queue_name, task_type 等）

        Returns:
            List[ScheduledTask]: 任务列表
        """
        await self._ensure_scheduler_initialized()

        from ..db.connector import get_pg_engine_and_factory
        from ..db.models import ScheduledTask

        _, session_factory = get_pg_engine_and_factory(
            dsn=self._scheduler_db_url,
            pool_size=10,
            max_overflow=20,
            pool_recycle=3600,
            echo=False
        )
        session = session_factory()
        try:
            return await ScheduledTask.list_tasks(session, **filters)
        finally:
            await session.close()

    async def remove_schedule(self, scheduler_id: str) -> bool:
        """
        移除定时任务

        Args:
            scheduler_id: 任务唯一标识符

        Returns:
            bool: 是否成功移除
        """
        await self._ensure_scheduler_initialized()

        from ..db.connector import get_pg_engine_and_factory
        from ..db.models import ScheduledTask

        _, session_factory = get_pg_engine_and_factory(
            dsn=self._scheduler_db_url,
            pool_size=10,
            max_overflow=20,
            pool_recycle=3600,
            echo=False
        )
        session = session_factory()
        try:
            task = await ScheduledTask.get_by_scheduler_id(session, scheduler_id)
            if not task:
                return False

            await ScheduledTask.delete_by_id(session, task.id)
            await session.commit()
            return True
        finally:
            await session.close()

    async def pause_schedule(self, scheduler_id: str) -> bool:
        """
        暂停定时任务

        Args:
            scheduler_id: 任务唯一标识符

        Returns:
            bool: 是否成功暂停
        """
        await self._ensure_scheduler_initialized()

        from ..db.connector import get_pg_engine_and_factory
        from ..db.models import ScheduledTask

        _, session_factory = get_pg_engine_and_factory(
            dsn=self._scheduler_db_url,
            pool_size=10,
            max_overflow=20,
            pool_recycle=3600,
            echo=False
        )
        session = session_factory()
        try:
            task = await ScheduledTask.get_by_scheduler_id(session, scheduler_id)
            if not task:
                return False

            task.enabled = False
            await ScheduledTask.update_task(session, task)
            await session.commit()
            return True
        finally:
            await session.close()

    async def resume_schedule(self, scheduler_id: str) -> bool:
        """
        恢复定时任务

        Args:
            scheduler_id: 任务唯一标识符

        Returns:
            bool: 是否成功恢复
        """
        await self._ensure_scheduler_initialized()

        from ..db.connector import get_pg_engine_and_factory
        from ..db.models import ScheduledTask

        _, session_factory = get_pg_engine_and_factory(
            dsn=self._scheduler_db_url,
            pool_size=10,
            max_overflow=20,
            pool_recycle=3600,
            echo=False
        )
        session = session_factory()
        try:
            task = await ScheduledTask.get_by_scheduler_id(session, scheduler_id)
            if not task:
                return False

            task.enabled = True
            await ScheduledTask.update_task(session, task)
            await session.commit()
            return True
        finally:
            await session.close()

