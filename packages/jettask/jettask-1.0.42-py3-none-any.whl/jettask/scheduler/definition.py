"""
定时任务定义类 - 类似 TaskMessage 的设计模式
用于定义定时任务，然后统一注册到数据库
"""
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from jettask.core.enums import TaskType


@dataclass
class Schedule:
    """
    定时任务定义对象

    这是一个定义定时任务的类，类似 TaskMessage 的设计模式。
    定时任务会定期向指定队列发送消息，队列中的消息可以被多个消费者处理。

    使用示例:
        # 1. 定义定时任务
        schedule1 = Schedule(
            scheduler_id="notify_every_30s",
            queue="notification_queue",
            interval_seconds=30,
            kwargs={"user_id": "user_123", "message": "定时提醒"}
        )

        schedule2 = Schedule(
            scheduler_id="report_cron",
            queue="report_queue",
            cron_expression="0 9 * * *",  # 每天9点
            description="每天生成报告"
        )

        # 2. 批量注册
        await app.register_schedules([schedule1, schedule2])

        # 3. 或单个注册
        await app.register_schedules(schedule1)
    """

    # 必需参数
    scheduler_id: str  # 任务唯一标识符（必填）
    queue: str         # 目标队列（必填）

    # 调度类型（三选一）
    interval_seconds: Optional[float] = None      # 间隔任务（秒）
    cron_expression: Optional[str] = None         # Cron表达式任务
    next_run_time: Optional[datetime] = None      # 一次性任务（指定执行时间）

    # 任务参数
    args: List[Any] = field(default_factory=list)
    kwargs: Dict[str, Any] = field(default_factory=dict)

    # 执行选项
    priority: Optional[int] = None      # 优先级（1最高，数字越大优先级越低）
    timeout: int = 300                  # 超时时间（秒）
    max_retries: int = 3                # 最大重试次数
    retry_delay: int = 60               # 重试延迟（秒）

    # 控制选项
    enabled: bool = True                # 是否启用
    description: Optional[str] = None   # 任务描述
    tags: List[str] = field(default_factory=list)        # 标签
    metadata: Dict[str, Any] = field(default_factory=dict)  # 额外元数据

    # 注册选项
    skip_if_exists: bool = True         # 如果已存在则跳过
    at_once: bool = True                # 是否立即执行一次

    def __post_init__(self):
        """初始化后处理"""
        self._validate()

    def _validate(self):
        """验证配置"""
        if not self.scheduler_id:
            raise ValueError("scheduler_id is required")

        if not self.queue:
            raise ValueError("queue is required")

        # 检查调度类型（必须指定一种）
        schedule_types = [
            self.interval_seconds is not None,
            self.cron_expression is not None,
            self.next_run_time is not None
        ]

        if sum(schedule_types) == 0:
            raise ValueError(
                "Must specify one schedule type: "
                "interval_seconds, cron_expression, or next_run_time"
            )

        if sum(schedule_types) > 1:
            raise ValueError(
                "Can only specify one schedule type: "
                "interval_seconds, cron_expression, or next_run_time"
            )

        # 验证具体参数
        if self.interval_seconds is not None and self.interval_seconds <= 0:
            raise ValueError(f"interval_seconds must be positive, got {self.interval_seconds}")

        if self.priority is not None and self.priority < 1:
            raise ValueError(f"priority must be positive (1 is highest), got {self.priority}")

    def get_task_type(self) -> TaskType:
        """获取任务类型"""
        if self.interval_seconds is not None:
            return TaskType.INTERVAL
        elif self.cron_expression is not None:
            return TaskType.CRON
        else:
            return TaskType.ONCE

    def to_dict(self) -> dict:
        """
        转换为字典格式（用于注册到数据库）

        Returns:
            dict: 任务字典
        """
        data = {
            'scheduler_id': self.scheduler_id,
            'queue': self.queue,
            'task_type': self.get_task_type().value,
            'task_args': self.args,
            'task_kwargs': self.kwargs,
            'enabled': self.enabled,
            'priority': self.priority,
            'timeout': self.timeout,
            'max_retries': self.max_retries,
            'retry_delay': self.retry_delay,
            'description': self.description,
            'tags': self.tags,
            'metadata': self.metadata,
        }

        # 添加调度相关参数
        if self.interval_seconds is not None:
            data['interval_seconds'] = self.interval_seconds
        elif self.cron_expression is not None:
            data['cron_expression'] = self.cron_expression
        elif self.next_run_time is not None:
            data['next_run_time'] = self.next_run_time

        return data

    def __repr__(self) -> str:
        """友好的字符串表示"""
        parts = [f"Schedule(scheduler_id='{self.scheduler_id}'"]
        parts.append(f"queue='{self.queue}'")

        if self.interval_seconds:
            parts.append(f"interval={self.interval_seconds}s")
        elif self.cron_expression:
            parts.append(f"cron='{self.cron_expression}'")
        elif self.next_run_time:
            parts.append(f"at={self.next_run_time}")

        if self.kwargs:
            parts.append(f"kwargs={self.kwargs}")

        return ", ".join(parts) + ")"
