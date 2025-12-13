"""
上下文传播管理

使用 contextvars 在异步上下文中传播 ExecutionContext。
"""

from collections.abc import Callable
from contextlib import asynccontextmanager, contextmanager
from contextvars import ContextVar
from typing import TypeVar

from df_test_framework.core.context.execution import ExecutionContext

T = TypeVar("T")

# 全局上下文变量
_current_context: ContextVar[ExecutionContext | None] = ContextVar(
    "execution_context",
    default=None,
)


def get_current_context() -> ExecutionContext | None:
    """获取当前上下文

    Returns:
        当前上下文，如果没有则返回 None

    示例:
        ctx = get_current_context()
        if ctx:
            print(f"Current trace: {ctx.trace_id}")
    """
    return _current_context.get()


def get_or_create_context() -> ExecutionContext:
    """获取当前上下文，如果不存在则创建根上下文

    Returns:
        当前上下文或新创建的根上下文

    示例:
        ctx = get_or_create_context()
        print(f"Trace ID: {ctx.trace_id}")
    """
    ctx = _current_context.get()
    if ctx is None:
        ctx = ExecutionContext.create_root()
        _current_context.set(ctx)
    return ctx


def set_current_context(ctx: ExecutionContext | None) -> None:
    """设置当前上下文

    Args:
        ctx: 要设置的上下文，None 表示清除

    示例:
        ctx = ExecutionContext.create_root()
        set_current_context(ctx)
    """
    _current_context.set(ctx)


@contextmanager
def with_context(ctx: ExecutionContext):
    """同步上下文作用域

    在作用域内设置指定的上下文，退出时恢复原上下文。

    Args:
        ctx: 要设置的上下文

    Yields:
        设置的上下文

    示例:
        ctx = ExecutionContext.create_root()
        with with_context(ctx) as current:
            print(f"In context: {current.trace_id}")
            # 此作用域内的所有操作都使用此上下文
        # 作用域外恢复原上下文
    """
    token = _current_context.set(ctx)
    try:
        yield ctx
    finally:
        _current_context.reset(token)


@asynccontextmanager
async def with_context_async(ctx: ExecutionContext):
    """异步上下文作用域

    在作用域内设置指定的上下文，退出时恢复原上下文。

    Args:
        ctx: 要设置的上下文

    Yields:
        设置的上下文

    示例:
        ctx = ExecutionContext.create_root()
        async with with_context_async(ctx) as current:
            response = await http_client.get("/api")
            # 此作用域内的所有操作都使用此上下文
    """
    token = _current_context.set(ctx)
    try:
        yield ctx
    finally:
        _current_context.reset(token)


def run_with_context[T](ctx: ExecutionContext, func: Callable[[], T]) -> T:
    """在指定上下文中运行函数

    Args:
        ctx: 要使用的上下文
        func: 要运行的函数

    Returns:
        函数返回值

    示例:
        ctx = ExecutionContext.create_root()
        result = run_with_context(ctx, lambda: do_something())
    """
    with with_context(ctx):
        return func()
