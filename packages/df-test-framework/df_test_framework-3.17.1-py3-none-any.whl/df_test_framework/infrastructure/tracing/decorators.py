"""追踪装饰器

提供便捷的函数/方法追踪装饰器

v3.10.0 新增 - P2.1 OpenTelemetry分布式追踪
"""

from __future__ import annotations

import functools
import inspect
from collections.abc import Callable
from typing import Any, TypeVar

from .manager import OTEL_AVAILABLE, get_tracing_manager

if OTEL_AVAILABLE:
    from opentelemetry import trace

F = TypeVar("F", bound=Callable[..., Any])


def trace_span(
    name: str | None = None,
    attributes: dict[str, Any] | None = None,
    record_args: bool = False,
    record_result: bool = False,
) -> Callable[[F], F]:
    """同步函数追踪装饰器

    为函数创建追踪span，自动记录执行时间和异常

    Args:
        name: span名称（默认使用函数名）
        attributes: 静态属性
        record_args: 是否记录函数参数
        record_result: 是否记录返回值

    Returns:
        装饰器函数

    示例:
        >>> @trace_span()
        >>> def get_user(user_id: int):
        ...     return {"id": user_id, "name": "Alice"}
        >>>
        >>> @trace_span("fetch_user", attributes={"component": "user_service"})
        >>> def fetch_user(user_id: int):
        ...     return api.get(f"/users/{user_id}")
        >>>
        >>> @trace_span(record_args=True, record_result=True)
        >>> def calculate(a: int, b: int) -> int:
        ...     return a + b
    """

    def decorator(func: F) -> F:
        span_name = name or func.__name__

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            manager = get_tracing_manager()

            # 准备span属性
            span_attrs = dict(attributes) if attributes else {}
            span_attrs["code.function"] = func.__name__
            span_attrs["code.namespace"] = func.__module__

            # 记录参数
            if record_args:
                sig = inspect.signature(func)
                bound = sig.bind(*args, **kwargs)
                bound.apply_defaults()

                for param_name, param_value in bound.arguments.items():
                    # 只记录可序列化的简单类型
                    if isinstance(param_value, (str, int, float, bool)):
                        span_attrs[f"arg.{param_name}"] = param_value
                    else:
                        span_attrs[f"arg.{param_name}"] = str(type(param_value).__name__)

            with manager.start_span(span_name, attributes=span_attrs) as span:
                try:
                    result = func(*args, **kwargs)

                    # 记录返回值
                    if record_result and result is not None:
                        if isinstance(result, (str, int, float, bool)):
                            span.set_attribute("result", result)
                        else:
                            span.set_attribute("result.type", type(result).__name__)

                    return result

                except Exception as e:
                    # 记录异常
                    span.record_exception(e)
                    if OTEL_AVAILABLE:
                        span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                    raise

        return wrapper  # type: ignore

    return decorator


def trace_async_span(
    name: str | None = None,
    attributes: dict[str, Any] | None = None,
    record_args: bool = False,
    record_result: bool = False,
) -> Callable[[F], F]:
    """异步函数追踪装饰器

    为异步函数创建追踪span

    Args:
        name: span名称（默认使用函数名）
        attributes: 静态属性
        record_args: 是否记录函数参数
        record_result: 是否记录返回值

    Returns:
        装饰器函数

    示例:
        >>> @trace_async_span()
        >>> async def fetch_user(user_id: int):
        ...     return await api.get(f"/users/{user_id}")
        >>>
        >>> @trace_async_span("async_calculate", record_result=True)
        >>> async def async_calculate(a: int, b: int) -> int:
        ...     await asyncio.sleep(0.1)
        ...     return a + b
    """

    def decorator(func: F) -> F:
        span_name = name or func.__name__

        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            manager = get_tracing_manager()

            # 准备span属性
            span_attrs = dict(attributes) if attributes else {}
            span_attrs["code.function"] = func.__name__
            span_attrs["code.namespace"] = func.__module__
            span_attrs["code.async"] = True

            # 记录参数
            if record_args:
                sig = inspect.signature(func)
                bound = sig.bind(*args, **kwargs)
                bound.apply_defaults()

                for param_name, param_value in bound.arguments.items():
                    if isinstance(param_value, (str, int, float, bool)):
                        span_attrs[f"arg.{param_name}"] = param_value
                    else:
                        span_attrs[f"arg.{param_name}"] = str(type(param_value).__name__)

            with manager.start_span(span_name, attributes=span_attrs) as span:
                try:
                    result = await func(*args, **kwargs)

                    # 记录返回值
                    if record_result and result is not None:
                        if isinstance(result, (str, int, float, bool)):
                            span.set_attribute("result", result)
                        else:
                            span.set_attribute("result.type", type(result).__name__)

                    return result

                except Exception as e:
                    span.record_exception(e)
                    if OTEL_AVAILABLE:
                        span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                    raise

        return wrapper  # type: ignore

    return decorator


class TraceClass:
    """类方法追踪装饰器

    为类的所有公共方法添加追踪

    示例:
        >>> @TraceClass(prefix="UserService")
        >>> class UserService:
        ...     def get_user(self, user_id: int):
        ...         return {"id": user_id}
        ...
        ...     def create_user(self, name: str):
        ...         return {"name": name}
        >>>
        >>> # 所有公共方法都会被追踪:
        >>> # - UserService.get_user
        >>> # - UserService.create_user
    """

    def __init__(
        self, prefix: str | None = None, exclude: list[str] | None = None, record_args: bool = False
    ):
        """初始化类追踪装饰器

        Args:
            prefix: span名称前缀（默认使用类名）
            exclude: 排除的方法名列表
            record_args: 是否记录方法参数
        """
        self.prefix = prefix
        self.exclude = exclude or []
        self.record_args = record_args

    def __call__(self, cls: type) -> type:
        """应用追踪到类

        Args:
            cls: 目标类

        Returns:
            装饰后的类
        """
        prefix = self.prefix or cls.__name__

        # 使用 vars(cls) 或 cls.__dict__ 只获取类自身定义的属性，避免继承的方法
        for attr_name, attr in vars(cls).items():
            # 跳过私有方法和排除的方法
            if attr_name.startswith("_") or attr_name in self.exclude:
                continue

            # 只装饰可调用对象
            if not callable(attr):
                continue

            # 检查是否是方法
            if inspect.isfunction(attr) or inspect.ismethod(attr):
                span_name = f"{prefix}.{attr_name}"

                # 检查是否是异步方法
                if inspect.iscoroutinefunction(attr):
                    decorated = trace_async_span(span_name, record_args=self.record_args)(attr)
                else:
                    decorated = trace_span(span_name, record_args=self.record_args)(attr)

                setattr(cls, attr_name, decorated)

        return cls


__all__ = [
    "trace_span",
    "trace_async_span",
    "TraceClass",
]
