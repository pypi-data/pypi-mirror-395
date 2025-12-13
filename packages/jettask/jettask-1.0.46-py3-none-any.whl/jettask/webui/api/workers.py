"""
Worker 监控模块 - Worker 状态监控、心跳管理、离线历史

提供 Worker 相关的监控和管理功能
"""
from fastapi import APIRouter, HTTPException, Request, Query, Path
from typing import Optional, List, Dict, Any
import logging

from jettask.schemas import (
    WorkersResponse,
    WorkerSummaryResponse,
    WorkerOfflineHistoryResponse
)

router = APIRouter(prefix="/workers", tags=["workers"])
logger = logging.getLogger(__name__)


# ============ Worker 监控 ============

@router.get(
    "/{queue_name}",
    summary="获取队列的 Worker 列表",
    description="获取指定队列所有 Worker 的实时心跳信息和状态",
    response_model=WorkersResponse,
    responses={
        200: {
            "description": "成功返回 Worker 列表"
        },
        500: {
            "description": "服务器内部错误",
            "content": {
                "application/json": {
                    "example": {"detail": "Monitor service not initialized"}
                }
            }
        }
    }
)
async def get_queue_workers(
    request: Request,
    namespace: str = Path(..., description="命名空间名称", example="default"),
    queue_name: str = Path(..., description="队列名称", example="email_queue")
) -> Dict[str, Any]:
    """
    ## 获取队列的 Worker 列表

    获取指定队列所有 Worker 的实时心跳信息，包括在线状态、处理任务等。

    **返回信息包括**:
    - Worker ID
    - 队列名称
    - 在线状态（online/offline）
    - 最后心跳时间
    - 已处理任务数
    - 当前正在处理的任务 ID

    **使用场景**:
    - Worker 监控面板
    - 实时状态查看
    - 负载分析
    - 故障诊断

    **示例请求**:
    ```bash
    curl -X GET "http://localhost:8001/api/v1/workers/default/email_queue"
    ```

    **注意事项**:
    - Worker 状态基于心跳时间判断，超过心跳超时时间视为离线
    - 离线 Worker 仍会在列表中显示一段时间
    - 心跳数据实时更新，可能有轻微延迟
    """
    try:
        # 从 app.state 获取 monitor 实例
        if not hasattr(request.app.state, 'monitor'):
            raise HTTPException(status_code=500, detail="Monitor service not initialized")

        monitor = request.app.state.monitor
        workers = await monitor.get_worker_heartbeats(queue_name)

        return {
            "success": True,
            "namespace": namespace,
            "queue": queue_name,
            "workers": workers
        }
    except Exception as e:
        logger.error(f"获取队列 {queue_name} 的 Worker 信息失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{queue_name}/summary",
    summary="获取队列 Worker 汇总统计",
    description="获取指定队列 Worker 的汇总统计信息，包括总数、在线数、离线数等",
    response_model=WorkerSummaryResponse,
    responses={
        200: {
            "description": "成功返回汇总统计"
        },
        500: {
            "description": "服务器内部错误"
        }
    }
)
async def get_queue_worker_summary(
    request: Request,
    namespace: str = Path(..., description="命名空间名称", example="default"),
    queue_name: str = Path(..., description="队列名称", example="email_queue"),
    fast: bool = Query(False, description="是否使用快速模式（不包含历史数据）", example=False)
) -> Dict[str, Any]:
    """
    ## 获取队列 Worker 汇总统计

    获取指定队列所有 Worker 的汇总统计信息，用于快速了解整体状况。

    **统计指标包括**:
    - 总 Worker 数
    - 在线 Worker 数
    - 离线 Worker 数
    - 总处理任务数
    - 平均每个 Worker 处理任务数

    **快速模式说明**:
    - `fast=false`: 完整模式，包含离线 Worker 历史数据（默认）
    - `fast=true`: 快速模式，只统计当前在线 Worker，性能更好

    **使用场景**:
    - 监控看板汇总信息
    - Worker 集群健康检查
    - 容量规划
    - 性能分析

    **示例请求**:
    ```bash
    # 获取完整统计
    curl -X GET "http://localhost:8001/api/v1/workers/default/email_queue/summary"

    # 使用快速模式
    curl -X GET "http://localhost:8001/api/v1/workers/default/email_queue/summary?fast=true"
    ```

    **注意事项**:
    - 快速模式适合实时监控场景
    - 完整模式适合分析历史趋势
    - 统计数据基于心跳时间，可能有轻微延迟
    """
    try:
        if not hasattr(request.app.state, 'monitor'):
            raise HTTPException(status_code=500, detail="Monitor service not initialized")

        monitor = request.app.state.monitor

        if fast:
            summary = await monitor.get_queue_worker_summary_fast(queue_name)
        else:
            summary = await monitor.get_queue_worker_summary(queue_name)

        return {
            "success": True,
            "namespace": namespace,
            "queue": queue_name,
            "summary": summary
        }
    except Exception as e:
        logger.error(f"获取队列 {queue_name} 的 Worker 汇总统计失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/offline-history",
    summary="获取全局 Worker 离线历史",
    description="获取所有 Worker 的离线历史记录，支持时间范围筛选",
    response_model=WorkerOfflineHistoryResponse,
    responses={
        200: {
            "description": "成功返回离线历史"
        },
        500: {
            "description": "服务器内部错误"
        }
    }
)
async def get_workers_offline_history(
    request: Request,
    limit: int = Query(100, ge=1, le=1000, description="返回记录数量限制", example=100),
    start_time: Optional[float] = Query(None, description="开始时间戳（Unix 时间戳）", example=1697644800),
    end_time: Optional[float] = Query(None, description="结束时间戳（Unix 时间戳）", example=1697731200)
) -> Dict[str, Any]:
    """
    ## 获取全局 Worker 离线历史

    获取所有命名空间、所有队列的 Worker 离线历史记录。

    **返回信息包括**:
    - Worker ID
    - 队列名称
    - 离线时间
    - 最后处理的任务 ID
    - 离线原因（heartbeat_timeout、shutdown、crash 等）

    **使用场景**:
    - Worker 稳定性分析
    - 故障诊断
    - 历史趋势分析
    - 运维报表

    **示例请求**:
    ```bash
    # 获取最近100条离线记录
    curl -X GET "http://localhost:8001/api/v1/workers/offline-history?limit=100"

    # 获取指定时间范围的离线记录
    curl -X GET "http://localhost:8001/api/v1/workers/offline-history?start_time=1697644800&end_time=1697731200&limit=50"
    ```

    **注意事项**:
    - 时间戳使用 Unix 时间戳格式（秒）
    - 默认返回最近100条记录
    - 最大可返回1000条记录
    - 记录按离线时间倒序排列
    """
    try:
        if not hasattr(request.app.state, 'monitor'):
            raise HTTPException(status_code=500, detail="Monitor service not initialized")

        monitor = request.app.state.monitor
        history = await monitor.get_worker_offline_history(limit, start_time, end_time)

        return {
            "success": True,
            "history": history,
            "total": len(history)
        }
    except Exception as e:
        logger.error(f"获取 Worker 离线历史失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{queue_name}/offline-history",
    summary="获取队列 Worker 离线历史",
    description="获取指定队列的 Worker 离线历史记录",
    response_model=WorkerOfflineHistoryResponse,
    responses={
        200: {
            "description": "成功返回队列离线历史"
        },
        500: {
            "description": "服务器内部错误"
        }
    }
)
async def get_queue_workers_offline_history(
    request: Request,
    namespace: str = Path(..., description="命名空间名称", example="default"),
    queue_name: str = Path(..., description="队列名称", example="email_queue"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数量限制", example=100),
    start_time: Optional[float] = Query(None, description="开始时间戳（Unix 时间戳）"),
    end_time: Optional[float] = Query(None, description="结束时间戳（Unix 时间戳）")
) -> Dict[str, Any]:
    """
    ## 获取队列 Worker 离线历史

    获取指定队列的 Worker 离线历史记录，用于分析特定队列的 Worker 稳定性。

    **使用场景**:
    - 分析特定队列的 Worker 稳定性
    - 诊断队列相关的 Worker 问题
    - 队列维护和优化

    **示例请求**:
    ```bash
    curl -X GET "http://localhost:8001/api/v1/workers/default/email_queue/offline-history?limit=50"
    ```

    **注意事项**:
    - 只返回该队列相关的 Worker 离线记录
    - 如果一个 Worker 服务多个队列,只要包含目标队列就会返回
    """
    try:
        if not hasattr(request.app.state, 'monitor'):
            raise HTTPException(status_code=500, detail="Monitor service not initialized")

        monitor = request.app.state.monitor

        # 获取所有历史记录，然后过滤出该队列的
        all_history = await monitor.get_worker_offline_history(limit * 10, start_time, end_time)
        queue_history = [
            record for record in all_history
            if queue_name in record.get('queues', '').split(',')
        ][:limit]

        return {
            "success": True,
            "namespace": namespace,
            "queue": queue_name,
            "history": queue_history,
            "total": len(queue_history)
        }
    except Exception as e:
        logger.error(f"获取队列 {queue_name} 的 Worker 离线历史失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ============ Worker 心跳监控 ============

@router.get(
    "/heartbeat/stats",
    summary="获取心跳监控统计",
    description="获取所有 Worker 的心跳监控统计信息",
    responses={
        200: {
            "description": "成功返回心跳统计",
            "content": {
                "application/json": {
                    "example": {
                        "total_workers": 50,
                        "online_workers": 45,
                        "offline_workers": 3,
                        "timeout_workers": 2
                    }
                }
            }
        },
        500: {
            "description": "服务器内部错误"
        }
    }
)
async def get_heartbeat_stats(request: Request) -> Dict[str, Any]:
    """
    ## 获取心跳监控统计

    获取所有 Worker 的心跳监控统计信息，用于整体健康度监控。

    **统计指标包括**:
    - 总 Worker 数
    - 在线 Worker 数
    - 离线 Worker 数
    - 心跳超时 Worker 数

    **使用场景**:
    - 全局监控大盘
    - 系统健康度评估
    - 告警规则触发
    - 运维看板

    **示例请求**:
    ```bash
    curl -X GET "http://localhost:8001/api/v1/workers/heartbeat/stats"
    ```

    **注意事项**:
    - 统计数据实时计算
    - 超时判断基于配置的心跳超时时间
    - 离线 Worker 会在一定时间后清理
    """
    try:
        if not hasattr(request.app.state, 'monitor'):
            raise HTTPException(status_code=500, detail="Monitor service not initialized")

        monitor = request.app.state.monitor
        stats = await monitor.get_heartbeat_stats()

        return stats
    except Exception as e:
        logger.error(f"获取心跳统计信息失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/heartbeat/{worker_id}",
    summary="检查 Worker 心跳状态",
    description="检查指定 Worker 的心跳状态，判断是否在线",
    responses={
        200: {
            "description": "成功返回心跳状态",
            "content": {
                "application/json": {
                    "example": {
                        "worker_id": "worker-001",
                        "is_online": True
                    }
                }
            }
        },
        500: {
            "description": "服务器内部错误"
        }
    }
)
async def check_worker_heartbeat(
    request: Request,
    worker_id: str = Path(..., description="Worker ID", example="worker-001")
) -> Dict[str, Any]:
    """
    ## 检查 Worker 心跳状态

    检查指定 Worker 的心跳状态，判断该 Worker 是否在线。

    **返回信息**:
    - Worker ID
    - 是否在线（true/false）

    **使用场景**:
    - 故障诊断
    - Worker 健康检查
    - 自动化运维脚本
    - 监控告警

    **示例请求**:
    ```bash
    curl -X GET "http://localhost:8001/api/v1/workers/heartbeat/worker-001"
    ```

    **判断逻辑**:
    - 如果 Worker 最后心跳时间在超时时间内,返回 `is_online: true`
    - 如果超过超时时间,返回 `is_online: false`
    - 如果从未收到心跳,返回 `is_online: false`

    **注意事项**:
    - 在线状态基于最后心跳时间判断
    - 默认心跳超时时间为30秒（可配置）
    - Worker ID 区分大小写
    """
    try:
        if not hasattr(request.app.state, 'monitor'):
            raise HTTPException(status_code=500, detail="Monitor service not initialized")

        monitor = request.app.state.monitor
        is_online = await monitor.check_worker_heartbeat(worker_id)

        return {
            "worker_id": worker_id,
            "is_online": is_online
        }
    except Exception as e:
        logger.error(f"检查 Worker {worker_id} 心跳状态失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
