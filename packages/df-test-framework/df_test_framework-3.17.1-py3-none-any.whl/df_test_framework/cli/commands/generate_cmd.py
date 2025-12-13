"""generate命令实现

生成测试代码文件。
"""

from __future__ import annotations

import json
from pathlib import Path

from ..generators import generate_pydantic_model_from_json
from ..templates import (
    ENV_BASE_TEMPLATE,
    ENV_DEV_TEMPLATE,
    ENV_EXAMPLE_TEMPLATE,
    ENV_PROD_TEMPLATE,
    ENV_TEST_TEMPLATE,
    GEN_API_CLIENT_TEMPLATE,
    GEN_BUILDER_TEMPLATE,
    GEN_REPOSITORY_TEMPLATE,
    GEN_TEST_COMPLETE_TEMPLATE,
    GEN_TEST_TEMPLATE,
    SETTINGS_ENHANCED_TEMPLATE,
)
from ..utils import (
    create_file,
    detect_project_name,
    replace_template_vars,
    to_pascal_case,
    to_snake_case,
)


def safe_relative_path(path: Path, base: Path = None) -> Path:
    """安全地计算相对路径，如果失败则返回绝对路径

    Args:
        path: 目标路径
        base: 基准路径（默认为当前工作目录）

    Returns:
        Path: 相对路径或绝对路径
    """
    if base is None:
        base = Path.cwd()

    try:
        # 转换为绝对路径后再计算相对路径
        abs_path = path.resolve()
        abs_base = base.resolve()
        return abs_path.relative_to(abs_base)
    except (ValueError, TypeError):
        # 如果计算失败，返回绝对路径
        return path.resolve()


def generate_test(
    name: str,
    *,
    feature: str = None,
    story: str = None,
    output_dir: Path = None,
    force: bool = False,
    template: str = "basic",
    api_path: str = None,
) -> None:
    """生成API测试文件

    Args:
        name: 测试名称（如: user_login）
        feature: Allure feature名称
        story: Allure story名称
        output_dir: 输出目录（默认: tests/api/）
        force: 是否强制覆盖
        template: 模板类型（basic=基础模板，complete=完整模板，默认: basic）
        api_path: API路径（如: users，默认与name相同）

    Example:
        >>> generate_test("user_login", feature="用户模块", story="登录功能")
        ✅ 测试文件生成成功！
        📁 文件路径: tests/api/test_user_login.py

        >>> generate_test("user_create", template="complete", api_path="users")
        ✅ 测试文件生成成功！（完整模板）
    """

    # 默认输出目录
    if output_dir is None:
        output_dir = Path.cwd() / "tests" / "api"

    # 名称转换
    test_name = to_snake_case(name)
    test_name_pascal = to_pascal_case(name)
    entity_name_pascal = test_name_pascal.replace("Test", "").replace("test", "")

    # 选择模板
    if template == "complete":
        template_content = GEN_TEST_COMPLETE_TEMPLATE
    else:
        template_content = GEN_TEST_TEMPLATE

    # 变量替换
    replacements = {
        "{test_name}": test_name,
        "{TestName}": test_name_pascal,
        "{EntityName}": entity_name_pascal,
        "{feature_name}": feature or test_name_pascal,
        "{story_name}": story or f"{test_name_pascal}功能",
        "{test_description}": name.replace("_", " "),
        "{method_name}": test_name,
        "{api_path}": api_path or test_name.replace("_", "/"),
    }

    content = replace_template_vars(template_content, replacements)

    # 创建文件
    file_path = output_dir / f"test_{test_name}.py"
    create_file(file_path, content, force=force)

    print("\n✅ 测试文件生成成功！")
    if template == "complete":
        print("📋 模板类型: 完整模板（包含实现示例）")
    else:
        print("📋 模板类型: 基础模板")
    print(f"📁 文件路径: {safe_relative_path(file_path)}")
    print("\n💡 下一步:")
    if template == "complete":
        print(f"  1. 根据实际API修改 {file_path.name} 中的示例代码")
        print("  2. 取消注释需要的Builder和Repository代码")
    else:
        print(f"  1. 编辑 {file_path.name} 完善测试逻辑")
    print(f"  3. 运行测试: pytest {safe_relative_path(file_path)} -v")


