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
            # 创建资产客户端
            client = AssetClient(
                api_base_url="http://localhost:8080",
                namespace="default"
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
        cache_ttl: int = 60,
        http_timeout: float = 10.0
    ):
        self.api_base_url = api_base_url.rstrip('/')
        self.namespace = namespace
        self.cache_ttl = cache_ttl
        self.http_timeout = http_timeout
        self._cache: Dict[str, AssetCache] = {}

    def _get_api_url(self, path: str) -> str:
        return f"{self.api_base_url}/api/task/v1/{self.namespace}{path}"

    async def get_assets(
        self,
        asset_group: str,
        asset_type: Optional[str] = None,
        status: str = "active",
        use_cache: bool = True
    ) -> List[AssetInfo]:
        cache_key = f"{asset_group}:{asset_type}:{status}"

        if use_cache and cache_key in self._cache:
            cache = self._cache[cache_key]
            if cache.last_refresh:
                age = (datetime.now(timezone.utc) - cache.last_refresh).total_seconds()
                if age < self.cache_ttl:
                    return cache.assets

        url = self._get_api_url(f"/assets/group/{asset_group}")
        params = {"status": status}

        try:
            async with httpx.AsyncClient(timeout=self.http_timeout) as http_client:
                resp = await http_client.get(url, params=params)
                resp.raise_for_status()
                data = resp.json()

                assets = []
                for item in data.get("data", []):
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

                self._cache[cache_key] = AssetCache(
                    assets=assets,
                    last_refresh=datetime.now(timezone.utc)
                )

                return assets

        except Exception as e:
            logger.error(f"获取资产列表失败: {e}")
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
        if check_func is None:
            check_func = self._default_comfyui_check

        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            if elapsed >= timeout:
                logger.warning(f"获取计算节点超时: asset_group={asset_group}")
                return None

            assets = await self.get_assets(
                asset_group=asset_group,
                asset_type="compute_node",
                status="active",
                use_cache=False  
            )

            if not assets:
                logger.warning(f"没有可用的计算节点: asset_group={asset_group}")
                await asyncio.sleep(poll_interval)
                continue

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

            available_nodes = [n for n in node_statuses if n.is_available]

            if not available_nodes:
                logger.debug(
                    f"所有节点都忙，等待 {poll_interval} 秒后重试... "
                    f"(节点状态: {[(n.name, n.queue_remaining) for n in node_statuses]})"
                )
                await asyncio.sleep(poll_interval)
                continue

            selected = self._select_node(available_nodes, strategy)

            logger.info(
                f"选中计算节点: {selected.name} (queue={selected.queue_remaining}, "
                f"可用节点数={len(available_nodes)}/{len(node_statuses)})"
            )

            return selected

    def _select_node(self, nodes: List[NodeStatus], strategy: str) -> NodeStatus:
        if strategy == "random":
            return random.choice(nodes)

        elif strategy == "weighted":
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

        else:  
            nodes.sort(key=lambda n: (n.queue_remaining, -n.weight))
            return nodes[0]

    async def get_api_key(
        self,
        asset_group: str,
        strategy: str = "random"
    ) -> Optional[Dict[str, Any]]:
        assets = await self.get_assets(
            asset_group=asset_group,
            asset_type="api_key",
            status="active"
        )

        if not assets:
            return None

        if strategy == "weighted":
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
        else:  
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
        timeout = config.get("timeout", 5.0)

        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.get(f"{url}/prompt")
            resp.raise_for_status()
            data = resp.json()
            return data.get("exec_info", {}).get("queue_remaining", 0)

    def clear_cache(self):
        self._cache.clear()


async def acquire_comfyui_node(
    api_base_url: str,
    namespace: str,
    asset_group: str = "comfyui",
    max_queue: int = 0,
    timeout: float = 300.0
) -> Optional[NodeStatus]:
    client = AssetClient(api_base_url, namespace)
    return await client.acquire_compute_node(
        asset_group=asset_group,
        max_queue=max_queue,
        timeout=timeout
    )


async def get_api_key(
    api_base_url: str,
    namespace: str,
    asset_group: str
) -> Optional[Dict[str, Any]]:
    client = AssetClient(api_base_url, namespace)
    return await client.get_api_key(asset_group)
