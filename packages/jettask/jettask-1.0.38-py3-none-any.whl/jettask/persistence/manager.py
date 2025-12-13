"""
统一的 PostgreSQL 消费者管理器
基于 NamespaceWorkerManagerBase 实现
"""
import asyncio
import logging
import multiprocessing
from typing import Dict, Optional
from jettask.core.namespace_manager_base import NamespaceWorkerManagerBase
from jettask.core.namespace import NamespaceContext
from jettask.persistence.consumer import PostgreSQLConsumer

logger = logging.getLogger(__name__)


class UnifiedConsumerManager(NamespaceWorkerManagerBase):
    """
    统一的消费者管理器

    基于 NamespaceWorkerManagerBase，专注于消费者特定的逻辑
    """

    def __init__(self,
                 task_center_url: str,
                 check_interval: int = 30,
                 concurrency: int = 4,
                 prefetch_multiplier: int = 100,
                 api_key: str = None,
                 debug: bool = False):
        """
        初始化消费者管理器

        Args:
            task_center_url: 任务中心URL
            check_interval: 命名空间检测间隔（秒）
            concurrency: 并发数（每个命名空间的 worker 进程数）
            prefetch_multiplier: 预取倍数（默认 100）
            api_key: API密钥（用于请求鉴权）
            debug: 是否启用调试模式
        """
        # 消费者特定参数
        self.concurrency = concurrency
        self.prefetch_multiplier = prefetch_multiplier

        # 消费者管理
        self.consumer_instance: Optional[PostgreSQLConsumer] = None  # 单命名空间模式（进程内）
        self.consumer_processes: Dict[str, multiprocessing.Process] = {}  # 多命名空间模式（多进程）

        # 调用基类初始化
        super().__init__(task_center_url, check_interval, debug, api_key=api_key)

    async def _run_worker_for_namespace(self, ns: NamespaceContext):
        """为单个命名空间运行消费者（进程内运行）"""
        logger.info(f"启动命名空间 {ns.name} 的消费者")

        try:
            logger.info(f"命名空间 {ns.name} 配置:")
            logger.info(f"  - Redis: 已配置")
            logger.info(f"  - PostgreSQL: 已配置")
            logger.info(f"  - Redis Prefix: {ns.redis_prefix}")

            # 创建消费者
            self.consumer_instance = PostgreSQLConsumer(
                pg_config=ns.pg_config,
                redis_config=ns.redis_config,
                prefix=ns.redis_prefix,
                namespace_name=ns.name
            )

            logger.info(f"✓ 消费者已创建: {ns.name}")

            # 运行消费者
            await self.consumer_instance.start(
                concurrency=self.concurrency,
                prefetch_multiplier=self.prefetch_multiplier
            )

        except Exception as e:
            logger.error(f"消费者运行失败: {e}", exc_info=self.debug)
            raise
        finally:
            if self.consumer_instance:
                await self.consumer_instance.stop()
                logger.info(f"消费者已停止: {ns.name}")

    def _should_start_worker(self, ns: NamespaceContext) -> bool:
        """判断是否应该为命名空间启动消费者"""
        return ns.has_pg and ns.has_redis

    async def _start_worker(self, ns_or_name):
        """启动消费者（多命名空间模式使用进程）"""
        # 在多命名空间模式下，传入的是 NamespaceContext
        # 提取名称并启动进程
        ns_name = ns_or_name.name if isinstance(ns_or_name, NamespaceContext) else ns_or_name

        # 如果进程已存在且存活，跳过
        if ns_name in self.consumer_processes:
            process = self.consumer_processes[ns_name]
            if process.is_alive():
                logger.debug(f"命名空间 {ns_name} 的消费者进程已在运行")
                return
            else:
                logger.info(f"清理已停止的消费者进程: {ns_name}")
                process.terminate()
                process.join(timeout=5)

        # 创建新进程
        logger.info(f"启动命名空间 {ns_name} 的消费者进程")

        # 构建单命名空间 URL
        base_url = self._get_base_url()
        single_ns_url = f"{base_url}/api/task/v1/{ns_name}"

        process = multiprocessing.Process(
            target=_run_consumer_in_process,
            args=(single_ns_url, self.concurrency, self.prefetch_multiplier, self.api_key, self.debug),
            name=f"Consumer-{ns_name}"
        )
        process.start()
        self.consumer_processes[ns_name] = process

        logger.info(f"✓ 消费者进程已启动: {ns_name} (PID: {process.pid})")

    async def _stop_worker(self, ns_name: str):
        """停止消费者"""
        if ns_name in self.consumer_processes:
            process = self.consumer_processes[ns_name]
            logger.info(f"停止消费者进程: {ns_name}")
            process.terminate()
            process.join(timeout=10)
            if process.is_alive():
                logger.warning(f"强制终止消费者进程: {ns_name}")
                process.kill()
                process.join()
            del self.consumer_processes[ns_name]

    def _get_running_workers(self) -> set[str]:
        """获取当前运行的消费者列表"""
        return set(self.consumer_processes.keys())

    async def _namespace_check_loop(self):
        """命名空间检查循环（重写以添加健康检查）"""
        logger.info("命名空间检查循环已启动（包含健康检查）")

        while self.running:
            try:
                # 健康检查：检查所有消费者进程
                dead_processes = []
                for ns_name, process in self.consumer_processes.items():
                    if not process.is_alive():
                        logger.warning(f"消费者进程 {ns_name} 已停止 (退出码: {process.exitcode})")
                        dead_processes.append(ns_name)

                # 重启已停止的进程
                for ns_name in dead_processes:
                    logger.info(f"重启消费者进程: {ns_name}")
                    await self._start_worker(ns_name)

                # 调用基类的命名空间检查逻辑（检测新增/删除）
                await super()._namespace_check_loop()
                return  # 基类方法会循环，这里直接返回

            except Exception as e:
                logger.error(f"健康检查循环异常: {e}", exc_info=self.debug)
                await asyncio.sleep(10)


def _run_consumer_in_process(task_center_url: str, concurrency: int,
                             prefetch_multiplier: int, api_key: str, debug: bool):
    """
    在独立进程中运行消费者（供多命名空间模式使用）

    Args:
        task_center_url: 单命名空间任务中心URL
        concurrency: 并发数
        prefetch_multiplier: 预取倍数
        api_key: API密钥（用于请求鉴权）
        debug: 是否启用调试模式
    """
    import logging
    import re

    # 从URL提取命名空间名称
    match = re.search(r'/api/task/v1/([^/]+)/?$', task_center_url)
    namespace_name = match.group(1) if match else 'unknown'

    # 配置日志
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format=f'%(asctime)s - [{namespace_name}] - %(name)s - %(levelname)s - %(message)s'
    )

    logger = logging.getLogger(__name__)

    # 创建管理器并运行（会自动检测为单命名空间模式）
    manager = UnifiedConsumerManager(
        task_center_url=task_center_url,
        concurrency=concurrency,
        prefetch_multiplier=prefetch_multiplier,
        api_key=api_key,
        debug=debug
    )

    # 运行异步任务
    try:
        logger.info(f"消费者进程启动: {namespace_name} (PID: {multiprocessing.current_process().pid})")
        asyncio.run(manager.run())
    except KeyboardInterrupt:
        logger.info("进程收到中断信号")
    except Exception as e:
        logger.error(f"进程异常退出: {e}", exc_info=debug)
        raise


__all__ = ['UnifiedConsumerManager']
