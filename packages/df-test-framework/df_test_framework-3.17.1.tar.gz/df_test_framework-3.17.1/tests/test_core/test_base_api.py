"""
测试BaseAPI核心功能

验证BaseAPI的响应解析和业务错误处理

v3.3.0 说明:
- BaseAPI不再支持拦截器（已移至HttpClient）
- 本测试只验证BaseAPI的核心功能：响应解析、业务错误处理
"""

from typing import Any
from unittest.mock import Mock

import httpx
import pytest
from pydantic import BaseModel

from df_test_framework.capabilities.clients.http.rest.httpx.base_api import (
    BaseAPI,
    BusinessError,
)


class MockHttpClient:
    """模拟HttpClient"""

    def __init__(self):
        self.last_url = ""
        self.last_kwargs = {}
        self.mock_response = None

    def get(self, url: str, **kwargs) -> httpx.Response:
        self.last_url = url
        self.last_kwargs = kwargs
        return self.mock_response

    def post(self, url: str, **kwargs) -> httpx.Response:
        self.last_url = url
        self.last_kwargs = kwargs
        return self.mock_response

    def put(self, url: str, **kwargs) -> httpx.Response:
        self.last_url = url
        self.last_kwargs = kwargs
        return self.mock_response

    def delete(self, url: str, **kwargs) -> httpx.Response:
        self.last_url = url
        self.last_kwargs = kwargs
        return self.mock_response


def create_mock_response(
    status_code: int = 200, json_data: dict[str, Any] = None
) -> httpx.Response:
    """创建mock httpx.Response"""
    mock_response = Mock(spec=httpx.Response)
    mock_response.status_code = status_code
    mock_response.text = str(json_data)
    mock_response.json.return_value = json_data or {}

    # Mock raise_for_status
    def raise_for_status():
        if status_code >= 400:
            error = httpx.HTTPStatusError(
                message=f"HTTP {status_code}", request=Mock(), response=mock_response
            )
            raise error

    mock_response.raise_for_status = raise_for_status
    return mock_response


class TestBaseAPIBusinessError:
    """测试业务错误处理"""

    def test_default_no_check(self):
        """测试默认不检查业务错误"""
        http_client = MockHttpClient()
        api = BaseAPI(http_client)

        # 默认 _check_business_error 不做任何检查
        response_data = {"code": 500, "message": "业务错误"}
        api._check_business_error(response_data)  # 不应抛出异常

    def test_custom_check_success_field(self):
        """测试自定义检查 success 字段"""

        class CustomAPI(BaseAPI):
            def _check_business_error(self, response_data):
                if not response_data.get("success", True):
                    raise BusinessError(
                        message=response_data.get("message", "未知错误"),
                        code=response_data.get("code"),
                        data=response_data,
                    )

        http_client = MockHttpClient()
        api = CustomAPI(http_client)

        # 成功情况
        api._check_business_error({"success": True, "data": {}})

        # 失败情况
        with pytest.raises(BusinessError) as exc_info:
            api._check_business_error({"success": False, "code": 1001, "message": "参数错误"})

        assert exc_info.value.code == 1001
        assert exc_info.value.message == "参数错误"

    def test_custom_check_code_field(self):
        """测试自定义检查 code 字段"""

        class CustomAPI(BaseAPI):
            def _check_business_error(self, response_data):
                code = response_data.get("code", 200)
                if code not in [200, 0]:
                    raise BusinessError(
                        message=response_data.get("message", "未知错误"),
                        code=code,
                        data=response_data,
                    )

        http_client = MockHttpClient()
        api = CustomAPI(http_client)

        # 成功情况
        api._check_business_error({"code": 200, "data": {}})
        api._check_business_error({"code": 0, "data": {}})

        # 失败情况
        with pytest.raises(BusinessError) as exc_info:
            api._check_business_error({"code": 500, "message": "服务器错误"})

        assert exc_info.value.code == 500
        assert exc_info.value.message == "服务器错误"

    def test_business_error_str(self):
        """测试BusinessError字符串表示"""
        error1 = BusinessError("错误消息")
        assert str(error1) == "[业务错误] 错误消息"

        error2 = BusinessError("错误消息", code=1001)
        assert str(error2) == "[业务错误 1001] 错误消息"


class TestBaseAPIParsing:
    """测试响应解析"""

    def test_parse_json_response(self):
        """测试解析JSON响应"""
        http_client = MockHttpClient()
        api = BaseAPI(http_client)

        response_data = {"code": 200, "data": {"id": 1, "name": "测试"}}
        mock_response = create_mock_response(200, response_data)

        result = api._parse_response(
            mock_response, raise_for_status=False, check_business_error=False
        )
        assert result == response_data

    def test_parse_with_pydantic_model(self):
        """测试使用Pydantic模型解析"""

        class UserModel(BaseModel):
            id: int
            name: str

        http_client = MockHttpClient()
        api = BaseAPI(http_client)

        response_data = {"id": 1, "name": "测试用户"}
        mock_response = create_mock_response(200, response_data)

        result = api._parse_response(
            mock_response, model=UserModel, raise_for_status=False, check_business_error=False
        )
        assert isinstance(result, UserModel)
        assert result.id == 1
        assert result.name == "测试用户"

    def test_parse_http_error(self):
        """测试HTTP错误"""
        http_client = MockHttpClient()
        api = BaseAPI(http_client)

        mock_response = create_mock_response(404, {"error": "Not Found"})

        with pytest.raises(httpx.HTTPStatusError):
            api._parse_response(mock_response, raise_for_status=True)

    def test_get_method(self):
        """测试GET方法"""
        http_client = MockHttpClient()
        api = BaseAPI(http_client)

        response_data = {"code": 200, "data": {}}
        http_client.mock_response = create_mock_response(200, response_data)

        result = api.get("/api/users", check_business_error=False)
        assert result == response_data
        assert http_client.last_url == "api/users"

    def test_post_method(self):
        """测试POST方法"""
        http_client = MockHttpClient()
        api = BaseAPI(http_client)

        response_data = {"code": 200, "data": {"id": 1}}
        http_client.mock_response = create_mock_response(200, response_data)

        result = api.post("/api/users", json={"name": "test"}, check_business_error=False)
        assert result == response_data
        assert http_client.last_url == "api/users"
        assert http_client.last_kwargs["json"] == {"name": "test"}

    def test_put_method(self):
        """测试PUT方法"""
        http_client = MockHttpClient()
        api = BaseAPI(http_client)

        response_data = {"code": 200, "data": {"id": 1}}
        http_client.mock_response = create_mock_response(200, response_data)

        result = api.put("/api/users/1", json={"name": "updated"}, check_business_error=False)
        assert result == response_data
        assert http_client.last_url == "api/users/1"

    def test_delete_method(self):
        """测试DELETE方法"""
        http_client = MockHttpClient()
        api = BaseAPI(http_client)

        response_data = {"code": 200, "data": {}}
        http_client.mock_response = create_mock_response(200, response_data)

        result = api.delete("/api/users/1", check_business_error=False)
        assert result == response_data
        assert http_client.last_url == "api/users/1"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
