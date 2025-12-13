"""API测试示例模板"""

TEST_EXAMPLE_TEMPLATE = """\"\"\"示例测试

演示如何使用df-test-framework v3.11.1编写测试用例。

v3.11.1最佳实践:
- ✅ 使用runtime fixture获取框架服务
- ✅ 使用settings fixture访问配置
- ✅ 使用http_client fixture发送HTTP请求（同步）
- ✅ 使用AsyncHttpClient进行高性能并发测试
- ✅ 使用Allure装饰器增强报告
- ✅ 使用with_overrides()进行运行时配置覆盖
- ✅ 使用配置化中间件（签名、Token自动处理）
\"\"\"

import pytest
import allure
from df_test_framework.testing.plugins import attach_json, step


@allure.feature("示例功能")
@allure.story("基础测试")
class TestExample:
    \"\"\"示例测试类\"\"\"

    @allure.title("测试框架初始化")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_framework_init(self, runtime, settings):
        \"\"\"测试框架初始化

        验证框架和配置加载正常。
        \"\"\"
        with step("验证Runtime初始化"):
            assert runtime is not None
            assert runtime.settings is not None

        with step("验证配置加载"):
            assert settings is not None
            assert settings.http is not None
            attach_json({{"api_base_url": settings.http.base_url}}, name="HTTP配置")

        with step("验证配置化中间件"):
            # v3.5: 中间件自动从配置加载，无需手动创建
            middleware_count = len(settings.http.middlewares)
            attach_json({{"middleware_count": middleware_count}}, name="中间件数量")

    @allure.title("测试HTTP客户端")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_http_client(self, http_client):
        \"\"\"测试HTTP客户端基本功能

        发送一个简单的HTTP请求验证客户端可用。
        注意：配置化中间件会自动添加签名/Token等认证信息。
        \"\"\"
        with step("发送GET请求"):
            # 注意：需要配置有效的API地址
            # v3.5: 如果配置了中间件，签名/Token会自动添加
            # response = http_client.get("/api/health")
            # assert response.status_code == 200
            pass  # 替换为实际的API调用

    @allure.title("测试运行时配置覆盖")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_runtime_override(self, runtime):
        \"\"\"测试运行时配置覆盖

        v3.5: 使用with_overrides()动态修改配置
        \"\"\"
        with step("创建带覆盖配置的RuntimeContext"):
            # 临时修改超时时间
            new_runtime = runtime.with_overrides({{
                "http.timeout": 60,  # 覆盖超时时间
            }})

            assert new_runtime.settings.http.timeout == 60
            assert runtime.settings.http.timeout != 60  # 原配置不变

        with step("验证配置隔离"):
            # v3.5: with_overrides()创建新实例，不影响原配置
            assert runtime.settings.http.timeout == runtime.settings.http.timeout

    @allure.title("测试Unit of Work模式")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.integration
    def test_uow_pattern(self, uow):
        \"\"\"测试Unit of Work模式

        v3.8: 使用uow fixture管理事务和Repository

        注意：需要在项目中实现uow fixture，参考gift-card-test项目
        \"\"\"
        with step("使用Repository查询"):
            # uow.cards.find_by_card_no("CARD_001")
            # uow.orders.find_by_order_no("ORDER_001")
            pass  # 替换为实际的Repository操作

        with step("执行SQL查询"):
            # from sqlalchemy import text
            # result = uow.session.execute(text("SELECT 1"))
            pass  # 替换为实际的SQL操作

        # ✅ 测试结束后自动回滚，数据不会保留
        # 如需持久化数据，调用 uow.commit()

    @allure.title("测试HTTP Mock功能")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_http_mock(self, http_mock, http_client):
        \"\"\"测试HTTP Mock功能

        v3.5新增: 使用http_mock进行接口Mock，无需真实服务
        \"\"\"
        with step("配置Mock响应"):
            # Mock GET /api/users 接口
            http_mock.get("/api/users", json={{
                "code": 200,
                "data": [{{"id": 1, "name": "Mock User"}}],
                "message": "success"
            }})

        with step("调用被Mock的接口"):
            # 发送请求，会返回Mock数据
            response = http_client.get("/api/users")
            data = response.json()
            attach_json(data, name="Mock响应数据")

        with step("验证Mock响应"):
            assert data["code"] == 200
            assert len(data["data"]) == 1
            assert data["data"][0]["name"] == "Mock User"

        with step("验证接口被调用"):
            # 验证Mock接口被调用了1次
            http_mock.assert_called("/api/users", "GET", times=1)

    @allure.title("测试时间Mock功能")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_time_mock(self, time_mock):
        \"\"\"测试时间Mock功能

        v3.5新增: 使用time_mock进行时间控制，测试时间敏感逻辑
        \"\"\"
        from datetime import datetime

        with step("冻结时间到指定时刻"):
            # 冻结时间到 2024-01-01 12:00:00
            time_mock.freeze("2024-01-01 12:00:00")
            now = datetime.now()
            assert now.year == 2024
            assert now.month == 1
            assert now.hour == 12

        with step("时间前进1小时"):
            # 将时间移动到 2024-01-01 13:00:00
            time_mock.move_to("2024-01-01 13:00:00")
            now = datetime.now()
            assert now.hour == 13

        with step("使用增量前进时间"):
            # 使用 tick 前进指定秒数
            time_mock.tick(seconds=3600)  # 前进1小时
            now = datetime.now()
            assert now.hour == 14

        # ✅ 测试结束后自动恢复真实时间


__all__ = ["TestExample"]
"""

__all__ = ["TEST_EXAMPLE_TEMPLATE"]
