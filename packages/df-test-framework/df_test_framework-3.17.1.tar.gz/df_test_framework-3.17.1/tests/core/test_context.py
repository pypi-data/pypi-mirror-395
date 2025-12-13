"""
测试 core.context - 上下文传播系统

v3.14.0 新增：
- ExecutionContext 上下文管理
- 上下文传播机制
- ContextVar 管理
"""

import pytest

from df_test_framework.core.context import (
    ExecutionContext,
    get_current_context,
    get_or_create_context,
    run_with_context,
    set_current_context,
    with_context,
    with_context_async,
)


class TestExecutionContext:
    """测试 ExecutionContext 基本功能"""

    def test_create_root_context(self):
        """测试创建根上下文"""
        ctx = ExecutionContext.create_root(user_id="user_001", tenant_id="tenant_a")

        assert ctx.user_id == "user_001"
        assert ctx.tenant_id == "tenant_a"
        assert ctx.trace_id is not None
        assert ctx.span_id is not None
        assert ctx.parent_span_id is None

    def test_create_child_context(self):
        """测试创建子上下文"""
        root = ExecutionContext.create_root(user_id="user_001")
        child = root.child_context(span_name="child_operation")

        # 验证继承关系
        assert child.trace_id == root.trace_id
        assert child.parent_span_id == root.span_id
        assert child.span_id != root.span_id
        assert child.user_id == root.user_id

    def test_context_baggage(self):
        """测试上下文行李"""
        ctx = ExecutionContext.create_root()
        ctx_with_env = ctx.with_baggage("env", "test")
        ctx_with_both = ctx_with_env.with_baggage("version", "1.0")

        # 原上下文不变
        assert ctx.baggage == {}

        # 新上下文包含 baggage
        assert ctx_with_env.baggage["env"] == "test"
        assert ctx_with_both.baggage["env"] == "test"
        assert ctx_with_both.baggage["version"] == "1.0"

    def test_context_immutability(self):
        """测试上下文不可变性"""
        ctx = ExecutionContext.create_root(user_id="user_001")

        # with_user 返回新上下文，原上下文不变
        new_ctx = ctx.with_user("user_002")

        assert ctx.user_id == "user_001"
        assert new_ctx.user_id == "user_002"
        assert ctx.trace_id == new_ctx.trace_id  # trace_id 相同

    def test_with_user(self):
        """测试设置用户 ID"""
        ctx = ExecutionContext.create_root()
        ctx_with_user = ctx.with_user("test_user")

        assert ctx.user_id is None
        assert ctx_with_user.user_id == "test_user"

    def test_with_tenant(self):
        """测试设置租户 ID"""
        ctx = ExecutionContext.create_root()
        ctx_with_tenant = ctx.with_tenant("tenant_001")

        assert ctx.tenant_id is None
        assert ctx_with_tenant.tenant_id == "tenant_001"

    def test_with_correlation_id(self):
        """测试设置关联 ID"""
        ctx = ExecutionContext.create_root()
        ctx_with_corr = ctx.with_correlation_id("corr_123")

        assert ctx.correlation_id is None
        assert ctx_with_corr.correlation_id == "corr_123"

    def test_to_dict(self):
        """测试转换为字典"""
        ctx = ExecutionContext.create_root(user_id="user_001", tenant_id="tenant_a")
        ctx_dict = ctx.to_dict()

        assert "trace_id" in ctx_dict
        assert "span_id" in ctx_dict
        assert ctx_dict["user_id"] == "user_001"
        assert ctx_dict["tenant_id"] == "tenant_a"


class TestContextManagement:
    """测试上下文管理"""

    def test_get_or_create_context_creates_new(self):
        """测试 get_or_create_context 创建新上下文"""
        # 清除当前上下文
        set_current_context(None)

        ctx = get_or_create_context()

        assert ctx is not None
        assert ctx.trace_id is not None

    def test_get_or_create_context_returns_existing(self):
        """测试 get_or_create_context 返回已存在的上下文"""
        original_ctx = ExecutionContext.create_root(user_id="existing_user")
        set_current_context(original_ctx)

        ctx = get_or_create_context()

        assert ctx is not None
        assert ctx.trace_id == original_ctx.trace_id
        assert ctx.user_id == "existing_user"

    def test_get_current_context_returns_none_when_no_context(self):
        """测试没有上下文时返回 None"""
        set_current_context(None)

        ctx = get_current_context()
        assert ctx is None

    def test_set_and_get_current_context(self):
        """测试设置和获取当前上下文"""
        ctx = ExecutionContext.create_root(user_id="set_test_user")
        set_current_context(ctx)

        current = get_current_context()
        assert current is not None
        assert current.user_id == "set_test_user"
        assert current.trace_id == ctx.trace_id

    def test_with_context_manager(self):
        """测试 with_context 上下文管理器"""
        set_current_context(None)

        ctx = ExecutionContext.create_root(user_id="context_manager_user")

        with with_context(ctx) as current:
            assert current is not None
            assert current.user_id == "context_manager_user"

            # 在作用域内能获取到上下文
            retrieved = get_current_context()
            assert retrieved is not None
            assert retrieved.trace_id == ctx.trace_id

        # 退出作用域后上下文恢复
        after_exit = get_current_context()
        assert after_exit is None

    @pytest.mark.asyncio
    async def test_with_context_async_manager(self):
        """测试 with_context_async 异步上下文管理器"""
        set_current_context(None)

        ctx = ExecutionContext.create_root(user_id="async_context_user")

        async with with_context_async(ctx) as current:
            assert current is not None
            assert current.user_id == "async_context_user"

            # 在作用域内能获取到上下文
            retrieved = get_current_context()
            assert retrieved is not None
            assert retrieved.trace_id == ctx.trace_id

        # 退出作用域后上下文恢复
        after_exit = get_current_context()
        assert after_exit is None

    def test_run_with_context(self):
        """测试 run_with_context 函数"""
        set_current_context(None)

        ctx = ExecutionContext.create_root(user_id="run_with_user")

        def get_user_id():
            current = get_current_context()
            return current.user_id if current else None

        result = run_with_context(ctx, get_user_id)

        assert result == "run_with_user"

        # 函数执行后上下文恢复
        after = get_current_context()
        assert after is None


