"""从 OpenAPI/Swagger 规范生成测试代码

基于 OpenAPI 规范自动生成测试用例、API 客户端和 Pydantic 模型。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..utils import (
    create_file,
    detect_project_name,
    to_pascal_case,
    to_snake_case,
)
from .openapi_parser import OPENAPI_AVAILABLE, OpenAPIParser


def generate_from_openapi(
    spec_path: str | Path,
    *,
    output_dir: Path | None = None,
    generate_tests: bool = True,
    generate_clients: bool = True,
    generate_models: bool = True,
    tags: list[str] | None = None,
    force: bool = False,
) -> None:
    """从 OpenAPI 规范生成测试代码

    Args:
        spec_path: OpenAPI 规范文件路径或 URL
        output_dir: 输出目录（默认: 当前目录）
        generate_tests: 是否生成测试用例
        generate_clients: 是否生成 API 客户端
        generate_models: 是否生成 Pydantic 模型
        tags: 过滤的标签列表（None 表示生成所有）
        force: 是否强制覆盖

    Example:
        >>> generate_from_openapi(
        ...     "https://api.example.com/swagger.json",
        ...     generate_tests=True,
        ...     generate_clients=True,
        ...     generate_models=True
        ... )
    """
    if not OPENAPI_AVAILABLE:
        print("❌ 错误: OpenAPI 功能需要安装 prance 和 pyyaml 库")
        print("   请运行: pip install 'prance[osv]' pyyaml")
        return

    # 检测项目名称
    project_name = detect_project_name()
    if not project_name:
        print("⚠️  错误: 无法检测项目名称，请在项目根目录下运行")
        return

    if output_dir is None:
        output_dir = Path.cwd()

    # 解析 OpenAPI 规范
    print(f"\n📝 解析 OpenAPI 规范: {spec_path}")
    try:
        parser = OpenAPIParser(spec_path)
    except Exception as e:
        print(f"❌ 解析失败: {e}")
        return

    # 获取 API 信息
    info = parser.get_info()
    print(f"📋 API: {info.get('title', 'Unknown')} v{info.get('version', '1.0.0')}")

    # 获取端点列表
    endpoints = parser.get_endpoints(tags=tags)
    print(f"📊 找到 {len(endpoints)} 个 API 端点")

    if not endpoints:
        print("⚠️  没有找到符合条件的 API 端点")
        return

    # 生成统计
    generated_files = []

    # 生成模型
    if generate_models:
        print("\n📝 生成 Pydantic 模型...")
        model_files = _generate_models(parser, project_name, output_dir, force)
        generated_files.extend(model_files)

    # 生成 API 客户端
    if generate_clients:
        print("\n📝 生成 API 客户端...")
        client_files = _generate_api_clients(endpoints, project_name, output_dir, force)
        generated_files.extend(client_files)

    # 生成测试用例
    if generate_tests:
        print("\n📝 生成测试用例...")
        test_files = _generate_tests(endpoints, project_name, output_dir, force)
        generated_files.extend(test_files)

    # 输出结果
    print("\n✅ 生成完成！")
    print(f"\n📁 共生成 {len(generated_files)} 个文件:")
    for file_type, file_path in generated_files:
        print(f"  ✓ {file_type:<20} {file_path}")

    print("\n💡 下一步:")
    print("  1. 查看生成的文件并根据需要调整")
    print("  2. 运行测试: pytest tests/ -v")
    print("  3. 查看 Allure 报告: allure serve reports/allure-results")


def _generate_models(
    parser: OpenAPIParser, project_name: str, output_dir: Path, force: bool
) -> list[tuple[str, Path]]:
    """生成 Pydantic 模型"""
    generated: list[tuple[str, Path]] = []
    schemas = parser.get_schemas()

    if not schemas:
        return generated

    models_dir = output_dir / "src" / project_name / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    for schema_name, schema_def in schemas.items():
        model_name = to_pascal_case(schema_name)
        file_name = to_snake_case(schema_name) + ".py"
        file_path = models_dir / file_name

        # 生成模型代码
        content = _build_model_code(model_name, schema_def)

        try:
            create_file(file_path, content, force=force)
            generated.append(("Model", file_path.relative_to(output_dir)))
        except FileExistsError:
            print(f"⚠️  模型文件已存在（跳过）: {file_path.name}")

    return generated


def _build_model_code(model_name: str, schema: dict) -> str:
    """构建 Pydantic 模型代码"""
    properties = schema.get("properties", {})
    required = schema.get("required", [])

    # 导入语句
    imports = ["from pydantic import BaseModel, Field"]
    if any(prop.get("type") == "array" for prop in properties.values()):
        imports[0] += ", List"

    # 字段定义
    fields = []
    for field_name, field_schema in properties.items():
        field_type = _get_python_type(field_schema)
        is_required = field_name in required
        description = field_schema.get("description", f"{field_name}字段")

        if is_required:
            fields.append(
                f'    {field_name}: {field_type} = Field(..., description="{description}")'
            )
        else:
            fields.append(
                f'    {field_name}: {field_type} | None = Field(None, description="{description}")'
            )

    code = f'''"""自动生成的 Pydantic 模型

