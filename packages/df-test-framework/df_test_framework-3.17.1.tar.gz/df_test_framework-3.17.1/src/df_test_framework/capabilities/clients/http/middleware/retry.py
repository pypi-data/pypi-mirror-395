"""
重试中间件

自动重试失败的 HTTP 请求。
"""

import asyncio
import logging
from collections.abc import Sequence

from df_test_framework.capabilities.clients.http.core.request import Request
from df_test_framework.capabilities.clients.http.core.response import Response
from df_test_framework.core.middleware import BaseMiddleware


class RetryMiddleware(BaseMiddleware[Request, Response]):
    """重试中间件

    自动重试失败请求，支持指数退避。

    特性：
    - 可配置重试次数
    - 可配置重试状态码
    - 可配置重试异常
    - 指数退避策略

    示例:
        middleware = RetryMiddleware(
            max_retries=3,
            initial_delay=1.0,
            backoff_factor=2.0,
            retry_on_status=[500, 502, 503, 504],
        )

        # 重试间隔: 1s, 2s, 4s...
    """

    def __init__(
        self,
        max_retries: int = 3,
        initial_delay: float = 1.0,
        backoff_factor: float = 2.0,
        max_delay: float = 60.0,
        retry_on_status: Sequence[int] | None = None,
        retry_on_exception: tuple[type[Exception], ...] | None = None,
        logger: logging.Logger | None = None,
        priority: int = 5,
    ):
        """初始化重试中间件

        Args:
            max_retries: 最大重试次数
            initial_delay: 初始延迟时间（秒）
            backoff_factor: 退避因子
            max_delay: 最大延迟时间（秒）
            retry_on_status: 需要重试的状态码
            retry_on_exception: 需要重试的异常类型
            logger: 日志对象
            priority: 优先级（应该较小，先执行）
        """
        super().__init__(name="RetryMiddleware", priority=priority)
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.backoff_factor = backoff_factor
        self.max_delay = max_delay
        self.retry_on_status = retry_on_status or [500, 502, 503, 504]
        self.retry_on_exception = retry_on_exception or (Exception,)
        self._logger = logger or logging.getLogger(__name__)

    async def __call__(
        self,
        request: Request,
        call_next,
    ) -> Response:
        """执行重试逻辑"""
        last_exception: Exception | None = None
        last_response: Response | None = None

        for attempt in range(self.max_retries):
            try:
                response = await call_next(request)

                # 检查是否需要重试
                if response.status_code not in self.retry_on_status:
                    return response

                last_response = response
                self._logger.warning(
                    f"Retry {attempt + 1}/{self.max_retries}: "
                    f"status={response.status_code}, "
                    f"url={request.method} {request.path}"
                )

            except self.retry_on_exception as e:
                last_exception = e
                self._logger.warning(
                    f"Retry {attempt + 1}/{self.max_retries}: "
                    f"error={e}, "
                    f"url={request.method} {request.path}"
                )

            # 等待后重试（最后一次不等待）
            if attempt < self.max_retries - 1:
                wait_time = min(
                    self.initial_delay * (self.backoff_factor**attempt),
                    self.max_delay,
                )
                await asyncio.sleep(wait_time)

        # 所有重试都失败
        if last_response:
            return last_response

        if last_exception:
            raise last_exception

        raise RuntimeError("Unexpected retry state")

    def should_retry(self, response: Response) -> bool:
        """判断是否应该重试

        Args:
            response: HTTP 响应

        Returns:
            是否应该重试
        """
        return response.status_code in self.retry_on_status
