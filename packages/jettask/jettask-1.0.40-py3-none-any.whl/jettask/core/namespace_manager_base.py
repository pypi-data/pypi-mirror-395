"""
命名空间管理器基类
为 Consumer 和 Scheduler 提供统一的命名空间管理逻辑
"""
import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from jettask.core.namespace import NamespaceManagerAPI, NamespaceContext

logger = logging.getLogger(__name__)


class NamespaceWorkerManagerBase(ABC):
    """
    命名空间工作器管理器基类

    提供统一的命名空间管理逻辑，子类只需实现具体的工作器运行逻辑。

    核心功能：
    1. 自动检测单/多命名空间模式
    2. 统一的命名空间配置获取
    3. 命名空间动态检测和管理
    4. 资源清理
    """

    def __init__(self,
                 task_center_url: str,
                 check_interval: int = 30,
                 debug: bool = False,
                 api_key: Optional[str] = None,
                 **kwargs):
        """
        初始化管理器基类

        Args:
            task_center_url: 任务中心URL
                - 单命名空间: http://localhost:8001/api/task/v1/namespace_name
                - 多命名空间: http://localhost:8001 或 http://localhost:8001/api
            check_interval: 命名空间检测间隔（秒）
            debug: 是否启用调试模式
            api_key: API密钥（用于请求鉴权）
            **kwargs: 子类特定的参数
        """
        self.task_center_url = task_center_url.rstrip('/')
        self.check_interval = check_interval
        self.debug = debug
        self.api_key = api_key

        # 检测模式
        self.is_single_namespace, self.namespace_name = self._detect_mode()

        # 命名空间管理器
        self.namespace_manager: Optional[NamespaceManagerAPI] = None

        # 运行状态
        self.running = False

        # 子类特定参数存储
        self._extra_params = kwargs

        logger.info(f"{self.__class__.__name__} 初始化完成")
        logger.info(f"  模式: {'单命名空间' if self.is_single_namespace else '多命名空间'}")
        if self.is_single_namespace:
            logger.info(f"  命名空间: {self.namespace_name}")
        logger.info(f"  任务中心: {self.task_center_url}")
        if self.api_key:
            logger.info(f"  鉴权: 已启用")

    def _detect_mode(self) -> tuple[bool, Optional[str]]:
        """
        检测是单命名空间还是多命名空间模式

        Returns:
            (is_single, namespace_name)
        """
        import re

        # 检查新格式: /api/task/v1/{namespace}
        match = re.search(r'/api/task/v1/([^/]+)/?$', self.task_center_url)
        if match:
            namespace_name = match.group(1)
            logger.info(f"检测到单命名空间模式: {namespace_name}")
            return True, namespace_name

        # 多命名空间模式
        logger.info("检测到多命名空间模式")
        return False, None

    def _get_base_url(self) -> str:
        """
        获取任务中心的基础URL（用于创建 NamespaceManagerAPI）

        Returns:
            基础URL（去除命名空间路径）
        """
        if self.is_single_namespace:
            # 从 http://localhost:8001/api/task/v1/default 提取 http://localhost:8001
            return self.task_center_url.rsplit('/api/task/v1/', 1)[0]

        # 多命名空间模式，移除末尾的 /api 或 /api/task 或 /api/task/v1
        url = self.task_center_url
        for suffix in ['/api/task/v1', '/api/task', '/api']:
            if url.endswith(suffix):
                url = url[:-len(suffix)]
                break

        return url

    @abstractmethod
    async def _run_worker_for_namespace(self, ns: NamespaceContext):
        """
        为单个命名空间运行工作器（子类必须实现）

        Args:
            ns: 命名空间上下文
        """
        pass

    @abstractmethod
    def _should_start_worker(self, ns: NamespaceContext) -> bool:
        """
        判断是否应该为命名空间启动工作器（子类必须实现）

        Args:
            ns: 命名空间上下文

        Returns:
            是否应该启动
        """
        pass

    @abstractmethod
    async def _start_worker(self, ns_or_name: Any):
        """
        启动工作器（子类必须实现）

        Args:
            ns_or_name: 命名空间上下文或名称（根据单/多命名空间模式不同）
        """
        pass

    @abstractmethod
    async def _stop_worker(self, ns_name: str):
        """
        停止工作器（子类必须实现）

        Args:
            ns_name: 命名空间名称
        """
        pass

    @abstractmethod
    def _get_running_workers(self) -> set[str]:
        """
        获取当前运行的工作器列表（子类必须实现）

        Returns:
            命名空间名称集合
        """
        pass

    async def _namespace_check_loop(self):
        """命名空间检查循环 - 检测新的命名空间（仅多命名空间模式）"""
        logger.info("命名空间检查循环已启动")

        while self.running:
            try:
                # 刷新命名空间列表
                await self.namespace_manager.refresh()
                namespaces = await self.namespace_manager.list_namespaces(enabled_only=True)

                # 获取当前所有应该运行的命名空间
                current_ns_map = {
                    ns.name: ns for ns in namespaces
                    if self._should_start_worker(ns)
                }
                current_namespaces = set(current_ns_map.keys())
                known_namespaces = self._get_running_workers()

                # 发现新命名空间
                new_namespaces = current_namespaces - known_namespaces
                if new_namespaces:
                    logger.info(f"发现新命名空间: {new_namespaces}")
                    for ns_name in new_namespaces:
                        ns = current_ns_map[ns_name]
                        await self._start_worker(ns)

                # 停止已删除的命名空间工作器
                removed_namespaces = known_namespaces - current_namespaces
                if removed_namespaces:
                    logger.info(f"命名空间已删除或禁用: {removed_namespaces}")
                    for ns_name in removed_namespaces:
                        await self._stop_worker(ns_name)

                # 等待下一次检查
                await asyncio.sleep(self.check_interval)

            except Exception as e:
                logger.error(f"命名空间检查循环异常: {e}", exc_info=self.debug)
                await asyncio.sleep(10)

    async def run(self):
        """
        运行管理器（统一的运行逻辑，自动处理单/多命名空间）

        核心思想：
        - 单命名空间: 在当前进程/任务中直接运行工作器
        - 多命名空间: 为每个命名空间启动独立的工作器
        """
        try:
            self.running = True

            # 获取基础URL并创建命名空间管理器
            base_url = self._get_base_url()
            self.namespace_manager = NamespaceManagerAPI(base_url, api_key=self.api_key)

            if self.is_single_namespace:
                # ==================== 单命名空间模式 ====================
                logger.info(f"单命名空间模式: {self.namespace_name}")

                # 获取命名空间上下文
                ns = await self.namespace_manager.get_namespace(self.namespace_name)

                # 直接运行工作器
                await self._run_worker_for_namespace(ns)

            else:
                # ==================== 多命名空间模式 ====================
                logger.info("多命名空间模式")
                logger.info(f"命名空间检测间隔: {self.check_interval}秒")

                # 获取所有命名空间
                await self.namespace_manager.refresh()
                namespaces = await self.namespace_manager.list_namespaces(enabled_only=True)

                # 为每个命名空间启动工作器
                for ns in namespaces:
                    if self._should_start_worker(ns):
                        await self._start_worker(ns)
                    else:
                        logger.warning(f"跳过命名空间 {ns.name}: 配置不满足要求")

                # 启动命名空间检查循环
                namespace_check_task = asyncio.create_task(self._namespace_check_loop())

                # 等待任务完成或出错
                await namespace_check_task

        except KeyboardInterrupt:
            logger.info("收到中断信号，停止所有工作器...")
        except Exception as e:
            logger.error(f"运行错误: {e}", exc_info=self.debug)
            raise
        finally:
            self.running = False

            # 停止所有工作器
            for ns_name in list(self._get_running_workers()):
                await self._stop_worker(ns_name)

            # 关闭命名空间管理器
            if self.namespace_manager:
                await self.namespace_manager.close()

            logger.info("所有工作器已停止")


__all__ = ['NamespaceWorkerManagerBase']
