"""测试文件生成模板"""

GEN_TEST_TEMPLATE = """\"\"\"测试文件: {test_name}

使用df-test-framework v3.11.1进行API测试。

v3.11.1特性:
- ✅ P0-1: BaseAPI 自动处理 Pydantic 序列化
- ✅ P0-2: Database 查询辅助方法 (find_one, find_many)
- ✅ P0-3: 增强 DataGenerator（订单号、手机号等）
- ✅ P1-1: API 类自动发现和注册（@api_class）
- ✅ P1-2: UoW 自动发现 Repository
- ✅ P1-3: CleanupManager 便捷清理方法
- ✅ 异步HTTP客户端（AsyncHttpClient）
- ✅ HTTP Mock支持（http_mock）
- ✅ 配置化中间件（签名、Token自动处理）
\"\"\"

import pytest
import allure
from df_test_framework import DataGenerator
from df_test_framework.testing.fixtures import SimpleCleanupManager
from df_test_framework.testing.plugins import attach_json, step


@allure.feature("{feature_name}")
@allure.story("{story_name}")
class Test{TestName}:
    \"\"\"{TestName}测试类\"\"\"

    @allure.title("测试{test_description}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_{method_name}(self, request, http_client, database, uow):
        \"\"\"测试{test_description}

        v3.11.1:
        - UoW 自动回滚数据（Repository 创建的数据）
        - CleanupManager 清理 API 数据
        \"\"\"
        # 初始化清理管理器（v3.11.1 P1-3）
        cleanup = SimpleCleanupManager(request, database)

        # 数据生成器（v3.11.1 P0-3）
        gen = DataGenerator()

        with step("准备测试数据"):
            # TODO: 准备测试数据
            # 方式1: 使用DataGenerator生成测试数据（v3.11.1 P0-3）
            # order_no = gen.order_no(prefix="TEST")
            # phone = gen.chinese_phone()
            # email = gen.email()

            # 方式2: 使用Builder模式快速构建数据
            # from {{project_name}}.builders import UserBuilder
            # user_data = UserBuilder().with_name("test_user").build()

            # 方式3: 使用Database查询辅助（v3.11.1 P0-2）
            # existing_user = database.find_one("users", {{"name": "test"}})
            pass

        with step("调用API"):
            # TODO: 调用API
            # 提示1: 配置化中间件会自动添加签名/Token
            # response = http_client.get("/api/path")

            # 提示2: 使用Pydantic模型会自动序列化（v3.11.1 P0-1）
            # from {{project_name}}.models.requests import CreateUserRequest
            # request_model = CreateUserRequest(name="Alice", email=gen.email())
            # response = http_client.post("/api/users", json=request_model)
            # # ✅ 自动调用 request_model.model_dump(mode='json', by_alias=True)

            # 提示3: 注册API数据清理（v3.11.1 P1-3）
            # response_data = response.json()
            # user_id = response_data["data"]["id"]
            # cleanup.add_api_data(http_client, "/api/users/{{id}}", user_id)
            pass

        with step("验证响应"):
            # TODO: 验证响应数据
            # data = response.json()
            # attach_json(data, name="响应数据")
            # assert data["code"] == 200
            pass

        with step("验证数据库"):
            # TODO: 验证数据库状态
            # 提示1: UoW自动发现Repository（v3.11.1 P1-2）
            # user = uow.users.find_by_id(user_id)  # ✅ uow.users 自动可用
            # assert user is not None

            # 提示2: Database查询辅助（v3.11.1 P0-2）
            # user = database.find_one("users", {{"id": user_id}})
            # users = database.find_many("users", {{"status": 1}})
            pass

        # ✅ 测试结束后:
        # - UoW 自动回滚（Repository 创建的数据）
        # - CleanupManager 自动清理（API 创建的数据）
        cleanup.cleanup()

    @allure.title("测试{test_description} - Mock模式")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_{method_name}_with_mock(self, http_mock, http_client):
        \"\"\"测试{test_description}（使用HTTP Mock）

        v3.5新增: 使用http_mock隔离外部依赖
        \"\"\"
        with step("配置Mock响应"):
            # TODO: 配置Mock
            # http_mock.get("/api/external", json={{
            #     "code": 200,
            #     "data": {{"mock": "data"}},
            # }})
            pass

        with step("调用API（返回Mock数据）"):
            # TODO: 调用API
            # response = http_client.get("/api/external")
            # data = response.json()
            # assert data["code"] == 200
            pass

        with step("验证Mock调用"):
            # TODO: 验证Mock被正确调用
            # http_mock.assert_called("/api/external", "GET", times=1)
            pass


__all__ = ["Test{TestName}"]
"""

__all__ = ["GEN_TEST_TEMPLATE"]
