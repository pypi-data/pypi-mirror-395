"""
数据模型定义
所有的Pydantic模型集中管理
"""

# 任务相关模型
from .task import (
    TasksRequest,
    TaskDetailResponse,
    TaskInfo,
    TaskActionRequest,
    TaskListResponse,
    TaskMessageRequest,
    SendTasksRequest,
    SendTasksResponse
)

# 队列相关模型
from .queue import (
    TimeRangeQuery,
    QueueStatsResponse,
    QueueTimelineResponse,
    TrimQueueRequest,
    QueueInfo,
    QueueStats,
    QueueActionRequest,
    TaskRunsQueryRequest
)

# 定时任务相关模型
from .scheduled_task import (
    ScheduledTaskRequest,
    ScheduledTaskResponse,
    ScheduledTaskInfo,
    ScheduleConfig,
    ScheduledTaskCreate,
    ScheduledTaskUpdate,
    ScheduledTaskCreateRequest
)

# 告警相关模型
from .alert import (
    AlertRuleRequest,
    AlertRuleCreate,
    AlertRuleUpdate,
    AlertRule,
    AlertInstance,
    AlertSummary
)

# 命名空间相关模型
from .namespace import (
    ConfigMode,
    NamespaceCreate,
    NamespaceUpdate,
    NamespaceResponse,
    NamespaceInfo,
    NamespaceCreateRequest,
    NamespaceUpdateRequest
)

# 积压监控相关模型
from .backlog import (
    BacklogLatestRequest,
    BacklogTrendRequest,
    BacklogSnapshot,
    BacklogStatistics,
    BacklogTrendResponse,
    BacklogAlert
)

# 认证相关模型
from .auth import (
    LoginRequest,
    TokenResponse,
    RefreshRequest,
    RefreshResponse
)

# 通用模型
from .common import (
    ErrorResponse,
    FilterCondition,
    BaseListRequest,
    TimeRangeRequest,
    BatchOperationRequest,
    BatchOperationResponse,
    PaginationResponse,
    ListResponse,
    HealthCheck,
    SystemConfigUpdateRequest,
    ApiResponse
)

# 监控和分析模型
from .monitoring import (
    MetricPoint,
    TimeSeries,
    MonitoringMetrics,
    AnalyticsData,
    SystemHealth,
    DashboardOverviewRequest,
    DashboardOverview,
    WorkerMetrics
)

# Webhook 相关模型
from .webhook import (
    WebhookStatus as WebhookStatusSchema,
    WebhookReceiveResponse,
    WebhookInfo,
    WebhookListResponse
)

# 资产管理相关模型
from .asset import (
    AssetType as AssetTypeSchema,
    AssetStatus as AssetStatusSchema,
    AssetCreate,
    AssetUpdate,
    AssetInfo,
    AssetListResponse,
    AssetGroupSummary,
    ComputeNodeStatus
)

# API 响应模型
from .responses import (
    SuccessResponse,
    DataResponse,
    PaginatedDataResponse,
    SystemStatsData,
    SystemStatsResponse,
    DashboardStatsData,
    DashboardStatsResponse,
    QueueRankingItem,
    TopQueuesResponse,
    NamespaceStatistics,
    NamespaceStatisticsResponse,
    WorkerHeartbeatInfo,
    WorkersResponse,
    WorkerSummary,
    WorkerSummaryResponse,
    WorkerOfflineRecord,
    WorkerOfflineHistoryResponse,
    DatabaseStatus,
    SystemSettings,
    SystemSettingsResponse,
    DatabaseStatusResponse
)

__all__ = [
    # Auth
    'LoginRequest',
    'TokenResponse',
    'RefreshRequest',
    'RefreshResponse',

    # Task
    'TasksRequest',
    'TaskDetailResponse',
    'TaskInfo',
    'TaskActionRequest',
    'TaskListResponse',
    'TaskMessageRequest',
    'SendTasksRequest',
    'SendTasksResponse',

    # Queue
    'TimeRangeQuery',
    'QueueStatsResponse',
    'QueueTimelineResponse',
    'TrimQueueRequest',
    'QueueInfo',
    'QueueStats',
    'QueueActionRequest',
    'TaskRunsQueryRequest',

    # Scheduled Task
    'ScheduledTaskRequest',
    'ScheduledTaskResponse',
    'ScheduledTaskInfo',
    'ScheduleConfig',
    'ScheduledTaskCreate',
    'ScheduledTaskUpdate',
    'ScheduledTaskCreateRequest',
    
    # Alert
    'AlertRuleRequest',
    'AlertRuleCreate',
    'AlertRuleUpdate',
    'AlertRule',
    'AlertInstance',
    'AlertSummary',
    
    # Namespace
    'ConfigMode',
    'NamespaceCreate',
    'NamespaceUpdate',
    'NamespaceResponse',
    'NamespaceInfo',
    'NamespaceCreateRequest',
    'NamespaceUpdateRequest',
    
    # Backlog
    'BacklogTrendRequest',
    'BacklogSnapshot',
    'BacklogStatistics',
    'BacklogTrendResponse',
    'BacklogAlert',
    
    # Common
    'ErrorResponse',
    'FilterCondition',
    'BaseListRequest',
    'TimeRangeRequest',
    'BatchOperationRequest',
    'BatchOperationResponse',
    'PaginationResponse',
    'ListResponse',
    'HealthCheck',
    'SystemConfigUpdateRequest',
    'ApiResponse',
    
    # Monitoring
    'MetricPoint',
    'TimeSeries',
    'MonitoringMetrics',
    'AnalyticsData',
    'SystemHealth',
    'DashboardOverviewRequest',
    'DashboardOverview',
    'WorkerMetrics',

    # Responses
    'SuccessResponse',
    'DataResponse',
    'PaginatedDataResponse',
    'SystemStatsData',
    'SystemStatsResponse',
    'DashboardStatsData',
    'DashboardStatsResponse',
    'QueueRankingItem',
    'TopQueuesResponse',
    'NamespaceStatistics',
    'NamespaceStatisticsResponse',
    'WorkerHeartbeatInfo',
    'WorkersResponse',
    'WorkerSummary',
    'WorkerSummaryResponse',
    'WorkerOfflineRecord',
    'WorkerOfflineHistoryResponse',
    'DatabaseStatus',
    'SystemSettings',
    'SystemSettingsResponse',
    'DatabaseStatusResponse',

    # Webhook
    'WebhookStatusSchema',
    'WebhookReceiveResponse',
    'WebhookInfo',
    'WebhookListResponse',

    # Asset
    'AssetTypeSchema',
    'AssetStatusSchema',
    'AssetCreate',
    'AssetUpdate',
    'AssetInfo',
    'AssetListResponse',
    'AssetGroupSummary',
    'ComputeNodeStatus'
]