"""
Worker 监控服务

提供 Worker 相关的监控功能
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import time

from .redis_monitor_service import RedisMonitorService

logger = logging.getLogger(__name__)


class WorkerMonitorService:
    """Worker 监控服务类"""

    def __init__(self, redis_service: RedisMonitorService):
        """
        初始化 Worker 监控服务

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

    async def get_worker_heartbeats(self, queue_name: str) -> List[Dict[str, Any]]:
        """
        获取指定队列的 Worker 心跳信息

        Args:
            queue_name: 队列名称

        Returns:
            Worker 心跳信息列表
        """
        worker_list = []
        current_time = datetime.now(timezone.utc).timestamp()

        try:
            # 使用 WorkerManager 获取所有 worker
            from jettask.worker.lifecycle import WorkerManager

            worker_manager = WorkerManager(
                redis_client=self.redis,
                redis_prefix=self.redis_prefix
            )

            # 获取所有 worker ID
            worker_ids = await worker_manager.get_all_workers()
            if not worker_ids:
                logger.debug(f"No workers found for queue {queue_name}")
                return []

            worker_keys = [f"{self.redis_prefix}:WORKER:{wid}" for wid in worker_ids]

            # 批量获取所有 worker 数据
            pipe = self.redis.pipeline()
            for key in worker_keys:
                pipe.hgetall(key)
            all_workers_data = await pipe.execute()

            # 处理每个 worker
            for i, worker_data in enumerate(all_workers_data):
                if not worker_data:
                    continue

                # 检查 worker 是否属于指定队列
                worker_queues = worker_data.get('queues', '')
                if queue_name not in worker_queues.split(','):
                    continue

                worker_id = worker_keys[i].split(':')[-1]
                last_heartbeat = float(worker_data.get('last_heartbeat', 0))
                is_alive = worker_data.get('is_alive', 'true').lower() == 'true'
                consumer_id = worker_data.get('consumer_id', worker_id)

                # 构建显示数据
                display_data = {
                    'consumer_id': consumer_id,
                    'consumer_name': f"{consumer_id}-{queue_name}",
                    'host': worker_data.get('host', 'unknown'),
                    'pid': int(worker_data.get('pid', 0)),
                    'queue': queue_name,
                    'last_heartbeat': last_heartbeat,
                    'last_heartbeat_time': datetime.fromtimestamp(last_heartbeat).isoformat(),
                    'seconds_ago': int(current_time - last_heartbeat),
                    'is_alive': is_alive,
                    # 队列特定的统计信息
                    'success_count': int(worker_data.get(f'{queue_name}:success_count', 0)),
                    'failed_count': int(worker_data.get(f'{queue_name}:failed_count', 0)),
                    'total_count': int(worker_data.get(f'{queue_name}:total_count', 0)),
                    'running_tasks': int(worker_data.get(f'{queue_name}:running_tasks', 0)),
                    'avg_processing_time': float(worker_data.get(f'{queue_name}:avg_processing_time', 0.0)),
                    'avg_latency_time': float(worker_data.get(f'{queue_name}:avg_latency_time', 0.0))
                }

                # 如果离线时间存在，添加离线时间信息
                if 'offline_time' in worker_data:
                    display_data['offline_time'] = float(worker_data['offline_time'])
                    display_data['offline_time_formatted'] = datetime.fromtimestamp(
                        float(worker_data['offline_time'])
                    ).isoformat()

                worker_list.append(display_data)

            logger.info(f"Retrieved {len(worker_list)} workers for queue {queue_name}")
            return worker_list

        except Exception as e:
            logger.error(f"Error getting worker heartbeats for queue {queue_name}: {e}", exc_info=True)
            return []

    async def get_queue_worker_summary(self, queue_name: str) -> Dict[str, Any]:
        """
        获取队列的 Worker 汇总统计信息（包含历史数据）

        Args:
            queue_name: 队列名称

        Returns:
            Worker 汇总统计字典
        """
        try:
            # 使用 WorkerManager
            from jettask.worker.lifecycle import WorkerManager

            worker_manager = WorkerManager(
                redis_client=self.redis,
                redis_prefix=self.redis_prefix
            )

            # 获取所有 worker ID
            worker_ids = await worker_manager.get_all_workers()
            worker_keys = [f"{self.redis_prefix}:WORKER:{wid}" for wid in worker_ids]

            if not worker_keys:
                return self._empty_summary()

            # 批量获取 worker 数据
            pipe = self.redis.pipeline()
            for key in worker_keys:
                pipe.hgetall(key)
            all_workers_data = await pipe.execute()

            # 过滤属于该队列的 worker
            queue_workers_data = []
            for worker_data in all_workers_data:
                if worker_data and queue_name in worker_data.get('queues', '').split(','):
                    queue_workers_data.append(worker_data)

            # 汇总统计
            stats = self._calculate_worker_stats(queue_workers_data, queue_name, include_history=True)
            stats['history_included'] = True

            logger.debug(f"Worker summary for queue {queue_name}: {stats}")
            return stats

        except Exception as e:
            logger.error(f"Error getting queue worker summary for {queue_name}: {e}", exc_info=True)
            return self._empty_summary()

    async def get_queue_worker_summary_fast(self, queue_name: str) -> Dict[str, Any]:
        """
        获取队列的 Worker 汇总统计信息（快速版，仅在线 Worker）

        Args:
            queue_name: 队列名称

        Returns:
            Worker 汇总统计字典
        """
        try:
            # 使用 WorkerManager
            from jettask.worker.lifecycle import WorkerManager

            worker_manager = WorkerManager(
                redis_client=self.redis,
                redis_prefix=self.redis_prefix
            )

            # 获取所有 worker ID
            worker_ids = await worker_manager.get_all_workers()
            worker_keys = [f"{self.redis_prefix}:WORKER:{wid}" for wid in worker_ids]

            if not worker_keys:
                return self._empty_summary()

            # 批量获取 worker 数据
            pipe = self.redis.pipeline()
            for worker_key in worker_keys:
                pipe.hgetall(worker_key)

            all_workers_data = await pipe.execute()

            # 过滤属于该队列的 worker
            worker_data_list = []
            for worker_data in all_workers_data:
                if worker_data and queue_name in worker_data.get('queues', '').split(','):
                    worker_data_list.append(worker_data)

            # 汇总统计（仅在线 Worker）
            stats = self._calculate_worker_stats(worker_data_list, queue_name, include_history=False)

            logger.debug(f"Fast worker summary for queue {queue_name}: {stats}")
            return stats

        except Exception as e:
            logger.error(f"Error getting fast queue worker summary for {queue_name}: {e}", exc_info=True)
            return self._empty_summary()

    async def get_worker_offline_history(
        self,
        limit: int = 100,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        获取 Worker 下线历史记录

        Args:
            limit: 返回记录数量限制
            start_time: 开始时间戳（可选）
            end_time: 结束时间戳（可选）

        Returns:
            离线历史记录列表
        """
        try:
            # 使用 WorkerManager
            from jettask.worker.lifecycle import WorkerManager

            worker_manager = WorkerManager(
                redis_client=self.redis,
                redis_prefix=self.redis_prefix
            )

            # 获取所有 worker ID
            worker_ids = await worker_manager.get_all_workers()
            worker_keys = [f"{self.redis_prefix}:WORKER:{wid}" for wid in worker_ids]

            if not worker_keys:
                return []

            # 批量获取所有 worker 数据
            pipe = self.redis.pipeline()
            for key in worker_keys:
                pipe.hgetall(key)
            all_workers_data = await pipe.execute()

            # 收集离线的 worker
            offline_workers = []

            for worker_data in all_workers_data:
                if not worker_data:
                    continue

                # 检查是否离线
                is_alive = worker_data.get('is_alive', 'true').lower() == 'true'
                if not is_alive and 'offline_time' in worker_data:
                    offline_time = float(worker_data.get('offline_time', 0))

                    # 时间范围过滤
                    if start_time and offline_time < start_time:
                        continue
                    if end_time and offline_time > end_time:
                        continue

                    # 构建离线记录
                    record = self._build_offline_record(worker_data, offline_time)
                    offline_workers.append((offline_time, record))

            # 按离线时间倒序排序
            offline_workers.sort(key=lambda x: x[0], reverse=True)

            # 返回指定数量的记录
            result = [record for _, record in offline_workers[:limit]]
            logger.info(f"Retrieved {len(result)} offline worker records")
            return result

        except Exception as e:
            logger.error(f"Error getting worker offline history: {e}", exc_info=True)
            return []

    def _empty_summary(self) -> Dict[str, Any]:
        """返回空的汇总统计"""
        return {
            'total_workers': 0,
            'online_workers': 0,
            'offline_workers': 0,
            'total_success_count': 0,
            'total_failed_count': 0,
            'total_count': 0,
            'total_running_tasks': 0,
            'avg_processing_time': 0.0,
            'avg_latency_time': 0.0
        }

    def _calculate_worker_stats(
        self,
        workers_data: List[Dict[str, Any]],
        queue_name: str,
        include_history: bool
    ) -> Dict[str, Any]:
        """
        计算 Worker 统计信息

        Args:
            workers_data: Worker 数据列表
            queue_name: 队列名称
            include_history: 是否包含离线 Worker 的历史数据

        Returns:
            统计信息字典
        """
        total_workers = len(workers_data)
        online_workers = 0
        offline_workers = 0
        total_success_count = 0
        total_failed_count = 0
        total_count = 0
        total_running_tasks = 0
        total_processing_time = 0.0
        processing_time_count = 0
        total_latency_time = 0.0
        latency_time_count = 0

        current_time = datetime.now(timezone.utc).timestamp()

        for worker_data in workers_data:
            try:
                last_heartbeat = float(worker_data.get('last_heartbeat', 0))
                is_alive = worker_data.get('is_alive', 'true').lower() == 'true'

                is_online = is_alive and (current_time - last_heartbeat) < 30

                if is_online:
                    online_workers += 1
                else:
                    offline_workers += 1
                    # 如果不包含历史，跳过离线 Worker 的统计
                    if not include_history:
                        continue

                # 统计数据
                success_count = int(worker_data.get(f'{queue_name}:success_count', 0))
                failed_count = int(worker_data.get(f'{queue_name}:failed_count', 0))
                running_tasks = int(worker_data.get(f'{queue_name}:running_tasks', 0))
                avg_processing_time = float(worker_data.get(f'{queue_name}:avg_processing_time', 0.0))
                avg_latency_time = float(worker_data.get(f'{queue_name}:avg_latency_time', 0.0))

                total_success_count += success_count
                total_failed_count += failed_count
                total_count += success_count + failed_count
                total_running_tasks += running_tasks

                if avg_processing_time > 0:
                    total_processing_time += avg_processing_time
                    processing_time_count += 1

                if avg_latency_time > 0:
                    total_latency_time += avg_latency_time
                    latency_time_count += 1

            except Exception as e:
                logger.warning(f"Error processing worker stats: {e}")
                continue

        # 计算平均值
        overall_avg_processing_time = 0.0
        if processing_time_count > 0:
            overall_avg_processing_time = total_processing_time / processing_time_count

        overall_avg_latency_time = 0.0
        if latency_time_count > 0:
            overall_avg_latency_time = total_latency_time / latency_time_count

        return {
            'total_workers': total_workers,
            'online_workers': online_workers,
            'offline_workers': offline_workers,
            'total_success_count': total_success_count,
            'total_failed_count': total_failed_count,
            'total_count': total_count,
            'total_running_tasks': total_running_tasks,
            'avg_processing_time': round(overall_avg_processing_time, 3),
            'avg_latency_time': round(overall_avg_latency_time, 3)
        }

    def _build_offline_record(self, worker_data: Dict[str, Any], offline_time: float) -> Dict[str, Any]:
        """
        构建离线记录

        Args:
            worker_data: Worker 数据
            offline_time: 离线时间戳

        Returns:
            离线记录字典
        """
        # 计算运行时长
        online_time = float(worker_data.get('created_at', offline_time))
        duration_seconds = int(offline_time - online_time)

        # 基础记录
        record = {
            'consumer_id': worker_data.get('consumer_id', ''),
            'host': worker_data.get('host', 'unknown'),
            'pid': int(worker_data.get('pid', 0)),
            'queues': worker_data.get('queues', ''),
            'online_time': online_time,
            'offline_time': offline_time,
            'duration_seconds': duration_seconds,
            'last_heartbeat': float(worker_data.get('last_heartbeat', 0)),
            'shutdown_reason': worker_data.get('shutdown_reason', 'unknown'),
            'online_time_str': datetime.fromtimestamp(online_time).isoformat(),
            'offline_time_str': datetime.fromtimestamp(offline_time).isoformat(),
        }

        # 格式化运行时长
        hours = duration_seconds // 3600
        minutes = (duration_seconds % 3600) // 60
        seconds = duration_seconds % 60
        record['duration_str'] = f"{hours}h {minutes}m {seconds}s"

        # 添加统计信息（聚合所有队列的数据）
        queues = worker_data.get('queues', '').split(',') if worker_data.get('queues') else []
        total_success = 0
        total_failed = 0
        total_count = 0
        total_processing_time = 0.0

        for queue in queues:
            if queue.strip():
                queue = queue.strip()
                total_success += int(worker_data.get(f'{queue}:success_count', 0))
                total_failed += int(worker_data.get(f'{queue}:failed_count', 0))
                count = int(worker_data.get(f'{queue}:total_count', 0))
                total_count += count

                avg_time = float(worker_data.get(f'{queue}:avg_processing_time', 0))
                if avg_time > 0 and count > 0:
                    total_processing_time += avg_time * count

        record['total_success_count'] = total_success
        record['total_failed_count'] = total_failed
        record['total_count'] = total_count
        record['total_running_tasks'] = 0  # 离线 worker 没有运行中的任务

        # 计算平均处理时间
        if total_count > 0:
            record['avg_processing_time'] = total_processing_time / total_count
        else:
            record['avg_processing_time'] = 0.0

        return record
