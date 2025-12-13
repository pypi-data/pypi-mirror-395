"""
中间件执行链
"""

from typing import Self

from df_test_framework.core.exceptions import MiddlewareAbort
from df_test_framework.core.middleware.protocol import (
    Middleware,
    Next,
)


class MiddlewareChain[TRequest, TResponse]:
    """中间件执行链

    执行顺序：
    - before: priority 升序（小的先执行）
    - after: priority 降序（大的先执行，即逆序）

    示例:
        chain = MiddlewareChain(send_request)
        chain.use(AuthMiddleware(priority=20))
        chain.use(SignMiddleware(priority=10))  # 先执行
        chain.use(LogMiddleware(priority=100))  # 最后执行

        response = await chain.execute(request)

    执行流程:
        SignMiddleware.before → AuthMiddleware.before → LogMiddleware.before
                                    ↓
                               send_request
                                    ↓
        SignMiddleware.after ← AuthMiddleware.after ← LogMiddleware.after
    """

    def __init__(self, handler: Next[TRequest, TResponse]):
        """初始化中间件链

        Args:
            handler: 最终处理函数（如发送 HTTP 请求）
        """
        self._handler = handler
        self._middlewares: list[Middleware[TRequest, TResponse]] = []

    def use(self, middleware: Middleware[TRequest, TResponse]) -> Self:
        """添加中间件（支持链式调用）

        Args:
            middleware: 要添加的中间件

        Returns:
            self，支持链式调用
        """
        self._middlewares.append(middleware)
        self._middlewares.sort(key=lambda m: m.priority)
        return self

    def use_many(self, middlewares: list[Middleware[TRequest, TResponse]]) -> Self:
        """批量添加中间件

        Args:
            middlewares: 中间件列表

        Returns:
            self，支持链式调用
        """
        for m in middlewares:
            self.use(m)
        return self

    def remove(self, middleware: Middleware[TRequest, TResponse]) -> Self:
        """移除中间件

        Args:
            middleware: 要移除的中间件

        Returns:
            self，支持链式调用
        """
        if middleware in self._middlewares:
            self._middlewares.remove(middleware)
        return self

    def clear(self) -> Self:
        """清空所有中间件

        Returns:
            self，支持链式调用
        """
        self._middlewares.clear()
        return self

    async def execute(self, request: TRequest) -> TResponse:
        """执行中间件链

        Args:
            request: 请求对象

        Returns:
            响应对象

        Raises:
            MiddlewareAbort: 如果中间件主动终止请求且未提供响应
        """
        # 构建洋葱：从内到外包装
        chain = self._handler
        for middleware in reversed(self._middlewares):
            chain = self._wrap(middleware, chain)

        try:
            return await chain(request)
        except MiddlewareAbort as e:
            if e.response is not None:
                return e.response
            raise

    def _wrap(
        self,
        middleware: Middleware[TRequest, TResponse],
        next_handler: Next[TRequest, TResponse],
    ) -> Next[TRequest, TResponse]:
        """包装中间件

        Args:
            middleware: 要包装的中间件
            next_handler: 下一个处理函数

        Returns:
            包装后的处理函数
        """

        async def wrapped(request: TRequest) -> TResponse:
            return await middleware(request, next_handler)

        return wrapped

    @property
    def middlewares(self) -> list[Middleware[TRequest, TResponse]]:
        """已注册的中间件列表（只读副本）"""
        return self._middlewares.copy()

    def __len__(self) -> int:
        """返回中间件数量"""
        return len(self._middlewares)

    def __contains__(self, middleware: Middleware[TRequest, TResponse]) -> bool:
        """检查中间件是否存在"""
        return middleware in self._middlewares
