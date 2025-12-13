"""
可观测性中间件

为 HTTP 请求添加追踪、指标和日志。
"""

import time
from typing import Any

from df_test_framework.capabilities.clients.http.core.request import Request
from df_test_framework.capabilities.clients.http.core.response import Response
from df_test_framework.core.context import get_or_create_context
from df_test_framework.core.events import HttpRequestEndEvent, HttpRequestStartEvent
from df_test_framework.core.middleware import BaseMiddleware
from df_test_framework.infrastructure.context.carriers.http import HttpContextCarrier
from df_test_framework.infrastructure.events import EventBus
from df_test_framework.infrastructure.telemetry import Telemetry


class HttpTelemetryMiddleware(BaseMiddleware[Request, Response]):
    """HTTP 可观测性中间件

    自动为每个 HTTP 请求：
    - 创建追踪 Span
    - 记录指标（duration、status）
    - 输出日志
    - 注入上下文到请求头
    - 发布事件到 EventBus

    示例:
        middleware = HttpTelemetryMiddleware(
            telemetry=telemetry,
            event_bus=event_bus,
        )

        client.use(middleware)
    """

    def __init__(
        self,
        telemetry: Telemetry | None = None,
        event_bus: EventBus | None = None,
        operation_name: str = "http.request",
        inject_context: bool = True,
        priority: int = 1,  # 最先执行
    ):
        """初始化可观测性中间件

        Args:
            telemetry: Telemetry 实例
            event_bus: EventBus 实例
            operation_name: 操作名称
            inject_context: 是否注入上下文到请求头
            priority: 优先级（应该最小，最先执行）
        """
        super().__init__(name="HttpTelemetryMiddleware", priority=priority)
        self._telemetry = telemetry
        self._event_bus = event_bus
        self._operation_name = operation_name
        self._inject_context = inject_context

    async def __call__(
        self,
        request: Request,
        call_next,
    ) -> Response:
        """添加可观测性"""
        # 获取或创建上下文
        ctx = get_or_create_context()

        # 注入上下文到请求头
        if self._inject_context:
            headers = HttpContextCarrier.inject(ctx, request.headers)
            request = request.with_headers(headers)

        # 提取属性
        attributes = self._extract_attributes(request)

        # 发布请求开始事件
        if self._event_bus:
            await self._event_bus.publish(
                HttpRequestStartEvent(
                    method=request.method,
                    url=request.path,
                    headers=request.headers,
                    context=ctx,
                )
            )

        start = time.monotonic()

        # 如果有 Telemetry，使用 span
        if self._telemetry:
            async with self._telemetry.span(self._operation_name, attributes) as span:
                try:
                    response = await call_next(request)
                    duration = time.monotonic() - start

                    # 记录响应属性
                    span.set_attribute("http.status_code", response.status_code)
                    span.set_attribute("http.response_size", len(response.body))

                    # 发布请求结束事件
                    await self._publish_end_event(request, response, duration, ctx)

                    return response

                except Exception as e:
                    duration = time.monotonic() - start
                    span.record_exception(e)
                    raise

        else:
            # 没有 Telemetry，直接调用
            try:
                response = await call_next(request)
                duration = time.monotonic() - start

                await self._publish_end_event(request, response, duration, ctx)

                return response

            except Exception:
                raise

    def _extract_attributes(self, request: Request) -> dict[str, Any]:
        """提取请求属性

        Args:
            request: HTTP 请求

        Returns:
            属性字典
        """
        return {
            "http.method": request.method,
            "http.url": request.path,
            "http.request_size": len(str(request.json)) if request.json else 0,
        }

    async def _publish_end_event(
        self,
        request: Request,
        response: Response,
        duration: float,
        ctx: Any,
    ) -> None:
        """发布请求结束事件"""
        if self._event_bus:
            await self._event_bus.publish(
                HttpRequestEndEvent(
                    method=request.method,
                    url=request.path,
                    status_code=response.status_code,
                    duration=duration,
                    headers=response.headers,
                    context=ctx,
                )
            )
