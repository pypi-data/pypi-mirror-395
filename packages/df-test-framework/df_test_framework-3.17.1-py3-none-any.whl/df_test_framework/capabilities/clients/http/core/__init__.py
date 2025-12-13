"""HTTP核心抽象

包含Request/Response等核心抽象

v3.16.0 更新:
- Interceptor/InterceptorChain 已完全移除
- 请使用 middleware.Middleware/MiddlewareChain
"""

from .request import Request
from .response import Response

__all__ = [
    "Request",
    "Response",
]
