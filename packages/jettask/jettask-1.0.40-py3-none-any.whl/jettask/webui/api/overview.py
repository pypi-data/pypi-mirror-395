"""
概览模块 - 系统总览、健康检查和仪表板统计
提供轻量级的路由入口，业务逻辑在 OverviewService 中实现
"""
from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional, Dict, Any
import logging
import traceback

from jettask.schemas import (
    TimeRangeQuery,
    SystemStatsResponse,
    DashboardStatsResponse,
    TopQueuesResponse,
    DataResponse
)
from jettask.webui.services.overview_service import OverviewService

logger = logging.getLogger(__name__)

# 创建概览路由，添加 /overview 前缀
router = APIRouter(prefix="/overview", tags=["overview"])


# ============ 健康检查和根路径 ============

@router.get(
    "/",
    summary="API 根路径",
    description="获取 API 基本信息和健康状态",
    response_model=DataResponse,
    responses={
        200: {
            "description": "成功返回 API 信息",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": {
                            "service": "JetTask WebUI API",
                            "version": "v1",
                            "status": "running"
                        }
                    }
                }
            }
        }
    }
)
async def root() -> Dict[str, Any]:
    """
    ## API 根路径

    返回 API 的基本信息，包括服务名称、版本和运行状态。

    **用途**:
    - 健康检查
    - 验证 API 是否可用
    - 获取 API 版本信息
    """
    return OverviewService.get_root_info()


# ============ 系统统计 ============

@router.get(
    "/system-stats",
    summary="获取系统统计信息",
    description="获取指定命名空间的系统级统计数据，包括队列、任务、Worker 等关键指标",
    response_model=SystemStatsResponse,
    responses={
        200: {
            "description": "成功返回系统统计数据"
        },
        500: {
            "description": "服务器内部错误",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "获取系统统计信息失败: Database connection error"
                    }
                }
            }
        }
    }
)
async def get_system_stats(
    namespace: str = Path(..., description="命名空间名称，用于隔离不同环境或项目的数据", example="default")
) -> Dict[str, Any]:
    """
    ## 获取系统统计信息

    返回指定命名空间的关键系统指标，用于系统概览页面展示。

    **统计指标包括**:
    - 队列总数
    - 任务总数
    - 活跃 Worker 数量
    - 各状态任务数量（待处理、处理中、已完成、失败）

    **使用场景**:
    - 系统概览页面
    - 监控大屏展示
    - 系统健康度检查

    **示例请求**:
    ```bash
    curl -X GET "http://localhost:8001/api/v1/overview/system-stats/default"
    ```
    """
    try:
        return await OverviewService.get_system_stats(namespace)
    except Exception as e:
        logger.error(f"获取系统统计信息失败: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ============ 仪表板统计 ============

@router.get(
    "/dashboard-stats",
    summary="获取仪表板统计数据",
    description="获取仪表板展示所需的关键业务指标，支持按时间范围和队列过滤",
    response_model=DashboardStatsResponse,
    responses={
        200: {
            "description": "成功返回仪表板统计数据"
        },
        500: {
            "description": "服务器内部错误"
        }
    }
)
async def get_dashboard_stats(
    namespace: str = Path(..., description="命名空间名称", example="default"),
    time_range: str = Query(
        default="24h",
        description="时间范围，支持: 15m, 1h, 6h, 24h, 7d, 30d",
        example="24h",
        regex="^(15m|1h|6h|24h|7d|30d)$"
    ),
    queues: Optional[str] = Query(
        None,
        description="逗号分隔的队列名称列表，为空则统计所有队列",
        example="email_queue,sms_queue"
    )
) -> Dict[str, Any]:
    """
    ## 获取仪表板统计数据

    提供仪表板展示所需的核心业务指标，包括任务处理情况、成功率、吞吐量等。

    **统计指标包括**:
    - 任务总数
    - 成功任务数
    - 失败任务数
    - 成功率 (%)
    - 吞吐量 (任务/秒)
    - 平均处理时间 (秒)

    **时间范围说明**:
    - `15m`: 最近 15 分钟
    - `1h`: 最近 1 小时
    - `6h`: 最近 6 小时
    - `24h`: 最近 24 小时 (默认)
    - `7d`: 最近 7 天
    - `30d`: 最近 30 天

    **使用场景**:
    - 仪表板首页
    - 业务报表
    - 性能监控

    **示例请求**:
    ```bash
    # 获取默认命名空间最近24小时的统计
    curl -X GET "http://localhost:8001/api/v1/overview/dashboard-stats/default"

    # 获取指定队列最近1小时的统计
    curl -X GET "http://localhost:8001/api/v1/overview/dashboard-stats/default?time_range=1h&queues=email_queue,sms_queue"
    ```
    """
    try:
        return await OverviewService.get_dashboard_stats(namespace, time_range, queues)
    except Exception as e:
        logger.error(f"获取仪表板统计数据失败: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ============ 队列排行榜 ============

@router.get(
    "/top-queues",
    summary="获取队列排行榜",
    description="根据指定指标获取队列排行榜，支持积压数和错误率两种排序方式",
    response_model=TopQueuesResponse,
    responses={
        200: {
            "description": "成功返回队列排行榜"
        },
        400: {
            "description": "请求参数错误",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "无效的指标类型: invalid_metric，仅支持 backlog 或 error"
                    }
                }
            }
        },
        500: {
            "description": "服务器内部错误"
        }
    }
)
async def get_top_queues(
    namespace: str = Path(..., description="命名空间名称", example="default"),
    metric: str = Query(
        default="backlog",
        description="排序指标类型",
        example="backlog",
        regex="^(backlog|error)$"
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="返回的队列数量限制",
        example=10
    ),
    time_range: str = Query(
        default="24h",
        description="统计时间范围",
        example="24h",
        regex="^(15m|1h|6h|24h|7d|30d)$"
    ),
    queues: Optional[str] = Query(
        None,
        description="逗号分隔的队列名称列表，为空则统计所有队列",
        example="email_queue,sms_queue"
    )
) -> Dict[str, Any]:
    """
    ## 获取队列排行榜

    根据指定指标对队列进行排序，帮助快速识别需要关注的队列。

    **支持的指标类型**:
    - `backlog`: 按积压任务数排序（降序）
    - `error`: 按错误率排序（降序）

    **排行数据包括**:
    - 队列名称
    - 指标值
    - 排名

    **使用场景**:
    - 识别积压严重的队列
    - 发现错误率高的队列
    - 优化资源分配
    - 容量规划

    **示例请求**:
    ```bash
    # 获取积压最多的前10个队列
    curl -X GET "http://localhost:8001/api/v1/overview/top-queues/default?metric=backlog&limit=10"

    # 获取错误率最高的前5个队列
    curl -X GET "http://localhost:8001/api/v1/overview/top-queues/default?metric=error&limit=5"
    ```
    """
    try:
        return await OverviewService.get_top_queues(namespace, metric, limit, time_range, queues)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"获取队列排行榜失败: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))



