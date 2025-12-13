"""
时间轴服务

提供队列任务的时间分布分析功能
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta, timezone

from .redis_monitor_service import RedisMonitorService

logger = logging.getLogger(__name__)


class TimelineService:
    """时间轴服务类"""

    def __init__(self, redis_service: RedisMonitorService):
        """
        初始化时间轴服务

        Args:
            redis_service: Redis 监控基础服务实例
        """
        self.redis_service = redis_service

    @property
    def redis(self):
        """获取 Redis 客户端"""
        return self.redis_service.redis

    @property
    def redis_prefix(self) -> str:
        """获取 Redis 前缀"""
        return self.redis_service.redis_prefix

    async def get_redis_timeline(
        self,
        queue_name: str,
        interval: str = "1m",
        duration: str = "1h",
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        context: str = "detail"
    ) -> Dict[str, Any]:
        """
        从 Redis Stream 获取队列任务的时间分布

        Args:
            queue_name: 队列名称
            interval: 时间间隔 (如 '1m', '5m', '1h')
            duration: 持续时间 (如 '1h', '24h')
            start_time: 开始时间（可选）
            end_time: 结束时间（可选）
            context: 上下文 ('overview' 或 'detail')

        Returns:
            时间轴数据
        """
        try:
            # 解析时间间隔和持续时间
            interval_seconds = self._parse_time_duration(interval)

            # 根据上下文设置不同的数据限制
            if context == "overview":
                # 首页概览：固定获取最近1小时的所有数据
                duration_seconds = 3600  # 1小时
                now = int(datetime.now(timezone.utc).timestamp() * 1000)
                start = now - duration_seconds * 1000
                min_id = f"{start}-0"
                max_id = "+"
                max_count = 100000  # 首页概览获取所有数据
            else:
                # 队列详情页：根据参数获取，但限制最多10000条
                if start_time and end_time:
                    # 使用提供的时间范围
                    min_id = start_time
                    max_id = end_time if end_time != '+' else '+'
                else:
                    # 使用duration参数计算时间范围
                    duration_seconds = self._parse_time_duration(duration)
                    now = int(datetime.now(timezone.utc).timestamp() * 1000)
                    start = now - duration_seconds * 1000
                    min_id = f"{start}-0"
                    max_id = "+"
                max_count = 10000  # 详情页限制10000条

            # 获取指定时间范围内的消息
            prefixed_queue_name = self.redis_service.get_prefixed_queue_name(queue_name)
            messages = await self.redis.xrange(
                prefixed_queue_name,
                min=min_id,
                max=max_id,
                count=max_count
            )

            # 按时间间隔统计任务数量
            buckets = {}
            bucket_size = interval_seconds * 1000  # 转换为毫秒

            # 计算实际的时间范围用于生成时间轴
            if start_time and end_time:
                # 从参数中解析时间范围
                if start_time != '-':
                    actual_start = int(start_time.split('-')[0])
                else:
                    actual_start = int(datetime.now(timezone.utc).timestamp() * 1000) - 86400000

                if end_time != '+':
                    actual_end = int(end_time.split('-')[0])
                else:
                    actual_end = int(datetime.now(timezone.utc).timestamp() * 1000)
            else:
                # 使用duration参数计算的时间范围
                actual_start = start
                actual_end = now

            for msg_id, _ in messages:
                # 从消息ID提取时间戳
                timestamp = int(msg_id.split('-')[0])
                bucket_key = (timestamp // bucket_size) * bucket_size
                buckets[bucket_key] = buckets.get(bucket_key, 0) + 1

            # 转换为时间序列数据
            timeline_data = []
            current_bucket = (actual_start // bucket_size) * bucket_size

            while current_bucket <= actual_end:
                timeline_data.append({
                    "timestamp": current_bucket,
                    "count": buckets.get(current_bucket, 0)
                })
                current_bucket += bucket_size

            # 计算实际任务总数
            total_tasks = len(messages)

            # 检查是否达到数据限制
            has_more = False
            if context == "detail" and total_tasks >= max_count:
                has_more = True

            logger.info(f"Redis 时间轴: 队列={queue_name}, 任务数={total_tasks}, 数据点={len(timeline_data)}")

            return {
                "timeline": timeline_data,
                "interval": interval,
                "duration": duration,
                "start": actual_start,
                "end": actual_end,
                "total_tasks": total_tasks,
                "message_count": len(messages),
                "has_more": has_more,
                "limit": max_count if context == "detail" else None,
                "source": "redis"
            }

        except Exception as e:
            logger.error(f"获取 Redis 时间轴失败: 队列={queue_name}, 错误={e}", exc_info=True)
            return {
                "timeline": [],
                "error": str(e),
                "source": "redis"
            }

    def _parse_time_duration(self, duration_str: str) -> int:
        """
        解析时间字符串为秒数

        Args:
            duration_str: 时间字符串 (如 '1h', '10m', '30s')

        Returns:
            秒数
        """
        units = {
            's': 1,
            'm': 60,
            'h': 3600,
            'd': 86400
        }

        if duration_str[-1] in units:
            value = int(duration_str[:-1])
            unit = duration_str[-1]
            return value * units[unit]

        # 默认为秒
        return int(duration_str)
