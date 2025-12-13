"""批量缓冲区管理器

负责收集任务数据和ACK信息，批量写入数据库并ACK。
支持 INSERT 和 UPDATE 两种操作类型。
"""

import time
import asyncio
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class BatchBuffer:
    """批量缓冲区管理器

    负责：
    1. 收集任务数据和ACK信息
    2. 判断是否应该刷新（批量大小或超时）
    3. 批量写入数据库并ACK
    4. 自动定时刷新机制
    """

    def __init__(
        self,
        max_size: int = 1000,
        max_delay: float = 5.0,
        operation_type: str = 'insert',  # 'insert' 或 'update'
        redis_client_getter=None  # 获取 Redis 客户端的函数
    ):
        """初始化缓冲区

        Args:
            max_size: 缓冲区最大容量（条数）
            max_delay: 最大延迟时间（秒）
            operation_type: 操作类型，'insert' 或 'update'
            redis_client_getter: 获取 Redis 客户端的可调用对象（用于批量获取数据）
        """
        self.max_size = max_size
        self.max_delay = max_delay
        self.operation_type = operation_type
        self.redis_client_getter = redis_client_getter

        # 任务数据缓冲区
        self.records: List[Dict[str, Any]] = []
        self.contexts: List[Any] = []  # 保存 TaskContext 用于 ACK

        # 刷新控制
        self.last_flush_time = time.time()
        self.flush_lock = asyncio.Lock()

        # 统计信息
        self.total_flushed = 0
        self.flush_count = 0

        # 定时刷新任务
        self._auto_flush_task: Optional[asyncio.Task] = None
        self._running = False
        self._db_manager = None

    async def add(self, record: dict, context: Any = None):
        """添加到缓冲区（线程安全）

        Args:
            record: 任务数据或更新数据
            context: TaskContext（用于 ACK）
        """
        # 🔧 跳过 TASK_CHANGES 队列的 INSERT 操作
        if self.operation_type == 'insert' and record.get('queue') == 'TASK_CHANGES':
            logger.debug(f"跳过 TASK_CHANGES 队列的 INSERT 操作: {record.get('stream_id')}")
            # 直接确认消息，不写入数据库
            if context and hasattr(context, 'ack'):
                try:
                    context.ack()
                    logger.debug(f"  ✓ 已确认 TASK_CHANGES 消息: {record.get('stream_id')}")
                except Exception as e:
                    logger.error(f"  ✗ 确认 TASK_CHANGES 消息失败: {e}")
            return

        self.records.append(record)
        if context:
            self.contexts.append(context)

    def should_flush(self) -> bool:
        """判断是否应该刷新

        Returns:
            是否需要刷新
        """
        if not self.records:
            return False

        # 缓冲区满了
        if len(self.records) >= self.max_size:
            logger.debug(
                f"[{self.operation_type.upper()}] 缓冲区已满 "
                f"({len(self.records)}/{self.max_size})，触发刷新"
            )
            return True

        # 超时了
        elapsed = time.time() - self.last_flush_time
        if elapsed >= self.max_delay:
            logger.debug(
                f"[{self.operation_type.upper()}] 缓冲区超时 "
                f"({elapsed:.1f}s >= {self.max_delay}s)，触发刷新"
            )
            return True

        return False

    async def flush(self, db_manager):
        """刷新缓冲区到数据库

        1. 加锁并拷贝数据，立即清空原始缓冲区（避免数据丢失）
        2. (UPDATE模式) 批量从 Redis 获取任务数据
        3. 批量写入数据库
        4. 批量ACK（如果有context）

        Args:
            db_manager: 数据库管理器，需要有 batch_insert_tasks 或 batch_update_tasks 方法
        """
        # 1. 加锁并拷贝数据，立即清空原始缓冲区
        if not self.records:
            return 0

        # 拷贝数据
        records_to_process = self.records.copy()
        contexts_to_process = self.contexts.copy()
        count = len(records_to_process)

        # 立即清空原始缓冲区，释放锁（避免阻塞新数据的 add）
        self.records.clear()
        self.contexts.clear()
        self.last_flush_time = time.time()

        # 2. 解锁后处理数据（使用拷贝的数据）
        start_time = time.time()

        try:
            logger.info(f"[{self.operation_type.upper()}] 开始批量刷新 {count} 条记录...")

            # print(f'{records_to_process=}')
            # 3. (UPDATE 模式) 批量从 Redis 获取任务数据
            if self.operation_type == 'update' and self.redis_client_getter:
                await self._batch_fetch_task_info_from_redis(records_to_process)

            # print(f'{records_to_process=}')
            # 4. 批量写入数据库
            if self.operation_type == 'insert':
                await db_manager.batch_insert_tasks(records_to_process)
                logger.info(f"  ✓ 批量插入 {count} 条任务记录")
            else:  # update
                await db_manager.batch_update_tasks(records_to_process)
                logger.info(f"  ✓ 批量更新 {count} 条任务状态")
            # 5. 批量ACK（使用 TaskContext.acks）
            if contexts_to_process:
                # 🔧 按 context 分组（因为不同的 ctx 可能有不同的 group_name）
                # 使用 (queue, group_name) 作为分组键
                ctx_groups = {}
                for ctx in contexts_to_process:
                    if hasattr(ctx, 'event_id') and hasattr(ctx, 'acks'):
                        # 使用 (queue, group_name) 作为分组键
                        group_key = (ctx.queue, ctx.group_name)
                        if group_key not in ctx_groups:
                            ctx_groups[group_key] = {'ctx': ctx, 'event_ids': []}
                        ctx_groups[group_key]['event_ids'].append(ctx.event_id)

                # 为每个分组调用 ctx.acks
                total_acked = 0
                for group_key, group_data in ctx_groups.items():
                    ctx = group_data['ctx']
                    event_ids = group_data['event_ids']
                    try:
                        ctx.acks(event_ids)
                        total_acked += len(event_ids)
                        logger.debug(
                            f"  ✓ ACK {len(event_ids)} 条消息 "
                            f"(queue={group_key[0]}, group={group_key[1]})"
                        )
                    except Exception as e:
                        logger.error(
                            f"  ✗ ACK 失败 (queue={group_key[0]}, group={group_key[1]}): {e}"
                        )

                if total_acked > 0:
                    logger.info(f"  ✓ 批量确认 {total_acked} 条消息")

            # 6. 统计
            self.total_flushed += count
            self.flush_count += 1
            elapsed = time.time() - start_time

            logger.info(
                f"[{self.operation_type.upper()}] ✓ 批量刷新完成! "
                f"本次: {count}条, "
                f"耗时: {elapsed:.3f}s, "
                f"总计: {self.total_flushed}条 ({self.flush_count}次刷新)"
            )

            return count

        except Exception as e:
            logger.error(
                f"[{self.operation_type.upper()}] ✗ 批量刷新失败: {e}",
                exc_info=True
            )
            # 失败时数据已经丢失（已从缓冲区移除），记录错误
            logger.error(f"  ✗ 丢失 {count} 条记录")
            raise

    def get_stats(self) -> dict:
        """获取统计信息

        Returns:
            统计信息字典
        """
        return {
            'operation_type': self.operation_type,
            'current_size': len(self.records),
            'max_size': self.max_size,
            'total_flushed': self.total_flushed,
            'flush_count': self.flush_count,
            'avg_per_flush': self.total_flushed // self.flush_count if self.flush_count > 0 else 0
        }

    async def _auto_flush_loop(self):
        """自动刷新循环

        定期检查缓冲区，如果满足刷新条件则自动刷新
        """
        logger.info(f"[{self.operation_type.upper()}] 启动自动刷新任务，检查间隔: {self.max_delay}s")

        while self._running:
            try:
                # 等待一段时间，使用 max_delay 作为检查间隔
                await asyncio.sleep(self.max_delay)

                # 检查是否需要刷新
                if self.should_flush():
                    logger.debug(
                        f"[{self.operation_type.upper()}] 自动刷新触发，"
                        f"缓冲区大小: {len(self.records)}"
                    )
                    await self.flush(self._db_manager)

            except asyncio.CancelledError:
                logger.info(f"[{self.operation_type.upper()}] 自动刷新任务被取消")
                break
            except Exception as e:
                logger.error(
                    f"[{self.operation_type.upper()}] 自动刷新任务出错: {e}",
                    exc_info=True
                )
                # 继续运行，不中断循环

    async def start_auto_flush(self, db_manager):
        """启动自动刷新任务（异步方法）

        Args:
            db_manager: 数据库管理器
        """
        if self._auto_flush_task is not None and not self._auto_flush_task.done():
            logger.warning(f"[{self.operation_type.upper()}] 自动刷新任务已在运行")
            return

        self._db_manager = db_manager
        self._running = True
        self._auto_flush_task = asyncio.create_task(self._auto_flush_loop())
        logger.info(f"[{self.operation_type.upper()}] 自动刷新任务已启动")

    async def stop_auto_flush(self):
        """停止自动刷新任务"""
        self._running = False

        if self._auto_flush_task is not None and not self._auto_flush_task.done():
            self._auto_flush_task.cancel()
            try:
                await self._auto_flush_task
            except asyncio.CancelledError:
                pass
            logger.info(f"[{self.operation_type.upper()}] 自动刷新任务已停止")

        # 最后刷新一次，确保不丢数据
        if self.records and self._db_manager:
            logger.info(f"[{self.operation_type.upper()}] 执行最终刷新，剩余 {len(self.records)} 条记录")
            await self.flush(self._db_manager)
    async def _batch_fetch_task_info_from_redis(self, records: List[Dict[str, Any]]):
        """批量从 Redis 获取任务信息（仅用于 UPDATE 模式）

        使用 pipeline 批量获取任务信息，大幅减少网络往返

        Args:
            records: 要处理的记录列表（传入的拷贝数据）
        """
        if not records or not self.redis_client_getter:
            return

        # 导入辅助函数
        from .consumer import _parse_task_info

        redis_client = self.redis_client_getter()
        if not redis_client:
            logger.error("无法获取 Redis 客户端")
            return

        # 收集所有需要查询的 task_id
        task_ids = [record['task_id'] for record in records if 'task_id' in record]
        if not task_ids:
            return

        logger.info(f"  ⏳ 使用 pipeline 批量获取 {len(task_ids)} 个任务信息...")

        try:
            # 使用 pipeline 批量查询
            pipeline = redis_client.pipeline()
            for task_id in task_ids:
                pipeline.hgetall(task_id)

            # 执行 pipeline
            results = await pipeline.execute()

            # 解析结果并更新 records
            valid_count = 0
            for record, task_info in zip(records, results):
                if not task_info:
                    logger.warning(f"  ⚠ 无法找到任务状态信息: {record.get('task_id')}")
                    continue

                # 解析任务信息
                parsed_info = _parse_task_info(task_info)
                # 更新 record，添加解析后的字段
                record.update(parsed_info)
                valid_count += 1

            logger.info(f"  ✓ 成功获取 {valid_count}/{len(task_ids)} 个任务信息")

        except Exception as e:
            logger.error(f"  ✗ 批量获取任务信息失败: {e}", exc_info=True)
