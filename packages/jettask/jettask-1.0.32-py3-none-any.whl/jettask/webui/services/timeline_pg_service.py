"""
PostgreSQL 时间轴服务

从 PostgreSQL 数据库获取任务时间分布数据
"""
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlalchemy.dialects import postgresql

logger = logging.getLogger(__name__)


class TimelinePgService:
    """PostgreSQL 时间轴服务"""

    def __init__(self):
        pass

    @staticmethod
    def parse_iso_datetime(time_str: str) -> datetime:
        """解析ISO格式的时间字符串，确保返回 UTC 时间"""
        if time_str.endswith('Z'):
            # Z 表示 UTC 时间
            dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
        else:
            dt = datetime.fromisoformat(time_str)

        # 如果没有时区信息，假定为 UTC
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        # 如果有时区信息，转换为 UTC
        elif dt.tzinfo != timezone.utc:
            dt = dt.astimezone(timezone.utc)

        return dt

    @staticmethod
    def parse_interval(interval: str) -> int:
        """解析时间间隔字符串，返回分钟数"""
        if interval.endswith('m'):
            return int(interval[:-1])
        elif interval.endswith('h'):
            return int(interval[:-1]) * 60
        elif interval.endswith('s'):
            return int(interval[:-1]) // 60 if int(interval[:-1]) >= 60 else 1
        else:
            return 5  # 默认5分钟

    @staticmethod
    def calculate_auto_interval(duration_seconds: float) -> tuple:
        """
        根据时间范围自动计算合适的时间间隔

        Returns:
            tuple: (interval_seconds, interval_type, interval_str)
        """
        if duration_seconds <= 300:  # <= 5分钟
            return 0.5, 'millisecond', '500ms'
        elif duration_seconds <= 900:  # <= 15分钟
            return 1, 'second', '1s'
        elif duration_seconds <= 1800:  # <= 30分钟
            return 2, 'second', '2s'
        elif duration_seconds <= 3600:  # <= 1小时
            return 30, 'second', '30s'
        elif duration_seconds <= 10800:  # <= 3小时
            return 300, 'minute', '5m'
        elif duration_seconds <= 21600:  # <= 6小时
            return 600, 'minute', '10m'
        elif duration_seconds <= 43200:  # <= 12小时
            return 1800, 'minute', '30m'
        elif duration_seconds <= 86400:  # <= 24小时
            return 3600, 'hour', '1h'
        elif duration_seconds <= 172800:  # <= 2天
            return 7200, 'hour', '2h'
        elif duration_seconds <= 604800:  # <= 7天
            return 21600, 'hour', '6h'
        else:  # > 7天
            return 86400, 'hour', '24h'

    @staticmethod
    def align_to_interval(dt: datetime, interval_seconds: float) -> datetime:
        """对齐时间到interval_seconds的整数倍"""
        if interval_seconds >= 3600:  # 大于等于1小时
            # 按小时对齐
            dt = dt.replace(minute=0, second=0, microsecond=0)
            interval_hours = int(interval_seconds // 3600)
            aligned_hour = (dt.hour // interval_hours) * interval_hours
            return dt.replace(hour=aligned_hour)
        elif interval_seconds >= 60:  # 大于等于1分钟
            # 按分钟对齐
            dt = dt.replace(second=0, microsecond=0)
            interval_minutes = int(interval_seconds // 60)
            total_minutes = dt.hour * 60 + dt.minute
            aligned_total_minutes = (total_minutes // interval_minutes) * interval_minutes
            aligned_hour = aligned_total_minutes // 60
            aligned_minute = aligned_total_minutes % 60
            return dt.replace(hour=aligned_hour, minute=aligned_minute)
        elif interval_seconds >= 1:  # 秒级别
            # 按秒对齐
            dt = dt.replace(microsecond=0)
            aligned_second = int(dt.second // interval_seconds) * int(interval_seconds)
            return dt.replace(second=aligned_second)
        else:  # 毫秒级别
            # 按毫秒对齐
            total_ms = dt.microsecond / 1000  # 转换为毫秒
            interval_ms = interval_seconds * 1000
            aligned_ms = int(total_ms // interval_ms) * interval_ms
            aligned_microsecond = int(aligned_ms * 1000)
            return dt.replace(microsecond=aligned_microsecond)

    async def get_single_queue_timeline(
        self,
        session: AsyncSession,
        queue_name: str,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        interval: str = "5m"
    ) -> Dict[str, Any]:
        """
        获取单个队列的时间轴数据

        Args:
            session: 数据库会话
            queue_name: 队列名称
            start_time: 开始时间（ISO格式字符串）
            end_time: 结束时间（ISO格式字符串）
            interval: 时间间隔（如 "5m", "1h"）

        Returns:
            时间轴数据
        """
        # 解析时间范围
        if not end_time:
            end_dt = datetime.now(timezone.utc)
        else:
            end_dt = self.parse_iso_datetime(end_time)

        if not start_time:
            start_dt = end_dt - timedelta(hours=1)
        else:
            start_dt = self.parse_iso_datetime(start_time)

        # 解析时间间隔
        interval_minutes = self.parse_interval(interval)

        try:
            # 使用 SQLAlchemy 的原生 SQL 查询（因为复杂的时间分组）
            query = text(f"""
            SELECT
                DATE_TRUNC('minute', created_at) -
                INTERVAL '{interval_minutes} minutes' * (EXTRACT(MINUTE FROM created_at)::int % {interval_minutes}) as time_bucket,
                COUNT(*) as count,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_count,
                SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed_count,
                AVG(CASE WHEN status = 'completed' AND processing_time IS NOT NULL
                    THEN processing_time ELSE NULL END) as avg_processing_time
            FROM tasks
            WHERE queue_name = :queue_name
                AND created_at >= :start_dt
                AND created_at < :end_dt
            GROUP BY time_bucket
            ORDER BY time_bucket
            """)

            result = await session.execute(query, {
                'queue_name': queue_name,
                'start_dt': start_dt,
                'end_dt': end_dt
            })
            rows = result.mappings().all()

            # 构建时间轴数据
            timeline = []
            for row in rows:
                timeline.append({
                    "time": row['time_bucket'].isoformat(),
                    "count": row['count'],
                    "completed_count": row['completed_count'],
                    "failed_count": row['failed_count'],
                    "avg_processing_time": float(row['avg_processing_time']) if row['avg_processing_time'] else 0
                })

            # 填充缺失的时间点
            filled_timeline = []
            current_time = start_dt
            timeline_dict = {item['time']: item for item in timeline}

            while current_time < end_dt:
                time_key = current_time.isoformat()
                if time_key in timeline_dict:
                    filled_timeline.append(timeline_dict[time_key])
                else:
                    filled_timeline.append({
                        "time": time_key,
                        "count": 0,
                        "completed_count": 0,
                        "failed_count": 0,
                        "avg_processing_time": 0
                    })
                current_time += timedelta(minutes=interval_minutes)

            return {
                "timeline": filled_timeline,
                "interval": interval,
                "start_time": start_dt.isoformat(),
                "end_time": end_dt.isoformat()
            }

        except Exception as e:
            logger.error(f"Error fetching timeline from PostgreSQL: {e}")
            return {
                "timeline": [],
                "interval": interval,
                "start_time": start_dt.isoformat(),
                "end_time": end_dt.isoformat(),
                "error": str(e)
            }

    def _build_time_bucket_query(
        self,
        interval_type: str,
        interval_seconds: float,
        interval_minutes: float
    ) -> text:
        """构建时间分组查询"""
        if interval_type == 'millisecond':
            return text(f"""
            SELECT
                DATE_TRUNC('second', created_at) +
                INTERVAL '{interval_seconds} seconds' * FLOOR(EXTRACT(MILLISECONDS FROM created_at) / ({interval_seconds} * 1000)) as time_bucket,
                COUNT(*) as count
            FROM tasks
            WHERE queue_name = :queue_name
                AND created_at >= :start_dt
                AND created_at < :end_dt
            GROUP BY time_bucket
            ORDER BY time_bucket
            """)
        elif interval_type == 'second':
            return text(f"""
            SELECT
                DATE_TRUNC('minute', created_at) +
                INTERVAL '{interval_seconds} seconds' * FLOOR(EXTRACT(SECOND FROM created_at) / {interval_seconds}) as time_bucket,
                COUNT(*) as count
            FROM tasks
            WHERE queue_name = :queue_name
                AND created_at >= :start_dt
                AND created_at < :end_dt
            GROUP BY time_bucket
            ORDER BY time_bucket
            """)
        elif interval_type == 'minute' and interval_minutes < 60:
            return text(f"""
            SELECT
                DATE_TRUNC('hour', created_at) +
                INTERVAL '{interval_minutes} minutes' * FLOOR(EXTRACT(MINUTE FROM created_at) / {interval_minutes}) as time_bucket,
                COUNT(*) as count
            FROM tasks
            WHERE queue_name = :queue_name
                AND created_at >= :start_dt
                AND created_at < :end_dt
            GROUP BY time_bucket
            ORDER BY time_bucket
            """)
        elif interval_minutes == 60:
            return text("""
            SELECT
                DATE_TRUNC('hour', created_at) as time_bucket,
                COUNT(*) as count
            FROM tasks
            WHERE queue_name = :queue_name
                AND created_at >= :start_dt
                AND created_at < :end_dt
            GROUP BY time_bucket
            ORDER BY time_bucket
            """)
        else:
            # 大于1小时的间隔
            interval_hours = int(interval_minutes // 60)
            return text(f"""
            SELECT
                DATE_TRUNC('day', created_at) +
                INTERVAL '{interval_hours} hours' * FLOOR(EXTRACT(HOUR FROM created_at) / {interval_hours}) as time_bucket,
                COUNT(*) as count
            FROM tasks
            WHERE queue_name = :queue_name
                AND created_at >= :start_dt
                AND created_at < :end_dt
            GROUP BY time_bucket
            ORDER BY time_bucket
            """)

    async def get_multiple_queues_timeline(
        self,
        session_factory,
        queues: str,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        获取多个队列的时间轴数据

        Args:
            session_factory: 会话工厂
            queues: 逗号分隔的队列名称列表
            start_time: 开始时间（ISO格式字符串）
            end_time: 结束时间（ISO格式字符串）

        Returns:
            多队列时间轴数据
        """
        # 解析队列列表
        if not queues or queues.strip() == "":
            end_dt = datetime.now(timezone.utc) if not end_time else self.parse_iso_datetime(end_time)
            start_dt = (end_dt - timedelta(hours=1)) if not start_time else self.parse_iso_datetime(start_time)

            return {
                "queues": [],
                "start_time": start_dt.isoformat(),
                "end_time": end_dt.isoformat(),
                "interval": "5m",
                "message": "No queues selected"
            }

        queue_list = [q.strip() for q in queues.split(',') if q.strip()][:10]  # 最多10个队列

        # 解析时间范围
        if not end_time:
            end_dt = datetime.now(timezone.utc)
        else:
            end_dt = self.parse_iso_datetime(end_time)

        if not start_time:
            start_dt = end_dt - timedelta(hours=1)
        else:
            start_dt = self.parse_iso_datetime(start_time)

        logger.info(f'start_dt={start_dt} end_dt={end_dt}')

        # 根据时间范围自动计算合适的时间间隔
        duration = (end_dt - start_dt).total_seconds()
        interval_seconds, interval_type, interval = self.calculate_auto_interval(duration)
        interval_minutes = interval_seconds / 60

        logger.info(f"Time range: {duration}s, using interval: {interval} -> {interval_seconds} seconds, type: {interval_type}")

        result = []

        for queue_name in queue_list:
            try:
                async with session_factory() as session:
                    # 构建查询
                    query = self._build_time_bucket_query(interval_type, interval_seconds, interval_minutes)

                    params = {
                        'queue_name': queue_name,
                        'start_dt': start_dt,
                        'end_dt': end_dt
                    }

                    # 执行查询
                    result_obj = await session.execute(query, params)
                    rows = result_obj.mappings().all()
                    logger.info(f'rows={rows}')

                    # 构建时间轴数据
                    timeline = []
                    for row in rows:
                        timeline.append({
                            "time": row['time_bucket'].isoformat(),
                            "count": row['count']
                        })

                    # 填充缺失的时间点
                    timeline_data = []
                    for item in timeline:
                        dt = datetime.fromisoformat(item['time'])
                        timeline_data.append((dt, item['count']))

                    # 按时间排序
                    timeline_data.sort(key=lambda x: x[0])

                    # 生成完整的时间序列
                    filled_timeline = []
                    current_time = self.align_to_interval(start_dt, interval_seconds)
                    timeline_index = 0

                    while current_time < end_dt:
                        # 查找是否有匹配的数据点
                        tolerance = timedelta(seconds=interval_seconds/2)
                        found = False

                        # 从当前位置开始查找
                        while timeline_index < len(timeline_data):
                            data_time, count = timeline_data[timeline_index]

                            # 计算时间差（秒）
                            time_diff = abs((data_time - current_time).total_seconds())

                            if time_diff < interval_seconds / 2:
                                # 找到匹配的数据
                                filled_timeline.append({
                                    "time": current_time.isoformat(),
                                    "count": count
                                })
                                found = True
                                timeline_index += 1
                                break
                            elif data_time > current_time + tolerance:
                                # 数据时间已经超过当前时间太多，停止查找
                                break
                            else:
                                # 这个数据点太早了，继续查找下一个
                                timeline_index += 1

                        if not found:
                            # 没有找到匹配的数据，填充0
                            filled_timeline.append({
                                "time": current_time.isoformat(),
                                "count": 0
                            })

                        current_time += timedelta(seconds=interval_seconds)

                    result.append({
                        "queue": queue_name,
                        "timeline": {
                            "timeline": filled_timeline,
                            "interval": interval
                        }
                    })

            except Exception as e:
                logger.error(f"Error fetching timeline for queue {queue_name}: {e}")
                result.append({
                    "queue": queue_name,
                    "timeline": {
                        "timeline": [],
                        "interval": interval,
                        "error": str(e)
                    }
                })

        return {
            "queues": result,
            "start_time": start_dt.isoformat(),
            "end_time": end_dt.isoformat(),
            "interval": interval
        }
