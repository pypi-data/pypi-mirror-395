"""PostgreSQL Consumer - 基于通配符队列的新实现

完全替换旧的 consumer.py 实现，使用 Jettask 通配符队列功能。
"""

import time
import logging
from datetime import datetime, timezone

from jettask import Jettask
from jettask.core.context import TaskContext
from jettask.db.connector import get_pg_engine_and_factory, DBConfig
from .buffer import BatchBuffer
from .persistence import TaskPersistence

logger = logging.getLogger(__name__)


def _decode_redis_field(value, field_type='str'):
    """解析 Redis 字段值（处理 bytes/str 类型）

    Args:
        value: Redis 返回的值（可能是 bytes 或 str）
        field_type: 目标类型 ('str', 'int', 'float')

    Returns:
        解析后的值，如果解析失败返回 None
    """
    if not value:
        return None

    # 如果是 bytes，先解码为 str
    if isinstance(value, bytes):
        try:
            value = value.decode('utf-8')
        except Exception:
            return None

    # 类型转换
    try:
        if field_type == 'int':
            return int(value) if value else 0
        elif field_type == 'float':
            return float(value) if value else None
        else:  # str
            return value
    except (ValueError, TypeError):
        return None


def _extract_task_name_from_consumer(consumer: str) -> str:
    """从 consumer 字段提取 task_name

    consumer 格式: YYDG-15b50489-9274-robust_bench2:8
    提取逻辑: 用'-'分割取最后一个，再用':'分割取第一个
    结果: robust_bench2

    Args:
        consumer: consumer 字段值

    Returns:
        task_name，如果解析失败返回 None
    """
    if not consumer:
        return None

    try:
        # 用 '-' 分割，取最后一个
        last_part = consumer.split('-')[-1]
        # 用 ':' 分割，取第一个
        task_name = last_part.split(':')[0]
        return task_name if task_name else None
    except (IndexError, AttributeError):
        logger.warning(f"Failed to extract task_name from consumer: {consumer}")
        return None


def _parse_task_info(task_info: dict) -> dict:
    """批量解析任务信息字段

    Args:
        task_info: Redis hgetall 返回的任务信息字典

    Returns:
        解析后的字段字典
    """
    consumer = _decode_redis_field(task_info.get(b'consumer'), 'str')

    # # 🔧 从 consumer 字段提取 task_name
    # task_name = _extract_task_name_from_consumer(consumer)

    return {
        'retries': _decode_redis_field(task_info.get(b'retries'), 'int'),
        'trigger_time': _decode_redis_field(task_info.get(b'trigger_time_float'), 'float'),
        'started_at': _decode_redis_field(task_info.get(b'started_at'), 'float'),
        'completed_at': _decode_redis_field(task_info.get(b'completed_at'), 'float'),
        'consumer': consumer,
        'queue': _decode_redis_field(task_info.get(b'queue'), 'str'),  # 🔧 添加 queue 字段
        'status': _decode_redis_field(task_info.get(b'status'), 'str'),
        'result': task_info.get(b'result'),  # 保持原始 bytes
        'error': task_info.get(b'exception') or task_info.get(b'error'),  # 保持原始 bytes
    }


def _extract_event_id_from_task_id(task_id: str) -> str:
    """从 task_id 中提取 event_id

    task_id 格式: prefix:TASK:event_id:queue:task_name

    Args:
        task_id: 任务 ID

    Returns:
        event_id (stream_id)，如果格式无效返回 None
    """
    if not task_id:
        return None

    parts = task_id.split(':')
    if len(parts) >= 3:
        return parts[2]  # 提取 event_id

    return None


def _extract_task_name_from_task_id(task_id: str) -> str:
    """从 task_id 中提取 task_name

    task_id 格式: prefix:TASK:event_id:queue:task_name

    Args:
        task_id: 任务 ID

    Returns:
        task_name，如果格式无效返回 None
    """
    if not task_id:
        return None

    parts = task_id.split(':')
    if len(parts) >= 5:
        return parts[4]  # 提取 task_name

    return None