def generate_builder(
    name: str,
    *,
    output_dir: Path = None,
    force: bool = False,
) -> None:
    """生成Builder类

    Args:
        name: 实体名称（如: user, order）
        output_dir: 输出目录（默认: src/<project>/builders/）
        force: 是否强制覆盖

    Example:
        >>> generate_builder("user")
        ✅ Builder类生成成功！
        📁 文件路径: src/my_project/builders/user_builder.py
    """

    # 检测项目名称
    project_name = detect_project_name()
    if not project_name:
        print("⚠️  错误: 无法检测项目名称，请在项目根目录下运行")
        return

    # 默认输出目录
    if output_dir is None:
        output_dir = Path.cwd() / "src" / project_name / "builders"

    # 名称转换
    entity_name = to_snake_case(name)
    entity_name_pascal = to_pascal_case(name)

    # 变量替换
    replacements = {
        "{entity_name}": entity_name,
        "{EntityName}": entity_name_pascal,
    }

    content = replace_template_vars(GEN_BUILDER_TEMPLATE, replacements)

    # 创建文件
    file_path = output_dir / f"{entity_name}_builder.py"
    create_file(file_path, content, force=force)

    print("\n✅ Builder类生成成功！")
    print(f"📁 文件路径: {safe_relative_path(file_path)}")
    print("\n💡 使用示例:")
    print(f"  from {project_name}.builders import {entity_name_pascal}Builder")
    print(f"  data = {entity_name_pascal}Builder().with_name('test').build()")


def generate_repository(
    name: str,
    *,
    table_name: str = None,
    output_dir: Path = None,
    force: bool = False,
) -> None:
    """生成Repository类

    Args:
        name: 实体名称（如: user, order）
        table_name: 数据库表名（默认与name相同）
        output_dir: 输出目录（默认: src/<project>/repositories/）
        force: 是否强制覆盖

    Example:
        >>> generate_repository("user", table_name="users")
        ✅ Repository类生成成功！
        📁 文件路径: src/my_project/repositories/user_repository.py
    """

    # 检测项目名称
    project_name = detect_project_name()
    if not project_name:
        print("⚠️  错误: 无法检测项目名称，请在项目根目录下运行")
        return

    # 默认输出目录
    if output_dir is None:
        output_dir = Path.cwd() / "src" / project_name / "repositories"

    # 名称转换
    entity_name = to_snake_case(name)
    entity_name_pascal = to_pascal_case(name)
    table_name = table_name or f"{entity_name}s"

    # 变量替换
    replacements = {
        "{entity_name}": entity_name,
        "{EntityName}": entity_name_pascal,
        "{table_name}": table_name,
    }

    content = replace_template_vars(GEN_REPOSITORY_TEMPLATE, replacements)

    # 创建文件
    file_path = output_dir / f"{entity_name}_repository.py"
    create_file(file_path, content, force=force)

    print("\n✅ Repository类生成成功！")
    print(f"📁 文件路径: {safe_relative_path(file_path)}")
    print("\n💡 使用示例:")
    print(f"  from {project_name}.repositories import {entity_name_pascal}Repository")
    print(f"  repo = {entity_name_pascal}Repository(database)")
    print("  item = repo.find_by_id(1)")


