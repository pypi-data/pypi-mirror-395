"""
EventPool - 事件池核心实现

负责：
1. 任务队列管理和消息分发
2. 消费者管理和生命周期控制
3. 优先级队列处理
4. 离线Worker恢复机制

核心组件集成：
- MessageSender/Reader: 消息发送和读取（通过container）
- QueueRegistry: 队列注册管理
- Worker ID: 直接使用 app.worker_id（在 App._start 中生成）
"""

from ..utils.serializer import dumps_str, loads_str
import time
import threading
import logging
import asyncio
import json
from collections import defaultdict, deque, Counter
from typing import List, Optional, TYPE_CHECKING, Union
import traceback
import redis
from redis import asyncio as aioredis

from jettask.db.connector import get_sync_redis_client, get_async_redis_client

from ..utils.helpers import get_hostname
import os
from jettask.config.lua_scripts import LUA_SCRIPT_BATCH_SEND_EVENT

if TYPE_CHECKING:
    from ..core.task import Task
    from ..core.app import Jettask

logger = logging.getLogger('app')

# Lua脚本：原子地更新Redis hash中的最大值
UPDATE_MAX_OFFSET_LUA = """
local hash_key = KEYS[1]
local field = KEYS[2] 
local new_value = tonumber(ARGV[1])

local current = redis.call('HGET', hash_key, field)
if current == false or tonumber(current) < new_value then
    redis.call('HSET', hash_key, field, new_value)
    return 1
else
    return 0
end
"""

