"""追踪拦截器测试

测试 HTTP 和 gRPC 追踪拦截器的功能
"""

import pytest

from df_test_framework.infrastructure.tracing.interceptors import (
    GrpcTracingInterceptor,
    SpanContextCarrier,
    TracingInterceptor,
)


class TestTracingInterceptorBasic:
    """HTTP 追踪拦截器基础测试"""

    def test_create_interceptor(self):
        """测试创建拦截器"""
        interceptor = TracingInterceptor()

        assert interceptor.name == "TracingInterceptor"
        assert interceptor.priority == 10
        assert interceptor.propagate_context is True
        assert interceptor.record_headers is False
        assert interceptor.record_body is False

    def test_create_interceptor_with_custom_config(self):
        """测试自定义配置"""
        interceptor = TracingInterceptor(
            name="CustomTracing",
            priority=5,
            record_headers=True,
            record_body=True,
            propagate_context=False,
            sensitive_headers=["x-custom-secret"],
        )

        assert interceptor.name == "CustomTracing"
        assert interceptor.priority == 5
        assert interceptor.record_headers is True
        assert interceptor.record_body is True
        assert interceptor.propagate_context is False
        assert "x-custom-secret" in interceptor.sensitive_headers

    def test_default_sensitive_headers(self):
        """测试默认敏感头列表"""
        interceptor = TracingInterceptor()

        assert "authorization" in interceptor.sensitive_headers
        assert "x-api-key" in interceptor.sensitive_headers
        assert "cookie" in interceptor.sensitive_headers


class TestSpanContextCarrier:
    """SpanContextCarrier 测试"""

    def test_set_and_get(self):
        """测试设置和获取"""
        SpanContextCarrier.clear()

        span_mock = object()
        start_time = 1234567890.123

        SpanContextCarrier.set(span_mock, start_time)

        retrieved_span, retrieved_time = SpanContextCarrier.get()
        assert retrieved_span is span_mock
        assert retrieved_time == start_time

    def test_clear(self):
        """测试清除"""
        span_mock = object()
        SpanContextCarrier.set(span_mock, 123.0)

        SpanContextCarrier.clear()

        span, start_time = SpanContextCarrier.get()
        assert span is None
        assert start_time is None


class TestGrpcTracingInterceptorBasic:
    """gRPC 追踪拦截器基础测试"""

    def test_create_interceptor(self):
        """测试创建拦截器"""
        interceptor = GrpcTracingInterceptor()

        assert interceptor.propagate_context is True
        assert interceptor.record_metadata is False

    def test_create_interceptor_with_custom_config(self):
        """测试自定义配置"""
        interceptor = GrpcTracingInterceptor(
            record_metadata=True,
            propagate_context=False,
            sensitive_keys=["x-custom-key"],
        )

        assert interceptor.record_metadata is True
        assert interceptor.propagate_context is False
        assert "x-custom-key" in interceptor.sensitive_keys

    def test_default_sensitive_keys(self):
        """测试默认敏感键列表"""
        interceptor = GrpcTracingInterceptor()

        assert "authorization" in interceptor.sensitive_keys
        assert "x-api-key" in interceptor.sensitive_keys
        assert "cookie" in interceptor.sensitive_keys

    def test_parse_method(self):
        """测试解析 gRPC 方法名"""
        interceptor = GrpcTracingInterceptor()

        # 标准格式
        service, method = interceptor._parse_method("/package.UserService/GetUser")
        assert service == "package.UserService"
        assert method == "GetUser"

        # 简单格式
        service, method = interceptor._parse_method("/MyService/DoSomething")
        assert service == "MyService"
        assert method == "DoSomething"

        # 无效格式
        service, method = interceptor._parse_method("invalid")
        assert service == "invalid"
        assert method == "unknown"

    def test_sanitize_value(self):
        """测试脱敏功能"""
        interceptor = GrpcTracingInterceptor(sensitive_keys=["secret-key"])

        # 敏感键
        result = interceptor._sanitize_value("secret-key", "my-secret-value")
        assert result == "***"

        # 非敏感键
        result = interceptor._sanitize_value("normal-key", "normal-value")
        assert result == "normal-value"

    def test_intercept_unary_without_otel(self):
        """测试无 OpenTelemetry 时的行为"""
        interceptor = GrpcTracingInterceptor()

        request = {"user_id": 123}
        metadata = [("x-request-id", "abc-123")]

        # 即使没有 OTEL，也应该正常返回
        result_request, result_metadata = interceptor.intercept_unary(
            "/UserService/GetUser", request, metadata
        )

        # 请求应该不变
        assert result_request == request

    def test_intercept_response_without_otel(self):
        """测试无 OpenTelemetry 时的响应拦截"""
        interceptor = GrpcTracingInterceptor()

        response = {"name": "Alice"}
        metadata = {"grpc-status": "0"}

        # 应该正常返回响应
        result = interceptor.intercept_response("/UserService/GetUser", response, metadata)
        assert result == response

    def test_build_request_attributes(self):
        """测试构建请求属性"""
        interceptor = GrpcTracingInterceptor(record_metadata=True)

        attrs = interceptor._build_request_attributes(
            full_method="/package.UserService/GetUser",
            service_name="package.UserService",
            method_name="GetUser",
            metadata=[("x-request-id", "abc-123"), ("authorization", "Bearer token")],
        )

        assert attrs["rpc.system"] == "grpc"
        assert attrs["rpc.service"] == "package.UserService"
        assert attrs["rpc.method"] == "GetUser"
        assert attrs["rpc.grpc.full_method"] == "/package.UserService/GetUser"

        # 验证元数据记录（非敏感键）
        assert attrs.get("rpc.request.metadata.x-request-id") == "abc-123"
        # 验证敏感键脱敏
        assert attrs.get("rpc.request.metadata.authorization") == "***"

    def test_build_request_attributes_without_metadata(self):
        """测试不记录元数据"""
        interceptor = GrpcTracingInterceptor(record_metadata=False)

        attrs = interceptor._build_request_attributes(
            full_method="/UserService/GetUser",
            service_name="UserService",
            method_name="GetUser",
            metadata=[("x-request-id", "abc-123")],
        )

        # 不应该包含元数据属性
        assert "rpc.request.metadata.x-request-id" not in attrs


class TestInterceptorImports:
    """测试拦截器导入"""

    def test_import_from_interceptors_package(self):
        """测试从 interceptors 包导入"""
        from df_test_framework.infrastructure.tracing.interceptors import (
            GrpcTracingInterceptor,
            SpanContextCarrier,
            TracingInterceptor,
        )

        assert TracingInterceptor is not None
        assert SpanContextCarrier is not None
        assert GrpcTracingInterceptor is not None

    def test_import_directly(self):
        """测试直接导入"""
        from df_test_framework.infrastructure.tracing.interceptors.grpc import (
            GrpcTracingInterceptor,
        )
        from df_test_framework.infrastructure.tracing.interceptors.http import (
            TracingInterceptor,
        )

        assert TracingInterceptor is not None
        assert GrpcTracingInterceptor is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
