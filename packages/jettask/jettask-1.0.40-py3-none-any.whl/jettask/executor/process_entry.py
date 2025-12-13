"""
多进程执行器的子进程入口

职责：
1. 清理继承的父进程状态
2. 初始化子进程环境
3. 启动任务执行器
"""
import os
import gc
import sys
import signal
import asyncio
import logging
import multiprocessing
from typing import List, Dict
import time 

# 不要在模块级别创建 logger，避免在 fork 时触发 logging 全局锁竞争
# logger 将在 subprocess_main 中创建
logger = None


class SubprocessInitializer:
    """子进程初始化器 - 负责清理和准备环境"""

    @staticmethod
    def cleanup_inherited_state():
        """
        清理从父进程继承的状态（fork模式）

        在 fork 模式下，子进程继承父进程的内存状态，包括：
        - Redis连接池和客户端
        - 事件循环对象
        - 线程对象和锁
        - 信号处理器

        我们需要正确清理这些资源，避免：
        - 子进程复用父进程的连接（会导致数据混乱）
        - 访问父进程的任务/线程（会导致死锁）
        - 信号处理器冲突
        """
        # 1. 重置信号处理器
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)

        # 2. 重置事件循环策略
        # 不要尝试访问或关闭旧循环，直接设置新的策略
        # 这样子进程在首次使用asyncio时会创建全新的循环
        try:
            asyncio.set_event_loop_policy(None)
            asyncio.set_event_loop(None)
        except Exception:
            pass

        # 3. 清空Redis连接池和客户端缓存
        # 这非常重要！防止子进程复用父进程的连接
        from jettask.db.connector import clear_all_cache
        clear_all_cache()

        # 4. 强制垃圾回收
        gc.collect()

    @staticmethod
    def setup_logging(process_id: int, redis_prefix: str):
        """配置子进程日志

        注意：在 fork 模式下，子进程会继承父进程的 logging handlers。
        这些 handlers 可能持有父进程的锁或文件描述符，导致死锁。
        因此需要先清除所有继承的 handlers，再手动创建全新的 handler。
        """
        # 0. 重置 logging 模块的全局锁（关键！）
        # 在 fork 后，logging 模块的全局锁可能处于被父进程持有的状态
        # 需要手动重新创建这些锁，避免死锁
        import threading
        logging._lock = threading.RLock()

        # 1. 清除根 logger 的所有 handlers
        root_logger = logging.getLogger()

        # 重置根logger的锁
        if hasattr(root_logger, '_lock'):
            root_logger._lock = threading.RLock()

        for handler in root_logger.handlers[:]:
            try:
                # 重置handler的锁
                if hasattr(handler, 'lock'):
                    handler.lock = threading.RLock()
                handler.close()
            except:
                pass
            root_logger.removeHandler(handler)

        # 2. 清除所有已存在的 logger 的 handlers，并重置 propagate
        for logger_name in list(logging.Logger.manager.loggerDict.keys()):
            logger_obj = logging.getLogger(logger_name)

            # 重置logger的锁
            if hasattr(logger_obj, '_lock'):
                logger_obj._lock = threading.RLock()

            if hasattr(logger_obj, 'handlers'):
                for handler in logger_obj.handlers[:]:
                    try:
                        # 重置handler的锁
                        if hasattr(handler, 'lock'):
                            handler.lock = threading.RLock()
                        handler.close()
                    except:
                        pass
                    logger_obj.removeHandler(handler)

                # 确保所有子 logger 的日志都能传播到根 logger
                logger_obj.propagate = True

        # 3. 手动创建全新的 handler
        # 不使用 logging.basicConfig()，因为它可能会复用某些全局状态
        # 而是手动创建一个全新的 StreamHandler
        formatter = logging.Formatter(
            fmt=f"%(asctime)s - %(levelname)s - [{redis_prefix}-P{process_id}] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)
        # 确保新handler有正确的锁
        handler.createLock()

        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(handler)

    @staticmethod
    def create_event_loop() -> asyncio.AbstractEventLoop:
        """创建全新的事件循环"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop


class MinimalApp:
    """
    最小化的 App 接口

    为子进程提供必要的接口，而不需要完整的 App 实例
    """
    def __init__(
        self,
        redis_client,
        async_redis_client,
        redis_url: str,
        redis_prefix: str,
        tasks: Dict,
        worker_id: str,
        worker_key: str
    ):
        self.redis = redis_client
        self.async_redis = async_redis_client
        self.redis_url = redis_url
        self.redis_prefix = redis_prefix
        self._tasks = tasks
        self.worker_id = worker_id
        self.worker_key = worker_key
        self._should_exit = False

        # ExecutorCore 需要的属性
        self._status_prefix = f"{redis_prefix}:STATUS:"
        self._result_prefix = f"{redis_prefix}:RESULT:"

        # EventPool 需要的属性
        self._tasks_by_queue = {}
        for task_name, task in tasks.items():
            task_queue = task.queue or redis_prefix
            if task_queue not in self._tasks_by_queue:
                self._tasks_by_queue[task_queue] = []
            self._tasks_by_queue[task_queue].append(task_name)

        # 这些属性会在初始化时设置
        self.ep = None
        self.consumer_manager = None
        self.worker_state = None  # EventPool 的恢复机制需要这个属性

    def get_task_by_name(self, task_name: str):
        """根据任务名称获取任务对象"""
        return self._tasks.get(task_name)

    def get_task_config(self, task_name: str) -> dict:
        """
        获取任务配置

        Args:
            task_name: 任务名称

        Returns:
            任务配置字典，如果任务不存在则返回None
        """
        task = self.get_task_by_name(task_name)
        if not task:
            return None

        return {
            'auto_ack': getattr(task, 'auto_ack', True),
            'queue': getattr(task, 'queue', None),
            'timeout': getattr(task, 'timeout', None),
            'max_retries': getattr(task, 'max_retries', 0),
            'retry_delay': getattr(task, 'retry_delay', None),
        }

    def cleanup(self):
        """清理资源"""
        pass


class SubprocessRunner:
    """子进程运行器 - 负责实际执行任务"""

    def __init__(
        self,
        process_id: int,
        redis_url: str,
        redis_prefix: str,
        queues: List[str],
        tasks: Dict,
        concurrency: int,
        prefetch_multiplier: int,
        max_connections: int,
        consumer_config: Dict,
        worker_id: str,
        worker_key: str
    ):
        self.process_id = process_id
        self.redis_url = redis_url
        self.redis_prefix = redis_prefix
        self.queues = queues
        self.tasks = tasks
        self.concurrency = concurrency
        self.prefetch_multiplier = prefetch_multiplier
        self.max_connections = max_connections
        self.consumer_config = consumer_config or {}
        self.worker_id = worker_id
        self.worker_key = worker_key

        # 子进程内部状态
        self.redis_client = None
        self.async_redis_client = None
        self.minimal_app = None
        self.event_pool = None
        self.executors = []
        self._should_exit = False

    def setup_signal_handlers(self):
        """设置信号处理器"""
        def signal_handler(signum, _frame):
            logger.debug(f"Process #{self.process_id} received signal {signum}")
            self._should_exit = True
            if self.minimal_app:
                self.minimal_app._should_exit = True
            if self.event_pool:
                self.event_pool._stop_reading = True

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def create_redis_connections(self):
        """创建独立的Redis连接（使用全局客户端实例）"""
        from jettask.db.connector import get_sync_redis_client, get_async_redis_client

        # logger.debug(f"Process #{self.process_id}: Creating Redis connections")

        # 同步连接（使用全局客户端实例）
        self.redis_client = get_sync_redis_client(
            redis_url=self.redis_url,
            decode_responses=True,
            max_connections=self.max_connections
        )

        # 异步连接（使用全局客户端实例）
        self.async_redis_client = get_async_redis_client(
            redis_url=self.redis_url,
            decode_responses=True,
            max_connections=self.max_connections
        )

    async def initialize_components(self):
        """初始化执行器组件"""
        from jettask.messaging.event_pool import EventPool
        from jettask.executor.task_executor import TaskExecutor
        from jettask.messaging.registry import QueueRegistry
        from jettask.worker.lifecycle import WorkerManager

        logger.debug(f"Process #{self.process_id}: Initializing components")

        # 直接使用传入的 tasks 参数创建 event queues（不需要通过队列反推）
        task_event_queues = {task_name: asyncio.Queue() for task_name in self.tasks.keys()}
        logger.debug(f"Process #{self.process_id}: Created event queues for tasks: {list(task_event_queues.keys())}")

        # 创建 MinimalApp
        self.minimal_app = MinimalApp(
            redis_client=self.redis_client,
            async_redis_client=self.async_redis_client,
            redis_url=self.redis_url,
            redis_prefix=self.redis_prefix,
            tasks=self.tasks,
            worker_id=self.worker_id,
            worker_key=self.worker_key
        )

        # 创建 QueueRegistry
        queue_registry = QueueRegistry(
            redis_client=self.redis_client,
            async_redis_client=self.async_redis_client,
            redis_prefix=self.redis_prefix
        )
        logger.debug(f"Process #{self.process_id}: Created QueueRegistry")

        # 创建用于二进制数据的Redis客户端（用于Stream操作）
        from jettask.db.connector import get_async_redis_client
        async_binary_redis_client = get_async_redis_client(
            self.redis_url,
            decode_responses=False,
            socket_timeout=None
        )

        # 初始化 WorkerManager（集成了离线恢复功能）
        # WorkerManager 现在同时负责 Worker 状态管理和离线消息恢复
        worker_manager = WorkerManager(
            redis_client=self.redis_client,
            async_redis_client=async_binary_redis_client,
            redis_prefix=self.redis_prefix,
            queue_formatter=lambda q: f"{self.redis_prefix}:QUEUE:{q}",
            queue_registry=queue_registry,
            app=self.minimal_app,
            tasks=self.tasks,
            task_event_queues=task_event_queues,
            worker_id=self.worker_id
        )
        # 设置 worker_state 供 EventPool 使用（offline_recovery 参数）
        self.minimal_app.worker_state = worker_manager
        logger.debug(f"Process #{self.process_id}: Created WorkerManager with recovery capabilities")

        # 启动 PubSub Listener 以支持即时离线恢复
        await worker_manager.start_listener()
        logger.info(f"Process #{self.process_id}: Started PubSub listener for instant offline worker recovery")

        # 创建 EventPool
        consumer_config = self.consumer_config.copy()
        consumer_config['redis_prefix'] = self.redis_prefix
        consumer_config['disable_heartbeat_process'] = True

        self.event_pool = EventPool(
            self.redis_client,
            self.async_redis_client,
            task_event_queues,  # ✅ 传递 task_event_queues
            self.tasks,  # ✅ 传递完整的 tasks 字典 {task_name: task_obj}
            queue_registry,  # ✅ 传递 QueueRegistry
            self.minimal_app.worker_state,  # ✅ offline_recovery - 直接使用 WorkerManager（它已经包含恢复功能）
            queues=self.queues,  # ✅ 传递 queues 参数以支持通配符模式
            redis_url=self.redis_url,
            consumer_config=consumer_config,
            redis_prefix=self.redis_prefix,
            app=self.minimal_app,
            worker_id=self.worker_id  # ✅ 传递 worker_id
        )

        # 将 EventPool 设置到 MinimalApp
        self.minimal_app.ep = self.event_pool

        # 初始化路由
        # ✅ 不再需要这行，因为 EventPool.__init__ 已经正确处理了 queues（包括通配符）
        # self.event_pool.queues = self.queues
        self.event_pool.init_routing()

        # 启动异步事件监听
        listening_task = asyncio.create_task(
            self.event_pool.listening_event(self.prefetch_multiplier)
        )

        # 为每个任务创建独立的 TaskExecutor
        for task_name, task_queue in task_event_queues.items():
            executor = TaskExecutor(
                event_queue=task_queue,
                app=self.minimal_app,
                task_name=task_name,
                worker_id=self.worker_id,
                worker_state_manager=worker_manager,
                concurrency=self.concurrency
            )

            # 初始化执行器
            await executor.initialize()

            # 启动执行器
            executor_task = asyncio.create_task(executor.run())
            self.executors.append((task_name, executor_task))
            logger.debug(f"Process #{self.process_id}: Started TaskExecutor for task '{task_name}'")

        # 返回所有任务
        return listening_task, [t for _, t in self.executors]

    async def run(self):
        """运行执行器主循环"""
        logger.debug(f"Process #{self.process_id} starting (PID: {os.getpid()})")

        listening_task = None
        executor_tasks = []

        try:
            listening_task, executor_tasks = await self.initialize_components()

            # 等待所有任务完成
            await asyncio.gather(listening_task, *executor_tasks)

        except asyncio.CancelledError:
            logger.debug(f"Process #{self.process_id} cancelled")
        except Exception as e:
            logger.error(f"Process #{self.process_id} error: {e}", exc_info=True)
        finally:
            # 清理
            logger.debug(f"Process #{self.process_id} cleaning up")

            if listening_task and not listening_task.done():
                listening_task.cancel()

            for _task_name, task in self.executors:
                if not task.done():
                    task.cancel()

            # 等待取消完成
            try:
                all_tasks = [listening_task] + executor_tasks if listening_task else executor_tasks
                await asyncio.wait_for(
                    asyncio.gather(*all_tasks, return_exceptions=True),
                    timeout=0.5
                )
            except asyncio.TimeoutError:
                pass

            # 清理 EventPool
            if self.event_pool and hasattr(self.event_pool, 'cleanup'):
                try:
                    self.event_pool.cleanup()
                except Exception as e:
                    logger.error(f"Error cleaning up EventPool: {e}")

            # 清理 lifecycle
            # if self.minimal_app and self.minimal_app.lifecycle:
            #     try:
            #         self.minimal_app.lifecycle.cleanup()
            #     except Exception as e:
            #         logger.error(f"Error cleaning up lifecycle: {e}")

            # 关闭 WorkerManager（停止 PubSub listener）
            if self.minimal_app and hasattr(self.minimal_app, 'worker_state') and self.minimal_app.worker_state:
                try:
                    await self.minimal_app.worker_state.stop_listener()
                    logger.debug(f"Process #{self.process_id}: Stopped PubSub listener")
                except Exception as e:
                    logger.error(f"Error stopping WorkerManager listener: {e}")

            # 关闭 Redis 连接
            if self.async_redis_client:
                try:
                    await self.async_redis_client.aclose()
                except Exception as e:
                    logger.error(f"Error closing async Redis client: {e}")

            logger.debug(f"Process #{self.process_id} stopped")


def subprocess_main(
    process_id: int,
    redis_url: str,
    redis_prefix: str,
    queues: List[str],
    tasks: Dict,
    concurrency: int,
    prefetch_multiplier: int,
    max_connections: int,
    consumer_config: Dict,
    worker_id: str,
    worker_key: str,
    shutdown_event
):
    """
    子进程主函数 - 这是子进程的真正入口点

    职责：
    1. 调用初始化器清理环境
    2. 创建运行器并执行
    3. 确保资源正确清理
    """
    
    try:
        # 设置进程名
        # multiprocessing.current_process().name = f"JetTask-Worker-{process_id}"
        # ========== 阶段1：清理和初始化 ==========
        initializer = SubprocessInitializer()
        initializer.cleanup_inherited_state()
        initializer.setup_logging(process_id, redis_prefix)

        # 在清理和配置logging后，创建一个新的logger实例
        global logger
        logger = logging.getLogger()
        logger.debug(f"Process #{process_id} starting in PID {os.getpid()}")
        # ========== 阶段2：创建运行器 ==========
        runner = SubprocessRunner(
            process_id=process_id,
            redis_url=redis_url,
            redis_prefix=redis_prefix,
            queues=queues,
            tasks=tasks,
            concurrency=concurrency,
            prefetch_multiplier=prefetch_multiplier,
            max_connections=max_connections,
            consumer_config=consumer_config,
            worker_id=worker_id,
            worker_key=worker_key
        )
        # 设置信号处理
        runner.setup_signal_handlers()
        # 创建 Redis 连接
        runner.create_redis_connections()
        # ========== 阶段3：运行 ==========
        loop = initializer.create_event_loop()

        try:
            if not shutdown_event.is_set():
                loop.run_until_complete(runner.run())
        except KeyboardInterrupt:
            logger.debug(f"Process #{process_id} received interrupt")
        except Exception as e:
            logger.error(f"Process #{process_id} fatal error: {e}", exc_info=True)
        finally:
            # 清理并发锁
            try:
                if worker_id:
                    from jettask.utils.rate_limit.concurrency_limiter import ConcurrencyRateLimiter
                    task_names = list(tasks.keys()) if tasks else []
                    ConcurrencyRateLimiter.cleanup_worker_locks(
                        redis_url=redis_url,
                        redis_prefix=redis_prefix,
                        worker_id=worker_id,
                        task_names=task_names
                    )
            except Exception as e:
                logger.error(f"Error during lock cleanup: {e}")

            # 关闭事件循环
            try:
                loop.close()
            except:
                pass

            logger.debug(f"Process #{process_id} exited")
            sys.exit(0)
    except Exception as e:
        import traceback 
        traceback.print_exc()
        print(f"Subprocess #{process_id} fatal error during initialization: {e}", file=sys.stderr)
        sys.exit(1)

__all__ = ['subprocess_main']
