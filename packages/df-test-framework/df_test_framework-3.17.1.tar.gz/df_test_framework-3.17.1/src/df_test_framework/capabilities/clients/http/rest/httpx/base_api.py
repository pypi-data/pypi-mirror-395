"""API基类

v3.3.0 重构:
- 简化为只提供HTTP方法封装和响应解析
- 拦截器功能移至HttpClient统一管理
- 不再支持BaseAPI层级的拦截器（请使用HttpClient的配置化拦截器系统）

详见: docs/INTERCEPTOR_ARCHITECTURE.md
"""

from typing import Any, TypeVar

import httpx
from loguru import logger
from pydantic import BaseModel, ValidationError

from .client import HttpClient

T = TypeVar("T", bound=BaseModel)


# ========== 业务异常 ==========


class BusinessError(Exception):
    """业务错误异常

    当API返回的业务状态码表示失败时抛出此异常

    Attributes:
        message: 错误消息
        code: 业务错误码
        data: 原始响应数据
    """

    def __init__(
        self, message: str, code: int | str | None = None, data: dict[str, Any] | None = None
    ):
        self.message = message
        self.code = code
        self.data = data
        super().__init__(message)

    def __str__(self) -> str:
        if self.code:
            return f"[业务错误 {self.code}] {self.message}"
        return f"[业务错误] {self.message}"


