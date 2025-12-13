"""
gRPC 上下文载体

负责在 gRPC Metadata 中注入和提取 ExecutionContext。
"""

import uuid

from df_test_framework.core.context.execution import ExecutionContext

# gRPC Metadata 键名（小写）
TRACE_ID_KEY = "x-trace-id"
SPAN_ID_KEY = "x-span-id"
PARENT_SPAN_ID_KEY = "x-parent-span-id"
REQUEST_ID_KEY = "x-request-id"
CORRELATION_ID_KEY = "x-correlation-id"
USER_ID_KEY = "x-user-id"
TENANT_ID_KEY = "x-tenant-id"
BAGGAGE_KEY_PREFIX = "x-baggage-"


def _generate_id() -> str:
    """生成唯一 ID"""
    return uuid.uuid4().hex[:16]


class GrpcContextCarrier:
    """gRPC 上下文载体

    负责在 gRPC Metadata 中注入和提取 ExecutionContext。

    注意: gRPC Metadata 键名必须是小写。

    示例:
        # 注入上下文到 metadata
        ctx = ExecutionContext.create_root()
        metadata = GrpcContextCarrier.inject(ctx, [])
        # metadata 现在包含追踪信息元组列表

        # 从 metadata 提取上下文
        ctx = GrpcContextCarrier.extract(incoming_metadata)
    """

    @staticmethod
    def inject(
        ctx: ExecutionContext,
        metadata: list[tuple[str, str]],
    ) -> list[tuple[str, str]]:
        """注入上下文到 gRPC Metadata

        Args:
            ctx: 执行上下文
            metadata: 原始 Metadata（元组列表）

        Returns:
            包含上下文信息的新 Metadata
        """
        result = list(metadata)

        # 注入追踪信息
        result.append((TRACE_ID_KEY, ctx.trace_id))
        result.append((SPAN_ID_KEY, ctx.span_id))
        result.append((REQUEST_ID_KEY, ctx.request_id))

        if ctx.parent_span_id:
            result.append((PARENT_SPAN_ID_KEY, ctx.parent_span_id))

        if ctx.correlation_id:
            result.append((CORRELATION_ID_KEY, ctx.correlation_id))

        # 注入业务信息
        if ctx.user_id:
            result.append((USER_ID_KEY, ctx.user_id))

        if ctx.tenant_id:
            result.append((TENANT_ID_KEY, ctx.tenant_id))

        # 注入 baggage
        for key, value in ctx.baggage.items():
            result.append((f"{BAGGAGE_KEY_PREFIX}{key.lower()}", value))

        return result

    @staticmethod
    def extract(metadata: list[tuple[str, str]]) -> ExecutionContext | None:
        """从 gRPC Metadata 提取上下文

        Args:
            metadata: gRPC Metadata（元组列表）

        Returns:
            执行上下文，如果没有追踪信息则返回 None
        """
        # 转换为字典（小写键）
        metadata_dict: dict[str, str] = {}
        for key, value in metadata:
            metadata_dict[key.lower()] = value

        trace_id = metadata_dict.get(TRACE_ID_KEY)
        if not trace_id:
            return None

        # 提取 baggage
        baggage: dict[str, str] = {}
        for key, value in metadata_dict.items():
            if key.startswith(BAGGAGE_KEY_PREFIX):
                baggage_key = key[len(BAGGAGE_KEY_PREFIX) :]
                baggage[baggage_key] = value

        return ExecutionContext(
            trace_id=trace_id,
            span_id=metadata_dict.get(SPAN_ID_KEY, _generate_id()),
            parent_span_id=metadata_dict.get(PARENT_SPAN_ID_KEY),
            request_id=metadata_dict.get(REQUEST_ID_KEY, _generate_id()),
            correlation_id=metadata_dict.get(CORRELATION_ID_KEY),
            user_id=metadata_dict.get(USER_ID_KEY),
            tenant_id=metadata_dict.get(TENANT_ID_KEY),
            baggage=baggage,
        )
