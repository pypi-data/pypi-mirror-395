"""
Pytest配置文件

定义全局fixture和测试配置。
"""

import pytest
from pydantic import Field

from df_test_framework import Bootstrap, FrameworkSettings


class TestSettings(FrameworkSettings):
    """测试环境配置"""

    api_base_url: str = Field(
        default="https://jsonplaceholder.typicode.com",
        description="测试API基础URL"
    )

    database_url: str = Field(
        default="sqlite:///./test.db",
        description="测试数据库URL"
    )


@pytest.fixture(scope="session")
def test_runtime():
    """
    创建测试运行时环境（Session级别，整个测试会话共享）
    """
    app = Bootstrap().with_settings(TestSettings).build()
    runtime = app.run()
    yield runtime
    # 清理资源（如果需要）


@pytest.fixture
def runtime(test_runtime):
    """
    提供runtime实例（Function级别，每个测试函数一个）
    """
    return test_runtime


@pytest.fixture
def http_client(runtime):
    """
    提供HTTP客户端fixture
    """
    return runtime.http_client()


@pytest.fixture
def database(runtime):
    """
    提供数据库客户端fixture
    """
    db = runtime.database()

    # 测试前准备
    yield db

    # 测试后清理（如果需要）
    # db.execute("DELETE FROM test_table")


@pytest.fixture
def sample_user_data():
    """
    提供测试用户数据
    """
    return {
        "name": "张三",
        "username": "zhangsan",
        "email": "zhangsan@example.com"
    }


@pytest.fixture
def sample_post_data():
    """
    提供测试文章数据
    """
    return {
        "userId": 1,
        "title": "测试文章标题",
        "body": "这是测试文章的内容"
    }
