"""
可观测性协议定义

Telemetry = Tracing + Metrics + Logging
"""

from contextlib import AbstractAsyncContextManager
from typing import Any, Protocol


class ISpan(Protocol):
    """Span 协议"""

    def set_attribute(self, key: str, value: Any) -> None:
        """设置属性"""
        ...

    def record_exception(self, exception: Exception) -> None:
        """记录异常"""
        ...

    def end(self) -> None:
        """结束 Span"""
        ...


class ITracer(Protocol):
    """Tracer 协议"""

    def start_span(
        self,
        name: str,
        attributes: dict[str, Any] | None = None,
    ) -> ISpan:
        """创建 Span"""
        ...

    def inject(self, carrier: dict[str, str]) -> None:
        """注入上下文到载体"""
        ...

    def extract(self, carrier: dict[str, str]) -> Any:
        """从载体提取上下文"""
        ...


class IMeter(Protocol):
    """Meter 协议"""

    def record_histogram(
        self,
        name: str,
        value: float,
        attributes: dict[str, Any] | None = None,
    ) -> None:
        """记录直方图"""
        ...

    def increment_counter(
        self,
        name: str,
        attributes: dict[str, Any] | None = None,
        amount: int = 1,
    ) -> None:
        """增加计数器"""
        ...

    def set_gauge(
        self,
        name: str,
        value: float,
        attributes: dict[str, Any] | None = None,
    ) -> None:
        """设置仪表盘"""
        ...


class ILogger(Protocol):
    """Logger 协议"""

    def debug(self, message: str, **kwargs: Any) -> None:
        """DEBUG 日志"""
        ...

    def info(self, message: str, **kwargs: Any) -> None:
        """INFO 日志"""
        ...

    def warning(self, message: str, **kwargs: Any) -> None:
        """WARNING 日志"""
        ...

    def error(self, message: str, **kwargs: Any) -> None:
        """ERROR 日志"""
        ...

    def log(self, level: str, message: str, **kwargs: Any) -> None:
        """通用日志"""
        ...


class ITelemetry(Protocol):
    """统一可观测性协议

    融合 Tracer + Meter + Logger
    """

    def span(
        self,
        name: str,
        attributes: dict[str, Any] | None = None,
        *,
        record_exception: bool = True,
        log_level: str = "DEBUG",
    ) -> AbstractAsyncContextManager[ISpan]:
        """创建追踪 Span，同时记录指标和日志"""
        ...

    def inject_context(self, carrier: dict[str, str]) -> None:
        """注入追踪上下文到载体"""
        ...

    def extract_context(self, carrier: dict[str, str]) -> Any:
        """从载体提取追踪上下文"""
        ...