def generate_api_client(
    name: str,
    *,
    api_path: str = None,
    output_dir: Path = None,
    force: bool = False,
) -> None:
    """生成API客户端类

    Args:
        name: API名称（如: user, order）
        api_path: API路径前缀（默认与name相同）
        output_dir: 输出目录（默认: src/<project>/apis/）
        force: 是否强制覆盖

    Example:
        >>> generate_api_client("user", api_path="users")
        ✅ API客户端类生成成功！
        📁 文件路径: src/my_project/apis/user_api.py
    """

    # 检测项目名称
    project_name = detect_project_name()
    if not project_name:
        print("⚠️  错误: 无法检测项目名称，请在项目根目录下运行")
        return

    # 默认输出目录
    if output_dir is None:
        output_dir = Path.cwd() / "src" / project_name / "apis"

    # 名称转换
    api_name = to_snake_case(name)
    api_name_pascal = to_pascal_case(name)
    api_path = api_path or f"{api_name}s"
    method_name = api_name

    # 变量替换
    replacements = {
        "{api_name}": api_name,
        "{ApiName}": api_name_pascal,
        "{api_path}": api_path,
        "{method_name}": method_name,
    }

    content = replace_template_vars(GEN_API_CLIENT_TEMPLATE, replacements)

    # 创建文件
    file_path = output_dir / f"{api_name}_api.py"
    create_file(file_path, content, force=force)

    print("\n✅ API客户端类生成成功！")
    print(f"📁 文件路径: {safe_relative_path(file_path)}")
    print("\n💡 使用示例:")
    print(f"  from {project_name}.apis import {api_name_pascal}API")
    print(f"  api = {api_name_pascal}API(http_client)")
    print(f"  result = api.get_{method_name}(1)")


__all__ = [
    "generate_test",
    "generate_builder",
    "generate_repository",
    "generate_api_client",
]


def generate_models_from_json(
    json_file: Path,
    *,
    model_name: str = None,
    output_dir: Path = None,
    force: bool = False,
) -> None:
    """从JSON响应生成Pydantic模型

    Args:
        json_file: JSON文件路径
        model_name: 模型名称（默认根据文件名生成）
        output_dir: 输出目录（默认: src/<project>/models/responses/）
        force: 是否强制覆盖

    Example:
        >>> generate_models_from_json(
        ...     Path("response.json"),
        ...     model_name="UserResponse"
        ... )
        ✅ 模型文件生成成功！
        📁 文件路径: src/my_project/models/responses/user_response.py
    """
    # 检测项目名称
    project_name = detect_project_name()
    if not project_name:
        print("⚠️  错误: 无法检测项目名称，请在项目根目录下运行")
        return

    # 默认输出目录
    if output_dir is None:
        output_dir = Path.cwd() / "src" / project_name / "models" / "responses"

    # 读取JSON文件
    if not json_file.exists():
        print(f"❌ 错误: JSON文件不存在: {json_file}")
        return

    try:
        json_content = json_file.read_text(encoding="utf-8")
        json_data = json.loads(json_content)
    except json.JSONDecodeError as e:
        print(f"❌ 错误: JSON解析失败: {e}")
        return

    # 推断模型名称
    if model_name is None:
        # 从文件名推断: user_create_response.json -> UserCreateResponse
        file_stem = json_file.stem
        model_name = to_pascal_case(file_stem)
        if not model_name.endswith("Response"):
            model_name += "Response"

    # 生成模型文件名
    model_file_name = to_snake_case(model_name) + ".py"
    output_file = output_dir / model_file_name

    # 检查文件是否存在
    if output_file.exists() and not force:
        print(f"⚠️  文件已存在: {output_file}")
        print("   使用 --force 强制覆盖")
        return

    # 生成模型
    generate_pydantic_model_from_json(
        json_data,
        model_name=model_name,
        wrap_in_base_response=True,
        output_file=output_file,
    )

    print("\n💡 使用示例:")
    print(f"  from {project_name}.models.responses import {model_name}, {model_name}Data")
    print(f"  response: {model_name} = ...")
    print("  print(response.data)")


