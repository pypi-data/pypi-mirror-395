"""
统一可观测性门面

融合 Tracer + Meter + Logger，一次埋点三份数据。
"""

import logging
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any

from df_test_framework.core.protocols.telemetry import ISpan, ITelemetry


@dataclass(frozen=True, slots=True)
class SpanContext:
    """Span 上下文"""

    trace_id: str
    span_id: str
    trace_flags: int = 0


class SimpleSpan(ISpan):
    """简单的 Span 实现（无依赖版本）"""

    def __init__(self, name: str, attributes: dict[str, Any] | None = None):
        self.name = name
        self._attributes = attributes.copy() if attributes else {}
        self._exception: Exception | None = None
        self._ended = False

    def set_attribute(self, key: str, value: Any) -> None:
        """设置属性"""
        self._attributes[key] = value

    def record_exception(self, exception: Exception) -> None:
        """记录异常"""
        self._exception = exception

    def end(self) -> None:
        """结束 Span"""
        self._ended = True

    @property
    def attributes(self) -> dict[str, Any]:
        """获取属性"""
        return self._attributes.copy()


class Telemetry(ITelemetry):
    """统一可观测性门面

    融合 Tracer + Meter + Logger，一次埋点三份数据。

    特性:
    - 一次 span() 调用自动记录 Trace Span、Histogram、Counter、Log
    - 支持上下文注入和提取
    - 异常自动捕获

    示例:
        telemetry = Telemetry(logger=logger)

        async with telemetry.span("http.request", {"method": "POST"}) as span:
            response = await send_request()
            span.set_attribute("status_code", response.status_code)

        # 自动记录：
        # - Log: Starting http.request / Completed http.request
        # - 如果有异常: ERROR log
    """

    def __init__(
        self,
        logger: logging.Logger | None = None,
        service_name: str = "df-test-framework",
        enable_tracing: bool = True,
        enable_metrics: bool = True,
        enable_logging: bool = True,
    ):
        """初始化 Telemetry

        Args:
            logger: 日志对象
            service_name: 服务名称
            enable_tracing: 是否启用追踪
            enable_metrics: 是否启用指标
            enable_logging: 是否启用日志
        """
        self._logger = logger or logging.getLogger(__name__)
        self._service_name = service_name
        self._enable_tracing = enable_tracing
        self._enable_metrics = enable_metrics
        self._enable_logging = enable_logging

        # 指标存储（简单实现）
        self._counters: dict[str, int] = {}
        self._histograms: dict[str, list[float]] = {}

    @asynccontextmanager
    async def span(
        self,
        name: str,
        attributes: dict[str, Any] | None = None,
        *,
        record_exception: bool = True,
        log_level: str = "DEBUG",
    ) -> AsyncIterator[ISpan]:
        """创建追踪 Span，同时记录指标和日志

        Args:
            name: Span 名称
            attributes: 初始属性
            record_exception: 是否记录异常
            log_level: 日志级别

        Yields:
            Span 对象

        示例:
            async with telemetry.span("db.query", {"table": "users"}) as span:
                result = await db.execute(query)
                span.set_attribute("row_count", len(result))
        """
        start = time.monotonic()
        span = SimpleSpan(name, attributes)

        if self._enable_logging:
            self._log(log_level, f"Starting {name}", extra=attributes)

        try:
            yield span

            # 成功：记录指标
            duration = time.monotonic() - start
            if self._enable_metrics:
                self._record_histogram(f"{name}.duration", duration, attributes)
                self._increment_counter(f"{name}.success", attributes)

            if self._enable_logging:
                self._log(
                    log_level,
                    f"Completed {name} in {duration:.3f}s",
                    extra=attributes,
                )

        except Exception as e:
            # 失败：记录异常
            duration = time.monotonic() - start
            if self._enable_metrics:
                self._record_histogram(f"{name}.duration", duration, attributes)
                self._increment_counter(f"{name}.error", attributes)

            if record_exception:
                span.record_exception(e)

            if self._enable_logging:
                self._logger.error(
                    f"Error in {name}: {e}",
                    extra=attributes,
                    exc_info=True,
                )
            raise
        finally:
            span.set_attribute("duration_ms", (time.monotonic() - start) * 1000)
            span.end()

    def inject_context(self, carrier: dict[str, str]) -> None:
        """注入追踪上下文到载体

        Args:
            carrier: 要注入的载体（如 HTTP Headers）
        """
        # 简单实现：从当前上下文获取信息
        from df_test_framework.core.context import get_current_context

        ctx = get_current_context()
        if ctx:
            carrier["X-Trace-Id"] = ctx.trace_id
            carrier["X-Span-Id"] = ctx.span_id
            carrier["X-Request-Id"] = ctx.request_id

    def extract_context(self, carrier: dict[str, str]) -> SpanContext | None:
        """从载体提取追踪上下文

        Args:
            carrier: 要提取的载体

        Returns:
            Span 上下文，未找到返回 None
        """
        trace_id = carrier.get("X-Trace-Id")
        span_id = carrier.get("X-Span-Id")

        if trace_id and span_id:
            return SpanContext(trace_id=trace_id, span_id=span_id)

        return None

    def _log(self, level: str, message: str, extra: dict[str, Any] | None = None) -> None:
        """记录日志"""
        log_method = getattr(self._logger, level.lower(), self._logger.debug)
        log_method(message, extra=extra or {})

    def _record_histogram(
        self,
        name: str,
        value: float,
        attributes: dict[str, Any] | None = None,
    ) -> None:
        """记录直方图"""
        key = f"{name}:{self._format_attributes(attributes)}"
        if key not in self._histograms:
            self._histograms[key] = []
        self._histograms[key].append(value)

    def _increment_counter(
        self,
        name: str,
        attributes: dict[str, Any] | None = None,
        amount: int = 1,
    ) -> None:
        """增加计数器"""
        key = f"{name}:{self._format_attributes(attributes)}"
        self._counters[key] = self._counters.get(key, 0) + amount

    def _format_attributes(self, attributes: dict[str, Any] | None) -> str:
        """格式化属性为字符串"""
        if not attributes:
            return ""
        return ",".join(f"{k}={v}" for k, v in sorted(attributes.items()))

    def get_counter(self, name: str) -> int:
        """获取计数器值（测试用）"""
        total = 0
        for key, value in self._counters.items():
            if key.startswith(f"{name}:"):
                total += value
        return total

    def get_histogram_values(self, name: str) -> list[float]:
        """获取直方图值（测试用）"""
        values = []
        for key, vals in self._histograms.items():
            if key.startswith(f"{name}:"):
                values.extend(vals)
        return values

    def reset_metrics(self) -> None:
        """重置所有指标（测试用）"""
        self._counters.clear()
        self._histograms.clear()
