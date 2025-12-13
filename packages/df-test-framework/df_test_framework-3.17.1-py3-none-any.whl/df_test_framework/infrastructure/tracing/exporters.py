"""追踪导出器配置

定义支持的追踪数据导出器类型

v3.10.0 新增 - P2.1 OpenTelemetry分布式追踪
"""

from __future__ import annotations

from enum import Enum
from typing import Any


class ExporterType(str, Enum):
    """导出器类型

    支持的追踪数据导出后端
    """

    CONSOLE = "console"
    """控制台输出，适合开发调试"""

    JAEGER = "jaeger"
    """Jaeger后端，需要运行Jaeger服务"""

    OTLP = "otlp"
    """OpenTelemetry Protocol，推荐使用"""

    ZIPKIN = "zipkin"
    """Zipkin后端"""

    NONE = "none"
    """不导出，仅用于测试"""


def create_exporter(exporter_type: ExporterType, endpoint: str | None = None, **kwargs: Any):
    """创建导出器实例

    Args:
        exporter_type: 导出器类型
        endpoint: 导出端点URL
        **kwargs: 额外配置参数

    Returns:
        SpanExporter实例

    Raises:
        ImportError: 未安装对应的导出器库
        ValueError: 不支持的导出器类型
    """
    if exporter_type == ExporterType.CONSOLE:
        from opentelemetry.sdk.trace.export import ConsoleSpanExporter

        return ConsoleSpanExporter()

    elif exporter_type == ExporterType.JAEGER:
        try:
            from opentelemetry.exporter.jaeger.thrift import JaegerExporter
        except ImportError:
            raise ImportError("Jaeger导出器需要安装: pip install opentelemetry-exporter-jaeger")

        # 默认Jaeger端点
        agent_host = kwargs.get("agent_host", "localhost")
        agent_port = kwargs.get("agent_port", 6831)

        return JaegerExporter(
            agent_host_name=agent_host,
            agent_port=agent_port,
        )

    elif exporter_type == ExporterType.OTLP:
        try:
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
        except ImportError:
            raise ImportError("OTLP导出器需要安装: pip install opentelemetry-exporter-otlp")

        # 默认OTLP端点
        otlp_endpoint = endpoint or "http://localhost:4317"

        return OTLPSpanExporter(
            endpoint=otlp_endpoint,
            insecure=kwargs.get("insecure", True),
        )

    elif exporter_type == ExporterType.ZIPKIN:
        try:
            from opentelemetry.exporter.zipkin.json import ZipkinExporter
        except ImportError:
            raise ImportError("Zipkin导出器需要安装: pip install opentelemetry-exporter-zipkin")

        # 默认Zipkin端点
        zipkin_endpoint = endpoint or "http://localhost:9411/api/v2/spans"

        return ZipkinExporter(endpoint=zipkin_endpoint)

    elif exporter_type == ExporterType.NONE:
        # 返回一个空操作的导出器
        from opentelemetry.sdk.trace import ReadableSpan
        from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult

        class NoOpExporter(SpanExporter):
            """空操作导出器，不执行任何导出操作"""

            def export(self, spans: list[ReadableSpan]) -> SpanExportResult:
                """导出 spans（不执行任何操作）"""
                return SpanExportResult.SUCCESS

            def shutdown(self) -> None:
                """关闭导出器"""
                pass

        return NoOpExporter()

    else:
        raise ValueError(f"不支持的导出器类型: {exporter_type}")


__all__ = ["ExporterType", "create_exporter"]
