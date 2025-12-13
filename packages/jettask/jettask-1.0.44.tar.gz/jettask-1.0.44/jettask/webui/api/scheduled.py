"""
定时任务模块 - 定时任务管理、执行和监控
提供轻量级的路由入口，业务逻辑在 ScheduledTaskService 中实现
"""
from fastapi import APIRouter, HTTPException, Request, Query
from typing import Optional
import logging

from jettask.schemas import ScheduledTaskRequest
from jettask.webui.services.scheduled_task_service import ScheduledTaskService

router = APIRouter(prefix="/scheduled", tags=["scheduled"])
logger = logging.getLogger(__name__)


# ============ 定时任务管理 ============

@router.get(
    "/",
    summary="获取定时任务列表",
    description="获取定时任务列表，支持分页、搜索和状态筛选",
    responses={
        200: {
            "description": "成功返回定时任务列表",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": [
                            {
                                "id": "task-001",
                                "name": "每日数据统计",
                                "namespace": "default",
                                "queue_name": "stat_queue",
                                "schedule_type": "cron",
                                "schedule_config": {"cron": "0 0 * * *"},
                                "is_active": True,
                                "next_run_time": "2025-10-19T00:00:00Z"
                            }
                        ],
                        "total": 50,
                        "page": 1,
                        "page_size": 20
                    }
                }
            }
        },
        500: {"description": "服务器内部错误"}
    }
)
async def get_scheduled_tasks(
    request: Request,
    page: int = Query(1, ge=1, description="页码，从 1 开始", example=1),
    page_size: int = Query(20, ge=1, le=100, description="每页数量，范围 1-100", example=20),
    search: Optional[str] = Query(None, description="搜索关键字，支持按名称、描述搜索", example="数据统计"),
    is_active: Optional[bool] = Query(None, description="是否只返回激活的任务", example=True)
):
    """
    ## 获取定时任务列表

    获取系统中所有定时任务的列表，支持分页、搜索和按状态筛选。

    **返回信息包括**:
    - 任务 ID 和名称
    - 命名空间和队列名称
    - 调度类型和配置
    - 激活状态
    - 下次执行时间
    - 创建和更新时间

    **调度类型**:
    - `cron`: Cron 表达式调度
    - `interval`: 固定间隔调度
    - `date`: 指定时间调度
    - `every`: 周期性调度

    **使用场景**:
    - 定时任务管理页面
    - 任务列表查看
    - 任务搜索和筛选

    **示例请求**:
    ```bash
    # 获取所有定时任务
    curl -X GET "http://localhost:8001/api/v1/scheduled/?page=1&page_size=20"

    # 搜索特定任务
    curl -X GET "http://localhost:8001/api/v1/scheduled/?search=数据统计"

    # 只获取激活的任务
    curl -X GET "http://localhost:8001/api/v1/scheduled/?is_active=true"
    ```

    **注意事项**:
    - 分页从 1 开始
    - 搜索支持模糊匹配
    - 返回结果按创建时间倒序排列

    Args:
        page: 页码（从1开始）
        page_size: 每页数量
        search: 搜索关键字
        is_active: 是否激活
    """
    try:
        app = request.app
        if not app or not hasattr(app.state, 'data_access'):
            raise HTTPException(status_code=500, detail="Data access not initialized")
        
        data_access = app.state.data_access
        
        async with data_access.get_session() as session:
            tasks, total = await data_access.fetch_scheduled_tasks(
                session=session,
                page=page,
                page_size=page_size,
                search=search,
                is_active=is_active
            )
        
        return {
            "success": True,
            "data": tasks,
            "total": total,
            "page": page,
            "page_size": page_size
        }
    except Exception as e:
        logger.error(f"获取定时任务列表失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/filter",
    summary="获取定时任务列表（高级筛选）",
    description="获取定时任务列表，支持高级筛选条件、时间范围查询和多维度过滤",
    responses={
        200: {
            "description": "成功返回筛选后的定时任务列表",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": [
                            {
                                "id": "task-001",
                                "name": "每日数据统计",
                                "namespace": "default",
                                "queue_name": "stat_queue",
                                "schedule_type": "cron",
                                "schedule_config": {"cron": "0 0 * * *"},
                                "is_active": True,
                                "next_run_time": "2025-10-19T00:00:00Z"
                            }
                        ],
                        "total": 50,
                        "page": 1,
                        "page_size": 20
                    }
                }
            }
        },
        400: {
            "description": "请求参数错误",
            "content": {
                "application/json": {
                    "example": {"detail": "时间范围参数无效"}
                }
            }
        },
        500: {"description": "服务器内部错误"}
    }
)
async def get_scheduled_tasks_with_filters(request: Request):
    """
    ## 获取定时任务列表（支持高级筛选）

    获取定时任务列表，支持多维度筛选条件、时间范围查询和复杂过滤逻辑。

    **请求体参数**:
    ```json
    {
        "page": 1,
        "page_size": 20,
        "search": "数据统计",
        "is_active": true,
        "filters": [
            {
                "field": "schedule_type",
                "operator": "eq",
                "value": "cron"
            },
            {
                "field": "namespace",
                "operator": "in",
                "value": ["default", "production"]
            }
        ],
        "time_range": "7d",
        "start_time": "2025-10-12T00:00:00Z",
        "end_time": "2025-10-19T23:59:59Z"
    }
    ```

    **筛选器支持的字段**:
    - `schedule_type`: 调度类型（cron/interval/date/every）
    - `namespace`: 命名空间
    - `queue_name`: 队列名称
    - `is_active`: 激活状态
    - `created_at`: 创建时间

    **筛选器支持的操作符**:
    - `eq`: 等于
    - `ne`: 不等于
    - `in`: 包含于列表
    - `gt`: 大于
    - `lt`: 小于
    - `gte`: 大于等于
    - `lte`: 小于等于

    **时间范围快捷值**:
    - `1h`: 最近1小时
    - `24h`: 最近24小时
    - `7d`: 最近7天
    - `30d`: 最近30天
    - `custom`: 自定义时间范围（需配合 start_time 和 end_time）

    **返回信息包括**:
    - 筛选后的任务列表
    - 总数和分页信息
    - 每个任务的完整配置

    **使用场景**:
    - 高级任务搜索
    - 多条件组合查询
    - 时间范围分析
    - 任务统计报表

    **示例请求**:
    ```bash
    # 查询最近7天创建的激活任务
    curl -X POST "http://localhost:8001/api/v1/scheduled/filter" \\
      -H "Content-Type: application/json" \\
      -d '{
        "page": 1,
        "page_size": 20,
        "is_active": true,
        "time_range": "7d"
      }'

    # 多条件组合查询
    curl -X POST "http://localhost:8001/api/v1/scheduled/filter" \\
      -H "Content-Type: application/json" \\
      -d '{
        "page": 1,
        "page_size": 20,
        "filters": [
          {
            "field": "schedule_type",
            "operator": "eq",
            "value": "cron"
          },
          {
            "field": "namespace",
            "operator": "in",
            "value": ["default", "production"]
          }
        ]
      }'

    # 自定义时间范围查询
    curl -X POST "http://localhost:8001/api/v1/scheduled/filter" \\
      -H "Content-Type: application/json" \\
      -d '{
        "page": 1,
        "page_size": 20,
        "time_range": "custom",
        "start_time": "2025-10-12T00:00:00Z",
        "end_time": "2025-10-19T23:59:59Z"
      }'
    ```

    **注意事项**:
    - 所有筛选条件之间为 AND 关系
    - 时间范围查询基于任务创建时间
    - 使用 custom 时间范围时，必须同时提供 start_time 和 end_time
    - 筛选器数组为空时等同于不使用筛选器
    """
    try:
        app = request.app
        if not app or not hasattr(app.state, 'data_access'):
            raise HTTPException(status_code=500, detail="Data access not initialized")
        
        data_access = app.state.data_access
        
        # 解析请求体
        body = await request.json()
        
        page = body.get('page', 1)
        page_size = body.get('page_size', 20)
        search = body.get('search')
        is_active = body.get('is_active')
        filters = body.get('filters', [])
        time_range = body.get('time_range')
        start_time = body.get('start_time')
        end_time = body.get('end_time')
        
        async with data_access.get_session() as session:
            tasks, total = await data_access.fetch_scheduled_tasks(
                session=session,
                page=page,
                page_size=page_size,
                search=search,
                is_active=is_active,
                filters=filters,
                time_range=time_range,
                start_time=start_time,
                end_time=end_time
            )
        
        return {
            "success": True,
            "data": tasks,
            "total": total,
            "page": page,
            "page_size": page_size
        }
    except Exception as e:
        logger.error(f"获取定时任务列表失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/",
    summary="创建定时任务",
    description="创建一个新的定时任务，支持多种调度类型和配置选项",
    status_code=201,
    responses={
        201: {
            "description": "定时任务创建成功",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": {
                            "id": "task-001",
                            "name": "每日数据统计",
                            "namespace": "default",
                            "queue_name": "stat_queue",
                            "schedule_type": "cron",
                            "schedule_config": {"cron": "0 0 * * *"},
                            "is_active": True,
                            "created_at": "2025-10-19T12:00:00Z"
                        },
                        "message": "定时任务创建成功"
                    }
                }
            }
        },
        400: {
            "description": "请求参数错误",
            "content": {
                "application/json": {
                    "example": {"detail": "调度配置无效: Cron表达式格式错误"}
                }
            }
        },
        500: {"description": "服务器内部错误"}
    }
)
async def create_scheduled_task(request: Request, task_request: ScheduledTaskRequest):
    """
    ## 创建定时任务

    创建一个新的定时任务，用于自动化执行周期性或定时的业务逻辑。

    **调度类型说明**:
    1. **cron**: 使用 Cron 表达式定义复杂的调度规则
       - 格式: `秒 分 时 日 月 周`
       - 示例: `0 0 * * *` (每天零点执行)
       - 支持标准 Cron 语法和扩展语法

    2. **interval**: 固定时间间隔执行
       - 以秒为单位的间隔时间
       - 适用于简单的周期性任务
       - 示例: `3600` (每小时执行一次)

    3. **date**: 指定具体日期时间执行一次
       - 用于一次性定时任务
       - 示例: `2025-12-31T23:59:59Z`

    4. **every**: 周期性执行（语义化表达）
       - 支持: seconds, minutes, hours, days, weeks
       - 示例: `{"value": 30, "unit": "minutes"}`

    **请求体参数**:
    ```json
    {
        "namespace": "default",
        "name": "每日数据统计",
        "queue_name": "stat_queue",
        "task_data": {
            "function": "tasks.daily_statistics",
            "args": [],
            "kwargs": {"date": "today"}
        },
        "schedule_type": "cron",
        "schedule_config": {
            "cron": "0 0 * * *",
            "timezone": "Asia/Shanghai"
        },
        "is_active": true,
        "description": "每天零点执行数据统计任务",
        "max_retry": 3,
        "timeout": 300
    }
    ```

    **配置参数说明**:
    - `namespace`: 命名空间（默认: default）
    - `name`: 任务名称（必填，唯一标识）
    - `queue_name`: 目标队列名称
    - `task_data`: 任务执行数据（function、args、kwargs）
    - `schedule_type`: 调度类型（cron/interval/date/every）
    - `schedule_config`: 调度配置（根据类型不同而不同）
    - `is_active`: 是否立即启用（默认: true）
    - `description`: 任务描述
    - `max_retry`: 最大重试次数（默认: 3）
    - `timeout`: 超时时间（秒，默认: 300）

    **返回信息包括**:
    - 任务 ID 和基本信息
    - 调度配置
    - 下次执行时间
    - 创建时间

    **使用场景**:
    - 定期数据统计和报表
    - 自动化备份任务
    - 定时清理和维护
    - 周期性数据同步
    - 定时消息推送

    **示例请求**:
    ```bash
    # 创建 Cron 定时任务
    curl -X POST "http://localhost:8001/api/v1/scheduled/" \\
      -H "Content-Type: application/json" \\
      -d '{
        "namespace": "default",
        "name": "每日数据统计",
        "queue_name": "stat_queue",
        "task_data": {
          "function": "tasks.daily_statistics",
          "args": [],
          "kwargs": {"date": "today"}
        },
        "schedule_type": "cron",
        "schedule_config": {
          "cron": "0 0 * * *",
          "timezone": "Asia/Shanghai"
        },
        "is_active": true,
        "description": "每天零点执行数据统计",
        "max_retry": 3,
        "timeout": 300
      }'

    # 创建固定间隔任务
    curl -X POST "http://localhost:8001/api/v1/scheduled/" \\
      -H "Content-Type: application/json" \\
      -d '{
        "namespace": "default",
        "name": "健康检查",
        "queue_name": "health_queue",
        "task_data": {
          "function": "tasks.health_check",
          "args": [],
          "kwargs": {}
        },
        "schedule_type": "interval",
        "schedule_config": {
          "interval": 60
        },
        "is_active": true,
        "description": "每分钟执行健康检查",
        "max_retry": 1,
        "timeout": 30
      }'

    # 创建一次性定时任务
    curl -X POST "http://localhost:8001/api/v1/scheduled/" \\
      -H "Content-Type: application/json" \\
      -d '{
        "namespace": "default",
        "name": "年度报表生成",
        "queue_name": "report_queue",
        "task_data": {
          "function": "tasks.generate_annual_report",
          "args": [2025],
          "kwargs": {}
        },
        "schedule_type": "date",
        "schedule_config": {
          "run_date": "2025-12-31T23:59:00Z"
        },
        "is_active": true,
        "description": "年底生成年度报表"
      }'
    ```

    **注意事项**:
    - 任务名称在同一命名空间内必须唯一
    - Cron 表达式会在创建时验证格式
    - 确保目标队列已存在且可用
    - 任务函数路径必须可导入
    - 时区默认为 UTC，建议明确指定
    - 创建后任务会根据调度配置自动计算下次执行时间
    - 如果 is_active 为 false，任务不会自动执行
    """
    try:
        app = request.app
        if not app or not hasattr(app.state, 'data_access'):
            raise HTTPException(status_code=500, detail="Data access not initialized")
        
        data_access = app.state.data_access
        
        # 验证调度配置
        ScheduledTaskService.validate_schedule_config(
            task_request.schedule_type, 
            task_request.schedule_config
        )
        
        task_data = {
            "namespace": task_request.namespace,
            "name": task_request.name,
            "queue_name": task_request.queue_name,
            "task_data": task_request.task_data,
            "schedule_type": task_request.schedule_type,
            "schedule_config": task_request.schedule_config,
            "is_active": task_request.is_active,
            "description": task_request.description,
            "max_retry": task_request.max_retry,
            "timeout": task_request.timeout
        }
        
        async with data_access.get_session() as session:
            task = await data_access.create_scheduled_task(session, task_data)
        
        return {
            "success": True,
            "data": task,
            "message": "定时任务创建成功"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"创建定时任务失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/{task_id}",
    summary="更新定时任务",
    description="更新指定定时任务的配置信息，支持部分更新",
    responses={
        200: {
            "description": "定时任务更新成功",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": {
                            "id": "task-001",
                            "name": "每日数据统计（已更新）",
                            "namespace": "default",
                            "queue_name": "stat_queue",
                            "schedule_type": "cron",
                            "schedule_config": {"cron": "0 1 * * *"},
                            "is_active": True,
                            "updated_at": "2025-10-19T12:30:00Z"
                        },
                        "message": "定时任务更新成功"
                    }
                }
            }
        },
        400: {
            "description": "请求参数错误",
            "content": {
                "application/json": {
                    "example": {"detail": "调度配置无效"}
                }
            }
        },
        404: {
            "description": "任务不存在",
            "content": {
                "application/json": {
                    "example": {"detail": "定时任务不存在"}
                }
            }
        },
        500: {"description": "服务器内部错误"}
    }
)
async def update_scheduled_task(request: Request, task_id: str, task_request: ScheduledTaskRequest):
    """
    ## 更新定时任务

    更新指定定时任务的配置信息，可以修改调度规则、任务数据、执行参数等。

    **可更新的字段**:
    - 任务名称和描述
    - 命名空间和队列名称
    - 调度类型和配置
    - 任务执行数据（function、args、kwargs）
    - 启用状态
    - 重试次数和超时时间

    **请求体参数**:
    ```json
    {
        "namespace": "default",
        "name": "每日数据统计（已更新）",
        "queue_name": "stat_queue",
        "task_data": {
            "function": "tasks.daily_statistics",
            "args": [],
            "kwargs": {"date": "today", "format": "detailed"}
        },
        "schedule_type": "cron",
        "schedule_config": {
            "cron": "0 1 * * *",
            "timezone": "Asia/Shanghai"
        },
        "is_active": true,
        "description": "每天凌晨1点执行详细数据统计",
        "max_retry": 5,
        "timeout": 600
    }
    ```

    **返回信息包括**:
    - 更新后的完整任务信息
    - 新的下次执行时间
    - 更新时间戳

    **使用场景**:
    - 调整任务执行时间
    - 修改任务参数
    - 更新调度策略
    - 临时禁用或启用任务
    - 调整超时和重试配置

    **示例请求**:
    ```bash
    # 更新任务执行时间
    curl -X PUT "http://localhost:8001/api/v1/scheduled/task-001" \\
      -H "Content-Type: application/json" \\
      -d '{
        "namespace": "default",
        "name": "每日数据统计",
        "queue_name": "stat_queue",
        "task_data": {
          "function": "tasks.daily_statistics",
          "args": [],
          "kwargs": {"date": "today"}
        },
        "schedule_type": "cron",
        "schedule_config": {
          "cron": "0 1 * * *",
          "timezone": "Asia/Shanghai"
        },
        "is_active": true,
        "description": "调整为凌晨1点执行"
      }'

    # 修改为间隔调度
    curl -X PUT "http://localhost:8001/api/v1/scheduled/task-001" \\
      -H "Content-Type: application/json" \\
      -d '{
        "namespace": "default",
        "name": "数据统计",
        "queue_name": "stat_queue",
        "task_data": {
          "function": "tasks.statistics",
          "args": [],
          "kwargs": {}
        },
        "schedule_type": "interval",
        "schedule_config": {
          "interval": 7200
        },
        "is_active": true,
        "description": "改为每2小时执行一次"
      }'

    # 更新任务参数
    curl -X PUT "http://localhost:8001/api/v1/scheduled/task-001" \\
      -H "Content-Type: application/json" \\
      -d '{
        "namespace": "default",
        "name": "每日数据统计",
        "queue_name": "stat_queue",
        "task_data": {
          "function": "tasks.daily_statistics",
          "args": [],
          "kwargs": {
            "date": "today",
            "include_details": true,
            "send_email": true
          }
        },
        "schedule_type": "cron",
        "schedule_config": {
          "cron": "0 0 * * *",
          "timezone": "Asia/Shanghai"
        },
        "is_active": true,
        "description": "增加邮件通知功能"
      }'
    ```

    **注意事项**:
    - 所有字段都必须提供完整值（非部分更新）
    - 更新调度配置后会重新计算下次执行时间
    - 如果任务正在执行，更新会在执行完成后生效
    - 修改 schedule_type 时必须同时提供对应的 schedule_config
    - 更新后的任务名称不能与其他任务重复
    - 调度配置会立即验证，无效配置会返回 400 错误
    """
    try:
        app = request.app
        if not app or not hasattr(app.state, 'data_access'):
            raise HTTPException(status_code=500, detail="Data access not initialized")
        
        data_access = app.state.data_access
        
        # 验证调度配置
        ScheduledTaskService.validate_schedule_config(
            task_request.schedule_type,
            task_request.schedule_config
        )
        
        task_data = {
            "namespace": task_request.namespace,
            "name": task_request.name,
            "queue_name": task_request.queue_name,
            "task_data": task_request.task_data,
            "schedule_type": task_request.schedule_type,
            "schedule_config": task_request.schedule_config,
            "is_active": task_request.is_active,
            "description": task_request.description,
            "max_retry": task_request.max_retry,
            "timeout": task_request.timeout
        }
        
        async with data_access.get_session() as session:
            task = await data_access.update_scheduled_task(session, task_id, task_data)
        
        return {
            "success": True,
            "data": task,
            "message": "定时任务更新成功"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"更新定时任务失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/{task_id}",
    summary="删除定时任务",
    description="删除指定的定时任务，操作不可逆",
    responses={
        200: {
            "description": "定时任务删除成功",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "定时任务 task-001 已删除"
                    }
                }
            }
        },
        404: {
            "description": "任务不存在",
            "content": {
                "application/json": {
                    "example": {"detail": "定时任务不存在"}
                }
            }
        },
        500: {"description": "服务器内部错误"}
    }
)
async def delete_scheduled_task(request: Request, task_id: str):
    """
    ## 删除定时任务

    删除指定的定时任务，包括任务配置和调度信息。

    **删除影响**:
    - 任务配置将被永久删除
    - 调度器将停止该任务的自动执行
    - 任务执行历史仍会保留（不会删除）
    - 如果任务正在执行，不会中断当前执行

    **返回信息包括**:
    - 操作成功标识
    - 删除确认消息

    **使用场景**:
    - 清理不再需要的定时任务
    - 移除测试任务
    - 任务下线
    - 系统维护和清理

    **示例请求**:
    ```bash
    # 删除指定定时任务
    curl -X DELETE "http://localhost:8001/api/v1/scheduled/task-001"
    ```

    **注意事项**:
    - 删除操作不可逆，请谨慎操作
    - 建议删除前先禁用任务，观察一段时间
    - 如果任务正在执行，删除后不会中断当前执行
    - 任务的历史执行记录不会被删除
    - 删除失败时会返回 404 错误
    - 建议在删除前导出重要的任务配置
    """
    try:
        app = request.app
        if not app or not hasattr(app.state, 'data_access'):
            raise HTTPException(status_code=500, detail="Data access not initialized")
        
        data_access = app.state.data_access
        
        async with data_access.get_session() as session:
            success = await data_access.delete_scheduled_task(session, task_id)
        
        if success:
            return {
                "success": True,
                "message": f"定时任务 {task_id} 已删除"
            }
        else:
            raise HTTPException(status_code=404, detail="定时任务不存在")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除定时任务失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/{task_id}/toggle",
    summary="启用/禁用定时任务",
    description="切换定时任务的启用状态，启用的任务会自动执行，禁用的任务会暂停调度",
    responses={
        200: {
            "description": "任务状态切换成功",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": {
                            "id": "task-001",
                            "is_active": False
                        },
                        "message": "定时任务状态已更新"
                    }
                }
            }
        },
        404: {
            "description": "任务不存在",
            "content": {
                "application/json": {
                    "example": {"detail": "定时任务不存在"}
                }
            }
        },
        500: {"description": "服务器内部错误"}
    }
)
async def toggle_scheduled_task(request: Request, task_id: str):
    """
    ## 启用/禁用定时任务

    切换定时任务的启用状态，用于快速暂停或恢复任务的自动执行。

    **状态说明**:
    - **启用（is_active=true）**: 任务会按照调度配置自动执行
    - **禁用（is_active=false）**: 任务暂停调度，不会自动执行

    **操作特点**:
    - 切换操作是幂等的（启用状态下再次启用不会报错）
    - 禁用任务不会中断正在执行的实例
    - 启用任务会立即重新计算下次执行时间
    - 保留所有任务配置和历史记录

    **返回信息包括**:
    - 任务 ID
    - 更新后的启用状态
    - 操作确认消息

    **使用场景**:
    - 临时暂停任务执行
    - 维护期间禁用定时任务
    - 快速恢复任务调度
    - 测试和调试
    - 紧急情况下快速停止任务

    **示例请求**:
    ```bash
    # 切换任务状态（启用↔禁用）
    curl -X POST "http://localhost:8001/api/v1/scheduled/task-001/toggle"
    ```

    **工作流示例**:
    ```bash
    # 场景1: 维护期间暂停任务
    # 1. 禁用任务
    curl -X POST "http://localhost:8001/api/v1/scheduled/task-001/toggle"
    # 2. 执行系统维护
    # 3. 维护完成后恢复任务
    curl -X POST "http://localhost:8001/api/v1/scheduled/task-001/toggle"

    # 场景2: 配合更新操作
    # 1. 先禁用任务
    curl -X POST "http://localhost:8001/api/v1/scheduled/task-001/toggle"
    # 2. 更新任务配置
    curl -X PUT "http://localhost:8001/api/v1/scheduled/task-001" \\
      -H "Content-Type: application/json" \\
      -d '{...}'
    # 3. 测试无误后启用任务
    curl -X POST "http://localhost:8001/api/v1/scheduled/task-001/toggle"
    ```

    **注意事项**:
    - 禁用任务不会删除任务配置
    - 禁用期间的执行历史仍会保留
    - 启用后会从当前时间重新计算下次执行时间
    - 如果任务正在执行，禁用操作不会中断当前执行
    - 频繁切换状态不会影响任务的正常运行
    """
    try:
        app = request.app
        if not app or not hasattr(app.state, 'data_access'):
            raise HTTPException(status_code=500, detail="Data access not initialized")
        
        data_access = app.state.data_access
        
        async with data_access.get_session() as session:
            task = await data_access.toggle_scheduled_task(session, task_id)
        
        if task:
            return {
                "success": True,
                "data": {
                    "id": task["id"],
                    "is_active": task["enabled"]  # 映射 enabled 到 is_active
                },
                "message": "定时任务状态已更新"
            }
        else:
            raise HTTPException(status_code=404, detail="定时任务不存在")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"切换定时任务状态失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/{task_id}/execute",
    summary="立即执行定时任务",
    description="手动触发定时任务立即执行一次，不影响原有调度计划",
    responses={
        200: {
            "description": "任务已加入执行队列",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": {
                            "task_id": "task-001",
                            "job_id": "job-123456",
                            "queue_name": "stat_queue",
                            "status": "queued"
                        },
                        "message": "定时任务已加入执行队列"
                    }
                }
            }
        },
        400: {
            "description": "请求参数错误",
            "content": {
                "application/json": {
                    "example": {"detail": "任务已禁用，无法执行"}
                }
            }
        },
        404: {
            "description": "任务不存在",
            "content": {
                "application/json": {
                    "example": {"detail": "定时任务不存在"}
                }
            }
        },
        500: {"description": "服务器内部错误"}
    }
)
async def execute_scheduled_task_now(request: Request, task_id: str):
    """
    ## 立即执行定时任务

    手动触发定时任务立即执行一次，用于测试、紧急执行或补偿性执行。

    **执行特点**:
    - 不影响原有的调度计划
    - 任务会立即加入执行队列
    - 可以多次手动触发（不受调度限制）
    - 禁用状态的任务也可以手动执行
    - 执行结果会记录到执行历史

    **执行流程**:
    1. 验证任务是否存在
    2. 读取任务配置（function、args、kwargs）
    3. 创建执行任务并加入队列
    4. 返回任务 ID 和队列信息
    5. 后台 Worker 异步执行任务

    **返回信息包括**:
    - 定时任务 ID
    - 执行任务 ID（job_id）
    - 目标队列名称
    - 任务状态（queued）

    **使用场景**:
    - 测试定时任务配置
    - 紧急执行未到时间的任务
    - 补偿执行失败的任务
    - 手动触发数据处理
    - 调试和故障排查

    **示例请求**:
    ```bash
    # 立即执行定时任务
    curl -X POST "http://localhost:8001/api/v1/scheduled/task-001/execute"
    ```

    **应用场景示例**:
    ```bash
    # 场景1: 测试新创建的定时任务
    # 1. 创建定时任务
    curl -X POST "http://localhost:8001/api/v1/scheduled/" \\
      -H "Content-Type: application/json" \\
      -d '{
        "name": "每日报表",
        "schedule_type": "cron",
        "schedule_config": {"cron": "0 0 * * *"},
        ...
      }'
    # 2. 立即执行测试
    curl -X POST "http://localhost:8001/api/v1/scheduled/task-001/execute"

    # 场景2: 紧急执行数据处理
    # 1. 查看任务状态
    curl -X GET "http://localhost:8001/api/v1/scheduled/?search=数据处理"
    # 2. 立即执行
    curl -X POST "http://localhost:8001/api/v1/scheduled/task-001/execute"
    # 3. 查看执行历史
    curl -X GET "http://localhost:8001/api/v1/scheduled/task-001/history"

    # 场景3: 补偿执行失败任务
    # 1. 查看失败历史
    curl -X GET "http://localhost:8001/api/v1/scheduled/task-001/history"
    # 2. 修复问题后重新执行
    curl -X POST "http://localhost:8001/api/v1/scheduled/task-001/execute"
    ```

    **注意事项**:
    - 立即执行不会影响下次调度时间
    - 任务会按照配置的 max_retry 和 timeout 参数执行
    - 如果队列积压严重，可能需要等待一段时间才能执行
    - 即使任务被禁用，仍然可以手动执行
    - 执行结果可以通过执行历史接口查询
    - 频繁手动执行可能导致队列积压，请谨慎使用
    - 返回 200 状态码仅表示任务已加入队列，不代表执行成功
    """
    try:
        app = request.app
        if not app or not hasattr(app.state, 'data_access'):
            raise HTTPException(status_code=500, detail="Data access not initialized")
        
        if not hasattr(app.state, 'namespace_data_access'):
            raise HTTPException(status_code=500, detail="Namespace data access not initialized")
        
        data_access = app.state.data_access
        namespace_data_access = app.state.namespace_data_access
        
        # 调用服务层执行任务
        result = await ScheduledTaskService.execute_task_now(
            data_access,
            namespace_data_access,
            task_id
        )
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"执行定时任务失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============ 执行历史和统计 ============

