"""API基类模板"""

BASE_API_TEMPLATE = """\"\"\"API基类

提供统一的API调用接口和业务错误处理。
\"\"\"

from df_test_framework import BaseAPI, HttpClient
from df_test_framework.capabilities.clients.http.rest.httpx import BusinessError


class {ProjectName}BaseAPI(BaseAPI):
    \"\"\"项目API基类

    继承框架的BaseAPI，添加项目特定的业务错误检查。

    特性:
    - 自动检查业务错误（code != 200）
    - 自动HTTP重试
    - 统一错误处理
    \"\"\"

    def __init__(self, http_client: HttpClient):
        super().__init__(http_client)

    def _check_business_error(self, response_data: dict) -> None:
        \"\"\"检查业务错误

        Args:
            response_data: 响应数据字典

        Raises:
            BusinessError: 业务错误（code != 200）
        \"\"\"
        code = response_data.get("code")
        if code != 200:
            message = response_data.get("message", "未知错误")
            raise BusinessError(f"[{{code}}] {{message}}")


__all__ = ["{ProjectName}BaseAPI"]
"""

__all__ = ["BASE_API_TEMPLATE"]
