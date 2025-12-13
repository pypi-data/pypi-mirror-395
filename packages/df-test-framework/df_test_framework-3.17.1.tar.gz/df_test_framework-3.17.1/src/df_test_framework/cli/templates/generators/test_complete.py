"""完整测试文件生成模板

包含实际实现示例，减少TODO占位符。
"""

GEN_TEST_COMPLETE_TEMPLATE = """\"\"\"测试文件: {test_name}

使用df-test-framework v3.7进行API测试。

测试覆盖:
- ✅ 正常场景：成功调用API
- ✅ 参数校验：参数化测试
- ✅ 异常场景：错误处理
- ✅ Mock场景：外部依赖隔离

v3.7特性:
- ✅ Unit of Work模式（uow）
- ✅ HTTP Mock支持（http_mock）
- ✅ 配置化中间件（签名、Token自动处理）
\"\"\"

import pytest
import allure
from assertpy import assert_that
from df_test_framework.testing.plugins import attach_json, step


@allure.feature("{feature_name}")
@allure.story("{story_name}")
class Test{TestName}:
    \"\"\"{TestName}测试类

    测试场景:
    1. test_{method_name}_success - 成功场景
    2. test_{method_name}_validation - 参数校验场景
    3. test_{method_name}_with_mock - Mock场景
    \"\"\"

    # ========== 正常场景 ==========

    @allure.title("测试{test_description} - 成功场景")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_{method_name}_success(
        self,
        http_client,
        uow,
        runtime  # v3.7 RuntimeContext
    ):
        \"\"\"测试{test_description} - 成功场景

        前置条件: 数据准备完成
        预期结果: API调用成功，返回预期数据

        示例: 测试创建用户接口
        \"\"\"
        with step("1. 准备测试数据"):
            # 使用 Builder 快速构建测试数据
            # 取消注释并根据实际情况修改：
            # from {{project_name}}.builders import {EntityName}Builder

            test_data = {{
                "name": "测试用户",
                "email": "test@example.com",
                "phone": "13800138000",
            }}

            # 使用Builder模式（推荐）:
            # test_data = (
            #     {EntityName}Builder()
            #     .with_name("测试用户")
            #     .with_email("test@example.com")
            #     .build()
            # )

            attach_json(test_data, name="请求数据")

        with step("2. 调用API"):
            # v3.5: 配置化中间件自动添加签名/Token
            # 根据实际API修改HTTP方法和路径
            response = http_client.post("/api/{api_path}", json=test_data)

            # 验证HTTP状态码
            assert_that(response.status_code).is_equal_to(200)

            # 解析响应
            result = response.json()
            attach_json(result, name="响应数据")

        with step("3. 验证响应数据"):
            # 验证响应结构（根据实际响应格式修改）
            assert_that(result).contains_key("code", "data", "message")
            assert_that(result["code"]).is_equal_to(200)
            assert_that(result["message"]).is_equal_to("success")

            # 验证业务数据
            data = result["data"]
            assert_that(data).is_not_none()
            # assert_that(data["id"]).is_not_none()  # 根据实际字段修改
            # assert_that(data["name"]).is_equal_to("测试用户")

        with step("4. 验证数据库状态"):
            # 使用 UoW 的 Repository 验证数据持久化
            # entity = uow.{entity_name}s.find_by_id(data["id"])
            #
            # assert_that(entity).is_not_none()
            # assert_that(entity.name).is_equal_to("测试用户")
            # assert_that(entity.status).is_equal_to("active")

            pass  # 如果不需要数据库验证，保留pass

        # ✅ 测试结束后自动回滚数据库，无需手动清理

    # ========== 参数校验场景 ==========

    @allure.title("测试{test_description} - 参数校验")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("invalid_field,invalid_value,expected_error", [
        ("name", "", "名称不能为空"),
        ("name", "a" * 101, "名称长度不能超过100"),
        ("email", "invalid_email", "邮箱格式错误"),
        ("phone", "123", "手机号格式错误"),
    ], ids=["空名称", "名称过长", "邮箱格式错误", "手机号格式错误"])
    def test_{method_name}_validation(
        self,
        http_client,
        invalid_field,
        invalid_value,
        expected_error
    ):
        \"\"\"测试{test_description} - 参数校验

        前置条件: 发送无效参数
        预期结果: 返回 400 错误，包含错误信息
        \"\"\"
        with step("构建无效请求数据"):
            # 构建包含无效字段的数据
            test_data = {{
                "name": "测试用户",
                "email": "test@example.com",
                "phone": "13800138000",
            }}
            test_data[invalid_field] = invalid_value
            attach_json(test_data, name="无效请求数据")

        with step("调用API并验证错误"):
            response = http_client.post("/api/{api_path}", json=test_data)

            # 验证返回400错误
            assert_that(response.status_code).is_equal_to(400)

            result = response.json()
            attach_json(result, name="错误响应")

            # 验证错误信息
            assert_that(result["code"]).is_equal_to(400)
            # 根据实际错误响应格式修改
            # assert_that(result["message"]).contains(expected_error)

    # ========== 异常场景 ==========

    @allure.title("测试{test_description} - 重复数据")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_{method_name}_duplicate(self, http_client, uow):
        \"\"\"测试{test_description} - 重复数据处理

        前置条件: 数据已存在
        预期结果: 返回 409 冲突错误
        \"\"\"
        with step("1. 创建第一条数据"):
            test_data = {{
                "name": "测试用户",
                "email": "duplicate@example.com",
            }}

            # 使用UoW的Repository直接创建数据
            # uow.{entity_name}s.create(test_data)

            # 或者通过API创建
            response = http_client.post("/api/{api_path}", json=test_data)
            assert_that(response.status_code).is_equal_to(200)

        with step("2. 尝试创建重复数据"):
            response = http_client.post("/api/{api_path}", json=test_data)

            # 验证返回409冲突错误（根据实际API行为修改）
            assert_that(response.status_code).is_in(400, 409)

            result = response.json()
            # assert_that(result["message"]).contains("已存在")

    # ========== Mock 场景 ==========

    @allure.title("测试{test_description} - Mock外部依赖")
    @allure.severity(allure.severity_level.NORMAL)
    def test_{method_name}_with_mock(self, http_mock, http_client):
        \"\"\"测试{test_description} - 使用 HTTP Mock 隔离外部依赖

        场景: 当API需要调用外部服务时，使用Mock隔离
        示例: 创建用户时需要调用短信服务发送验证码
        \"\"\"
        with step("1. 配置Mock响应"):
            # Mock外部短信服务
            http_mock.post("/api/sms/send", json={{
                "code": 200,
                "data": {{"message_id": "mock_123"}}
            }})

            # Mock其他外部服务
            # http_mock.get("/api/external/validate", json={{
            #     "code": 200,
            #     "data": {{"valid": True}}
            # }})

        with step("2. 调用API（触发外部调用）"):
            test_data = {{
                "name": "测试用户",
                "phone": "13800138000",
            }}

            response = http_client.post("/api/{api_path}", json=test_data)
            assert_that(response.status_code).is_equal_to(200)

        with step("3. 验证Mock被正确调用"):
            # 验证Mock服务被调用
            http_mock.assert_called("/api/sms/send", "POST", times=1)

            # 验证调用参数（如果需要）
            # calls = http_mock.get_calls("/api/sms/send")
            # assert_that(calls).is_length(1)
            # assert_that(calls[0]["json"]["phone"]).is_equal_to("13800138000")


__all__ = ["Test{TestName}"]
"""

__all__ = ["GEN_TEST_COMPLETE_TEMPLATE"]
