"""任务持久化模块

负责解析Redis Stream消息，并将任务数据批量插入PostgreSQL数据库。
"""

import logging
from typing import Dict, List, Any
from datetime import datetime, timezone

from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert

from jettask.db.models.task import Task
from jettask.db.models.task_metrics_minute import TaskMetricsMinute
from jettask.db.models.task_runs_metrics_minute import TaskRunsMetricsMinute

logger = logging.getLogger(__name__)


class TaskPersistence:
    """任务持久化处理器

    职责：
    - 解析Stream消息为任务信息
    - 批量插入任务到PostgreSQL的tasks表
    - 处理插入失败的降级策略
    """

    def __init__(
        self,
        async_session_local: sessionmaker,
        namespace_id: str,
        namespace_name: str
    ):
        """初始化任务持久化处理器

        Args:
            async_session_local: SQLAlchemy会话工厂
            namespace_id: 命名空间ID
            namespace_name: 命名空间名称
        """
        self.AsyncSessionLocal = async_session_local
        self.namespace_id = namespace_id
        self.namespace_name = namespace_name


    async def batch_insert_tasks(self, tasks: List[Dict[str, Any]]) -> int:
        """批量插入任务（兼容 buffer.py 调用接口）

        Args:
            tasks: 任务记录列表

        Returns:
            实际插入的记录数
        """
        if not tasks:
            return 0

        logger.info(f"[BATCH INSERT] 批量插入 {len(tasks)} 条任务...")

        try:
            async with self.AsyncSessionLocal() as session:
                # 准备 ORM 数据
                # 🔧 关键说明：
                # - tasks 是分区表，按 trigger_time 分区，主键是 (stream_id, trigger_time)
                # - trigger_time 是任务触发时间（TIMESTAMP 类型）
                # - created_at 是记录的实际插入时间（DEFAULT NOW()）
                # - 同一个 stream_id 只会插入一次，业务逻辑保证不会重复
                insert_data = []
                for record in tasks:
                    # record 是从 consumer.py 传入的格式
                    scheduled_task_id = record.get('scheduled_task_id')
                    trigger_time = record.get('trigger_time')

                    # 将 Unix 时间戳转换为 datetime 对象
                    if isinstance(trigger_time, (int, float)):
                        trigger_time = datetime.fromtimestamp(trigger_time, timezone.utc)

                    insert_data.append({
                        'stream_id': record['stream_id'],
                        'queue': record['queue'],
                        'namespace': record['namespace'],
                        'scheduled_task_id': str(scheduled_task_id) if scheduled_task_id is not None else None,
                        'payload': record.get('payload', {}),
                        'priority': record.get('priority', 0),
                        'delay': record.get('delay', 0),
                        'trigger_time': trigger_time,
                        # created_at 由数据库 DEFAULT NOW() 自动设置
                        'source': record.get('source', 'redis_stream'),
                        'task_metadata': record.get('metadata', {})
                    })

                # 批量插入 - 使用 PostgreSQL 的 INSERT ON CONFLICT DO NOTHING
                # 使用约束名称而不是列名
                stmt = insert(Task).values(insert_data).on_conflict_do_nothing(
                    constraint='tasks_pkey'
                )

                await session.execute(stmt)

                # 同步更新聚合表（按分钟粒度）
                await self._update_metrics_aggregation(session, insert_data)

                await session.commit()

                logger.info(f"[BATCH INSERT] ✓ 成功插入 {len(insert_data)} 条任务")
                return len(insert_data)

        except Exception as e:
            logger.error(f"[BATCH INSERT] ✗ 批量插入失败: {e}", exc_info=True)
            return 0

    async def batch_update_tasks(self, updates: List[Dict[str, Any]]) -> int:
        """批量更新任务执行状态到 task_runs 表

        使用 PostgreSQL 的 INSERT ... ON CONFLICT DO UPDATE 实现 UPSERT 操作，
        如果记录存在则更新，不存在则插入。

        Args:
            updates: 更新记录列表，每条记录包含：
                - stream_id: Redis Stream ID（主键）
                - status: 任务状态
                - result: 执行结果
                - error: 错误信息
                - started_at: 开始时间
                - completed_at: 完成时间
                - retries: 重试次数

        Returns:
            实际更新的记录数
        """
        if not updates:
            return 0

        # logger.info(f"[BATCH UPDATE] 批量更新 {len(updates)} 条任务状态...")
        # logger.info(f"[BATCH UPDATE] 更新记录示例: {updates[0] if updates else 'N/A'}")

        try:
            from sqlalchemy.dialects.postgresql import insert
            from ..db.models import TaskRun
            from ..utils.serializer import loads_str
            from datetime import datetime, timezone

            # 对相同 stream_id 的记录进行去重，保留最新的
            # 使用字典，key 是 stream_id，value 是记录（后面的会覆盖前面的）
            deduplicated = {}
            for record in updates:
                stream_id = record['stream_id']
                deduplicated[stream_id] = record

            # 转换回列表
            unique_updates = list(deduplicated.values())

            if len(unique_updates) < len(updates):
                logger.info(
                    f"[BATCH UPDATE] 去重: {len(updates)} 条 → {len(unique_updates)} 条 "
                    f"(合并了 {len(updates) - len(unique_updates)} 条重复记录)"
                )

            async with self.AsyncSessionLocal() as session:
                # 准备 UPSERT 数据（用于写入 task_runs 表）
                upsert_data = []
                # 准备聚合统计数据（包含额外字段用于统计）
                aggregation_data = []

                for record in unique_updates:
                    logger.debug(f"处理记录: {record}")
                    # 解析 result 字段（如果是序列化的字符串）
                    result = record.get('result')
                    if result and isinstance(result, bytes):
                        try:
                            result = loads_str(result)
                        except Exception:
                            result = result.decode('utf-8') if isinstance(result, bytes) else result

                    # 解析 error 字段
                    error = record.get('error')
                    if error and isinstance(error, bytes):
                        error = error.decode('utf-8')

                    # 🔧 获取 trigger_time（任务触发时间，不会变化）
                    trigger_time = record.get('trigger_time')
                    if trigger_time is None:
                        # 如果没有 trigger_time，使用 started_at 作为后备
                        # （兼容旧数据，新数据必须有 trigger_time）
                        trigger_time = record.get('started_at')
                        logger.warning(f"Record missing trigger_time, using started_at as fallback: {record.get('stream_id')}")

                    # 获取并转换时间字段
                    started_at = record.get('started_at')
                    completed_at = record.get('completed_at')

                    # 将 Unix 时间戳转换为 datetime 对象
                    if isinstance(trigger_time, (int, float)):
                        trigger_time_dt = datetime.fromtimestamp(trigger_time, timezone.utc)
                    else:
                        trigger_time_dt = trigger_time

                    if isinstance(started_at, (int, float)):
                        started_at_dt = datetime.fromtimestamp(started_at, timezone.utc)
                    else:
                        started_at_dt = started_at

                    if isinstance(completed_at, (int, float)):
                        completed_at_dt = datetime.fromtimestamp(completed_at, timezone.utc)
                    else:
                        completed_at_dt = completed_at

                    # 计算执行时长（使用原始Unix时间戳）
                    duration = None
                    if started_at and completed_at:
                        duration = completed_at - started_at

                    # 解析 status 字段
                    status = record.get('status')
                    if status and isinstance(status, bytes):
                        status = status.decode('utf-8')

                    # 解析 consumer 字段
                    consumer = record.get('consumer')
                    if consumer and isinstance(consumer, bytes):
                        consumer = consumer.decode('utf-8')

                    # 🔧 获取 task_name（已从 consumer 提取）
                    task_name = record.get('task_name')

                    # task_runs 表记录
                    # 🔧 关键说明：
                    # - task_runs 是分区表，按 trigger_time 分区，主键是 (task_name, trigger_time, stream_id)
                    # - 主键顺序按粒度从粗到细：task_name > trigger_time > stream_id
                    # - task_name: 任务名称（粗粒度）
                    # - trigger_time: 任务触发时间（分区键），在任务创建时确定，后续不会变化（即使重试）
                    # - stream_id: Redis Stream ID（细粒度）
                    # - started_at: 任务实际开始执行时间，可能因重试而变化
                    # - created_at: 记录的实际插入时间（DEFAULT NOW()）
                    # - UPSERT 能通过 (task_name, trigger_time, stream_id) 正确匹配已有记录，避免重复
                    upsert_record = {
                        'task_name': task_name,
                        'trigger_time': trigger_time_dt,
                        'stream_id': record['stream_id'],
                        'status': status,
                        'result': result,
                        'error': error,
                        'started_at': started_at_dt,
                        'completed_at': completed_at_dt,
                        'retries': record.get('retries', 0),
                        'duration': duration,
                        'consumer': consumer,
                        # created_at 由数据库 DEFAULT NOW() 自动设置
                        'updated_at': datetime.now(timezone.utc),
                    }
                    logger.debug(f"upsert_record: {upsert_record}")
                    upsert_data.append(upsert_record)

                    # 聚合统计数据（包含 queue, namespace, trigger_time）
                    aggregation_record = {
                        'stream_id': record['stream_id'],
                        'task_name': task_name,
                        'status': status,
                        'started_at': started_at,
                        'completed_at': completed_at,
                        'retries': record.get('retries', 0),
                        'duration': duration,
                        # 这些字段来自原始 record，用于聚合统计
                        'queue': record.get('queue'),
                        'namespace': record.get('namespace'),
                        'trigger_time': record.get('trigger_time'),  # 用于计算时间桶
                    }
                    aggregation_data.append(aggregation_record)

                logger.info(f"[BATCH UPDATE] 准备写入 {len(upsert_data)} 条记录")
    
                # 批量 UPSERT - 如果存在则更新，不存在则插入
                stmt = insert(TaskRun).values(upsert_data)

                # 定义冲突时的更新策略
                # 使用 COALESCE 避免用 NULL 覆盖已有数据
                from sqlalchemy import func
                stmt = stmt.on_conflict_do_update(
                    constraint='task_runs_pkey',  # 主键：(task_name, trigger_time, stream_id)
                    set_={
                        # status 总是更新（状态变化）
                        'status': stmt.excluded.status,
                        # 其他字段：如果新值不是 NULL，则更新；否则保留旧值
                        'result': func.coalesce(stmt.excluded.result, TaskRun.result),
                        'error': func.coalesce(stmt.excluded.error, TaskRun.error),
                        'started_at': func.coalesce(stmt.excluded.started_at, TaskRun.started_at),
                        'completed_at': func.coalesce(stmt.excluded.completed_at, TaskRun.completed_at),
                        'retries': func.coalesce(stmt.excluded.retries, TaskRun.retries),
                        'duration': func.coalesce(stmt.excluded.duration, TaskRun.duration),
                        'consumer': func.coalesce(stmt.excluded.consumer, TaskRun.consumer),
                        'task_name': func.coalesce(stmt.excluded.task_name, TaskRun.task_name),
                        # trigger_time 是主键的一部分，不能更新
                        # created_at 在首次插入时由数据库 DEFAULT NOW() 设置，后续更新不会改变
                        # updated_at 总是更新为当前时间
                        'updated_at': stmt.excluded.updated_at,
                    }
                )

                await session.execute(stmt)

                # 🔧 同步更新聚合统计表（使用包含 queue/namespace/trigger_time 的数据）
                await self._update_task_runs_metrics_aggregation(session, aggregation_data)

                await session.commit()

                logger.info(f"[BATCH UPDATE] ✓ 成功更新 {len(upsert_data)} 条任务状态")
                return len(upsert_data)

        except Exception as e:
            logger.error(f"[BATCH UPDATE] ✗ 批量更新失败: {e}", exc_info=True)
            return 0

    async def _update_metrics_aggregation(self, session, tasks_data: List[Dict[str, Any]]) -> None:
        """
        更新任务指标聚合表（按分钟粒度）

        在同一事务中，将新插入的任务统计到聚合表中。
        使用 INSERT ON CONFLICT DO UPDATE 来处理并发更新。

        Args:
            session: 数据库会话（在同一事务中）
            tasks_data: 任务数据列表
        """
        if not tasks_data:
            return

        logger.debug(f"Updating metrics aggregation for {len(tasks_data)} tasks")

        # 按照 (namespace, queue, time_bucket) 分组统计
        from collections import defaultdict

        metrics_map = defaultdict(int)

        for task in tasks_data:
            # 获取任务触发时间（用于聚合统计）
            trigger_time = task.get('trigger_time')
            if not trigger_time:
                continue

            # 将 Unix 时间戳转换为 datetime
            if isinstance(trigger_time, (int, float)):
                trigger_datetime = datetime.fromtimestamp(trigger_time, timezone.utc)
            elif isinstance(trigger_time, str):
                trigger_datetime = datetime.fromisoformat(trigger_time.replace('Z', '+00:00'))
            else:
                trigger_datetime = trigger_time

            # 计算分钟级别的时间桶（去掉秒和微秒）
            time_bucket = trigger_datetime.replace(second=0, microsecond=0)

            # 分组键：(namespace, queue, time_bucket)
            key = (
                task['namespace'],
                task['queue'],
                time_bucket
            )

            metrics_map[key] += 1

        # 批量更新聚合表
        metrics_data = []
        for (namespace, queue, time_bucket), count in metrics_map.items():
            metrics_data.append({
                'namespace': namespace,
                'queue': queue,
                'time_bucket': time_bucket,
                'task_count': count,
                'updated_at': datetime.now(timezone.utc)
            })

        if not metrics_data:
            return

        # 使用 INSERT ON CONFLICT DO UPDATE 来递增计数器
        stmt = insert(TaskMetricsMinute).values(metrics_data)
        stmt = stmt.on_conflict_do_update(
            # 主键冲突时更新
            index_elements=['namespace', 'queue', 'time_bucket'],
            # 递增 task_count，更新 updated_at
            set_={
                'task_count': TaskMetricsMinute.task_count + stmt.excluded.task_count,
                'updated_at': stmt.excluded.updated_at
            }
        )

        await session.execute(stmt)
        logger.debug(f"Updated {len(metrics_data)} metric entries in aggregation table")

    async def _update_task_runs_metrics_aggregation(
        self, session, tasks_data: List[Dict[str, Any]]
    ) -> None:
        """
        更新任务执行指标聚合表（按分钟粒度）

        在同一事务中，将任务执行状态统计到聚合表中。
        使用 INSERT ON CONFLICT DO UPDATE 来处理并发更新。

        Args:
            session: 数据库会话（在同一事务中）
            tasks_data: 任务执行数据列表（包含 status, duration, trigger_time, started_at 等）
        """
        if not tasks_data:
            return

        logger.debug(f"Updating task_runs metrics aggregation for {len(tasks_data)} tasks")

        from sqlalchemy import func

        # 按照 (time_bucket, namespace, queue, task_name) 分组统计
        # 使用字典存储聚合数据
        metrics_map = {}

        for task in tasks_data:
            # 获取任务开始时间（用于确定时间桶）
            started_at = task.get('started_at')
            if not started_at:
                # 如果没有开始时间，跳过
                continue

            # 计算分钟级别的时间桶
            # 将 Unix 时间戳转换为 datetime，然后去掉秒和微秒
            bucket_dt = datetime.fromtimestamp(started_at, tz=timezone.utc)
            time_bucket = bucket_dt.replace(second=0, microsecond=0)

            # 获取命名空间
            namespace = task.get('namespace') or 'default'

            # 获取队列名称
            queue = task.get('queue') or 'unknown'

            # 获取任务名称
            task_name = task.get('task_name') or 'unknown'

            # 分组键：(time_bucket, namespace, queue, task_name)
            key = (time_bucket, namespace, queue, task_name)

            # 初始化该键的聚合数据
            if key not in metrics_map:
                metrics_map[key] = {
                    'total_count': 0,
                    'success_count': 0,
                    'failed_count': 0,
                    'retry_count': 0,
                    'total_duration': 0.0,
                    'max_duration': None,
                    'min_duration': None,
                    'total_delay': 0.0,
                    'max_delay': None,
                    'min_delay': None,
                    'running_concurrency': 0,
                }

            metrics = metrics_map[key]

            # 更新计数
            metrics['total_count'] += 1

            # 根据状态更新成功/失败计数
            status = task.get('status')
            if status == 'success':
                metrics['success_count'] += 1
            elif status in ('failed', 'error'):
                metrics['failed_count'] += 1

            # 累加重试次数
            retries = task.get('retries') or 0
            metrics['retry_count'] += retries

            # 累加执行时长
            duration = task.get('duration')
            if duration is not None and duration > 0:
                metrics['total_duration'] += duration
                # 更新最大/最小执行时间
                if metrics['max_duration'] is None or duration > metrics['max_duration']:
                    metrics['max_duration'] = duration
                if metrics['min_duration'] is None or duration < metrics['min_duration']:
                    metrics['min_duration'] = duration

            # 计算执行延迟 (started_at - trigger_time)
            trigger_time = task.get('trigger_time')
            if trigger_time is not None and started_at is not None:
                delay = started_at - trigger_time
                if delay >= 0:  # 只处理正延迟
                    metrics['total_delay'] += delay
                    # 更新最大/最小延迟
                    if metrics['max_delay'] is None or delay > metrics['max_delay']:
                        metrics['max_delay'] = delay
                    if metrics['min_delay'] is None or delay < metrics['min_delay']:
                        metrics['min_delay'] = delay

            # 并发计数（简单实现：每个任务在其开始分钟内计数 +1）
            metrics['running_concurrency'] += 1

        if not metrics_map:
            return

        # 批量更新聚合表
        metrics_data = []
        for (time_bucket, namespace, queue, task_name), metrics in metrics_map.items():
            metrics_data.append({
                'time_bucket': time_bucket,
                'namespace': namespace,  # 🔧 添加 namespace
                'queue': queue,  # 🔧 添加 queue
                'task_name': task_name,
                'total_count': metrics['total_count'],
                'success_count': metrics['success_count'],
                'failed_count': metrics['failed_count'],
                'retry_count': metrics['retry_count'],
                'total_duration': metrics['total_duration'],
                'max_duration': metrics['max_duration'],
                'min_duration': metrics['min_duration'],
                'total_delay': metrics['total_delay'],
                'max_delay': metrics['max_delay'],
                'min_delay': metrics['min_delay'],
                'running_concurrency': metrics['running_concurrency'],
                'updated_at': datetime.now(timezone.utc)
            })

        if not metrics_data:
            return

        # 使用 INSERT ON CONFLICT DO UPDATE
        stmt = insert(TaskRunsMetricsMinute).values(metrics_data)
        stmt = stmt.on_conflict_do_update(
            # 主键冲突时更新（主键为 time_bucket, namespace, queue, task_name）
            index_elements=['time_bucket', 'namespace', 'queue', 'task_name'],
            set_={
                # 累加计数类指标
                'total_count': TaskRunsMetricsMinute.total_count + stmt.excluded.total_count,
                'success_count': TaskRunsMetricsMinute.success_count + stmt.excluded.success_count,
                'failed_count': TaskRunsMetricsMinute.failed_count + stmt.excluded.failed_count,
                'retry_count': TaskRunsMetricsMinute.retry_count + stmt.excluded.retry_count,
                # 累加执行时间
                'total_duration': TaskRunsMetricsMinute.total_duration + stmt.excluded.total_duration,
                # 更新最大/最小执行时间
                'max_duration': func.greatest(
                    func.coalesce(TaskRunsMetricsMinute.max_duration, stmt.excluded.max_duration),
                    stmt.excluded.max_duration
                ),
                'min_duration': func.least(
                    func.coalesce(TaskRunsMetricsMinute.min_duration, stmt.excluded.min_duration),
                    stmt.excluded.min_duration
                ),
                # 累加延迟
                'total_delay': TaskRunsMetricsMinute.total_delay + stmt.excluded.total_delay,
                # 更新最大/最小延迟
                'max_delay': func.greatest(
                    func.coalesce(TaskRunsMetricsMinute.max_delay, stmt.excluded.max_delay),
                    stmt.excluded.max_delay
                ),
                'min_delay': func.least(
                    func.coalesce(TaskRunsMetricsMinute.min_delay, stmt.excluded.min_delay),
                    stmt.excluded.min_delay
                ),
                # 更新并发峰值（取最大值）
                'running_concurrency': func.greatest(
                    TaskRunsMetricsMinute.running_concurrency,
                    stmt.excluded.running_concurrency
                ),
                # 更新时间戳
                'updated_at': stmt.excluded.updated_at
            }
        )

        await session.execute(stmt)
        logger.debug(f"Updated {len(metrics_data)} task_runs metric entries in aggregation table")
