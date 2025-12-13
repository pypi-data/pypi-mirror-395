"""API 类自动注册装饰器单元测试"""

from df_test_framework.capabilities.clients.http.rest.httpx.base_api import BaseAPI
from df_test_framework.testing.decorators.api_class import (
    _api_registry,
    api_class,
    create_api_fixture,
    get_api_registry,
    load_api_fixtures,
)


class TestApiClassDecorator:
    """api_class 装饰器测试"""

    def setup_method(self):
        """每个测试前清空注册表"""
        _api_registry.clear()

    def test_decorator_with_name(self):
        """测试带名称的装饰器"""

        @api_class("test_api")
        class TestAPI(BaseAPI):
            pass

        assert "test_api" in _api_registry
        assert _api_registry["test_api"][0] == TestAPI
        assert _api_registry["test_api"][1] == "session"  # 默认 scope

    def test_decorator_auto_name(self):
        """测试自动生成名称"""

        @api_class()
        class UserAPI(BaseAPI):
            pass

        assert "user_api" in _api_registry

    def test_decorator_auto_name_with_api_suffix(self):
        """测试自动生成名称（已有 API 后缀）"""

        @api_class()
        class MasterCardAPI(BaseAPI):
            pass

        # MasterCardAPI -> master_card_api
        assert "master_card_api" in _api_registry

    def test_decorator_custom_scope(self):
        """测试自定义 scope"""

        @api_class("custom_api", scope="function")
        class CustomAPI(BaseAPI):
            pass

        assert _api_registry["custom_api"][1] == "function"

    def test_decorator_with_dependencies(self):
        """测试带依赖的装饰器"""

        @api_class("dep_api", http_client="custom_http", db="database")
        class DepAPI(BaseAPI):
            pass

        deps = _api_registry["dep_api"][2]
        assert deps["http_client"] == "custom_http"
        assert deps["db"] == "database"

    def test_decorator_returns_class(self):
        """测试装饰器返回原始类"""

        @api_class("orig_api")
        class OriginalAPI(BaseAPI):
            pass

        assert OriginalAPI.__name__ == "OriginalAPI"


class TestGetApiRegistry:
    """get_api_registry 函数测试"""

    def setup_method(self):
        """每个测试前清空注册表"""
        _api_registry.clear()

    def test_get_registry_copy(self):
        """测试获取注册表副本"""

        @api_class("reg_api")
        class RegAPI(BaseAPI):
            pass

        registry = get_api_registry()
        assert "reg_api" in registry

        # 修改副本不影响原始
        registry["new_api"] = None
        assert "new_api" not in _api_registry

    def test_get_empty_registry(self):
        """测试获取空注册表"""
        registry = get_api_registry()
        assert registry == {}


class TestCreateApiFixture:
    """create_api_fixture 函数测试"""

    def test_create_fixture_basic(self):
        """测试创建基本 fixture"""

        class SimpleAPI(BaseAPI):
            def __init__(self, http_client):
                super().__init__(http_client)

        fixture = create_api_fixture(SimpleAPI, "simple_api")
        assert fixture is not None
        assert fixture.__name__ == "simple_api"

    def test_create_fixture_with_scope(self):
        """测试创建带 scope 的 fixture"""

        class ScopedAPI(BaseAPI):
            def __init__(self, http_client):
                super().__init__(http_client)

        fixture = create_api_fixture(ScopedAPI, "scoped_api", scope="module")
        assert fixture is not None

    def test_create_fixture_auto_infer_deps(self):
        """测试自动推断依赖"""

        class AutoAPI(BaseAPI):
            def __init__(self, http_client, settings):
                super().__init__(http_client)
                self.settings = settings

        fixture = create_api_fixture(AutoAPI, "auto_api")
        assert fixture is not None


class TestLoadApiFixtures:
    """load_api_fixtures 函数测试"""

    def setup_method(self):
        """每个测试前清空注册表"""
        _api_registry.clear()

    def test_load_fixtures_to_module(self):
        """测试加载 fixtures 到模块"""

        @api_class("load_api")
        class LoadAPI(BaseAPI):
            def __init__(self, http_client):
                super().__init__(http_client)

        module_globals = {}
        load_api_fixtures(module_globals)

        assert "load_api" in module_globals

    def test_load_multiple_fixtures(self):
        """测试加载多个 fixtures"""

        @api_class("api_one")
        class APIOne(BaseAPI):
            def __init__(self, http_client):
                super().__init__(http_client)

        @api_class("api_two")
        class APITwo(BaseAPI):
            def __init__(self, http_client):
                super().__init__(http_client)

        module_globals = {}
        load_api_fixtures(module_globals)

        assert "api_one" in module_globals
        assert "api_two" in module_globals


class TestAutoNaming:
    """自动命名测试"""

    def setup_method(self):
        """每个测试前清空注册表"""
        _api_registry.clear()

    def test_camel_case_conversion(self):
        """测试驼峰命名转换"""

        @api_class()
        class PaymentGatewayAPI(BaseAPI):
            pass

        # PaymentGatewayAPI -> payment_gateway_api
        assert "payment_gateway_api" in _api_registry

    def test_single_word(self):
        """测试单词命名"""

        @api_class()
        class OrderAPI(BaseAPI):
            pass

        # OrderAPI -> order_api
        assert "order_api" in _api_registry

    def test_already_snake_case(self):
        """测试已经是 snake_case 的类名"""

        @api_class()
        class UserProfileAPI(BaseAPI):  # noqa: N801
            pass

        # 会按驼峰规则转换
        assert any("user" in key.lower() for key in _api_registry.keys())
