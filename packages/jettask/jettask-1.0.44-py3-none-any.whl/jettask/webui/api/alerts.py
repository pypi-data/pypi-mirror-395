"""
告警管理路由
提供轻量级的路由入口，业务逻辑在 AlertService 中实现
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import logging

from jettask.schemas import AlertRuleRequest
from jettask.webui.services.alert_service import AlertService

router = APIRouter(prefix="/alerts", tags=["alerts"])
logger = logging.getLogger(__name__)


@router.get(
    "/rules",
    summary="获取告警规则列表",
    description="分页获取系统中配置的所有告警规则，支持按激活状态筛选",
    responses={
        200: {
            "description": "成功返回告警规则列表"
        },
        500: {
            "description": "服务器内部错误",
            "content": {
                "application/json": {
                    "example": {"detail": "获取告警规则列表失败: Database error"}
                }
            }
        }
    }
)
async def get_alert_rules(
    page: int = Query(1, ge=1, description="页码，从 1 开始", example=1),
    page_size: int = Query(20, ge=1, le=100, description="每页数量，范围 1-100", example=20),
    is_active: Optional[bool] = Query(None, description="是否只返回激活的规则", example=True)
):
    """
    ## 获取告警规则列表

    分页获取系统中配置的所有告警规则，每个规则包含监控指标、阈值、告警级别等完整信息。

    **功能说明**:
    - 支持分页查询，避免一次返回过多数据
    - 可按激活状态筛选规则
    - 返回每个规则的完整配置和状态信息

    **返回信息包括**:
    - 规则基本信息（ID、名称、描述）
    - 监控指标类型和阈值
    - 比较操作符和评估窗口
    - 告警级别和通知渠道
    - 启用状态和创建时间

    **使用场景**:
    - 告警规则管理页面
    - 告警配置概览
    - 规则状态监控

    **示例请求**:
    ```bash
    # 获取第一页的告警规则列表
    curl -X GET "http://localhost:8001/api/v1/alerts/rules?page=1&page_size=20"

    # 只获取激活的告警规则
    curl -X GET "http://localhost:8001/api/v1/alerts/rules?is_active=true"
    ```

    **注意事项**:
    - 分页参数超出范围时返回空列表
    - 返回的规则按创建时间倒序排列
    """
    try:
        return AlertService.get_alert_rules(page, page_size, is_active)
    except Exception as e:
        logger.error(f"获取告警规则列表失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/rules",
    summary="创建告警规则",
    description="创建一个新的告警规则，用于监控系统指标并在达到阈值时触发告警",
    status_code=201,
    responses={
        201: {
            "description": "告警规则创建成功"
        },
        400: {
            "description": "请求参数错误",
            "content": {
                "application/json": {
                    "example": {"detail": "规则名称已存在"}
                }
            }
        },
        500: {
            "description": "服务器内部错误"
        }
    }
)
async def create_alert_rule(request: AlertRuleRequest):
    """
    ## 创建告警规则

    创建一个新的告警规则，用于监控系统指标（如任务失败率、队列积压等）并在达到阈值时触发告警通知。

    **请求体参数**:
    ```json
    {
        "rule_name": "任务失败率告警",
        "metric_type": "task_failure_rate",
        "threshold": 0.1,
        "operator": "gt",
        "duration": 300,
        "severity": "high",
        "enabled": true,
        "description": "当任务失败率超过10%时触发告警"
    }
    ```

    **指标类型 (metric_type)**:
    - `task_failure_rate`: 任务失败率
    - `queue_backlog`: 队列积压数量
    - `worker_health`: Worker 健康状态
    - `task_execution_time`: 任务执行时间
    - `memory_usage`: 内存使用率
    - `cpu_usage`: CPU 使用率

    **比较操作符 (operator)**:
    - `gt`: 大于 (>)
    - `gte`: 大于等于 (>=)
    - `lt`: 小于 (<)
    - `lte`: 小于等于 (<=)
    - `eq`: 等于 (==)
    - `ne`: 不等于 (!=)

    **告警级别 (severity)**:
    - `low`: 低级告警（提示性信息）
    - `medium`: 中级告警（需要关注）
    - `high`: 高级告警（需要及时处理）
    - `critical`: 严重告警（需要立即处理）

    **使用场景**:
    - 监控任务执行健康度
    - 监控系统资源使用情况
    - 及时发现异常状态
    - 预防性运维

    **示例请求**:
    ```bash
    # 创建任务失败率告警
    curl -X POST "http://localhost:8001/api/v1/alerts/rules" \\
      -H "Content-Type: application/json" \\
      -d '{
        "rule_name": "任务失败率告警",
        "metric_type": "task_failure_rate",
        "threshold": 0.1,
        "operator": "gt",
        "duration": 300,
        "severity": "high",
        "enabled": true,
        "description": "当任务失败率超过10%且持续5分钟时触发告警"
      }'

    # 创建队列积压告警
    curl -X POST "http://localhost:8001/api/v1/alerts/rules" \\
      -H "Content-Type: application/json" \\
      -d '{
        "rule_name": "队列积压告警",
        "metric_type": "queue_backlog",
        "threshold": 1000,
        "operator": "gte",
        "duration": 600,
        "severity": "medium",
        "enabled": true,
        "description": "当队列积压任务数超过1000且持续10分钟时告警"
      }'
    ```

    **注意事项**:
    - 规则名称必须唯一
    - duration 参数表示持续时间（秒），指标需要持续满足条件才会触发告警
    - 创建后规则默认启用，可以通过 toggle 接口禁用
    - 建议根据实际业务场景合理设置阈值，避免告警过于频繁
    """
    try:
        return AlertService.create_alert_rule(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"创建告警规则失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/rules/{rule_id}",
    summary="更新告警规则",
    description="更新指定告警规则的配置信息，包括阈值、告警级别等",
    responses={
        200: {
            "description": "告警规则更新成功"
        },
        400: {
            "description": "请求参数错误",
            "content": {
                "application/json": {
                    "example": {"detail": "配置参数无效"}
                }
            }
        },
        404: {
            "description": "告警规则不存在",
            "content": {
                "application/json": {
                    "example": {"detail": "告警规则 'xxx' 不存在"}
                }
            }
        },
        500: {
            "description": "服务器内部错误"
        }
    }
)
async def update_alert_rule(rule_id: str, request: AlertRuleRequest):
    """
    ## 更新告警规则

    更新指定告警规则的配置信息，可以修改监控指标、阈值、告警级别等所有字段。

    **请求体参数**:
    ```json
    {
        "rule_name": "任务失败率告警（已更新）",
        "metric_type": "task_failure_rate",
        "threshold": 0.15,
        "operator": "gt",
        "duration": 600,
        "severity": "critical",
        "enabled": true,
        "description": "更新后的描述信息"
    }
    ```

    **可更新的字段**:
    - 规则名称和描述
    - 监控指标类型
    - 告警阈值
    - 比较操作符
    - 持续时间
    - 告警级别
    - 启用状态

    **使用场景**:
    - 调整告警阈值
    - 修改告警级别
    - 更新规则描述
    - 优化告警策略

    **示例请求**:
    ```bash
    # 更新告警阈值和级别
    curl -X PUT "http://localhost:8001/api/v1/alerts/rules/rule-123" \\
      -H "Content-Type: application/json" \\
      -d '{
        "rule_name": "任务失败率告警",
        "metric_type": "task_failure_rate",
        "threshold": 0.15,
        "operator": "gt",
        "duration": 600,
        "severity": "critical",
        "enabled": true,
        "description": "提高阈值到15%，延长持续时间到10分钟"
      }'
    ```

    **注意事项**:
    - 更新规则会立即生效
    - 如果规则正在触发告警，更新后会重新评估
    - 建议更新前先测试新的配置是否合理
    - 所有字段都必须提供（完整更新）
    """
    try:
        return AlertService.update_alert_rule(rule_id, request)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"更新告警规则失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/rules/{rule_id}",
    summary="删除告警规则",
    description="删除指定的告警规则，删除后将停止监控该规则",
    responses={
        200: {
            "description": "告警规则删除成功",
            "content": {
                "application/json": {
                    "example": {"success": True, "message": "告警规则已删除"}
                }
            }
        },
        404: {
            "description": "告警规则不存在",
            "content": {
                "application/json": {
                    "example": {"detail": "告警规则 'xxx' 不存在"}
                }
            }
        },
        500: {
            "description": "服务器内部错误"
        }
    }
)
async def delete_alert_rule(rule_id: str):
    """
    ## 删除告警规则

    删除指定的告警规则，删除后将停止对该指标的监控和告警。

    **删除规则**:
    - 删除操作不可逆，请谨慎操作
    - 删除后会停止该规则的所有监控
    - 历史告警记录会保留

    **使用场景**:
    - 清理不再需要的告警规则
    - 移除过时的监控指标
    - 告警策略调整

    **示例请求**:
    ```bash
    curl -X DELETE "http://localhost:8001/api/v1/alerts/rules/rule-123"
    ```

    **注意事项**:
    - 删除规则会停止该规则的监控，但不会删除历史告警记录
    - 如果规则正在触发告警，删除后告警将自动解除
    - 建议删除前先禁用规则，观察一段时间再删除
    - 删除操作不可恢复，重要规则建议先导出备份
    """
    try:
        return AlertService.delete_alert_rule(rule_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"删除告警规则失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/rules/{rule_id}/toggle",
    summary="启用/禁用告警规则",
    description="切换告警规则的启用状态，禁用后将暂停监控",
    responses={
        200: {
            "description": "告警规则状态切换成功",
            "content": {
                "application/json": {
                    "example": {"success": True, "enabled": True, "message": "告警规则已启用"}
                }
            }
        },
        404: {
            "description": "告警规则不存在",
            "content": {
                "application/json": {
                    "example": {"detail": "告警规则 'xxx' 不存在"}
                }
            }
        },
        500: {
            "description": "服务器内部错误"
        }
    }
)
async def toggle_alert_rule(rule_id: str):
    """
    ## 启用/禁用告警规则

    切换告警规则的启用状态。禁用后规则将暂停监控，不会触发新的告警；启用后恢复监控。

    **功能说明**:
    - 如果规则当前是启用状态，则禁用
    - 如果规则当前是禁用状态，则启用
    - 切换操作立即生效

    **使用场景**:
    - 临时停止某个告警规则的监控
    - 系统维护期间暂停告警
    - 测试和调试时快速切换规则状态
    - 避免告警风暴时临时关闭规则

    **示例请求**:
    ```bash
    # 切换告警规则状态
    curl -X POST "http://localhost:8001/api/v1/alerts/rules/rule-123/toggle"
    ```

    **返回示例**:
    ```json
    {
        "success": true,
        "enabled": false,
        "message": "告警规则已禁用"
    }
    ```

    **注意事项**:
    - 禁用规则后，正在触发的告警不会自动解除
    - 启用规则后会立即开始监控，可能会立即触发告警
    - 建议在系统维护期间临时禁用告警规则
    - 禁用状态会持久化保存，需要手动重新启用
    """
    try:
        return AlertService.toggle_alert_rule(rule_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"切换告警规则状态失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/rules/{rule_id}/history",
    summary="获取告警触发历史",
    description="分页获取指定告警规则的历史触发记录",
    responses={
        200: {
            "description": "成功返回告警历史记录"
        },
        404: {
            "description": "告警规则不存在",
            "content": {
                "application/json": {
                    "example": {"detail": "告警规则 'xxx' 不存在"}
                }
            }
        },
        500: {
            "description": "服务器内部错误"
        }
    }
)
async def get_alert_history(
    rule_id: str,
    page: int = Query(1, ge=1, description="页码，从 1 开始", example=1),
    page_size: int = Query(20, ge=1, le=100, description="每页数量，范围 1-100", example=20)
):
    """
    ## 获取告警触发历史

    分页获取指定告警规则的历史触发记录，用于分析告警趋势和问题排查。

    **返回信息包括**:
    - 告警触发时间
    - 告警级别
    - 触发时的指标值
    - 告警状态（活跃/已解决/已确认）
    - 持续时间
    - 解决时间和解决说明

    **使用场景**:
    - 分析告警触发频率和趋势
    - 排查系统问题
    - 评估告警规则的合理性
    - 生成告警报告

    **示例请求**:
    ```bash
    # 获取告警规则的历史记录
    curl -X GET "http://localhost:8001/api/v1/alerts/rules/rule-123/history?page=1&page_size=20"
    ```

    **返回示例**:
    ```json
    {
        "success": true,
        "data": {
            "total": 45,
            "page": 1,
            "page_size": 20,
            "items": [
                {
                    "id": "alert-001",
                    "triggered_at": "2025-10-19T10:30:00Z",
                    "resolved_at": "2025-10-19T10:45:00Z",
                    "severity": "high",
                    "metric_value": 0.18,
                    "threshold": 0.1,
                    "status": "resolved",
                    "duration": 900
                }
            ]
        }
    }
    ```

    **注意事项**:
    - 历史记录按触发时间倒序排列（最新的在前）
    - 包含已解决和未解决的所有告警记录
    - 可用于统计分析和问题排查
    """
    try:
        return AlertService.get_alert_history(rule_id, page, page_size)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"获取告警历史失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/rules/{rule_id}/test",
    summary="测试告警规则",
    description="测试告警规则的通知功能，发送测试告警消息",
    responses={
        200: {
            "description": "测试通知发送成功",
            "content": {
                "application/json": {
                    "example": {"success": True, "message": "测试通知已发送"}
                }
            }
        },
        404: {
            "description": "告警规则不存在",
            "content": {
                "application/json": {
                    "example": {"detail": "告警规则 'xxx' 不存在"}
                }
            }
        },
        500: {
            "description": "服务器内部错误"
        }
    }
)
async def test_alert_rule(rule_id: str):
    """
    ## 测试告警规则

    测试告警规则的通知功能，向配置的通知渠道发送测试告警消息，用于验证告警配置是否正确。

    **功能说明**:
    - 发送测试告警消息到配置的通知渠道
    - 验证通知渠道是否配置正确
    - 不会创建真实的告警记录
    - 测试消息会标注为"测试告警"

    **使用场景**:
    - 验证告警规则配置是否正确
    - 测试通知渠道是否可用
    - 检查告警消息格式
    - 新建规则后的功能验证

    **示例请求**:
    ```bash
    # 测试告警规则
    curl -X POST "http://localhost:8001/api/v1/alerts/rules/rule-123/test"
    ```

    **返回示例**:
    ```json
    {
        "success": true,
        "message": "测试通知已发送",
        "channels": ["email", "webhook"],
        "test_time": "2025-10-19T10:30:00Z"
    }
    ```

    **注意事项**:
    - 测试通知会实际发送到配置的通知渠道
    - 如果通知渠道未配置，测试会失败
    - 测试不会触发真实的告警流程
    - 建议在规则创建或修改后进行测试
    - 频繁测试可能会导致通知渠道限流
    """
    try:
        return AlertService.test_alert_rule(rule_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"测试告警规则失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============ 告警统计接口 ============

@router.get(
    "/statistics",
    summary="获取告警统计信息",
    description="获取告警系统的统计数据，包括告警数量、级别分布等",
    responses={
        200: {
            "description": "成功返回告警统计信息"
        },
        500: {
            "description": "服务器内部错误",
            "content": {
                "application/json": {
                    "example": {"detail": "获取告警统计信息失败: Database error"}
                }
            }
        }
    }
)
async def get_alert_statistics(
    namespace: Optional[str] = Query(None, description="命名空间名称，不指定则统计所有命名空间", example="default")
):
    """
    ## 获取告警统计信息

    获取告警系统的统计数据，包括总告警数、活跃告警数、按级别分类的告警数等，用于监控和分析。

    **返回信息包括**:
    - 总告警数量
    - 活跃告警数量
    - 已解决告警数量
    - 按级别分类的告警数（critical、high、medium、low）
    - 近24小时告警趋势
    - 告警规则总数

    **使用场景**:
    - 告警监控仪表板
    - 系统健康度评估
    - 告警趋势分析
    - 运维报表生成

    **示例请求**:
    ```bash
    # 获取所有命名空间的告警统计
    curl -X GET "http://localhost:8001/api/v1/alerts/statistics"

    # 获取指定命名空间的告警统计
    curl -X GET "http://localhost:8001/api/v1/alerts/statistics?namespace=default"
    ```

    **返回示例**:
    ```json
    {
        "success": true,
        "data": {
            "total_alerts": 156,
            "active_alerts": 12,
            "resolved_alerts": 144,
            "critical_alerts": 3,
            "high_alerts": 5,
            "medium_alerts": 4,
            "low_alerts": 0,
            "total_rules": 8,
            "active_rules": 6,
            "alert_trend_24h": {
                "00:00": 2,
                "01:00": 1,
                "02:00": 0,
                ...
            }
        }
    }
    ```

    **注意事项**:
    - 如果不指定命名空间，返回所有命名空间的汇总统计
    - 统计数据为实时查询，可能会有轻微延迟
    - 24小时趋势数据按小时粒度统计
    """
    try:
        return AlertService.get_alert_statistics(namespace)
    except Exception as e:
        logger.error(f"获取告警统计信息失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============ 活跃告警管理 ============

@router.get(
    "/active",
    summary="获取当前活跃的告警",
    description="获取系统中当前正在活跃状态的告警列表",
    responses={
        200: {
            "description": "成功返回活跃告警列表"
        },
        500: {
            "description": "服务器内部错误",
            "content": {
                "application/json": {
                    "example": {"detail": "获取活跃告警失败: Database error"}
                }
            }
        }
    }
)
async def get_active_alerts(
    namespace: Optional[str] = Query(None, description="命名空间名称，不指定则返回所有命名空间的活跃告警", example="default")
):
    """
    ## 获取当前活跃的告警

    获取系统中当前正在活跃状态的告警列表，即尚未解决的告警。

    **返回信息包括**:
    - 告警ID和规则名称
    - 告警级别（critical、high、medium、low）
    - 触发时间和持续时间
    - 当前指标值和阈值
    - 告警状态（活跃/已确认）
    - 命名空间信息
    - 告警消息和详细描述

    **告警状态**:
    - `active`: 活跃告警（未确认）
    - `acknowledged`: 已确认告警（但未解决）

    **使用场景**:
    - 告警监控大屏
    - 实时告警通知
    - 运维值班查看
    - 问题快速响应

    **示例请求**:
    ```bash
    # 获取所有活跃告警
    curl -X GET "http://localhost:8001/api/v1/alerts/active"

    # 获取指定命名空间的活跃告警
    curl -X GET "http://localhost:8001/api/v1/alerts/active?namespace=default"
    ```

    **返回示例**:
    ```json
    {
        "success": true,
        "data": [
            {
                "id": "alert-001",
                "rule_id": "rule-123",
                "rule_name": "任务失败率告警",
                "severity": "high",
                "status": "active",
                "metric_value": 0.18,
                "threshold": 0.1,
                "message": "任务失败率超过阈值",
                "started_at": "2025-10-19T10:30:00Z",
                "duration": 1800,
                "namespace": "default"
            },
            {
                "id": "alert-002",
                "rule_id": "rule-456",
                "rule_name": "队列积压告警",
                "severity": "medium",
                "status": "acknowledged",
                "metric_value": 1250,
                "threshold": 1000,
                "message": "队列积压任务数超过阈值",
                "started_at": "2025-10-19T09:15:00Z",
                "duration": 6300,
                "acknowledged_at": "2025-10-19T10:00:00Z",
                "acknowledged_by": "admin",
                "namespace": "default"
            }
        ]
    }
    ```

    **注意事项**:
    - 返回的告警按告警级别和触发时间排序（严重的在前）
    - 已确认但未解决的告警也会包含在结果中
    - 不包括已解决的告警
    - 可用于实时监控和告警响应
    """
    try:
        return AlertService.get_active_alerts(namespace)
    except Exception as e:
        logger.error(f"获取活跃告警失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/active/{alert_id}/acknowledge",
    summary="确认告警",
    description="确认一个活跃的告警，表示已知晓该告警并正在处理",
    responses={
        200: {
            "description": "告警确认成功",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "告警已确认",
                        "acknowledged_at": "2025-10-19T10:30:00Z",
                        "acknowledged_by": "admin"
                    }
                }
            }
        },
        404: {
            "description": "告警不存在",
            "content": {
                "application/json": {
                    "example": {"detail": "告警 'xxx' 不存在"}
                }
            }
        },
        500: {
            "description": "服务器内部错误"
        }
    }
)
async def acknowledge_alert(
    alert_id: str,
    user: str = Query("system", description="确认用户名称", example="admin")
):
    """
    ## 确认告警

    确认一个活跃的告警，表示已知晓该告警并正在处理中。确认后告警状态变为"已确认"，但仍保持活跃。

    **功能说明**:
    - 将告警状态从"活跃"变更为"已确认"
    - 记录确认时间和确认人
    - 告警仍然保持活跃，直到问题解决
    - 可用于告警认领和责任分配

    **使用场景**:
    - 运维人员接手处理告警
    - 告警认领和责任划分
    - 防止多人重复处理同一告警
    - 告警处理流程跟踪

    **示例请求**:
    ```bash
    # 确认告警
    curl -X POST "http://localhost:8001/api/v1/alerts/active/alert-001/acknowledge?user=admin"
    ```

    **返回示例**:
    ```json
    {
        "success": true,
        "message": "告警已确认",
        "alert_id": "alert-001",
        "acknowledged_at": "2025-10-19T10:30:00Z",
        "acknowledged_by": "admin"
    }
    ```

    **注意事项**:
    - 只能确认活跃状态的告警
    - 已确认的告警可以重复确认（更新确认时间和确认人）
    - 确认操作不会解决告警，需要调用 resolve 接口解决
    - 建议在开始处理告警时立即确认
    - user 参数应传入实际操作人的用户名
    """
    try:
        return AlertService.acknowledge_alert(alert_id, user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"确认告警失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/active/{alert_id}/resolve",
    summary="解决告警",
    description="标记告警为已解决状态，并可添加解决说明",
    responses={
        200: {
            "description": "告警解决成功",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "告警已解决",
                        "resolved_at": "2025-10-19T10:45:00Z"
                    }
                }
            }
        },
        404: {
            "description": "告警不存在",
            "content": {
                "application/json": {
                    "example": {"detail": "告警 'xxx' 不存在"}
                }
            }
        },
        500: {
            "description": "服务器内部错误"
        }
    }
)
async def resolve_alert(
    alert_id: str,
    resolution_note: Optional[str] = Query(None, description="解决说明，记录如何解决该告警", example="已修复任务处理逻辑，重启相关服务")
):
    """
    ## 解决告警

    标记告警为已解决状态，表示问题已经处理完成。可以添加解决说明，记录问题原因和处理方法。

    **功能说明**:
    - 将告警状态变更为"已解决"
    - 记录解决时间
    - 可选添加解决说明（建议填写）
    - 告警从活跃列表中移除
    - 保留在历史记录中供查询

    **使用场景**:
    - 问题处理完成后关闭告警
    - 记录问题解决方法
    - 建立知识库和问题处理文档
    - 告警生命周期管理

    **示例请求**:
    ```bash
    # 解决告警（不添加说明）
    curl -X POST "http://localhost:8001/api/v1/alerts/active/alert-001/resolve"

    # 解决告警并添加说明
    curl -X POST "http://localhost:8001/api/v1/alerts/active/alert-001/resolve?resolution_note=已修复任务处理逻辑，重启相关服务"
    ```

    **返回示例**:
    ```json
    {
        "success": true,
        "message": "告警已解决",
        "alert_id": "alert-001",
        "resolved_at": "2025-10-19T10:45:00Z",
        "resolution_note": "已修复任务处理逻辑，重启相关服务",
        "duration": 900
    }
    ```

    **注意事项**:
    - 只能解决活跃状态或已确认状态的告警
    - 已解决的告警不能再次解决
    - 建议添加详细的解决说明，便于后续问题排查和知识积累
    - 解决操作会记录到告警历史中
    - 如果问题再次出现，会创建新的告警实例
    - 解决说明应包含问题原因、处理步骤和验证方法
    """
    try:
        return AlertService.resolve_alert(alert_id, resolution_note)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"解决告警失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


__all__ = ['router']