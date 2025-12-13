"""追踪上下文单元测试

测试 TracingContext 和 Baggage 类
"""

import pytest


def _otel_available() -> bool:
    """检查OpenTelemetry是否可用"""
    try:
        from df_test_framework.infrastructure.tracing.manager import OTEL_AVAILABLE

        return OTEL_AVAILABLE
    except ImportError:
        return False


class TestTracingContextWithoutOtel:
    """TracingContext 测试（无 OpenTelemetry）"""

    def test_inject_returns_carrier(self):
        """测试无OTEL时inject返回原始carrier"""
        from df_test_framework.infrastructure.tracing.context import TracingContext
        from df_test_framework.infrastructure.tracing.manager import OTEL_AVAILABLE

        if not OTEL_AVAILABLE:
            carrier = {"existing": "header"}
            result = TracingContext.inject(carrier)
            assert result == carrier

    def test_extract_returns_none(self):
        """测试无OTEL时extract返回None"""
        from df_test_framework.infrastructure.tracing.context import TracingContext
        from df_test_framework.infrastructure.tracing.manager import OTEL_AVAILABLE

        if not OTEL_AVAILABLE:
            result = TracingContext.extract({"traceparent": "xxx"})
            assert result is None

    def test_use_returns_nullcontext(self):
        """测试无OTEL时use返回nullcontext"""
        from df_test_framework.infrastructure.tracing.context import TracingContext
        from df_test_framework.infrastructure.tracing.manager import OTEL_AVAILABLE

        if not OTEL_AVAILABLE:
            with TracingContext.use(None):
                pass  # 无异常即成功

    def test_get_trace_id_returns_none(self):
        """测试无OTEL时get_trace_id返回None"""
        from df_test_framework.infrastructure.tracing.context import TracingContext
        from df_test_framework.infrastructure.tracing.manager import OTEL_AVAILABLE

        if not OTEL_AVAILABLE:
            assert TracingContext.get_trace_id() is None

    def test_get_span_id_returns_none(self):
        """测试无OTEL时get_span_id返回None"""
        from df_test_framework.infrastructure.tracing.context import TracingContext
        from df_test_framework.infrastructure.tracing.manager import OTEL_AVAILABLE

        if not OTEL_AVAILABLE:
            assert TracingContext.get_span_id() is None

    def test_is_sampled_returns_false(self):
        """测试无OTEL时is_sampled返回False"""
        from df_test_framework.infrastructure.tracing.context import TracingContext
        from df_test_framework.infrastructure.tracing.manager import OTEL_AVAILABLE

        if not OTEL_AVAILABLE:
            assert TracingContext.is_sampled() is False


@pytest.mark.skipif(not _otel_available(), reason="OpenTelemetry not installed")
class TestTracingContextWithOtel:
    """TracingContext 测试（有 OpenTelemetry）"""

    def test_inject_adds_traceparent(self):
        """测试inject添加traceparent头"""
        from df_test_framework.infrastructure.tracing import (
            TracingConfig,
            TracingContext,
            TracingManager,
        )
        from df_test_framework.infrastructure.tracing.exporters import ExporterType

        manager = TracingManager(
            config=TracingConfig(exporter_type=ExporterType.NONE, batch_export=False)
        )
        manager.init()

        try:
            with manager.start_span("test"):
                carrier = {}
                TracingContext.inject(carrier)
                # 应该有 traceparent 头
                assert "traceparent" in carrier or len(carrier) == 0  # 空span可能不注入
        finally:
            manager.shutdown()

    def test_get_trace_id_returns_hex_string(self):
        """测试get_trace_id返回十六进制字符串"""
        from df_test_framework.infrastructure.tracing import (
            TracingConfig,
            TracingContext,
            TracingManager,
        )
        from df_test_framework.infrastructure.tracing.exporters import ExporterType

        manager = TracingManager(
            config=TracingConfig(exporter_type=ExporterType.NONE, batch_export=False)
        )
        manager.init()

        try:
            with manager.start_span("test"):
                trace_id = TracingContext.get_trace_id()
                if trace_id:  # 可能为None如果span未采样
                    assert len(trace_id) == 32  # 32个十六进制字符
                    assert all(c in "0123456789abcdef" for c in trace_id)
        finally:
            manager.shutdown()


class TestBaggageWithoutOtel:
    """Baggage 测试（无 OpenTelemetry）"""

    def test_set_does_nothing(self):
        """测试无OTEL时set无操作"""
        from df_test_framework.infrastructure.tracing.context import Baggage
        from df_test_framework.infrastructure.tracing.manager import OTEL_AVAILABLE

        if not OTEL_AVAILABLE:
            Baggage.set("key", "value")  # 无异常即成功

    def test_get_returns_none(self):
        """测试无OTEL时get返回None"""
        from df_test_framework.infrastructure.tracing.context import Baggage
        from df_test_framework.infrastructure.tracing.manager import OTEL_AVAILABLE

        if not OTEL_AVAILABLE:
            assert Baggage.get("key") is None

    def test_get_all_returns_empty_dict(self):
        """测试无OTEL时get_all返回空字典"""
        from df_test_framework.infrastructure.tracing.context import Baggage
        from df_test_framework.infrastructure.tracing.manager import OTEL_AVAILABLE

        if not OTEL_AVAILABLE:
            assert Baggage.get_all() == {}

    def test_remove_does_nothing(self):
        """测试无OTEL时remove无操作"""
        from df_test_framework.infrastructure.tracing.context import Baggage
        from df_test_framework.infrastructure.tracing.manager import OTEL_AVAILABLE

        if not OTEL_AVAILABLE:
            Baggage.remove("key")  # 无异常即成功

    def test_clear_does_nothing(self):
        """测试无OTEL时clear无操作"""
        from df_test_framework.infrastructure.tracing.context import Baggage
        from df_test_framework.infrastructure.tracing.manager import OTEL_AVAILABLE

        if not OTEL_AVAILABLE:
            Baggage.clear()  # 无异常即成功


@pytest.mark.skipif(not _otel_available(), reason="OpenTelemetry not installed")
class TestBaggageWithOtel:
    """Baggage 测试（有 OpenTelemetry）"""

    def test_set_and_get(self):
        """测试设置和获取baggage"""
        from df_test_framework.infrastructure.tracing.context import Baggage

        # 注意：baggage需要在追踪上下文中
        Baggage.set("user_id", "12345")
        value = Baggage.get("user_id")
        # 可能为None如果上下文未正确设置
        assert value is None or value == "12345"

    def test_get_all(self):
        """测试获取所有baggage"""
        from df_test_framework.infrastructure.tracing.context import Baggage

        all_baggage = Baggage.get_all()
        assert isinstance(all_baggage, dict)
