"""
遥测导出器

支持多种导出后端：
- Console: 控制台输出
- OTLP: OpenTelemetry Protocol
- Jaeger: Jaeger 追踪系统
- Prometheus: Prometheus 指标

注意：这些导出器需要安装对应的可选依赖。
"""

# 导出器将在需要时实现
# from df_test_framework.infrastructure.telemetry.exporters.console import ConsoleExporter
# from df_test_framework.infrastructure.telemetry.exporters.otlp import OtlpExporter

__all__: list[str] = []
