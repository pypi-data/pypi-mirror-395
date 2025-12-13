"""
中间件便捷基类
"""

from df_test_framework.core.middleware.protocol import (
    Middleware,
    Next,
)


class BaseMiddleware[TRequest, TResponse](Middleware[TRequest, TResponse]):
    """中间件便捷基类

    提供默认实现，子类只需覆盖 __call__

    Args:
        name: 中间件名称（默认使用类名）
        priority: 优先级（默认 100）

    示例:
        class LoggingMiddleware(BaseMiddleware[HttpRequest, HttpResponse]):
            def __init__(self):
                super().__init__(priority=100)

            async def __call__(self, request, call_next):
                print(f"Request: {request.method} {request.path}")
                response = await call_next(request)
                print(f"Response: {response.status_code}")
                return response
    """

    def __init__(
        self,
        name: str | None = None,
        priority: int = 100,
    ):
        self.name = name or self.__class__.__name__
        self.priority = priority

    async def __call__(
        self,
        request: TRequest,
        call_next: Next[TRequest, TResponse],
    ) -> TResponse:
        """默认实现：直接传递"""
        return await call_next(request)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, priority={self.priority})"


class SyncMiddleware[TRequest, TResponse](BaseMiddleware[TRequest, TResponse]):
    """同步中间件基类

    适用于不需要异步操作的简单场景。
    子类只需覆盖 before 和/或 after 方法。

    示例:
        class AddHeaderMiddleware(SyncMiddleware[HttpRequest, HttpResponse]):
            def __init__(self, key: str, value: str):
                super().__init__()
                self.key = key
                self.value = value

            def before(self, request):
                return request.with_header(self.key, self.value)

        class LogResponseMiddleware(SyncMiddleware[HttpRequest, HttpResponse]):
            def after(self, response):
                print(f"Status: {response.status_code}")
                return response
    """

    def before(self, request: TRequest) -> TRequest:
        """前置处理（同步）

        Args:
            request: 请求对象

        Returns:
            处理后的请求对象
        """
        return request

    def after(self, response: TResponse) -> TResponse:
        """后置处理（同步）

        Args:
            response: 响应对象

        Returns:
            处理后的响应对象
        """
        return response

    async def __call__(
        self,
        request: TRequest,
        call_next: Next[TRequest, TResponse],
    ) -> TResponse:
        """执行同步中间件"""
        request = self.before(request)
        response = await call_next(request)
        response = self.after(response)
        return response