def generate_settings(
    *,
    with_interceptors: bool = True,
    with_profile: bool = True,
    output_dir: Path = None,
    force: bool = False,
) -> None:
    """生成项目配置文件

    Args:
        with_interceptors: 是否包含拦截器配置（默认: True）
        with_profile: 是否生成Profile环境配置文件（默认: True）
        output_dir: 输出目录（默认: src/<project>/）
        force: 是否强制覆盖

    Example:
        >>> generate_settings(with_interceptors=True, with_profile=True)
        ✅ 配置文件生成成功！
        📁 生成文件:
          - src/my_project/settings.py
          - .env
          - .env.dev
          - .env.test
          - .env.prod
          - .env.example
    """
    import datetime

    # 检测项目名称
    project_name = detect_project_name()
    if not project_name:
        print("⚠️  错误: 无法检测项目名称，请在项目根目录下运行")
        return

    # 默认输出目录
    if output_dir is None:
        output_dir = Path.cwd() / "src" / project_name

    # 名称转换
    project_name_snake = to_snake_case(project_name)
    project_name_pascal = to_pascal_case(project_name)

    # 生成的文件列表
    generated_files = []

    # === 生成 settings.py ===
    print("\n📝 生成配置文件...")

    # 使用增强模板（包含拦截器配置）
    settings_template = SETTINGS_ENHANCED_TEMPLATE

    # 变量替换
    replacements = {
        "{project_name}": project_name,
        "{project_name_snake}": project_name_snake,
        "{ProjectName}": project_name_pascal,
    }

    settings_content = replace_template_vars(settings_template, replacements)

    # 创建 settings.py 文件
    settings_file = output_dir / "settings.py"
    create_file(settings_file, settings_content, force=force)
    generated_files.append(("settings.py", safe_relative_path(settings_file)))

    # === 生成 .env 文件 ===
    if with_profile:
        print("📝 生成环境配置文件...")

        # 当前时间戳
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        env_replacements = {
            "{project_name}": project_name,
            "{timestamp}": timestamp,
        }

        # .env - 基础配置
        env_file = Path.cwd() / ".env"
        env_content = replace_template_vars(ENV_BASE_TEMPLATE, env_replacements)
        create_file(env_file, env_content, force=force)
        generated_files.append((".env", safe_relative_path(env_file)))

        # .env.dev - 开发环境
        env_dev_file = Path.cwd() / ".env.dev"
        env_dev_content = replace_template_vars(ENV_DEV_TEMPLATE, env_replacements)
        create_file(env_dev_file, env_dev_content, force=force)
        generated_files.append((".env.dev", safe_relative_path(env_dev_file)))

        # .env.test - 测试环境
        env_test_file = Path.cwd() / ".env.test"
        env_test_content = replace_template_vars(ENV_TEST_TEMPLATE, env_replacements)
        create_file(env_test_file, env_test_content, force=force)
        generated_files.append((".env.test", safe_relative_path(env_test_file)))

        # .env.prod - 生产环境
        env_prod_file = Path.cwd() / ".env.prod"
        env_prod_content = replace_template_vars(ENV_PROD_TEMPLATE, env_replacements)
        create_file(env_prod_file, env_prod_content, force=force)
        generated_files.append((".env.prod", safe_relative_path(env_prod_file)))

        # .env.example - 配置示例
        env_example_file = Path.cwd() / ".env.example"
        env_example_content = replace_template_vars(ENV_EXAMPLE_TEMPLATE, env_replacements)
        create_file(env_example_file, env_example_content, force=force)
        generated_files.append((".env.example", safe_relative_path(env_example_file)))

    # === 输出结果 ===
    print("\n✅ 配置文件生成成功！")
    if with_interceptors:
        print("📋 包含功能: v3.5 配置化拦截器（签名、Token认证）")
    if with_profile:
        print("📋 包含功能: Profile 环境配置（dev/test/prod）")

    print("\n📁 生成的文件:")
    for file_name, file_path in generated_files:
        print(f"  ✓ {file_name:<20} {file_path}")

    print("\n💡 下一步:")
    print("  1. 编辑 settings.py，启用需要的拦截器（取消注释）")
    print("  2. 编辑 .env 文件，配置实际的服务地址和密钥")
    print("  3. 在 conftest.py 中使用配置:")
    print(f"     from {project_name_snake}.settings import {project_name_pascal}Settings")
    print(f"     runtime = Bootstrap().with_settings({project_name_pascal}Settings).build().run()")
    print("\n  4. 切换环境:")
    print("     ENV=dev pytest   # 使用开发环境")
    print("     ENV=test pytest  # 使用测试环境")


__all__ = [
    "generate_test",
    "generate_builder",
    "generate_repository",
    "generate_api_client",
    "generate_models_from_json",
    "generate_settings",
]
