"""init命令实现

创建测试项目脚手架。
"""

from __future__ import annotations

import os
from pathlib import Path

from ..templates import (
    BASE_API_TEMPLATE,
    CONFTEST_TEMPLATE,
    CONSTANTS_ERROR_CODES_TEMPLATE,
    DATA_CLEANERS_TEMPLATE,
    DOCS_API_TEMPLATE,
    ENHANCED_GITIGNORE_TEMPLATE,
    ENV_TEMPLATE,
    FIXTURES_INIT_TEMPLATE,
    PYPROJECT_TOML_TEMPLATE,
    README_TEMPLATE,
    SCRIPT_RUN_TESTS_TEMPLATE,
    SETTINGS_TEMPLATE,
    TEST_EXAMPLE_TEMPLATE,
    UI_CONFTEST_TEMPLATE,
    UI_FIXTURES_INIT_TEMPLATE,
    UI_PAGE_OBJECT_TEMPLATE,
    UI_SETTINGS_TEMPLATE,
    UI_TEST_EXAMPLE_TEMPLATE,
    UOW_TEMPLATE,  # v3.7.0+
    UTILS_CONVERTERS_TEMPLATE,
    # 增强功能模板
    UTILS_VALIDATORS_TEMPLATE,
)
from ..utils import create_file, replace_template_vars, to_pascal_case, to_snake_case
from .cicd import generate_cicd_files


def _get_framework_dependency() -> str:
    """智能选择框架依赖

    根据环境自动选择合适的依赖方式：
    1. CI 环境（自动检测） → 本地路径依赖
    2. DF_TEST_LOCAL_DEV=1 → 本地路径依赖
    3. 默认 → PyPI 版本依赖

    Returns:
        框架依赖字符串

    Example:
        >>> os.environ["CI"] = "true"
        >>> _get_framework_dependency()
        '"df-test-framework @ file://.."'

        >>> os.environ.pop("CI")
        >>> _get_framework_dependency()
        '"df-test-framework>=3.5.0"'
    """
    # 检测 CI 环境（GitHub Actions, GitLab CI, Jenkins 等都会设置 CI=true）
    if os.getenv("CI") == "true":
        return '"df-test-framework @ file://.."'

    # 检测本地开发标志
    if os.getenv("DF_TEST_LOCAL_DEV") == "1":
        return '"df-test-framework @ file://.."'

    # 生产环境：从 PyPI 安装
    return '"df-test-framework>=3.5.0"'