class TestContextPropagation:
    """测试上下文传播"""

    @pytest.mark.asyncio
    async def test_context_propagates_through_async_calls(self):
        """测试上下文在异步调用中传播"""
        root_ctx = ExecutionContext.create_root(user_id="propagation_user")

        async with with_context_async(root_ctx):
            ctx1 = get_current_context()
            assert ctx1 is not None
            assert ctx1.user_id == "propagation_user"

            # 嵌套异步函数仍能获取上下文
            async def level2():
                ctx2 = get_current_context()
                assert ctx2 is not None
                assert ctx2.trace_id == ctx1.trace_id
                return ctx2.user_id

            user_id = await level2()
            assert user_id == "propagation_user"

    def test_context_isolation_between_scopes(self):
        """测试不同作用域之间的上下文隔离"""
        ctx1 = ExecutionContext.create_root(user_id="user1")
        ctx2 = ExecutionContext.create_root(user_id="user2")

        with with_context(ctx1):
            current1 = get_current_context()
            assert current1.user_id == "user1"

        with with_context(ctx2):
            current2 = get_current_context()
            assert current2.user_id == "user2"

    def test_nested_context_managers(self):
        """测试嵌套上下文管理器"""
        outer_ctx = ExecutionContext.create_root(user_id="outer")
        inner_ctx = ExecutionContext.create_root(user_id="inner")

        with with_context(outer_ctx):
            assert get_current_context().user_id == "outer"

            with with_context(inner_ctx):
                assert get_current_context().user_id == "inner"

            # 内层退出后恢复外层上下文
            assert get_current_context().user_id == "outer"

    @pytest.mark.asyncio
    async def test_child_context_inherits_parent_info(self):
        """测试子上下文继承父上下文信息"""
        root = ExecutionContext.create_root(user_id="parent_user", tenant_id="tenant_123")

        async with with_context_async(root):
            # 创建子上下文
            child = root.child_context("child_operation")

            # 验证继承
            assert child.trace_id == root.trace_id
            assert child.user_id == "parent_user"
            assert child.tenant_id == "tenant_123"
            assert child.parent_span_id == root.span_id

    def test_context_with_multiple_baggage_items(self):
        """测试多个 baggage 项"""
        ctx = ExecutionContext.create_root()
        ctx_with_items = (
            ctx.with_baggage("env", "test")
            .with_baggage("version", "1.0")
            .with_baggage("region", "us-west")
        )

        assert len(ctx_with_items.baggage) == 3
        assert ctx_with_items.baggage["env"] == "test"
        assert ctx_with_items.baggage["version"] == "1.0"
        assert ctx_with_items.baggage["region"] == "us-west"


class TestContextChaining:
    """测试上下文链式调用"""

    def test_fluent_context_building(self):
        """测试流式构建上下文"""
        ctx = (
            ExecutionContext.create_root()
            .with_user("user_001")
            .with_tenant("tenant_a")
            .with_correlation_id("corr_123")
            .with_baggage("env", "test")
            .with_baggage("version", "1.0")
        )

        assert ctx.user_id == "user_001"
        assert ctx.tenant_id == "tenant_a"
        assert ctx.correlation_id == "corr_123"
        assert ctx.baggage["env"] == "test"
        assert ctx.baggage["version"] == "1.0"

    def test_context_chain_immutability(self):
        """测试链式调用中的不可变性"""
        ctx1 = ExecutionContext.create_root()
        ctx2 = ctx1.with_user("user_001")
        ctx3 = ctx2.with_tenant("tenant_a")

        # 每个ctx都是独立的
        assert ctx1.user_id is None
        assert ctx1.tenant_id is None

        assert ctx2.user_id == "user_001"
        assert ctx2.tenant_id is None

        assert ctx3.user_id == "user_001"
        assert ctx3.tenant_id == "tenant_a"

        # 但它们共享 trace_id
        assert ctx1.trace_id == ctx2.trace_id == ctx3.trace_id
