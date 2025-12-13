"""追踪装饰器单元测试

测试 trace_span 和 trace_async_span 装饰器
"""

import asyncio

import pytest


def _otel_available() -> bool:
    """检查OpenTelemetry是否可用"""
    try:
        from df_test_framework.infrastructure.tracing.manager import OTEL_AVAILABLE

        return OTEL_AVAILABLE
    except ImportError:
        return False


@pytest.mark.skipif(not _otel_available(), reason="OpenTelemetry not installed")
class TestTraceSpanDecorator:
    """trace_span 装饰器测试"""

    def test_decorator_without_args(self):
        """测试无参数装饰器"""
        from df_test_framework.infrastructure.tracing.decorators import trace_span

        @trace_span()
        def my_function():
            return "result"

        result = my_function()
        assert result == "result"

    def test_decorator_with_name(self):
        """测试带名称的装饰器"""
        from df_test_framework.infrastructure.tracing.decorators import trace_span

        @trace_span("custom_name")
        def my_function():
            return 42

        result = my_function()
        assert result == 42

    def test_decorator_with_attributes(self):
        """测试带属性的装饰器"""
        from df_test_framework.infrastructure.tracing.decorators import trace_span

        @trace_span("operation", attributes={"key": "value"})
        def my_function(x, y):
            return x + y

        result = my_function(1, 2)
        assert result == 3

    def test_decorator_records_args(self):
        """测试记录参数"""
        from df_test_framework.infrastructure.tracing.decorators import trace_span

        @trace_span(record_args=True)
        def my_function(name: str, age: int):
            return f"{name} is {age}"

        result = my_function("Alice", 30)
        assert result == "Alice is 30"

    def test_decorator_records_result(self):
        """测试记录返回值"""
        from df_test_framework.infrastructure.tracing.decorators import trace_span

        @trace_span(record_result=True)
        def calculate(a: int, b: int) -> int:
            return a * b

        result = calculate(5, 6)
        assert result == 30

    def test_decorator_handles_exception(self):
        """测试异常处理"""
        from df_test_framework.infrastructure.tracing.decorators import trace_span

        @trace_span()
        def failing_function():
            raise ValueError("test error")

        with pytest.raises(ValueError, match="test error"):
            failing_function()

    def test_decorator_preserves_function_metadata(self):
        """测试保留函数元数据"""
        from df_test_framework.infrastructure.tracing.decorators import trace_span

        @trace_span("my_op")
        def documented_function():
            """This is the docstring."""
            pass

        assert documented_function.__name__ == "documented_function"
        assert documented_function.__doc__ == "This is the docstring."


@pytest.mark.skipif(not _otel_available(), reason="OpenTelemetry not installed")
class TestTraceAsyncSpanDecorator:
    """trace_async_span 装饰器测试"""

    @pytest.mark.asyncio
    async def test_async_decorator_without_args(self):
        """测试无参数异步装饰器"""
        from df_test_framework.infrastructure.tracing.decorators import trace_async_span

        @trace_async_span()
        async def my_async_function():
            await asyncio.sleep(0.01)
            return "async_result"

        result = await my_async_function()
        assert result == "async_result"

    @pytest.mark.asyncio
    async def test_async_decorator_with_name(self):
        """测试带名称的异步装饰器"""
        from df_test_framework.infrastructure.tracing.decorators import trace_async_span

        @trace_async_span("async_custom_name")
        async def my_async_function():
            return 100

        result = await my_async_function()
        assert result == 100

    @pytest.mark.asyncio
    async def test_async_decorator_records_args(self):
        """测试异步装饰器记录参数"""
        from df_test_framework.infrastructure.tracing.decorators import trace_async_span

        @trace_async_span(record_args=True)
        async def fetch_user(user_id: int):
            await asyncio.sleep(0.01)
            return {"id": user_id, "name": "Test User"}

        result = await fetch_user(123)
        assert result == {"id": 123, "name": "Test User"}

    @pytest.mark.asyncio
    async def test_async_decorator_handles_exception(self):
        """测试异步异常处理"""
        from df_test_framework.infrastructure.tracing.decorators import trace_async_span

        @trace_async_span()
        async def failing_async_function():
            await asyncio.sleep(0.01)
            raise RuntimeError("async error")

        with pytest.raises(RuntimeError, match="async error"):
            await failing_async_function()


@pytest.mark.skipif(not _otel_available(), reason="OpenTelemetry not installed")
class TestTraceClass:
    """TraceClass 装饰器测试"""

    def test_class_decorator_traces_methods(self):
        """测试类装饰器追踪方法"""
        from df_test_framework.infrastructure.tracing.decorators import TraceClass

        @TraceClass(prefix="MyService")
        class MyService:
            def get_data(self):
                return "data"

            def process(self, value: int):
                return value * 2

        service = MyService()
        assert service.get_data() == "data"
        assert service.process(5) == 10

    def test_class_decorator_excludes_methods(self):
        """测试类装饰器排除方法"""
        from df_test_framework.infrastructure.tracing.decorators import TraceClass

        @TraceClass(exclude=["helper"])
        class MyService:
            def main_method(self):
                return "main"

            def helper(self):
                return "helper"

        service = MyService()
        assert service.main_method() == "main"
        assert service.helper() == "helper"

    def test_class_decorator_skips_private_methods(self):
        """测试类装饰器跳过私有方法"""
        from df_test_framework.infrastructure.tracing.decorators import TraceClass

        @TraceClass()
        class MyService:
            def public_method(self):
                return "public"

            def _private_method(self):
                return "private"

            def __dunder_method__(self):
                return "dunder"

        service = MyService()
        assert service.public_method() == "public"
        assert service._private_method() == "private"

    @pytest.mark.asyncio
    async def test_class_decorator_handles_async_methods(self):
        """测试类装饰器处理异步方法"""
        from df_test_framework.infrastructure.tracing.decorators import TraceClass

        @TraceClass(prefix="AsyncService")
        class AsyncService:
            async def fetch(self):
                await asyncio.sleep(0.01)
                return "fetched"

            def sync_method(self):
                return "sync"

        service = AsyncService()
        assert await service.fetch() == "fetched"
        assert service.sync_method() == "sync"

    def test_class_decorator_with_record_args(self):
        """测试类装饰器记录参数"""
        from df_test_framework.infrastructure.tracing.decorators import TraceClass

        @TraceClass(record_args=True)
        class Calculator:
            def add(self, a: int, b: int) -> int:
                return a + b

            def multiply(self, x: int, y: int) -> int:
                return x * y

        calc = Calculator()
        assert calc.add(2, 3) == 5
        assert calc.multiply(4, 5) == 20