def init_project(
    path: Path, *, project_type: str = "api", ci_platform: str = "none", force: bool = False
) -> None:
    """初始化测试项目

    创建完整的项目结构，支持不同类型的测试项目。

    项目类型:
    - api: API测试项目（默认）
    - ui: UI测试项目（基于Playwright）
    - full: 完整项目（API + UI）

    CI/CD平台:
    - github-actions: GitHub Actions工作流
    - gitlab-ci: GitLab CI配置
    - jenkins: Jenkins Pipeline
    - all: 所有平台
    - none: 不生成CI/CD配置（默认）

    Args:
        path: 项目路径
        project_type: 项目类型（api, ui, full）
        ci_platform: CI/CD平台（github-actions, gitlab-ci, jenkins, all, none）
        force: 是否强制覆盖已存在的文件

    Raises:
        FileExistsError: 文件已存在且force=False
        ValueError: 不支持的项目类型

    Example:
        >>> init_project(Path("my-test-project"), project_type="api")
        ✅ API测试项目初始化成功！
        ...
        >>> init_project(Path("my-test-project"), project_type="api", ci_platform="github-actions")
        ✅ API测试项目初始化成功！
        ✅ GitHub Actions工作流配置已生成！
        ...
    """
    if project_type not in ("api", "ui", "full"):
        raise ValueError(f"不支持的项目类型: {project_type}，支持: api, ui, full")
    # 创建项目根目录
    path.mkdir(parents=True, exist_ok=True)

    # 项目名称转换
    project_name_raw = path.name
    project_name = to_snake_case(project_name_raw)
    project_name_pascal = to_pascal_case(project_name_raw)

    # 变量替换字典
    replacements = {
        "{project_name}": project_name,
        "{ProjectName}": project_name_pascal,
        "{framework_dependency}": _get_framework_dependency(),  # 智能依赖选择
    }

    def replace_template(template: str) -> str:
        """替换模板中的变量"""
        return replace_template_vars(template, replacements)

    # 根据项目类型选择模板
    if project_type in ("api", "full"):
        settings_template = SETTINGS_TEMPLATE
        conftest_template = CONFTEST_TEMPLATE
        fixtures_template = FIXTURES_INIT_TEMPLATE
    else:  # ui
        settings_template = UI_SETTINGS_TEMPLATE
        conftest_template = UI_CONFTEST_TEMPLATE
        fixtures_template = UI_FIXTURES_INIT_TEMPLATE

    # 基础文件结构（所有项目类型共有）
    files_to_create = {
        # src目录
        f"src/{project_name}/__init__.py": '"""项目根模块"""\n\n__version__ = "1.0.0"\n',
        f"src/{project_name}/config/__init__.py": replace_template(
            '"""配置模块"""\n\nfrom .settings import {ProjectName}Settings\n\n__all__ = ["{ProjectName}Settings"]\n'
        ),
        f"src/{project_name}/config/settings.py": replace_template(settings_template),
        f"src/{project_name}/fixtures/__init__.py": replace_template(fixtures_template),
        # utils目录（工具函数）
        f"src/{project_name}/utils/__init__.py": replace_template(
            '"""工具函数模块"""\n\nfrom .validators import *\nfrom .converters import *\n\n__all__ = ["validators", "converters"]\n'
        ),
        f"src/{project_name}/utils/validators.py": replace_template(UTILS_VALIDATORS_TEMPLATE),
        f"src/{project_name}/utils/converters.py": replace_template(UTILS_CONVERTERS_TEMPLATE),
        # constants目录（常量定义）
        f"src/{project_name}/constants/__init__.py": replace_template(
            '"""常量模块"""\n\nfrom .error_codes import *\n\n__all__ = ["error_codes"]\n'
        ),
        f"src/{project_name}/constants/error_codes.py": replace_template(
            CONSTANTS_ERROR_CODES_TEMPLATE
        ),
        # tests目录
        "tests/__init__.py": '"""测试根模块"""\n',
        "tests/conftest.py": replace_template(conftest_template),
        "tests/data/fixtures/.gitkeep": "",
        "tests/data/files/.gitkeep": "",
        # 配置文件（pytest配置已整合到pyproject.toml）
        ".env.example": replace_template(ENV_TEMPLATE),
        ".gitignore": ENHANCED_GITIGNORE_TEMPLATE,
        "README.md": replace_template(README_TEMPLATE),
        "pyproject.toml": replace_template(PYPROJECT_TOML_TEMPLATE),
        # 文档目录
        "docs/api.md": replace_template(DOCS_API_TEMPLATE),
        # 脚本目录
        "scripts/run_tests.sh": replace_template(SCRIPT_RUN_TESTS_TEMPLATE),
        # reports子目录占位文件
        "reports/screenshots/.gitkeep": "",
        "reports/allure-results/.gitkeep": "",
        "reports/logs/.gitkeep": "",
    }

    # API项目特有文件
    if project_type in ("api", "full"):
        api_files = {
            f"src/{project_name}/apis/__init__.py": replace_template(
                '"""API封装模块"""\n\nfrom .base import {ProjectName}BaseAPI\n\n__all__ = ["{ProjectName}BaseAPI"]\n'
            ),
            f"src/{project_name}/apis/base.py": replace_template(BASE_API_TEMPLATE),
            f"src/{project_name}/models/__init__.py": '"""数据模型模块"""\n',
            f"src/{project_name}/models/requests/__init__.py": '"""请求模型"""\n',
            f"src/{project_name}/models/responses/__init__.py": '"""响应模型"""\n',
            f"src/{project_name}/repositories/__init__.py": '"""Repository层"""\n',
            f"src/{project_name}/builders/__init__.py": '"""Builder层"""\n',
            f"src/{project_name}/uow.py": replace_template(UOW_TEMPLATE),  # ✅ v3.7.0+
            f"src/{project_name}/fixtures/data_cleaners.py": replace_template(
                DATA_CLEANERS_TEMPLATE
            ),
            "tests/api/__init__.py": '"""API测试模块"""\n',
            "tests/api/test_example.py": replace_template(TEST_EXAMPLE_TEMPLATE),
        }
        files_to_create.update(api_files)

    # UI项目特有文件
    if project_type in ("ui", "full"):
        # 创建HomePage页面对象示例
        home_page_template = replace_template(
            UI_PAGE_OBJECT_TEMPLATE.replace("{page_name}", "home")
            .replace("{PageName}", "Home")
            .replace("{page_url}", "/")
        )

        ui_files = {
            f"src/{project_name}/pages/__init__.py": replace_template(
                '"""页面对象模块"""\n\nfrom .home_page import HomePage\n\n__all__ = ["HomePage"]\n'
            ),
            f"src/{project_name}/pages/home_page.py": home_page_template,
            "tests/ui/__init__.py": '"""UI测试模块"""\n',
            "tests/ui/test_home_page.py": replace_template(UI_TEST_EXAMPLE_TEMPLATE),
        }
        # UI项目也添加data_cleaners（E2E测试可能需要）
        if project_type == "ui":
            ui_files[f"src/{project_name}/fixtures/data_cleaners.py"] = replace_template(
                DATA_CLEANERS_TEMPLATE
            )
        files_to_create.update(ui_files)

    # 创建所有文件
    created_files = []
    for file_path_str, content in files_to_create.items():
        file_path = path / file_path_str
        try:
            create_file(file_path, content, force=force)
            created_files.append(file_path_str)
        except FileExistsError as e:
            print(f"⚠️  跳过: {e}")
            continue

    # 打印成功信息
    print(f"\n✅ {project_type.upper()}测试项目初始化成功！")
    print(f"📁 项目路径: {path.absolute()}\n")
    print("📋 已创建的文件:")
    for file in created_files:
        print(f"  ✓ {file}")

    print("\n🚀 下一步:")
    print(f"  1. cd {path.name}")

    if project_type in ("ui", "full"):
        print("  2. pip install playwright")
        print("  3. playwright install  # 安装浏览器驱动")
        step_num = 4
    else:
        step_num = 2

    print(f"  {step_num}. cp .env.example .env")
    print(f"  {step_num + 1}. 编辑 .env 文件，配置相关设置")

    if project_type == "api":
        print(f"  {step_num + 2}. pytest tests/api/ -v  # 运行API测试")
    elif project_type == "ui":
        print(f"  {step_num + 2}. pytest tests/ui/ -v  # 运行UI测试")
        print("\n💡 提示:")
        print("  - 使用 --headed 参数查看浏览器界面: pytest --headed")
        print("  - 使用 --browser 选择浏览器: pytest --browser firefox")
    else:  # full
        print(f"  {step_num + 2}. pytest tests/api/ -v  # 运行API测试")
        print(f"  {step_num + 3}. pytest tests/ui/ -v  # 运行UI测试")
        print("\n💡 提示:")
        print("  - UI测试: 使用 --headed 查看浏览器界面")
        print("  - 失败截图保存在 reports/screenshots/ 目录")

    print("\n📚 参考文档: https://github.com/your-org/df-test-framework")

    # 生成CI/CD配置文件（如果指定）
    if ci_platform != "none":
        print("\n🔧 生成CI/CD配置...")
        try:
            cicd_files = generate_cicd_files(path, ci_platform)
            if cicd_files:
                print(f"✅ {ci_platform.upper()} 配置已生成！")
                print("📋 CI/CD文件:")
                for file in cicd_files:
                    relative_path = file.relative_to(path)
                    print(f"  ✓ {relative_path}")

                print("\n💡 CI/CD使用提示:")
                if ci_platform in ("github-actions", "all"):
                    print("  - GitHub Actions: 在仓库Settings → Secrets中配置环境变量")
                if ci_platform in ("gitlab-ci", "all"):
                    print("  - GitLab CI: 在项目Settings → CI/CD → Variables中配置")
                if ci_platform in ("jenkins", "all"):
                    print("  - Jenkins: 在Pipeline配置中添加凭据")
                print("  - 详细文档: docs/user-guide/ci-cd.md")
        except Exception as e:
            print(f"⚠️  CI/CD配置生成失败: {e}")


__all__ = ["init_project"]
