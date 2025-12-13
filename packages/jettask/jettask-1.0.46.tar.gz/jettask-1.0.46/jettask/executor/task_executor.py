"""
任务执行器

职责：
1. 从事件队列获取消息
2. 执行任务并管理生命周期
3. 限流控制和批处理
"""

import asyncio
import logging
import time
import os
from typing import Set
from collections import deque

from .core import ExecutorCore
from ..messaging.delay_queue import AsyncDelayQueue
from ..worker.lifecycle import WorkerManager
from ..utils.rate_limit.manager import RateLimiterManager

logger = logging.getLogger('app')


class TaskExecutor:
    """
    任务执行器 - 负责单个任务类型的执行

    这是真正执行任务的核心组件，无论是在单进程还是多进程模式下。

    职责：
    1. 从 event_queue 获取消息
    2. 应用限流控制
    3. 执行任务
    4. 批处理管道优化
    """

    def __init__(self, event_queue, app, task_name: str, worker_id: str, worker_state_manager, concurrency: int = 100):
        """
        初始化任务执行器

        Args:
            event_queue: asyncio.Queue，接收待执行的消息
            app: Application 实例（或 MinimalApp）
            task_name: 任务名称
            worker_id: Worker ID
            worker_state_manager: WorkerManager 实例
            concurrency: 并发数（实际由限流器控制）
        """
        self.event_queue = event_queue
        self.app = app
        self.task_name = task_name
        self.concurrency = concurrency
        self.worker_id = worker_id
        self.worker_state_manager = worker_state_manager
        # 核心组件
        self.executor_core = ExecutorCore(
            app=app,
            task_name=task_name,
            concurrency=concurrency
        )

        # 将executor_core存储到app，供手动ACK使用
        if not hasattr(app, '_executor_core'):
            app._executor_core = self.executor_core

        # 同时也设置到 task._app 上（解决多进程模式下 MinimalApp 与原始 app 不一致的问题）
        task_obj = app.get_task_by_name(task_name)
        if task_obj and hasattr(task_obj, '_app') and not hasattr(task_obj._app, '_executor_core'):
            task_obj._app._executor_core = self.executor_core

        # 活动任务集合
        self._active_tasks: Set[asyncio.Task] = set()

        # Pipeline 配置
        self.max_buffer_size = 5000

        # 延迟队列（用于处理延迟任务）
        self.delay_queue = AsyncDelayQueue()

        logger.debug(f"TaskExecutor initialized for task '{task_name}'")

    async def initialize(self):
        """
        初始化执行器组件

        在开始执行前调用，初始化限流器、WorkerState 等
        """
        # 确保有 consumer_id

        # 初始化 WorkerManager（如果尚未初始化）
        # if not self.app.worker_state_manager:
        #     self.app.worker_state_manager = WorkerManager(
        #         redis_client=self.app.ep.redis_client,
        #         async_redis_client=self.app.ep.async_redis_client,
        #         redis_prefix=self.executor_core.prefix,
        #         event_pool=self.app.ep
        #     )
        #     await self.app.worker_state_manager.start_listener()

        # 初始化时间同步
        from jettask.utils.time_sync import init_time_sync
        time_sync = await init_time_sync(self.app.ep.async_redis_client)
        logger.debug(f"TimeSync initialized, offset={time_sync.get_offset():.6f}s")

        # 初始化限流器
        self.executor_core.rate_limiter_manager = RateLimiterManager(
            redis_client=self.app.ep.async_redis_client,
            worker_id=self.worker_id,
            redis_prefix=self.executor_core.prefix,
            worker_state_manager=self.worker_state_manager
        )
        logger.debug(f"RateLimiterManager initialized for worker {self.worker_id}")

        # 加载限流配置
        await self.executor_core.rate_limiter_manager.load_config_from_redis()

    async def run(self):
        """
        执行主循环

        持续从 event_queue 获取消息并执行，直到收到停止信号
        """
        logger.debug(f"TaskExecutor started for task '{self.task_name}'")

        tasks_batch = []

        try:
            while True:
                # 检查退出信号
                if hasattr(self.app, '_should_exit') and self.app._should_exit:
                    logger.debug(f"TaskExecutor[{self.task_name}] detected shutdown signal")
                    break

                # 检查父进程（防止孤儿进程）
                if hasattr(os, 'getppid') and os.getppid() == 1:
                    logger.warning(f"TaskExecutor[{self.task_name}] parent died, exiting")
                    break

                current_time = time.time()

                # 1. 先从延迟队列获取到期任务
                expired_tasks = self.delay_queue.get_expired_tasks()
                for expired_task in expired_tasks:
                    # 清理延迟标记
                    event_data = expired_task.get('event_data', {})
                    event_data.pop("execute_at", None)
                    event_data.pop("is_delayed", None)

                    tasks_batch.append(expired_task)
                    logger.debug(
                        f"[{self.task_name}] Delayed task {expired_task.get('event_id', 'unknown')} "
                        f"expired and ready for execution"
                    )

                # 2. 从 event_queue 获取新任务（带超时）
                event = None
                try:
                    event = await asyncio.wait_for(self.event_queue.get(), timeout=0.1)
                except asyncio.TimeoutError:
                    pass
                
                if event:
                    # 检查是否是延迟任务（检查 event_data 中的 execute_at 字段）
                    event_data = event.get('event_data', {})
                    execute_at = event_data.get("execute_at")

                    if execute_at is not None:
                        # 这是一个延迟任务，检查是否到期
                        current_time = time.time()

                        if execute_at > current_time:
                            # 还没到执行时间，放入延迟队列
                            delay = execute_at - current_time
                            self.delay_queue.put(event, delay)
                            logger.debug(
                                f"[{self.task_name}] Delayed task {event.get('event_id', 'unknown')} "
                                f"by {delay:.3f}s (execute_at={execute_at:.3f})"
                            )
                            continue
                        else:
                            # 已到期，移除 execute_at 字段并立即处理
                            event_data.pop("execute_at", None)
                            event_data.pop("is_delayed", None)
                            logger.debug(
                                f"[{self.task_name}] Delayed task {event.get('event_id', 'unknown')} "
                                f"already expired, executing immediately"
                            )

                    # 立即处理的任务（无延迟或已到期）
                    tasks_batch.append(event)
                    logger.debug(
                        f"[{self.task_name}] Got event: {event.get('event_id', 'unknown')}"
                    )

                # 批量处理任务
                if tasks_batch:
                    await self._process_batch(tasks_batch)
                    tasks_batch.clear()

                # 智能缓冲区管理
                if self._should_flush_buffers(current_time):
                    asyncio.create_task(self.executor_core._flush_all_buffers())

                # 智能休眠
                await self._smart_sleep()

        except asyncio.CancelledError:
            logger.debug(f"TaskExecutor[{self.task_name}] cancelled")
        except Exception as e:
            logger.error(f"TaskExecutor[{self.task_name}] error: {e}", exc_info=True)
        finally:
            await self.cleanup()

    async def _process_batch(self, tasks_batch):
        """处理一批任务"""
        for event in tasks_batch:
            event_data = event.get('event_data', {})
            event_task_name = event_data.get("_task_name") or event_data.get("name")

            if not event_task_name:
                logger.error(f"No task_name in event {event.get('event_id')}")
                continue

            # 验证任务名称
            if event_task_name != self.task_name:
                logger.error(
                    f"Task name mismatch: {event_task_name} != {self.task_name}"
                )
                continue

            # 限流控制
            logger.debug(
                f"[{self.task_name}] Acquiring rate limit, event_id={event.get('event_id')}"
            )

            rate_limit_token = await self.executor_core.rate_limiter_manager.acquire(
                task_name=self.task_name,
                timeout=None
            )

            if not rate_limit_token:
                logger.error(f"Failed to acquire token for {self.task_name}")
                continue

            logger.debug(
                f"[{self.task_name}] Acquired token={rate_limit_token}, starting execution"
            )

            self.executor_core.batch_counter += 1

            # 创建任务并自动释放限流许可
            async def execute_with_release(event_data, token):
                try:
                    await self.executor_core.execute_task(**event_data)
                finally:
                    await self.executor_core.rate_limiter_manager.release(
                        self.task_name, task_id=token
                    )

            task = asyncio.create_task(execute_with_release(event, rate_limit_token))
            self._active_tasks.add(task)
            task.add_done_callback(self._active_tasks.discard)

    def _should_flush_buffers(self, current_time: float) -> bool:
        """判断是否需要刷新缓冲区"""
        # 检查缓冲区是否满
        buffer_full = (
            len(self.executor_core.pending_acks) >= self.max_buffer_size or
            len(self.executor_core.status_updates) >= self.max_buffer_size or
            len(self.executor_core.data_updates) >= self.max_buffer_size or
            len(self.executor_core.task_info_updates) >= self.max_buffer_size
        )

        if buffer_full:
            return True

        # 检查是否有待处理数据
        has_pending_data = (
            self.executor_core.pending_acks or
            self.executor_core.status_updates or
            self.executor_core.data_updates or
            self.executor_core.task_info_updates
        )

        if not has_pending_data:
            return False

        # 检查是否超时
        for data_type, config in self.executor_core.pipeline_config.items():
            time_since_flush = current_time - self.executor_core.last_pipeline_flush[data_type]

            if data_type == 'ack' and self.executor_core.pending_acks:
                if time_since_flush >= config['max_delay']:
                    return True
            elif data_type == 'task_info' and self.executor_core.task_info_updates:
                if time_since_flush >= config['max_delay']:
                    return True
            elif data_type == 'status' and self.executor_core.status_updates:
                if time_since_flush >= config['max_delay']:
                    return True
            elif data_type == 'data' and self.executor_core.data_updates:
                if time_since_flush >= config['max_delay']:
                    return True

        return False

    async def _smart_sleep(self):
        """智能休眠 - 根据队列状态和延迟任务决定休眠时间"""
        has_events = False

        if isinstance(self.event_queue, deque):
            has_events = bool(self.event_queue)
        elif isinstance(self.event_queue, asyncio.Queue):
            has_events = not self.event_queue.empty()

        if has_events:
            # 有待处理事件，立即继续
            await asyncio.sleep(0)
        else:
            # 无事件，计算休眠时间
            has_pending = (
                self.executor_core.pending_acks or
                self.executor_core.status_updates or
                self.executor_core.data_updates or
                self.executor_core.task_info_updates
            )

            if has_pending:
                # 有待刷新的数据，先刷新
                await self.executor_core._flush_all_buffers()

            # 检查延迟队列中下一个任务的到期时间
            next_expire_time = self.delay_queue.get_next_expire_time()
            if next_expire_time is not None:
                # 有延迟任务，计算到下一个任务到期的时间
                current_time = time.time()
                sleep_time = max(0.001, min(0.1, next_expire_time - current_time))
                await asyncio.sleep(sleep_time)
            else:
                # 没有延迟任务，使用默认休眠时间
                await asyncio.sleep(0.001)

    async def cleanup(self):
        """清理资源"""
        logger.debug(f"TaskExecutor[{self.task_name}] cleaning up")

        # 清空延迟队列
        self.delay_queue.clear()
        logger.debug("Delay queue cleared")

        # 设置停止标志
        if hasattr(self.app.ep, '_stop_reading'):
            self.app.ep._stop_reading = True

        # 取消活动任务
        if self._active_tasks:
            logger.debug(
                f"TaskExecutor[{self.task_name}] cancelling {len(self._active_tasks)} active tasks"
            )
            for task in self._active_tasks:
                if not task.done():
                    task.cancel()

            if self._active_tasks:
                try:
                    await asyncio.wait_for(
                        asyncio.gather(*self._active_tasks, return_exceptions=True),
                        timeout=0.2
                    )
                except asyncio.TimeoutError:
                    logger.warning(
                        f"TaskExecutor[{self.task_name}] some tasks did not complete in time"
                    )

        # 清理 ExecutorCore
        await self.executor_core.cleanup()

        logger.debug(f"TaskExecutor[{self.task_name}] stopped")


__all__ = ['TaskExecutor']
