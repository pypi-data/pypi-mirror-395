"""
中间件协议定义

统一的中间件协议，适用于所有能力层（HTTP/gRPC/Database/MQ）。
"""

from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import TypeVar

TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")

# 类型别名 - 使用 Python 3.12+ 的 type 语句
# Next 函数类型
Next = Callable[[TRequest], Awaitable[TResponse]]

# 中间件函数类型
MiddlewareFunc = Callable[[TRequest, Next[TRequest, TResponse]], Awaitable[TResponse]]


class Middleware[TRequest, TResponse](ABC):
    """统一中间件协议

    洋葱模型：before 和 after 在同一作用域

    泛型实例化示例:
    - Middleware[HttpRequest, HttpResponse]      # HTTP
    - Middleware[GrpcRequest, GrpcResponse]      # gRPC
    - Middleware[Query, QueryResult]             # Database
    - Middleware[Message, PublishResult]         # MQ

    属性:
        name: 中间件名称
        priority: 优先级（数字越小越先执行）

    示例:
        class TimingMiddleware(Middleware[HttpRequest, HttpResponse]):
            async def __call__(self, request, call_next):
                start = time.monotonic()
                response = await call_next(request)
                print(f"Duration: {time.monotonic() - start:.3f}s")
                return response
    """

    name: str = ""
    priority: int = 100  # 数字越小越先执行

    @abstractmethod
    async def __call__(
        self,
        request: TRequest,
        call_next: Next[TRequest, TResponse],
    ) -> TResponse:
        """洋葱模型核心方法

        实现此方法来定义中间件行为。

        Args:
            request: 请求对象
            call_next: 调用下一个中间件或最终处理器的函数

        Returns:
            响应对象

        示例:
            async def __call__(self, request, call_next):
                # before 逻辑
                start = time.monotonic()
                request = request.with_header("X-Timing", "start")

                # 调用下一个中间件或最终处理器
                response = await call_next(request)

                # after 逻辑（同一作用域，可直接访问 start）
                duration = time.monotonic() - start
                logger.info(f"Request took {duration:.3f}s")

                return response
        """
        ...
