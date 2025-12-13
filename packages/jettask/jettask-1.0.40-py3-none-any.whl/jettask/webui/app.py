import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from jettask.webui.config import webui_config
from jettask.db.connector import get_pg_engine_and_factory
import uvicorn

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    try:
        # 配置日志格式 - 根据环境变量 JETTASK_LOG_FORMAT 决定
        # 注意：只配置jettask相关的logger，不影响uvicorn的彩色日志
        log_format = os.environ.get('JETTASK_LOG_FORMAT', 'text').lower()
        log_level = logging.INFO

        # 只配置 jettask.* 开头的logger，保留uvicorn的彩色日志
        from jettask.utils.task_logger import JSONFormatter, ExtendedTextFormatter, TaskContextFilter
        import sys

        # 获取所有需要配置的jettask logger
        jettask_logger_names = [name for name in logging.Logger.manager.loggerDict
                                if name.startswith('jettask')]

        # 如果还没有jettask logger，至少配置根jettask logger
        if not jettask_logger_names:
            jettask_logger_names = ['jettask']

        # 配置jettask相关的logger
        for logger_name in jettask_logger_names:
            jettask_logger = logging.getLogger(logger_name)
            jettask_logger.setLevel(log_level)

            # 清除已有的handler，避免重复
            jettask_logger.handlers.clear()

            handler = logging.StreamHandler(sys.stderr)
            handler.addFilter(TaskContextFilter())

            if log_format == 'json':
                handler.setFormatter(JSONFormatter())
            else:
                handler.setFormatter(ExtendedTextFormatter(
                    '%(asctime)s - %(levelname)s - [%(task_id)s] - %(name)s - %(message)s'
                ))

            jettask_logger.addHandler(handler)
            jettask_logger.propagate = False  # 不传播到父logger

        if log_format == 'json':
            logger.info("日志格式已配置为 JSON (仅jettask相关日志)")
        else:
            logger.info("日志格式已配置为 TEXT (仅jettask相关日志)")

        # 获取数据库信息用于日志显示
        db_info = webui_config.get_database_info()

        # 记录任务中心配置（显示实际使用的配置）
        logger.info("=" * 60)
        logger.info("任务中心配置:")
        logger.info(f"  配置模式: {'Nacos' if webui_config.use_nacos else '环境变量'}")

        # 显示数据库连接信息
        if db_info['host']:
            logger.info(f"  元数据库: {db_info['host']}:{db_info['port']}/{db_info['database']}")
        else:
            logger.info(f"  元数据库: {webui_config.pg_url}")

        logger.info(f"  Redis: {webui_config._mask_url(webui_config.redis_url)}")
        logger.info(f"  Redis Prefix: {webui_config.redis_prefix}")
        logger.info(f"  API服务: {webui_config.api_host}:{webui_config.api_port}")
        logger.info(f"  基础URL: {webui_config.base_url}")
        logger.info("=" * 60)

        # 初始化元数据库会话工厂（用于命名空间管理等操作）
        meta_db_engine, meta_db_session_factory = get_pg_engine_and_factory(
            webui_config.meta_database_url
        )
        app.state.meta_db_engine = meta_db_engine
        app.state.meta_db_session_factory = meta_db_session_factory
        logger.info("元数据库会话工厂已初始化")

        logger.info("JetTask WebUI 启动成功")
    except Exception as e:
        logger.error(f"启动失败: {e}")
        import traceback
        traceback.print_exc()
        raise

    yield

    # Shutdown - 清理元数据库连接
    if hasattr(app.state, 'meta_db_engine') and app.state.meta_db_engine:
        await app.state.meta_db_engine.dispose()
        logger.info("元数据库连接已关闭")


app = FastAPI(title="Jettask Monitor", lifespan=lifespan)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源（生产环境应该指定具体域名）
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)

# 配置统一鉴权中间件（支持API Key和JWT Token两种方式）
# 后端服务可以使用 X-API-Key 头
# 前端用户可以使用 Authorization: Bearer <token> 头
from jettask.webui.middleware import UnifiedAuthMiddleware
from jettask.webui.utils.jwt_utils import JWTManager

# 获取认证配置
api_key = os.environ.get('JETTASK_API_KEY')
remote_token_verify_url = webui_config.remote_token_verify_url

# 只有在配置了远程认证URL时才初始化JWT管理器
# 因为JWT Token是给前端用户登录后使用的，而登录需要远程认证
jwt_manager = None
if remote_token_verify_url:
    jwt_manager = JWTManager(
        secret_key=webui_config.jwt_secret_key,
        algorithm=webui_config.jwt_algorithm,
        access_token_expire_minutes=webui_config.jwt_access_token_expire_minutes,
        refresh_token_expire_days=webui_config.jwt_refresh_token_expire_days
    )
    logger.info(f"JWT Manager 已初始化（用于前端用户认证）")

# 注册统一鉴权中间件
app.add_middleware(
    UnifiedAuthMiddleware,
    api_key=api_key,
    jwt_manager=jwt_manager
)

# 记录认证配置状态
auth_methods = []
if api_key:
    auth_methods.append("API Key（后端服务）")
if jwt_manager:
    auth_methods.append("JWT Token（前端用户）")

if auth_methods:
    logger.info(f"UnifiedAuthMiddleware 已注册 - 支持鉴权方式: {', '.join(auth_methods)}")
else:
    logger.warning("UnifiedAuthMiddleware 已注册 - 未配置任何鉴权方式，所有请求无需认证")

# 配置 Namespace 自动注入中间件
# 这个中间件会自动检测路由中的 {namespace} 参数，并注入到 request.state.ns
from jettask.webui.middleware import NamespaceMiddleware
app.add_middleware(NamespaceMiddleware)
logger.info("NamespaceMiddleware 已注册 - 所有包含 {namespace} 的路由将自动注入命名空间上下文")

# 注册 API 路由
from jettask.webui.api import api_router
app.include_router(api_router)


if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    uvicorn.run(app, host="0.0.0.0", port=8000)