"""OpenAPI/Swagger 规范解析器

解析 OpenAPI 3.0/Swagger 2.0 规范文件，提取 API 信息用于代码生成。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import prance
    import yaml

    OPENAPI_AVAILABLE = True
except ImportError:
    OPENAPI_AVAILABLE = False
    prance = None
    yaml = None


class OpenAPIParser:
    """OpenAPI 规范解析器

    支持 OpenAPI 3.0 和 Swagger 2.0 格式。

    Example:
        >>> parser = OpenAPIParser("swagger.json")
        >>> endpoints = parser.get_endpoints()
        >>> for endpoint in endpoints:
        ...     print(endpoint.path, endpoint.method)
    """

    def __init__(self, spec_path: str | Path):
        """初始化解析器

        Args:
            spec_path: OpenAPI 规范文件路径（JSON 或 YAML）
                      或 URL（如: https://api.example.com/swagger.json）
        """
        if not OPENAPI_AVAILABLE:
            raise ImportError(
                "OpenAPI 功能需要安装 prance 和 pyyaml 库\n请运行: pip install 'prance[osv]' pyyaml"
            )

        self.spec_path = spec_path
        self.spec: dict[str, Any] = {}
        self._load_spec()

    def _load_spec(self) -> None:
        """加载 OpenAPI 规范文件"""
        # 检查是否为 URL
        if isinstance(self.spec_path, str) and self.spec_path.startswith(("http://", "https://")):
            # 从 URL 加载
            parser = prance.ResolvingParser(self.spec_path, lazy=True)
            parser.parse()
            self.spec = parser.specification
        else:
            # 从本地文件加载
            spec_file = Path(self.spec_path)
            if not spec_file.exists():
                raise FileNotFoundError(f"OpenAPI 规范文件不存在: {spec_file}")

            # 解析文件
            parser = prance.ResolvingParser(str(spec_file), lazy=True)
            parser.parse()
            self.spec = parser.specification

    def get_info(self) -> dict[str, Any]:
        """获取 API 基本信息

        Returns:
            包含 title, version, description 等信息的字典
        """
        return self.spec.get("info", {})

    def get_base_url(self) -> str:
        """获取 API 基础 URL

        Returns:
            基础 URL 字符串
        """
        # OpenAPI 3.0
        if "servers" in self.spec and self.spec["servers"]:
            return self.spec["servers"][0].get("url", "")

        # Swagger 2.0
        if "host" in self.spec:
            scheme = self.spec.get("schemes", ["http"])[0]
            base_path = self.spec.get("basePath", "")
            return f"{scheme}://{self.spec['host']}{base_path}"

        return ""

    def get_endpoints(self, tags: list[str] | None = None) -> list[APIEndpoint]:
        """获取所有 API 端点

        Args:
            tags: 过滤的标签列表，None 表示获取所有端点

        Returns:
            APIEndpoint 对象列表
        """
        endpoints = []

        paths = self.spec.get("paths", {})
        for path, path_item in paths.items():
            for method, operation in path_item.items():
                # 跳过非 HTTP 方法的键（如 parameters, $ref 等）
                if method not in ["get", "post", "put", "delete", "patch", "head", "options"]:
                    continue

                # 标签过滤
                operation_tags = operation.get("tags", [])
                if tags and not any(tag in operation_tags for tag in tags):
                    continue

                endpoint = APIEndpoint(
                    path=path,
                    method=method.upper(),
                    operation_id=operation.get("operationId", ""),
                    summary=operation.get("summary", ""),
                    description=operation.get("description", ""),
                    tags=operation_tags,
                    parameters=self._parse_parameters(operation.get("parameters", [])),
                    request_body=self._parse_request_body(operation.get("requestBody")),
                    responses=self._parse_responses(operation.get("responses", {})),
                )

                endpoints.append(endpoint)

        return endpoints

    def _parse_parameters(self, parameters: list[dict]) -> list[APIParameter]:
        """解析参数列表"""
        parsed_params = []

        for param in parameters:
            # 解析 $ref 引用
            if "$ref" in param:
                param = self._resolve_ref(param["$ref"])

            param_obj = APIParameter(
                name=param.get("name", ""),
                location=param.get("in", ""),  # query, path, header, cookie
                required=param.get("required", False),
                schema=param.get("schema", {}),
                description=param.get("description", ""),
            )
            parsed_params.append(param_obj)

        return parsed_params

    def _parse_request_body(self, request_body: dict | None) -> dict | None:
        """解析请求体"""
        if not request_body:
            return None

        # 解析 $ref 引用
        if "$ref" in request_body:
            request_body = self._resolve_ref(request_body["$ref"])

        content = request_body.get("content", {})
        if "application/json" in content:
            return {
                "content_type": "application/json",
                "schema": content["application/json"].get("schema", {}),
                "required": request_body.get("required", False),
            }

        return None

    def _parse_responses(self, responses: dict) -> dict[str, dict]:
        """解析响应定义"""
        parsed_responses = {}

        for status_code, response in responses.items():
            # 解析 $ref 引用
            if "$ref" in response:
                response = self._resolve_ref(response["$ref"])

            content = response.get("content", {})
            if "application/json" in content:
                parsed_responses[status_code] = {
                    "description": response.get("description", ""),
                    "schema": content["application/json"].get("schema", {}),
                }

        return parsed_responses

    def _resolve_ref(self, ref: str) -> dict:
        """解析 $ref 引用

        Args:
            ref: 引用路径，如 "#/components/schemas/User"

        Returns:
            解析后的对象
        """
        # 移除开头的 #/
        ref_path = ref.lstrip("#/")
        parts = ref_path.split("/")

        # 逐层访问
        obj = self.spec
        for part in parts:
            obj = obj.get(part, {})

        return obj

    def get_schemas(self) -> dict[str, dict]:
        """获取所有数据模型定义

        Returns:
            模型名称到模型定义的映射
        """
        # OpenAPI 3.0
        if "components" in self.spec:
            return self.spec["components"].get("schemas", {})

        # Swagger 2.0
        if "definitions" in self.spec:
            return self.spec["definitions"]

        return {}

    def get_tags(self) -> list[str]:
        """获取所有标签

        Returns:
            标签名称列表
        """
        tags = self.spec.get("tags", [])
        return [tag.get("name", "") for tag in tags if "name" in tag]


class APIEndpoint:
    """API 端点信息"""

    def __init__(
        self,
        path: str,
        method: str,
        operation_id: str = "",
        summary: str = "",
        description: str = "",
        tags: list[str] | None = None,
        parameters: list[APIParameter] | None = None,
        request_body: dict | None = None,
        responses: dict | None = None,
    ):
        self.path = path
        self.method = method
        self.operation_id = operation_id
        self.summary = summary
        self.description = description
        self.tags = tags or []
        self.parameters = parameters or []
        self.request_body = request_body
        self.responses = responses or {}

    def get_path_params(self) -> list[APIParameter]:
        """获取路径参数"""
        return [p for p in self.parameters if p.location == "path"]

    def get_query_params(self) -> list[APIParameter]:
        """获取查询参数"""
        return [p for p in self.parameters if p.location == "query"]

    def get_success_response(self) -> dict | None:
        """获取成功响应（200/201）"""
        for code in ["200", "201"]:
            if code in self.responses:
                return self.responses[code]
        return None

    def __repr__(self) -> str:
        return f"<APIEndpoint {self.method} {self.path}>"


class APIParameter:
    """API 参数信息"""

    def __init__(
        self,
        name: str,
        location: str,
        required: bool = False,
        schema: dict | None = None,
        description: str = "",
    ):
        self.name = name
        self.location = location  # query, path, header, cookie
        self.required = required
        self.schema = schema or {}
        self.description = description

    def get_type(self) -> str:
        """获取参数类型"""
        return self.schema.get("type", "string")

    def __repr__(self) -> str:
        return f"<APIParameter {self.name} ({self.location})>"


__all__ = ["OpenAPIParser", "APIEndpoint", "APIParameter", "OPENAPI_AVAILABLE"]
