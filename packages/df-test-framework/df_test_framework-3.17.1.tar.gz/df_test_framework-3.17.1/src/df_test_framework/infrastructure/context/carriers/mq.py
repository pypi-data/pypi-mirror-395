"""
MQ 上下文载体

负责在消息队列消息头中注入和提取 ExecutionContext。
"""

import uuid

from df_test_framework.core.context.execution import ExecutionContext

# MQ 消息头键名
TRACE_ID_KEY = "trace_id"
SPAN_ID_KEY = "span_id"
PARENT_SPAN_ID_KEY = "parent_span_id"
REQUEST_ID_KEY = "request_id"
CORRELATION_ID_KEY = "correlation_id"
USER_ID_KEY = "user_id"
TENANT_ID_KEY = "tenant_id"
BAGGAGE_KEY_PREFIX = "baggage_"


def _generate_id() -> str:
    """生成唯一 ID"""
    return uuid.uuid4().hex[:16]


class MqContextCarrier:
    """MQ 上下文载体

    负责在消息队列消息头中注入和提取 ExecutionContext。

    适用于 Kafka、RabbitMQ、RocketMQ 等消息队列。

    示例:
        # 注入上下文到消息头
        ctx = ExecutionContext.create_root()
        headers = MqContextCarrier.inject(ctx, {})

        # 发送消息
        producer.send(topic, message, headers=headers)

        # 从消息头提取上下文
        ctx = MqContextCarrier.extract(message.headers)
    """

    @staticmethod
    def inject(
        ctx: ExecutionContext,
        headers: dict[str, str],
    ) -> dict[str, str]:
        """注入上下文到消息头

        Args:
            ctx: 执行上下文
            headers: 原始消息头

        Returns:
            包含上下文信息的新消息头
        """
        result = headers.copy()

        # 注入追踪信息
        result[TRACE_ID_KEY] = ctx.trace_id
        result[SPAN_ID_KEY] = ctx.span_id
        result[REQUEST_ID_KEY] = ctx.request_id

        if ctx.parent_span_id:
            result[PARENT_SPAN_ID_KEY] = ctx.parent_span_id

        if ctx.correlation_id:
            result[CORRELATION_ID_KEY] = ctx.correlation_id

        # 注入业务信息
        if ctx.user_id:
            result[USER_ID_KEY] = ctx.user_id

        if ctx.tenant_id:
            result[TENANT_ID_KEY] = ctx.tenant_id

        # 注入 baggage
        for key, value in ctx.baggage.items():
            result[f"{BAGGAGE_KEY_PREFIX}{key}"] = value

        return result

    @staticmethod
    def extract(headers: dict[str, str] | None) -> ExecutionContext | None:
        """从消息头提取上下文

        Args:
            headers: 消息头

        Returns:
            执行上下文，如果没有追踪信息则返回 None
        """
        if not headers:
            return None

        trace_id = headers.get(TRACE_ID_KEY)
        if not trace_id:
            return None

        # 提取 baggage
        baggage: dict[str, str] = {}
        for key, value in headers.items():
            if key.startswith(BAGGAGE_KEY_PREFIX):
                baggage_key = key[len(BAGGAGE_KEY_PREFIX) :]
                baggage[baggage_key] = value

        return ExecutionContext(
            trace_id=trace_id,
            span_id=headers.get(SPAN_ID_KEY, _generate_id()),
            parent_span_id=headers.get(PARENT_SPAN_ID_KEY),
            request_id=headers.get(REQUEST_ID_KEY, _generate_id()),
            correlation_id=headers.get(CORRELATION_ID_KEY),
            user_id=headers.get(USER_ID_KEY),
            tenant_id=headers.get(TENANT_ID_KEY),
            baggage=baggage,
        )
