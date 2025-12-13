"""
统一的调度器管理器
基于 NamespaceWorkerManagerBase 实现
"""
import asyncio
import logging
from typing import Dict
from jettask.core.namespace_manager_base import NamespaceWorkerManagerBase
from jettask.core.namespace import NamespaceContext
from jettask.scheduler.scheduler import TaskScheduler

logger = logging.getLogger(__name__)


class UnifiedSchedulerManager(NamespaceWorkerManagerBase):
    """
    统一的调度器管理器

    基于 NamespaceWorkerManagerBase，专注于调度器特定的逻辑
    """

    def __init__(self,
                 task_center_url: str,
                 scan_interval: float = 1.0,
                 batch_size: int = 100,
                 lookahead_seconds: int = 3600,
                 check_interval: int = 30,
                 api_key: str = None,
                 debug: bool = False):
        """
        初始化调度器管理器

        Args:
            task_center_url: 任务中心URL
            scan_interval: 调度器扫描间隔（秒）
            batch_size: 每批处理的最大任务数
            lookahead_seconds: 提前查看时间（秒）
            check_interval: 命名空间检测间隔（秒）
            api_key: API密钥（用于请求鉴权）
            debug: 是否启用调试模式
        """
        # 调度器特定参数
        self.scan_interval = scan_interval
        self.batch_size = batch_size
        self.lookahead_seconds = lookahead_seconds

        # 调度器管理（多命名空间模式使用任务）
        self.scheduler_tasks: Dict[str, asyncio.Task] = {}
        self.schedulers: Dict[str, TaskScheduler] = {}

        # 调用基类初始化
        super().__init__(task_center_url, check_interval, debug, api_key=api_key)

        # 打印调度器配置
        logger.info(f"扫描间隔: {self.scan_interval}秒")
        logger.info(f"批次大小: {self.batch_size}")
        logger.info(f"提前查看: {self.lookahead_seconds}秒")

    async def _run_worker_for_namespace(self, ns: NamespaceContext):
        """为单个命名空间运行调度器"""
        logger.info(f"启动命名空间 {ns.name} 的调度器")

        try:
            # 获取 Jettask 应用实例
            jettask_app = await ns.get_jettask_app()

            logger.info(f"命名空间 {ns.name} 配置:")
            logger.info(f"  - Redis: 已配置")
            logger.info(f"  - PostgreSQL: 已配置")
            logger.info(f"  - Redis Prefix: {ns.redis_prefix}")

            # 创建调度器
            scheduler = TaskScheduler(
                app=jettask_app,
                db_url=ns.pg_config['url'],
                scan_interval=self.scan_interval,
                batch_size=self.batch_size,
                lookahead_seconds=self.lookahead_seconds
            )

            # 缓存调度器（用于多命名空间模式）
            self.schedulers[ns.name] = scheduler

            logger.info(f"✓ 调度器已创建: {ns.name}")

            # 运行调度器（阻塞等待直到停止）
            await scheduler.start(wait=True)

        except asyncio.CancelledError:
            logger.info(f"调度器被取消: {ns.name}")
            raise
        except Exception as e:
            logger.error(f"命名空间 {ns.name} 调度器运行失败: {e}", exc_info=self.debug)
            raise
        finally:
            # 清理
            if ns.name in self.schedulers:
                scheduler = self.schedulers[ns.name]
                await scheduler.stop()
                del self.schedulers[ns.name]
                logger.info(f"调度器已停止: {ns.name}")

    def _should_start_worker(self, ns: NamespaceContext) -> bool:
        """判断是否应该为命名空间启动调度器"""
        return ns.has_pg and ns.has_redis

    async def _start_worker(self, ns_or_name):
        """启动调度器（多命名空间模式使用异步任务）"""
        # 在多命名空间模式下，传入的是 NamespaceContext
        ns = ns_or_name

        # 如果任务已存在且未完成，跳过
        if ns.name in self.scheduler_tasks:
            task = self.scheduler_tasks[ns.name]
            if not task.done():
                logger.debug(f"命名空间 {ns.name} 的调度器任务已在运行")
                return
            else:
                # 检查是否有异常
                try:
                    task.result()
                except Exception as e:
                    logger.error(f"命名空间 {ns.name} 的调度器任务异常退出: {e}")

        # 创建新任务
        logger.info(f"启动命名空间 {ns.name} 的调度器任务")

        task = asyncio.create_task(
            self._run_worker_for_namespace(ns),
            name=f"Scheduler-{ns.name}"
        )
        self.scheduler_tasks[ns.name] = task

        logger.info(f"✓ 调度器任务已启动: {ns.name}")

    async def _stop_worker(self, ns_name: str):
        """停止调度器"""
        if ns_name in self.scheduler_tasks:
            task = self.scheduler_tasks[ns_name]
            logger.info(f"停止调度器任务: {ns_name}")
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            del self.scheduler_tasks[ns_name]

        # 如果有缓存的调度器实例，也停止它
        if ns_name in self.schedulers:
            scheduler = self.schedulers[ns_name]
            logger.info(f"停止调度器实例: {ns_name}")
            await scheduler.stop()
            del self.schedulers[ns_name]

    def _get_running_workers(self) -> set[str]:
        """获取当前运行的调度器列表"""
        return set(self.scheduler_tasks.keys())


__all__ = ['UnifiedSchedulerManager']
