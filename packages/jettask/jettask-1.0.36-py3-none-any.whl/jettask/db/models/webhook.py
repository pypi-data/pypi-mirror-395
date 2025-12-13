"""
Webhook 模型

对应 webhooks 表，用于存储第三方平台的 webhook 回调通知
"""
from sqlalchemy import Column, Integer, Text, TIMESTAMP, Index, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime, timezone
from typing import Dict, Any
import enum

from ..base import Base


class WebhookStatus(str, enum.Enum):
    """Webhook 处理状态"""
    PENDING = "pending"      # 待处理（刚接收到）
    SUCCESS = "success"      # 已被任务获取
    FAILED = "failed"        # 处理失败


class Webhook(Base):
    """
    Webhook 回调通知表

    存储第三方平台（如模型服务商）发送的 webhook 通知
    设计为极简模式，任意 JSON 数据都可以存储
    """
    __tablename__ = 'webhooks'

    # 主键
    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增主键')

    # 命名空间
    namespace = Column(Text, nullable=False, comment='命名空间')

    # 回调 ID - 用于关联任务和 webhook
    # 任务在调用第三方 API 时生成此 ID，第三方回调时通过 URL 路径传回
    callback_id = Column(Text, nullable=False, index=True, comment='回调 ID，用于关联任务')

    # 原始数据 - 接收任意 JSON 结构
    payload = Column(JSONB, nullable=False, comment='原始 webhook 载荷（任意 JSON）')

    # 处理状态
    status = Column(
        SQLEnum(
            WebhookStatus,
            name='webhook_status',
            create_constraint=False,
            values_callable=lambda x: [e.value for e in x]
        ),
        nullable=False,
        default=WebhookStatus.PENDING,
        comment='处理状态'
    )

    # 时间戳
    received_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment='接收时间'
    )

    # 索引
    __table_args__ = (
        Index('idx_webhooks_namespace', 'namespace'),
        Index('idx_webhooks_namespace_callback_id', 'namespace', 'callback_id'),
        Index('idx_webhooks_received_at', 'received_at'),
    )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'namespace': self.namespace,
            'callback_id': self.callback_id,
            'payload': self.payload,
            'status': self.status.value if self.status else None,
            'received_at': self.received_at.isoformat() if self.received_at else None,
        }

    def __repr__(self) -> str:
        return f"<Webhook(id={self.id}, callback_id='{self.callback_id}', status='{self.status}')>"
