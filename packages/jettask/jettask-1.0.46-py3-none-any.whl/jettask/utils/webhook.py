"""
Webhook 工具类

提供给任务使用的 webhook 相关工具函数
"""
import asyncio
import json
import uuid
import logging
from typing import Optional, Dict, Any, List, Callable, AsyncIterator
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

    path = f"{namespace}/webhooks/{callback_id}"
    return urljoin(base_url, path)


class WebhookAwaiter:
    """
    Webhook 等待器

    支持接收多次回调通知，提供迭代器和条件等待两种使用方式。

    Example 1: 等待直到满足条件（推荐）
        ```python
        @app.task(queue="image_gen")
        async def generate_image(prompt: str):
            async with WebhookAwaiter(
                redis_client=app.redis,
                namespace="default",
                base_url="https://api.example.com"
            ) as awaiter:
                # 调用第三方 API
                await replicate.run(
                    model="stability-ai/sdxl",
                    input={"prompt": prompt},
                    webhook=awaiter.webhook_url
                )

                # 等待直到状态为 completed 或 failed
                result = await awaiter.wait_until(
                    condition=lambda p: p.get("status") in ("succeeded", "failed"),
                    timeout=600
                )

            return result
        ```

    Example 2: 迭代接收所有回调
        ```python
        @app.task(queue="video_process")
        async def process_video(video_url: str):
            async with WebhookAwaiter(
                redis_client=app.redis,
                namespace="default",
                base_url="https://api.example.com"
            ) as awaiter:
                # 调用第三方 API
                await start_video_process(video_url, webhook=awaiter.webhook_url)

                # 迭代接收所有回调
                async for payload in awaiter.iter_callbacks(timeout=1800):
                    status = payload.get("status")
                    progress = payload.get("progress", 0)

                    print(f"状态: {status}, 进度: {progress}%")

                    if status == "completed":
                        return payload.get("output")
                    elif status == "failed":
                        raise Exception(payload.get("error"))

            raise TimeoutError("处理超时")
        ```

    Example 3: 手动循环接收
        ```python
        async with WebhookAwaiter(...) as awaiter:
            await start_task(webhook=awaiter.webhook_url)

            while True:
                payload = await awaiter.wait_next(timeout=60)
                if payload is None:
                    continue  # 超时，继续等待

                if payload.get("status") == "completed":
                    return payload
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
            redis_client: Redis 客户端（异步）
            namespace: 命名空间
            base_url: 服务基础 URL
            callback_id: 回调 ID（可选，不提供则自动生成）
        """
        self.redis_client = redis_client
        self.namespace = namespace
        self.base_url = base_url
        self.callback_id = callback_id or generate_callback_id()
        self._webhook_url = None
        self._pubsub = None
        self._channel_name = f"{WEBHOOK_CHANNEL_PREFIX}{namespace}:{self.callback_id}"
        self._result_key = f"{WEBHOOK_CHANNEL_PREFIX}result:{namespace}:{self.callback_id}"
        self._started = False
        self._closed = False

    @property
    def webhook_url(self) -> str:
        """获取 webhook URL"""
        if self._webhook_url is None:
            self._webhook_url = build_webhook_url(
                self.base_url, self.namespace, self.callback_id
            )
        return self._webhook_url

    async def _ensure_subscribed(self):
        """确保已订阅 Redis channel"""
        if self._pubsub is None:
            self._pubsub = self.redis_client.pubsub()
            await self._pubsub.subscribe(self._channel_name)
            self._started = True
            logger.debug(f"已订阅 webhook channel: {self._channel_name}")

    async def _pubsub_listener(self, result_queue: asyncio.Queue) -> None:
        """
        Pub/Sub 监听任务（内部方法）

        持续监听 Redis pub/sub channel，收到消息后放入队列
        """
        while not self._closed:
            try:
                message = await self._pubsub.get_message(
                    ignore_subscribe_messages=True,
                    timeout=1.0
                )

                if message and message.get("type") == "message":
                    try:
                        data = json.loads(message["data"])
                        logger.debug(f"通过 pub/sub 收到 webhook: callback_id={self.callback_id}")
                        await result_queue.put(("pubsub", data.get("payload")))
                        return  # 收到消息后退出
                    except json.JSONDecodeError:
                        logger.warning(f"解析 pub/sub 消息失败: {message}")

            except asyncio.CancelledError:
                return
            except Exception as e:
                logger.warning(f"pub/sub 异常: {e}")
                await asyncio.sleep(0.5)

    async def _poll_listener(self, result_queue: asyncio.Queue, poll_interval: float = 2.0) -> None:
        """
        轮询监听任务（内部方法）

        定期轮询 Redis list，收到消息后放入队列
        """
        while not self._closed:
            try:
                result = await self.redis_client.lpop(self._result_key)
                if result:
                    try:
                        data = json.loads(result)
                        logger.debug(f"通过轮询收到 webhook: callback_id={self.callback_id}")
                        await result_queue.put(("poll", data.get("payload")))
                        return  # 收到消息后退出
                    except json.JSONDecodeError:
                        logger.warning(f"解析 Redis list 结果失败: {result}")
            except asyncio.CancelledError:
                return
            except Exception as e:
                logger.warning(f"轮询 Redis 失败: {e}")

            await asyncio.sleep(poll_interval)

    async def _get_next_message(self, timeout: float) -> Optional[Dict[str, Any]]:
        """
        获取下一条消息（内部方法）

        使用两个并发任务同时监听 pub/sub 和轮询 Redis list，
        任一任务获取到消息即返回。
        """
        await self._ensure_subscribed()

        if self._closed:
            return None

        # 创建结果队列
        result_queue: asyncio.Queue = asyncio.Queue()

        # 创建并发任务
        pubsub_task = asyncio.create_task(self._pubsub_listener(result_queue))
        poll_task = asyncio.create_task(self._poll_listener(result_queue))

        try:
            # 等待队列中的结果，设置超时
            result = await asyncio.wait_for(result_queue.get(), timeout=timeout)
            source, payload = result
            logger.debug(f"收到 webhook（来源: {source}）: callback_id={self.callback_id}")
            return payload

        except asyncio.TimeoutError:
            logger.debug(f"等待 webhook 超时: callback_id={self.callback_id}")
            return None

        finally:
            # 取消所有任务
            pubsub_task.cancel()
            poll_task.cancel()

            # 等待任务完成（忽略取消异常）
            for task in [pubsub_task, poll_task]:
                try:
                    await task
                except asyncio.CancelledError:
                    pass

    async def wait_next(self, timeout: float = 60.0) -> Optional[Dict[str, Any]]:
        """
        等待下一次回调

        Args:
            timeout: 超时时间（秒），默认 60 秒

        Returns:
            webhook 载荷数据，超时返回 None
        """
        # 先检查是否有已到达的消息
        try:
            result = await self.redis_client.lpop(self._result_key)
            if result:
                data = json.loads(result)
                logger.debug(f"获取已存在的 webhook: callback_id={self.callback_id}")
                return data.get("payload")
        except Exception:
            pass

        return await self._get_next_message(timeout)

    async def wait_until(
        self,
        condition: Callable[[Dict[str, Any]], bool],
        timeout: float = 300.0,
        on_progress: Optional[Callable[[Dict[str, Any]], None]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        等待直到回调满足指定条件

        Args:
            condition: 条件函数，接收 payload，返回 True 表示满足条件
            timeout: 总超时时间（秒），默认 300 秒
            on_progress: 可选的进度回调函数，每次收到回调时调用

        Returns:
            满足条件的 payload，超时返回 None

        Example:
            ```python
            # 等待状态变为 completed 或 failed
            result = await awaiter.wait_until(
                condition=lambda p: p.get("status") in ("succeeded", "failed"),
                timeout=600,
                on_progress=lambda p: print(f"进度: {p.get('progress', 0)}%")
            )
            ```
        """
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining = timeout - elapsed

            if remaining <= 0:
                logger.warning(f"wait_until 超时: callback_id={self.callback_id}")
                return None

            # 等待下一条消息，使用剩余时间作为超时
            payload = await self.wait_next(timeout=min(remaining, 60.0))

            if payload is None:
                # 单次等待超时，但总时间可能还没到，继续等待
                continue

            # 调用进度回调
            if on_progress:
                try:
                    on_progress(payload)
                except Exception as e:
                    logger.warning(f"进度回调异常: {e}")

            # 检查条件
            try:
                if condition(payload):
                    logger.info(f"wait_until 条件满足: callback_id={self.callback_id}")
                    return payload
            except Exception as e:
                logger.warning(f"条件检查异常: {e}")

    async def iter_callbacks(
        self,
        timeout: float = 300.0,
        idle_timeout: float = 60.0
    ) -> AsyncIterator[Dict[str, Any]]:
        """
        迭代接收所有回调

        Args:
            timeout: 总超时时间（秒），默认 300 秒
            idle_timeout: 单次等待超时时间（秒），默认 60 秒
                          超过此时间没有收到回调，迭代器结束

        Yields:
            每次收到的 webhook payload

        Example:
            ```python
            async for payload in awaiter.iter_callbacks(timeout=600):
                print(f"收到回调: {payload}")
                if payload.get("status") == "completed":
                    break
            ```
        """
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining = timeout - elapsed

            if remaining <= 0:
                logger.debug(f"iter_callbacks 总超时: callback_id={self.callback_id}")
                return

            # 等待下一条消息
            wait_time = min(remaining, idle_timeout)
            payload = await self.wait_next(timeout=wait_time)

            if payload is None:
                # 单次等待超时，结束迭代
                logger.debug(f"iter_callbacks 空闲超时: callback_id={self.callback_id}")
                return

            yield payload

    async def get_all_pending(self) -> List[Dict[str, Any]]:
        """
        获取所有已到达但未处理的回调

        Returns:
            所有待处理的 payload 列表
        """
        results = []
        while True:
            try:
                result = await self.redis_client.lpop(self._result_key)
                if not result:
                    break
                data = json.loads(result)
                results.append(data.get("payload"))
            except Exception as e:
                logger.warning(f"获取待处理回调失败: {e}")
                break
        return results

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._closed = True

        # 清理 pub/sub
        if self._pubsub:
            try:
                await self._pubsub.unsubscribe(self._channel_name)
                await self._pubsub.close()
            except Exception:
                pass

        # 清理 Redis 中的结果数据
        try:
            await self.redis_client.delete(self._result_key)
        except Exception:
            pass

        return False


# 兼容旧 API 的便捷函数
async def wait_for_webhook(
    redis_client,
    namespace: str,
    callback_id: str,
    timeout: float = 300.0,
    fallback_poll_interval: float = 5.0
) -> Optional[Dict[str, Any]]:
    """
    等待单次 webhook 回调结果（兼容旧 API）

    注意：此函数只等待一次回调。如果第三方服务会发送多次回调，
    请使用 WebhookAwaiter 的 wait_until() 或 iter_callbacks() 方法。

    Args:
        redis_client: Redis 客户端
        namespace: 命名空间
        callback_id: 回调 ID
        timeout: 超时时间（秒），默认 300 秒
        fallback_poll_interval: 兜底轮询间隔（秒），默认 5 秒（已废弃，保留兼容）

    Returns:
        Dict[str, Any]: webhook 载荷数据，超时返回 None
    """
    awaiter = WebhookAwaiter(
        redis_client=redis_client,
        namespace=namespace,
        base_url="",  # 不需要构建 URL
        callback_id=callback_id
    )

    async with awaiter:
        return await awaiter.wait_next(timeout=timeout)
