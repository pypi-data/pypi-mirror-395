"""
TaskRun 模型

对应 task_runs 表，用于存储任务执行记录
"""
from sqlalchemy import Column, String, Integer, Text, TIMESTAMP, Float, Index, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime, timezone
from typing import Optional, Dict, Any

from ..base import Base


class TaskRun(Base):
    """
    任务执行记录表

    存储每次任务执行的状态、结果和执行时间等信息
    """
    __tablename__ = 'task_runs'

    # 复合主键 - (task_name, trigger_time, stream_id)
    # 说明：
    # - task_runs 是分区表（按 trigger_time 分区），主键必须包含分区键
    # - 主键顺序按粒度从粗到细排列，以提高索引复用率：
    #   - task_name: 任务名称（粗粒度，可能只有几十种任务）
    #   - trigger_time: 任务触发时间（中粒度，分区键）
    #   - stream_id: Redis Stream 事件ID（细粒度，1:1对应任务）
    # 这样的顺序支持：
    #   - 按 task_name 查询（复用索引前缀）
    #   - 按 task_name + trigger_time 范围查询
    #   - 按 task_name + trigger_time + stream_id 精确查询
    task_name = Column(Text, primary_key=True, nullable=False, comment='任务名称（粗粒度）')
    trigger_time = Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False, comment='任务触发时间（分区键）')
    stream_id = Column(Text, primary_key=True, comment='Redis Stream 事件ID（细粒度）')

    # 执行状态
    status = Column(String(50), nullable=True, comment='任务状态 (pending/running/success/failed/retrying)')

    # 执行结果
    result = Column(JSONB, nullable=True, comment='任务执行结果')
    error = Column(Text, nullable=True, comment='错误信息（如果失败）')

    # 执行时间
    started_at = Column(TIMESTAMP(timezone=True), nullable=True, comment='开始执行时间（TIMESTAMP 类型），可能因重试而变化')
    completed_at = Column(TIMESTAMP(timezone=True), nullable=True, comment='完成时间（TIMESTAMP 类型）')

    # 重试次数
    retries = Column(Integer, nullable=True, default=0, comment='重试次数')

    # 执行时长（秒）
    duration = Column(Float, nullable=True, comment='执行时长（秒）')

    # 消费者信息
    consumer = Column(Text, nullable=True, comment='执行该任务的消费者ID')

    # 记录创建和更新时间
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment='记录创建时间'
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment='记录更新时间'
    )

    # 索引
    # 注意：主键 (task_name, trigger_time, stream_id) 已自动创建索引
    # 可以复用主键索引支持：
    #   - 按 task_name 查询
    #   - 按 (task_name, trigger_time) 范围查询
    #   - 按 (task_name, trigger_time, stream_id) 精确查询
    __table_args__ = (
        Index('idx_task_runs_status', 'status'),
        Index('idx_task_runs_stream_id', 'stream_id'),  # 支持按 stream_id 反查
        Index('idx_task_runs_started_at', 'started_at'),
    )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'task_name': self.task_name,
            'trigger_time': self.trigger_time.isoformat() if self.trigger_time else None,
            'stream_id': self.stream_id,
            'status': self.status,
            'result': self.result,
            'error': self.error,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'retries': self.retries,
            'duration': self.duration,
            'consumer': self.consumer,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        return f"<TaskRun(stream_id='{self.stream_id}', status='{self.status}')>"
