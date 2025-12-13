"""
远程认证提供者

通过调用远程HTTP API验证企业SSO token
"""
import logging
from typing import Optional, Dict, Any
import aiohttp
from .auth_provider import AuthProvider, AuthResult

logger = logging.getLogger(__name__)


class RemoteAuthProvider(AuthProvider):
    """
    远程认证提供者

    通过HTTP API调用企业现有的认证服务验证 token。
    企业 SSO 系统返回 token 的 metadata（用户信息）。

    配置示例：
    {
        "verify_url": "https://auth.company.com/api/v1/verify",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json"
        },
        "timeout": 10,
        "token_field": "token",              # 请求中 token 字段名
        "token_location": "body",            # token 位置: body/header/query
        "success_field": "success",          # 响应中表示成功的字段
        "username_field": "data.username",   # 响应中用户名字段
        "user_info_field": "data"            # 响应中用户信息字段
    }

    使用流程：
    1. 前端用户在企业 SSO 系统登录，获得 access_token
    2. 前端调用我们的登录接口，传入这个 access_token
    3. 后端调用此 Provider 验证 token
    4. 企业认证 API 返回 token 的 metadata（用户信息）
    5. 后端生成自己的 JWT token 返回给前端
    """

    def __init__(
        self,
        verify_url: str,
        method: str = "POST",
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 10,
        token_field: str = "token",
        token_location: str = "body",
        success_field: str = "success",
        username_field: str = "username",
        user_info_field: Optional[str] = None,
        verify_ssl: bool = True
    ):
        """
        初始化远程认证提供者

        Args:
            verify_url: 验证 token 的 API URL
            method: HTTP方法（GET/POST）
            headers: 额外的请求头
            timeout: 请求超时时间（秒）
            token_field: token 字段名（如 "token", "access_token"）
            token_location: token 位置（body/header/query）
            success_field: 响应中表示认证成功的字段（支持点号分隔的嵌套路径）
            username_field: 响应中用户名字段（支持点号分隔的嵌套路径）
            user_info_field: 响应中用户信息字段（支持点号分隔的嵌套路径）
            verify_ssl: 是否验证SSL证书
        """
        self.verify_url = verify_url
        self.method = method.upper()
        self.headers = headers or {}
        self.timeout = timeout
        self.token_field = token_field
        self.token_location = token_location.lower()
        self.success_field = success_field
        self.username_field = username_field
        self.user_info_field = user_info_field
        self.verify_ssl = verify_ssl

        logger.info(
            f"RemoteAuthProvider 初始化完成\n"
            f"  验证URL: {verify_url}\n"
            f"  HTTP方法: {self.method}\n"
            f"  Token位置: {self.token_location} (字段名: {self.token_field})\n"
            f"  成功标志字段: {self.success_field}\n"
            f"  用户名字段: {self.username_field}\n"
            f"  用户信息字段: {self.user_info_field}\n"
            f"  SSL验证: {self.verify_ssl}"
        )

    def _get_nested_value(self, data: Dict[str, Any], field_path: str, default=None):
        """
        从嵌套字典中获取值，支持点号分隔的路径

        Args:
            data: 数据字典
            field_path: 字段路径，如 "data.user.name"
            default: 默认值

        Returns:
            字段值或默认值
        """
        parts = field_path.split('.')
        value = data
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
                if value is None:
                    return default
            else:
                return default
        return value

    async def verify_token(self, token: str) -> AuthResult:
        """
        验证企业 SSO token

        Args:
            token: 企业 SSO access_token

        Returns:
            AuthResult: 认证结果（包含用户信息）
        """
        try:
            logger.info(f"远程 token 验证请求: {self.method} {self.verify_url}")

            # 准备请求参数
            headers = self.headers.copy()
            params = None
            json_data = None

            # 根据 token_location 设置 token
            if self.token_location == "header":
                # Token 放在请求头中
                headers[self.token_field] = token
            elif self.token_location == "query":
                # Token 放在查询参数中
                params = {self.token_field: token}
            else:
                # Token 放在请求体中（默认）
                json_data = {self.token_field: token}

            # 创建 SSL 上下文
            ssl_context = None if self.verify_ssl else False

            # 创建超时配置
            timeout = aiohttp.ClientTimeout(total=self.timeout)

            # 发送HTTP请求
            async with aiohttp.ClientSession(timeout=timeout) as session:
                if self.method == "POST":
                    async with session.post(
                        self.verify_url,
                        headers=headers,
                        params=params,
                        json=json_data,
                        ssl=ssl_context
                    ) as response:
                        status = response.status
                        response_data = await response.json()
                elif self.method == "GET":
                    async with session.get(
                        self.verify_url,
                        headers=headers,
                        params=params,
                        ssl=ssl_context
                    ) as response:
                        status = response.status
                        response_data = await response.json()
                else:
                    logger.error(f"不支持的HTTP方法: {self.method}")
                    return AuthResult(
                        success=False,
                        error_message="认证服务配置错误"
                    )

            # 检查HTTP状态码
            if status != 200:
                logger.warning(f"远程 token 验证失败 - HTTP {status}")
                return AuthResult(
                    success=False,
                    error_message=f"Token 验证失败: HTTP {status}"
                )

            # 检查认证是否成功
            success = self._get_nested_value(
                response_data,
                self.success_field,
                default=False
            )

            logger.debug(
                f"远程认证响应解析:\n"
                f"  success_field配置: '{self.success_field}'\n"
                f"  从响应中提取的success值: {success!r} (类型: {type(success).__name__})\n"
                f"  完整响应: {response_data}"
            )

            if not success:
                logger.warning(
                    f"远程 token 验证失败 - 认证服务返回失败\n"
                    f"  配置的success_field: '{self.success_field}'\n"
                    f"  从响应中获取的值: {success!r}\n"
                    f"  完整响应数据: {response_data}\n"
                    f"  提示: 请检查 JETTASK_REMOTE_TOKEN_SUCCESS_FIELD 环境变量配置是否正确"
                )
                # 尝试获取错误信息
                error_msg = self._get_nested_value(
                    response_data,
                    "message",
                    default="Token 验证失败"
                )
                return AuthResult(
                    success=False,
                    error_message=str(error_msg)
                )

            # 提取用户信息
            username = self._get_nested_value(
                response_data,
                self.username_field,
                default=None
            )

            if not username:
                logger.error("远程认证响应中缺少用户名信息")
                return AuthResult(
                    success=False,
                    error_message="认证服务返回的用户信息不完整"
                )

            user_info = None
            if self.user_info_field:
                user_info = self._get_nested_value(
                    response_data,
                    self.user_info_field
                )

            # 添加认证方法信息
            if user_info is None:
                user_info = {}
            if isinstance(user_info, dict):
                user_info["auth_method"] = "remote"
                user_info["auth_url"] = self.verify_url

            logger.info(f"远程 token 验证成功: {username}")
            return AuthResult(
                success=True,
                username=username,
                user_info=user_info
            )

        except aiohttp.ClientError as e:
            logger.error(f"远程 token 验证请求失败: {e}")
            return AuthResult(
                success=False,
                error_message="无法连接到认证服务"
            )

        except TimeoutError:
            logger.error(f"远程 token 验证超时 (timeout: {self.timeout}s)")
            return AuthResult(
                success=False,
                error_message="认证服务响应超时"
            )

        except Exception as e:
            logger.error(f"远程 token 验证发生异常: {e}", exc_info=True)
            return AuthResult(
                success=False,
                error_message="认证过程发生错误"
            )

    def get_provider_name(self) -> str:
        """获取认证提供者名称"""
        return "remote"
