"""
中间件装饰器

将函数转换为中间件对象。
"""

from collections.abc import Callable

from df_test_framework.core.middleware.protocol import (
    Middleware,
    MiddlewareFunc,
    Next,
)


def middleware[T, R](
    priority: int = 100,
    name: str | None = None,
) -> Callable[[MiddlewareFunc[T, R]], Middleware[T, R]]:
    """装饰器：将函数转换为中间件

    使用此装饰器可以快速创建中间件，无需定义类。

    Args:
        priority: 优先级（数字越小越先执行）
        name: 中间件名称（默认使用函数名）

    Returns:
        装饰器函数

    示例:
        @middleware(priority=50)
        async def timing_middleware(request: HttpRequest, call_next) -> HttpResponse:
            start = time.monotonic()
            response = await call_next(request)
            print(f"Duration: {time.monotonic() - start:.3f}s")
            return response

        client.use(timing_middleware)

        @middleware(priority=10, name="signature")
        async def add_signature(request, call_next):
            request = request.with_header("X-Sign", compute_sign(request))
            return await call_next(request)
    """

    def decorator(func: MiddlewareFunc[T, R]) -> Middleware[T, R]:
        class FuncMiddleware(Middleware[T, R]):
            def __init__(self) -> None:
                self.name = name or func.__name__
                self.priority = priority
                self._func = func

            async def __call__(
                self,
                request: T,
                call_next: Next[T, R],
            ) -> R:
                return await self._func(request, call_next)

            def __repr__(self) -> str:
                return f"FuncMiddleware(func={self._func.__name__!r}, priority={self.priority})"

        return FuncMiddleware()

    return decorator
