"""测试 init_cmd.py - 项目初始化命令

测试覆盖:
- init_project() 函数
- API项目初始化
- UI项目初始化
- Full项目初始化
- 文件生成验证
- 智能依赖选择（CI环境检测）
"""

import shutil

import pytest

from df_test_framework.cli.commands.init_cmd import _get_framework_dependency, init_project


class TestInitProject:
    """测试项目初始化功能"""

    @pytest.fixture
    def temp_project_dir(self, tmp_path):
        """临时项目目录"""
        project_dir = tmp_path / "test_project"
        yield project_dir
        # 清理
        if project_dir.exists():
            shutil.rmtree(project_dir, ignore_errors=True)

    def test_init_api_project(self, temp_project_dir, capsys):
        """测试初始化API项目"""
        # 执行初始化
        init_project(temp_project_dir, project_type="api", force=True)

        # 验证输出
        captured = capsys.readouterr()
        assert "✅" in captured.out
        assert "API测试项目初始化成功" in captured.out

        # 验证目录结构
        assert temp_project_dir.exists()
        assert (temp_project_dir / "src" / "test_project").exists()
        assert (temp_project_dir / "tests").exists()

        # 验证关键文件（v3.13.0: pytest配置已整合到pyproject.toml）
        assert (temp_project_dir / "pyproject.toml").exists()
        assert (temp_project_dir / ".env.example").exists()
        assert (temp_project_dir / "README.md").exists()

        # 验证API特定文件
        assert (temp_project_dir / "src" / "test_project" / "apis").exists()
        assert (temp_project_dir / "src" / "test_project" / "apis" / "base.py").exists()
        assert (temp_project_dir / "tests" / "api").exists()
        assert (temp_project_dir / "tests" / "api" / "test_example.py").exists()

    def test_init_ui_project(self, temp_project_dir):
        """测试初始化UI项目"""
        # 执行初始化
        init_project(temp_project_dir, project_type="ui", force=True)

        # 验证目录结构
        assert temp_project_dir.exists()

        # 验证UI特定文件
        assert (temp_project_dir / "src" / "test_project" / "pages").exists()
        assert (temp_project_dir / "src" / "test_project" / "pages" / "home_page.py").exists()
        assert (temp_project_dir / "tests" / "ui").exists()
        assert (temp_project_dir / "tests" / "ui" / "test_home_page.py").exists()

    def test_init_full_project(self, temp_project_dir):
        """测试初始化Full项目（API + UI）"""
        # 执行初始化
        init_project(temp_project_dir, project_type="full", force=True)

        # 验证API文件
        assert (temp_project_dir / "src" / "test_project" / "apis").exists()
        assert (temp_project_dir / "tests" / "api").exists()

        # 验证UI文件
        assert (temp_project_dir / "src" / "test_project" / "pages").exists()
        assert (temp_project_dir / "tests" / "ui").exists()

    def test_init_project_with_invalid_type(self, temp_project_dir):
        """测试使用无效的项目类型"""
        with pytest.raises(ValueError, match="不支持的项目类型"):
            init_project(temp_project_dir, project_type="invalid")

    def test_init_project_creates_config_files(self, temp_project_dir):
        """测试创建配置文件"""
        init_project(temp_project_dir, project_type="api", force=True)

        # 验证配置文件内容（v3.13.0: pytest配置已整合到pyproject.toml）
        pyproject = (temp_project_dir / "pyproject.toml").read_text(encoding="utf-8")
        assert "df-test-framework" in pyproject
        assert "df_settings_class" in pyproject
        assert "asyncio_mode" in pyproject  # v3.13.0: pytest-asyncio配置

    def test_init_project_creates_settings(self, temp_project_dir):
        """测试创建settings文件"""
        init_project(temp_project_dir, project_type="api", force=True)

        settings_file = temp_project_dir / "src" / "test_project" / "config" / "settings.py"
        assert settings_file.exists()

        content = settings_file.read_text(encoding="utf-8")
        assert "TestProjectSettings" in content
        assert "FrameworkSettings" in content
        # v3.5+ 使用 HTTPSettings 替代 HTTPConfig
        assert "HTTPSettings" in content

    def test_init_project_creates_fixtures(self, temp_project_dir):
        """测试创建fixtures文件"""
        init_project(temp_project_dir, project_type="api", force=True)

        fixtures_init = temp_project_dir / "src" / "test_project" / "fixtures" / "__init__.py"
        assert fixtures_init.exists()

        content = fixtures_init.read_text(encoding="utf-8")
        # v3.11.1: 框架通过 pytest_plugins 自动提供核心 fixtures，项目不再需要导入
        # 验证文档说明存在
        assert "框架自动提供（通过 pytest_plugins）" in content
        assert "runtime" in content
        assert "http_client" in content
        assert "database" in content
        assert "http_mock" in content
        assert "time_mock" in content

    def test_init_project_force_overwrite(self, temp_project_dir):
        """测试强制覆盖已存在的文件"""
        # 第一次初始化
        init_project(temp_project_dir, project_type="api", force=True)

        # 修改一个文件
        readme = temp_project_dir / "README.md"
        readme.write_text("Modified content", encoding="utf-8")

        # 第二次初始化（强制覆盖）
        init_project(temp_project_dir, project_type="api", force=True)

        # 验证文件被覆盖
        content = readme.read_text(encoding="utf-8")
        assert "Modified content" not in content

    def test_init_project_creates_utils(self, temp_project_dir):
        """测试创建utils工具模块"""
        init_project(temp_project_dir, project_type="api", force=True)

        # 验证utils目录
        utils_dir = temp_project_dir / "src" / "test_project" / "utils"
        assert utils_dir.exists()
        assert (utils_dir / "validators.py").exists()
        assert (utils_dir / "converters.py").exists()

    def test_init_project_creates_constants(self, temp_project_dir):
        """测试创建constants常量模块"""
        init_project(temp_project_dir, project_type="api", force=True)

        # 验证constants目录
        constants_dir = temp_project_dir / "src" / "test_project" / "constants"
        assert constants_dir.exists()
        assert (constants_dir / "error_codes.py").exists()

    def test_init_project_creates_docs(self, temp_project_dir):
        """测试创建文档目录"""
        init_project(temp_project_dir, project_type="api", force=True)

        # 验证docs目录
        docs_dir = temp_project_dir / "docs"
        assert docs_dir.exists()
        assert (docs_dir / "api.md").exists()

    def test_init_project_creates_scripts(self, temp_project_dir):
        """测试创建scripts脚本目录"""
        init_project(temp_project_dir, project_type="api", force=True)

        # 验证scripts目录
        scripts_dir = temp_project_dir / "scripts"
        assert scripts_dir.exists()
        assert (scripts_dir / "run_tests.sh").exists()


