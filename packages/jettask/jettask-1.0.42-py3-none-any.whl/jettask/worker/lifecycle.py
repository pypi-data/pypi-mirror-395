import os
import time
import asyncio
import logging
import json
from typing import Dict, List, Optional, Set, Callable, Any
import msgpack

from .heartbeat import HeartbeatManager

logger = logging.getLogger(__name__)


# ============================================================================
# Worker 状态管理
# ============================================================================

class WorkerManager:
    """Worker管理器 - Worker状态的唯一管理入口

    ⚠️ 重要：所有Worker状态的修改都必须通过这个类进行，不要直接操作Redis！

    职责:
    1. Worker ID 生成和复用
    2. Worker 注册表管理
    3. Worker 状态字段的读写
    4. Redis Pub/Sub 状态变更通知
    5. Worker 查询和统计
    """

    def __init__(self, redis_client, async_redis_client, redis_prefix: str = "jettask", event_pool=None,
                 queue_formatter=None, queue_registry=None, app=None, tasks: dict = None,
                 task_event_queues: dict = None, worker_id: str = None):
        """初始化Worker状态管理器

        Args:
            redis_client: 同步Redis客户端
            async_redis_client: 异步Redis客户端
            redis_prefix: Redis key前缀
            event_pool: EventPool实例（可选），用于事件驱动的消息恢复
            queue_formatter: 队列格式化函数
            queue_registry: 队列注册表
            app: App实例（用于访问worker_state_manager和worker_id）
            tasks: 任务字典 {task_name: task_obj}
            task_event_queues: 任务事件队列字典 {task_name: asyncio.Queue}
            worker_id: 当前 worker ID
        """
        self.sync_redis = redis_client
        self.redis = async_redis_client
        self.async_redis = async_redis_client
        self.redis_prefix = redis_prefix
        self.active_workers_key = f"{redis_prefix}:ACTIVE_WORKERS"
        self.workers_registry_key = f"{redis_prefix}:REGISTRY:WORKERS"
        self.event_pool = event_pool
        self.worker_prefix = 'WORKER'

        # Pub/Sub通道名称
        self.worker_state_channel = f"{redis_prefix}:WORKER_STATE_CHANGE"

        # 监听器订阅
        self._pubsub = None
        self._listener_task: Optional[asyncio.Task] = None
        self._running = False
        self._callbacks: Set[Callable] = set()

        # Pub/Sub 配置
        self._health_check_interval = 60
        self._health_check_task: Optional[asyncio.Task] = None

        # Worker扫描器相关（从 WorkerScanner 合并）
        self._initialized = False
        self._last_full_sync = 0
        self._full_sync_interval = 60
        self._scan_counter = 0
        self._partial_check_interval = 10

        # 离线 Worker 恢复相关（从 OfflineWorkerRecovery 合并）
        self._stop_recovery = False
        self._recovery_task = None  # 用于存储后台恢复任务
        self.queue_formatter = queue_formatter or (lambda q: f"{self.redis_prefix}:QUEUE:{q}")
        self.worker_state_manager = app.worker_state_manager if (app and hasattr(app, 'worker_state_manager')) else None
        self.queue_registry = queue_registry
        self.app = app
        self.tasks = tasks or {}
        self.task_event_queues = task_event_queues or {}
        self.worker_id = worker_id

        # 离线 Worker 清理相关
        self._stop_cleanup = False
        self._cleanup_task = None  # 用于存储后台清理任务

    def _get_worker_key(self, worker_id: str) -> str:
        """获取worker的Redis key"""
        return f"{self.redis_prefix}:WORKER:{worker_id}"

    async def initialize_worker(self, worker_id: str, worker_info: Dict[str, Any]):
        """初始化worker（首次创建）"""
        worker_key = self._get_worker_key(worker_id)
        current_time = time.time()

        worker_info.setdefault('is_alive', 'true')
        worker_info.setdefault('messages_transferred', 'false')
        worker_info.setdefault('created_at', str(current_time))
        worker_info.setdefault('last_heartbeat', str(current_time))

        pipeline = self.redis.pipeline()
        pipeline.hset(worker_key, mapping=worker_info)
        pipeline.zadd(self.active_workers_key, {worker_id: current_time})
        await pipeline.execute()

        logger.debug(f"Initialized worker {worker_id}")

    async def set_worker_online(self, worker_id: str, worker_data: dict = None):
        """设置worker为在线状态"""
        worker_key = self._get_worker_key(worker_id)
        old_alive = await self.redis.hget(worker_key, 'is_alive')
        old_alive = old_alive.decode('utf-8') if isinstance(old_alive, bytes) else old_alive

        current_time = time.time()
        pipeline = self.redis.pipeline()
        pipeline.hset(worker_key, 'is_alive', 'true')
        pipeline.hset(worker_key, 'last_heartbeat', str(current_time))

        # 当 worker 从离线变为在线时，重置 messages_transferred
        # 这表示是一个新的 worker 实例，还没有进行消息转移
        if old_alive != 'true':
            pipeline.hset(worker_key, 'messages_transferred', 'false')

        if worker_data:
            pipeline.hset(worker_key, mapping=worker_data)

        pipeline.zadd(self.active_workers_key, {worker_id: current_time})
        await pipeline.execute()

        if old_alive != 'true':
            await self._publish_state_change(worker_id, 'online')
            logger.debug(f"Worker {worker_id} is now ONLINE")

    async def set_worker_offline(self, worker_id: str, reason: str = "unknown"):
        """设置worker为离线状态"""
        worker_key = self._get_worker_key(worker_id)
        old_alive = await self.redis.hget(worker_key, 'is_alive')
        old_alive = old_alive.decode('utf-8') if isinstance(old_alive, bytes) else old_alive

        current_time = time.time()
        pipeline = self.redis.pipeline()
        pipeline.hset(worker_key, 'messages_transferred', 'false')  # 重置消息转移标记，允许其他worker接管消息
        pipeline.hset(worker_key, 'is_alive', 'false')
        pipeline.hset(worker_key, 'offline_reason', reason)
        pipeline.hset(worker_key, 'offline_time', str(current_time))
        pipeline.zrem(self.active_workers_key, worker_id)
        await pipeline.execute()

        if old_alive == 'true':
            await self._publish_state_change(worker_id, 'offline', reason)
            logger.debug(f"Worker {worker_id} is now OFFLINE (reason: {reason})")

    async def update_worker_heartbeat(self, worker_id: str, heartbeat_data: dict = None):
        """更新worker心跳（确保在线状态）"""
        worker_key = self._get_worker_key(worker_id)
        current_time = time.time()

        pipeline = self.redis.pipeline()
        pipeline.hset(worker_key, 'is_alive', 'true')
        pipeline.hset(worker_key, 'last_heartbeat', str(current_time))

        if heartbeat_data:
            pipeline.hset(worker_key, mapping=heartbeat_data)

        pipeline.zadd(self.active_workers_key, {worker_id: current_time})
        await pipeline.execute()

    async def update_worker_field(self, worker_id: str, field: str, value: str):
        """更新worker的单个字段"""
        worker_key = self._get_worker_key(worker_id)
        await self.redis.hset(worker_key, field, value)

    async def update_worker_fields(self, worker_id: str, fields: Dict[str, Any]):
        """批量更新worker的多个字段"""
        worker_key = self._get_worker_key(worker_id)
        await self.redis.hset(worker_key, mapping=fields)

    async def record_group_info(
        self,
        worker_id: str,
        queue: str,
        task_name: str,
        group_name: str,
        consumer_name: str,
        redis_prefix: str
    ):
        """记录 task 的 group 信息到 worker hash 表

        Args:
            worker_id: Worker ID
            queue: 队列名（不带前缀）
            task_name: 任务名
            group_name: Consumer group 名称
            consumer_name: Consumer 名称
            redis_prefix: Redis 前缀
        """
        try:
            worker_key = self._get_worker_key(worker_id)

            # 构建 group 信息
            group_info = {
                'queue': queue,
                'task_name': task_name,
                'group_name': group_name,
                'consumer_name': consumer_name,
                'stream_key': f"{redis_prefix}:QUEUE:{queue}"
            }

            # 将 group 信息存储到 worker 的 hash 中
            field_name = f"group_info:{queue}"
            await self.redis.hset(
                worker_key,
                field_name,
                json.dumps(group_info)
            )
            # logger.debug(f"{field_name=} Recorded group info for worker {worker_id}, task {task_name}: {group_info}")

        except Exception as e:
            logger.error(f"Error recording group info for worker {worker_id}: {e}", exc_info=True)

    def update_worker_field_sync(self, worker_id: str, field: str, value: str):
        """更新worker的单个字段（同步版本，供心跳线程使用）"""
        worker_key = self._get_worker_key(worker_id)
        self.sync_redis.hset(worker_key, field, value)
        logger.debug(f"Updated worker {worker_id} field {field}={value}")

    def update_worker_fields_sync(self, worker_id: str, fields: Dict[str, Any]):
        """批量更新worker的多个字段（同步版本，供心跳线程使用）"""
        worker_key = self._get_worker_key(worker_id)
        self.sync_redis.hset(worker_key, mapping=fields)
        logger.debug(f"Updated worker {worker_id} fields: {list(fields.keys())}")

    async def increment_queue_stats(self, worker_id: str, queue: str,
                                   running_tasks_delta: int = None,
                                   success_count_increment: int = None,
                                   failed_count_increment: int = None,
                                   total_count_increment: int = None,
                                   processing_time_increment: float = None,
                                   latency_time_increment: float = None):
        """增量更新worker在特定队列上的累积统计信息"""
        worker_key = self._get_worker_key(worker_id)
        pipeline = self.redis.pipeline()

        if running_tasks_delta is not None and running_tasks_delta != 0:
            pipeline.hincrby(worker_key, f'{queue}:running_tasks', running_tasks_delta)

        if success_count_increment is not None:
            pipeline.hincrby(worker_key, f'{queue}:success_count', success_count_increment)

        if failed_count_increment is not None:
            pipeline.hincrby(worker_key, f'{queue}:failed_count', failed_count_increment)

        if total_count_increment is not None:
            pipeline.hincrby(worker_key, f'{queue}:total_count', total_count_increment)

        if processing_time_increment is not None:
            pipeline.hincrbyfloat(worker_key, f'{queue}:total_processing_time', processing_time_increment)

        if latency_time_increment is not None:
            pipeline.hincrbyfloat(worker_key, f'{queue}:total_latency_time', latency_time_increment)

        await pipeline.execute()

    async def get_queue_total_stats(self, worker_id: str, queue: str) -> dict:
        """获取队列的累积统计数据"""
        worker_key = self._get_worker_key(worker_id)
        fields = [
            f'{queue}:total_count',
            f'{queue}:total_processing_time',
            f'{queue}:total_latency_time'
        ]
        values = await self.redis.hmget(worker_key, fields)

        return {
            'total_count': int(values[0]) if values[0] else 0,
            'total_processing_time': float(values[1]) if values[1] else 0.0,
            'total_latency_time': float(values[2]) if values[2] else 0.0
        }

    async def update_queue_stats(self, worker_id: str, queue: str,
                                 running_tasks: int = None,
                                 avg_processing_time: float = None,
                                 avg_latency_time: float = None):
        """更新worker在特定队列上的统计信息"""
        worker_key = self._get_worker_key(worker_id)
        pipeline = self.redis.pipeline()

        if running_tasks is not None:
            pipeline.hset(worker_key, f'{queue}:running_tasks', str(running_tasks))

        if avg_processing_time is not None:
            pipeline.hset(worker_key, f'{queue}:avg_processing_time', f'{avg_processing_time:.3f}')

        if avg_latency_time is not None:
            pipeline.hset(worker_key, f'{queue}:avg_latency_time', f'{avg_latency_time:.3f}')

        await pipeline.execute()

    async def mark_messages_transferred(self, worker_id: str, transferred: bool = True):
        """标记worker的消息是否已转移"""
        worker_key = self._get_worker_key(worker_id)
        await self.redis.hset(worker_key, 'messages_transferred', 'true' if transferred else 'false')

    async def get_worker_info(self, worker_id: str) -> Optional[Dict[str, str]]:
        """获取worker的完整信息"""
        worker_key = self._get_worker_key(worker_id)
        data = await self.redis.hgetall(worker_key)

        if not data:
            return None

        result = {}
        for k, v in data.items():
            key = k.decode('utf-8') if isinstance(k, bytes) else k
            value = v.decode('utf-8') if isinstance(v, bytes) else v
            result[key] = value

        return result

    async def get_worker_field(self, worker_id: str, field: str) -> Optional[str]:
        """获取worker的单个字段值"""
        worker_key = self._get_worker_key(worker_id)
        value = await self.redis.hget(worker_key, field)

        if value is None:
            return None

        return value.decode('utf-8') if isinstance(value, bytes) else value

    async def is_worker_alive(self, worker_id: str) -> bool:
        """检查worker是否在线"""
        is_alive = await self.get_worker_field(worker_id, 'is_alive')
        return is_alive == 'true'

    # ========== Worker ID 生成和复用 ==========

    def generate_worker_id(self, prefix: str) -> str:
        """
        生成新的 Worker ID

        格式: {prefix}-{uuid}-{pid}
        例如: YYDG-a1b2c3d4-12345

        Args:
            prefix: Worker ID 前缀（通常是主机名）

        Returns:
            生成的 Worker ID
        """
        import uuid
        return f"{prefix}-{uuid.uuid4().hex[:8]}-{os.getpid()}"

    async def find_reusable_worker_id(self, prefix: str) -> Optional[str]:
        """
        查找可复用的离线 Worker ID

        Args:
            prefix: Worker ID 前缀

        Returns:
            可复用的 Worker ID，如果没有则返回 None
        """
        try:
            offline_workers = await self.get_offline_workers()

            for worker_id in offline_workers:
                if isinstance(worker_id, bytes):
                    worker_id = worker_id.decode('utf-8')
                if worker_id.startswith(prefix):
                    logger.debug(f"Found reusable worker ID: {worker_id}")
                    return worker_id
        except Exception as e:
            logger.warning(f"Error finding reusable worker ID: {e}")

        return None

    # ========== Worker 注册表管理 ==========

    async def register_worker(self, worker_id: str):
        """注册 Worker 到全局注册表"""
        await self.async_redis.sadd(self.workers_registry_key, worker_id)
        logger.debug(f"Registered worker: {worker_id}")

    async def unregister_worker(self, worker_id: str):
        """从全局注册表注销 Worker"""
        await self.async_redis.srem(self.workers_registry_key, worker_id)
        logger.debug(f"Unregistered worker: {worker_id}")

    async def get_all_workers(self) -> Set[str]:
        """获取所有已注册的 Worker ID"""
        return await self.async_redis.smembers(self.workers_registry_key)

    def get_all_workers_sync(self) -> Set[str]:
        """同步方式获取所有已注册的 Worker ID"""
        return self.sync_redis.smembers(self.workers_registry_key)

    async def get_worker_count(self) -> int:
        """获取已注册的 Worker 总数"""
        return await self.async_redis.scard(self.workers_registry_key)

    async def get_offline_workers(self) -> Set[str]:
        """获取所有离线的 Worker ID

        离线 Worker 是指已注册但 is_alive=false 的 Worker
        """
        all_workers = await self.get_all_workers()
        offline_workers = set()

        for worker_id in all_workers:
            if isinstance(worker_id, bytes):
                worker_id = worker_id.decode('utf-8')

            worker_key = f"{self.redis_prefix}:WORKER:{worker_id}"
            is_alive = await self.async_redis.hget(worker_key, 'is_alive')

            if is_alive:
                is_alive = is_alive.decode('utf-8') if isinstance(is_alive, bytes) else is_alive
                if is_alive != 'true':
                    offline_workers.add(worker_id)
            else:
                # Worker key 不存在或没有 is_alive 字段，认为离线
                offline_workers.add(worker_id)

        return offline_workers

    async def get_workers_for_task(self, task_name: str, only_alive: bool = True) -> Set[str]:
        """获取执行特定任务的 Worker 列表

        通过检查 WORKER:* hash 中的 group_info 字段来判断哪些 Worker 在处理该任务

        Args:
            task_name: 任务名称
            only_alive: 是否只返回在线的 Worker（默认 True）

        Returns:
            处理该任务的 Worker ID 集合
        """
        all_worker_ids = await self.get_all_workers()
        matched_workers = set()
        group_info_prefix = f"group_info:{self.redis_prefix}:QUEUE:"

        for worker_id in all_worker_ids:
            if isinstance(worker_id, bytes):
                worker_id = worker_id.decode('utf-8')

            worker_key = f"{self.redis_prefix}:WORKER:{worker_id}"
            worker_info = await self.async_redis.hgetall(worker_key)

            if not worker_info:
                continue

            # 解码 bytes keys
            decoded_info = {}
            for k, v in worker_info.items():
                key = k.decode('utf-8') if isinstance(k, bytes) else k
                val = v.decode('utf-8') if isinstance(v, bytes) else v
                decoded_info[key] = val

            # 检查 is_alive 状态
            if only_alive:
                is_alive = decoded_info.get('is_alive', 'false')
                if is_alive != 'true':
                    continue

            # 检查是否包含该任务的 group_info
            # 格式: group_info:test5:QUEUE:robust_bench2:benchmark_task
            for key in decoded_info.keys():
                if key.startswith(group_info_prefix):
                    parts = key.split(':')
                    if len(parts) >= 5:
                        worker_task_name = parts[-1]  # 最后一部分是 task_name
                        if worker_task_name == task_name:
                            matched_workers.add(worker_id)
                            break

        return matched_workers

    async def get_active_worker_count_for_task(self, task_name: str) -> int:
        """获取执行特定任务的在线 Worker 数量

        Args:
            task_name: 任务名称

        Returns:
            在线 Worker 数量
        """
        workers = await self.get_workers_for_task(task_name, only_alive=True)
        return len(workers)

    async def find_all_offline_workers(
        self,
        worker_prefix: str = 'WORKER'
    ):
        """查找所有离线的 Worker（生成器）

        查找条件：
        1. Worker 已离线（is_alive=false）
        2. 消息未转移（messages_transferred=false）

        Args:
            worker_prefix: Worker 键前缀（默认 'WORKER'）

        Yields:
            (worker_key, worker_data) 元组
        """
        try:
            # 获取所有 worker ID
            worker_ids = await self.get_all_workers()
            logger.debug(f"[Recovery] Scanning {len(worker_ids)} workers in registry")

            for worker_id in worker_ids:
                # 解码 worker_id（可能是 bytes）
                if isinstance(worker_id, bytes):
                    worker_id = worker_id.decode('utf-8')

                # 构建 worker key
                worker_key = f"{self.redis_prefix}:{worker_prefix}:{worker_id}"

                try:
                    # 直接使用自身的方法读取 worker 信息
                    decoded_worker_data = await self.get_worker_info(worker_id)

                    if not decoded_worker_data:
                        continue

                    # 检查 worker 是否离线且消息未转移
                    is_alive = decoded_worker_data.get('is_alive', 'false') == 'true'
                    messages_transferred = decoded_worker_data.get('messages_transferred', 'false') == 'true'

                    # 找到离线且消息未转移的 worker，立即 yield
                    if not is_alive and not messages_transferred:
                        logger.debug(
                            f"[Recovery] Found offline worker: {worker_id}, "
                            f"is_alive={is_alive}, "
                            f"messages_transferred={messages_transferred}"
                        )
                        yield (worker_key, decoded_worker_data)

                except Exception as e:
                    logger.error(f"[Recovery] Error processing worker key {worker_key}: {e}")
                    continue

        except Exception as e:
            logger.error(f"[Recovery] Error finding all offline workers: {e}")

    async def find_offline_workers_for_task(
        self,
        task_name: str,
        worker_prefix: str = 'WORKER'
    ) -> List[tuple]:
        """查找指定任务的离线 Worker

        查找条件：
        1. Worker 已离线（is_alive=false）
        2. 消息未转移（messages_transferred=false）
        3. Worker 的 group_info 中有该任务

        Args:
            task_name: 任务名称
            worker_prefix: Worker 键前缀（默认 'WORKER'）

        Returns:
            离线 Worker 列表，每项为 (worker_key, worker_data) 元组
        """
        # 获取所有离线 workers
        all_offline_workers = await self.find_all_offline_workers(worker_prefix)
        logger.debug(f"[Recovery] Found {len(all_offline_workers)} offline workers, filtering for task {task_name}")

        # 筛选出包含指定任务的 workers
        task_offline_workers = []

        for worker_key, worker_data in all_offline_workers:
            # 检查 worker 的 group_info 中是否有该任务
            has_task = False
            for key, value in worker_data.items():
                if key.startswith('group_info:'):
                    try:
                        import json
                        group_info = json.loads(value)
                        if group_info.get('task_name') == task_name:
                            has_task = True
                            break
                    except Exception as e:
                        logger.error(f"[Recovery] Error parsing group_info: {e}")

            if has_task:
                # 从 worker_key 中提取 worker_id
                worker_id = worker_key.split(':')[-1]
                logger.debug(
                    f"[Recovery] Found offline worker needing recovery: {worker_id}, task={task_name}"
                )
                task_offline_workers.append((worker_key, worker_data))
            else:
                worker_id = worker_key.split(':')[-1]
                logger.debug(
                    f"[Recovery] Worker {worker_id} is offline but not responsible for task {task_name}"
                )

        logger.debug(f"[Recovery] Found {len(task_offline_workers)} offline workers for task {task_name}")
        return task_offline_workers

    async def get_all_workers_info(self, only_alive: bool = True) -> Dict[str, Dict[str, str]]:
        """获取所有worker的信息"""
        pattern = f"{self.redis_prefix}:WORKER:*"
        result = {}

        cursor = 0
        while True:
            cursor, keys = await self.redis.scan(cursor, match=pattern, count=100)

            for key in keys:
                if isinstance(key, bytes):
                    key = key.decode('utf-8')

                parts = key.split(":")
                if len(parts) >= 3:
                    worker_id = parts[2]
                    worker_info = await self.get_worker_info(worker_id)
                    if worker_info:
                        if only_alive and worker_info.get('is_alive') != 'true':
                            continue
                        result[worker_id] = worker_info

            if cursor == 0:
                break

        return result

    async def delete_worker(self, worker_id: str, unregister: bool = True):
        """删除worker的所有数据

        Args:
            worker_id: Worker ID
            unregister: 是否同时从注册表注销（默认 True）
        """
        worker_key = self._get_worker_key(worker_id)
        pipeline = self.redis.pipeline()
        pipeline.delete(worker_key)  # 删除 worker hash
        pipeline.zrem(self.active_workers_key, worker_id)  # 从活跃 workers 中移除

        if unregister:
            pipeline.srem(self.workers_registry_key, worker_id)  # 从注册表中注销

        await pipeline.execute()
        logger.debug(f"Deleted worker {worker_id}" + (" and unregistered" if unregister else ""))

    async def _publish_state_change(self, worker_id: str, state: str, reason: str = None):
        """发布状态变更信号"""
        message = {
            'worker_id': worker_id,
            'state': state,
            'timestamp': asyncio.get_event_loop().time()
        }

        if reason:
            message['reason'] = reason

        await self.redis.publish(
            self.worker_state_channel,
            json.dumps(message)
        )

        logger.debug(f"Published state change: {message}")

    async def start_listener(self):
        """启动状态变更监听器"""
        if self._running:
            logger.warning("Worker state listener already running")
            return

        self._running = True
        self._pubsub = await self._create_and_subscribe_pubsub()
        self._listener_task = asyncio.create_task(self._listen_loop())
        self._health_check_task = asyncio.create_task(self._health_check_loop())

        logger.debug(f"Started worker state listener on channel: {self.worker_state_channel}")

    async def stop_listener(self):
        """停止状态变更监听器"""
        if not self._running:
            return

        self._running = False

        if self._listener_task:
            self._listener_task.cancel()
            try:
                await self._listener_task
            except asyncio.CancelledError:
                pass

        if self._health_check_task:
            self._health_check_task.cancel()
            try:
                await self._health_check_task
            except asyncio.CancelledError:
                pass

        if self._pubsub:
            await self._pubsub.unsubscribe(self.worker_state_channel)
            await self._pubsub.close()

        logger.debug("Stopped worker state listener")

    async def _create_and_subscribe_pubsub(self):
        """创建 PubSub 连接并订阅频道"""
        if self._pubsub:
            try:
                await self._pubsub.close()
            except:
                pass

        pubsub = self.redis.pubsub()
        await pubsub.subscribe(self.worker_state_channel)

        # 标记PubSub连接，防止被空闲连接清理
        if hasattr(pubsub, 'connection') and pubsub.connection:
            pubsub.connection._is_pubsub_connection = True
            socket_timeout = pubsub.connection.socket_timeout if hasattr(pubsub.connection, 'socket_timeout') else 'N/A'
            logger.debug(f"Marked PubSub connection {id(pubsub.connection)} to prevent cleanup, socket_timeout={socket_timeout}")

        logger.debug(f"Created and subscribed to Redis Pub/Sub channel: {self.worker_state_channel}")
        return pubsub

    async def _health_check_loop(self):
        """定期检查 Pub/Sub 连接健康状态"""
        while self._running:
            try:
                await asyncio.sleep(self._health_check_interval)

                if not self._running:
                    break

                if self._pubsub and self._pubsub.connection:
                    try:
                        await asyncio.wait_for(self._pubsub.ping(), timeout=5.0)
                        logger.debug("Pub/Sub health check: OK")
                    except Exception as e:
                        logger.warning(f"Pub/Sub health check failed: {e}")
                else:
                    logger.warning("Pub/Sub connection is None")

            except asyncio.CancelledError:
                logger.debug("Health check loop cancelled")
                break
            except Exception as e:
                logger.error(f"Error in health check loop: {e}")

    async def _listen_loop(self):
        """监听循环（支持自动重连）"""
        retry_delay = 1
        max_retry_delay = 30

        while self._running:
            try:
                async for message in self._pubsub.listen():
                    if message['type'] == 'message':
                        try:
                            data = json.loads(message['data'])

                            # 检测到 worker 离线事件时，立即触发一次离线消息恢复
                            if data.get('state') == 'offline':
                                worker_id = data.get('worker_id')
                                if worker_id:
                                    logger.debug(f"[StateManager] Worker {worker_id} offline event received, triggering recovery")
                                    try:
                                        # 直接异步调用恢复处理
                                        # 由于内部使用非阻塞锁，如果锁被占用会快速跳过，不会长时间阻塞
                                        await self._process_offline_workers_once()
                                    except Exception as e:
                                        logger.error(f"[StateManager] Error during offline worker recovery: {e}", exc_info=True)

                            # 调用注册的回调函数
                            for callback in self._callbacks:
                                try:
                                    if asyncio.iscoroutinefunction(callback):
                                        await callback(data)
                                    else:
                                        callback(data)
                                except Exception as e:
                                    logger.error(f"Error in state change callback: {e}")

                        except Exception as e:
                            logger.error(f"Error processing state change message: {e}")

                retry_delay = 1

            except asyncio.CancelledError:
                logger.debug("Listen loop cancelled")
                break
            except Exception as e:
                logger.error(f"Error in listen loop: {e}")

                if not self._running:
                    break

                logger.warning(f"Attempting to reconnect to Redis Pub/Sub in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)

                try:
                    self._pubsub = await self._create_and_subscribe_pubsub()
                    logger.debug(f"Successfully reconnected to Redis Pub/Sub")
                    retry_delay = 1
                except Exception as reconnect_error:
                    logger.error(f"Failed to reconnect to Redis Pub/Sub: {reconnect_error}")
                    retry_delay = min(retry_delay * 2, max_retry_delay)

        logger.debug("Listen loop exited")

    def register_callback(self, callback: Callable):
        """注册状态变更回调"""
        self._callbacks.add(callback)
        logger.debug(f"Registered state change callback: {callback.__name__}")

    def unregister_callback(self, callback: Callable):
        """注销状态变更回调"""
        self._callbacks.discard(callback)
        logger.debug(f"Unregistered state change callback: {callback.__name__}")

    # ========================================================================
    # Worker 扫描和超时检测（从 WorkerScanner 合并）
    # ========================================================================

    async def scan_timeout_workers(self) -> List[Dict]:
        """快速扫描超时的 worker - O(log N) 复杂度

        每个 worker 使用自己存储的 heartbeat_timeout 值进行超时判断。
        这个值由 HeartbeatManager 在 worker 初始化时设置。

        Returns:
            超时的 worker 列表
        """
        self._scan_counter += 1
        if self._scan_counter >= self._partial_check_interval:
            self._scan_counter = 0
            asyncio.create_task(self._partial_check())

        current_time = time.time()

        potential_timeout_worker_ids = await self.async_redis.zrangebyscore(
            self.active_workers_key,
            min=0,
            max=current_time - 1
        )

        if not potential_timeout_worker_ids:
            return []

        # 直接使用自身的方法获取 worker 信息
        all_workers_info = await self.get_all_workers_info(only_alive=False)
        workers_data = [all_workers_info.get(wid) for wid in potential_timeout_worker_ids]

        result = []
        cleanup_pipeline = self.async_redis.pipeline()
        need_cleanup = False

        for worker_id, worker_data in zip(potential_timeout_worker_ids, workers_data):
            if not worker_data:
                cleanup_pipeline.zrem(self.active_workers_key, worker_id)
                cleanup_pipeline.srem(self.workers_registry_key, worker_id)
                need_cleanup = True
                continue

            # 使用 worker 自己存储的 heartbeat_timeout
            # 这个值在 HeartbeatManager 初始化 worker 时设置
            worker_heartbeat_timeout = float(worker_data.get('heartbeat_timeout', 15.0))
            last_heartbeat = float(worker_data.get('last_heartbeat', 0))
            worker_cutoff_time = current_time - worker_heartbeat_timeout

            if last_heartbeat >= worker_cutoff_time:
                cleanup_pipeline.zadd(self.active_workers_key, {worker_id: last_heartbeat})
                need_cleanup = True
                continue

            is_alive = worker_data.get('is_alive', 'true') == 'true'
            if not is_alive:
                cleanup_pipeline.zrem(self.active_workers_key, worker_id)
                need_cleanup = True
                continue

            logger.debug(f"Worker {worker_id} timeout: last_heartbeat={last_heartbeat}, timeout={worker_heartbeat_timeout}s")
            worker_key = f"{self.redis_prefix}:{self.worker_prefix}:{worker_id}"
            result.append({
                'worker_key': worker_key,
                'worker_data': worker_data,
                'worker_id': worker_id
            })

        if need_cleanup:
            await cleanup_pipeline.execute()

        if result:
            logger.debug(f"Found {len(result)} timeout workers")

        return result

    async def update_heartbeat(self, worker_id: str, heartbeat_time: Optional[float] = None):
        """原子性更新心跳"""
        if heartbeat_time is None:
            heartbeat_time = time.time()

        pipeline = self.async_redis.pipeline()
        worker_key = f"{self.redis_prefix}:{self.worker_prefix}:{worker_id}"

        pipeline.hset(worker_key, 'last_heartbeat', str(heartbeat_time))
        pipeline.zadd(self.active_workers_key, {worker_id: heartbeat_time})

        await pipeline.execute()

    async def add_worker(self, worker_id: str, worker_data: Dict):
        """添加新 worker"""
        heartbeat_time = float(worker_data.get('last_heartbeat', time.time()))

        pipeline = self.async_redis.pipeline()
        worker_key = f"{self.redis_prefix}:{self.worker_prefix}:{worker_id}"

        pipeline.hset(worker_key, mapping=worker_data)
        pipeline.zadd(self.active_workers_key, {worker_id: heartbeat_time})

        await pipeline.execute()
        logger.debug(f"Added worker {worker_id} to system")

    async def remove_worker(self, worker_id: str):
        """移除 worker（标记为离线并从活跃集合中移除）"""
        await self.set_worker_offline(worker_id, reason="heartbeat_timeout")
        await self.async_redis.zrem(self.active_workers_key, worker_id)

    async def cleanup_stale_workers(self, max_age_seconds: float = 3600):
        """清理过期的 worker 记录"""
        current_time = time.time()
        cutoff_time = current_time - max_age_seconds

        stale_worker_ids = await self.async_redis.zrangebyscore(
            self.active_workers_key,
            min=0,
            max=cutoff_time
        )

        if not stale_worker_ids:
            return 0

        pipeline = self.async_redis.pipeline()

        for worker_id in stale_worker_ids:
            worker_key = f"{self.redis_prefix}:{self.worker_prefix}:{worker_id}"
            pipeline.delete(worker_key)

        pipeline.zrem(self.active_workers_key, *stale_worker_ids)

        await pipeline.execute()

        logger.debug(f"Cleaned up {len(stale_worker_ids)} stale worker records")
        return len(stale_worker_ids)

    async def _partial_check(self):
        """部分一致性检查"""
        try:
            sample_size = min(10, await self.async_redis.zcard(self.active_workers_key))
            if sample_size == 0:
                return

            random_workers = await self.async_redis.zrandmember(
                self.active_workers_key, sample_size, withscores=True
            )

            # zrandmember withscores=True 返回的是扁平列表: [member1, score1, member2, score2, ...]
            # 需要将其转换为 [(member1, score1), (member2, score2), ...] 格式
            if random_workers:
                # 将扁平列表转换为元组对
                worker_pairs = [(random_workers[i], random_workers[i+1]) for i in range(0, len(random_workers), 2)]
            else:
                worker_pairs = []

            for worker_id, zset_score in worker_pairs:
                worker_key = f"{self.redis_prefix}:{self.worker_prefix}:{worker_id}"
                hash_heartbeat = await self.async_redis.hget(worker_key, 'last_heartbeat')

                if not hash_heartbeat:
                    await self.async_redis.zrem(self.active_workers_key, worker_id)
                    logger.debug(f"Partial check: removed {worker_id}")
                else:
                    hash_time = float(hash_heartbeat)
                    # zset_score 可能是字符串，需要转换为 float
                    zset_score_float = float(zset_score)
                    if abs(hash_time - zset_score_float) > 1.0:
                        await self.async_redis.zadd(self.active_workers_key, {worker_id: hash_time})
                        logger.debug(f"Partial check: synced {worker_id}")

        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.error(f"Partial check error: {e}", exc_info=True)

    async def get_active_count(self) -> int:
        """获取活跃 worker 数量 - O(1)"""
        return await self.async_redis.zcard(self.active_workers_key)

    # ========================================================================
    # 离线 Worker 恢复功能（从 OfflineWorkerRecovery 合并）
    # ========================================================================

    async def start_recovery(self, recovery_interval: float = 30.0):
        """
        启动循环恢复检测

        定期调用 _process_offline_workers_once 处理离线 workers

        Args:
            recovery_interval: 恢复检测间隔（秒）
        """
        logger.debug(f"[Recovery] Starting offline worker recovery loop (interval={recovery_interval}s)")
        self._stop_recovery = False

        while not self._stop_recovery:
            try:
                # 执行一次离线 worker 处理
                await self._process_offline_workers_once()

                # 等待下次检测
                await asyncio.sleep(recovery_interval)

            except asyncio.CancelledError:
                logger.debug("[Recovery] Recovery loop cancelled")
                break
            except Exception as e:
                logger.error(f"[Recovery Loop] Unexpected error: {e}")
                await asyncio.sleep(recovery_interval)

        logger.debug("[Recovery] Offline worker recovery loop stopped")

    async def start(self, recovery_interval: float = 30.0):
        """
        启动恢复处理（兼容 OfflineWorkerRecovery 接口）

        这是 start_recovery() 的别名，用于兼容 EventPool 的接口

        Args:
            recovery_interval: 恢复检测间隔（秒）
        """
        await self.start_recovery(recovery_interval)

    async def _process_offline_workers_once(self):
        """
        处理一次离线 workers

        遍历所有离线 workers，解析其 group_info，为相关任务转移消息
        """
        from redis.asyncio.lock import Lock as AsyncLock

        # 使用异步生成器遍历所有离线 workers
        # 好处：拿到一个 worker 就立即处理，而不是等待所有 worker 都查询完
        async for worker_key, worker_data in self.find_all_offline_workers():
            
            if self._stop_recovery:
                break

            # 提取 worker_id
            worker_id = worker_key.split(':')[-1]

            # 使用分布式锁防止多个进程同时处理同一个 worker
            lock_key = f"{self.redis_prefix}:RECOVERY:WORKER_LOCK:{worker_id}"
            worker_lock = AsyncLock(
                self.async_redis,
                lock_key,
                timeout=300,  # 5分钟超时（处理一个 worker 可能需要较长时间）
                blocking=False  # 非阻塞，获取不到锁就跳过
            )

            # 尝试获取锁
            if not await worker_lock.acquire():
                logger.debug(
                    f"[Recovery] Worker {worker_id} is being processed by another worker, skipping"
                )
                continue

            try:
                logger.debug(f"[Recovery] Processing worker={worker_id}")

                # 跟踪该 worker 的 group_info 处理状态
                group_info_results = {}  # {group_info_key: bool}

                # 遍历 worker_data，查找 group_info 开头的 key
                for key, value in worker_data.items():
                    if not key.startswith('group_info:'):
                        continue

                    try:
                        # 解析 group_info 数据
                        group_info = json.loads(value)
                        task_name = group_info.get('task_name')

                        # 检查是否已经标记为转移成功
                        already_transferred = group_info.get('messages_transferred', 'false')
                        if already_transferred == 'true':
                            logger.debug(
                                f"[Recovery] Group_info already transferred: worker={worker_id}, "
                                f"task={task_name}, skipping"
                            )
                            group_info_results[key] = True
                            continue

                        # 检查 task_name 是否在我们维护的 self.tasks 中
                        if task_name not in self.tasks:
                            logger.debug(f"[Recovery] Task {task_name} not in managed tasks, skipping {self.tasks=}")
                            group_info_results[key] = True  # 标记为已处理（跳过）
                            continue

                        # 获取该任务的 event_queue
                        task_event_queue = self.task_event_queues.get(task_name)
                        if not task_event_queue:
                            logger.warning(f"[Recovery] No event queue for task {task_name}, skipping")
                            group_info_results[key] = False  # 标记为失败
                            continue

                        # 提取 group_info 中的信息
                        queue_name = group_info.get('queue')  # 如 "robust_bench2:8"
                        group_name = group_info.get('group_name')
                        offline_consumer_name = group_info.get('consumer_name')
                        stream_key_suffix = group_info.get('stream_key')  # 如 "test5:QUEUE:robust_bench2:8"

                        if not all([queue_name, group_name, offline_consumer_name]):
                            logger.warning(f"[Recovery] Incomplete group_info: {group_info}")
                            group_info_results[key] = False  # 标记为失败
                            continue

                        # 构建完整的 stream_key
                        stream_key = stream_key_suffix

                        logger.debug(
                            f"[Recovery] Processing worker={worker_id}, task={task_name}, "
                            f"queue={queue_name}, group={group_name}"
                        )

                        # 转移消息
                        success = await self._transfer_messages(
                            stream_key=stream_key,
                            group_name=group_name,
                            offline_consumer_name=offline_consumer_name,
                            task_name=task_name,
                            queue_name=queue_name,
                            task_event_queue=task_event_queue,
                            worker_id=worker_id,
                            worker_data=worker_data,
                            group_info_key=key
                        )

                        group_info_results[key] = success

                        if success:
                            logger.debug(
                                f"[Recovery] Successfully transferred messages for "
                                f"worker={worker_id}, task={task_name}, queue={queue_name}"
                            )
                        else:
                            logger.warning(
                                f"[Recovery] Failed to transfer messages for "
                                f"worker={worker_id}, task={task_name}, queue={queue_name}"
                            )

                    except json.JSONDecodeError as e:
                        logger.error(f"[Recovery] Failed to parse group_info: {e}")
                        group_info_results[key] = False
                    except Exception as e:
                        logger.error(f"[Recovery] Error processing group_info: {e}")
                        group_info_results[key] = False

                # 处理完该 worker 的所有 group_info 后，检查是否都成功
                # 重要: 必须从 Redis 重新读取最新的 worker 数据，以确保检查所有 group_info 的状态
                # 因为 worker_data 是快照，可能不包含最新的 messages_transferred 标记
                logger.debug(f"[Recovery] Checking all group_info statuses for worker={worker_id}")

                # 从 Redis 重新读取最新的 worker 数据
                fresh_worker_data = await self.get_worker_info(worker_id)
                if not fresh_worker_data:
                    logger.warning(f"[Recovery] Worker {worker_id} not found in Redis, skipping final check")
                    continue

                # 检查该 worker 的所有 group_info 的 messages_transferred 状态
                all_group_infos_transferred = True
                group_info_count = 0
                transferred_count = 0

                for key, value in fresh_worker_data.items():
                    if not key.startswith('group_info:'):
                        continue

                    group_info_count += 1
                    try:
                        group_info = json.loads(value)
                        is_transferred = group_info.get('messages_transferred', 'false')

                        if is_transferred == 'true':
                            transferred_count += 1
                            logger.debug(
                                f"[Recovery] Group_info {key} already transferred for worker={worker_id}"
                            )
                        else:
                            all_group_infos_transferred = False
                            logger.warning(
                                f"[Recovery] Group_info {key} NOT yet transferred for worker={worker_id}, "
                                f"cannot mark worker-level messages_transferred=true"
                            )
                    except json.JSONDecodeError as e:
                        logger.error(f"[Recovery] Failed to parse group_info {key}: {e}")
                        all_group_infos_transferred = False

                logger.debug(
                    f"[Recovery] Worker {worker_id} has {group_info_count} group_infos, "
                    f"{transferred_count} transferred"
                )

                # 标记 worker 级别的 messages_transferred = true 的条件：
                # 1. 没有 group_info（group_info_count == 0）- 没有消息需要转移
                # 2. 有 group_info 且全部已转移（group_info_count > 0 and all_group_infos_transferred）
                if group_info_count == 0:
                    # 没有 group_info，说明该 worker 没有消费任何队列，直接标记为已转移
                    await self.async_redis.hset(
                        worker_key,
                        'messages_transferred',
                        'true'
                    )
                    logger.info(
                        f"[Recovery] Worker {worker_id} has no group_infos, "
                        f"marked worker-level messages_transferred=true"
                    )
                elif all_group_infos_transferred:
                    # 所有 group_info 都已转移
                    await self.async_redis.hset(
                        worker_key,
                        'messages_transferred',
                        'true'
                    )
                    logger.info(
                        f"[Recovery] All {group_info_count} group_infos transferred successfully for worker={worker_id}, "
                        f"marked worker-level messages_transferred=true"
                    )
                else:
                    # 有 group_info 但未全部转移
                    logger.warning(
                        f"[Recovery] Not all group_infos transferred for worker={worker_id} "
                        f"({transferred_count}/{group_info_count}), will retry in next cycle"
                    )

            except Exception as e:
                logger.error(f"[Recovery] Error processing worker {worker_key}: {e}")
            finally:
                # 释放锁
                await worker_lock.release()
                logger.debug(f"[Recovery] Released lock for worker={worker_id}")

    async def _transfer_messages(
        self,
        stream_key: str,
        group_name: str,
        offline_consumer_name: str,
        task_name: str,
        queue_name: str,
        task_event_queue: asyncio.Queue,
        worker_id: str,
        worker_data: dict,
        group_info_key: str
    ) -> bool:
        """
        转移离线 worker 的消息到当前 worker 的 event_queue

        Args:
            stream_key: Stream 键（如 "test5:QUEUE:robust_bench2:8"）
            group_name: 消费者组名称
            offline_consumer_name: 离线消费者名称
            task_name: 任务名称
            queue_name: 队列名称（如 "robust_bench2:8"）
            task_event_queue: 任务事件队列
            worker_id: 离线 worker ID
            worker_data: 离线 worker 数据
            group_info_key: group_info 的 Redis key（如 "group_info:test5:QUEUE:robust_bench2:benchmark_task"）

        Returns:
            是否成功转移（True=成功，False=失败）
        """

        total_transferred = 0

        try:
            # 检查是否已经转移过消息
            messages_transferred = worker_data.get('messages_transferred', 'false')
            if isinstance(messages_transferred, bytes):
                messages_transferred = messages_transferred.decode('utf-8')

            if messages_transferred.lower() == 'true':
                logger.debug(f"[Recovery] Messages already transferred for worker={worker_id}")
                return False

            try:
                # 批量处理 pending 消息
                batch_size = 100

                while True:
                    # 获取 pending 消息
                    detailed_pending = await self.async_redis.xpending_range(
                        stream_key,
                        group_name,
                        min='-',
                        max='+',
                        count=batch_size,
                        consumername=offline_consumer_name
                    )

                    if not detailed_pending:
                        logger.debug(
                            f"[Recovery] No pending messages for worker={worker_id}, "
                            f"task={task_name}, queue={queue_name}"
                        )
                        break

                    logger.debug(
                        f"[Recovery] Found {len(detailed_pending)} pending messages for "
                        f"worker={worker_id}, task={task_name}, queue={queue_name}"
                    )

                    # 提取消息 ID
                    message_ids = [msg['message_id'] for msg in detailed_pending]

                    # 使用 XCLAIM 转移消息到当前 worker
                    claimed_messages = await self.async_redis.xclaim(
                        stream_key,
                        group_name,
                        self.worker_id,  # 当前 worker ID
                        min_idle_time=0,
                        message_ids=message_ids
                    )

                    if not claimed_messages:
                        logger.warning(
                            f"[Recovery] Failed to claim messages for worker={worker_id}, "
                            f"task={task_name}, queue={queue_name}"
                        )
                        break

                    logger.debug(
                        f"[Recovery] Claimed {len(claimed_messages)} messages for "
                        f"worker={worker_id}, task={task_name}, queue={queue_name}"
                    )

                    # 将消息放入 task_event_queue
                    for msg_id, msg_data in claimed_messages:
                        try:
                            if isinstance(msg_id, bytes):
                                msg_id = msg_id.decode('utf-8')

                            # 解析消息数据
                            data_field = msg_data.get(b'data') or msg_data.get('data')
                            if not data_field:
                                logger.warning(f"[Recovery] No data field in message {msg_id}")
                                continue

                            parsed_data = msgpack.unpackb(data_field, raw=False)

                            # 添加元数据
                            parsed_data['_task_name'] = task_name
                            parsed_data['queue'] = queue_name

                            # 构建任务项
                            task_item = {
                                'queue': queue_name,
                                'event_id': msg_id,
                                'event_data': parsed_data,
                                'consumer': self.worker_id,
                                'group_name': group_name
                            }

                            # 放入队列
                            await task_event_queue.put(task_item)
                            total_transferred += 1

                            logger.debug(
                                f"[Recovery] Put message {msg_id} into event_queue for task={task_name}"
                            )

                        except Exception as e:
                            logger.error(f"[Recovery] Error processing message {msg_id}: {e}")

            except Exception as e:
                # 即使处理消息时出错，也要标记为已转移，避免重复处理
                logger.error(
                    f"[Recovery] Error during message recovery for worker={worker_id}, "
                    f"task={task_name}, queue={queue_name}: {e}, will still mark as transferred"
                )

            # 无论是否有消息、是否出错，都标记该 group_info 的消息已转移
            # 这样可以避免重复处理，即使没有消息也表示已经检查过了

            # 从 Redis 重新读取最新的 group_info（而不是使用快照）
            group_info_value = await self.async_redis.hget(
                self._get_worker_key(worker_id),
                group_info_key
            )

            if group_info_value:
                # 处理 bytes 类型
                if isinstance(group_info_value, bytes):
                    group_info_value = group_info_value.decode('utf-8')

                # 解析并添加转移状态
                group_info = json.loads(group_info_value)
                group_info['messages_transferred'] = 'true'

                # 使用 update_worker_field 方法写回 Redis
                await self.update_worker_field(
                    worker_id,
                    group_info_key,
                    json.dumps(group_info)
                )
                logger.debug(
                    f"[Recovery] Marked group_info transferred: worker={worker_id}, "
                    f"task={task_name}, queue={queue_name}, key={group_info_key}, transferred={total_transferred} messages"
                )
            else:
                logger.warning(
                    f"[Recovery] group_info not found in Redis for key={group_info_key}, "
                    f"worker={worker_id}, cannot mark as transferred"
                )

          

            return True  # 成功转移

        except Exception as e:
            logger.error(
                f"[Recovery] Error transferring messages for worker={worker_id}, "
                f"task={task_name}, queue={queue_name}: {e}"
            )
            return False  # 转移失败

    def stop_recovery(self):
        """停止恢复处理"""
        self._stop_recovery = True

    # ========================================================================
    # 离线 Worker 清理功能（定时清理已转移消息的离线 Worker）
    # ========================================================================

    async def start_cleanup_task(self, cleanup_interval: float = 86400.0):
        """
        启动定时清理任务，每天执行一次

        清理条件：
        1. Worker 已离线（is_alive=false）
        2. 消息已转移（messages_transferred=true）
        3. 离线时间超过 1 天（offline_time > 1 day）

        Args:
            cleanup_interval: 清理间隔（秒），默认 86400 秒 = 24 小时
        """
        logger.info(f"[Cleanup] Starting offline worker cleanup task (interval={cleanup_interval}s)")
        self._stop_cleanup = False

        while not self._stop_cleanup:
            try:
                # 执行一次清理
                await self._cleanup_offline_workers_once()

                # 等待下次清理
                await asyncio.sleep(cleanup_interval)

            except asyncio.CancelledError:
                logger.info("[Cleanup] Cleanup task cancelled")
                break
            except Exception as e:
                logger.error(f"[Cleanup] Unexpected error: {e}", exc_info=True)
                await asyncio.sleep(cleanup_interval)

        logger.info("[Cleanup] Offline worker cleanup task stopped")

    async def _cleanup_offline_workers_once(self):
        """
        执行一次离线 Worker 清理

        清理满足以下条件的 worker：
        1. is_alive = false
        2. messages_transferred = true
        3. offline_time > 1 day
        """
        from redis.asyncio.lock import Lock as AsyncLock

        current_time = time.time()
        one_day_ago = current_time - 86400  # 24 小时前
        cleanup_count = 0

        try:
            # 获取所有已注册的 worker
            all_worker_ids = await self.get_all_workers()
            logger.info(f"[Cleanup] Scanning {len(all_worker_ids)} workers for cleanup")

            for worker_id in all_worker_ids:
                if self._stop_cleanup:
                    break

                # 解码 worker_id
                if isinstance(worker_id, bytes):
                    worker_id = worker_id.decode('utf-8')

                # 使用分布式锁防止并发清理同一个 worker
                lock_key = f"{self.redis_prefix}:CLEANUP:WORKER_LOCK:{worker_id}"
                worker_lock = AsyncLock(
                    self.async_redis,
                    lock_key,
                    timeout=60,  # 1分钟超时
                    blocking=False  # 非阻塞
                )

                # 尝试获取锁
                if not await worker_lock.acquire():
                    logger.debug(f"[Cleanup] Worker {worker_id} is being processed by another worker, skipping")
                    continue

                try:
                    # 获取 worker 信息
                    worker_info = await self.get_worker_info(worker_id)

                    if not worker_info:
                        # 数据不一致：注册表中有记录，但 worker hash 不存在
                        # 清理注册表中的脏数据
                        logger.warning(
                            f"[Cleanup] Worker {worker_id} in registry but hash not found, "
                            f"cleaning up inconsistent data"
                        )
                        await self.delete_worker(worker_id)
                        cleanup_count += 1
                        continue

                    # 检查清理条件
                    is_alive = worker_info.get('is_alive', 'false')
                    messages_transferred = worker_info.get('messages_transferred', 'false')
                    offline_time_str = worker_info.get('offline_time', '0')

                    # 转换类型
                    is_alive_bool = (is_alive == 'true')
                    messages_transferred_bool = (messages_transferred == 'true')

                    try:
                        offline_time = float(offline_time_str)
                    except (ValueError, TypeError):
                        offline_time = 0

                    # 判断是否需要清理
                    should_cleanup = (
                        not is_alive_bool  # 已离线
                        and messages_transferred_bool  # 消息已转移
                        and offline_time > 0  # 有离线时间
                        and offline_time < one_day_ago  # 离线超过 1 天
                    )

                    if should_cleanup:
                        # 计算离线时长
                        offline_duration = current_time - offline_time
                        offline_hours = offline_duration / 3600

                        logger.info(
                            f"[Cleanup] Cleaning up worker {worker_id}: "
                            f"offline for {offline_hours:.1f} hours, "
                            f"messages_transferred={messages_transferred}"
                        )

                        # 删除 worker 记录（同时从注册表注销，使用 pipeline 保证原子性）
                        await self.delete_worker(worker_id)

                        cleanup_count += 1
                        logger.info(f"[Cleanup] Successfully cleaned up worker {worker_id}")

                    else:
                        # 记录为什么不清理（调试用）
                        if is_alive_bool:
                            reason = "still alive"
                        elif not messages_transferred_bool:
                            reason = "messages not transferred"
                        elif offline_time == 0:
                            reason = "no offline_time"
                        elif offline_time >= one_day_ago:
                            offline_duration = current_time - offline_time
                            offline_hours = offline_duration / 3600
                            reason = f"offline for only {offline_hours:.1f} hours (< 24h)"
                        else:
                            reason = "unknown"

                        logger.debug(
                            f"[Cleanup] Worker {worker_id} not eligible for cleanup: {reason}"
                        )

                except Exception as e:
                    logger.error(f"[Cleanup] Error processing worker {worker_id}: {e}", exc_info=True)
                finally:
                    # 释放锁
                    await worker_lock.release()

            if cleanup_count > 0:
                logger.info(f"[Cleanup] Cleaned up {cleanup_count} offline workers")
            else:
                logger.info("[Cleanup] No workers eligible for cleanup")

        except Exception as e:
            logger.error(f"[Cleanup] Error during cleanup: {e}", exc_info=True)

    def stop_cleanup(self):
        """停止清理任务"""
        self._stop_cleanup = True


__all__ = [
    'WorkerManager',
    'HeartbeatManager',
]
