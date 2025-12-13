"""
日志中间件

记录 HTTP 请求和响应日志。
"""

import logging
import time

from df_test_framework.capabilities.clients.http.core.request import Request
from df_test_framework.capabilities.clients.http.core.response import Response
from df_test_framework.core.middleware import BaseMiddleware


class LoggingMiddleware(BaseMiddleware[Request, Response]):
    """日志中间件

    记录 HTTP 请求和响应的详细信息。

    可配置日志级别和输出内容。

    示例:
        middleware = LoggingMiddleware(
            level="DEBUG",
            log_request=True,
            log_response=True,
            log_body=True,
        )
    """

    def __init__(
        self,
        logger: logging.Logger | None = None,
        level: str = "DEBUG",
        log_request: bool = True,
        log_response: bool = True,
        log_headers: bool = False,
        log_body: bool = True,
        mask_fields: list[str] | None = None,
        max_body_length: int = 1000,
        priority: int = 100,
    ):
        """初始化日志中间件

        Args:
            logger: 日志对象
            level: 日志级别
            log_request: 是否记录请求
            log_response: 是否记录响应
            log_headers: 是否记录 Headers
            log_body: 是否记录 Body
            mask_fields: 需要脱敏的字段
            max_body_length: 最大记录体长度
            priority: 优先级（应该较大，最后执行）
        """
        super().__init__(name="LoggingMiddleware", priority=priority)
        self._logger = logger or logging.getLogger(__name__)
        self._level = getattr(logging, level.upper(), logging.DEBUG)
        self.log_request = log_request
        self.log_response = log_response
        self.log_headers = log_headers
        self.log_body = log_body
        self.mask_fields = mask_fields or ["password", "token", "secret"]
        self.max_body_length = max_body_length

    async def __call__(
        self,
        request: Request,
        call_next,
    ) -> Response:
        """记录请求和响应"""
        # 记录请求
        if self.log_request:
            self._log_request(request)

        start = time.monotonic()

        try:
            response = await call_next(request)
            duration = time.monotonic() - start

            # 记录响应
            if self.log_response:
                self._log_response(request, response, duration)

            return response

        except Exception as e:
            duration = time.monotonic() - start
            self._log_error(request, e, duration)
            raise

    def _log_request(self, request: Request) -> None:
        """记录请求"""
        parts = [f"→ {request.method} {request.path}"]

        if self.log_headers and request.headers:
            headers_str = ", ".join(f"{k}={v}" for k, v in request.headers.items())
            parts.append(f"  Headers: {headers_str}")

        if self.log_body:
            if request.json:
                body_str = str(request.json)
                if len(body_str) > self.max_body_length:
                    body_str = body_str[: self.max_body_length] + "..."
                parts.append(f"  Body: {body_str}")

        self._logger.log(self._level, "\n".join(parts))

    def _log_response(
        self,
        request: Request,
        response: Response,
        duration: float,
    ) -> None:
        """记录响应"""
        status_emoji = "✓" if response.is_success else "✗"
        parts = [
            f"← {request.method} {request.path} "
            f"{status_emoji} {response.status_code} ({duration:.3f}s)"
        ]

        if self.log_headers and response.headers:
            headers_str = ", ".join(f"{k}={v}" for k, v in response.headers.items())
            parts.append(f"  Headers: {headers_str}")

        if self.log_body:
            body_str = response.text
            if len(body_str) > self.max_body_length:
                body_str = body_str[: self.max_body_length] + "..."
            parts.append(f"  Body: {body_str}")

        self._logger.log(self._level, "\n".join(parts))

    def _log_error(
        self,
        request: Request,
        error: Exception,
        duration: float,
    ) -> None:
        """记录错误"""
        self._logger.error(f"← {request.method} {request.path} ✗ ERROR ({duration:.3f}s): {error}")
