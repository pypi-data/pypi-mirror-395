"""
使用Fixture进行测试示例

演示如何使用框架提供的各种fixture。
"""

import pytest


class TestWithRuntime:
    """使用runtime fixture的测试"""

    def test_access_settings(self, runtime):
        """测试访问配置"""
        assert runtime.settings is not None
        assert runtime.settings.api_base_url is not None

    def test_get_http_client(self, runtime):
        """测试获取HTTP客户端"""
        http_client = runtime.http_client()
        assert http_client is not None

    def test_get_database(self, runtime):
        """测试获取数据库客户端"""
        database = runtime.database()
        assert database is not None


class TestWithHttpClient:
    """使用http_client fixture的测试"""

    def test_http_client_get(self, http_client):
        """测试HTTP GET请求"""
        response = http_client.get("/users/1")

        assert response.status_code == 200
        assert response.json()["id"] == 1

    def test_http_client_post(self, http_client, sample_user_data):
        """测试HTTP POST请求"""
        response = http_client.post("/users", json=sample_user_data)

        assert response.status_code == 201
        assert response.json()["name"] == sample_user_data["name"]


class TestWithDatabase:
    """使用database fixture的测试"""

    def test_database_execute(self, database):
        """测试数据库执行"""
        # 创建临时表
        database.execute("""
            CREATE TABLE IF NOT EXISTS temp_test (
                id INTEGER PRIMARY KEY,
                value TEXT
            )
        """)

        # 插入数据
        database.execute(
            "INSERT INTO temp_test (id, value) VALUES (?, ?)",
            (1, "test")
        )

        # 查询数据
        result = database.execute("SELECT * FROM temp_test WHERE id = 1")

        assert len(result) == 1
        assert result[0]["value"] == "test"

        # 清理
        database.execute("DROP TABLE temp_test")


class TestWithMultipleFixtures:
    """使用多个fixture的测试"""

    def test_with_runtime_and_http_client(self, runtime, http_client):
        """测试同时使用runtime和http_client"""
        # 使用runtime
        settings = runtime.settings

        # 使用http_client
        response = http_client.get("/users/1")

        assert response.status_code == 200
        assert settings is not None

    def test_with_all_fixtures(self, runtime, http_client, database):
        """测试同时使用所有fixture"""
        # 验证所有fixture都可用
        assert runtime is not None
        assert http_client is not None
        assert database is not None

        # 使用HTTP客户端
        response = http_client.get("/users/1")
        assert response.status_code == 200

        # 使用数据库
        result = database.execute("SELECT 1 as num")
        assert result[0]["num"] == 1


class TestWithSampleData:
    """使用测试数据fixture的测试"""

    def test_with_sample_user_data(self, sample_user_data):
        """测试使用示例用户数据"""
        assert "name" in sample_user_data
        assert "email" in sample_user_data
        assert sample_user_data["name"] == "张三"

    def test_with_sample_post_data(self, sample_post_data):
        """测试使用示例文章数据"""
        assert "title" in sample_post_data
        assert "body" in sample_post_data
        assert sample_post_data["userId"] == 1

    def test_create_user_with_sample_data(self, http_client, sample_user_data):
        """测试使用示例数据创建用户"""
        response = http_client.post("/users", json=sample_user_data)

        assert response.status_code == 201
        assert response.json()["name"] == sample_user_data["name"]


@pytest.fixture
def custom_fixture():
    """自定义fixture示例"""
    print("\n设置自定义fixture")
    yield "自定义数据"
    print("\n清理自定义fixture")


class TestWithCustomFixture:
    """使用自定义fixture的测试"""

    def test_custom_fixture(self, custom_fixture):
        """测试自定义fixture"""
        assert custom_fixture == "自定义数据"


# Fixture scope示例
@pytest.fixture(scope="module")
def module_fixture():
    """模块级别的fixture（整个模块只执行一次）"""
    return "模块级别数据"


@pytest.fixture(scope="function")
def function_fixture():
    """函数级别的fixture（每个测试函数都执行一次）"""
    return "函数级别数据"


class TestFixtureScope:
    """Fixture作用域测试"""

    def test_module_fixture_1(self, module_fixture):
        """第一次使用模块fixture"""
        assert module_fixture == "模块级别数据"

    def test_module_fixture_2(self, module_fixture):
        """第二次使用模块fixture（不会重新创建）"""
        assert module_fixture == "模块级别数据"

    def test_function_fixture_1(self, function_fixture):
        """第一次使用函数fixture"""
        assert function_fixture == "函数级别数据"

    def test_function_fixture_2(self, function_fixture):
        """第二次使用函数fixture（会重新创建）"""
        assert function_fixture == "函数级别数据"
