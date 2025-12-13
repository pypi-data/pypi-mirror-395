"""GraphQL 客户端实现"""

from __future__ import annotations

import json
from typing import Any

import httpx
from loguru import logger

from df_test_framework.capabilities.clients.graphql.models import (
    GraphQLError,
    GraphQLRequest,
    GraphQLResponse,
)

# 敏感字段名称（用于日志过滤）
SENSITIVE_KEYS = frozenset(
    {
        "password",
        "token",
        "secret",
        "api_key",
        "apikey",
        "access_token",
        "refresh_token",
        "authorization",
        "credential",
        "private_key",
    }
)


class GraphQLClient:
    """GraphQL 客户端

    支持标准 GraphQL 协议的 HTTP 传输

    Examples:
        >>> client = GraphQLClient("https://api.github.com/graphql")
        >>> client.set_header("Authorization", "Bearer YOUR_TOKEN")
        >>>
        >>> # 执行查询
        >>> query = '''
        ...     query GetUser($login: String!) {
        ...         user(login: $login) {
        ...             id
        ...             name
        ...             email
        ...         }
        ...     }
        ... '''
        >>> response = client.execute(query, {"login": "octocat"})
        >>> print(response.data)
        >>>
        >>> # 执行变更
        >>> mutation = '''
        ...     mutation CreateIssue($input: CreateIssueInput!) {
        ...         createIssue(input: $input) {
        ...             issue {
        ...                 id
        ...                 title
        ...             }
        ...         }
        ...     }
        ... '''
        >>> response = client.execute(mutation, {"input": {...}})
    """

    def __init__(
        self,
        url: str,
        headers: dict[str, str] | None = None,
        timeout: int = 30,
        verify_ssl: bool = True,
    ) -> None:
        """初始化 GraphQL 客户端

        Args:
            url: GraphQL 端点 URL
            headers: 默认请求头
            timeout: 请求超时时间（秒）
            verify_ssl: 是否验证 SSL 证书
        """
        self.url = url
        self.headers = headers or {}
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        # 设置默认 Content-Type
        if "Content-Type" not in self.headers:
            self.headers["Content-Type"] = "application/json"

        self._client = httpx.Client(
            timeout=timeout,
            verify=verify_ssl,
            headers=self.headers,
        )

    def set_header(self, key: str, value: str) -> None:
        """设置请求头

        Args:
            key: 请求头名称
            value: 请求头值
        """
        self.headers[key] = value
        self._client.headers[key] = value

    def remove_header(self, key: str) -> None:
        """移除请求头

        Args:
            key: 请求头名称
        """
        self.headers.pop(key, None)
        self._client.headers.pop(key, None)

    def _sanitize_variables(self, variables: dict[str, Any] | None) -> dict[str, Any] | None:
        """过滤变量中的敏感信息（用于日志输出）

        Args:
            variables: 原始变量字典

        Returns:
            过滤后的变量字典（敏感值被替换为 "***"）
        """
        if not variables:
            return variables

        def _sanitize_value(key: str, value: Any) -> Any:
            """递归过滤敏感值"""
            if key.lower() in SENSITIVE_KEYS:
                return "***"
            if isinstance(value, dict):
                return {k: _sanitize_value(k, v) for k, v in value.items()}
            if isinstance(value, list):
                return [_sanitize_value(key, item) for item in value]
            return value

        return {k: _sanitize_value(k, v) for k, v in variables.items()}

    def _parse_response(self, http_response: httpx.Response, operation: str) -> GraphQLResponse:
        """统一处理 HTTP 响应并解析为 GraphQL 响应

        Args:
            http_response: HTTP 响应对象
            operation: 操作描述（用于日志）

        Returns:
            GraphQL 响应对象

        Raises:
            json.JSONDecodeError: JSON 解析失败
        """
        try:
            response_data = http_response.json()
        except json.JSONDecodeError as e:
            logger.error(f"{operation} response JSON parse failed: {e}")
            # 返回包含错误信息的响应
            return GraphQLResponse(
                data=None,
                errors=[
                    GraphQLError(
                        message=f"Invalid JSON response: {e}",
                        extensions={"raw_response": http_response.text[:500]},
                    )
                ],
            )

        response = GraphQLResponse(**response_data)

        if not response.is_success:
            logger.warning(f"{operation} errors: {response.errors}")

        return response

    def execute(
        self,
        query: str,
        variables: dict[str, Any] | None = None,
        operation_name: str | None = None,
    ) -> GraphQLResponse:
        """执行 GraphQL 操作

        Args:
            query: GraphQL 查询/变更/订阅语句
            variables: 变量字典
            operation_name: 操作名称（可选）

        Returns:
            GraphQL 响应对象

        Raises:
            httpx.HTTPError: HTTP 请求失败
        """
        request = GraphQLRequest(
            query=query,
            variables=variables,
            operation_name=operation_name,
        )

        logger.debug(f"GraphQL Request: {request.query[:100]}...")
        if variables:
            # 过滤敏感信息后再记录日志
            logger.debug(f"Variables: {self._sanitize_variables(variables)}")

        try:
            http_response = self._client.post(
                self.url,
                json=request.model_dump(exclude_none=True),
            )
            http_response.raise_for_status()

            return self._parse_response(http_response, "GraphQL execute")

        except httpx.HTTPError as e:
            logger.error(f"HTTP request failed: {e}")
            raise

    def execute_batch(
        self,
        operations: list[tuple[str, dict[str, Any] | None]],
    ) -> list[GraphQLResponse]:
        """批量执行 GraphQL 操作

        Args:
            operations: 操作列表，每个元素为 (query, variables) 元组

        Returns:
            响应列表

        Raises:
            httpx.HTTPError: HTTP 请求失败
        """
        batch_request = [
            GraphQLRequest(query=query, variables=variables).model_dump(exclude_none=True)
            for query, variables in operations
        ]

        logger.debug(f"GraphQL Batch Request: {len(batch_request)} operations")

        try:
            http_response = self._client.post(
                self.url,
                json=batch_request,
            )
            http_response.raise_for_status()

            try:
                response_data = http_response.json()
            except json.JSONDecodeError as e:
                logger.error(f"Batch response JSON parse failed: {e}")
                # 返回包含错误信息的单个响应
                return [
                    GraphQLResponse(
                        data=None,
                        errors=[
                            GraphQLError(
                                message=f"Invalid JSON response: {e}",
                                extensions={"raw_response": http_response.text[:500]},
                            )
                        ],
                    )
                ]

            responses = [GraphQLResponse(**data) for data in response_data]
            return responses

        except httpx.HTTPError as e:
            logger.error(f"HTTP batch request failed: {e}")
            raise

    def upload_file(
        self,
        query: str,
        variables: dict[str, Any],
        files: dict[str, tuple[str, bytes, str]],
    ) -> GraphQLResponse:
        """上传文件（multipart/form-data）

        Args:
            query: GraphQL 变更语句
            variables: 变量字典
            files: 文件字典，格式为 {变量名: (文件名, 文件内容, MIME类型)}

        Returns:
            GraphQL 响应对象

        Raises:
            httpx.HTTPError: HTTP 请求失败
        """
        operations = {
            "query": query,
            "variables": variables,
        }

        # 构建 map 字段（文件映射）
        file_map = {}
        for idx, var_name in enumerate(files.keys()):
            file_map[str(idx)] = [f"variables.{var_name}"]

        # 构建 multipart 数据
        multipart_data = {
            "operations": (None, json.dumps(operations), "application/json"),
            "map": (None, json.dumps(file_map), "application/json"),
        }

        # 添加文件
        for idx, (var_name, (filename, content, mime_type)) in enumerate(files.items()):
            multipart_data[str(idx)] = (filename, content, mime_type)

        logger.debug(f"GraphQL File Upload: {query[:100]}...")
        if variables:
            logger.debug(f"Variables: {self._sanitize_variables(variables)}")

        try:
            # 使用局部 headers 副本，避免并发场景下的竞态条件
            # 移除 Content-Type，让 httpx 自动设置 multipart/form-data
            request_headers = {k: v for k, v in self.headers.items() if k != "Content-Type"}

            http_response = self._client.post(
                self.url,
                files=multipart_data,  # type: ignore
                headers=request_headers,
            )
            http_response.raise_for_status()

            return self._parse_response(http_response, "File upload")

        except httpx.HTTPError as e:
            logger.error(f"File upload failed: {e}")
            raise

    def close(self) -> None:
        """关闭客户端，释放资源"""
        self._client.close()
        logger.debug("GraphQL client closed")

    def __enter__(self) -> GraphQLClient:
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        """上下文管理器退出"""
        self.close()
