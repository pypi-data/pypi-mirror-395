"""GraphQL 客户端模块

提供 GraphQL API 测试能力，支持：
- Query/Mutation/Subscription 操作
- 变量参数化
- 片段（Fragment）支持
- 批量查询
- 文件上传
- 订阅（WebSocket）
"""

from df_test_framework.capabilities.clients.graphql.client import GraphQLClient
from df_test_framework.capabilities.clients.graphql.models import (
    GraphQLError,
    GraphQLRequest,
    GraphQLResponse,
)
from df_test_framework.capabilities.clients.graphql.query_builder import QueryBuilder

__all__ = [
    "GraphQLClient",
    "GraphQLRequest",
    "GraphQLResponse",
    "GraphQLError",
    "QueryBuilder",
]
