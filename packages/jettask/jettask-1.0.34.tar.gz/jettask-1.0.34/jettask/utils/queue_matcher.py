"""
队列通配符匹配工具

提供队列名称的通配符匹配功能，支持动态队列发现场景。
"""

import fnmatch
from typing import List, Dict, Set, Tuple


def is_wildcard_pattern(queue: str) -> bool:
    """
    检查队列名是否包含通配符

    Args:
        queue: 队列名称

    Returns:
        bool: 如果包含 * 或 ? 通配符则返回 True

    Examples:
        >>> is_wildcard_pattern('robust_*')
        True
        >>> is_wildcard_pattern('test?')
        True
        >>> is_wildcard_pattern('normal_queue')
        False
    """
    return '*' in queue or '?' in queue


def separate_wildcard_and_static_queues(queues: List[str]) -> Tuple[List[str], List[str]]:
    """
    分离通配符队列和静态队列

    Args:
        queues: 队列列表

    Returns:
        tuple: (wildcard_patterns, static_queues)
            - wildcard_patterns: 包含通配符的队列模式列表
            - static_queues: 不包含通配符的静态队列列表

    Examples:
        >>> separate_wildcard_and_static_queues(['test*', 'robot', 'data?'])
        (['test*', 'data?'], ['robot'])
    """
    wildcard_patterns = []
    static_queues = []

    for queue in queues:
        if is_wildcard_pattern(queue):
            wildcard_patterns.append(queue)
        else:
            static_queues.append(queue)

    return wildcard_patterns, static_queues


def match_queue_to_pattern(queue: str, patterns: List[str]) -> str:
    """
    将实际队列名匹配到通配符模式

    Args:
        queue: 实际队列名，如 'robust_bench2'
        patterns: 通配符模式列表，如 ['robust_*', 'test*']

    Returns:
        str: 匹配到的模式，如果没有匹配则返回 None

    Examples:
        >>> match_queue_to_pattern('robust_bench2', ['robust_*', 'test*'])
        'robust_*'
        >>> match_queue_to_pattern('robot', ['robust_*', 'test*'])
        None
    """
    for pattern in patterns:
        if fnmatch.fnmatch(queue, pattern):
            return pattern
    return None


def find_matching_tasks(
    queue: str,
    tasks_by_queue: Dict[str, List[str]],
    wildcard_mode: bool = False
) -> List[str]:
    """
    为实际队列名查找对应的任务列表

    支持两种方式：
    1. 直接匹配：queue 在 tasks_by_queue 的键中
    2. 通配符匹配：使用通配符模式匹配 tasks_by_queue 的键

    Args:
        queue: 实际队列名，如 'robust_bench2'
        tasks_by_queue: 任务映射字典，键可能是通配符，如 {'robust_*': ['task1']}
        wildcard_mode: 是否启用通配符匹配模式

    Returns:
        List[str]: 匹配到的任务名称列表

    Examples:
        >>> tasks_by_queue = {'robust_*': ['benchmark_task'], 'robot': ['clean_task']}
        >>> find_matching_tasks('robust_bench2', tasks_by_queue, wildcard_mode=True)
        ['benchmark_task']
        >>> find_matching_tasks('robot', tasks_by_queue, wildcard_mode=True)
        ['clean_task']
    """
    # 先尝试直接匹配
    task_names = tasks_by_queue.get(queue, [])

    # 如果没有直接匹配且启用了通配符模式，尝试通配符匹配
    if not task_names and wildcard_mode:
        for pattern, pattern_tasks in tasks_by_queue.items():
            # 检查实际队列名是否匹配 tasks_by_queue 中的通配符模式
            if fnmatch.fnmatch(queue, pattern):
                task_names.extend(pattern_tasks)

    return task_names


def match_task_queue_to_patterns(
    task_queue: str,
    queue_patterns: List[str]
) -> bool:
    """
    检查任务的队列名是否匹配任何队列模式

    Args:
        task_queue: 任务的队列名（可能是通配符），如 'robust_*'
        queue_patterns: 队列模式列表（可能包含通配符），如 ['robust_*', 'test']

    Returns:
        bool: 如果匹配则返回 True

    Examples:
        >>> match_task_queue_to_patterns('robust_*', ['robust_*'])
        True
        >>> match_task_queue_to_patterns('robust_*', ['test*'])
        True  # 'robust_*' 匹配 'test*' 的模式
        >>> match_task_queue_to_patterns('robot', ['robust_*'])
        False
    """
    for queue_pattern in queue_patterns:
        # 如果队列模式包含通配符
        if is_wildcard_pattern(queue_pattern):
            # 检查 task_queue 是否匹配这个通配符模式
            if fnmatch.fnmatch(task_queue, queue_pattern) or task_queue == queue_pattern:
                return True
        else:
            # 精确匹配
            if task_queue == queue_pattern:
                return True

    return False


def discover_matching_queues(
    wildcard_patterns: List[str],
    all_queues: Set[str]
) -> Set[str]:
    """
    从所有队列中发现匹配通配符模式的队列

    Args:
        wildcard_patterns: 通配符模式列表，如 ['test*', 'robust_*']
        all_queues: 所有可用的队列集合

    Returns:
        Set[str]: 匹配到的队列集合

    Examples:
        >>> all_queues = {'test1', 'test2', 'robust_bench', 'robot'}
        >>> discover_matching_queues(['test*'], all_queues)
        {'test1', 'test2'}
    """
    matched_queues = set()

    for pattern in wildcard_patterns:
        # 使用fnmatch进行通配符匹配
        for queue in all_queues:
            if fnmatch.fnmatch(queue, pattern):
                matched_queues.add(queue)

    return matched_queues
