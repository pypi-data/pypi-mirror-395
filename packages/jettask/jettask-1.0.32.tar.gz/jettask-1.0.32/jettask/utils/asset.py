"""
资产获取工具类

提供给任务使用的资产获取和负载均衡功能
通过 HTTP API 获取资产列表，无需直接连接数据库
"""
import asyncio
import random
import logging
from typing import Optional, Dict, Any, List, Callable, Awaitable
from datetime import datetime, timezone
from dataclasses import dataclass, field
import httpx

logger = logging.getLogger(__name__)


@dataclass
class NodeStatus:
    """节点状态"""
    asset_id: int
    name: str
    url: str
    config: Dict[str, Any]
    weight: int
    queue_remaining: int = 0
    is_available: bool = True
    last_check: Optional[datetime] = None
    error: Optional[str] = None


@dataclass
class AssetInfo:
    """资产信息"""
    id: int
    name: str
    asset_type: str
    asset_group: str
    config: Dict[str, Any]
    status: str
    weight: int


@dataclass
class AssetCache:
    """资产缓存"""
    assets: List[AssetInfo] = field(default_factory=list)
    last_refresh: Optional[datetime] = None


class AssetClient:
    """
    资产客户端

    通过 HTTP API 获取和管理资产，提供负载均衡功能

    Example:
        ```python
        from jettask.utils.asset import AssetClient

        @app.task(queue="image_gen")
        async def generate_image(prompt: str):
            # 创建资产客户端（使用 API Key 认证）
            client = AssetClient(
                api_base_url="http://localhost:8080",
                namespace="default",
                api_key="your-api-key"
            )

            # 获取最空闲的 ComfyUI 节点
            node = await client.acquire_compute_node(
                asset_group="comfyui",
                max_queue=0,      # 只选择空闲节点
                timeout=600       # 等待最多 10 分钟
            )

            if node is None:
                raise Exception("没有可用的 ComfyUI 节点")

            # 使用节点
            result = await call_comfyui(node.url, prompt)
            return result
        ```
    """

    def __init__(
        self,
        api_base_url: str,
        namespace: str,
        api_key: Optional[str] = None,
        jwt_token: Optional[str] = None,
        cache_ttl: int = 60,
        http_timeout: float = 10.0
    ):
        """
        初始化资产客户端

        Args:
            api_base_url: API 基础 URL（如 http://localhost:8080）
            namespace: 命名空间
            api_key: API Key（X-API-Key 认证方式）
            jwt_token: JWT Token（Bearer Token 认证方式）
            cache_ttl: 资产列表缓存时间（秒）
            http_timeout: HTTP 请求超时时间（秒）

        Note:
            api_key 和 jwt_token 二选一，优先使用 api_key
        """
        self.api_base_url = api_base_url.rstrip('/')
        self.namespace = namespace
        self.api_key = api_key
        self.jwt_token = jwt_token
        self.cache_ttl = cache_ttl
        self.http_timeout = http_timeout
        self._cache: Dict[str, AssetCache] = {}

    def _get_auth_headers(self) -> Dict[str, str]:
        """获取认证请求头"""
        headers = {}
        if self.api_key:
            headers['X-API-Key'] = self.api_key
        elif self.jwt_token:
            headers['Authorization'] = f'Bearer {self.jwt_token}'
        return headers

    def _get_api_url(self, path: str) -> str:
        """构建 API URL"""
        return f"{self.api_base_url}/api/task/v1/{self.namespace}{path}"

    async def get_assets(
        self,
        asset_group: str,
        asset_type: Optional[str] = None,
        status: str = "active",
        use_cache: bool = True
    ) -> List[AssetInfo]:
        """
        获取资产列表

        Args:
            asset_group: 资产分组
            asset_type: 资产类型（可选）
            status: 状态筛选
            use_cache: 是否使用缓存

        Returns:
            资产列表
        """
        cache_key = f"{asset_group}:{asset_type}:{status}"

        # 检查缓存
        if use_cache and cache_key in self._cache:
            cache = self._cache[cache_key]
            if cache.last_refresh:
                age = (datetime.now(timezone.utc) - cache.last_refresh).total_seconds()
                if age < self.cache_ttl:
                    return cache.assets

        # 通过 API 获取
        url = self._get_api_url(f"/assets/group/{asset_group}")
        params = {"status": status}
        headers = self._get_auth_headers()

        try:
            async with httpx.AsyncClient(timeout=self.http_timeout) as http_client:
                resp = await http_client.get(url, params=params, headers=headers)
                resp.raise_for_status()
                data = resp.json()

                assets = []
                for item in data.get("data", []):
                    # 按类型筛选
                    if asset_type and item.get("asset_type") != asset_type:
                        continue

                    assets.append(AssetInfo(
                        id=item["id"],
                        name=item["name"],
                        asset_type=item["asset_type"],
                        asset_group=item["asset_group"],
                        config=item.get("config", {}),
                        status=item["status"],
                        weight=item.get("weight", 1)
                    ))

                # 更新缓存
                self._cache[cache_key] = AssetCache(
                    assets=assets,
                    last_refresh=datetime.now(timezone.utc)
                )

                return assets

        except Exception as e:
            logger.error(f"获取资产列表失败: {e}")
            # 如果有缓存，返回缓存数据
            if cache_key in self._cache:
                return self._cache[cache_key].assets
            return []

    async def acquire_compute_node(
        self,
        asset_group: str,
        check_func: Optional[Callable[[str, Dict[str, Any]], Awaitable[int]]] = None,
        max_queue: int = 0,
        timeout: float = 300.0,
        poll_interval: float = 5.0,
        strategy: str = "least_busy"
    ) -> Optional[NodeStatus]:
        """
        获取计算节点（带负载均衡）

        会检查所有节点的负载情况，选择最空闲的节点。
        如果所有节点都忙，会等待直到有空闲节点或超时。

        Args:
            asset_group: 资产分组（如 "comfyui"）
            check_func: 检查节点队列的异步函数，签名: async (url, config) -> queue_remaining
                        如果不提供，使用默认的 ComfyUI 检查函数
            max_queue: 最大允许的队列数，为 0 表示只选择空闲节点
            timeout: 等待超时时间（秒）
            poll_interval: 轮询间隔（秒）
            strategy: 选择策略
                - "least_busy": 选择队列最少的节点（默认）
                - "random": 从可用节点中随机选择
                - "weighted": 按权重加权随机选择

        Returns:
            NodeStatus: 选中的节点状态，超时返回 None

        Example:
            ```python
            # 使用默认的 ComfyUI 检查函数
            node = await client.acquire_compute_node("comfyui")

            # 使用自定义检查函数
            async def check_sd_webui(url, config):
                async with httpx.AsyncClient() as client:
                    resp = await client.get(f"{url}/sdapi/v1/progress")
                    data = resp.json()
                    return 1 if data.get("state", {}).get("job") else 0

            node = await client.acquire_compute_node(
                "sd_webui",
                check_func=check_sd_webui
            )
            ```
        """
        if check_func is None:
            check_func = self._default_comfyui_check

        start_time = asyncio.get_event_loop().time()

        while True:
            # 检查超时
            elapsed = asyncio.get_event_loop().time() - start_time
            if elapsed >= timeout:
                logger.warning(f"获取计算节点超时: asset_group={asset_group}")
                return None

            # 获取所有活跃的计算节点
            assets = await self.get_assets(
                asset_group=asset_group,
                asset_type="compute_node",
                status="active",
                use_cache=False  # 获取节点时不使用缓存，确保状态最新
            )

            if not assets:
                logger.warning(f"没有可用的计算节点: asset_group={asset_group}")
                await asyncio.sleep(poll_interval)
                continue

            # 检查每个节点的状态
            node_statuses: List[NodeStatus] = []

            for asset in assets:
                url = asset.config.get("url", "")
                if not url:
                    continue

                status = NodeStatus(
                    asset_id=asset.id,
                    name=asset.name,
                    url=url,
                    config=asset.config,
                    weight=asset.weight,
                    last_check=datetime.now(timezone.utc)
                )

                try:
                    queue_remaining = await check_func(url, asset.config)
                    status.queue_remaining = queue_remaining
                    status.is_available = queue_remaining <= max_queue
                except Exception as e:
                    status.is_available = False
                    status.error = str(e)
                    logger.warning(f"检查节点 {asset.name} 失败: {e}")

                node_statuses.append(status)

            # 筛选可用节点
            available_nodes = [n for n in node_statuses if n.is_available]

            if not available_nodes:
                logger.debug(
                    f"所有节点都忙，等待 {poll_interval} 秒后重试... "
                    f"(节点状态: {[(n.name, n.queue_remaining) for n in node_statuses]})"
                )
                await asyncio.sleep(poll_interval)
                continue

            # 根据策略选择节点
            selected = self._select_node(available_nodes, strategy)

            logger.info(
                f"选中计算节点: {selected.name} (queue={selected.queue_remaining}, "
                f"可用节点数={len(available_nodes)}/{len(node_statuses)})"
            )

            return selected

    def _select_node(self, nodes: List[NodeStatus], strategy: str) -> NodeStatus:
        """根据策略选择节点"""
        if strategy == "random":
            return random.choice(nodes)

        elif strategy == "weighted":
            # 按权重加权随机
            total_weight = sum(n.weight for n in nodes)
            if total_weight == 0:
                return random.choice(nodes)

            r = random.uniform(0, total_weight)
            cumulative = 0
            for node in nodes:
                cumulative += node.weight
                if r <= cumulative:
                    return node
            return nodes[-1]

        else:  # least_busy（默认）
            # 选择队列最少的，队列相同时按权重选择
            nodes.sort(key=lambda n: (n.queue_remaining, -n.weight))
            return nodes[0]

    async def get_api_key(
        self,
        asset_group: str,
        strategy: str = "random"
    ) -> Optional[Dict[str, Any]]:
        """
        获取 API 密钥

        Args:
            asset_group: 资产分组（如 "openai"）
            strategy: 选择策略
                - "random": 随机选择（默认）
                - "weighted": 按权重选择

        Returns:
            包含 asset_id, name, config 的字典，或 None
        """
        assets = await self.get_assets(
            asset_group=asset_group,
            asset_type="api_key",
            status="active"
        )

        if not assets:
            return None

        if strategy == "weighted":
            # 按权重加权随机
            total_weight = sum(a.weight for a in assets)
            if total_weight == 0:
                selected = random.choice(assets)
            else:
                r = random.uniform(0, total_weight)
                cumulative = 0
                selected = assets[-1]
                for asset in assets:
                    cumulative += asset.weight
                    if r <= cumulative:
                        selected = asset
                        break
        else:  # random
            selected = random.choice(assets)

        return {
            "asset_id": selected.id,
            "name": selected.name,
            "config": selected.config
        }

    async def get_config(
        self,
        asset_group: str,
        name: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        获取配置项

        Args:
            asset_group: 资产分组
            name: 配置名称（可选，不指定则返回第一个）

        Returns:
            配置字典，或 None
        """
        assets = await self.get_assets(
            asset_group=asset_group,
            asset_type="config",
            status="active"
        )

        if not assets:
            return None

        if name:
            for asset in assets:
                if asset.name == name:
                    return asset.config
            return None

        return assets[0].config

    @staticmethod
    async def _default_comfyui_check(url: str, config: Dict[str, Any]) -> int:
        """
        默认的 ComfyUI 队列检查函数

        调用 GET /prompt 接口，返回 queue_remaining
        """
        timeout = config.get("timeout", 5.0)

        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.get(f"{url}/prompt")
            resp.raise_for_status()
            data = resp.json()
            return data.get("exec_info", {}).get("queue_remaining", 0)

    def clear_cache(self):
        """清空缓存"""
        self._cache.clear()


# 便捷函数
async def acquire_comfyui_node(
    api_base_url: str,
    namespace: str,
    asset_group: str = "comfyui",
    max_queue: int = 0,
    timeout: float = 300.0,
    api_key: Optional[str] = None,
    jwt_token: Optional[str] = None
) -> Optional[NodeStatus]:
    """
    获取 ComfyUI 节点的便捷函数

    Args:
        api_base_url: API 基础 URL（如 http://localhost:8080）
        namespace: 命名空间
        asset_group: 资产分组，默认 "comfyui"
        max_queue: 最大允许的队列数
        timeout: 超时时间
        api_key: API Key 认证（可选）
        jwt_token: JWT Token 认证（可选）

    Returns:
        NodeStatus 或 None

    Example:
        ```python
        from jettask.utils.asset import acquire_comfyui_node

        @app.task(queue="image_gen")
        async def generate_image(prompt: str):
            node = await acquire_comfyui_node(
                api_base_url="http://localhost:8080",
                namespace="default",
                api_key="your-api-key",
                timeout=600
            )

            if node is None:
                raise Exception("没有可用的 ComfyUI 节点")

            # 使用节点
            result = await call_comfyui(node.url, prompt)
            return result
        ```
    """
    client = AssetClient(api_base_url, namespace, api_key=api_key, jwt_token=jwt_token)
    return await client.acquire_compute_node(
        asset_group=asset_group,
        max_queue=max_queue,
        timeout=timeout
    )


async def get_api_key(
    api_base_url: str,
    namespace: str,
    asset_group: str,
    api_key: Optional[str] = None,
    jwt_token: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    获取 API 密钥的便捷函数

    Args:
        api_base_url: API 基础 URL
        namespace: 命名空间
        asset_group: 资产分组（如 "openai"）
        api_key: API Key 认证（可选）
        jwt_token: JWT Token 认证（可选）

    Returns:
        包含 asset_id, name, config 的字典，或 None

    Example:
        ```python
        from jettask.utils.asset import get_api_key

        @app.task(queue="chat")
        async def chat(message: str):
            key_info = await get_api_key(
                api_base_url="http://localhost:8080",
                namespace="default",
                asset_group="openai",
                api_key="your-api-key"
            )

            if key_info is None:
                raise Exception("没有可用的 OpenAI Key")

            api_key = key_info["config"]["api_key"]
            # 使用 API Key
            ...
        ```
    """
    client = AssetClient(api_base_url, namespace, api_key=api_key, jwt_token=jwt_token)
    return await client.get_api_key(asset_group)
