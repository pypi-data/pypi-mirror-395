"""
服务基类
提供公共的时间范围处理方法
"""
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Any
import logging

from jettask.schemas import TimeRangeQuery

logger = logging.getLogger(__name__)


class TimeRangeResult:
    """时间范围处理结果"""
    def __init__(self, start_time: datetime, end_time: datetime, interval: str, interval_seconds: int, granularity: str):
        self.start_time = start_time
        self.end_time = end_time
        self.interval = interval
        self.interval_seconds = interval_seconds
        self.granularity = granularity


class QueueResolutionResult:
    """队列解析结果"""
    def __init__(
        self,
        target_queues: List[str],
        all_priority_queues: List[str],
        base_queue_map: Dict[str, str]
    ):
        """
        Args:
            target_queues: 有效的基础队列列表
            all_priority_queues: 展开后的所有优先级队列列表
            base_queue_map: 优先级队列到基础队列的映射
        """
        self.target_queues = target_queues
        self.all_priority_queues = all_priority_queues
        self.base_queue_map = base_queue_map


class BaseService:
    """服务基类，提供公共的集成方法"""

    @staticmethod
    def _parse_time_range(time_range: str, end_time: datetime) -> datetime:
        """
        解析时间范围字符串

        Args:
            time_range: 时间范围字符串，如 "24h", "7d", "30m"
            end_time: 结束时间

        Returns:
            开始时间
        """
        if time_range.endswith('m'):
            minutes = int(time_range[:-1])
            return end_time - timedelta(minutes=minutes)
        elif time_range.endswith('h'):
            hours = int(time_range[:-1])
            return end_time - timedelta(hours=hours)
        elif time_range.endswith('d'):
            days = int(time_range[:-1])
            return end_time - timedelta(days=days)
        else:
            return end_time - timedelta(hours=24)  # 默认24小时

    @staticmethod
    def _parse_time_range_query(query: TimeRangeQuery) -> TimeRangeResult:
        """
        解析TimeRangeQuery对象

        Args:
            query: 时间范围查询对象

        Returns:
            时间范围处理结果
        """
        # 如果有结束时间，使用它；否则使用当前时间
        if query.end_time:
            end_time = datetime.fromisoformat(query.end_time.replace('Z', '+00:00')) if isinstance(query.end_time, str) else query.end_time
        else:
            end_time = datetime.now(timezone.utc)

        # 如果有开始时间，使用它；否则基于interval或默认24小时
        if query.start_time:
            start_time = datetime.fromisoformat(query.start_time.replace('Z', '+00:00')) if isinstance(query.start_time, str) else query.start_time
        else:
            # 使用interval字段来计算开始时间，默认为24小时
            interval = query.interval or "24h"
            start_time = BaseService._parse_time_range(interval, end_time)

        return BaseService._calculate_dynamic_interval(start_time, end_time)

    @staticmethod
    def _calculate_dynamic_interval(start_time: datetime, end_time: datetime, target_points: int = 200) -> TimeRangeResult:
        """
        根据时间范围动态计算合适的时间间隔

        Args:
            start_time: 开始时间
            end_time: 结束时间
            target_points: 目标数据点数量，默认200

        Returns:
            时间范围处理结果，包含计算出的最佳间隔
        """
        duration = (end_time - start_time).total_seconds()
        ideal_interval_seconds = duration / target_points

        # 选择合适的间隔
        intervals = [
            (1, '1 seconds', 'second'),
            (5, '5 seconds', 'second'),
            (10, '10 seconds', 'second'),
            (30, '30 seconds', 'second'),
            (60, '1 minute', 'minute'),
            (300, '5 minutes', 'minute'),
            (600, '10 minutes', 'minute'),
            (1800, '30 minutes', 'minute'),
            (3600, '1 hour', 'hour'),
            (21600, '6 hours', 'hour'),
            (43200, '12 hours', 'hour'),
            (86400, '1 day', 'day')
        ]

        for seconds, interval_str, granularity in intervals:
            if ideal_interval_seconds <= seconds:
                return TimeRangeResult(start_time, end_time, interval_str, seconds, granularity)

        # 默认返回1天间隔
        return TimeRangeResult(start_time, end_time, '1 day', 86400, 'day')

    @classmethod
    def _resolve_time_range(
        cls,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        time_range: Optional[str] = None,
        default_range: str = "1h",
        target_points: int = 200,
        min_interval_seconds: int = 0
    ) -> TimeRangeResult:
        """
        统一处理时间范围参数的高级方法

        支持三种输入方式：
        1. 仅传入 time_range 字符串（如 "15m", "1h", "24h", "7d"）
        2. 仅传入 start_time 和 end_time
        3. 都不传入，使用默认时间范围

        Args:
            start_time: 开始时间（可选）
            end_time: 结束时间（可选）
            time_range: 时间范围字符串（可选），如 "15m", "1h", "24h", "7d"
            default_range: 默认时间范围字符串，默认 "1h"
            target_points: 目标数据点数量，默认200
            min_interval_seconds: 最小间隔秒数，默认0（无限制）。
                                  设置为60表示最小粒度为分钟。

        Returns:
            TimeRangeResult: 包含解析后的时间范围和计算出的最佳间隔

        Examples:
            # 使用时间范围字符串
            result = cls._resolve_time_range(time_range="24h")

            # 使用具体时间
            result = cls._resolve_time_range(start_time=start, end_time=end)

            # 使用默认时间范围
            result = cls._resolve_time_range()

            # 自定义默认范围和目标点数
            result = cls._resolve_time_range(default_range="15m", target_points=100)

            # 设置最小粒度为分钟（60秒）
            result = cls._resolve_time_range(time_range="1h", min_interval_seconds=60)
        """
        now = datetime.now(timezone.utc)

        # 处理时间范围
        if time_range and not start_time:
            # 优先使用 time_range 字符串
            start_time = cls._parse_time_range(time_range, now)
            end_time = now
        elif not start_time:
            # 使用默认时间范围
            start_time = cls._parse_time_range(default_range, now)
            end_time = now

        # 确保 end_time 有值
        if not end_time:
            end_time = now

        # 计算动态时间间隔
        result = cls._calculate_dynamic_interval(start_time, end_time, target_points)

        # 如果设置了最小间隔，确保不低于最小值
        if min_interval_seconds > 0 and result.interval_seconds < min_interval_seconds:
            # 重新计算，使用最小间隔
            granularity = "second"
            if min_interval_seconds >= 86400:
                granularity = "day"
            elif min_interval_seconds >= 3600:
                granularity = "hour"
            elif min_interval_seconds >= 60:
                granularity = "minute"

            # 构建间隔描述
            if min_interval_seconds == 60:
                interval_str = "1 minute"
            elif min_interval_seconds == 300:
                interval_str = "5 minutes"
            elif min_interval_seconds == 600:
                interval_str = "10 minutes"
            elif min_interval_seconds == 1800:
                interval_str = "30 minutes"
            elif min_interval_seconds == 3600:
                interval_str = "1 hour"
            else:
                interval_str = f"{min_interval_seconds} seconds"

            logger.debug(
                f"时间间隔 {result.interval_seconds}s 小于最小值 {min_interval_seconds}s，"
                f"已调整为 {interval_str}"
            )

            result = TimeRangeResult(
                start_time=result.start_time,
                end_time=result.end_time,
                interval=interval_str,
                interval_seconds=min_interval_seconds,
                granularity=granularity
            )

        return result

    @staticmethod
    async def _resolve_queues(
        queues: List[str],
        registry,
        expand_priority: bool = True
    ) -> QueueResolutionResult:
        """
        统一处理队列名称解析

        验证队列是否存在于注册表中，并可选择性地展开为优先级队列。

        Args:
            queues: 请求的基础队列名称列表
            registry: QueueRegistry 实例
            expand_priority: 是否展开为优先级队列，默认 True

        Returns:
            QueueResolutionResult: 包含解析后的队列信息

        Examples:
            # 展开优先级队列
            result = await cls._resolve_queues(["email_queue"], registry)
            # result.target_queues = ["email_queue"]
            # result.all_priority_queues = ["email_queue:1", "email_queue:2", "email_queue:3"]
            # result.base_queue_map = {"email_queue:1": "email_queue", ...}

            # 不展开优先级队列
            result = await cls._resolve_queues(["email_queue"], registry, expand_priority=False)
            # result.target_queues = ["email_queue"]
            # result.all_priority_queues = ["email_queue"]
            # result.base_queue_map = {"email_queue": "email_queue"}
        """
        # 获取注册表中的所有基础队列
        all_base_queues = await registry.get_base_queues()

        # 过滤出存在于注册表中的队列
        target_queues = [q for q in queues if q in all_base_queues]

        if not expand_priority:
            # 不展开优先级队列
            base_queue_map = {q: q for q in target_queues}
            return QueueResolutionResult(
                target_queues=target_queues,
                all_priority_queues=target_queues,
                base_queue_map=base_queue_map
            )

        # 展开基础队列到所有优先级队列
        all_priority_queues = []
        base_queue_map = {}  # priority_queue -> base_queue 的映射

        for base_queue in target_queues:
            priority_queues = await registry.get_priority_queues_for_base(base_queue)
            if priority_queues:
                all_priority_queues.extend(priority_queues)
                for pq in priority_queues:
                    base_queue_map[pq] = base_queue
            else:
                # 如果没有优先级队列，可能队列名本身就是完整的
                all_priority_queues.append(base_queue)
                base_queue_map[base_queue] = base_queue

        logger.debug(f"队列解析: {queues} -> target={target_queues}, priority={all_priority_queues}")

        return QueueResolutionResult(
            target_queues=target_queues,
            all_priority_queues=all_priority_queues,
            base_queue_map=base_queue_map
        )
