"""
测试 core.middleware - 统一中间件系统

v3.14.0 新增：
- Middleware 协议
- MiddlewareChain 链式调用
- BaseMiddleware, SyncMiddleware
- @middleware 装饰器
"""

import asyncio
import time

import pytest

from df_test_framework.core import MiddlewareAbort, MiddlewareError
from df_test_framework.core.middleware import (
    BaseMiddleware,
    MiddlewareChain,
    SyncMiddleware,
    middleware,
)


# ==================== 测试数据模型 ====================
class MockRequest:
    """测试请求对象"""

    def __init__(self, value: str):
        self.value = value
        self.headers: dict[str, str] = {}

    def with_header(self, key: str, value: str) -> "MockRequest":
        self.headers[key] = value
        return self


class MockResponse:
    """测试响应对象"""

    def __init__(self, value: str):
        self.value = value


# ==================== 测试中间件实现 ====================
class AddHeaderMiddleware(BaseMiddleware):
    """添加请求头的中间件"""

    def __init__(self, key: str, value: str, priority: int = 50):
        super().__init__(priority=priority)
        self.key = key
        self.value = value

    async def __call__(self, request: MockRequest, call_next) -> MockResponse:
        request.with_header(self.key, self.value)
        return await call_next(request)


class LoggingMiddleware(BaseMiddleware):
    """日志中间件"""

    def __init__(self, logs: list[str], priority: int = 100):
        super().__init__(priority=priority)
        self.logs = logs

    async def __call__(self, request: MockRequest, call_next) -> MockResponse:
        self.logs.append(f"before: {request.value}")
        response = await call_next(request)
        self.logs.append(f"after: {response.value}")
        return response


class TimingMiddleware(BaseMiddleware):
    """计时中间件（测试状态共享）"""

    def __init__(self, timings: dict[str, float], priority: int = 10):
        super().__init__(priority=priority)
        self.timings = timings

    async def __call__(self, request: MockRequest, call_next) -> MockResponse:
        start = time.monotonic()
        response = await call_next(request)
        duration = time.monotonic() - start
        self.timings[request.value] = duration
        return response


class ErrorMiddleware(BaseMiddleware):
    """测试异常处理的中间件"""

    async def __call__(self, request: MockRequest, call_next) -> MockResponse:
        try:
            return await call_next(request)
        except ValueError:
            raise MiddlewareError("Handled ValueError in middleware")


class AbortMiddleware(BaseMiddleware):
    """测试中止的中间件"""

    def __init__(self, abort_value: str, priority: int = 5):
        super().__init__(priority=priority)
        self.abort_value = abort_value

    async def __call__(self, request: MockRequest, call_next) -> MockResponse:
        if request.value == self.abort_value:
            raise MiddlewareAbort("Request aborted by AbortMiddleware")
        return await call_next(request)