从 OpenAPI 规范生成
"""

{imports[0]}


class {model_name}(BaseModel):
    """{model_name}模型"""

{chr(10).join(fields) if fields else "    pass"}
'''

    return code


def _get_python_type(schema: dict) -> str:
    """将 OpenAPI 类型转换为 Python 类型"""
    schema_type = schema.get("type", "string")

    type_mapping = {
        "string": "str",
        "integer": "int",
        "number": "float",
        "boolean": "bool",
        "array": "List[Any]",
        "object": "dict",
    }

    # 处理数组类型
    if schema_type == "array" and "items" in schema:
        item_type = _get_python_type(schema["items"])
        return f"List[{item_type}]"

    return type_mapping.get(schema_type, "Any")


def _generate_api_clients(
    endpoints: list, project_name: str, output_dir: Path, force: bool
) -> list[tuple[str, Path]]:
    """生成 API 客户端"""
    generated: list[tuple[str, Path]] = []

    # 按标签分组
    endpoints_by_tag: dict[str, list[Any]] = {}
    for endpoint in endpoints:
        tag = endpoint.tags[0] if endpoint.tags else "default"
        if tag not in endpoints_by_tag:
            endpoints_by_tag[tag] = []
        endpoints_by_tag[tag].append(endpoint)

    apis_dir = output_dir / "src" / project_name / "apis"
    apis_dir.mkdir(parents=True, exist_ok=True)

    # 为每个标签生成一个客户端
    for tag, tag_endpoints in endpoints_by_tag.items():
        client_name = to_snake_case(tag)
        file_name = f"{client_name}_api.py"
        file_path = apis_dir / file_name

        # 生成客户端代码
        content = _build_client_code(tag, tag_endpoints)

        try:
            create_file(file_path, content, force=force)
            generated.append(("API Client", file_path.relative_to(output_dir)))
        except FileExistsError:
            print(f"⚠️  客户端文件已存在（跳过）: {file_path.name}")

    return generated


def _build_client_code(tag: str, endpoints: list) -> str:
    """构建 API 客户端代码"""
    class_name = to_pascal_case(tag) + "API"

    # 生成方法
    methods = []
    for endpoint in endpoints:
        method_name = _endpoint_to_method_name(endpoint)
        method_code = _build_method_code(endpoint, method_name)
        methods.append(method_code)

    code = f'''"""自动生成的 API 客户端

