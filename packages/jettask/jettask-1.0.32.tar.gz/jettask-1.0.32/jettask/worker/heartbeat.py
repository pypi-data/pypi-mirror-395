"""
Worker 心跳管理

提供基于协程的心跳管理功能，在主进程中运行。

HeartbeatManager 是一个异步协程管理器，负责定期向 Redis 发送心跳信号。
"""

import os
import socket
import uuid
import time
import asyncio
import logging
from typing import Optional, TYPE_CHECKING
from ..messaging.registry import QueueRegistry
if TYPE_CHECKING:
    from .lifecycle import WorkerManager
logger = logging.getLogger(__name__)

class HeartbeatManager:
    """基于协程的心跳管理器（在 CLI 主进程中运行）"""

    # 全局 timeout scanner 任务（类级别属性）
    _global_scanner_task = None
    _global_scanner_stop_event = None
    _global_worker_manager = None  # 全局 WorkerManager 实例
    _scanner_interval = None  # 扫描间隔（由 start_global_timeout_scanner 设置）

    def __init__(self, queue_registry: QueueRegistry, worker_manager: "WorkerManager", async_redis_client=None,
                 worker_key=None, worker_id=None, redis_prefix=None, redis_url=None,
                 interval=5.0, heartbeat_timeout=15.0):
        """初始化心跳协程管理器

        Args:
            queue_registry: QueueRegistry 实例（必需），用于发现匹配的队列
            worker_manager: WorkerManager 实例（必需），用于更新 worker 状态
            async_redis_client: 异步 Redis 客户端
            worker_key: Worker 键
            worker_id: Worker ID
            redis_prefix: Redis 前缀
            redis_url: Redis URL（用于重连）
            interval: 心跳间隔
            heartbeat_timeout: 心跳超时时间
        """
        if queue_registry is None:
            raise ValueError("queue_registry is required")
        if worker_manager is None:
            raise ValueError("worker_manager is required")

        # Queue registry 用于发现匹配的队列
        self.queue_registry = queue_registry

        # Worker manager 用于更新 worker 状态
        self.worker_manager = worker_manager

        self.async_redis_client = async_redis_client
        self.worker_key = worker_key
        self.worker_id = worker_id
        self.redis_prefix = redis_prefix
        self.redis_url = redis_url
        self.interval = interval
        self.consumer_id = worker_id
        self.heartbeat_interval = interval
        self.heartbeat_timeout = heartbeat_timeout
        self._last_heartbeat_time = None

        self._stop_event = asyncio.Event()
        self._heartbeat_task = None
        self.heartbeat_process = self

        # 用于等待首次心跳的事件
        self._first_heartbeat_done = asyncio.Event()

    @classmethod
    async def create_and_start(cls, queue_registry, worker_manager, async_redis_client,
                        redis_prefix: str, interval: float = 5.0, heartbeat_timeout: float = 15.0,
                        worker_state=None):
        """
        创建心跳管理器并启动，生成 worker_id 后等待首次心跳成功

        Args:
            queue_registry: QueueRegistry 实例（必需），用于发现匹配的队列
            worker_manager: WorkerManager 实例（必需），用于更新 worker 状态
            async_redis_client: 异步 Redis 客户端
            redis_prefix: Redis 前缀
            interval: 心跳间隔（秒）
            heartbeat_timeout: 心跳超时时间（秒），建议为 interval 的 3 倍
            worker_state: WorkerState 实例（用于查找可复用的 worker_id）

        Returns:
            HeartbeatManager 实例（包含 worker_id 和 worker_key 属性）
        """
        # 1. 生成 worker_id

        # 生成主机名前缀
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            prefix = hostname if hostname != 'localhost' else ip
        except:
            prefix = os.environ.get('HOSTNAME', 'unknown')

        # 尝试复用离线的 worker_id
        reusable_id = None
        if worker_state:
            reusable_id = await worker_state.find_reusable_worker_id(prefix=prefix)

        # 生成或复用 worker_id
        if reusable_id:
            worker_id = reusable_id
            logger.debug(f"[PID {os.getpid()}] Reusing offline worker ID: {worker_id}")
        else:
            worker_id = worker_state.generate_worker_id(prefix) if worker_state else f"{prefix}-{uuid.uuid4().hex[:8]}-{os.getpid()}"
            logger.debug(f"[PID {os.getpid()}] Generated new worker ID: {worker_id}")

        worker_key = f"{redis_prefix}:WORKER:{worker_id}"

        # 2. 创建心跳管理器
        manager = cls(
            queue_registry=queue_registry,
            worker_manager=worker_manager,
            async_redis_client=async_redis_client,
            worker_key=worker_key,
            worker_id=worker_id,
            redis_prefix=redis_prefix,
            interval=interval,
            heartbeat_timeout=heartbeat_timeout
        )

        # 3. 启动心跳协程
        manager.start()

        # 4. 等待首次心跳成功（最多等待 10 秒）
        try:
            await asyncio.wait_for(manager._first_heartbeat_done.wait(), timeout=10)
        except asyncio.TimeoutError:
            logger.warning(f"Timeout waiting for first heartbeat for worker {worker_id}")

        # 返回管理器对象，调用方可以通过 manager.worker_id 和 manager.worker_key 访问
        return manager

    def start(self):
        """启动心跳协程"""
        if self._heartbeat_task and not self._heartbeat_task.done():
            logger.warning("Heartbeat task already running")
            return

        self._stop_event.clear()

        # 启动心跳任务
        self._heartbeat_task = asyncio.create_task(
            self._heartbeat_loop(),
            name=f"Heartbeat-{self.worker_id}"
        )
        # logger.debug(f"Heartbeat task started for worker {self.worker_id}")

    async def stop(self):
        """停止心跳协程"""
        if not self._heartbeat_task:
            return

        logger.debug(f"Stopping heartbeat task for worker {self.worker_id}")
        self._stop_event.set()

        # 使用 WorkerManager 设置 worker 为离线状态
        try:
            await self.worker_manager.set_worker_offline(self.worker_id, reason='heartbeat_stopped')
            logger.debug(f"Worker {self.worker_id} marked as offline")
        except Exception as e:
            logger.error(f"Error marking worker offline: {e}", exc_info=True)


    async def _heartbeat_loop(self):
        """心跳循环（异步协程）"""
        hostname = socket.gethostname()
        pid = str(os.getpid())

        logger.debug(f"Heartbeat task starting for worker {self.worker_id}")

        heartbeat_count = 0
        last_log_time = time.time()
        first_heartbeat = True

        while not self._stop_event.is_set():
            try:
                current_time = time.time()

                needs_full_init = False
                publish_online_signal = False

                old_alive = await self.async_redis_client.hget(self.worker_key, 'is_alive')
                consumer_id = await self.async_redis_client.hget(self.worker_key, 'consumer_id')

                if not consumer_id:
                    needs_full_init = True
                    publish_online_signal = True
                    logger.warning(f"Worker {self.worker_id} key missing critical fields, reinitializing...")
                elif first_heartbeat and old_alive != 'true':
                    publish_online_signal = True

                # 标记首次心跳完成（在第一次心跳逻辑执行后）
                if first_heartbeat:
                    first_heartbeat = False

                if needs_full_init:
                    # 使用 WorkerManager 初始化 worker
                    worker_info = {
                        'consumer_id': self.worker_id,
                        'host': hostname,
                        'pid': pid,
                        'heartbeat_timeout': str(self.heartbeat_timeout),
                    }

                    await self.worker_manager.initialize_worker(self.worker_id, worker_info)
                    await self.worker_manager.register_worker(self.worker_id)
                    logger.debug(f"Reinitialized worker {self.worker_id} with full info")

                elif publish_online_signal:
                    # 从离线变为在线，使用 WorkerManager 的 set_worker_online
                    # 注意：需要更新 heartbeat_timeout，因为可能是复用的 worker_id，配置可能已变更
                    worker_data = {
                        'host': hostname,
                        'heartbeat_timeout': str(self.heartbeat_timeout),
                    }

                    logger.debug(f"Worker {self.worker_id} 准备调用 set_worker_online，worker_data={worker_data}")
                    await self.worker_manager.set_worker_online(self.worker_id, worker_data)
                    logger.debug(f"Worker {self.worker_id} set_worker_online 完成")
                    await self.worker_manager.register_worker(self.worker_id)
                    logger.debug(f"Worker {self.worker_id} is now ONLINE (heartbeat_timeout={self.heartbeat_timeout}s)")

                else:
                    # 普通心跳更新，使用 WorkerManager 的 update_worker_heartbeat
                    heartbeat_data = {
                        'host': hostname
                    }
                    await self.worker_manager.update_worker_heartbeat(self.worker_id, heartbeat_data)

                self._last_heartbeat_time = current_time
                heartbeat_count += 1

                # 如果这是首次心跳，通知等待的协程
                if heartbeat_count == 1:
                    self._first_heartbeat_done.set()
                    logger.debug(f"First heartbeat completed for worker {self.worker_id}, will continue every {self.interval}s")

                # 每次心跳都记录（调试用）
                logger.debug(f"Heartbeat #{heartbeat_count} sent for worker {self.worker_id}, waiting {self.interval}s for next")

                if current_time - last_log_time >= 30:
                    logger.debug(f"Heartbeat task: sent {heartbeat_count} heartbeats for worker {self.worker_id} in last 30s")
                    last_log_time = current_time
                    heartbeat_count = 0

            except Exception as e:
                logger.error(f"Error in heartbeat task: {e}", exc_info=True)
                if "Timeout connecting" in str(e) or "Connection" in str(e):
                    try:
                        await self.async_redis_client.aclose()
                    except:
                        pass
                    try:
                        if self.redis_url:
                            from jettask.db.connector import get_async_redis_client
                            self.async_redis_client = get_async_redis_client(
                                redis_url=self.redis_url,
                                decode_responses=True,
                            )
                            logger.debug(f"Reconnected to Redis for heartbeat task {self.worker_id}")
                    except Exception as reconnect_error:
                        logger.error(f"Failed to reconnect Redis: {reconnect_error}")
                await asyncio.sleep(5)

            try:
                await asyncio.wait_for(self._stop_event.wait(), timeout=self.interval)
            except asyncio.TimeoutError:
                pass  # 超时是正常的，继续下一次循环

        logger.debug(f"Heartbeat task exiting for worker {self.worker_id}")

    def is_healthy(self) -> bool:
        """检查心跳协程是否健康"""
        if not self._heartbeat_task:
            return False

        if self._heartbeat_task.done():
            logger.error(f"Heartbeat task for worker {self.worker_id} is done")
            return False
        return True

    def get_last_heartbeat_time(self) -> Optional[float]:
        """获取最后一次心跳时间"""
        return self._last_heartbeat_time

    def is_heartbeat_timeout(self) -> bool:
        """检查心跳是否已超时"""
        last_heartbeat = self.get_last_heartbeat_time()
        if last_heartbeat is None:
            return False

        current_time = time.time()
        return (current_time - last_heartbeat) > self.heartbeat_timeout

    # ========================================================================
    # 全局 Worker 超时扫描器（协程版本）
    # ========================================================================

    @classmethod
    def start_global_timeout_scanner(cls, scan_interval: float, worker_manager: "WorkerManager"):
        """启动全局 Worker 超时扫描器（协程版本）

        每个 worker 使用自己存储的 heartbeat_timeout 进行超时判断。
        这个值由 HeartbeatManager 在 worker 初始化时设置到 worker_data 中。

        Args:
            scan_interval: 扫描间隔（秒），由 Jettask 初始化时的 scanner_interval 参数传入
            worker_manager: WorkerManager 实例，用于扫描和更新 worker 状态

        Returns:
            Scanner 任务对象
        """
        cls._scanner_interval = scan_interval
        if cls._global_scanner_task and not cls._global_scanner_task.done():
            logger.warning("Global worker timeout scanner already running")
            return cls._global_scanner_task

        # 保存 worker_manager 引用
        cls._global_worker_manager = worker_manager
        cls._global_scanner_stop_event = asyncio.Event()

        async def scanner_loop():
            """扫描器协程循环"""
            logger.debug(f"Worker timeout scanner started (interval={cls._scanner_interval}s)")

            try:
                while not cls._global_scanner_stop_event.is_set():
                    try:
                        # 扫描超时的 Worker
                        # 每个 worker 使用自己存储的 heartbeat_timeout 进行超时判断
                        timeout_workers = await cls._global_worker_manager.scan_timeout_workers()

                        if timeout_workers:
                            logger.debug(f"Processing {len(timeout_workers)} timeout workers")

                            # 处理每个超时的 Worker
                            for worker_info in timeout_workers:
                                worker_id = worker_info['worker_id']
                                try:
                                    # 标记为离线
                                    await cls._global_worker_manager.set_worker_offline(
                                        worker_id,
                                        reason="heartbeat_timeout"
                                    )
                                    logger.debug(f"Marked worker {worker_id} as offline due to timeout")
                                except Exception as e:
                                    logger.error(f"Error marking worker {worker_id} offline: {e}")

                        # 等待下次扫描
                        try:
                            await asyncio.wait_for(
                                cls._global_scanner_stop_event.wait(),
                                timeout=cls._scanner_interval
                            )
                        except asyncio.TimeoutError:
                            pass  # 超时是正常的，继续下一次循环

                    except Exception as e:
                        logger.error(f"Error in worker scanner loop: {e}", exc_info=True)
                        await asyncio.sleep(cls._scanner_interval)

            except asyncio.CancelledError:
                logger.debug("Worker timeout scanner cancelled")
                raise
            finally:
                logger.debug("Worker timeout scanner stopped")

        # 启动扫描器任务
        cls._global_scanner_task = asyncio.create_task(
            scanner_loop(),
            name="GlobalWorkerTimeoutScanner"
        )
        logger.debug("Global worker timeout scanner task created")
        return cls._global_scanner_task

    @classmethod
    async def stop_global_timeout_scanner(cls):
        """停止全局 Worker 超时扫描器"""
        if not cls._global_scanner_task:
            return

        logger.debug("Stopping global worker timeout scanner...")

        if cls._global_scanner_stop_event:
            cls._global_scanner_stop_event.set()

        if cls._global_scanner_task and not cls._global_scanner_task.done():
            cls._global_scanner_task.cancel()
            try:
                await cls._global_scanner_task
            except asyncio.CancelledError:
                pass

        cls._global_scanner_task = None
        cls._global_scanner_stop_event = None
        logger.debug("Global worker timeout scanner stopped")

    @classmethod
    def is_global_scanner_running(cls) -> bool:
        """检查全局扫描器是否在运行"""
        return cls._global_scanner_task is not None and not cls._global_scanner_task.done()


__all__ = ['HeartbeatManager']

