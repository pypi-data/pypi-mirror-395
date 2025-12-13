"""
空操作 Telemetry 实现

用于禁用可观测性或测试场景。
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from df_test_framework.core.protocols.telemetry import ISpan, ITelemetry


class NoopSpan(ISpan):
    """空操作 Span"""

    def set_attribute(self, key: str, value: Any) -> None:
        """设置属性（空操作）"""
        pass

    def record_exception(self, exception: Exception) -> None:
        """记录异常（空操作）"""
        pass

    def end(self) -> None:
        """结束 Span（空操作）"""
        pass


class NoopTelemetry(ITelemetry):
    """空操作 Telemetry 实现

    用于禁用可观测性或测试场景。
    所有操作都是空操作，不产生任何副作用。

    示例:
        telemetry = NoopTelemetry()

        async with telemetry.span("test") as span:
            span.set_attribute("key", "value")  # 无操作
    """

    @asynccontextmanager
    async def span(
        self,
        name: str,
        attributes: dict[str, Any] | None = None,
        *,
        record_exception: bool = True,
        log_level: str = "DEBUG",
    ) -> AsyncIterator[ISpan]:
        """创建空操作 Span"""
        yield NoopSpan()

    def inject_context(self, carrier: dict[str, str]) -> None:
        """注入上下文（空操作）"""
        pass

    def extract_context(self, carrier: dict[str, str]) -> None:
        """提取上下文（空操作）"""
        return None
