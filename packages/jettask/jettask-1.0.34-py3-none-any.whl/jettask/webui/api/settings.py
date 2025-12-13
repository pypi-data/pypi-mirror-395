"""
设置模块 - 系统配置
提供轻量级的路由入口，业务逻辑在 SettingsService 中实现
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging
import traceback

from jettask.schemas import SystemSettingsResponse, DatabaseStatusResponse
from jettask.webui.services.settings_service import SettingsService

logger = logging.getLogger(__name__)

# 创建设置模块路由，添加 /settings 前缀
router = APIRouter(prefix="/settings", tags=["settings"])


# ============ 系统配置接口 ============

@router.get(
    "/system",
    summary="获取系统配置信息",
    description="获取系统级别的配置信息，包括 API 版本、服务名称、运行环境、数据库状态等",
    response_model=SystemSettingsResponse,
    responses={
        200: {
            "description": "成功返回系统配置信息"
        },
        500: {
            "description": "服务器内部错误",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "获取系统配置失败: Configuration error"
                    }
                }
            }
        }
    }
)
async def get_system_settings() -> Dict[str, Any]:
    """
    ## 获取系统配置信息

    返回 JetTask WebUI 的系统级配置信息，用于系统管理和监控。

    **配置信息包括**:
    - API 版本号
    - 服务名称
    - 运行环境 (development/staging/production)
    - 调试模式状态
    - 数据库连接状态和配置

    **使用场景**:
    - 系统设置页面
    - 运维监控
    - 故障排查
    - 环境验证

    **示例请求**:
    ```bash
    curl -X GET "http://localhost:8001/api/v1/settings/system"
    ```

    **示例响应**:
    ```json
    {
        "success": true,
        "data": {
            "api_version": "v1",
            "service_name": "JetTask WebUI",
            "environment": "development",
            "debug_mode": true,
            "database": {
                "connected": true,
                "host": "localhost",
                "port": 5432,
                "database": "jettask",
                "pool_size": 10,
                "active_connections": 3
            }
        }
    }
    ```
    """
    try:
        return SettingsService.get_system_settings()
    except Exception as e:
        logger.error(f"获取系统配置失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/database-status",
    summary="检查数据库连接状态",
    description="检查数据库（PostgreSQL/MySQL）的连接状态和性能指标",
    response_model=DatabaseStatusResponse,
    responses={
        200: {
            "description": "成功返回数据库状态"
        },
        500: {
            "description": "服务器内部错误或数据库连接失败",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "数据库状态检查失败: Connection refused"
                    }
                }
            }
        }
    }
)
async def check_database_status() -> Dict[str, Any]:
    """
    ## 检查数据库连接状态

    检查 JetTask 数据库的连接状态、配置信息和性能指标。

    **返回信息包括**:
    - 连接状态 (connected: true/false)
    - 主机地址和端口
    - 数据库名称
    - 连接池大小
    - 当前活跃连接数

    **使用场景**:
    - 系统健康检查
    - 数据库监控
    - 故障诊断
    - 容量规划

    **示例请求**:
    ```bash
    curl -X GET "http://localhost:8001/api/v1/settings/database-status"
    ```

    **示例响应**:
    ```json
    {
        "success": true,
        "data": {
            "connected": true,
            "host": "localhost",
            "port": 5432,
            "database": "jettask",
            "pool_size": 10,
            "active_connections": 3
        }
    }
    ```

    **注意事项**:
    - 此接口会实际连接数据库进行检查
    - 如果数据库不可用，将返回 500 错误
    - 建议配置监控告警
    """
    try:
        return await SettingsService.check_database_status()
    except Exception as e:
        logger.error(f"数据库状态检查失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


__all__ = ['router']