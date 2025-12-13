"""
Webhook 工具类

提供给任务使用的 webhook 相关工具函数
"""
import asyncio
import json
import uuid
import logging
from typing import Optional, Dict, Any
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

# Redis key 前缀
WEBHOOK_CHANNEL_PREFIX = "jettask:webhook:"


def generate_callback_id() -> str:
    """
    生成唯一的回调 ID

    Returns:
        str: 格式为 cb_{uuid} 的回调 ID
    """
    return f"cb_{uuid.uuid4().hex[:16]}"


def build_webhook_url(base_url: str, namespace: str, callback_id: str) -> str:
    """
    构建 webhook 回调 URL

    Args:
        base_url: 服务基础 URL，如 https://api.example.com
        namespace: 命名空间
        callback_id: 回调 ID

    Returns:
        str: 完整的 webhook URL

    Example:
        >>> build_webhook_url("https://api.example.com", "default", "cb_abc123")
        'https://api.example.com/api/task/v1/default/webhooks/cb_abc123'
    """
    # 确保 base_url 以 / 结尾
    if not base_url.endswith('/'):
        base_url = base_url + '/'

    path = f"api/task/v1/{namespace}/webhooks/{callback_id}"
    return urljoin(base_url, path)


async def wait_for_webhook(
    redis_client,
    namespace: str,
    callback_id: str,
    timeout: float = 300.0,
    fallback_poll_interval: float = 5.0
) -> Optional[Dict[str, Any]]:
    """
    等待 webhook 回调结果

    使用 Redis pub/sub 作为主要通知机制，同时有一个低频轮询作为兜底，
    防止 pub/sub 连接异常断开导致消息丢失。

    Args:
        redis_client: Redis 客户端
        namespace: 命名空间
        callback_id: 回调 ID
        timeout: 超时时间（秒），默认 300 秒（5分钟）
        fallback_poll_interval: 兜底轮询间隔（秒），默认 5 秒

    Returns:
        Dict[str, Any]: webhook 载荷数据，超时返回 None

    Example:
        ```python
        @app.task(queue="image_gen")
        async def generate_image(prompt: str):
            # 1. 生成回调 ID 和 URL
            callback_id = generate_callback_id()
            webhook_url = build_webhook_url(
                "https://api.example.com",
                "default",
                callback_id
            )

            # 2. 调用第三方 API，传递 webhook URL
            response = await third_party_api.generate(
                prompt=prompt,
                webhook_url=webhook_url
            )

            # 3. 等待 webhook 回调
            result = await wait_for_webhook(
                redis_client=app.redis,
                namespace="default",
                callback_id=callback_id,
                timeout=600  # 10 分钟超时
            )

            if result is None:
                raise TimeoutError("等待第三方回调超时")

            return result
        ```
    """
    result_key = f"{WEBHOOK_CHANNEL_PREFIX}result:{namespace}:{callback_id}"
    channel_name = f"{WEBHOOK_CHANNEL_PREFIX}{namespace}:{callback_id}"

    # 先检查是否已经有结果（处理 webhook 在订阅前就到达的情况）
    existing = await redis_client.lpop(result_key)
    if existing:
        try:
            data = json.loads(existing)
            logger.info(f"找到已存在的 webhook 结果: callback_id={callback_id}")
            return data.get("payload")
        except json.JSONDecodeError:
            logger.warning(f"解析已存在的 webhook 结果失败: {existing}")

    # 创建 pub/sub 订阅
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(channel_name)

    try:
        start_time = asyncio.get_event_loop().time()
        last_poll_time = start_time

        while True:
            # 检查是否超时
            current_time = asyncio.get_event_loop().time()
            elapsed = current_time - start_time
            if elapsed >= timeout:
                logger.warning(f"等待 webhook 超时: callback_id={callback_id}")
                return None

            # 尝试从 pub/sub 获取消息（短超时，快速响应）
            try:
                message = await asyncio.wait_for(
                    pubsub.get_message(ignore_subscribe_messages=True, timeout=0.5),
                    timeout=1.0
                )

                if message and message.get("type") == "message":
                    try:
                        data = json.loads(message["data"])
                        logger.info(f"通过 pub/sub 收到 webhook 结果: callback_id={callback_id}")
                        return data.get("payload")
                    except json.JSONDecodeError:
                        logger.warning(f"解析 pub/sub 消息失败: {message}")

            except asyncio.TimeoutError:
                pass
            except Exception as e:
                # pub/sub 可能断开，记录警告但继续轮询
                logger.warning(f"pub/sub 异常: {e}")

            # 兜底轮询：定期检查 Redis list（低频率）
            if current_time - last_poll_time >= fallback_poll_interval:
                last_poll_time = current_time
                try:
                    result = await redis_client.lpop(result_key)
                    if result:
                        try:
                            data = json.loads(result)
                            logger.info(f"通过兜底轮询收到 webhook 结果: callback_id={callback_id}")
                            return data.get("payload")
                        except json.JSONDecodeError:
                            logger.warning(f"解析 Redis list 结果失败: {result}")
                except Exception as e:
                    logger.warning(f"兜底轮询 Redis 失败: {e}")

            # 短暂休眠避免 CPU 空转
            await asyncio.sleep(0.1)

    finally:
        # 清理订阅
        try:
            await pubsub.unsubscribe(channel_name)
            await pubsub.close()
        except Exception:
            pass


class WebhookAwaiter:
    """
    Webhook 等待器

    提供更友好的 API 来等待 webhook 回调

    Example:
        ```python
        @app.task(queue="image_gen")
        async def generate_image(prompt: str):
            # 使用 WebhookAwaiter
            async with WebhookAwaiter(
                redis_client=app.redis,
                namespace="default",
                base_url="https://api.example.com"
            ) as awaiter:
                # 获取 webhook URL
                webhook_url = awaiter.webhook_url

                # 调用第三方 API
                await third_party_api.generate(prompt=prompt, webhook_url=webhook_url)

                # 等待结果
                result = await awaiter.wait(timeout=600)

            return result
        ```
    """

    def __init__(
        self,
        redis_client,
        namespace: str,
        base_url: str,
        callback_id: Optional[str] = None
    ):
        """
        初始化 WebhookAwaiter

        Args:
            redis_client: Redis 客户端
            namespace: 命名空间
            base_url: 服务基础 URL
            callback_id: 回调 ID（可选，不提供则自动生成）
        """
        self.redis_client = redis_client
        self.namespace = namespace
        self.base_url = base_url
        self.callback_id = callback_id or generate_callback_id()
        self._webhook_url = None

    @property
    def webhook_url(self) -> str:
        """获取 webhook URL"""
        if self._webhook_url is None:
            self._webhook_url = build_webhook_url(
                self.base_url, self.namespace, self.callback_id
            )
        return self._webhook_url

    async def wait(
        self,
        timeout: float = 300.0,
        fallback_poll_interval: float = 5.0
    ) -> Optional[Dict[str, Any]]:
        """
        等待 webhook 回调结果

        Args:
            timeout: 超时时间（秒）
            fallback_poll_interval: 兜底轮询间隔（秒），默认 5 秒

        Returns:
            webhook 载荷数据，超时返回 None
        """
        return await wait_for_webhook(
            redis_client=self.redis_client,
            namespace=self.namespace,
            callback_id=self.callback_id,
            timeout=timeout,
            fallback_poll_interval=fallback_poll_interval
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # 清理 Redis 中的结果数据
        result_key = f"{WEBHOOK_CHANNEL_PREFIX}result:{self.namespace}:{self.callback_id}"
        try:
            await self.redis_client.delete(result_key)
        except Exception:
            pass
        return False