class BaseAPI:
    """
    API基类

    职责:
    - 管理HttpClient
    - 提供便捷的get/post/put/delete方法
    - 解析响应为Pydantic模型
    - 处理业务错误

    v3.3.0 简化:
    - ❌ 移除拦截器管理（请使用HttpClient的配置化拦截器系统）
    - ✅ 专注于API封装和响应解析

    使用拦截器的推荐方式:
        # 在HTTPConfig中配置拦截器（全局生效）
        >>> settings = FrameworkSettings(
        ...     http=HTTPConfig(
        ...         interceptors=[
        ...             SignatureInterceptorConfig(type="signature", ...),
        ...             BearerTokenInterceptorConfig(type="bearer_token", ...)
        ...         ]
        ...     )
        ... )
        >>> client = HttpClient(base_url="...", config=settings.http)
        >>> api = MyAPI(client)

        # 或者编程式添加拦截器
        >>> client = HttpClient(base_url="...")
        >>> client.request_interceptors.append(
        ...     InterceptorFactory.create(SignatureInterceptorConfig(...))
        ... )
    """

    def __init__(self, http_client: HttpClient):
        """
        初始化API基类

        Args:
            http_client: HTTP客户端实例
        """
        self.http_client = http_client

    def _check_business_error(self, response_data: dict[str, Any]) -> None:
        """
        检查业务错误 (可在子类中重写)

        默认实现不检查业务错误,适用于没有统一响应格式的项目
        子类可以根据自己的业务响应格式重写此方法

        常见实现示例:

        # 示例1: 检查 success 字段
        def _check_business_error(self, response_data):
            if not response_data.get("success", True):
                raise BusinessError(
                    message=response_data.get("message", "未知错误"),
                    code=response_data.get("code"),
                    data=response_data
                )

        # 示例2: 检查 code 字段
        def _check_business_error(self, response_data):
            code = response_data.get("code", 200)
            if code not in [200, 0]:  # 假设200和0表示成功
                raise BusinessError(
                    message=response_data.get("message", "未知错误"),
                    code=code,
                    data=response_data
                )

        Args:
            response_data: 响应数据字典

        Raises:
            BusinessError: 业务错误
        """
        pass  # 默认不检查,由子类决定是否实现

    def _parse_response(
        self,
        response: httpx.Response,
        model: type[T] | None = None,
        raise_for_status: bool = True,
        check_business_error: bool = True,
    ) -> T | dict[str, Any]:
        """
        解析响应数据

        Args:
            response: HTTP响应对象
            model: Pydantic模型类,如果提供则解析为模型实例
            raise_for_status: 是否在HTTP错误时抛出异常
            check_business_error: 是否检查业务错误 (调用_check_business_error方法)

        Returns:
            解析后的数据 (Pydantic模型实例或字典)

        Raises:
            httpx.HTTPStatusError: 当HTTP状态码表示错误且raise_for_status=True时
            BusinessError: 当业务状态码表示错误且check_business_error=True时
            ValidationError: 当响应数据验证失败时
        """
        # 检查HTTP状态码
        if raise_for_status:
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP错误: {e.response.status_code} - {e.response.text}")
                raise

        # 解析JSON响应
        try:
            response_data = response.json()
        except Exception as e:
            logger.error(f"解析JSON失败: {str(e)}, 响应内容: {response.text}")
            raise

        # 检查业务错误
        if check_business_error:
            try:
                self._check_business_error(response_data)
            except BusinessError as e:
                logger.error(f"业务错误: {e}")
                logger.debug(f"响应数据: {response_data}")
                raise

        # 如果提供了模型,则解析为模型实例
        if model:
            try:
                return model.model_validate(response_data)
            except ValidationError as e:
                logger.error(f"响应数据验证失败: {e.error_count()} 个错误")
                logger.debug(f"验证错误详情: {e.errors()}")
                logger.debug(f"原始响应数据: {response_data}")
                raise
            except Exception as e:
                logger.error(f"解析响应模型失败: {str(e)}")
                logger.debug(f"响应数据: {response_data}")
                raise

        return response_data

    def _build_url(self, endpoint: str) -> str:
        """
        构建完整URL

        Args:
            endpoint: API端点路径

        Returns:
            完整的URL
        """
        # 移除endpoint开头的斜杠(如果有)
        endpoint = endpoint.lstrip("/")
        return endpoint

    def get(
        self,
        endpoint: str,
        model: type[T] | None = None,
        **kwargs,
    ) -> T | dict[str, Any]:
        """
        发送GET请求

        Args:
            endpoint: API端点
            model: 响应模型类
            **kwargs: 其他请求参数
                - params: 查询参数（支持 dict 或 Pydantic 模型）

        Returns:
            解析后的响应数据

        Note:
            如果 params 参数是 Pydantic BaseModel 实例，会自动序列化为字典。
            序列化时会使用 by_alias=True（使用字段别名）和 exclude_none=True（排除 None 值）。

            示例:
                >>> class QueryRequest(BaseModel):
                ...     user_id: str = Field(alias="userId")
                ...     status: str | None = None
                >>>
                >>> request = QueryRequest(user_id="user_001")
                >>> api.get("/users", params=request)  # 自动转换为 {"userId": "user_001"}
        """
        # 自动处理 Pydantic 模型序列化为查询参数
        if "params" in kwargs and isinstance(kwargs["params"], BaseModel):
            kwargs["params"] = kwargs["params"].model_dump(
                mode="json", by_alias=True, exclude_none=True
            )

        url = self._build_url(endpoint)
        response = self.http_client.get(url, **kwargs)
        return self._parse_response(response, model)

    def post(
        self,
        endpoint: str,
        model: type[T] | None = None,
        **kwargs,
    ) -> T | dict[str, Any]:
        """
        发送POST请求

        Args:
            endpoint: API端点
            model: 响应模型类
            **kwargs: 其他请求参数

        Returns:
            解析后的响应数据

        Note:
            如果 json 参数是 Pydantic BaseModel 实例，会自动序列化为字典
        """
        # 自动处理 Pydantic 模型序列化
        if "json" in kwargs and isinstance(kwargs["json"], BaseModel):
            kwargs["json"] = kwargs["json"].model_dump(mode="json", by_alias=True)

        url = self._build_url(endpoint)
        response = self.http_client.post(url, **kwargs)
        return self._parse_response(response, model)

    def put(
        self,
        endpoint: str,
        model: type[T] | None = None,
        **kwargs,
    ) -> T | dict[str, Any]:
        """
        发送PUT请求

        Args:
            endpoint: API端点
            model: 响应模型类
            **kwargs: 其他请求参数

        Returns:
            解析后的响应数据

        Note:
            如果 json 参数是 Pydantic BaseModel 实例，会自动序列化为字典
        """
        # 自动处理 Pydantic 模型序列化
        if "json" in kwargs and isinstance(kwargs["json"], BaseModel):
            kwargs["json"] = kwargs["json"].model_dump(mode="json", by_alias=True)

        url = self._build_url(endpoint)
        response = self.http_client.put(url, **kwargs)
        return self._parse_response(response, model)

    def delete(
        self,
        endpoint: str,
        model: type[T] | None = None,
        **kwargs,
    ) -> T | dict[str, Any]:
        """
        发送DELETE请求

        Args:
            endpoint: API端点
            model: 响应模型类
            **kwargs: 其他请求参数

        Returns:
            解析后的响应数据
        """
        url = self._build_url(endpoint)
        response = self.http_client.delete(url, **kwargs)
        return self._parse_response(response, model)

    def patch(
        self,
        endpoint: str,
        model: type[T] | None = None,
        **kwargs,
    ) -> T | dict[str, Any]:
        """
        发送PATCH请求

        Args:
            endpoint: API端点
            model: 响应模型类
            **kwargs: 其他请求参数

        Returns:
            解析后的响应数据

        Note:
            如果 json 参数是 Pydantic BaseModel 实例，会自动序列化为字典
        """
        # 自动处理 Pydantic 模型序列化
        if "json" in kwargs and isinstance(kwargs["json"], BaseModel):
            kwargs["json"] = kwargs["json"].model_dump(mode="json", by_alias=True)

        url = self._build_url(endpoint)
        response = self.http_client.patch(url, **kwargs)
        return self._parse_response(response, model)


__all__ = [
    "BaseAPI",
    "BusinessError",
]