# 注意：/{task_id}/history 端点已被移除，因为 task_execution_history 表已废弃
# 如需查看定时任务的执行历史，请使用 task_runs 表和相关的队列任务查询接口

@router.get(
    "/{task_id}/trend",
    summary="获取定时任务执行趋势",
    description="获取指定定时任务的执行趋势数据，用于可视化分析和监控",
    responses={
        200: {
            "description": "成功返回执行趋势数据",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": {
                            "task_id": "task-001",
                            "time_points": [
                                "2025-10-13T00:00:00Z",
                                "2025-10-14T00:00:00Z",
                                "2025-10-15T00:00:00Z",
                                "2025-10-16T00:00:00Z",
                                "2025-10-17T00:00:00Z",
                                "2025-10-18T00:00:00Z",
                                "2025-10-19T00:00:00Z"
                            ],
                            "success_count": [10, 12, 11, 13, 12, 14, 15],
                            "failed_count": [1, 0, 2, 0, 1, 0, 0],
                            "avg_duration": [320, 315, 330, 310, 325, 318, 312],
                            "total_executions": 91,
                            "success_rate": 95.6
                        },
                        "time_range": "7d"
                    }
                }
            }
        },
        400: {
            "description": "请求参数错误",
            "content": {
                "application/json": {
                    "example": {"detail": "无效的时间范围参数"}
                }
            }
        },
        404: {
            "description": "任务不存在",
            "content": {
                "application/json": {
                    "example": {"detail": "定时任务不存在"}
                }
            }
        },
        500: {"description": "服务器内部错误"}
    }
)
async def get_scheduled_task_execution_trend(
    request: Request,
    task_id: str,
    time_range: str = Query("7d", description="时间范围，支持: 1h, 24h, 7d, 30d, 90d", example="7d")
):
    """
    ## 获取定时任务执行趋势

    获取指定定时任务在特定时间范围内的执行趋势数据，用于监控和分析任务执行情况。

    **返回数据包括**:
    - 时间点序列（X 轴）
    - 成功执行次数（按时间点统计）
    - 失败执行次数（按时间点统计）
    - 平均执行时长（秒，按时间点统计）
    - 总执行次数
    - 成功率（百分比）

    **时间范围参数**:
    - `1h`: 最近1小时（按分钟聚合）
    - `24h`: 最近24小时（按小时聚合）
    - `7d`: 最近7天（按天聚合）
    - `30d`: 最近30天（按天聚合）
    - `90d`: 最近90天（按周聚合）

    **数据聚合规则**:
    - 1小时范围：按分钟聚合，返回60个数据点
    - 24小时范围：按小时聚合，返回24个数据点
    - 7天范围：按天聚合，返回7个数据点
    - 30天范围：按天聚合，返回30个数据点
    - 90天范围：按周聚合，返回13个数据点

    **使用场景**:
    - 任务执行情况可视化
    - 性能趋势分析
    - 故障模式识别
    - 容量规划
    - SLA 监控

    **示例请求**:
    ```bash
    # 查看最近7天的执行趋势
    curl -X GET "http://localhost:8001/api/v1/scheduled/task-001/trend?time_range=7d"

    # 查看最近24小时的执行趋势
    curl -X GET "http://localhost:8001/api/v1/scheduled/task-001/trend?time_range=24h"

    # 查看最近30天的执行趋势
    curl -X GET "http://localhost:8001/api/v1/scheduled/task-001/trend?time_range=30d"
    ```

    **数据可视化示例**:
    ```bash
    # 获取趋势数据并用于图表展示
    curl -X GET "http://localhost:8001/api/v1/scheduled/task-001/trend?time_range=7d" \\
      | jq '.data'

    # 返回的数据可以直接用于前端图表库（如 ECharts、Chart.js）
    # X轴: time_points
    # Y轴（折线图1）: success_count (成功次数)
    # Y轴（折线图2）: failed_count (失败次数)
    # Y轴（折线图3）: avg_duration (平均时长)
    ```

    **配合其他接口使用**:
    ```bash
    # 1. 查看任务列表
    curl -X GET "http://localhost:8001/api/v1/scheduled/"

    # 2. 查看执行趋势（发现异常）
    curl -X GET "http://localhost:8001/api/v1/scheduled/task-001/trend?time_range=7d"

    # 3. 查看详细执行历史
    curl -X GET "http://localhost:8001/api/v1/scheduled/task-001/history"

    # 4. 如果发现问题，更新任务配置
    curl -X PUT "http://localhost:8001/api/v1/scheduled/task-001" \\
      -H "Content-Type: application/json" \\
      -d '{...}'
    ```

    **注意事项**:
    - 时间范围参数必须是支持的值之一
    - 趋势数据基于历史执行记录计算
    - 如果时间范围内没有执行记录，对应数据点为 0
    - 平均时长只计算成功执行的任务
    - 成功率 = (成功次数 / 总执行次数) × 100%
    - 数据会实时计算，可能有轻微延迟
    """
    try:
        app = request.app
        if not app or not hasattr(app.state, 'data_access'):
            raise HTTPException(status_code=500, detail="Data access not initialized")
        
        data_access = app.state.data_access
        
        async with data_access.get_session() as session:
            data = await data_access.fetch_task_execution_trend(
                session=session,
                task_id=task_id,
                time_range=time_range
            )
        
        return {
            "success": True,
            "data": data,
            "time_range": time_range
        }
    except Exception as e:
        logger.error(f"获取定时任务执行趋势失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/statistics",
    summary="获取定时任务统计数据",
    description="获取指定命名空间下所有定时任务的统计数据和概览信息",
    responses={
        200: {
            "description": "成功返回统计数据",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": {
                            "namespace": "default",
                            "total_tasks": 25,
                            "active_tasks": 18,
                            "inactive_tasks": 7,
                            "total_executions_today": 156,
                            "successful_executions_today": 148,
                            "failed_executions_today": 8,
                            "success_rate_today": 94.9,
                            "avg_execution_duration": 285,
                            "next_executions": [
                                {
                                    "task_id": "task-001",
                                    "task_name": "每日数据统计",
                                    "next_run_time": "2025-10-20T00:00:00Z"
                                },
                                {
                                    "task_id": "task-002",
                                    "task_name": "健康检查",
                                    "next_run_time": "2025-10-19T13:00:00Z"
                                }
                            ],
                            "task_type_distribution": {
                                "cron": 15,
                                "interval": 8,
                                "date": 2
                            }
                        }
                    }
                }
            }
        },
        404: {
            "description": "命名空间不存在",
            "content": {
                "application/json": {
                    "example": {"detail": "命名空间 'production' 不存在"}
                }
            }
        },
        500: {"description": "服务器内部错误"}
    }
)
async def get_scheduled_tasks_statistics(request: Request, namespace: str):
    """
    ## 获取定时任务统计数据

    获取指定命名空间下所有定时任务的统计信息和运行概览。

    **统计数据包括**:
    - 任务总数、活跃任务数、非活跃任务数
    - 今日执行总次数、成功次数、失败次数
    - 今日成功率（百分比）
    - 平均执行时长（秒）
    - 即将执行的任务列表（最近5个）
    - 任务类型分布（cron/interval/date）

    **任务状态统计**:
    - `total_tasks`: 命名空间下所有定时任务总数
    - `active_tasks`: 启用状态的任务数量
    - `inactive_tasks`: 禁用状态的任务数量

    **执行统计**:
    - `total_executions_today`: 今日（UTC 0点至当前时间）总执行次数
    - `successful_executions_today`: 今日成功执行次数
    - `failed_executions_today`: 今日失败执行次数
    - `success_rate_today`: 今日成功率 = (成功次数 / 总次数) × 100%

    **性能统计**:
    - `avg_execution_duration`: 今日平均执行时长（秒，仅计算成功的任务）

    **即将执行的任务**:
    - 按下次执行时间升序排列
    - 最多返回5个即将执行的任务
    - 包含任务 ID、名称和下次执行时间

    **使用场景**:
    - 定时任务管理首页概览
    - 运营监控看板
    - 定时任务健康度评估
    - 容量规划和分析
    - 管理决策支持

    **示例请求**:
    ```bash
    # 获取默认命名空间的统计数据
    curl -X GET "http://localhost:8001/api/v1/scheduled/statistics/default"

    # 获取生产环境的统计数据
    curl -X GET "http://localhost:8001/api/v1/scheduled/statistics/production"

    # 获取测试环境的统计数据
    curl -X GET "http://localhost:8001/api/v1/scheduled/statistics/test"
    ```

    **与其他接口配合使用**:
    ```bash
    # 1. 查看所有命名空间
    curl -X GET "http://localhost:8001/api/v1/namespaces/"

    # 2. 查看特定命名空间的定时任务统计
    curl -X GET "http://localhost:8001/api/v1/scheduled/statistics/default"

    # 3. 查看该命名空间下的所有定时任务
    curl -X GET "http://localhost:8001/api/v1/scheduled/?page=1&page_size=50"

    # 4. 查看某个任务的详细执行历史
    curl -X GET "http://localhost:8001/api/v1/scheduled/task-001/history"

    # 5. 查看某个任务的执行趋势
    curl -X GET "http://localhost:8001/api/v1/scheduled/task-001/trend?time_range=7d"
    ```

    **监控告警示例**:
    ```bash
    # 定期检查统计数据，设置告警阈值
    STATS=$(curl -s "http://localhost:8001/api/v1/scheduled/statistics/default")
    SUCCESS_RATE=$(echo $STATS | jq '.data.success_rate_today')

    # 如果成功率低于 95%，触发告警
    if (( $(echo "$SUCCESS_RATE < 95" | bc -l) )); then
      echo "Alert: Success rate is below 95%: $SUCCESS_RATE%"
      # 发送告警通知
    fi
    ```

    **注意事项**:
    - 统计数据基于 UTC 时区计算
    - 今日数据从 UTC 0点开始统计
    - 命名空间参数区分大小写
    - 如果命名空间不存在，返回 404 错误
    - 统计数据实时计算，可能有轻微延迟（通常小于1秒）
    - 即将执行的任务列表只包含启用状态的任务
    - 平均执行时长不包括失败和超时的任务
    """
    try:
        app = request.app
        if not app or not hasattr(app.state, 'data_access'):
            raise HTTPException(status_code=500, detail="Data access not initialized")
        
        data_access = app.state.data_access
        
        async with data_access.AsyncSessionLocal() as session:
            # 获取统计数据，传递命名空间参数
            stats = await data_access.get_scheduled_tasks_statistics(session, namespace)
            return stats
    except Exception as e:
        logger.error(f"获取定时任务统计失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


__all__ = ['router']