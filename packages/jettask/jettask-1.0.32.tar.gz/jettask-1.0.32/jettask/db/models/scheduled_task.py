"""
ScheduledTask 模型

对应 scheduled_tasks 表，用于定时任务调度
"""
from sqlalchemy import (
    Column, BigInteger, String, Integer, Text, Boolean,
    TIMESTAMP, Index, Numeric, ForeignKey, select, update, delete, and_, or_
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List
from decimal import Decimal
import json
import croniter
import logging

from ..base import Base
from jettask.core.enums import TaskType, TaskStatus

logger = logging.getLogger('app')


class ScheduledTask(Base):
    """
    定时任务表

    定时任务以 queue 为核心，定期向指定队列发送消息
    """
    __tablename__ = 'scheduled_tasks'

    # 主键
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='自增主键')

    # 唯一标识
    scheduler_id = Column(
        String(255),
        nullable=False,
        unique=True,
        comment='任务的唯一标识符（用于去重）'
    )

    # 任务类型
    task_type = Column(
        String(50),
        nullable=False,
        comment='任务类型: cron, interval, once'
    )

    # 任务执行相关
    queue_name = Column(String(100), nullable=False, comment='目标队列名')
    namespace = Column(String(100), default='default', comment='命名空间')
    task_args = Column(JSONB, default=[], comment='任务参数')
    task_kwargs = Column(JSONB, default={}, comment='任务关键字参数')

    # 调度相关
    cron_expression = Column(String(100), comment='cron表达式 (task_type=cron时使用)')
    interval_seconds = Column(Numeric(10, 2), comment='间隔秒数 (task_type=interval时使用)')
    next_run_time = Column(TIMESTAMP(timezone=True), comment='下次执行时间（任务真正应该执行的时间）')
    next_trigger_time = Column(TIMESTAMP(timezone=True), comment='下次触发时间（调度器应该发送任务的时间，可能提前于next_run_time）')
    last_run_time = Column(TIMESTAMP(timezone=True), comment='上次执行时间')

    # 状态和控制
    enabled = Column(Boolean, default=True, comment='是否启用')
    max_retries = Column(Integer, default=3, comment='最大重试次数')
    retry_delay = Column(Integer, default=60, comment='重试延迟(秒)')
    timeout = Column(Integer, default=300, comment='任务超时时间(秒)')
    priority = Column(Integer, comment='任务优先级 (1=最高, 数字越大优先级越低，NULL=默认最低)')

    # 元数据 (使用 column name override 避免与 SQLAlchemy 的 metadata 属性冲突)
    description = Column(Text, comment='任务描述')
    tags = Column(JSONB, default=[], comment='标签')
    task_metadata = Column('metadata', JSONB, default={}, comment='额外元数据')

    # 时间戳
    created_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        comment='创建时间'
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment='更新时间'
    )

    # 索引
    __table_args__ = (
        Index('idx_scheduled_tasks_next_run', 'next_run_time', postgresql_where=(enabled == True)),  # noqa: E712
        Index('idx_scheduled_tasks_task_type', 'task_type'),
        Index('idx_scheduled_tasks_queue', 'queue_name'),
        Index('idx_scheduled_tasks_enabled', 'enabled'),
        Index('idx_scheduled_tasks_scheduler_id', 'scheduler_id', unique=True),
    )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'scheduler_id': self.scheduler_id,
            'task_type': self.task_type,
            'queue_name': self.queue_name,
            'namespace': self.namespace,
            'task_args': self.task_args,
            'task_kwargs': self.task_kwargs,
            'cron_expression': self.cron_expression,
            'interval_seconds': float(self.interval_seconds) if self.interval_seconds else None,
            'next_run_time': self.next_run_time.isoformat() if self.next_run_time else None,
            'next_trigger_time': self.next_trigger_time.isoformat() if self.next_trigger_time else None,
            'last_run_time': self.last_run_time.isoformat() if self.last_run_time else None,
            'enabled': self.enabled,
            'max_retries': self.max_retries,
            'retry_delay': self.retry_delay,
            'timeout': self.timeout,
            'priority': self.priority,
            'description': self.description,
            'tags': self.tags,
            'metadata': self.task_metadata,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        return f"<ScheduledTask(id={self.id}, scheduler_id='{self.scheduler_id}', queue='{self.queue_name}', type='{self.task_type}')>"

    def validate(self):
        """验证任务配置"""
        if self.task_type == TaskType.CRON.value and not self.cron_expression:
            raise ValueError(f"Task (queue={self.queue_name}) with type CRON must have cron_expression")

        if self.task_type == TaskType.INTERVAL.value and not self.interval_seconds:
            raise ValueError(f"Task (queue={self.queue_name}) with type INTERVAL must have interval_seconds")

        # ONCE类型任务不应该有interval_seconds参数
        if self.task_type == TaskType.ONCE.value and self.interval_seconds is not None:
            raise ValueError(f"Task (queue={self.queue_name}) with type ONCE should not have interval_seconds. Use next_run_time to specify when to run the task")

    def calculate_next_run_time(self, from_time: Optional[datetime] = None) -> Optional[datetime]:
        """计算下次执行时间

        注意：如果计算出的时间仍在过去（任务长时间未运行），
        会自动跳到当前时间之后的下一个周期，避免无限循环补齐历史任务。
        """
        if not self.enabled:
            return None

        from_time = from_time or datetime.now(timezone.utc)
        now = datetime.now(timezone.utc)

        if self.task_type == TaskType.ONCE.value:
            # 一次性任务，如果没有执行过就返回设定的时间
            if self.last_run_time is None:
                return self.next_run_time or from_time
            return None

        elif self.task_type == TaskType.INTERVAL.value:
            # 间隔任务
            if self.last_run_time:
                interval = float(self.interval_seconds) if isinstance(self.interval_seconds, Decimal) else self.interval_seconds
                next_run = self.last_run_time + timedelta(seconds=interval)

                # 🔧 如果计算出的时间仍在过去（说明任务长时间未运行）
                # 直接跳到当前时间之后的下一个周期，避免无限循环
                if next_run < now:
                    # 计算需要跳过多少个周期
                    missed_intervals = int((now - next_run).total_seconds() / interval) + 1
                    next_run = next_run + timedelta(seconds=interval * missed_intervals)
                    logger.warning(
                        f"任务 {self.scheduler_id} 长时间未运行，跳过 {missed_intervals} 个周期，"
                        f"下次执行: {next_run}"
                    )

                return next_run
            return from_time

        elif self.task_type == TaskType.CRON.value:
            # Cron表达式任务
            # 使用当前时间而不是from_time，确保得到未来的时间
            base_time = max(from_time, now)
            cron = croniter.croniter(self.cron_expression, base_time)
            return cron.get_next(datetime)

        return None

    def calculate_trigger_time(self, next_run: datetime) -> datetime:
        """
        计算触发时间（调度器应该发送任务的时间）

        策略：
        - 间隔 < 60秒：不提前触发，trigger_time = run_time
        - 间隔 >= 60秒：提前 interval/5，但最多提前3600秒（1小时）

        Args:
            next_run: 下次执行时间

        Returns:
            下次触发时间
        """
        if self.task_type == TaskType.ONCE.value:
            # 一次性任务不提前触发
            return next_run

        # 获取间隔时间（秒）
        interval_seconds = 0
        if self.task_type == TaskType.INTERVAL.value and self.interval_seconds:
            interval_seconds = float(self.interval_seconds) if isinstance(self.interval_seconds, Decimal) else self.interval_seconds
        elif self.task_type == TaskType.CRON.value and self.last_run_time:
            # Cron任务：计算与上次执行时间的间隔
            interval_seconds = (next_run - self.last_run_time).total_seconds()

        # 间隔小于60秒：不提前触发
        if interval_seconds < 60:
            return next_run

        # 计算提前时间：interval / 5，但最多1小时
        advance_seconds = min(interval_seconds / 5, 3600)

        trigger_time = next_run - timedelta(seconds=advance_seconds)

        logger.info(
            f"计算触发时间: scheduler_id={self.scheduler_id}, "
            f"interval={interval_seconds}s, advance={advance_seconds}s, "
            f"next_run={next_run}, trigger={trigger_time}"
        )

        return trigger_time

    def update_next_run_time(self):
        """更新下次执行时间"""
        self.last_run_time = datetime.now()
        self.next_run_time = self.calculate_next_run_time(from_time=self.last_run_time)

    def to_redis_value(self) -> str:
        """转换为Redis存储的值"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_redis_value(cls, value: str) -> 'ScheduledTask':
        """从Redis值创建实例"""
        data = json.loads(value)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict) -> 'ScheduledTask':
        """从字典创建实例"""
        # 转换datetime字符串
        for key in ['next_run_time', 'next_trigger_time', 'last_run_time', 'created_at', 'updated_at']:
            if data.get(key) and isinstance(data[key], str):
                data[key] = datetime.fromisoformat(data[key])

        # 兼容旧的 scheduled_until 字段
        if 'scheduled_until' in data:
            data.pop('scheduled_until')

        # 转换interval_seconds为float（处理Decimal类型）
        if data.get('interval_seconds'):
            if isinstance(data['interval_seconds'], Decimal):
                data['interval_seconds'] = float(data['interval_seconds'])

        # 处理 metadata 字段映射
        if 'metadata' in data:
            data['task_metadata'] = data.pop('metadata')

        # 创建实例
        instance = cls()
        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        return instance

    # ==================== 数据库操作类方法 ====================

    @classmethod
    async def create(cls, session: AsyncSession, task: 'ScheduledTask') -> 'ScheduledTask':
        """创建定时任务"""
        # 设置默认值
        if not task.created_at:
            task.created_at = datetime.now(timezone.utc)
        if not task.updated_at:
            task.updated_at = datetime.now(timezone.utc)

        # 为新任务计算初始的 next_run_time（如果还没有设置）
        if not task.next_run_time:
            # INTERVAL 和 CRON 任务需要计算初始执行时间
            if task.task_type in [TaskType.INTERVAL.value, TaskType.CRON.value]:
                task.next_run_time = task.calculate_next_run_time()
                logger.debug(f"计算初始执行时间: scheduler_id={task.scheduler_id}, next_run_time={task.next_run_time}")

        # 计算初始的 next_trigger_time
        if task.next_run_time and not task.next_trigger_time:
            task.next_trigger_time = task.calculate_trigger_time(task.next_run_time)
            logger.debug(f"计算初始触发时间: scheduler_id={task.scheduler_id}, next_trigger_time={task.next_trigger_time}")

        session.add(task)
        await session.flush()
        await session.refresh(task)

        logger.debug(f"创建任务: id={task.id}, scheduler_id={task.scheduler_id}, next_run_time={task.next_run_time}")
        return task

    @classmethod
    async def get_by_id(cls, session: AsyncSession, task_id: int) -> Optional['ScheduledTask']:
        """通过ID获取任务"""
        result = await session.execute(
            select(cls).where(cls.id == task_id)
        )
        return result.scalar_one_or_none()

    @classmethod
    async def get_by_scheduler_id(cls, session: AsyncSession, scheduler_id: str) -> Optional['ScheduledTask']:
        """通过scheduler_id获取任务"""
        result = await session.execute(
            select(cls).where(cls.scheduler_id == scheduler_id)
        )
        return result.scalar_one_or_none()

    @classmethod
    async def update_task(cls, session: AsyncSession, task: 'ScheduledTask') -> 'ScheduledTask':
        """更新任务"""
        task.updated_at = datetime.now(timezone.utc)
        merged_task = await session.merge(task)
        await session.flush()
        await session.refresh(merged_task)

        logger.debug(f"更新任务: id={merged_task.id}, scheduler_id={merged_task.scheduler_id}")
        return merged_task

    @classmethod
    async def delete_by_id(cls, session: AsyncSession, task_id: int) -> bool:
        """删除任务"""
        result = await session.execute(
            delete(cls).where(cls.id == task_id)
        )
        deleted = result.rowcount > 0
        logger.debug(f"删除任务: id={task_id}, success={deleted}")
        return deleted

    @classmethod
    async def list_tasks(
        cls,
        session: AsyncSession,
        enabled: Optional[bool] = None,
        task_type: Optional[TaskType] = None,
        queue_name: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List['ScheduledTask']:
        """列出任务"""
        query = select(cls)

        conditions = []
        if enabled is not None:
            conditions.append(cls.enabled == enabled)
        if task_type is not None:
            conditions.append(cls.task_type == task_type.value)
        if queue_name is not None:
            conditions.append(cls.queue_name == queue_name)

        if conditions:
            query = query.where(and_(*conditions))

        query = query.order_by(cls.created_at.desc())
        query = query.limit(limit).offset(offset)

        result = await session.execute(query)
        return list(result.scalars().all())

    @classmethod
    async def get_ready_tasks(
        cls,
        session: AsyncSession,
        batch_size: int = 100,
        lookahead_seconds: int = 60
    ) -> List['ScheduledTask']:
        """
        获取即将触发的任务

        新设计：
        - 查询条件改为 next_trigger_time <= now
        - next_trigger_time 是提前计算的触发时间，可能早于 next_run_time
        - 任务会被提前发送到队列，但带有 delay 参数，在 next_run_time 时才真正执行

        Args:
            session: 数据库会话
            batch_size: 批次大小
            lookahead_seconds: 向前查看的秒数（这个参数在新设计中不再使用，保留是为了兼容性）
        """
        now = datetime.now(timezone.utc)

        logger.info(f"get_ready_tasks: now={now}")

        # 新查询：查找 next_trigger_time <= now 的任务
        # 这些任务应该被发送到队列（可能带delay）
        query = select(cls).where(
            and_(
                cls.enabled == True,
                cls.next_trigger_time <= now,
                cls.next_trigger_time.isnot(None)
            )
        ).order_by(cls.next_trigger_time).limit(batch_size)

        result = await session.execute(query)
        tasks = list(result.scalars().all())

        logger.info(f"get_ready_tasks: found {len(tasks)} tasks")
        for task in tasks:
            logger.info(
                f"  - Task id={task.id}, scheduler_id={task.scheduler_id}, "
                f"trigger={task.next_trigger_time}, run={task.next_run_time}"
            )

        return tasks

    @classmethod
    async def update_next_run(
        cls,
        session: AsyncSession,
        task_id: int,
        next_run_time: Optional[datetime],
        last_run_time: datetime
    ):
        """更新任务的下次执行时间"""
        await session.execute(
            update(cls)
            .where(cls.id == task_id)
            .values(
                next_run_time=next_run_time,
                last_run_time=last_run_time,
                updated_at=datetime.now(timezone.utc)
            )
        )
        logger.debug(f"更新任务执行时间: id={task_id}, next_run={next_run_time}")

    @classmethod
    async def disable_once_task(cls, session: AsyncSession, task_id: int):
        """禁用一次性任务"""
        await session.execute(
            update(cls)
            .where(cls.id == task_id)
            .values(
                enabled=False,
                next_run_time=None,
                updated_at=datetime.now(timezone.utc)
            )
        )
        logger.debug(f"禁用一次性任务: id={task_id}")

    @classmethod
    async def batch_update_next_run_times(cls, session: AsyncSession, updates: List[tuple]):
        """
        批量更新任务的下次执行时间和触发时间

        Args:
            session: 数据库会话
            updates: 更新列表，格式为 [(task_id, next_run_time, next_trigger_time, last_run_time), ...]
        """
        if not updates:
            return

        logger.info(f"batch_update_next_run_times: starting update for {len(updates)} tasks")

        for task_id, next_run_time, next_trigger_time, last_run_time in updates:
            await session.execute(
                update(cls)
                .where(cls.id == task_id)
                .values(
                    next_run_time=next_run_time,
                    next_trigger_time=next_trigger_time,
                    last_run_time=last_run_time,
                    updated_at=datetime.now(timezone.utc)
                )
            )

        logger.info(f"batch_update_next_run_times: completed {len(updates)} updates")

    @classmethod
    async def batch_disable_once_tasks(cls, session: AsyncSession, task_ids: List[int]):
        """批量禁用一次性任务"""
        if not task_ids:
            return

        await session.execute(
            update(cls)
            .where(cls.id.in_(task_ids))
            .values(
                enabled=False,
                next_run_time=None,
                updated_at=datetime.now(timezone.utc)
            )
        )
        logger.debug(f"批量禁用一次性任务: count={len(task_ids)}")

    @classmethod
    async def batch_create(cls, session: AsyncSession, tasks: List['ScheduledTask'], skip_existing: bool = True) -> List['ScheduledTask']:
        """
        批量创建任务

        Args:
            session: 数据库会话
            tasks: 任务列表
            skip_existing: 是否跳过已存在的任务

        Returns:
            成功创建的任务列表
        """
        if not tasks:
            return []

        created_tasks = []

        # 1. 查询已存在的 scheduler_id
        scheduler_ids = [t.scheduler_id for t in tasks if t.scheduler_id]
        existing_ids = set()

        if scheduler_ids and skip_existing:
            result = await session.execute(
                select(cls.scheduler_id)
                .where(cls.scheduler_id.in_(scheduler_ids))
            )
            existing_ids = {row[0] for row in result.all()}

        # 2. 过滤并创建任务
        now = datetime.now(timezone.utc)
        for task in tasks:
            if task.scheduler_id in existing_ids:
                logger.debug(f"跳过已存在的任务: scheduler_id={task.scheduler_id}")
                continue

            if not task.created_at:
                task.created_at = now
            if not task.updated_at:
                task.updated_at = now

            session.add(task)
            created_tasks.append(task)

        # 3. 刷新以获取生成的ID
        if created_tasks:
            await session.flush()
            for task in created_tasks:
                await session.refresh(task)

        logger.info(f"批量创建任务: 成功创建 {len(created_tasks)}/{len(tasks)} 个任务")
        return created_tasks
