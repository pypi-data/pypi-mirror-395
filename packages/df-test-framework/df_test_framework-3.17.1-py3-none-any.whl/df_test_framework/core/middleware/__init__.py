"""
统一中间件系统

洋葱模型中间件，适用于 HTTP/gRPC/Database/MQ 等场景。

特点:
- 泛型设计: Middleware[TRequest, TResponse]
- 洋葱模型: before/after 在同一作用域
- 异步原生: async-first
- 优先级控制: priority 越小越先执行
"""

from df_test_framework.core.middleware.base import (
    BaseMiddleware,
    SyncMiddleware,
)
from df_test_framework.core.middleware.chain import MiddlewareChain
from df_test_framework.core.middleware.decorator import middleware
from df_test_framework.core.middleware.protocol import (
    Middleware,
    MiddlewareFunc,
    Next,
)

__all__ = [
    # 协议
    "Middleware",
    "Next",
    "MiddlewareFunc",
    # 链
    "MiddlewareChain",
    # 基类
    "BaseMiddleware",
    "SyncMiddleware",
    # 装饰器
    "middleware",
]