# ============ 概览统计数据 ============

@router.post(
    "/dashboard-overview-stats",
    summary="获取概览页面统计数据",
    description="获取概览页面所需的时间序列统计数据，包括任务处理趋势、并发数量、处理时间等",
    response_model=Dict[str, Any],
    responses={
        200: {
            "description": "成功返回时间序列统计数据",
            "content": {
                "application/json": {
                    "example": {
                        "task_trend": [
                            {"timestamp": "2025-10-18T10:00:00Z", "completed": 120, "failed": 5},
                            {"timestamp": "2025-10-18T10:05:00Z", "completed": 135, "failed": 3}
                        ],
                        "concurrency": [
                            {"timestamp": "2025-10-18T10:00:00Z", "value": 15},
                            {"timestamp": "2025-10-18T10:05:00Z", "value": 18}
                        ],
                        "processing_time": [
                            {"timestamp": "2025-10-18T10:00:00Z", "avg": 2.3, "p50": 2.1, "p95": 4.5},
                            {"timestamp": "2025-10-18T10:05:00Z", "avg": 2.1, "p50": 1.9, "p95": 4.2}
                        ],
                        "creation_latency": [
                            {"timestamp": "2025-10-18T10:00:00Z", "avg": 0.5, "p95": 1.2}
                        ],
                        "granularity": "5m"
                    }
                }
            }
        },
        500: {
            "description": "服务器内部错误，返回空数据"
        }
    }
)
async def get_dashboard_overview_stats(
    namespace: str = Path(..., description="命名空间名称", example="default"),
    query: TimeRangeQuery = ...
) -> Dict[str, Any]:
    """
    ## 获取概览页面统计数据

    返回概览页面所需的时间序列统计数据，用于绘制趋势图表。

    **请求体参数**:
    ```json
    {
        "time_range": "1h",         // 可选: 时间范围（如 15m, 1h, 6h, 24h）
        "start_time": "2025-10-18T09:00:00Z",  // 可选: 开始时间（ISO格式）
        "end_time": "2025-10-18T10:00:00Z",    // 可选: 结束时间（ISO格式）
        "queue_name": "email_queue"  // 可选: 队列名称
    }
    ```

    **返回的时间序列数据**:
    - `task_trend`: 任务处理趋势（完成数、失败数）
    - `concurrency`: 任务并发数量
    - `processing_time`: 任务处理时间（平均值、P50、P95）
    - `creation_latency`: 任务创建延迟（平均值、P95）
    - `granularity`: 数据粒度（如 minute、5m、hour）

    **数据粒度说明**:
    - 时间范围 <= 1h: 粒度为 1分钟
    - 时间范围 <= 6h: 粒度为 5分钟
    - 时间范围 <= 24h: 粒度为 15分钟
    - 时间范围 > 24h: 粒度为 1小时

    **使用场景**:
    - 概览页面趋势图
    - 性能监控图表
    - 实时数据看板

    **示例请求**:
    ```bash
    curl -X POST "http://localhost:8001/api/v1/overview/dashboard-overview-stats/default" \\
      -H "Content-Type: application/json" \\
      -d '{"time_range": "1h", "queue_name": "email_queue"}'
    ```
    """
    try:
        return await OverviewService.get_dashboard_overview_stats(namespace, query)
    except Exception as e:
        logger.error(f"获取概览统计数据失败: {e}")
        traceback.print_exc()
        # 返回空数据而不是抛出异常
        return {
            "task_trend": [],
            "concurrency": [],
            "processing_time": [],
            "creation_latency": [],
            "granularity": "minute"
        }


__all__ = ['router']