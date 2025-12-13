"""测试 GraphQL 查询构建器"""

from df_test_framework.capabilities.clients.graphql.query_builder import QueryBuilder


class TestQueryBuilder:
    """测试 QueryBuilder"""

    def test_simple_query(self) -> None:
        """测试简单查询"""
        query = QueryBuilder().query("getUser").field("id").field("name").field("email").build()

        assert "query {" in query
        assert "getUser" in query
        assert "id" in query
        assert "name" in query
        assert "email" in query

    def test_query_with_arguments(self) -> None:
        """测试带参数的查询"""
        query = QueryBuilder().query("getUser", {"id": "123"}).field("id").field("name").build()

        assert 'getUser(id: "123")' in query

    def test_query_with_variables(self) -> None:
        """测试带变量的查询"""
        query = (
            QueryBuilder()
            .query("getUser", {"id": "$userId"})
            .field("id")
            .field("name")
            .variable("userId", "ID!")
            .build()
        )

        assert "query($userId: ID!)" in query
        assert "getUser(id: $userId)" in query

    def test_query_with_nested_fields(self) -> None:
        """测试嵌套字段查询"""
        query = (
            QueryBuilder()
            .query("getUser")
            .field("id")
            .field("name")
            .field("posts", ["id", "title", "content"])
            .build()
        )

        assert "getUser" in query
        assert "posts" in query
        assert "title" in query
        assert "content" in query

    def test_mutation(self) -> None:
        """测试变更操作"""
        mutation = (
            QueryBuilder()
            .mutation("createUser", {"input": "$input"})
            .field("id")
            .field("name")
            .variable("input", "CreateUserInput!")
            .build()
        )

        assert "mutation($input: CreateUserInput!)" in mutation
        assert "createUser(input: $input)" in mutation

    def test_subscription(self) -> None:
        """测试订阅操作"""
        subscription = (
            QueryBuilder()
            .subscription("messageAdded", {"channelId": "$channelId"})
            .field("id")
            .field("content")
            .variable("channelId", "ID!")
            .build()
        )

        assert "subscription($channelId: ID!)" in subscription
        assert "messageAdded(channelId: $channelId)" in subscription

    def test_multiple_variables(self) -> None:
        """测试多个变量"""
        query = (
            QueryBuilder()
            .query("searchUsers", {"name": "$name", "limit": "$limit"})
            .field("id")
            .field("name")
            .variable("name", "String!")
            .variable("limit", "Int")
            .build()
        )

        assert "$name: String!" in query
        assert "$limit: Int" in query

    def test_format_boolean_value(self) -> None:
        """测试布尔值格式化"""
        query = QueryBuilder().query("getUsers", {"active": True}).field("id").build()

        assert "active: true" in query

    def test_format_null_value(self) -> None:
        """测试 null 值格式化"""
        query = QueryBuilder().query("getUsers", {"email": None}).field("id").build()

        assert "email: null" in query

    def test_format_list_value(self) -> None:
        """测试列表值格式化"""
        query = QueryBuilder().query("getUsers", {"ids": [1, 2, 3]}).field("id").build()

        assert "ids: [1, 2, 3]" in query

    def test_format_dict_value(self) -> None:
        """测试字典值格式化"""
        query = (
            QueryBuilder()
            .query("createUser", {"input": {"name": "Alice", "age": 30}})
            .field("id")
            .build()
        )

        assert 'input: {name: "Alice", age: 30}' in query

    def test_deeply_nested_fields(self) -> None:
        """测试深度嵌套字段"""
        query = (
            QueryBuilder()
            .query("getUser")
            .field("id")
            .field("profile", ["bio", "avatar"])
            .field("posts", ["id", "title"])
            .build()
        )

        assert "profile" in query
        assert "bio" in query
        assert "avatar" in query
        assert "posts" in query
