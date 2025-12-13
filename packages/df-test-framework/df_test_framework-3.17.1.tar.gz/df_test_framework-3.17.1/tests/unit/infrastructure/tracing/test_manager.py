"""TracingManager 单元测试

测试追踪管理器的核心功能
"""

import pytest


def _otel_available() -> bool:
    """检查OpenTelemetry是否可用"""
    try:
        from df_test_framework.infrastructure.tracing.manager import OTEL_AVAILABLE

        return OTEL_AVAILABLE
    except ImportError:
        return False


class TestTracingConfig:
    """TracingConfig 测试"""

    def test_default_config(self):
        """测试默认配置"""
        from df_test_framework.infrastructure.tracing.manager import TracingConfig

        config = TracingConfig()

        assert config.service_name == "df-test-framework"
        assert config.enabled is True
        assert config.batch_export is True
        assert config.sample_rate == 1.0

    def test_custom_config(self):
        """测试自定义配置"""
        from df_test_framework.infrastructure.tracing.exporters import ExporterType
        from df_test_framework.infrastructure.tracing.manager import TracingConfig

        config = TracingConfig(
            service_name="my-service",
            exporter_type=ExporterType.OTLP,
            endpoint="http://localhost:4317",
            batch_export=False,
            sample_rate=0.5,
            enabled=True,
            extra_attributes={"env": "test"},
        )

        assert config.service_name == "my-service"
        assert config.exporter_type == ExporterType.OTLP
        assert config.endpoint == "http://localhost:4317"
        assert config.batch_export is False
        assert config.sample_rate == 0.5
        assert config.extra_attributes == {"env": "test"}


class TestTracingManagerWithoutOtel:
    """TracingManager 测试（无 OpenTelemetry）"""

    def test_init_without_otel_raises_error(self):
        """测试未安装OTEL时初始化抛出错误"""
        from df_test_framework.infrastructure.tracing.manager import OTEL_AVAILABLE, TracingManager

        if not OTEL_AVAILABLE:
            manager = TracingManager()
            with pytest.raises(ImportError, match="OpenTelemetry"):
                manager.init()


@pytest.mark.skipif(not _otel_available(), reason="OpenTelemetry not installed")
class TestTracingManagerWithOtel:
    """TracingManager 测试（有 OpenTelemetry）"""

    def test_init_creates_provider(self):
        """测试初始化创建TracerProvider"""
        from df_test_framework.infrastructure.tracing.exporters import ExporterType
        from df_test_framework.infrastructure.tracing.manager import TracingConfig, TracingManager

        manager = TracingManager(
            config=TracingConfig(
                service_name="test-service",
                exporter_type=ExporterType.NONE,  # 使用NoOp导出器
                batch_export=False,
            )
        )

        # 验证初始化
        assert not manager.is_initialized
        manager.init()
        assert manager.is_initialized
        assert manager.is_enabled

        # 清理
        manager.shutdown()
        assert not manager.is_initialized

    def test_start_span_creates_span(self):
        """测试创建span"""
        from df_test_framework.infrastructure.tracing.exporters import ExporterType
        from df_test_framework.infrastructure.tracing.manager import TracingConfig, TracingManager

        manager = TracingManager(
            config=TracingConfig(
                service_name="test-service", exporter_type=ExporterType.NONE, batch_export=False
            )
        )
        manager.init()

        try:
            with manager.start_span("test_operation", attributes={"key": "value"}) as span:
                assert span is not None
                assert span.is_recording()
        finally:
            manager.shutdown()

    def test_add_event(self):
        """测试添加事件"""
        from df_test_framework.infrastructure.tracing.exporters import ExporterType
        from df_test_framework.infrastructure.tracing.manager import TracingConfig, TracingManager

        manager = TracingManager(
            config=TracingConfig(
                service_name="test-service", exporter_type=ExporterType.NONE, batch_export=False
            )
        )
        manager.init()

        try:
            with manager.start_span("test_operation"):
                manager.add_event("test_event", {"attr": "value"})
                # 事件已添加（无异常）
        finally:
            manager.shutdown()

    def test_disabled_tracing(self):
        """测试禁用追踪"""
        from df_test_framework.infrastructure.tracing.manager import TracingConfig, TracingManager

        config = TracingConfig(service_name="test-service", enabled=False)
        manager = TracingManager(config=config)
        manager.init()

        assert manager.is_initialized
        assert not manager.is_enabled

        manager.shutdown()


class TestGlobalTracingManager:
    """全局追踪管理器测试"""

    def test_get_default_manager(self):
        """测试获取默认管理器"""
        # 重置全局管理器
        import df_test_framework.infrastructure.tracing.manager as manager_module
        from df_test_framework.infrastructure.tracing.manager import (
            get_tracing_manager,
        )

        manager_module._default_manager = None

        manager = get_tracing_manager()
        assert manager is not None
        assert isinstance(manager, manager_module.TracingManager)

    def test_set_custom_manager(self):
        """测试设置自定义管理器"""
        from df_test_framework.infrastructure.tracing.manager import (
            TracingManager,
            get_tracing_manager,
            set_tracing_manager,
        )

        custom_manager = TracingManager(service_name="custom-service")
        set_tracing_manager(custom_manager)

        retrieved = get_tracing_manager()
        assert retrieved is custom_manager
        assert retrieved.config.service_name == "custom-service"


def _otel_available() -> bool:
    """检查OpenTelemetry是否可用"""
    try:
        from df_test_framework.infrastructure.tracing.manager import OTEL_AVAILABLE

        return OTEL_AVAILABLE
    except ImportError:
        return False
