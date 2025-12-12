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

WEBHOOK_CHANNEL_PREFIX = "jettask:webhook:"


def generate_callback_id() -> str:
    return f"cb_{uuid.uuid4().hex[:16]}"


def build_webhook_url(base_url: str, namespace: str, callback_id: str) -> str:
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
    result_key = f"{WEBHOOK_CHANNEL_PREFIX}result:{namespace}:{callback_id}"
    channel_name = f"{WEBHOOK_CHANNEL_PREFIX}{namespace}:{callback_id}"

    existing = await redis_client.lpop(result_key)
    if existing:
        try:
            data = json.loads(existing)
            logger.info(f"找到已存在的 webhook 结果: callback_id={callback_id}")
            return data.get("payload")
        except json.JSONDecodeError:
            logger.warning(f"解析已存在的 webhook 结果失败: {existing}")

    pubsub = redis_client.pubsub()
    await pubsub.subscribe(channel_name)

    try:
        start_time = asyncio.get_event_loop().time()
        last_poll_time = start_time

        while True:
            current_time = asyncio.get_event_loop().time()
            elapsed = current_time - start_time
            if elapsed >= timeout:
                logger.warning(f"等待 webhook 超时: callback_id={callback_id}")
                return None

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
                logger.warning(f"pub/sub 异常: {e}")

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

            await asyncio.sleep(0.1)

    finally:
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
        self.redis_client = redis_client
        self.namespace = namespace
        self.base_url = base_url
        self.callback_id = callback_id or generate_callback_id()
        self._webhook_url = None

    @property
    def webhook_url(self) -> str:
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
        result_key = f"{WEBHOOK_CHANNEL_PREFIX}result:{self.namespace}:{self.callback_id}"
        try:
            await self.redis_client.delete(result_key)
        except Exception:
            pass
        return False
