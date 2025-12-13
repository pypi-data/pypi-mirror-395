"""
任务监控服务

提供任务相关的监控功能
"""
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
import redis.asyncio as aioredis

from .redis_monitor_service import RedisMonitorService

logger = logging.getLogger(__name__)


class TaskMonitorService:
    """任务监控服务类"""

    def __init__(self, redis_service: RedisMonitorService):
        """
        初始化任务监控服务

        Args:
            redis_service: Redis 监控基础服务实例
        """
        self.redis_service = redis_service

    @property
    def redis(self) -> aioredis.Redis:
        """获取 Redis 客户端"""
        return self.redis_service.redis

    @property
    def redis_prefix(self) -> str:
        """获取 Redis 前缀"""
        return self.redis_service.redis_prefix

    async def get_task_info(self, stream_id: str, queue_name: str) -> Optional[Dict[str, Any]]:
        """
        获取单个任务的详细信息

        Args:
            stream_id: Stream ID
            queue_name: 队列名称

        Returns:
            任务信息字典，如果任务不存在则返回 None
        """
        try:
            prefixed_queue = self.redis_service.get_prefixed_queue_name(queue_name)

            # 从 Stream 获取消息
            messages = await self.redis.xrange(prefixed_queue, min=stream_id, max=stream_id, count=1)

            if not messages:
                logger.warning(f"Task not found in stream: {stream_id} in queue {queue_name}")
                return None

            msg_id, msg_data = messages[0]

            # 检查消息是否在 pending 队列中
            pending_entries = await self.redis.xpending_range(
                prefixed_queue,
                f"{self.redis_prefix}:GROUP:{queue_name}",
                min=msg_id,
                max=msg_id,
                count=1
            )

            is_pending = len(pending_entries) > 0
            consumer_name = pending_entries[0]["consumer"].decode() if is_pending else None
            delivery_count = pending_entries[0]["times_delivered"] if is_pending else 0

            # 构建任务信息
            task_info = {
                "stream_id": msg_id,
                "queue": queue_name,
                "data": msg_data,
                "is_pending": is_pending,
                "consumer": consumer_name,
                "delivery_count": delivery_count,
                "timestamp": int(msg_id.split('-')[0])
            }

            logger.debug(f"Retrieved task info for {stream_id}: pending={is_pending}, consumer={consumer_name}")
            return task_info

        except Exception as e:
            logger.error(f"Error getting task info for {stream_id} in queue {queue_name}: {e}", exc_info=True)
            return None

    async def get_stream_info(self, queue_name: str) -> Optional[Dict[str, Any]]:
        """
        获取 Stream 的统计信息

        Args:
            queue_name: 队列名称

        Returns:
            Stream 信息字典
        """
        try:
            prefixed_queue = self.redis_service.get_prefixed_queue_name(queue_name)

            # 获取 Stream 信息
            info = await self.redis.xinfo_stream(prefixed_queue)

            stream_info = {
                "length": info.get("length", 0),
                "first_entry": info.get("first-entry"),
                "last_entry": info.get("last-entry"),
                "groups": info.get("groups", 0)
            }

            logger.debug(f"Retrieved stream info for queue {queue_name}: length={stream_info['length']}")
            return stream_info

        except Exception as e:
            logger.error(f"Error getting stream info for queue {queue_name}: {e}", exc_info=True)
            return None

    async def get_queue_tasks(
        self,
        queue_name: str,
        start: str = "-",
        end: str = "+",
        count: int = 100,
        reverse: bool = False
    ) -> List[Dict[str, Any]]:
        """
        获取队列中的任务列表

        Args:
            queue_name: 队列名称
            start: 起始 ID（默认 "-" 表示最小 ID）
            end: 结束 ID（默认 "+" 表示最大 ID）
            count: 返回的任务数量
            reverse: 是否反向获取（从新到旧）

        Returns:
            任务列表
        """
        try:
            prefixed_queue = self.redis_service.get_prefixed_queue_name(queue_name)

            # 根据 reverse 参数选择查询方向
            if reverse:
                messages = await self.redis.xrevrange(prefixed_queue, max=end, min=start, count=count)
            else:
                messages = await self.redis.xrange(prefixed_queue, min=start, max=end, count=count)

            if not messages:
                logger.debug(f"No tasks found in queue {queue_name}")
                return []

            # 获取 pending 信息（批量查询优化）
            group_name = f"{self.redis_prefix}:GROUP:{queue_name}"

            # 尝试获取所有 pending 消息的信息
            try:
                pending_entries = await self.redis.xpending_range(
                    prefixed_queue,
                    group_name,
                    min="-",
                    max="+",
                    count=10000  # 获取足够多的 pending 信息
                )
                # 构建 pending 映射：{msg_id: {consumer, delivery_count}}
                pending_map = {}
                for entry in pending_entries:
                    msg_id = entry["message_id"]
                    pending_map[msg_id] = {
                        "consumer": entry["consumer"].decode() if isinstance(entry["consumer"], bytes) else entry["consumer"],
                        "delivery_count": entry["times_delivered"]
                    }
            except Exception as e:
                logger.warning(f"Error getting pending info for queue {queue_name}: {e}")
                pending_map = {}

            # 构建任务列表
            tasks = []
            for msg_id, msg_data in messages:
                # 检查是否在 pending 中
                pending_info = pending_map.get(msg_id)
                is_pending = pending_info is not None

                # 解析时间戳
                try:
                    timestamp_ms = int(msg_id.split('-')[0])
                except (ValueError, IndexError):
                    timestamp_ms = 0

                # 解析消息数据
                task_data = {}
                for key, value in msg_data.items():
                    # Redis 返回的值可能是 bytes
                    if isinstance(key, bytes):
                        key = key.decode('utf-8')
                    if isinstance(value, bytes):
                        value = value.decode('utf-8')
                    task_data[key] = value

                # 构建任务信息
                task = {
                    "stream_id": msg_id,
                    "queue": queue_name,
                    "data": task_data,
                    "is_pending": is_pending,
                    "consumer": pending_info["consumer"] if is_pending else None,
                    "delivery_count": pending_info["delivery_count"] if is_pending else 0,
                    "timestamp": timestamp_ms,
                    "timestamp_iso": datetime.fromtimestamp(timestamp_ms / 1000).isoformat() if timestamp_ms else None
                }

                tasks.append(task)

            logger.info(f"Retrieved {len(tasks)} tasks from queue {queue_name} (reverse={reverse})")
            return tasks

        except Exception as e:
            logger.error(f"Error getting queue tasks for {queue_name}: {e}", exc_info=True)
            return []
