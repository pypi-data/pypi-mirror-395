"""
执行上下文

贯穿整个请求链路，自动传播到子操作。
"""

import uuid
from dataclasses import dataclass, field


def _generate_id() -> str:
    """生成 16 字符的唯一 ID"""
    return uuid.uuid4().hex[:16]


@dataclass(frozen=True, slots=True)
class ExecutionContext:
    """执行上下文

    贯穿整个请求链路，自动传播到子操作。

    包含：
    - 追踪信息（trace_id, span_id）
    - 请求信息（request_id, correlation_id）
    - 业务信息（user_id, tenant_id）
    - 扩展信息（baggage）

    属性:
        trace_id: 追踪 ID，贯穿整个请求链路
        span_id: Span ID，标识当前操作
        parent_span_id: 父 Span ID
        request_id: 请求 ID
        correlation_id: 关联 ID（用于业务关联）
        user_id: 用户 ID
        tenant_id: 租户 ID
        baggage: 扩展信息（跨服务传播的键值对）

    示例:
        # 创建根上下文
        ctx = ExecutionContext.create_root()

        # 创建子上下文（新的 Span）
        child_ctx = ctx.child_context()

        # 添加业务信息
        ctx_with_user = ctx.with_user("user_001")

        # 添加 baggage
        ctx_with_env = ctx.with_baggage("env", "test")
    """

    # 追踪信息
    trace_id: str
    span_id: str
    parent_span_id: str | None = None

    # 请求信息
    request_id: str = field(default_factory=_generate_id)
    correlation_id: str | None = None

    # 业务信息
    user_id: str | None = None
    tenant_id: str | None = None

    # 扩展信息（跨服务传播的键值对）
    baggage: dict[str, str] = field(default_factory=dict)

    @classmethod
    def create_root(
        cls,
        request_id: str | None = None,
        user_id: str | None = None,
        tenant_id: str | None = None,
    ) -> "ExecutionContext":
        """创建根上下文

        Args:
            request_id: 请求 ID（可选，默认自动生成）
            user_id: 用户 ID（可选）
            tenant_id: 租户 ID（可选）

        Returns:
            新的根上下文
        """
        trace_id = _generate_id()
        return cls(
            trace_id=trace_id,
            span_id=_generate_id(),
            request_id=request_id or _generate_id(),
            user_id=user_id,
            tenant_id=tenant_id,
        )

    def child_context(self, span_name: str | None = None) -> "ExecutionContext":
        """创建子上下文（新 Span）

        子上下文继承父上下文的 trace_id 和业务信息，
        但有新的 span_id。

        Args:
            span_name: Span 名称（可选，仅用于调试）

        Returns:
            新的子上下文
        """
        return ExecutionContext(
            trace_id=self.trace_id,
            span_id=_generate_id(),
            parent_span_id=self.span_id,
            request_id=self.request_id,
            correlation_id=self.correlation_id,
            user_id=self.user_id,
            tenant_id=self.tenant_id,
            baggage=self.baggage.copy(),
        )

    def with_baggage(self, key: str, value: str) -> "ExecutionContext":
        """添加 baggage 项

        返回新的上下文，原上下文不变（不可变对象）。

        Args:
            key: baggage 键
            value: baggage 值

        Returns:
            包含新 baggage 的上下文
        """
        return ExecutionContext(
            trace_id=self.trace_id,
            span_id=self.span_id,
            parent_span_id=self.parent_span_id,
            request_id=self.request_id,
            correlation_id=self.correlation_id,
            user_id=self.user_id,
            tenant_id=self.tenant_id,
            baggage={**self.baggage, key: value},
        )

    def with_user(self, user_id: str) -> "ExecutionContext":
        """设置用户 ID

        Args:
            user_id: 用户 ID

        Returns:
            包含用户 ID 的上下文
        """
        return ExecutionContext(
            trace_id=self.trace_id,
            span_id=self.span_id,
            parent_span_id=self.parent_span_id,
            request_id=self.request_id,
            correlation_id=self.correlation_id,
            user_id=user_id,
            tenant_id=self.tenant_id,
            baggage=self.baggage,
        )

    def with_tenant(self, tenant_id: str) -> "ExecutionContext":
        """设置租户 ID

        Args:
            tenant_id: 租户 ID

        Returns:
            包含租户 ID 的上下文
        """
        return ExecutionContext(
            trace_id=self.trace_id,
            span_id=self.span_id,
            parent_span_id=self.parent_span_id,
            request_id=self.request_id,
            correlation_id=self.correlation_id,
            user_id=self.user_id,
            tenant_id=tenant_id,
            baggage=self.baggage,
        )

    def with_correlation_id(self, correlation_id: str) -> "ExecutionContext":
        """设置关联 ID

        Args:
            correlation_id: 关联 ID

        Returns:
            包含关联 ID 的上下文
        """
        return ExecutionContext(
            trace_id=self.trace_id,
            span_id=self.span_id,
            parent_span_id=self.parent_span_id,
            request_id=self.request_id,
            correlation_id=correlation_id,
            user_id=self.user_id,
            tenant_id=self.tenant_id,
            baggage=self.baggage,
        )

    def to_dict(self) -> dict[str, str | None]:
        """转换为字典

        Returns:
            上下文信息字典
        """
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "request_id": self.request_id,
            "correlation_id": self.correlation_id,
            "user_id": self.user_id,
            "tenant_id": self.tenant_id,
        }
