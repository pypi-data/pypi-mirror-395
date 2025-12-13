"""
异步延迟队列 - 基于 asyncio 和 heapq 的高效延迟任务存储

核心特性：
1. 纯数据结构：只负责存储和检索，不执行任务
2. 高性能：插入/删除都是 O(log n)
3. 线程安全：在 asyncio 事件循环内安全使用
4. 支持取消：可以取消指定任务
"""

import heapq
import time
import logging
from typing import Dict, List, Optional

logger = logging.getLogger('app')


class AsyncDelayQueue:
    """
    异步延迟队列 - 纯数据结构

    使用最小堆（heapq）管理延迟任务，提供添加、获取到期任务、取消等操作。
    不主动执行任务，由外部（如 TaskExecutor.run()）主动调用 get_expired_tasks() 获取。
    """

    def __init__(self):
        """初始化延迟队列"""
        self.heap = []  # [(exec_time, counter, task_id, task_data)]
        self._counter = 0  # 保证堆内唯一排序（相同时间的任务按插入顺序）
        self._task_map: Dict[str, int] = {}  # task_id -> counter 映射，用于取消任务

        logger.debug("AsyncDelayQueue initialized")

    def put(self, task_data: Dict, delay: float) -> str:
        """
        添加一个延迟任务

        Args:
            task_data: 任务数据（字典格式）
            delay: 延迟秒数

        Returns:
            str: 任务ID（可用于取消）
        """
        exec_time = time.time() + delay
        task_id = task_data.get('event_id', f'task_{self._counter}')

        self._counter += 1
        heapq.heappush(self.heap, (exec_time, self._counter, task_id, task_data))
        self._task_map[task_id] = self._counter

        logger.debug(
            f"[DelayQueue] Added task {task_id}, delay={delay:.3f}s, "
            f"exec_time={exec_time:.3f}, queue_size={len(self.heap)}"
        )
        return task_id

    def get_expired_tasks(self) -> List[Dict]:
        """
        获取所有到期的任务

        主动式获取，由外部定期调用此方法检查是否有任务到期。

        Returns:
            List[Dict]: 到期任务列表，每个元素是任务数据字典
        """
        current_time = time.time()
        expired_tasks = []

        # 从堆顶开始取出所有到期的任务
        while self.heap:
            exec_time, counter, task_id, task_data = self.heap[0]

            # 如果堆顶任务还没到期，说明后面的都没到期（最小堆）
            if exec_time > current_time:
                break

            # 任务已到期，弹出
            heapq.heappop(self.heap)

            # 检查是否已被取消
            if task_id not in self._task_map:
                logger.debug(f"[DelayQueue] Task {task_id} was cancelled, skipping")
                continue

            # 从映射中移除
            self._task_map.pop(task_id, None)

            # 添加到结果列表
            expired_tasks.append(task_data)

        if expired_tasks:
            logger.info(
                f"[DelayQueue] Retrieved {len(expired_tasks)} expired tasks, "
                f"remaining={len(self.heap)}"
            )

        return expired_tasks

    def cancel(self, task_id: str) -> bool:
        """
        取消一个延迟任务

        Args:
            task_id: 任务ID

        Returns:
            bool: 是否成功取消
        """
        if task_id not in self._task_map:
            return False

        # 标记为已取消（从映射中删除）
        self._task_map.pop(task_id)
        logger.debug(f"[DelayQueue] Cancelled task {task_id}")
        return True

    def get_next_expire_time(self) -> Optional[float]:
        """
        获取下一个任务的到期时间

        用于智能休眠：计算到下一个任务到期的时间间隔

        Returns:
            Optional[float]: 到期时间（Unix时间戳），如果没有任务返回None
        """
        if not self.heap:
            return None

        # 从堆顶找第一个未取消的任务
        for exec_time, counter, task_id, task_data in self.heap:
            if task_id in self._task_map:
                return exec_time

        return None

    def size(self) -> int:
        """获取队列中的任务数量（包括已取消但未清理的）"""
        return len(self.heap)

    def active_size(self) -> int:
        """获取队列中活跃任务数量（不包括已取消的）"""
        return len(self._task_map)

    def is_empty(self) -> bool:
        """检查队列是否为空（没有活跃任务）"""
        return len(self._task_map) == 0

    def clear(self):
        """清空队列"""
        self.heap.clear()
        self._task_map.clear()
        logger.debug("[DelayQueue] Cleared all tasks")


__all__ = ['AsyncDelayQueue']
