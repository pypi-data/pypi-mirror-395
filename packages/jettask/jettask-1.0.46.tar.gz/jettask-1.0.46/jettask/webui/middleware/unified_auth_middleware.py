"""
统一鉴权中间件

支持两种鉴权方式（二选一）：
1. API Key鉴权：X-API-Key header（适合后端服务调用）
2. JWT Token鉴权：Authorization: Bearer <token> header（适合前端用户登录）
"""
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from jettask.webui.utils.jwt_utils import JWTManager

logger = logging.getLogger(__name__)


class UnifiedAuthMiddleware(BaseHTTPMiddleware):
    """统一鉴权中间件

    检查请求头中的认证信息，支持以下两种方式（二选一）：
    1. X-API-Key: <api_key>
    2. Authorization: Bearer <jwt_token>

    如果配置了API密钥和JWT，则必须提供其中一种认证方式。
    如果都未配置，则跳过鉴权（仅用于开发环境）。
    """

    def __init__(
        self,
        app,
        api_key: str = None,
        jwt_manager: JWTManager = None,
        exclude_paths: list = None
    ):
        """
        初始化统一鉴权中间件

        Args:
            app: ASGI application
            api_key: API密钥（可选）
            jwt_manager: JWT管理器（可选）
            exclude_paths: 不需要鉴权的路径列表（如登录接口）
        """
        super().__init__(app)
        self.api_key = api_key
        self.jwt_manager = jwt_manager
        self.exclude_paths = exclude_paths or [
            '/api/task/v1/auth/login',
            '/api/task/v1/auth/refresh',
            '/docs',
            '/redoc',
            '/openapi.json'
        ]
        # Webhook 接收接口需要特殊处理（第三方平台回调无法携带我们的认证信息）
        self.webhook_path_pattern = '/webhooks/'

        # 日志记录配置状态
        auth_methods = []
        if self.api_key:
            auth_methods.append("API Key")
        if self.jwt_manager:
            auth_methods.append("JWT Token")

        if auth_methods:
            logger.info(f"统一鉴权中间件已启用 - 支持鉴权方式: {', '.join(auth_methods)}")
            logger.info(f"鉴权豁免路径: {', '.join(self.exclude_paths)}")
        else:
            logger.warning("统一鉴权中间件未启用 - 所有请求无需鉴权（仅用于开发环境）")

    async def dispatch(self, request: Request, call_next):
        """处理请求"""
        # 检查是否为豁免路径
        if self._is_excluded_path(request.url.path):
            logger.debug(f"跳过鉴权（豁免路径）: {request.url.path}")
            return await call_next(request)

        # Webhook 接收接口特殊处理：仅 POST 请求跳过鉴权（第三方回调）
        # GET/DELETE 等管理操作仍需鉴权
        if self._is_webhook_callback(request):
            logger.debug(f"跳过鉴权（Webhook 回调）: {request.url.path}")
            return await call_next(request)

        # 如果没有配置任何鉴权方式，跳过鉴权
        if not self.api_key and not self.jwt_manager:
            return await call_next(request)

        # 尝试API Key鉴权
        if self.api_key:
            api_key = request.headers.get('X-API-Key')
            if api_key and api_key == self.api_key:
                logger.debug(f"API Key鉴权通过: {request.url.path}")
                # 将认证信息存储到request.state中
                request.state.auth_type = "api_key"
                request.state.auth_user = "api_key_user"
                return await call_next(request)

        # 尝试JWT Token鉴权
        if self.jwt_manager:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header[7:]  # 移除 "Bearer " 前缀
                payload = self.jwt_manager.verify_token(token, token_type="access")
                if payload:
                    subject = payload.get('sub')
                    logger.debug(f"JWT Token鉴权通过: {request.url.path}, user={subject}")
                    # 将认证信息存储到request.state中
                    request.state.auth_type = "jwt_token"
                    request.state.auth_user = subject
                    request.state.auth_payload = payload
                    return await call_next(request)
                else:
                    logger.warning(f"JWT Token验证失败: {request.url.path}")
                    return JSONResponse(
                        status_code=401,
                        content={
                            "error": "Unauthorized",
                            "message": "无效或过期的token，请重新登录"
                        }
                    )

        # 如果两种方式都失败，返回401
        logger.warning(
            f"鉴权失败: {request.url.path} from {request.client.host if request.client else 'unknown'}"
        )
        return JSONResponse(
            status_code=401,
            content={
                "error": "Unauthorized",
                "message": "请提供有效的认证信息（X-API-Key 或 Authorization: Bearer <token>）"
            }
        )

    def _is_excluded_path(self, path: str) -> bool:
        """检查路径是否在豁免列表中"""
        for excluded in self.exclude_paths:
            if path.startswith(excluded):
                return True
        return False

    def _is_webhook_callback(self, request: Request) -> bool:
        """
        检查是否为 Webhook 回调请求

        Webhook 接收接口特殊处理：
        - POST /api/task/v1/{namespace}/webhooks/{callback_id} 需要跳过鉴权
          因为第三方平台回调时无法携带我们的认证信息
        - GET/DELETE 等管理操作仍需鉴权
        """
        if request.method != 'POST':
            return False

        path = request.url.path
        # 匹配 /api/task/v1/{namespace}/webhooks/{callback_id} 模式
        # 路径格式: /api/task/v1/xxx/webhooks/cb_xxx
        if self.webhook_path_pattern in path:
            parts = path.split('/')
            # 检查路径结构: ['', 'api', 'task', 'v1', '{namespace}', 'webhooks', '{callback_id}']
            if len(parts) >= 7 and parts[5] == 'webhooks':
                return True
        return False
