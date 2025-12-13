"""
HTTP 上下文载体

负责在 HTTP Headers 中注入和提取 ExecutionContext。
"""

import uuid

from df_test_framework.core.context.execution import ExecutionContext

# 标准 Header 名称
TRACE_ID_HEADER = "X-Trace-Id"
SPAN_ID_HEADER = "X-Span-Id"
PARENT_SPAN_ID_HEADER = "X-Parent-Span-Id"
REQUEST_ID_HEADER = "X-Request-Id"
CORRELATION_ID_HEADER = "X-Correlation-Id"
USER_ID_HEADER = "X-User-Id"
TENANT_ID_HEADER = "X-Tenant-Id"
BAGGAGE_HEADER_PREFIX = "X-Baggage-"


def _generate_id() -> str:
    """生成唯一 ID"""
    return uuid.uuid4().hex[:16]


class HttpContextCarrier:
    """HTTP 上下文载体

    负责在 HTTP Headers 中注入和提取 ExecutionContext。

    示例:
        # 注入上下文到请求头
        ctx = ExecutionContext.create_root()
        headers = HttpContextCarrier.inject(ctx, {})
        # headers 现在包含追踪信息

        # 从响应头提取上下文
        ctx = HttpContextCarrier.extract(response_headers)
        if ctx:
            print(f"Trace ID: {ctx.trace_id}")
    """

    @staticmethod
    def inject(
        ctx: ExecutionContext,
        headers: dict[str, str],
    ) -> dict[str, str]:
        """注入上下文到 HTTP Headers

        Args:
            ctx: 执行上下文
            headers: 原始 Headers

        Returns:
            包含上下文信息的新 Headers
        """
        result = headers.copy()

        # 注入追踪信息
        result[TRACE_ID_HEADER] = ctx.trace_id
        result[SPAN_ID_HEADER] = ctx.span_id
        result[REQUEST_ID_HEADER] = ctx.request_id

        if ctx.parent_span_id:
            result[PARENT_SPAN_ID_HEADER] = ctx.parent_span_id

        if ctx.correlation_id:
            result[CORRELATION_ID_HEADER] = ctx.correlation_id

        # 注入业务信息
        if ctx.user_id:
            result[USER_ID_HEADER] = ctx.user_id

        if ctx.tenant_id:
            result[TENANT_ID_HEADER] = ctx.tenant_id

        # 注入 baggage
        for key, value in ctx.baggage.items():
            result[f"{BAGGAGE_HEADER_PREFIX}{key}"] = value

        return result

    @staticmethod
    def extract(headers: dict[str, str]) -> ExecutionContext | None:
        """从 HTTP Headers 提取上下文

        Args:
            headers: HTTP Headers

        Returns:
            执行上下文，如果没有追踪信息则返回 None
        """
        # 大小写不敏感的 header 查找
        headers_lower = {k.lower(): v for k, v in headers.items()}

        trace_id = headers_lower.get(TRACE_ID_HEADER.lower())
        if not trace_id:
            return None

        # 提取 baggage
        baggage: dict[str, str] = {}
        prefix_lower = BAGGAGE_HEADER_PREFIX.lower()
        for key, value in headers_lower.items():
            if key.startswith(prefix_lower):
                baggage_key = key[len(prefix_lower) :]
                baggage[baggage_key] = value

        return ExecutionContext(
            trace_id=trace_id,
            span_id=headers_lower.get(SPAN_ID_HEADER.lower(), _generate_id()),
            parent_span_id=headers_lower.get(PARENT_SPAN_ID_HEADER.lower()),
            request_id=headers_lower.get(REQUEST_ID_HEADER.lower(), _generate_id()),
            correlation_id=headers_lower.get(CORRELATION_ID_HEADER.lower()),
            user_id=headers_lower.get(USER_ID_HEADER.lower()),
            tenant_id=headers_lower.get(TENANT_ID_HEADER.lower()),
            baggage=baggage,
        )

    @staticmethod
    def get_header_names() -> list[str]:
        """获取所有标准 Header 名称

        Returns:
            Header 名称列表
        """
        return [
            TRACE_ID_HEADER,
            SPAN_ID_HEADER,
            PARENT_SPAN_ID_HEADER,
            REQUEST_ID_HEADER,
            CORRELATION_ID_HEADER,
            USER_ID_HEADER,
            TENANT_ID_HEADER,
        ]
