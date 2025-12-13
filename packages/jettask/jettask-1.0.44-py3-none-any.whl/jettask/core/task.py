from ..utils.serializer import dumps_str, loads_str
import inspect
from dataclasses import dataclass
from typing import Any, Optional, TYPE_CHECKING, get_type_hints, Union

if TYPE_CHECKING:
    from .app import Jettask

from .context import TaskContext


@dataclass
class ExecuteResponse:
    delay: Optional[float] = None 
    urgent_retry: bool = False 
    reject: bool = False
    retry_time: Optional[float] = None


class Request:
    id: str = None
    name: str = None
    app: "Jettask" = None

    def __init__(self, *args, **kwargs) -> None:
        self._update(*args, **kwargs)

    def _update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)


class Task:
    _app: "Jettask" = None
    name: str = None
    queue: str = None
    trigger_time: float = None
    retry_config: Optional[dict] = None  # 存储任务级别的重试配置

    def __call__(self, event_id: str, trigger_time: float, queue: str,
                 group_name: Optional[str] = None,
                 scheduled_task_id: Optional[int] = None,
                 metadata: Optional[dict] = None,
                 *args: Any, **kwds: Any) -> Any:
        # 检查函数签名以进行依赖注入
        injected_args, injected_kwargs = self._inject_dependencies(
            event_id, trigger_time, queue, group_name, scheduled_task_id, metadata, args, kwds
        )
        return self.run(*injected_args, **injected_kwargs)

    def _inject_dependencies(self, event_id: str, trigger_time: float, queue: str,
                            group_name: Optional[str], scheduled_task_id: Optional[int],
                            metadata: Optional[dict],
                            args: tuple, kwargs: dict) -> tuple:
        """
        基于类型注解自动注入TaskContext
        """
        import logging
        logger = logging.getLogger(__name__)

        # 获取run方法的签名
        try:
            sig = inspect.signature(self.run)
            type_hints = get_type_hints(self.run)
            logger.debug(f"[TaskContext注入] 任务 {self.name} - 签名: {sig}, 类型提示: {type_hints}")
        except (ValueError, TypeError, NameError) as e:
            # 如果获取签名失败，返回原始参数
            logger.warning(f"[TaskContext注入] 任务 {self.name} - 获取签名失败: {e}")
            return args, kwargs
        
        # 创建TaskContext实例
        # group_name 和 scheduled_task_id 作为方法参数传入，不再从 kwargs 中提取
        # metadata 包含所有任务元数据
        context = TaskContext(
            event_id=event_id,
            name=self.name,
            trigger_time=trigger_time,
            app=self._app,
            queue=queue,  # 优先使用真实队列名，fallback到任务定义的队列
            scheduled_task_id=scheduled_task_id,  # 从参数直接传递
            group_name=group_name,  # 从参数直接传递
            metadata=metadata or {},  # 🔧 传递元数据字典
            # worker_id和retry_count可以从其他地方获取
            # 暂时使用默认值
        )
        
        # 构建最终的参数列表
        params_list = list(sig.parameters.items())
        final_args = []
        final_kwargs = dict(kwargs)  # 保留原有的kwargs
        args_list = list(args)
        args_consumed = 0  # 记录已消费的原始参数数量
        
        for idx, (param_name, param) in enumerate(params_list):
            # 跳过self参数
            if param_name == 'self':
                continue
            
            # 检查参数类型是否是TaskContext
            param_type = type_hints.get(param_name)
            
            # 如果是仅关键字参数
            if param.kind == param.KEYWORD_ONLY:
                if param_type is TaskContext and param_name not in final_kwargs:
                    final_kwargs[param_name] = context
                # 关键字参数不影响位置参数的处理
                continue
            
            # 处理位置参数
            if param.kind in (param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD):
                if param_type is TaskContext:
                    # 这是一个TaskContext参数，注入context
                    final_args.append(context)
                elif param_name in final_kwargs:
                    # 如果在kwargs中已经有这个参数，跳过（kwargs优先）
                    continue
                elif args_consumed < len(args_list):
                    # 使用原始参数列表中的下一个参数
                    final_args.append(args_list[args_consumed])
                    args_consumed += 1
                else:
                    # 没有更多的位置参数了，结束
                    break
        
        # 如果还有剩余的位置参数，添加到末尾（处理*args的情况）
        if args_consumed < len(args_list):
            final_args.extend(args_list[args_consumed:])

        logger.debug(f"[TaskContext注入] 任务 {self.name} - 注入后参数: args={final_args}, kwargs={list(final_kwargs.keys())}")

        return tuple(final_args), final_kwargs

    def run(self, *args, **kwargs):
        """The body of the task executed by workers."""
        raise NotImplementedError("Tasks must define the run method.")

    @classmethod
    def bind_app(cls, app):
        cls._app = app

    @property
    def is_wildcard_queue(self) -> bool:
        """
        检测当前 task 是否使用通配符队列

        Returns:
            bool: 如果队列模式是通配符（如 'test*', '*', 'queue_*'），返回 True；否则返回 False

        Examples:
            >>> task = Task()
            >>> task.queue = "test*"
            >>> task.is_wildcard_queue
            True
            >>> task.queue = "static_queue"
            >>> task.is_wildcard_queue
            False
        """
        from ..utils.queue_matcher import is_wildcard_pattern

        if not self.queue:
            return False

        return is_wildcard_pattern(self.queue)


    def on_before(self, event_id, pedding_count, args, kwargs) -> ExecuteResponse:
        return ExecuteResponse()

    def on_end(self, event_id, pedding_count, args, kwargs, result) -> ExecuteResponse:
        return ExecuteResponse()

    def on_success(self, event_id, args, kwargs, result) -> ExecuteResponse:
        return ExecuteResponse()

    def read_pending(
        self,
        queue: str = None,
        asyncio: bool = False,
    ):
        queue = queue or self.queue
        if asyncio:
            return self._get_pending(queue)
        return self._app.ep.read_pending(queue, queue)

    async def _get_pending(self, queue: str):
        return await self._app.ep.read_pending(queue, queue, asyncio=True)

