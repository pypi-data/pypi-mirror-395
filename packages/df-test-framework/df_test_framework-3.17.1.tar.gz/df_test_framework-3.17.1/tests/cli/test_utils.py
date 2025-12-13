"""测试 utils.py - CLI工具函数

测试覆盖:
- to_snake_case() - 名称转换为蛇形
- to_pascal_case() - 名称转换为帕斯卡
- create_file() - 文件创建
- replace_template_vars() - 模板变量替换
- detect_project_name() - 项目名称检测
"""

import shutil

import pytest

from df_test_framework.cli.utils import (
    create_file,
    detect_project_name,
    replace_template_vars,
    to_pascal_case,
    to_snake_case,
)


class TestNameConversion:
    """测试名称转换函数"""

    def test_to_snake_case_with_hyphens(self):
        """测试横杠分隔转蛇形"""
        assert to_snake_case("my-test-project") == "my_test_project"
        assert to_snake_case("gift-card-api") == "gift_card_api"

    def test_to_snake_case_with_spaces(self):
        """测试空格分隔转蛇形"""
        assert to_snake_case("my test project") == "my_test_project"
        assert to_snake_case("user login test") == "user_login_test"

    def test_to_snake_case_with_camel_case(self):
        """测试驼峰命名转蛇形"""
        assert to_snake_case("MyTestProject") == "my_test_project"
        assert to_snake_case("UserLogin") == "user_login"
        assert to_snake_case("HTTPClient") == "http_client"
        assert to_snake_case("XMLParser") == "xml_parser"

    def test_to_snake_case_already_snake(self):
        """测试已经是蛇形的名称"""
        assert to_snake_case("my_test_project") == "my_test_project"
        assert to_snake_case("user_login") == "user_login"

    def test_to_snake_case_mixed_format(self):
        """测试混合格式"""
        assert to_snake_case("my-TestProject") == "my_test_project"
        assert to_snake_case("User-Login_Test") == "user_login_test"

    def test_to_pascal_case_with_hyphens(self):
        """测试横杠分隔转帕斯卡"""
        assert to_pascal_case("my-test-project") == "MyTestProject"
        assert to_pascal_case("gift-card-api") == "GiftCardApi"

    def test_to_pascal_case_with_underscores(self):
        """测试下划线分隔转帕斯卡"""
        assert to_pascal_case("my_test_project") == "MyTestProject"
        assert to_pascal_case("user_login") == "UserLogin"

    def test_to_pascal_case_with_camel_case(self):
        """测试驼峰命名转帕斯卡"""
        assert to_pascal_case("UserLogin") == "UserLogin"
        assert to_pascal_case("myTestProject") == "MyTestProject"

    def test_to_pascal_case_with_spaces(self):
        """测试空格分隔转帕斯卡"""
        assert to_pascal_case("my test project") == "MyTestProject"


class TestCreateFile:
    """测试文件创建函数"""

    @pytest.fixture
    def temp_dir(self, tmp_path):
        """临时目录"""
        yield tmp_path
        # 清理
        for item in tmp_path.iterdir():
            if item.is_dir():
                shutil.rmtree(item, ignore_errors=True)
            else:
                item.unlink()

    def test_create_file_simple(self, temp_dir):
        """测试创建简单文件"""
        file_path = temp_dir / "test.txt"
        content = "Hello World"

        create_file(file_path, content)

        assert file_path.exists()
        assert file_path.read_text(encoding="utf-8") == content

    def test_create_file_with_directory(self, temp_dir):
        """测试创建带目录的文件"""
        file_path = temp_dir / "subdir" / "nested" / "test.txt"
        content = "Nested file"

        create_file(file_path, content)

        assert file_path.exists()
        assert file_path.read_text(encoding="utf-8") == content

    def test_create_file_already_exists_without_force(self, temp_dir):
        """测试文件已存在且不强制覆盖"""
        file_path = temp_dir / "existing.txt"
        file_path.write_text("Original content", encoding="utf-8")

        with pytest.raises(FileExistsError, match="already exists"):
            create_file(file_path, "New content", force=False)

        # 验证文件内容未被修改
        assert file_path.read_text(encoding="utf-8") == "Original content"

    def test_create_file_already_exists_with_force(self, temp_dir):
        """测试文件已存在且强制覆盖"""
        file_path = temp_dir / "existing.txt"
        file_path.write_text("Original content", encoding="utf-8")

        create_file(file_path, "New content", force=True)

        assert file_path.read_text(encoding="utf-8") == "New content"

    def test_create_file_with_chinese_content(self, temp_dir):
        """测试创建包含中文的文件"""
        file_path = temp_dir / "chinese.txt"
        content = "你好，世界！"

        create_file(file_path, content)

        assert file_path.read_text(encoding="utf-8") == content