class TestFrameworkDependency:
    """测试智能依赖选择功能（v3.10.0+）"""

    def test_get_framework_dependency_in_ci(self, monkeypatch):
        """测试 CI 环境自动使用本地路径"""
        # 模拟 CI 环境
        monkeypatch.setenv("CI", "true")

        result = _get_framework_dependency()

        assert result == '"df-test-framework @ file://.."'

    def test_get_framework_dependency_with_local_dev_flag(self, monkeypatch):
        """测试 DF_TEST_LOCAL_DEV=1 使用本地路径"""
        # 清除 CI 环境变量
        monkeypatch.delenv("CI", raising=False)
        # 设置本地开发标志
        monkeypatch.setenv("DF_TEST_LOCAL_DEV", "1")

        result = _get_framework_dependency()

        assert result == '"df-test-framework @ file://.."'

    def test_get_framework_dependency_default(self, monkeypatch):
        """测试默认使用 PyPI 版本"""
        # 清除所有环境变量
        monkeypatch.delenv("CI", raising=False)
        monkeypatch.delenv("DF_TEST_LOCAL_DEV", raising=False)

        result = _get_framework_dependency()

        assert result == '"df-test-framework>=3.5.0"'

    def test_init_project_uses_correct_dependency_in_ci(self, tmp_path, monkeypatch):
        """测试 CI 环境生成的项目使用本地路径依赖"""
        # 模拟 CI 环境
        monkeypatch.setenv("CI", "true")

        project_dir = tmp_path / "ci_test_project"
        init_project(project_dir, project_type="api", force=True)

        # 读取 pyproject.toml
        pyproject = (project_dir / "pyproject.toml").read_text(encoding="utf-8")

        # 验证使用了本地路径依赖
        assert "df-test-framework @ file://.." in pyproject
        assert "df-test-framework>=3.5.0" not in pyproject

    def test_init_project_uses_correct_dependency_default(self, tmp_path, monkeypatch):
        """测试默认环境生成的项目使用 PyPI 版本"""
        # 清除环境变量
        monkeypatch.delenv("CI", raising=False)
        monkeypatch.delenv("DF_TEST_LOCAL_DEV", raising=False)

        project_dir = tmp_path / "default_test_project"
        init_project(project_dir, project_type="api", force=True)

        # 读取 pyproject.toml
        pyproject = (project_dir / "pyproject.toml").read_text(encoding="utf-8")

        # 验证使用了 PyPI 版本
        assert "df-test-framework>=3.5.0" in pyproject
        assert "df-test-framework @ file://.." not in pyproject


__all__ = ["TestInitProject", "TestFrameworkDependency"]
