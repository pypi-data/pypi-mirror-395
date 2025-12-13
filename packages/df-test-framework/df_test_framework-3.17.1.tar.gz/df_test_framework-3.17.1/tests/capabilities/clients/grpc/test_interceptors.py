"""测试 gRPC 拦截器"""

import pytest

from df_test_framework.capabilities.clients.grpc.interceptors import (
    LoggingInterceptor,
    MetadataInterceptor,
    RetryInterceptor,
    TimingInterceptor,
)


class TestLoggingInterceptor:
    """测试 LoggingInterceptor"""

    def test_intercept_unary_request(self) -> None:
        """测试拦截请求"""
        interceptor = LoggingInterceptor(log_request=True, log_response=False)

        request = {"name": "test"}
        metadata = [("key", "value")]

        result_request, result_metadata = interceptor.intercept_unary(
            "TestMethod", request, metadata
        )

        assert result_request == request
        assert result_metadata == metadata

    def test_intercept_response(self) -> None:
        """测试拦截响应"""
        interceptor = LoggingInterceptor(log_request=False, log_response=True)

        response = {"result": "success"}
        metadata = {"request-id": "123"}

        result_response = interceptor.intercept_response("TestMethod", response, metadata)

        assert result_response == response


class TestMetadataInterceptor:
    """测试 MetadataInterceptor"""

    def test_add_metadata(self) -> None:
        """测试添加元数据"""
        interceptor = MetadataInterceptor()
        interceptor.add_metadata("Authorization", "Bearer token123")

        assert "Authorization" in interceptor.metadata
        assert interceptor.metadata["Authorization"] == "Bearer token123"

    def test_remove_metadata(self) -> None:
        """测试移除元数据"""
        interceptor = MetadataInterceptor({"key": "value"})
        interceptor.remove_metadata("key")

        assert "key" not in interceptor.metadata

    def test_intercept_unary_combines_metadata(self) -> None:
        """测试拦截器合并元数据"""
        interceptor = MetadataInterceptor(
            {
                "Authorization": "Bearer token",
                "X-Request-ID": "123",
            }
        )

        request = {}
        metadata = [("Content-Type", "application/grpc")]

        _, result_metadata = interceptor.intercept_unary("TestMethod", request, metadata)

        # 验证元数据已合并
        assert len(result_metadata) == 3
        assert ("Content-Type", "application/grpc") in result_metadata
        assert ("Authorization", "Bearer token") in result_metadata
        assert ("X-Request-ID", "123") in result_metadata


class TestRetryInterceptor:
    """测试 RetryInterceptor"""

    def test_default_retry_configuration(self) -> None:
        """测试默认重试配置"""
        interceptor = RetryInterceptor()

        assert interceptor.max_retries == 3
        assert interceptor.retry_on_codes == [14]  # UNAVAILABLE
        assert interceptor.backoff_multiplier == 2.0
        assert interceptor.initial_backoff == 0.1

    def test_custom_retry_configuration(self) -> None:
        """测试自定义重试配置"""
        interceptor = RetryInterceptor(
            max_retries=5,
            retry_on_codes=[14, 13],  # UNAVAILABLE, INTERNAL
            backoff_multiplier=1.5,
            initial_backoff=0.5,
        )

        assert interceptor.max_retries == 5
        assert interceptor.retry_on_codes == [14, 13]
        assert interceptor.backoff_multiplier == 1.5
        assert interceptor.initial_backoff == 0.5

    def test_should_retry(self) -> None:
        """测试是否应该重试"""
        interceptor = RetryInterceptor(retry_on_codes=[14, 13])

        assert interceptor.should_retry(14) is True
        assert interceptor.should_retry(13) is True
        assert interceptor.should_retry(5) is False  # NOT_FOUND

    def test_calculate_backoff(self) -> None:
        """测试计算退避时间"""
        interceptor = RetryInterceptor(
            initial_backoff=1.0,
            backoff_multiplier=2.0,
        )

        assert interceptor.calculate_backoff(0) == 1.0  # 1.0 * 2^0
        assert interceptor.calculate_backoff(1) == 2.0  # 1.0 * 2^1
        assert interceptor.calculate_backoff(2) == 4.0  # 1.0 * 2^2
        assert interceptor.calculate_backoff(3) == 8.0  # 1.0 * 2^3


class TestTimingInterceptor:
    """测试 TimingInterceptor"""

    def test_intercept_unary_adds_start_time(self) -> None:
        """测试拦截器添加开始时间"""
        interceptor = TimingInterceptor()

        request = {}
        metadata = []

        _, result_metadata = interceptor.intercept_unary("TestMethod", request, metadata)

        # 验证添加了开始时间
        assert len(result_metadata) == 1
        assert result_metadata[0][0] == "x-start-time"
        assert float(result_metadata[0][1]) > 0

    def test_intercept_response_calculates_duration(self) -> None:
        """测试拦截器计算耗时"""
        import time

        interceptor = TimingInterceptor()

        # 模拟请求
        request = {}
        metadata = []
        _, metadata_with_time = interceptor.intercept_unary("TestMethod", request, metadata)

        # 等待一小段时间
        time.sleep(0.01)

        # 模拟响应
        response = {"result": "ok"}
        response_metadata = dict(metadata_with_time)

        interceptor.intercept_response("TestMethod", response, response_metadata)

        # 验证记录了耗时
        assert "TestMethod" in interceptor.timings
        assert len(interceptor.timings["TestMethod"]) == 1
        assert interceptor.timings["TestMethod"][0] >= 0.01

    def test_get_average_timing(self) -> None:
        """测试获取平均耗时"""
        interceptor = TimingInterceptor()

        # 手动添加一些耗时记录
        interceptor.timings["TestMethod"] = [0.1, 0.2, 0.3]

        average = interceptor.get_average_timing("TestMethod")
        assert average == pytest.approx(0.2)

    def test_get_average_timing_nonexistent_method(self) -> None:
        """测试获取不存在方法的耗时"""
        interceptor = TimingInterceptor()

        average = interceptor.get_average_timing("NonExistentMethod")
        assert average is None

    def test_get_all_timings(self) -> None:
        """测试获取所有耗时统计"""
        interceptor = TimingInterceptor()

        # 手动添加耗时记录
        interceptor.timings["Method1"] = [0.1, 0.2, 0.3]
        interceptor.timings["Method2"] = [0.5, 0.6]

        all_timings = interceptor.get_all_timings()

        assert "Method1" in all_timings
        assert "Method2" in all_timings

        assert all_timings["Method1"]["count"] == 3
        assert all_timings["Method1"]["average"] == pytest.approx(0.2)
        assert all_timings["Method1"]["min"] == pytest.approx(0.1)
        assert all_timings["Method1"]["max"] == pytest.approx(0.3)
        assert all_timings["Method1"]["total"] == pytest.approx(0.6)

        assert all_timings["Method2"]["count"] == 2
        assert all_timings["Method2"]["average"] == pytest.approx(0.55)
