"""
API测试示例

演示如何使用框架进行HTTP API测试。
"""

import pytest


class TestUserAPI:
    """用户API测试"""

    def test_get_user(self, http_client):
        """测试获取单个用户"""
        # 发送GET请求
        response = http_client.get("/users/1")

        # 断言状态码
        assert response.status_code == 200

        # 断言响应数据
        user = response.json()
        assert user["id"] == 1
        assert "name" in user
        assert "email" in user

    def test_get_all_users(self, http_client):
        """测试获取所有用户"""
        response = http_client.get("/users")

        assert response.status_code == 200

        users = response.json()
        assert isinstance(users, list)
        assert len(users) > 0

    def test_create_user(self, http_client, sample_user_data):
        """测试创建用户"""
        response = http_client.post("/users", json=sample_user_data)

        assert response.status_code == 201

        created_user = response.json()
        assert created_user["name"] == sample_user_data["name"]
        assert created_user["email"] == sample_user_data["email"]

    def test_update_user(self, http_client):
        """测试更新用户"""
        update_data = {
            "name": "李四",
            "email": "lisi@example.com"
        }

        response = http_client.put("/users/1", json=update_data)

        assert response.status_code == 200

        updated_user = response.json()
        assert updated_user["name"] == update_data["name"]

    def test_delete_user(self, http_client):
        """测试删除用户"""
        response = http_client.delete("/users/1")

        assert response.status_code == 200


class TestPostAPI:
    """文章API测试"""

    def test_get_posts(self, http_client):
        """测试获取文章列表"""
        response = http_client.get("/posts")

        assert response.status_code == 200

        posts = response.json()
        assert isinstance(posts, list)
        assert len(posts) > 0

    def test_get_user_posts(self, http_client):
        """测试获取指定用户的文章"""
        response = http_client.get("/posts", params={"userId": 1})

        assert response.status_code == 200

        posts = response.json()
        assert all(post["userId"] == 1 for post in posts)

    def test_create_post(self, http_client, sample_post_data):
        """测试创建文章"""
        response = http_client.post("/posts", json=sample_post_data)

        assert response.status_code == 201

        post = response.json()
        assert post["title"] == sample_post_data["title"]
        assert post["body"] == sample_post_data["body"]


@pytest.mark.parametrize("user_id,expected_name", [
    (1, "Leanne Graham"),
    (2, "Ervin Howell"),
])
def test_get_user_parametrized(http_client, user_id, expected_name):
    """参数化测试：测试多个用户"""
    response = http_client.get(f"/users/{user_id}")

    assert response.status_code == 200

    user = response.json()
    assert user["id"] == user_id
    assert user["name"] == expected_name


class TestErrorHandling:
    """错误处理测试"""

    def test_get_nonexistent_user(self, http_client):
        """测试获取不存在的用户"""
        response = http_client.get("/users/999999")

        # JSONPlaceholder返回空对象，状态码200
        assert response.status_code == 200

    def test_invalid_endpoint(self, http_client):
        """测试无效的端点"""
        response = http_client.get("/invalid-endpoint")

        assert response.status_code == 404


class TestHeaders:
    """请求头测试"""

    def test_custom_headers(self, http_client):
        """测试自定义请求头"""
        headers = {
            "X-Custom-Header": "TestValue"
        }

        response = http_client.get("/users/1", headers=headers)

        assert response.status_code == 200


class TestQueryParams:
    """查询参数测试"""

    def test_filter_posts_by_user(self, http_client):
        """测试通过用户ID过滤文章"""
        params = {"userId": 1}

        response = http_client.get("/posts", params=params)

        assert response.status_code == 200

        posts = response.json()
        assert all(post["userId"] == 1 for post in posts)

    def test_multiple_params(self, http_client):
        """测试多个查询参数"""
        params = {
            "userId": 1,
            "id": 1
        }

        response = http_client.get("/posts", params=params)

        assert response.status_code == 200

        posts = response.json()
        assert len(posts) == 1
        assert posts[0]["id"] == 1
        assert posts[0]["userId"] == 1