class PostgreSQLConsumer:
    """PostgreSQL Consumer - 基于通配符队列

    核心特性：
    1. 使用 @app.task(queue='*') 监听所有队列
    2. 使用 @app.task(queue='TASK_CHANGES') 处理状态更新
    3. 批量 INSERT 和 UPDATE
    4. 自动队列发现（Jettask 内置）
    """

    def __init__(
        self,
        pg_config,  # 可以是字典或配置对象
        redis_config,  # 可以是字典或配置对象
        prefix: str = "jettask",
        namespace_id: str = None,
        namespace_name: str = None,
        batch_size: int = 1000,
        flush_interval: float = 5.0
    ):
        """初始化 PG Consumer

        Args:
            pg_config: PostgreSQL配置（字典或对象）
            redis_config: Redis配置（字典或对象）
            prefix: Redis键前缀
            node_id: 节点ID（兼容旧接口，不使用）
            namespace_id: 命名空间ID
            namespace_name: 命名空间名称
            enable_backlog_monitor: 是否启用积压监控（兼容旧接口，不使用）
            backlog_monitor_interval: 积压监控间隔（兼容旧接口，不使用）
            batch_size: 批量大小
            flush_interval: 刷新间隔（秒）
        """
        self.pg_config = pg_config
        self.redis_config = redis_config
        self.redis_prefix = prefix
        self.namespace_id = namespace_id
        self.namespace_name = namespace_name or "default"

        # 构建 Redis URL（兼容字典和对象两种格式）
        if isinstance(redis_config, dict):
            # 字典格式 - 优先使用 'url' 字段
            redis_url = redis_config.get('url') or redis_config.get('redis_url')
            if not redis_url:
                # 从独立字段构建
                password = redis_config.get('password', '')
                host = redis_config.get('host', 'localhost')
                port = redis_config.get('port', 6379)
                db = redis_config.get('db', 0)
                redis_url = f"redis://"
                if password:
                    redis_url += f":{password}@"
                redis_url += f"{host}:{port}/{db}"
        else:
            # 对象格式
            redis_url = f"redis://"
            if hasattr(redis_config, 'password') and redis_config.password:
                redis_url += f":{redis_config.password}@"
            redis_url += f"{redis_config.host}:{redis_config.port}/{redis_config.db}"

        self.redis_url = redis_url
        logger.debug(f"构建 Redis URL: {redis_url}")

        # 数据库引擎和会话（将在 start 时初始化）
        self.async_engine = None
        self.AsyncSessionLocal = None
        self.db_manager = None

        # 创建 Jettask 应用
        self.app = Jettask(
            redis_url=redis_url,
            redis_prefix=prefix
        )

        # 创建两个独立的批量缓冲区
        # 1. INSERT 缓冲区（用于新任务持久化）
        self.insert_buffer = BatchBuffer(
            max_size=batch_size,
            max_delay=flush_interval,
            operation_type='insert'
        )

        # 2. UPDATE 缓冲区（用于任务状态更新）
        self.update_buffer = BatchBuffer(
            max_size=batch_size // 2,  # 状态更新通常更频繁，用较小的批次
            max_delay=flush_interval,
            operation_type='update',
            redis_client_getter=lambda: self.app.async_binary_redis  # 批量获取任务信息
        )

        # 注册任务
        self._register_tasks()

        # 运行控制
        self._running = False

        # auto flush 启动标志（在 worker 进程中懒加载启动）
        self._auto_flush_started = False

    async def _ensure_auto_flush_started(self):
        """确保 auto flush 在 worker 进程中启动（只启动一次）"""
        if not self._auto_flush_started:
            logger.info("[Worker进程] 启动缓冲区自动刷新任务...")
            await self.insert_buffer.start_auto_flush(self.db_manager)
            await self.update_buffer.start_auto_flush(self.db_manager)
            self._auto_flush_started = True
            logger.info("[Worker进程] ✓ 缓冲区自动刷新任务已启动")

    def _register_tasks(self):
        """注册任务处理器"""
        # 创建闭包函数来访问实例属性
        consumer = self  # 捕获 self 引用

        @self.app.task(queue='*', auto_ack=False, name=f'{self.namespace_name}._handle_persist_task')
        async def _handle_persist_task(ctx: TaskContext, *args, **kwargs):
            # print(f'{args=} {kwargs=}')
            return await consumer._do_handle_persist_task(ctx, *args, **kwargs)

        @self.app.task(queue='TASK_CHANGES', auto_ack=False, name=f'{self.namespace_name}._handle_status_update')
        async def _handle_status_update(ctx: TaskContext, **kwargs):
            # print(f'{kwargs=}')

            return await consumer._do_handle_status_update(ctx, **kwargs)

    async def _do_handle_persist_task(self, ctx: TaskContext, *args, **kwargs):
        """处理任务持久化（INSERT）

        使用通配符 queue='*' 监听所有队列
        Jettask 会自动发现新队列并开始消费

        Args:
            ctx: Jettask 自动注入的任务上下文（包含 queue, event_id 等）
            **kwargs: 任务的原始数据字段
        """
        # 🔧 确保 auto flush 在 worker 进程中启动（懒加载）
        await self._ensure_auto_flush_started()

        # 添加关键日志，确认方法被调用
        # logger.info(f"[持久化任务] 收到消息 - 队列: {ctx.queue}, Stream ID: {ctx.event_id}, task_name: {kwargs.get('task_name')}, metadata: {ctx.metadata}")

        # 跳过 TASK_CHANGES 队列（由另一个任务处理）
        if ctx.queue == f'TASK_CHANGES':
            logger.debug(f"[持久化任务] 跳过 TASK_CHANGES 队列: {ctx.event_id}")
            ctx.acks([ctx.event_id])
            return

        try:

            # 🔧 从 ctx.metadata 中提取元数据
            metadata = ctx.metadata or {}

            trigger_time = metadata.get('trigger_time', time.time())
            if isinstance(trigger_time, (str, bytes)):
                trigger_time = float(trigger_time)

            priority = metadata.get('priority', 0)
            if priority and isinstance(priority, (str, bytes)):
                priority = int(priority)
            elif priority is None:
                priority = 0

            # 提取 delay 参数
            delay = metadata.get('delay', 0)
            if delay and isinstance(delay, (str, bytes)):
                delay = float(delay)
            elif delay is None:
                delay = 0

            scheduled_task_id = metadata.get('scheduled_task_id')

            payload = {
                'args': args,
                'kwargs': kwargs,
            }

            # 🔧 关键说明：
            # - tasks 是分区表，按 trigger_time 分区，主键是 (stream_id, trigger_time)
            # - trigger_time 在任务生命周期中不会变化，确保 UPSERT 能正确匹配已有记录
            # - created_at 使用数据库默认值（NOW()），表示记录真正的创建时间
            # - 不要在 record 中设置 created_at，让数据库自动生成
            record = {
                'stream_id': ctx.event_id,
                'queue': ctx.queue.replace(f'{self.redis_prefix}:QUEUE:', ''),
                'payload': payload,
                'priority': priority,
                'delay': delay,
                # created_at 不设置，使用数据库默认值
                'trigger_time': trigger_time,  # 直接存储 Unix 时间戳
                'scheduled_task_id': scheduled_task_id,
                'namespace': self.namespace_name,
                'source': 'scheduler' if scheduled_task_id else 'redis_stream',
            }

            # 添加到缓冲区（不立即处理，不立即 ACK）
            await self.insert_buffer.add(record, ctx)
            logger.debug(f"[持久化任务] 已添加到缓冲区，当前大小: {len(self.insert_buffer.records)}/{self.insert_buffer.max_size}")

            # 检查是否需要刷新（批量大小或超时）
            if self.insert_buffer.should_flush():
                logger.info(f"[持久化任务] 触发刷新，缓冲区大小: {len(self.insert_buffer.records)}")
                await self.insert_buffer.flush(self.db_manager)

            # 同时检查 UPDATE 缓冲区是否需要刷新（利用这次机会）
            if self.update_buffer.should_flush():
                await self.update_buffer.flush(self.db_manager)

        except Exception as e:
            logger.error(f"持久化任务失败: {e}", exc_info=True)
            # 出错也要 ACK，避免消息堆积
            ctx.acks([ctx.event_id])

    async def _do_handle_status_update(self, ctx: TaskContext, **kwargs):
        """处理任务状态更新（UPDATE）

        消费 TASK_CHANGES 队列，批量更新数据库中的任务状态

        Args:
            ctx: Jettask 自动注入的任务上下文
            **kwargs: 任务的原始数据字段（包含 task_id）
        """
        # 添加关键日志，确认方法被调用
        # logger.info(f"[状态更新] 收到消息 - 队列: {ctx.queue}, Stream ID: {ctx.event_id}, kwargs: {kwargs}")

        # 🔧 确保 auto flush 在 worker 进程中启动（懒加载）
        await self._ensure_auto_flush_started()

        try:
            # 从消息中获取 task_id
            task_id = kwargs.get('task_id')
            if not task_id:
                logger.warning(f"TASK_CHANGES 消息缺少 task_id: {ctx.event_id}")
                ctx.acks([ctx.event_id])
                return

            # 从 task_id 中提取 event_id (stream_id) 和 task_name
            event_id = _extract_event_id_from_task_id(task_id)
            if not event_id:
                logger.error(f"无效的 task_id 格式: {task_id}")
                ctx.acks([ctx.event_id])
                return

            task_name = _extract_task_name_from_task_id(task_id)

            # print(f'{task_id=} {event_id=} {task_name=}')
            # 只保存 task_id 和 task_name，延迟到批量刷新时再获取任务信息
            update_record = {
                'task_id': task_id,
                'stream_id': event_id,
                'task_name': task_name,
                'namespace': self.namespace_name,  # 🔧 添加 namespace 字段
            }

            # 添加到状态更新缓冲区
            await self.update_buffer.add(update_record, ctx)
            logger.debug(f"[状态更新] 已添加到缓冲区，当前大小: {len(self.update_buffer.records)}/{self.update_buffer.max_size}")

            # 检查是否需要刷新（批量大小或超时）
            if self.update_buffer.should_flush():
                logger.info(f"[状态更新] 触发刷新，缓冲区大小: {len(self.update_buffer.records)}")
                await self.update_buffer.flush(self.db_manager)

            # 同时检查 INSERT 缓冲区是否需要刷新（利用这次机会）
            if self.insert_buffer.should_flush():
                await self.insert_buffer.flush(self.db_manager)

        except Exception as e:
            logger.error(f"更新任务状态失败: {e}", exc_info=True)
            # 出错也要 ACK
            ctx.acks([ctx.event_id])

    async def start(self, concurrency: int = 4, prefetch_multiplier: int = 1):
        """启动 Consumer

        Args:
            concurrency: 并发数
        """
        logger.info(f"Starting PostgreSQL consumer (wildcard queue mode)")
        logger.info(f"Namespace: {self.namespace_name} ({self.namespace_id or 'N/A'})")

        # 1. 使用 connector.py 统一管理数据库连接
        # 解析 PostgreSQL 配置为标准 DSN
        dsn = DBConfig.parse_pg_config(self.pg_config)

        # 使用全局单例引擎和会话工厂
        self.async_engine, self.AsyncSessionLocal = get_pg_engine_and_factory(
            dsn,
            pool_size=50,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=300,
            echo=False
        )

        logger.debug(f"使用全局 PostgreSQL 连接池: {dsn[:50]}...")

        # 2. 初始化任务持久化管理器
        self.db_manager = TaskPersistence(
            async_session_local=self.AsyncSessionLocal,
            namespace_id=self.namespace_id,
            namespace_name=self.namespace_name
        )

        # 3. 设置运行状态
        self._running = True

        # 4. 注意：不在主进程中启动 auto flush
        # auto flush 会在 worker 子进程中懒加载启动（首次任务执行时）
        # 这样避免进程隔离问题（主进程的 asyncio.Task 无法在子进程中运行）

        # 5. 在启动 worker 前执行一些同步的准备工作（从 app.start() 中提取）
        # 标记 worker 已启动
        self.app._worker_started = True

        # 如果配置了任务中心且配置尚未加载，从任务中心获取配置
        if self.app.task_center and self.app.task_center.is_enabled and not self.app._task_center_config:
            self.app._load_config_from_task_center()

        # 注册所有待注册的限流配置到 Redis
        logger.info("正在注册待注册的限流配置...")
        self.app._apply_pending_rate_limits()

        # 注册清理处理器（只在启动worker时注册）
        self.app._setup_cleanup_handlers()

        # 启动 Worker（使用通配符队列）
        logger.info("=" * 60)
        logger.info(f"启动 PG Consumer (通配符队列模式)")
        logger.info("=" * 60)
        logger.info(f"命名空间: {self.namespace_name} ({self.namespace_id or 'N/A'})")
        logger.info(f"监听队列: * (所有队列) + TASK_CHANGES (状态更新)")
        logger.info(f"INSERT 批量: {self.insert_buffer.max_size} 条")
        logger.info(f"UPDATE 批量: {self.update_buffer.max_size} 条")
        logger.info(f"刷新间隔: {self.insert_buffer.max_delay} 秒")
        logger.info(f"并发数: {concurrency}")
        logger.info("=" * 60)

        try:
            # 启动 Worker
            # 注意：这里调用 _start() 而不是 start()，因为：
            # - app.start() 是同步方法，内部使用 asyncio.run()
            # - app._start() 是异步方法，可以在已有的事件循环中使用 await
            # - 我们的 consumer.start() 是异步的，所以必须调用 _start()

            # 获取已注册任务的名称
            task_names = list(self.app._tasks.keys())
            logger.info(f"已注册的任务: {task_names}")

            await self.app._start(
                tasks=task_names,  # 🎯 关键：传递任务名称列表
                concurrency=concurrency,
                prefetch_multiplier=prefetch_multiplier
            )
        finally:
            await self.stop()

    async def stop(self):
        """停止 Consumer"""
        logger.info("停止 PG Consumer...")
        self._running = False

        # 停止自动刷新任务（会自动执行最后一次刷新）
        try:
            await self.insert_buffer.stop_auto_flush()
            await self.update_buffer.stop_auto_flush()
            logger.info("✓ 缓冲区自动刷新任务已停止")
        except Exception as e:
            logger.error(f"停止自动刷新任务失败: {e}")

        # 注意：不关闭数据库引擎，因为它是全局单例，由 connector.py 管理
        # 多个 consumer 实例可能共享同一个引擎

        # 打印统计信息
        insert_stats = self.insert_buffer.get_stats()
        update_stats = self.update_buffer.get_stats()

        logger.info("=" * 60)
        logger.info("PG Consumer 统计信息")
        logger.info("=" * 60)
        logger.info(f"INSERT: 总计 {insert_stats['total_flushed']} 条, "
                   f"刷新 {insert_stats['flush_count']} 次, "
                   f"平均 {insert_stats['avg_per_flush']} 条/次")
        logger.info(f"UPDATE: 总计 {update_stats['total_flushed']} 条, "
                   f"刷新 {update_stats['flush_count']} 次, "
                   f"平均 {update_stats['avg_per_flush']} 条/次")
        logger.info("=" * 60)

        logger.info("PG Consumer 已停止")