# ==================== 测试 MiddlewareChain ====================
class TestMiddlewareChain:
    """测试 MiddlewareChain 链式调用"""

    @pytest.mark.asyncio
    async def test_empty_chain(self):
        """测试空链直接返回"""

        async def handler(req: MockRequest) -> MockResponse:
            return MockResponse(req.value)

        chain = MiddlewareChain(handler)
        request = MockRequest("test")

        response = await chain.execute(request)
        assert response.value == "test"

    @pytest.mark.asyncio
    async def test_single_middleware(self):
        """测试单个中间件"""

        async def handler(req: MockRequest) -> MockResponse:
            return MockResponse(req.value)

        chain = MiddlewareChain(handler)
        chain.use(AddHeaderMiddleware("X-Single", "value"))

        request = MockRequest("test")
        response = await chain.execute(request)
        assert "X-Single" in request.headers
        assert response.value == "test"

    @pytest.mark.asyncio
    async def test_multiple_middlewares_execution_order(self):
        """测试多个中间件按优先级执行（洋葱模型）"""
        logs: list[str] = []

        async def handler(req: MockRequest) -> MockResponse:
            return MockResponse(req.value)

        chain = MiddlewareChain(handler)
        chain.use(LoggingMiddleware(logs, priority=100))  # 内层
        chain.use(AddHeaderMiddleware("X-Header", "value", priority=50))
        chain.use(TimingMiddleware({}, priority=10))  # 外层

        request = MockRequest("test")
        response = await chain.execute(request)

        # 验证洋葱模型：before/after 记录
        assert logs == ["before: test", "after: test"]
        assert "X-Header" in request.headers
        assert response.value == "test"

    @pytest.mark.asyncio
    async def test_middleware_state_sharing(self):
        """测试中间件作用域内状态共享"""
        timings: dict[str, float] = {}

        async def handler(req: MockRequest) -> MockResponse:
            await asyncio.sleep(0.01)  # 模拟慢操作
            return MockResponse(req.value)

        chain = MiddlewareChain(handler)
        chain.use(TimingMiddleware(timings, priority=10))

        request = MockRequest("slow_operation")
        await chain.execute(request)

        # 验证计时记录
        assert "slow_operation" in timings
        assert timings["slow_operation"] > 0.01

    @pytest.mark.asyncio
    async def test_middleware_error_handling(self):
        """测试中间件异常处理"""

        async def handler(req: MockRequest) -> MockResponse:
            raise ValueError("Simulated error")

        chain = MiddlewareChain(handler)
        chain.use(ErrorMiddleware(priority=10))

        request = MockRequest("error_test")

        with pytest.raises(MiddlewareError, match="Handled ValueError"):
            await chain.execute(request)

    @pytest.mark.asyncio
    async def test_middleware_abort(self):
        """测试中间件中止执行"""
        logs: list[str] = []

        async def handler(req: MockRequest) -> MockResponse:
            return MockResponse("should not reach here")

        chain = MiddlewareChain(handler)
        chain.use(AbortMiddleware("abort_me", priority=5))  # 最外层
        chain.use(LoggingMiddleware(logs, priority=100))

        request = MockRequest("abort_me")

        with pytest.raises(MiddlewareAbort, match="Request aborted"):
            await chain.execute(request)

        # 验证日志中间件没有执行
        assert len(logs) == 0

    @pytest.mark.asyncio
    async def test_chain_use_returns_self(self):
        """测试 use() 方法返回自身（支持链式调用）"""

        async def handler(req: MockRequest) -> MockResponse:
            return MockResponse(req.value)

        chain = MiddlewareChain(handler)
        result = (
            chain.use(AddHeaderMiddleware("X-1", "v1"))
            .use(AddHeaderMiddleware("X-2", "v2"))
            .use(AddHeaderMiddleware("X-3", "v3"))
        )

        assert result is chain
        assert len(chain) == 3


# ==================== 测试 SyncMiddleware ====================
class TestSyncMiddleware:
    """测试 SyncMiddleware 同步中间件"""

    @pytest.mark.asyncio
    async def test_sync_middleware_before_only(self):
        """测试只有 before 的同步中间件"""

        class SyncAddHeaderMiddleware(SyncMiddleware):
            def before(self, request: MockRequest) -> MockRequest:
                return request.with_header("X-Sync", "sync_value")

        async def handler(req: MockRequest) -> MockResponse:
            return MockResponse(req.value)

        chain = MiddlewareChain(handler)
        chain.use(SyncAddHeaderMiddleware())

        request = MockRequest("test")
        response = await chain.execute(request)

        assert "X-Sync" in request.headers
        assert request.headers["X-Sync"] == "sync_value"
        assert response.value == "test"

    @pytest.mark.asyncio
    async def test_sync_middleware_with_after(self):
        """测试带 after 的同步中间件"""

        class SyncLoggingMiddleware(SyncMiddleware):
            def __init__(self, logs: list[str], priority: int = 50):
                super().__init__(priority=priority)
                self.logs = logs

            def before(self, request: MockRequest) -> MockRequest:
                self.logs.append(f"sync_before: {request.value}")
                return request

            def after(self, response: MockResponse) -> MockResponse:
                self.logs.append(f"sync_after: {response.value}")
                return response

        logs: list[str] = []

        async def handler(req: MockRequest) -> MockResponse:
            return MockResponse(req.value)

        chain = MiddlewareChain(handler)
        chain.use(SyncLoggingMiddleware(logs))

        request = MockRequest("sync_test")
        response = await chain.execute(request)

        assert logs == ["sync_before: sync_test", "sync_after: sync_test"]
        assert response.value == "sync_test"


