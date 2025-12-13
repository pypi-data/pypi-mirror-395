"""
时间处理工具函数
"""
import json
from datetime import datetime, timezone
from typing import Dict, Any, List


def parse_iso_datetime(time_str: str) -> datetime:
    """
    解析 ISO 格式的时间字符串，确保返回 UTC 时间

    Args:
        time_str: ISO 格式的时间字符串

    Returns:
        UTC 时间的 datetime 对象
    """
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


def format_task_timestamps(task: Dict[str, Any], fields: List[str] = None) -> Dict[str, Any]:
    """
    将任务对象中的时间字段转换为 ISO 格式字符串

    Args:
        task: 任务字典
        fields: 需要转换的字段列表，默认为 ['created_at', 'started_at', 'completed_at']

    Returns:
        转换后的任务字典
    """
    if fields is None:
        fields = ['created_at', 'started_at', 'completed_at']

    for field in fields:
        if task.get(field):
            # PostgreSQL 的 TIMESTAMP WITH TIME ZONE 会返回 aware datetime
            if task[field].tzinfo is None:
                # 如果没有时区信息，假定为 UTC
                task[field] = task[field].replace(tzinfo=timezone.utc)
            task[field] = task[field].isoformat()

    return task


def parse_task_json_fields(task: Dict[str, Any], fields: List[str] = None) -> Dict[str, Any]:
    """
    解析任务对象中的 JSON 字段

    Args:
        task: 任务字典
        fields: 需要解析的字段列表，默认为 ['task_data', 'result', 'metadata']

    Returns:
        解析后的任务字典
    """
    if fields is None:
        fields = ['task_data', 'result', 'metadata']

    for field in fields:
        if task.get(field) and isinstance(task[field], str):
            try:
                task[field] = json.loads(task[field])
            except:
                pass

    return task


def task_obj_to_dict(task_obj) -> Dict[str, Any]:
    """
    将 Task ORM 对象转换为字典

    Args:
        task_obj: Task ORM 对象

    Returns:
        任务字典
    """
    task = {
        'id': task_obj.id,
        'queue_name': task_obj.queue_name,
        'task_name': task_obj.task_name,
        'task_data': task_obj.task_data,
        'priority': task_obj.priority,
        'retry_count': task_obj.retry_count,
        'max_retry': task_obj.max_retry,
        'status': task_obj.status,
        'result': task_obj.result,
        'error_message': task_obj.error_message,
        'created_at': task_obj.created_at,
        'started_at': task_obj.started_at,
        'completed_at': task_obj.completed_at,
        'worker_id': task_obj.worker_id,
        'execution_time': task_obj.execution_time,
        'duration': task_obj.duration,
        'metadata': task_obj.task_metadata,
        'next_sync_time': task_obj.next_sync_time,
        'sync_check_count': task_obj.sync_check_count
    }

    # 转换时间戳为 ISO 格式
    task = format_task_timestamps(task)

    # 解析 JSON 字段
    task = parse_task_json_fields(task)

    return task