class TestReplaceTemplateVars:
    """测试模板变量替换函数"""

    def test_replace_single_variable(self):
        """测试替换单个变量"""
        template = "Hello {name}!"
        result = replace_template_vars(template, {"{name}": "World"})
        assert result == "Hello World!"

    def test_replace_multiple_variables(self):
        """测试替换多个变量"""
        template = "Project: {project_name}, Type: {project_type}"
        replacements = {"{project_name}": "my-project", "{project_type}": "api"}
        result = replace_template_vars(template, replacements)
        assert result == "Project: my-project, Type: api"

    def test_replace_with_empty_dict(self):
        """测试空替换字典"""
        template = "No changes here"
        result = replace_template_vars(template, {})
        assert result == "No changes here"

    def test_replace_variable_multiple_times(self):
        """测试变量出现多次"""
        template = "{name} loves {name}"
        result = replace_template_vars(template, {"{name}": "Alice"})
        assert result == "Alice loves Alice"

    def test_replace_with_chinese(self):
        """测试替换中文变量"""
        template = "欢迎使用 {framework_name}"
        result = replace_template_vars(template, {"{framework_name}": "DF测试框架"})
        assert result == "欢迎使用 DF测试框架"


class TestDetectProjectName:
    """测试项目名称检测函数"""

    @pytest.fixture
    def temp_project(self, tmp_path):
        """创建临时项目目录"""
        import os

        old_cwd = os.getcwd()
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        os.chdir(project_dir)

        yield project_dir

        os.chdir(old_cwd)
        if project_dir.exists():
            shutil.rmtree(project_dir, ignore_errors=True)

    def test_detect_from_pyproject_toml(self, temp_project):
        """测试从pyproject.toml检测项目名"""
        pyproject = temp_project / "pyproject.toml"
        pyproject.write_text(
            '[project]\nname = "my-awesome-project"\nversion = "1.0.0"', encoding="utf-8"
        )

        name = detect_project_name()
        assert name == "my-awesome-project"

    def test_detect_from_pyproject_toml_with_quotes(self, temp_project):
        """测试从pyproject.toml检测项目名（不同引号）"""
        pyproject = temp_project / "pyproject.toml"
        pyproject.write_text(
            "[project]\nname = 'single-quote-project'\nversion = '1.0.0'", encoding="utf-8"
        )

        name = detect_project_name()
        assert name == "single-quote-project"

    def test_detect_from_pyproject_toml_with_spaces(self, temp_project):
        """测试从pyproject.toml检测项目名（带空格）"""
        pyproject = temp_project / "pyproject.toml"
        pyproject.write_text(
            '[project]\n  name  =  "spaced-project"  \nversion = "1.0.0"', encoding="utf-8"
        )

        name = detect_project_name()
        assert name == "spaced-project"

    def test_detect_fallback_to_directory_name(self, temp_project):
        """测试无pyproject.toml时回退到目录名"""
        name = detect_project_name()
        assert name == "test_project"

    def test_detect_from_pyproject_toml_malformed(self, temp_project):
        """测试pyproject.toml格式错误时回退到目录名"""
        pyproject = temp_project / "pyproject.toml"
        pyproject.write_text(
            "[project]\nversion = '1.0.0'",  # 没有name字段
            encoding="utf-8",
        )

        name = detect_project_name()
        assert name == "test_project"


__all__ = [
    "TestNameConversion",
    "TestCreateFile",
    "TestReplaceTemplateVars",
    "TestDetectProjectName",
]