# ==================== 测试 @middleware 装饰器 ====================
class TestMiddlewareDecorator:
    """测试 @middleware 装饰器"""

    @pytest.mark.asyncio
    async def test_function_middleware_basic(self):
        """测试函数式中间件"""

        @middleware(priority=50)
        async def add_timestamp(request: MockRequest, call_next):
            request.with_header("X-Timestamp", str(time.time()))
            return await call_next(request)

        async def handler(req: MockRequest) -> MockResponse:
            return MockResponse(req.value)

        chain = MiddlewareChain(handler)
        chain.use(add_timestamp)

        request = MockRequest("test")
        response = await chain.execute(request)

        assert "X-Timestamp" in request.headers
        assert response.value == "test"

    @pytest.mark.asyncio
    async def test_function_middleware_priority(self):
        """测试函数式中间件优先级"""
        logs: list[str] = []

        @middleware(priority=10)
        async def outer_middleware(request: MockRequest, call_next):
            logs.append("outer_before")
            response = await call_next(request)
            logs.append("outer_after")
            return response

        @middleware(priority=100)
        async def inner_middleware(request: MockRequest, call_next):
            logs.append("inner_before")
            response = await call_next(request)
            logs.append("inner_after")
            return response

        async def handler(req: MockRequest) -> MockResponse:
            return MockResponse(req.value)

        chain = MiddlewareChain(handler)
        chain.use(inner_middleware)
        chain.use(outer_middleware)

        request = MockRequest("test")
        await chain.execute(request)

        # 洋葱模型：outer → inner → handler → inner → outer
        assert logs == ["outer_before", "inner_before", "inner_after", "outer_after"]

    @pytest.mark.asyncio
    async def test_function_middleware_default_priority(self):
        """测试函数式中间件默认优先级"""

        @middleware()
        async def default_priority_middleware(request: MockRequest, call_next):
            request.with_header("X-Default", "value")
            return await call_next(request)

        # 验证默认优先级是 100
        assert default_priority_middleware.priority == 100

        async def handler(req: MockRequest) -> MockResponse:
            return MockResponse(req.value)

        chain = MiddlewareChain(handler)
        chain.use(default_priority_middleware)

        request = MockRequest("test")
        await chain.execute(request)
        assert "X-Default" in request.headers


# ==================== 测试复杂场景 ====================
class TestMiddlewareComplexScenarios:
    """测试复杂场景"""

    @pytest.mark.asyncio
    async def test_retry_middleware_pattern(self):
        """测试重试中间件模式"""
        attempt_count = {"value": 0}

        class RetryMiddleware(BaseMiddleware):
            def __init__(self, max_attempts: int = 3, priority: int = 5):
                super().__init__(priority=priority)
                self.max_attempts = max_attempts

            async def __call__(self, request: MockRequest, call_next) -> MockResponse:
                last_error = None
                for attempt in range(self.max_attempts):
                    try:
                        return await call_next(request)
                    except ValueError as e:
                        last_error = e
                        if attempt < self.max_attempts - 1:
                            await asyncio.sleep(0.01)
                raise MiddlewareError(f"Max retries exceeded: {last_error}")

        async def flaky_handler(req: MockRequest) -> MockResponse:
            attempt_count["value"] += 1
            if attempt_count["value"] < 3:
                raise ValueError("Temporary failure")
            return MockResponse("success")

        chain = MiddlewareChain(flaky_handler)
        chain.use(RetryMiddleware(max_attempts=3))

        request = MockRequest("retry_test")
        response = await chain.execute(request)

        assert attempt_count["value"] == 3
        assert response.value == "success"

    @pytest.mark.asyncio
    async def test_middleware_chain_reusability(self):
        """测试中间件链可重用性"""
        logs: list[str] = []

        async def handler(req: MockRequest) -> MockResponse:
            return MockResponse(req.value)

        chain = MiddlewareChain(handler)
        chain.use(LoggingMiddleware(logs, priority=50))

        # 第一次执行
        await chain.execute(MockRequest("request1"))
        # 第二次执行
        await chain.execute(MockRequest("request2"))

        # 验证两次请求都被记录
        assert len(logs) == 4
        assert logs[0] == "before: request1"
        assert logs[1] == "after: request1"
        assert logs[2] == "before: request2"
        assert logs[3] == "after: request2"
