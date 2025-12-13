"""API客户端生成模板"""

GEN_API_CLIENT_TEMPLATE = """\"\"\"API客户端: {api_name}

封装{api_name}相关的API调用。
\"\"\"

from df_test_framework import BaseAPI, HttpClient
from df_test_framework.capabilities.clients.http.rest.httpx import BusinessError
from df_test_framework.testing.decorators import api_class
from typing import Dict, Any, List


@api_class("{api_name}_api", scope="session")
class {ApiName}API(BaseAPI):
    \"\"\"{ApiName} API客户端

    封装{api_name}相关的HTTP API调用。

    Example:
        >>> api = {ApiName}API(http_client)
        >>> # GET请求
        >>> result = api.get_{method_name}(item_id)
        >>> # POST请求
        >>> result = api.create_{method_name}(data)
        >>> # PUT请求
        >>> result = api.update_{method_name}(item_id, data)
        >>> # DELETE请求
        >>> api.delete_{method_name}(item_id)
    \"\"\"

    def __init__(self, http_client: HttpClient):
        \"\"\"初始化API客户端

        Args:
            http_client: HTTP客户端
        \"\"\"
        super().__init__(http_client)
        self.base_path = "/api/{api_path}"

    def get_{method_name}(self, {method_name}_id: int) -> Dict[str, Any]:
        \"\"\"获取单个{api_name}

        Args:
            {method_name}_id: {api_name} ID

        Returns:
            Dict: {api_name}数据

        Raises:
            BusinessError: 业务错误
        \"\"\"
        response = self.http_client.get(f"{{self.base_path}}/{{{{method_name}}_id}}")
        data = response.json()
        self._check_business_error(data)
        return data

    def list_{method_name}s(self, page: int = 1, size: int = 10) -> List[Dict[str, Any]]:
        \"\"\"获取{api_name}列表

        Args:
            page: 页码
            size: 每页数量

        Returns:
            List[Dict]: {api_name}列表
        \"\"\"
        response = self.http_client.get(
            self.base_path,
            params={{"page": page, "size": size}}
        )
        data = response.json()
        self._check_business_error(data)
        return data.get("data", [])

    def create_{method_name}(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        \"\"\"创建{api_name}

        Args:
            request_data: 请求数据

        Returns:
            Dict: 创建结果
        \"\"\"
        response = self.http_client.post(self.base_path, json=request_data)
        data = response.json()
        self._check_business_error(data)
        return data

    def update_{method_name}(self, {method_name}_id: int, request_data: Dict[str, Any]) -> Dict[str, Any]:
        \"\"\"更新{api_name}

        Args:
            {method_name}_id: {api_name} ID
            request_data: 请求数据

        Returns:
            Dict: 更新结果
        \"\"\"
        response = self.http_client.put(
            f"{{self.base_path}}/{{{{method_name}}_id}}",
            json=request_data
        )
        data = response.json()
        self._check_business_error(data)
        return data

    def delete_{method_name}(self, {method_name}_id: int) -> None:
        \"\"\"删除{api_name}

        Args:
            {method_name}_id: {api_name} ID
        \"\"\"
        response = self.http_client.delete(f"{{self.base_path}}/{{{{method_name}}_id}}")
        data = response.json()
        self._check_business_error(data)

    def _check_business_error(self, response_data: dict) -> None:
        \"\"\"检查业务错误

        Args:
            response_data: 响应数据

        Raises:
            BusinessError: 业务错误
        \"\"\"
        code = response_data.get("code")
        if code != 200:
            message = response_data.get("message", "未知错误")
            raise BusinessError(f"[{{code}}] {{message}}")


__all__ = ["{ApiName}API"]
"""

__all__ = ["GEN_API_CLIENT_TEMPLATE"]
