"""导出器单元测试

测试 ExporterType 和 create_exporter 函数
"""

import pytest


def _otel_available() -> bool:
    """检查OpenTelemetry是否可用"""
    try:
        from df_test_framework.infrastructure.tracing.manager import OTEL_AVAILABLE

        return OTEL_AVAILABLE
    except ImportError:
        return False


class TestExporterType:
    """ExporterType 枚举测试"""

    def test_exporter_type_values(self):
        """测试导出器类型值"""
        from df_test_framework.infrastructure.tracing.exporters import ExporterType

        assert ExporterType.CONSOLE.value == "console"
        assert ExporterType.JAEGER.value == "jaeger"
        assert ExporterType.OTLP.value == "otlp"
        assert ExporterType.ZIPKIN.value == "zipkin"
        assert ExporterType.NONE.value == "none"

    def test_exporter_type_is_string_enum(self):
        """测试ExporterType是字符串枚举"""
        from df_test_framework.infrastructure.tracing.exporters import ExporterType

        # 可以用字符串比较
        assert ExporterType.CONSOLE == "console"
        assert ExporterType.OTLP == "otlp"


@pytest.mark.skipif(not _otel_available(), reason="OpenTelemetry not installed")
class TestCreateExporter:
    """create_exporter 函数测试"""

    def test_create_console_exporter(self):
        """测试创建控制台导出器"""
        from opentelemetry.sdk.trace.export import ConsoleSpanExporter

        from df_test_framework.infrastructure.tracing.exporters import ExporterType, create_exporter

        exporter = create_exporter(ExporterType.CONSOLE)
        assert isinstance(exporter, ConsoleSpanExporter)

    def test_create_none_exporter(self):
        """测试创建空操作导出器"""
        from opentelemetry.sdk.trace.export import SpanExporter

        from df_test_framework.infrastructure.tracing.exporters import ExporterType, create_exporter

        exporter = create_exporter(ExporterType.NONE)
        assert isinstance(exporter, SpanExporter)

    def test_create_jaeger_exporter_not_installed(self):
        """测试创建Jaeger导出器（未安装时）"""
        from df_test_framework.infrastructure.tracing.exporters import ExporterType, create_exporter

        try:
            import opentelemetry.exporter.jaeger.thrift  # noqa: F401

            # 如果已安装，跳过此测试
            pytest.skip("Jaeger exporter is installed")
        except ImportError:
            with pytest.raises(ImportError, match="Jaeger导出器需要安装"):
                create_exporter(ExporterType.JAEGER)

    def test_create_otlp_exporter_not_installed(self):
        """测试创建OTLP导出器（未安装时）"""
        from df_test_framework.infrastructure.tracing.exporters import ExporterType, create_exporter

        try:
            import opentelemetry.exporter.otlp.proto.grpc.trace_exporter  # noqa: F401

            # 如果已安装，跳过此测试
            pytest.skip("OTLP exporter is installed")
        except ImportError:
            with pytest.raises(ImportError, match="OTLP导出器需要安装"):
                create_exporter(ExporterType.OTLP)

    def test_create_zipkin_exporter_not_installed(self):
        """测试创建Zipkin导出器（未安装时）"""
        from df_test_framework.infrastructure.tracing.exporters import ExporterType, create_exporter

        try:
            import opentelemetry.exporter.zipkin.json  # noqa: F401

            # 如果已安装，跳过此测试
            pytest.skip("Zipkin exporter is installed")
        except ImportError:
            with pytest.raises(ImportError, match="Zipkin导出器需要安装"):
                create_exporter(ExporterType.ZIPKIN)

    def test_invalid_exporter_type(self):
        """测试无效导出器类型"""
        from df_test_framework.infrastructure.tracing.exporters import create_exporter

        with pytest.raises(ValueError, match="不支持的导出器类型"):
            create_exporter("invalid")
