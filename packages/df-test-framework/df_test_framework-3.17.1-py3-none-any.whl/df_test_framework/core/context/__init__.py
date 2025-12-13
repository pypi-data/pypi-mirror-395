"""
上下文传播系统

提供请求上下文的创建、管理和传播能力。

核心组件:
- ExecutionContext: 执行上下文，贯穿整个请求链路
- get_current_context: 获取当前上下文
- with_context: 上下文作用域管理
"""

from df_test_framework.core.context.execution import ExecutionContext
from df_test_framework.core.context.propagation import (
    get_current_context,
    get_or_create_context,
    run_with_context,
    set_current_context,
    with_context,
    with_context_async,
)

__all__ = [
    # 上下文
    "ExecutionContext",
    # 传播
    "get_current_context",
    "get_or_create_context",
    "with_context",
    "with_context_async",
    "run_with_context",
    "set_current_context",
]
