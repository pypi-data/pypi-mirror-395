"""
定时任务调度模块

本模块提供：
- TaskScheduler - 定时任务调度器，负责周期性扫描和触发任务
"""
import asyncio
import logging
from typing import Optional, List
from datetime import datetime, timezone
import time
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from jettask.core.message import TaskMessage
from jettask.db.models import ScheduledTask, TaskType
from jettask.db.connector import get_pg_engine_and_factory, _get_safe_pg_dsn

logger = logging.getLogger('app')


# ==================== TaskScheduler ====================


class TaskScheduler:
    """
    定时任务调度器

    设计理念：
    1. 直接从数据库读取即将到期的任务（避免 Redis 中间层）
    2. 提前1小时获取任务，利用延迟任务功能（TaskMessage 的 delay 参数）
    3. 发送后立即更新数据库状态，防止重复发送
    4. 减少数据库查询频率，提高系统可维护性

    工作流程：
    1. 定期扫描数据库（默认30秒一次）
    2. 查找未来1小时内需要执行的任务
    3. 使用 TaskMessage + delay 发送到队列
    4. 更新任务状态（周期性任务计算下次执行时间，一次性任务禁用）
    """

    def __init__(
        self,
        app,
        db_url: str,
        scan_interval: float = 3.0,
        batch_size: int = 100,
        lookahead_seconds: int = 3600,  # 默认提前1小时
        **kwargs  # 忽略其他参数
    ):
        """
        初始化调度器

        Args:
            app: Jettask应用实例
            db_url: PostgreSQL连接URL
            scan_interval: 扫描间隔（秒），默认30秒
            batch_size: 每次处理的任务数量，默认100
            lookahead_seconds: 提前查看时间（秒），默认3600秒（1小时）
        """
        self.app = app
        self.db_url = db_url

        self.scan_interval = scan_interval
        self.batch_size = batch_size
        self.lookahead_seconds = lookahead_seconds

        # 获取并保存 session_factory（复用连接池）
        _, self._session_factory = get_pg_engine_and_factory(
            dsn=db_url,
            pool_size=10,
            max_overflow=20,
            pool_recycle=3600,
            echo=False
        )

        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._stop_event = asyncio.Event()

        logger.info(
            f"TaskScheduler initialized: "
            f"scan_interval={scan_interval}s, "
            f"batch_size={batch_size}, "
            f"lookahead={lookahead_seconds}s, "
            f"db_url={_get_safe_pg_dsn(db_url)}"
        )

    async def start(self, wait: bool = False):
        """
        启动调度器

        Args:
            wait: 是否等待调度器完成（阻塞式）
                  - False（默认）：启动后台任务并立即返回
                  - True：启动并等待调度器完成（阻塞直到停止）
        """
        if self._running:
            logger.warning("Scheduler already running")
            return

        self._running = True
        self._stop_event.clear()

        # 启动后台任务
        self._task = asyncio.create_task(self._run_loop())

        logger.info("TaskScheduler started")

        # 如果需要等待完成
        if wait:
            try:
                await self._task
            except asyncio.CancelledError:
                logger.info("Scheduler was cancelled")
            except Exception as e:
                logger.error(f"Scheduler error: {e}", exc_info=True)
                raise

    async def stop(self):
        """
        停止调度器

        优雅地停止调度器并等待后台任务完成
        """
        if not self._running:
            logger.warning("Scheduler is not running")
            return

        logger.info("Stopping TaskScheduler...")

        # 设置停止标志
        self._running = False
        self._stop_event.set()

        # 等待后台任务完成
        if self._task and not self._task.done():
            try:
                await asyncio.wait_for(self._task, timeout=10.0)
            except asyncio.TimeoutError:
                logger.warning("Scheduler task did not finish in time, cancelling...")
                self._task.cancel()
                try:
                    await self._task
                except asyncio.CancelledError:
                    pass
            except Exception as e:
                logger.error(f"Error while stopping scheduler: {e}", exc_info=True)

        logger.info("TaskScheduler stopped")

    async def _run_loop(self):
        """调度器主循环"""
        logger.info("Scheduler loop started")

        try:
            while self._running:
                try:
                    # 执行一次调度
                    await self._schedule_once()
                    print(f'{self.scan_interval=}')
                    # 等待下一次检查（支持提前中断）
                    try:
                        await asyncio.wait_for(
                            self._stop_event.wait(),
                            timeout=self.scan_interval
                        )
                        # 如果stop_event被设置，退出循环
                        break
                    except asyncio.TimeoutError:
                        # 超时是正常的，继续下一轮
                        pass

                except Exception as e:
                    logger.error(f"Error in scheduler loop: {e}", exc_info=True)
                    # 发生错误时等待一会再继续
                    await asyncio.sleep(5)

        except asyncio.CancelledError:
            logger.info("Scheduler loop cancelled")

        finally:
            logger.info("Scheduler loop exited")

    async def _schedule_once(self):
        """
        执行一次调度检查

        工作流程：
        1. 从数据库获取未来 lookahead_seconds 秒内需要执行的任务
        2. 对每个任务计算精确的延迟时间
        3. 使用 TaskMessage + delay 发送到队列
        4. 立即更新数据库状态，防止下次扫描重复发送

        Returns:
            处理的任务数量
        """
        start_time = time.time()
        logger.debug("开始调度检查...")  # 改为 INFO 级别

        # 使用数据库会话
        session = self._session_factory()
        try:
            async with session.begin():
                # 1. 从数据库获取即将执行的任务
                tasks = await ScheduledTask.get_ready_tasks(
                    session,
                    batch_size=self.batch_size,
                    lookahead_seconds=self.lookahead_seconds
                )

                if not tasks:
                    logger.debug("No tasks ready to schedule")
                    return 0

                logger.info(f"Found {len(tasks)} tasks ready to schedule (within {self.lookahead_seconds}s)")

                # 2. 发送任务到队列并更新状态
                scheduled_count = 0
                failed_tasks = []

                for task in tasks:
                    try:
                        # 发送任务到队列
                        success = await self._send_task_with_delay(task)

                        if success:
                            scheduled_count += 1
                        else:
                            failed_tasks.append(task)

                    except Exception as e:
                        logger.error(
                            f"Error scheduling task {task.scheduler_id}: {e}",
                            exc_info=True
                        )
                        failed_tasks.append(task)

                # 3. 批量更新任务状态
                # 注意：即使发送失败，也要更新状态，避免重复发送
                # 失败的任务会在下一个周期重试
                await self._update_tasks_after_scheduling(session, tasks)

        finally:
            await session.close()

        duration = time.time() - start_time
        logger.info(
            f"Schedule cycle completed: "
            f"scheduled={scheduled_count}, "
            f"failed={len(failed_tasks)}, "
            f"duration={duration:.2f}s"
        )

        # 如果有失败的任务，记录详细信息
        if failed_tasks:
            failed_ids = [t.scheduler_id for t in failed_tasks]
            logger.warning(f"Failed to schedule tasks: {failed_ids}")

        return scheduled_count

    async def _send_task_with_delay(self, task: ScheduledTask) -> bool:
        """
        发送任务到队列（带延迟）

        核心逻辑：
        1. 计算任务应该延迟多少秒执行
        2. 使用 TaskMessage 创建任务
        3. 设置 delay 参数
        4. 调用 app.send_tasks 发送

        Args:
            task: 定时任务对象

        Returns:
            是否成功发送
        """

        # 计算延迟时间（使用UTC时间）
        now = datetime.now(timezone.utc)
        delay = None

        if task.next_run_time:
            if task.next_run_time > now:
                # 任务还未到期：设置精确的delay时间
                delay = (task.next_run_time - now).total_seconds()
            else:
                # 任务已到期：立即执行，不设置delay
                delay = None

        # 构建任务消息
        msg = TaskMessage(
            queue=task.queue_name,
            args=task.task_args if task.task_args else [],
            kwargs=task.task_kwargs if task.task_kwargs else {},
            priority=task.priority,
            delay=delay,
            scheduled_task_id=task.id  # 标记为定时任务触发
        )

        try:
            # 发送任务（使用异步方式）
            event_ids = await self.app.send_tasks([msg], asyncio=True)

            if event_ids:
                event_id = event_ids[0]

                # 记录详细日志
                if delay:
                    logger.info(
                        f"Scheduled task: scheduler_id={task.scheduler_id}, "
                        f"queue={task.queue_name}, "
                        f"event_id={event_id}, "
                        f"delay={delay:.1f}s"
                    )
                else:
                    logger.info(
                        f"Scheduled task (immediate): scheduler_id={task.scheduler_id}, "
                        f"queue={task.queue_name}, "
                        f"event_id={event_id}"
                    )
                return True
            else:
                logger.warning(f"Failed to send task {task.scheduler_id}: no event_id returned")
                return False

        except Exception as e:
            logger.error(f"Error sending task {task.scheduler_id}: {e}", exc_info=True)
            return False

    async def _update_tasks_after_scheduling(self, session: AsyncSession, tasks: List[ScheduledTask]):
        """
        调度后更新任务状态

        重要：即使发送失败，也要更新状态，避免重复发送
        失败的任务会在下一个调度周期重试

        核心逻辑：
        - last_run_time 设置为任务原本的 next_run_time（任务应该执行的时间）
        - 基于 last_run_time 计算新的 next_run_time
        - 这样可以确保任务按照固定间隔执行，不受调度延迟影响

        Args:
            session: 数据库会话
            tasks: 已调度的任务列表
        """
        updates = []  # 周期性任务的更新
        once_task_ids = []  # 一次性任务的ID

        for task in tasks:
            if task.task_type == TaskType.ONCE.value:
                # 一次性任务：禁用并清空next_run_time
                once_task_ids.append(task.id)
            else:
                # 周期性任务：
                # 1. last_run_time 设置为任务的 next_run_time（任务原本应该执行的时间）
                # 2. 基于 last_run_time 计算新的 next_run_time
                # 3. 计算新的 next_trigger_time
                last_run = task.next_run_time
                task.last_run_time = last_run
                next_run = task.calculate_next_run_time(from_time=last_run)
                next_trigger = task.calculate_trigger_time(next_run) if next_run else None

                updates.append((task.id, next_run, next_trigger, last_run))

        # 批量更新
        if updates:
            try:
                await ScheduledTask.batch_update_next_run_times(session, updates)
                logger.info(f"Updated {len(updates)} recurring tasks")
                # 记录详细的更新信息
                for task_id, next_run, next_trigger, last_run in updates:
                    logger.info(
                        f"  Task {task_id}: next_run={next_run}, "
                        f"next_trigger={next_trigger}, last_run={last_run}"
                    )
            except Exception as e:
                logger.error(f"Failed to update recurring tasks: {e}", exc_info=True)

        if once_task_ids:
            try:
                await ScheduledTask.batch_disable_once_tasks(session, once_task_ids)
                logger.info(f"Disabled {len(once_task_ids)} once tasks")
            except Exception as e:
                logger.error(f"Failed to disable once tasks: {e}", exc_info=True)

    async def trigger_now(self, task_id: int) -> bool:
        """
        立即触发一个任务（不修改其调度时间）

        用于手动触发或测试

        Args:
            task_id: 任务ID

        Returns:
            是否成功触发
        """
        session = self._session_factory()
        try:
            task = await ScheduledTask.get_by_id(session, task_id)
            if not task:
                logger.warning(f"Task {task_id} not found")
                return False

            # 不使用delay，立即执行
            msg = TaskMessage(
                queue=task.queue_name,
                args=task.task_args if task.task_args else [],
                kwargs=task.task_kwargs if task.task_kwargs else {},
                priority=task.priority,
                scheduled_task_id=task.id
            )

            try:
                event_ids = await self.app.send_tasks([msg], asyncio=True)

                if event_ids:
                    logger.info(
                        f"Manually triggered task {task.scheduler_id}: "
                        f"event_id={event_ids[0]}"
                    )
                    return True

            except Exception as e:
                logger.error(f"Error triggering task {task.scheduler_id}: {e}", exc_info=True)

            return False
        finally:
            await session.close()

    async def trigger_by_scheduler_id(self, scheduler_id: str) -> bool:
        """
        通过 scheduler_id 立即触发任务

        Args:
            scheduler_id: 任务的唯一标识符

        Returns:
            是否成功触发
        """
        session = self._session_factory()
        try:
            task = await ScheduledTask.get_by_scheduler_id(session, scheduler_id)
            if not task:
                logger.warning(f"Task with scheduler_id '{scheduler_id}' not found")
                return False

            return await self.trigger_now(task.id)
        finally:
            await session.close()


__all__ = ['TaskScheduler']