class EventPool(object):
    STATE_MACHINE_NAME = "STATE_MACHINE"
    TIMEOUT = 60 * 5

    def __init__(
        self,
        redis_client: redis.StrictRedis,
        async_redis_client: Optional[aioredis.StrictRedis] = None,
        task_event_queues=None,
        tasks: dict = None,
        queue_registry=None,  # 必需参数
        offline_recovery=None,  # 必需参数
        queues: list = None,
        redis_url: str = None,
        consumer_config: dict = None,
        redis_prefix: str = None,
        app: Optional["Jettask"] = None,
        worker_id: str = None,
    ) -> None:
        self.redis_client = redis_client

        # 懒加载：延迟创建所有异步客户端，避免在子线程中创建
        self._async_redis_client = async_redis_client  # 保存传入的（如果有）
        self._binary_redis_client = None
        self._async_binary_redis_client = None

        self._redis_url = redis_url or 'redis://localhost:6379/0'
        self.redis_prefix = redis_prefix or 'jettask'
        self.app = app  # 保存app引用
        self.worker_id = worker_id  # 保存 worker_id
        self.task_event_queues = task_event_queues  # 保存 task_event_queues

        self.tasks = tasks
        # ✅ 在初始化阶段分离通配符模式和静态队列
        # self.queues 始终只存储静态队列（或动态发现的队列）
        # self.wildcard_patterns 存储通配符模式，用于动态队列发现
        from jettask.utils.queue_matcher import separate_wildcard_and_static_queues

        self.wildcard_patterns, static_queues = separate_wildcard_and_static_queues(queues or [])
        self.queues = static_queues  # self.queues 只包含静态队列
        self.wildcard_mode = len(self.wildcard_patterns) > 0  # 是否启用通配符模式
        
        # 保存consumer_config供后续使用
        self.consumer_config = consumer_config or {}
        self.consumer_config['queues'] = queues or []
        self.consumer_config['redis_prefix'] = redis_prefix or 'jettask'
        self.consumer_config['redis_url'] = redis_url or 'redis://localhost:6379/0'

        # queue_registry 和 offline_recovery 是必需参数，直接使用
        self.queue_registry = queue_registry
        self.offline_recovery = offline_recovery

        # 创建带前缀的队列名称映射
        self.prefixed_queues = {}

        # 优先级队列管理（简化：直接从Redis读取，不再使用缓存）

        # 用于跟踪广播消息
        self._broadcast_message_tracker = {}

        self.solo_routing_tasks = {}
        self.solo_running_state = {}
        self.solo_urgent_retry = {}
        self.batch_routing_tasks = {}
        self.task_scheduler = {}
        self.running_task_state_mappings = {}
        self.delay_tasks = []
        self.solo_agg_task = {}
        self.rlock = threading.RLock()
        self._claimed_message_ids = set()  # 跟踪已认领的消息ID，防止重复处理
        self._stop_reading = False  # 用于控制停止读取的标志
        self._queue_stop_flags = {queue: False for queue in (queues or [])}  # 每个队列的停止标志 


    async def record_group_info_async(self, queue: str, task_name: str, group_name: str, consumer_name: str):
        """异步记录task的group信息到worker hash表

        注意：此方法委托给 WorkerManager.record_group_info 处理
        """
        if not self.worker_id:
            logger.warning("Cannot record group info: worker_id not initialized")
            return
        # logger.debug(f'记录优先级 {queue=} {task_name=} {group_name=} {consumer_name=}')
        try:
            # 委托给 WorkerManager 处理
            if self.app and hasattr(self.app, 'worker_state'):
                await self.app.worker_state.record_group_info(
                    worker_id=self.worker_id,
                    queue=queue,
                    task_name=task_name,
                    group_name=group_name,
                    consumer_name=consumer_name,
                    redis_prefix=self.redis_prefix
                )
            else:
                logger.warning("Cannot record group info: worker_state not available")

        except Exception as e:
            logger.error(f"Error recording task group info: {e}", exc_info=True)

    def _put_task(self, event_queue: Union[deque, asyncio.Queue], task, urgent: bool = False):
        """统一的任务放入方法"""
        # 如果是deque，使用原有逻辑
        if isinstance(event_queue, deque):
            if urgent:
                event_queue.appendleft(task)
            else:
                event_queue.append(task)
        # 如果是asyncio.Queue，则暂时只能按顺序放入（Queue不支持优先级）
        elif isinstance(event_queue, asyncio.Queue):
            # 对于asyncio.Queue，我们需要在async上下文中操作
            # 这里先保留接口，具体实现在async方法中
            pass
    
    async def _async_put_task(self, event_queue: asyncio.Queue, task, urgent: bool = False):
        """异步任务放入方法"""
        await event_queue.put(task)

    def init_routing(self):
        for queue in self.queues:
            self.solo_agg_task[queue] = defaultdict(list)
            self.solo_routing_tasks[queue] = defaultdict(list)
            self.solo_running_state[queue]  = defaultdict(bool)
            self.batch_routing_tasks[queue]  = defaultdict(list)
            self.task_scheduler[queue] = defaultdict(int)
            self.running_task_state_mappings[queue] = defaultdict(dict)
            
    def get_prefixed_queue_name(self, queue: str) -> str:
        """为队列名称添加前缀"""
        return f"{self.redis_prefix}:QUEUE:{queue}"

    @property
    def async_redis_client(self):
        """获取异步 Redis 客户端（懒加载）"""
        if self._async_redis_client is None:
            self._async_redis_client = get_async_redis_client(
                self._redis_url, decode_responses=True, socket_timeout=None
            )
        return self._async_redis_client

    @property
    def binary_redis_client(self):
        """获取同步二进制 Redis 客户端（懒加载）"""
        if self._binary_redis_client is None:
            self._binary_redis_client = get_sync_redis_client(
                self._redis_url, decode_responses=False, socket_timeout=None
            )
        return self._binary_redis_client

    @property
    def async_binary_redis_client(self):
        """获取异步二进制 Redis 客户端（懒加载）"""
        if self._async_binary_redis_client is None:
            self._async_binary_redis_client = get_async_redis_client(
                self._redis_url, decode_responses=False, socket_timeout=None
            )
        return self._async_binary_redis_client

    def get_redis_client(self, asyncio: bool = False, binary: bool = False):
        """获取Redis客户端

        Args:
            asyncio: 是否使用异步客户端
            binary: 是否使用二进制客户端（用于Stream操作）
        """
        if binary:
            return self.async_binary_redis_client if asyncio else self.binary_redis_client
        return self.async_redis_client if asyncio else self.redis_client

    def _batch_send_event_sync(self, prefixed_queue, messages: List[dict], pipe):
        """批量发送事件（同步）"""
        # 准备Lua脚本参数
        lua_args = [self.redis_prefix.encode() if isinstance(self.redis_prefix, str) else self.redis_prefix]

        for message in messages:
            # 确保消息格式正确
            if 'data' in message:
                data = message['data'] if isinstance(message['data'], bytes) else dumps_str(message['data'])
            else:
                data = dumps_str(message)
            lua_args.append(data)

        # 获取同步Redis客户端
        client = self.get_redis_client(asyncio=False, binary=True)

        # 执行Lua脚本
        results = client.eval(
            LUA_SCRIPT_BATCH_SEND_EVENT,
            1,  # 1个KEY
            prefixed_queue,  # KEY[1]: stream key
            *lua_args  # ARGV: prefix, data1, data2, ...
        )

        # 解码所有返回的Stream ID
        return [r.decode('utf-8') if isinstance(r, bytes) else r for r in results]

    async def _batch_send_event(self, prefixed_queue, messages: List[dict], pipe):
        """批量发送事件（异步）"""
        # 准备Lua脚本参数
        lua_args = [self.redis_prefix.encode() if isinstance(self.redis_prefix, str) else self.redis_prefix]

        for message in messages:
            # 确保消息格式正确
            if 'data' in message:
                data = message['data'] if isinstance(message['data'], bytes) else dumps_str(message['data'])
            else:
                data = dumps_str(message)
            lua_args.append(data)

        # 获取异步Redis客户端（不使用pipe，直接使用client）
        client = self.get_redis_client(asyncio=True, binary=True)

        # 执行Lua脚本
        results = await client.eval(
            LUA_SCRIPT_BATCH_SEND_EVENT,
            1,  # 1个KEY
            prefixed_queue,  # KEY[1]: stream key
            *lua_args  # ARGV: prefix, data1, data2, ...
        )

        # 解码所有返回的Stream ID
        return [r.decode('utf-8') if isinstance(r, bytes) else r for r in results]
    
    def is_urgent(self, routing_key):
        is_urgent = self.solo_urgent_retry.get(routing_key, False)
        if is_urgent == True:
            del self.solo_urgent_retry[routing_key]
        return is_urgent
    
    async def scan_priority_queues(self, base_queue: str) -> list:
        """扫描Redis中的优先级队列
        
        Args:
            base_queue: 基础队列名（不带优先级后缀）
        
        Returns:
            按优先级排序的队列列表
        """
        pattern = f"{self.redis_prefix}:QUEUE:{base_queue}:*"
        
        try:
            # 使用 QueueRegistry 获取优先级队列，避免 scan
            from jettask.messaging.registry import QueueRegistry
            registry = QueueRegistry(
                redis_client=self.redis_client,
                async_redis_client=self.async_redis_client,
                redis_prefix=self.redis_prefix
            )
            
            # 获取基础队列的所有优先级队列
            priority_queue_names = await registry.get_priority_queues_for_base(base_queue)
            priority_queues = set(priority_queue_names)
            
            # 如果没有优先级队列，检查是否有带优先级后缀的队列
            if not priority_queues:
                all_queues = await registry.get_all_queues()
                for queue in all_queues:
                    if queue.startswith(f"{base_queue}:"):
                        priority_queues.add(queue)
            
            # 添加基础队列（无优先级）
            priority_queues.add(base_queue)
            
            # 按优先级排序（数字越小优先级越高）
            sorted_queues = []
            for q in priority_queues:
                if ':' in q:
                    base, priority = q.rsplit(':', 1)
                    if base == base_queue and priority.isdigit():
                        sorted_queues.append((int(priority), q))
                    else:
                        sorted_queues.append((float('inf'), q))  # 非数字优先级放最后
                else:
                    sorted_queues.append((float('inf'), q))  # 无优先级放最后
            
            sorted_queues.sort(key=lambda x: x[0])
            return [q[1] for q in sorted_queues]
            
        except Exception as e:
            import traceback
            logger.error(f"Error scanning priority queues for {base_queue}: {e}\n{traceback.format_exc()}")
            return [base_queue]  # 返回基础队列作为fallback
    
    async def _ensure_consumer_group_and_record_info(
        self,
        prefixed_queue: str,
        task_name: str,
        consumer_name: str,
        base_group_name: str
    ) -> str:
        """统一的方法：创建 consumer group 并记录 group_info

        Args:
            prefixed_queue: 带前缀的队列名（如 "test5:QUEUE:robust_bench2:6"）
            task_name: 任务名
            consumer_name: consumer 名称（必传）
            base_group_name: 基础队列的 group_name（必传）

        Returns:
            str: 使用的 group_name
        """
        # 提取实际队列名（去除前缀）
        actual_queue_name = prefixed_queue.replace(f"{self.redis_prefix}:QUEUE:", "")

        # 所有队列（包括优先级队列）都使用基础队列的 group_name
        group_name = base_group_name

        # 创建 consumer group
        try:
            await self.async_redis_client.xgroup_create(
                name=prefixed_queue,
                groupname=group_name,
                id="0",
                mkstream=True
            )
            logger.debug(f"Created consumer group {group_name} for queue {prefixed_queue}")
        except Exception as e:
            if "BUSYGROUP" in str(e):
                logger.debug(f"Consumer group {group_name} already exists for queue {prefixed_queue}")
            else:
                logger.warning(f"Error creating consumer group {group_name} for {prefixed_queue}: {e}")

        # 每个队列都记录自己的 group_info（包括优先级队列）
        # 优先级队列使用完整的队列名（包含优先级后缀）
        await self.record_group_info_async(
            actual_queue_name, task_name, group_name, consumer_name
        )

        return group_name

    async def get_priority_queues_direct(self, base_queue: str) -> list:
        """直接从Redis获取所有队列列表（包括基础队列和优先级队列）

        Args:
            base_queue: 基础队列名

        Returns:
            所有队列列表（已加上前缀），基础队列在第一个位置，其余按优先级排序
        """
        # 直接从注册表获取优先级队列
        from jettask.messaging.registry import QueueRegistry
        registry = QueueRegistry(self.redis_client, self.async_redis_client, self.redis_prefix)

        # 获取基础队列的所有优先级队列（包括基础队列自己）
        priority_queue_names = await registry.get_priority_queues_for_base(base_queue)
        priority_queues = []

        # 添加所有优先级队列（带数字后缀的）
        for pq_name in priority_queue_names:
            # 只添加优先级队列（带数字后缀的）
            if ':' in pq_name and pq_name.rsplit(':', 1)[1].isdigit():
                # 构建完整的队列名
                prefixed_pq = f"{self.redis_prefix}:QUEUE:{pq_name}"
                priority = int(pq_name.rsplit(':', 1)[1])
                priority_queues.append((priority, prefixed_pq))

        # 按优先级排序（数字越小优先级越高）
        priority_queues.sort(key=lambda x: x[0])

        # 基础队列放在第一个位置，其余按优先级排序
        base_prefixed = f"{self.redis_prefix}:QUEUE:{base_queue}"
        return [base_prefixed] + [q[1] for q in priority_queues]
  
    
    @classmethod
    def separate_by_key(cls, lst):
        groups = {}
        for item in lst:
            key = item[0]['routing_key']
            if key not in groups:
                groups[key] = []
            groups[key].append(item)
        result = []
        group_values = list(groups.values())
        while True:
            exists_data = False
            for values in group_values:
                try:
                    result.append(values.pop(0))
                    exists_data = True
                except:
                    pass
            if not exists_data:
                break
        return result
    
    async def _unified_task_checker(self, event_queue: asyncio.Queue, checker_type: str = 'solo_agg'):
        """统一的任务检查器，减少代码重复"""
        last_solo_running_state = defaultdict(dict)
        last_wait_time = defaultdict(int)
        queue_batch_tasks = defaultdict(list)
        left_queue_batch_tasks = defaultdict(list)
        
        # 延迟任务专用状态
        delay_tasks = getattr(self, 'delay_tasks', []) if checker_type == 'delay' else []
        
        while True:
            has_work = False
            current_time = time.time()
            
            if checker_type == 'delay':
                # 延迟任务逻辑
                put_count = 0
                need_del_index = []
                for i in range(len(delay_tasks)):
                    schedule_time = delay_tasks[i][0]
                    task = delay_tasks[i][1]
                    if schedule_time <= current_time:
                        try:
                            await self._async_put_task(event_queue, task)
                            need_del_index.append(i)
                            put_count += 1
                            has_work = True
                        except IndexError:
                            pass
                for i in need_del_index:
                    del delay_tasks[i]
                    
            elif checker_type == 'solo_agg':
                # Solo聚合任务逻辑
                for queue in self.queues:
                    for agg_key, tasks in self.solo_agg_task[queue].items():
                        if not tasks:
                            continue
                            
                        has_work = True
                        need_del_index = []
                        need_lock_routing_keys = []
                        sort_by_tasks = self.separate_by_key(tasks)
                        max_wait_time = 5
                        max_records = 3
                        
                        for index, (routing, task) in enumerate(sort_by_tasks):
                            routing_key = routing['routing_key']
                            max_records = routing.get('max_records', 1)
                            max_wait_time = routing.get('max_wait_time', 0)
                            
                            with self.rlock:
                                if self.solo_running_state[queue].get(routing_key, 0) > 0:
                                    continue
                                    
                            if len(queue_batch_tasks[queue] + left_queue_batch_tasks[queue]) >= max_records:
                                break 
                                
                            task["routing"] = routing

                            if self.is_urgent(routing_key):
                                left_queue_batch_tasks[queue].append(task)
                            else:
                                queue_batch_tasks[queue].append(task)
                            need_lock_routing_keys.append(routing_key)
                            need_del_index.append(index)

                        for routing_key, count in Counter(need_lock_routing_keys).items():
                            with self.rlock:
                                self.solo_running_state[queue][routing_key] = count
                                
                        if last_solo_running_state[queue] != self.solo_running_state[queue]:
                            last_solo_running_state[queue] = self.solo_running_state[queue].copy()
                            
                        tasks = [task for index, task in enumerate(sort_by_tasks) if index not in need_del_index]
                        self.solo_agg_task[queue][agg_key] = tasks
                        
                        if (len(queue_batch_tasks[queue] + left_queue_batch_tasks[queue]) >= max_records or 
                            (last_wait_time[queue] and last_wait_time[queue] < current_time - max_wait_time)):
                            for task in queue_batch_tasks[queue]:
                                await self._async_put_task(event_queue, task)
                            for task in left_queue_batch_tasks[queue]:
                                await self._async_put_task(event_queue, task)    
                            queue_batch_tasks[queue] = []
                            left_queue_batch_tasks[queue] = []
                            last_wait_time[queue] = 0
                        elif last_wait_time[queue] == 0:
                            last_wait_time[queue] = current_time
            
            # 统一的睡眠策略
            sleep_time = self._get_optimal_sleep_time(has_work, checker_type)
            await asyncio.sleep(sleep_time)
    
    def _get_optimal_sleep_time(self, has_work: bool, checker_type: str) -> float:
        """获取最优睡眠时间"""
        if checker_type == 'delay':
            return 0.001 if has_work else 1.0
        elif has_work:
            return 0.001  # 有工作时极短休眠
        else:
            return 0.01   # 无工作时短暂休眠
    
    
    async def async_check_solo_agg_tasks(self, event_queue: asyncio.Queue):
        """异步版本的聚合任务检查"""
        await self._unified_task_checker(event_queue, checker_type='solo_agg')
    
    async def check_solo_agg_tasks(self, event_queue: asyncio.Queue):
        """聚合任务检查"""
        await self._unified_task_checker(event_queue, checker_type='solo_agg')
    
    def check_sole_tasks(self, event_queue: Union[deque, asyncio.Queue]):
        agg_task_mappings = {queue:  defaultdict(list) for queue in self.queues}
        agg_wait_task_mappings = {queue:  defaultdict(float) for queue in self.queues}
        task_max_wait_time_mapping = {}
        make_up_for_index_mappings = {queue:  defaultdict(int) for queue in self.queues} 
        while True:
            put_count = 0
            for queue in self.queues:
                agg_task = agg_task_mappings[queue]
                for routing_key, tasks in self.solo_routing_tasks[queue].items():
                    schedule_time = self.task_scheduler[queue][routing_key]
                    if tasks:
                        for task in tasks:
                            prev_routing = task[0]
                            if agg_key:= prev_routing.get('agg_key'):
                                if not self.running_task_state_mappings[queue][agg_key]:
                                    self.solo_running_state[queue][routing_key] = False
                                    break 
                    if (
                        schedule_time <= time.time()
                        and self.solo_running_state[queue][routing_key] == False
                    ) :
                            try:
                                routing, task = tasks.pop(0)
                            except IndexError:
                                continue
                            task["routing"] = routing
                            
                            agg_key = routing.get('agg_key')
                            if agg_key is not None:
                                start_time = agg_wait_task_mappings[queue][agg_key]
                                if not start_time:
                                    agg_wait_task_mappings[queue][agg_key] = time.time()
                                    start_time = agg_wait_task_mappings[queue][agg_key]
                                agg_task[agg_key].append(task)
                                max_wait_time = routing.get('max_wait_time', 3)
                                task_max_wait_time_mapping[agg_key] = max_wait_time
                                if len(agg_task[agg_key])>=routing.get('max_records', 100) or time.time()-start_time>=max_wait_time:
                                    logger.debug(f'{agg_key=} {len(agg_task[agg_key])} 已满，准备发车！{routing.get("max_records", 100)} {time.time()-start_time} {max_wait_time}')
                                    for task in agg_task[agg_key]:
                                        task['routing']['version'] = 1
                                        self.running_task_state_mappings[queue][agg_key][task['event_id']] = time.time()
                                        self._put_task(event_queue, task, urgent=self.is_urgent(routing_key))
                                    agg_task[agg_key] = []
                                    make_up_for_index_mappings[queue][agg_key] = 0 
                                    agg_wait_task_mappings[queue][agg_key] = 0
                            else:
                                self._put_task(event_queue, task, urgent=self.is_urgent(routing_key))
                            self.solo_running_state[queue][routing_key] = True
                            put_count += 1
                for agg_key in agg_task.keys():
                    if not agg_task[agg_key]:
                        continue
                    start_time = agg_wait_task_mappings[queue][agg_key]
                    max_wait_time = task_max_wait_time_mapping[agg_key]
                    if make_up_for_index_mappings[queue][agg_key]>= len(agg_task[agg_key])-1:
                        make_up_for_index_mappings[queue][agg_key] = 0
                    routing = agg_task[agg_key][make_up_for_index_mappings[queue][agg_key]]['routing']
                    routing_key = routing['routing_key']
                    self.solo_running_state[queue][routing_key] = False
                    make_up_for_index_mappings[queue][agg_key] += 1
                    if time.time()-start_time>=max_wait_time:
                        logger.debug(f'{agg_key=} {len(agg_task[agg_key])}被迫发车！ {time.time()-start_time} {max_wait_time}')
                        for task in agg_task[agg_key]:
                            task['routing']['version'] = 1
                            self.running_task_state_mappings[queue][agg_key][task['event_id']] = time.time()
                            self._put_task(event_queue, task, urgent=self.is_urgent(routing_key))
                        agg_task[agg_key] = []
                        make_up_for_index_mappings[queue][agg_key] = 0
                        agg_wait_task_mappings[queue][agg_key] = 0
            # 优化：根据处理任务数量动态调整休眠时间
            if not put_count:
                time.sleep(0.001)
            elif put_count < 5:
                time.sleep(0.0005)  # 少量任务时极短休眠
                
    async def check_batch_tasks(self, event_queue: asyncio.Queue):
        """批量任务检查 - 已简化为统一检查器"""
        # 批量任务逻辑已整合到其他检查器中，这个函数保留以兼容
        await asyncio.sleep(0.1)

    async def check_delay_tasks(self, event_queue: asyncio.Queue):
        """延迟任务检查"""
        await self._unified_task_checker(event_queue, checker_type='delay')

    def _handle_redis_error(self, error: Exception, consecutive_errors: int, queue: str = None) -> tuple[bool, int]:
        """处理Redis错误的通用方法
        返回: (should_recreate_connection, new_consecutive_errors)
        """
        if isinstance(error, redis.exceptions.ConnectionError):
            logger.error(f'Redis连接错误: {error}')
            logger.error(traceback.format_exc())
            consecutive_errors += 1
            if consecutive_errors >= 5:
                logger.error(f'连续连接失败{consecutive_errors}次，重新创建连接')
                return True, 0
            return False, consecutive_errors
            
        elif isinstance(error, redis.exceptions.ResponseError):
            if "NOGROUP" in str(error) and queue:
                logger.warning(f'队列 {queue} 或消费者组不存在')
                return False, consecutive_errors
            else:
                logger.error(f'Redis错误: {error}')
                logger.error(traceback.format_exc())
                consecutive_errors += 1
                return False, consecutive_errors
        else:
            logger.error(f'意外错误: {error}')
            logger.error(traceback.format_exc())
            consecutive_errors += 1
            return False, consecutive_errors

    def _process_message_common(self, event_id: str, event_data: dict, queue: str, event_queue, is_async: bool = False, consumer_name: str = None, group_name: str = None):
        """通用的消息处理逻辑，供同步和异步版本使用"""
        # 检查消息是否已被认领，防止重复处理
        if event_id in self._claimed_message_ids:
            logger.debug(f"跳过已认领的消息 {event_id}")
            return event_id
        
        # 解析消息中的实际数据
        # event_data 格式: {b'data': b'{"name": "...", "event_id": "...", ...}'}
        actual_event_id = event_id  # 默认使用Stream ID
        parsed_event_data = None  # 解析后的数据
        
        # 检查是否有data字段（Stream消息格式）
        if 'data' in event_data or b'data' in event_data:
            data_field = event_data.get('data') or event_data.get(b'data')
            if data_field:
                try:
                    # 直接解析二进制数据，不需要解码
                    if isinstance(data_field, bytes):
                        parsed_data = loads_str(data_field)
                    else:
                        parsed_data = data_field
                    # 检查是否有原始的event_id（延迟任务会有）
                    if 'event_id' in parsed_data:
                        actual_event_id = parsed_data['event_id']
                    # 使用解析后的数据作为event_data
                    parsed_event_data = parsed_data
                except (ValueError, UnicodeDecodeError):
                    pass  # 解析失败，使用默认的Stream ID
        
        # 如果成功解析了数据，使用解析后的数据；否则使用原始数据
        final_event_data = parsed_event_data if parsed_event_data is not None else event_data
        
        routing = final_event_data.get("routing")
        
        # 从消息体中获取实际的队列名（可能包含优先级后缀）
        # 这确保ACK使用正确的stream key
        actual_queue = final_event_data.get('queue', queue)

        # 如果没有传入group_name，使用默认值（prefixed_queue）
        if not group_name:
            prefixed_queue = self.get_prefixed_queue_name(queue)
            group_name = prefixed_queue

        # 提取并确保 offset 在 event_data 中（关键：确保延迟任务的 offset 能被传递到 executor）
        offset = None
        if 'offset' in final_event_data:
            try:
                offset = int(final_event_data['offset'])
            except (ValueError, TypeError):
                pass
        # 如果 final_event_data 中没有 offset，从原始 event_data 中提取（Stream 消息格式）
        elif 'offset' in event_data or b'offset' in event_data:
            offset_field = event_data.get('offset') or event_data.get(b'offset')
            if offset_field:
                try:
                    offset = int(offset_field)
                    # 将 offset 添加到 final_event_data 中，确保 executor 能提取
                    final_event_data['offset'] = offset
                except (ValueError, TypeError):
                    pass

        task_item = {
            "queue": actual_queue,  # 使用消息体中的实际队列名（可能包含优先级）
            "event_id": actual_event_id,
            "event_data": final_event_data,  # 使用解析后的数据（包含 offset）
            "consumer": consumer_name,  # 添加消费者信息
            "group_name": group_name,  # 添加group_name用于ACK
        }
        
        push_flag = True
        if routing:
            # routing 现在直接是对象，不需要反序列化
            if agg_key := routing.get('agg_key'):
                self.solo_agg_task[queue][agg_key].append(
                    [routing, task_item]
                )
                push_flag = False
        
        if push_flag:
            if is_async:
                # 这里不能直接await，需要返回一个标记
                return ('async_put', task_item)
            else:
                self._put_task(event_queue, task_item)
        
        return event_id
    
    async def _execute_recovery_for_queue(self, queue: str, log_prefix: str = "Recovery") -> int:
        """
        执行单个队列的消息恢复（封装通用逻辑）

        Args:
            queue: 队列名称
            log_prefix: 日志前缀，用于区分调用场景（如"Recovery Event"或"Recovery Fallback"）

        Returns:
            int: 恢复的消息数量
        """
        # 查找队列对应的所有任务
        from jettask.utils.queue_matcher import find_matching_tasks
        task_names = find_matching_tasks(queue, self.app._tasks_by_queue, self.wildcard_mode)

        if not task_names:
            logger.debug(f"[{log_prefix}] No tasks found for queue {queue}")
            return 0

        total_recovered = 0

        # 为每个任务执行恢复
        for task_name in task_names:
            # 获取该任务的恢复器（如果已创建）
            recovery_key = f"recovery_{task_name}"
            recovery = getattr(self, recovery_key, None)

            if not recovery:
                # 创建新的恢复器（使用 WorkerManager）
                from jettask.worker.lifecycle import WorkerManager
                recovery = WorkerManager(
                    redis_client=self.redis_client,
                    async_redis_client=self.async_binary_redis_client,
                    redis_prefix=self.redis_prefix,
                    queue_formatter=lambda q: f"{self.redis_prefix}:QUEUE:{q}",
                    queue_registry=self.queue_registry,
                    app=self.app,
                    tasks=self.tasks,
                    task_event_queues=self.task_event_queues,
                    worker_id=self.worker_id
                )
                setattr(self, recovery_key, recovery)

            # 获取当前 consumer
            base_queue = queue.split(':')[0]

            try:
                current_consumer = self.get_consumer_name(base_queue)
            except Exception as e:
                logger.warning(f"[{log_prefix}] Failed to get consumer for queue {queue}: {e}")
                continue

            # 创建一个回调函数，根据 task_name 获取对应的 event_queue
            def get_event_queue_by_task(tn: str):
                """根据 task_name 获取对应的 event_queue"""
                if self.task_event_queues:
                    return self.task_event_queues.get(tn)
                return None

            # 执行恢复（传入 event_queue_callback）
            try:
                recovered = await recovery.recover_offline_workers(
                    task_name=task_name,
                    event_queue=None,  # 保持为 None，通过 callback 传递
                    event_queue_callback=get_event_queue_by_task  # 传入回调函数
                )
                total_recovered += recovered

                if recovered > 0:
                    logger.debug(f"[{log_prefix}] Recovered {recovered} messages for task {task_name} on queue {queue}")
            except Exception as e:
                logger.error(f"[{log_prefix}] Error recovering task {task_name} on queue {queue}: {e}")
                continue

        return total_recovered

    async def handle_worker_offline_event(self, worker_id: str, queues: list = None):
        """
        处理 Worker 离线事件（事件驱动）
        当收到 Worker 离线通知时立即处理消息转移

        Args:
            worker_id: 离线的 Worker ID
            queues: Worker 负责的队列列表（可选，如果不提供则从 Redis 读取）
        """
        try:
            logger.debug(f"[Recovery Event] Received offline event for worker {worker_id}")
            
            # print(f'恢复消息1111 {self.app._tasks_by_queue=}')
            # 如果没有提供队列列表，通过 WorkerManager 获取
            if not queues:
                if self.app and hasattr(self.app, 'worker_state'):
                    worker_info = await self.app.worker_state.get_worker_info(worker_id)
                    if worker_info:
                        queues_str = worker_info.get('queues', '')
                        queues = queues_str.split(',') if queues_str else []
                else:
                    logger.warning(f"[Recovery Event] WorkerManager not available, cannot get worker info for {worker_id}")
                    return

            if not queues:
                logger.warning(f"[Recovery Event] No queues found for worker {worker_id}, skipping recovery")
                return

            # 检查 task_event_queues 是否可用
            if not self.task_event_queues:
                logger.warning(f"[Recovery Event] No task_event_queues available, recovered messages will not be executed")

            # 为每个队列触发恢复
            for queue in queues:
                if not queue.strip():
                    continue

                logger.debug(f"[Recovery Event] Triggering recovery for worker {worker_id} on queue {queue}")

                try:
                    # 使用封装的方法执行恢复
                    recovered = await self._execute_recovery_for_queue(queue, log_prefix="Recovery Event")

                    if recovered > 0:
                        logger.debug(f"[Recovery Event] Recovered {recovered} messages from worker {worker_id} on queue {queue}")
                    else:
                        logger.debug(f"[Recovery Event] No messages to recover from worker {worker_id} on queue {queue}")
                except Exception as e:
                    logger.warning(f"[Recovery Event] Failed to recover queue {queue}: {e}")
                    continue

        except Exception as e:
            logger.error(f"[Recovery Event] Error handling offline event for worker {worker_id}: {e}", exc_info=True)

    async def _perform_self_recovery(self, queues: set, event_queue: dict):
        """
        在worker启动时执行"自我恢复"

        场景：Worker复用了离线worker ID，但此时worker已经变为在线状态(is_alive=true)，
        周期性扫描只查找is_alive=false的worker，会漏掉当前worker之前的pending消息。

        解决方案：主动恢复"当前worker"的pending消息，无论is_alive状态如何。

        Args:
            queues: 需要恢复的队列集合（包括优先级队列）
            event_queue: 事件队列字典
        """
        logger.debug("[Recovery Self] Starting self-recovery for current worker...")

        # 获取当前 worker ID
        current_worker_id = self.worker_id

        if not current_worker_id:
            logger.debug("[Recovery Self] No worker_id available, skipping self-recovery")
            return

        worker_key = f"{self.redis_prefix}:WORKER:{current_worker_id}"
        logger.debug(f"[Recovery Self] Checking pending messages for worker: {current_worker_id}")

        # event_queue callback
        def get_event_queue_by_task(task_name: str):
            """根据 task_name 获取对应的 event_queue"""
            if event_queue:
                return event_queue.get(task_name)
            return None

        total_recovered = 0

        # 按队列恢复消息
        for queue in queues:
            try:
                # 获取基础队列名
                base_queue = queue
                if ':' in queue and queue.rsplit(':', 1)[-1].isdigit():
                    base_queue = queue.rsplit(':', 1)[0]

                # 等待 lifecycle 初始化
                current_consumer = None
                for _ in range(5):
                    try:
                        current_consumer = self.get_consumer_name(base_queue)
                        if current_consumer:
                            # 优先级队列需要添加后缀
                            if base_queue != queue:
                                priority_suffix = queue.rsplit(':', 1)[-1]
                                current_consumer = f"{current_consumer}:{priority_suffix}"
                            break
                    except:
                        pass
                    await asyncio.sleep(0.1)

                if not current_consumer:
                    logger.warning(f"[Recovery Self] Cannot get consumer for queue {queue}, skipping")
                    continue

                # 构建 stream_key
                stream_key = f"{self.redis_prefix}:QUEUE:{queue}"

                # 获取 group_info
                worker_data = await self.async_redis_client.hgetall(worker_key)
                if not worker_data:
                    logger.debug(f"[Recovery Self] Worker {current_worker_id} has no data")
                    continue

                # 解码 worker_data
                decoded_worker_data = {}
                for k, v in worker_data.items():
                    key = k.decode('utf-8') if isinstance(k, bytes) else k
                    value = v.decode('utf-8') if isinstance(v, bytes) else v
                    decoded_worker_data[key] = value

                # 提取 group_info
                group_infos = []
                for key, value in decoded_worker_data.items():
                    if key.startswith('group_info:'):
                        try:
                            group_info = json.loads(value)
                            if group_info.get('queue') == base_queue:
                                group_infos.append(group_info)
                        except Exception as e:
                            logger.error(f"[Recovery Self] Error parsing group_info: {e}")

                if not group_infos:
                    logger.debug(f"[Recovery Self] No group_info for queue {queue}")
                    continue

                # 尝试恢复每个 group 的 pending 消息
                for group_info in group_infos:
                    try:
                        task_name = group_info.get('task_name')
                        group_name = group_info.get('group_name')

                        if not task_name or not group_name:
                            continue

                        # 构建离线 consumer 名称
                        # 统一 group_name 架构：所有队列使用同一个 consumer name
                        offline_consumer_name = group_info.get('consumer_name')

                        # 检查是否有 pending 消息
                        pending_info = await self.async_binary_redis_client.xpending(stream_key, group_name)
                        if not pending_info or pending_info.get('pending', 0) == 0:
                            continue

                        # 查询详细的 pending 消息
                        detailed_pending = await self.async_binary_redis_client.xpending_range(
                            stream_key, group_name,
                            min='-', max='+', count=100,
                            consumername=offline_consumer_name
                        )

                        if not detailed_pending:
                            continue

                        logger.debug(
                            f"[Recovery Self] Found {len(detailed_pending)} pending messages "
                            f"for worker {current_worker_id}, queue {queue}, task {task_name}"
                        )

                        # 认领消息
                        message_ids = [msg['message_id'] for msg in detailed_pending]
                        claimed_messages = await self.async_binary_redis_client.xclaim(
                            stream_key, group_name, current_consumer,
                            min_idle_time=0,  # 立即认领
                            message_ids=message_ids
                        )

                        if claimed_messages:
                            logger.debug(
                                f"[Recovery Self] Claimed {len(claimed_messages)} messages "
                                f"from {offline_consumer_name} to {current_consumer}"
                            )

                            # 将消息放入 event_queue
                            task_event_queue = get_event_queue_by_task(task_name)
                            if task_event_queue:
                                for msg_id, msg_data in claimed_messages:
                                    if isinstance(msg_id, bytes):
                                        msg_id = msg_id.decode('utf-8')

                                    data_field = msg_data.get(b'data') or msg_data.get('data')
                                    if data_field:
                                        try:
                                            import msgpack
                                            parsed_data = msgpack.unpackb(data_field, raw=False)
                                            parsed_data['_task_name'] = task_name
                                            parsed_data['queue'] = queue

                                            task_item = {
                                                'queue': queue,
                                                'event_id': msg_id,
                                                'event_data': parsed_data,
                                                'consumer': current_consumer,
                                                'group_name': group_name
                                            }

                                            await task_event_queue.put(task_item)
                                            total_recovered += 1
                                        except Exception as e:
                                            logger.error(f"[Recovery Self] Error processing message: {e}")
                            else:
                                logger.warning(f"[Recovery Self] No event_queue for task {task_name}")

                    except Exception as e:
                        logger.error(f"[Recovery Self] Error recovering group {group_info}: {e}", exc_info=True)

            except Exception as e:
                logger.error(f"[Recovery Self] Error recovering queue {queue}: {e}", exc_info=True)

        if total_recovered > 0:
            logger.debug(f"[Recovery Self] Self-recovery completed: recovered {total_recovered} messages")
        else:
            logger.debug("[Recovery Self] Self-recovery completed: no pending messages found")

    async def _update_read_offset(self, queue: str, group_name: str, offset: int):
        """更新已读取的offset（只更新最大值）

        Args:
            queue: 队列名（不带前缀，可能包含优先级后缀，如 "robust_bench2:8"）
            group_name: consumer group名称（格式：{prefix}:QUEUE:{base_queue}:{task_name}）
            offset: 读取的offset值
        """
        try:
            if offset is None:
                return

            read_offset_key = f"{self.redis_prefix}:READ_OFFSETS"

            # 从 group_name 中提取 task_name（最后一段）
            task_name = group_name.split(':')[-1]

            # 构建 field：队列名（含优先级）+ 任务名
            # 例如：robust_bench2:8:benchmark_task
            field = f"{queue}:{task_name}"

            # 使用Lua脚本原子地更新最大offset
            await self.async_redis_client.eval(
                UPDATE_MAX_OFFSET_LUA,
                2,  # keys数量
                read_offset_key,  # KEYS[1]
                field,  # KEYS[2]
                offset  # ARGV[1]
            )
            logger.debug(f"Updated read offset for {field}: {offset}")
        except Exception as e:
            logger.error(f"Error updating read offset: {e}")

    # ==================== 通配符队列发现相关方法 ====================

    async def _initial_queue_discovery(self):
        """初始队列发现（启动时执行一次）- 仅在通配符模式下使用"""
        if not self.wildcard_mode:
            return

        try:
            logger.debug("[QueueDiscovery] Performing initial queue discovery...")

            # 从 QUEUE_REGISTRY 获取所有队列
            queue_members = await self.async_redis_client.smembers(
                self._queue_registry_key.encode()
            )

            discovered_queues = set()
            for queue_bytes in queue_members:
                queue_name = queue_bytes.decode('utf-8') if isinstance(queue_bytes, bytes) else str(queue_bytes)
                discovered_queues.add(queue_name)

            if not discovered_queues:
                # 如果注册表为空，尝试从现有数据初始化
                logger.warning("[QueueDiscovery] QUEUE_REGISTRY is empty, initializing from existing data...")

                await self.queue_registry.initialize_from_existing_data()
                discovered_queues = await self.queue_registry.get_all_queues()

            logger.debug(f"[QueueDiscovery] Initial discovery found {len(discovered_queues)} queues: {discovered_queues}")

            # 更新队列列表
            self._discovered_queues = discovered_queues
            # 过滤掉通配符本身，只保留实际队列
            self.queues = [q for q in discovered_queues if q != '*']

            # 更新队列配置
            self.consumer_config['queues'] = self.queues

        except Exception as e:
            logger.error(f"[QueueDiscovery] Initial discovery failed: {e}", exc_info=True)
            self._discovered_queues = set()
            self.queues = []

    # ==================== 结束：通配符队列发现相关方法 ====================

    async def _check_queues_with_messages(
        self,
        all_queues: list,
        check_backlog: dict,
        group_name: str
    ) -> list:
        """检查哪些队列有待读取的消息

        Args:
            all_queues: 所有队列列表
            check_backlog: check_backlog字典
            group_name: group名称

        Returns:
            queues_with_messages: 有消息的队列列表
        """
        queues_with_messages = []

        try:
            # 批量获取已发送和已读取的offset
            queue_offsets_key = f"{self.redis_prefix}:QUEUE_OFFSETS"
            read_offsets_key = f"{self.redis_prefix}:READ_OFFSETS"

            # 使用pipeline批量获取offset
            pipe = self.async_redis_client.pipeline()

            # 获取所有队列的已发送offset
            for q in all_queues:
                # 从队列名中提取实际的队列名（去掉前缀）
                actual_queue = q.replace(f"{self.redis_prefix}:QUEUE:", "")
                pipe.hget(queue_offsets_key, actual_queue)

            # 提取 task_name（从 group_name 中）
            task_name = group_name.split(':')[-1]

            # 获取所有队列的已读取offset
            for q in all_queues:
                actual_queue = q.replace(f"{self.redis_prefix}:QUEUE:", "")
                # field 格式：队列名（含优先级）:任务名
                field = f"{actual_queue}:{task_name}"
                pipe.hget(read_offsets_key, field)

            results = await pipe.execute()

            # 分析结果，确定哪些队列有待读取的消息
            half_len = len(all_queues)
            for i, q in enumerate(all_queues):
                # ✅ 如果该队列需要读取 pending 消息，直接加入列表，跳过 offset 检查
                # 默认为 True，这样第一次读取时（check_backlog 为空）会尝试所有队列
                if check_backlog.get(q, True):
                    queues_with_messages.append(q)
                    logger.debug(f"Queue {q} needs to read pending messages, skipping offset check")
                    continue

                sent_offset = results[i]  # 已发送的offset
                read_offset = results[half_len + i]  # 已读取的offset

                # 转换为整数
                sent = int(sent_offset) if sent_offset else 0
                read = int(read_offset) if read_offset else 0

                # 如果已发送的offset大于已读取的offset，说明有消息待读取
                if sent > read:
                    queues_with_messages.append(q)
                    logger.debug(f"Queue {q} has {sent - read} unread messages (sent={sent}, read={read})")

            # 如果没有队列有消息，记录下来
            if not queues_with_messages:
                logger.debug("No queues have unread messages, will wait for new messages")

        except Exception as e:
            # 出错时回退到原始逻辑
            logger.debug(f"Failed to check queue offsets: {e}")
            queues_with_messages = all_queues

        return queues_with_messages

    async def _ensure_group_info_for_all_queues(
        self,
        all_queues: list,
        task_name: str,
        consumer_name: str,
        group_name: str
    ):
        """为所有队列恢复group_info（不影响读取进度）

        Args:
            all_queues: 所有队列列表（已按优先级排序，已带前缀）
            task_name: 任务名
            consumer_name: 消费者名
            group_name: 统一的group_name
        """
        # 统一恢复所有队列的group_info
        for queue in all_queues:
            await self._ensure_consumer_group_and_record_info(
                queue, task_name, consumer_name, group_name
            )

        logger.debug(f"Restored group_info for {len(all_queues)} queues for task {task_name}")

    async def _initialize_queue_for_task(
        self,
        queue_name: str,
        task_name: str,
        consumer_name: str,
        lastid: dict,
        check_backlog: dict,
        base_group_name: str
    ):
        """初始化单个队列用于任务监听

        Args:
            queue_name: 队列名（已带前缀）
            task_name: 任务名
            consumer_name: 消费者名
            lastid: lastid字典（会被更新）
            check_backlog: check_backlog字典（会被更新）
            base_group_name: 基础队列的group_name（必传）
        """
        # 创建consumer group并记录group_info
        await self._ensure_consumer_group_and_record_info(
            queue_name, task_name, consumer_name, base_group_name
        )

        # 初始化读取状态：首次读取pending消息（从"0"开始）
        lastid[queue_name] = "0"
        check_backlog[queue_name] = True

        logger.debug(f"Initialized queue {queue_name} for task {task_name}")

    async def _initialize_all_queues_for_task(
        self,
        all_queues: list,
        task_name: str,
        consumer_name: str,
        lastid: dict,
        check_backlog: dict,
        base_group_name: str
    ) -> list:
        """初始化所有队列（基础队列 + 优先级队列）用于任务监听

        Args:
            all_queues: 所有队列列表（已按优先级排序，已带前缀）
            task_name: 任务名
            consumer_name: 消费者名
            lastid: lastid字典（会被更新）
            check_backlog: check_backlog字典（会被更新）
            base_group_name: 基础队列的group_name（必传）

        Returns:
            all_queues: 所有队列列表
        """
        # 统一初始化所有队列
        for queue in all_queues:
            await self._initialize_queue_for_task(
                queue, task_name, consumer_name, lastid, check_backlog, base_group_name
            )

        logger.debug(f"Initialized {len(all_queues)} queues for task {task_name}")

        return all_queues

    async def _read_messages_from_queues(
        self,
        all_queues: list,
        check_backlog: dict,
        group_name: str,
        lastid: dict,
        task_name: str,
        messages_needed: int
    ) -> list:
        """
        从多个队列中按优先级顺序读取消息

        Args:
            all_queues: 所有队列列表（已按优先级排序）
            check_backlog: 字典，标记每个队列是否需要读取历史消息
            group_name: 消费者组名称
            lastid: 字典，记录每个队列的最后读取ID
            task_name: 任务名称
            messages_needed: 需要读取的消息数量

        Returns:
            list: 读取到的消息列表
        """
        messages = []

        # 预先检查哪些队列有待读取的消息
        # check_backlog.get(q, True) 默认为 True，第一次读取时会尝试所有队列
        queues_with_messages = await self._check_queues_with_messages(
            all_queues, check_backlog, group_name
        )

        if not queues_with_messages:
            return messages

        # 按优先级顺序读取有消息的队列
        for q in queues_with_messages:
            if messages_needed <= 0:
                break  # 已经读取足够的消息

            q_bytes = q.encode() if isinstance(q, str) else q
            # 使用 check_backlog 判断是否需要读取历史消息
            # 默认为 True，第一次读取时（check_backlog 为空）会从头读取以恢复 pending 消息
            if check_backlog.get(q, True):
                myid = lastid.get(q, "0-0")
            else:
                myid = ">"
            myid_bytes = myid.encode() if isinstance(myid, str) else myid

            try:
                # print(f'{myid_bytes=} {self.worker_id=} {check_backlog=} {q_bytes=}')
                # 所有队列（包括优先级队列）都使用基础队列的 group_name
                # 从当前优先级队列读取（最多读取messages_needed个）
                q_messages = await self.async_binary_redis_client.xreadgroup(
                    groupname=group_name,
                    consumername=self.worker_id,
                    streams={q_bytes: myid_bytes},
                    count=messages_needed,  # 只读取需要的数量
                    block=100  # 非阻塞
                )
                logger.debug(f'{group_name=} {q_bytes=} {self.worker_id=} {q_messages=}')
                if q_messages:
                    # logger.debug(f"Read messages from {q}: {len(q_messages[0][1]) if q_messages else 0} messages")
                    # if check_backlog.get(q, True):
                    #     print(f'先处理历史消息：{q_bytes=} {group_name=} {q_messages=}')
                    # 记录从哪个队列读取的
                    messages.extend(q_messages)
                    messages_read = len(q_messages[0][1]) if q_messages else 0
                    messages_needed -= messages_read

                    # 如果高优先级队列还有消息，继续从该队列读取
                    # 直到该队列空了或者达到prefetch限制
                    if messages_read > 0 and messages_needed > 0:
                        # 该队列可能还有更多消息，下次循环继续优先从这个队列读
                        # 但现在先处理已读取的消息
                        break  # 跳出for循环，处理已有消息

            except Exception as e:
                if "NOGROUP" in str(e):
                    # consumer group 不存在（可能是 Redis 被清空了），重新创建
                    logger.warning(f"NOGROUP error for queue {q}, recreating consumer group...")
                    try:
                        # 为队列创建consumer group并初始化读取状态
                        await self._initialize_queue_for_task(
                            q, task_name, self.worker_id, lastid, check_backlog, base_group_name=group_name
                        )

                        # 确保这个队列在 all_queues 中（可能因 Redis 清空而丢失）
                        if q not in all_queues:
                            all_queues.append(q)
                            logger.debug(f"Re-added queue {q} to all_queues after NOGROUP recovery")
                    except Exception as recreate_error:
                        logger.error(f"Failed to recreate consumer group for {q}: {recreate_error}")
                else:
                    logger.debug(f"Error reading from queue {q}: {e}")
                continue

        return messages

    async def _report_delivered_offsets(self, messages: list, group_name: str):
        """
        上报已投递的offset（用于积压监控）

        Args:
            messages: Redis Stream 消息列表
            group_name: 消费者组名称
        """
        try:
            from jettask.utils.stream_backlog import report_delivered_offset
            # 对每个stream的消息上报offset
            for msg in messages:
                stream_name = msg[0]
                if isinstance(stream_name, bytes):
                    stream_name = stream_name.decode('utf-8')
                # 提取队列名（去掉前缀）
                queue_name = stream_name.replace(f"{self.redis_prefix}:STREAM:", "")
                await report_delivered_offset(
                    self.async_redis_client,
                    self.redis_prefix,
                    queue_name,
                    group_name,
                    [msg]
                )
        except Exception as e:
            # 监控失败不影响主流程
            logger.debug(f"Failed to report delivered offset: {e}")

    async def listen_event_by_task(self, task_obj: "Task", queue_name: str, prefetch_multiplier: int):
        """为单个任务监听事件"""
        # 恢复读取历史 pending 消息的逻辑
        check_backlog = {}  # {queue_name: bool} - 首次读取 pending 消息
        lastid = {}  # 每个队列的lastid - 首次为 "0"，后续为 ">"
        consecutive_errors = 0
        max_consecutive_errors = 5

        # 从 task_obj 获取 task_name
        task_name = task_obj.name

        # 从 self.task_event_queues 中提取该任务的事件队列
        task_event_queue = self.task_event_queues.get(task_name)
        if not task_event_queue:
            logger.error(f"No event queue found for task {task_name}")
            return

        # 定义必要的变量
        # 注意：这里的 queue_name 参数已经是真实队列名（由 _listen_task 传入）
        # 不再使用 task.queue（可能是通配符），而是使用传入的真实队列名

        # 直接获取所有队列（包括基础队列和优先级队列）
        # 基础队列在第一个位置
        # all_queues = await self.get_priority_queues_direct(queue_name)
        all_queues = []
        prefixed_queue = queue_name # 基础队列

        # 使用函数名作为group_name，实现任务隔离（用于后续消息处理）
        group_name = f"{prefixed_queue}:{task_name}"

        # # 初始化所有队列
        # await self._initialize_all_queues_for_task(
        #     all_queues, task_name, self.worker_id, lastid, check_backlog, group_name
        # )

        # 记录上次优先级队列更新时间和上次group_info检查时间
        last_priority_update = 0

        while not self._stop_reading:
            # 定期直接从Redis获取所有队列（每1秒检查一次）
            current_time = time.time()
            if current_time - last_priority_update >= 1:  # 简化为固定1秒间隔
                new_all_queues = await self.get_priority_queues_direct(queue_name)
                # 如果队列有变化，更新本地变量并初始化新队列
                if new_all_queues != all_queues:
                    # logger.debug(f"Queues updated for {queue_name}: {all_queues} -> {new_all_queues}")

                    # 找出新增的队列
                    new_queues = set(new_all_queues) - set(all_queues)
                    if new_queues:
                        # logger.debug(f"Initializing {len(new_queues)} new queues: {new_queues}")
                        # 初始化新队列
                        for new_queue in new_queues:
                            await self._initialize_queue_for_task(
                                new_queue, task_name, self.worker_id, lastid, check_backlog, group_name
                            )

                    # 更新队列列表
                    all_queues = new_all_queues
                last_priority_update = current_time

            # 处理正常的Stream消息（支持优先级队列）
            # 实现真正的优先级消费：
            # 1. 先检查event_queue是否已满
            # 2. 优先从高优先级队列读取
            # 3. 只有高优先级队列空了才读取低优先级
            # 4. 不超过prefetch_multiplier限制
            
            # 检查内存队列是否已满
            current_queue_size = task_event_queue.qsize() if hasattr(task_event_queue, 'qsize') else 0
            if current_queue_size >= prefetch_multiplier:
                # 内存队列已满，等待处理
                await asyncio.sleep(0.01)  # 短暂等待
                continue

            # 计算还能读取的消息数
            messages_needed = prefetch_multiplier - current_queue_size

            if messages_needed <= 0:
                # 不需要读取更多消息
                await asyncio.sleep(0.01)
                continue

            # 从队列中读取消息
            messages = await self._read_messages_from_queues(
                all_queues, check_backlog, group_name, lastid, task_name, messages_needed
            )

            # 如果没有读取到消息，短暂等待
            if not messages:
                await asyncio.sleep(0.2)
                continue


            try:
                # logger.debug(f'{group_name=} {self.worker_id=} {block_time=}')
                consecutive_errors = 0
                # if check_backlog and messages:
                #     logger.debug(f'先消费之前的消息 {group_name=} ')
                # logger.debug(f'{check_backlog=} {messages=}')

                # 上报已投递的offset（用于积压监控）
                await self._report_delivered_offsets(messages, group_name)
                
                # 收集需要跳过的消息ID
                skip_message_ids = []
                
                # 用于记录每个队列的最大offset（批量更新）
                max_offsets_per_queue = {}
                
                for message in messages:
                    # print(f'{message=}')
                    # message[0]是stream名称，message[1]是消息列表
                    stream_name = message[0]
                    if isinstance(stream_name, bytes):
                        stream_name = stream_name.decode('utf-8')
                    
                    # 根据这个具体队列的消息数量，更新该队列的check_backlog状态
                    if len(message[1]) == 0:
                        # 这个队列没有历史消息了，下次读取最新消息
                        check_backlog[stream_name] = False
                    
                    for event in message[1]:
                        event_id = event[0]
                        # 更新对应队列的lastid
                        lastid[stream_name] = event_id
                        # 将bytes类型的event_id转换为字符串
                        if isinstance(event_id, bytes):
                            event_id = event_id.decode('utf-8')
                        event_data = event[1]
                        
                        # 解析消息内容，决定是否处理
                        should_process = True
                        
                        try:
                            # 解析data字段中的消息
                            if b'data' in event_data or 'data' in event_data:
                                data_field = event_data.get(b'data') or event_data.get('data')
                                
                                # 直接解析二进制数据，不需要解码
                                parsed_data = loads_str(data_field)

                            
                                # 每个task都有独立的consumer group
                                # 检查消息是否指定了目标task（用于精确路由）
                                target_tasks = parsed_data.get('_target_tasks', None)
                                if target_tasks and task_name not in target_tasks:
                                    # 这个消息指定了其他task处理
                                    should_process = False
                                
                                if should_process:
                                    # 添加task_name到数据中（用于执行器识别任务）
                                    parsed_data['_task_name'] = task_name
                                    
                                    # 提取offset字段（如果存在）
                                    offset_field = event_data.get(b'offset') or event_data.get('offset')
                                    message_offset = None
                                    if offset_field:
                                        # 将offset添加到parsed_data中
                                        if isinstance(offset_field, bytes):
                                            offset_field = offset_field.decode('utf-8')
                                        parsed_data['offset'] = offset_field
                                        try:
                                            message_offset = int(offset_field)
                                        except (ValueError, TypeError):
                                            pass
                                    
                                    # 更新event_data
                                    event_data.clear()
                                    for key, value in parsed_data.items():
                                        event_data[key] = value
                                    
                                    # 收集每个队列的最大offset（不要每条消息都记录）
                                    if message_offset is not None:
                                        # 从stream_name提取实际的队列名
                                        actual_queue_name = stream_name.replace(f"{self.redis_prefix}:QUEUE:", "")
                                        # 更新该队列的最大offset
                                        if actual_queue_name not in max_offsets_per_queue:
                                            max_offsets_per_queue[actual_queue_name] = message_offset
                                        else:
                                            max_offsets_per_queue[actual_queue_name] = max(max_offsets_per_queue[actual_queue_name], message_offset)
                                    
                                    logger.debug(f"Task {task_name} will process message {event_id}")
                            else:
                                # 没有data字段，跳过消息
                                should_process = False
                        except Exception as e:
                            logger.error(f"Task {task_name}: Error parsing message data: {e}")
                        
                        if should_process:
                            # 处理消息 - 消息会被放入队列，由执行器处理并ACK
                            # 使用消息体中的实际队列名（可能包含优先级）
                            actual_queue = event_data.get('queue', queue_name)

                            # 统一 group_name 架构：所有队列（包括优先级队列）使用同一个 consumer name
                            # 不再需要为优先级队列添加后缀
                            result = self._process_message_common(
                                event_id, event_data, actual_queue, task_event_queue,
                                is_async=True, consumer_name=self.worker_id, group_name=group_name
                            )
                            if isinstance(result, tuple) and result[0] == 'async_put':
                                await self._async_put_task(task_event_queue, result[1])
                                logger.debug(f"Put task {event_id} into task_event_queue")
                            # 注意：这里不ACK，由执行器在处理完成后ACK
                        else:
                            # 不属于当前task的消息，收集起来批量ACK
                            skip_message_ids.append(event_id)
                        
                
                # 批量ACK不需要的消息（所有队列使用同一个 group_name）
                if skip_message_ids:
                    group_name_bytes = group_name.encode() if isinstance(group_name, str) else group_name
                    for q in all_queues:
                        q_bytes = q.encode() if isinstance(q, str) else q
                        try:
                            await self.async_binary_redis_client.xack(q_bytes, group_name_bytes, *skip_message_ids)
                        except:
                            pass  # 忽略ACK错误
                    logger.debug(f"Task {task_name} batch ACKed {len(skip_message_ids)} skipped messages")

                # 批量更新每个队列的最大已读取offset（所有队列使用同一个 group_name）
                if max_offsets_per_queue:
                    for queue_name, max_offset in max_offsets_per_queue.items():
                        asyncio.create_task(self._update_read_offset(queue_name, group_name, max_offset))
                    logger.debug(f"Updated read offsets for {len(max_offsets_per_queue)} queues")
                    
            except Exception as e:
                error_msg = str(e)
                import traceback
                traceback.print_exc()
                logger.error(f"Error in task listener {task_name}: {e}")
                consecutive_errors += 1
                if consecutive_errors >= max_consecutive_errors:
                    logger.error(f"Too many errors for task {task_name}, restarting...")
                    consecutive_errors = 0
                await asyncio.sleep(min(consecutive_errors, 5))


    async def _listen_task(self, task_obj: "Task", prefetch_multiplier: int):
        """
        为单个任务启动监听（以task为粒度）

        每个任务负责管理自己的队列监听，包括：
        1. 静态队列：直接监听
        2. 通配符队列：定期发现新队列并动态监听

        Args:
            task_obj: Task 对象（包含 name, queue, is_wildcard_queue 等属性）
            prefetch_multiplier: 预取倍数
        """
        # 使用 Task 类的 is_wildcard_queue 属性判断是否为通配符模式
        if task_obj.is_wildcard_queue:
            # 通配符模式：需要定期发现新队列
            await self._listen_task_with_wildcard(task_obj, prefetch_multiplier)
        else:
            # 静态队列模式：直接调用核心监听逻辑
            await self._start_single_queue_listener(task_obj, task_obj.queue, prefetch_multiplier)

    async def _start_single_queue_listener(self, task_obj: "Task", queue_name: str, prefetch_multiplier: int):
        """
        启动单个队列的监听（核心可复用逻辑）

        这个方法封装了为单个队列启动监听的完整逻辑，可以被：
        - _listen_task 在静态队列模式下直接 await 调用
        - _listen_task_with_wildcard 创建为后台任务异步调用

        Args:
            task_obj: Task 对象
            queue_name: 具体的队列名称（非通配符）
            prefetch_multiplier: 预取倍数
        """
        task_name = task_obj.name

        # 注册队列到 self.queues
        await self._register_queue_for_task(queue_name, task_name)

        logger.debug(f"[Task: {task_name}] 开始监听队列: {queue_name}")

        # 直接调用 listen_event_by_task 进行监听（这是阻塞的）
        await self.listen_event_by_task(
            task_obj,
            queue_name,
            prefetch_multiplier
        )

    async def _listen_task_with_wildcard(self, task_obj: "Task", prefetch_multiplier: int):
        """
        为任务监听通配符队列（动态发现新队列）

        Args:
            task_obj: Task 对象
            prefetch_multiplier: 预取倍数
        """
        task_name = task_obj.name
        wildcard_pattern = task_obj.queue

        logger.debug(f"[Task: {task_name}] 开始监听通配符队列: {wildcard_pattern}")

        # 记录已监听的队列（简化为 set）
        monitored_queues = set()

        # 定期发现新队列
        discovery_interval = 5.0  # 5秒检查一次

        while not self._stop_reading:
            try:
                # 1. 从注册表中发现匹配的队列
                matched_queues = await self.queue_registry.discover_matching_queues(wildcard_pattern)

                # 2. 找出新增的队列
                new_queues = matched_queues - monitored_queues

                if new_queues:
                    logger.debug(f"[Task: {task_name}] 发现新队列: {list(new_queues)}")

                    # 3. 为每个新队列启动监听任务（复用 _start_single_queue_listener）
                    for queue_name in new_queues:
                        # 创建后台任务，调用核心监听逻辑
                        listen_task = asyncio.create_task(
                            self._start_single_queue_listener(
                                task_obj,
                                queue_name,
                                prefetch_multiplier
                            )
                        )
                        self._background_tasks.append(listen_task)
                        monitored_queues.add(queue_name)

                        logger.debug(f"[Task: {task_name}] 已为队列 {queue_name} 启动监听")

                # 4. 等待下次检查
                await asyncio.sleep(discovery_interval)

            except asyncio.CancelledError:
                logger.debug(f"[Task: {task_name}] 通配符队列监听已取消")
                break
            except Exception as e:
                logger.error(f"[Task: {task_name}] 通配符队列监听出错: {e}", exc_info=True)
                await asyncio.sleep(discovery_interval)

    async def _register_queue_for_task(self, queue: str, task_name: str):
        """
        为任务注册队列到 self.queues 和 Redis

        Args:
            queue: 队列名称
            task_name: 任务名称
        """
        # 添加到 self.queues（如果不存在）
        if queue not in self.queues:
            self.queues.append(queue)
            self.queues.sort()

            # 添加停止标志
            self._queue_stop_flags[queue] = False

            # 更新 Redis 中的 worker queues 字段
            try:
                if self.worker_id and self.app and hasattr(self.app, 'worker_state'):
                    await self.app.worker_state.update_worker_field(
                        self.worker_id,
                        'queues',
                        ','.join(sorted(self.queues))
                    )
                    logger.debug(f"[Task: {task_name}] 新增队列 {queue}，当前总队列: {self.queues}")
            except Exception as e:
                logger.error(f"[Task: {task_name}] 更新 worker queues 字段失败: {e}", exc_info=True)


    async def listening_event(self, prefetch_multiplier: int = 1):
        """监听事件 - 为每个task创建独立的consumer group（以task为粒度）

        新架构：
        - 以 task 为粒度进行监听，而非以 queue 为粒度
        - 每个 task 负责管理自己的队列监听（包括通配符模式的动态队列发现）
        - 简化了队列管理逻辑，职责更加清晰
        - task_event_queues 在初始化时传入，不再作为方法参数

        Args:
            prefetch_multiplier: 预取倍数
        """
        # 验证 task_event_queues 是否已初始化
        if not self.task_event_queues:
            raise RuntimeError("task_event_queues not initialized")

        if not isinstance(self.task_event_queues, dict):
            raise TypeError(f"task_event_queues must be a dict[str, asyncio.Queue], got {type(self.task_event_queues)}")

        # logger.debug(f"Using task-isolated event queue mode for tasks: {list(self.task_event_queues.keys())}")

        # 保存所有创建的任务，以便清理时能够取消它们
        self._background_tasks = []

        if not self.tasks:
            raise RuntimeError("No tasks configured for EventPool")

        tasks = []

        # 检查 worker_id 是否已初始化
        if not self.worker_id:
            raise RuntimeError("Worker ID not initialized, cannot start listeners")

        # 直接遍历 self.tasks（任务字典）
        for task_name, task_obj in self.tasks.items():
            # 验证任务对象
            if not task_obj:
                logger.warning(f"Task {task_name} has no task object, skipping...")
                continue

            # 检查任务是否配置了队列
            # 注意：不使用 self.redis_prefix 作为 fallback，它只是命名空间前缀
            if not task_obj.queue:
                logger.warning(f"Task {task_name} has no queue configured, skipping...")
                continue

            logger.debug(f"为任务 {task_name} 启动监听，队列模式: {task_obj.queue}, worker_id: {self.worker_id}")

            # 为每个任务创建监听任务
            task = asyncio.create_task(
                self._listen_task(
                    task_obj=task_obj,
                    prefetch_multiplier=prefetch_multiplier
                )
            )
            tasks.append(task)
            self._background_tasks.append(task)

        # logger.debug(f"共为 {len(tasks)} 个任务启动了监听")


        # 启动离线 worker 恢复任务（每 30 秒扫描一次）
        recovery_task = asyncio.create_task(
            self.offline_recovery.start(recovery_interval=30.0)
        )
        self._background_tasks.append(recovery_task)
        logger.debug("[Recovery] Started offline worker recovery loop")

        # 启动离线 worker 清理任务（每天执行一次）
        cleanup_task = asyncio.create_task(
            self.offline_recovery.start_cleanup_task(cleanup_interval=86400.0)
        )
        self._background_tasks.append(cleanup_task)
        logger.debug("[Cleanup] Started offline worker cleanup task")

        try:
            # 等待所有任务
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            logger.debug("listening_event tasks cancelled, cleaning up...")

            # 取消所有后台任务
            for task in self._background_tasks:
                if not task.done():
                    task.cancel()
            # 等待所有任务完成（使用return_exceptions=True避免再次抛出异常）
            if self._background_tasks:
                try:
                    await asyncio.wait_for(
                        asyncio.gather(*self._background_tasks, return_exceptions=True),
                        timeout=0.2
                    )
                except asyncio.TimeoutError:
                    logger.debug("Some background tasks did not complete in time")
            raise

    def read_pending(self, groupname: str, queue: str, asyncio: bool = False):
        client = self.get_redis_client(asyncio, binary=True)
        prefixed_queue = self.get_prefixed_queue_name(queue)
        return client.xpending(prefixed_queue, groupname)

    def ack(self, queue, event_id, asyncio: bool = False):
        client = self.get_redis_client(asyncio, binary=True)
        prefixed_queue = self.get_prefixed_queue_name(queue)
        result = client.xack(prefixed_queue, prefixed_queue, event_id)
        # 清理已认领的消息ID
        if event_id in self._claimed_message_ids:
            self._claimed_message_ids.remove(event_id)
        return result
    def _safe_redis_operation(self, operation, *args, max_retries=3, **kwargs):
        """
        安全的Redis操作，带有重试机制

        注意：Redis连接池已配置为无限重试（InfiniteRetry），会自动处理连接失败。
        这里的重试主要用于处理应用层面的临时错误。
        """
        for attempt in range(max_retries):
            try:
                return operation(*args, **kwargs)
            except (redis.exceptions.TimeoutError, redis.exceptions.ConnectionError) as e:
                if attempt == max_retries - 1:
                    logger.error(f"Redis操作失败，已重试{max_retries}次: {e}")
                    raise

                logger.warning(f"Redis操作失败，第{attempt + 1}次重试: {e}")
                # 不需要手动重新创建连接，连接池会自动重试
                time.sleep(min(2 ** attempt, 5))  # 指数退避，最多5秒
    
    def cleanup(self):
        """清理EventPool资源"""
        # 立即设置停止标志，阻止后台任务继续处理
        self._stop_reading = True

        # 停止恢复和清理任务
        if hasattr(self, 'offline_recovery') and self.offline_recovery:
            if hasattr(self.offline_recovery, 'stop_recovery'):
                self.offline_recovery.stop_recovery()
            if hasattr(self.offline_recovery, 'stop_cleanup'):
                self.offline_recovery.stop_cleanup()

        # EventPool cleanup - 目前没有需要清理的资源
        logger.debug("EventPool cleanup completed")