从 OpenAPI 规范生成
"""

from df_test_framework import BaseAPI


class {class_name}(BaseAPI):
    """{tag} API 客户端

    自动从 OpenAPI 规范生成
    """

{chr(10).join(methods)}
'''

    return code


def _endpoint_to_method_name(endpoint) -> str:
    """将端点转换为方法名"""
    if endpoint.operation_id:
        return to_snake_case(endpoint.operation_id)

    # 从路径和方法生成
    path_parts = [p for p in endpoint.path.split("/") if p and not p.startswith("{")]
    method = endpoint.method.lower()

    if method == "get":
        return "get_" + "_".join(path_parts)
    elif method == "post":
        return "create_" + "_".join(path_parts)
    elif method == "put":
        return "update_" + "_".join(path_parts)
    elif method == "delete":
        return "delete_" + "_".join(path_parts)
    else:
        return method + "_" + "_".join(path_parts)


def _build_method_code(endpoint, method_name: str) -> str:
    """构建方法代码"""
    # 路径参数
    path_params = endpoint.get_path_params()
    query_params = endpoint.get_query_params()

    # 方法参数
    params = []
    if path_params:
        params.extend([f"{p.name}: {_get_python_type(p.schema)}" for p in path_params])
    if endpoint.request_body:
        params.append("data: dict")
    if query_params:
        params.append("**kwargs")

    params_str = ", ".join(params)

    # 构建路径
    path = endpoint.path
    for param in path_params:
        path = path.replace(f"{{{param.name}}}", "{param.name}")

    # HTTP 方法
    http_method = endpoint.method.lower()

    # 生成代码
    doc = f'"""{endpoint.summary or method_name}"""'

    if endpoint.request_body:
        body_arg = ", json=data"
    else:
        body_arg = ""

    code = f'''    def {method_name}(self, {params_str}):
        {doc}
        return self.{http_method}(f"{path}"{body_arg})
'''

    return code


def _generate_tests(
    endpoints: list, project_name: str, output_dir: Path, force: bool
) -> list[tuple[str, Path]]:
    """生成测试用例"""
    generated: list[tuple[str, Path]] = []

    # 按标签分组
    endpoints_by_tag: dict[str, list[Any]] = {}
    for endpoint in endpoints:
        tag = endpoint.tags[0] if endpoint.tags else "default"
        if tag not in endpoints_by_tag:
            endpoints_by_tag[tag] = []
        endpoints_by_tag[tag].append(endpoint)

    tests_dir = output_dir / "tests" / "api"
    tests_dir.mkdir(parents=True, exist_ok=True)

    # 为每个标签生成一个测试文件
    for tag, tag_endpoints in endpoints_by_tag.items():
        test_name = to_snake_case(tag)
        file_name = f"test_{test_name}_api.py"
        file_path = tests_dir / file_name

        # 生成测试代码
        content = _build_test_code(tag, tag_endpoints, project_name)

        try:
            create_file(file_path, content, force=force)
            generated.append(("Test", file_path.relative_to(output_dir)))
        except FileExistsError:
            print(f"⚠️  测试文件已存在（跳过）: {file_path.name}")

    return generated


def _build_test_code(tag: str, endpoints: list, project_name: str) -> str:
    """构建测试代码"""
    class_name = "Test" + to_pascal_case(tag) + "API"
    api_client_name = to_pascal_case(tag) + "API"

    # 生成测试方法
    test_methods = []
    for endpoint in endpoints:
        method_code = _build_test_method_code(endpoint)
        test_methods.append(method_code)

    code = f'''"""自动生成的测试文件

从 OpenAPI 规范生成
"""

import pytest
import allure
from assertpy import assert_that
from df_test_framework.testing.plugins import attach_json, step
from {project_name}.apis import {api_client_name}


@allure.feature("{tag}")
class {class_name}:
    """API 测试类

    自动从 OpenAPI 规范生成
    """

{chr(10).join(test_methods)}
'''

    return code


def _build_test_method_code(endpoint) -> str:
    """构建测试方法代码

    ⚠️ 注意：v3.7.0+ 生成的测试使用 http_client fixture
    如需数据清理支持，请手动添加 uow fixture 和数据清理逻辑
    """
    method_name = _endpoint_to_method_name(endpoint)
    test_name = f"test_{method_name}"

    doc = f'"""{endpoint.summary or method_name}"""'

    # 构建测试代码（v3.7.0+：建议同时使用 http_client 和 uow）
    code = f'''    @allure.title("{endpoint.summary or method_name}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def {test_name}(self, http_client, uow):
        {doc}
        with step("准备测试数据"):
            # TODO: 如需创建测试数据，使用 uow 的 Repository
            # user_repo = uow.repository(UserRepository)
            # test_user_id = user_repo.create({{"name": "test_user"}})
            # uow.commit()
            pass

        with step("调用API"):
            response = http_client.{endpoint.method.lower()}("{endpoint.path}")
            assert_that(response.status_code).is_equal_to(200)

        with step("验证响应"):
            data = response.json()
            attach_json(data, name="响应数据")
            # TODO: 添加具体的断言
            assert_that(data).is_not_none()

        # ✅ 测试结束后，uow 会自动回滚所有数据
'''

    return code


__all__ = ["generate_from_openapi"]
