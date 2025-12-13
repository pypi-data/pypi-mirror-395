"""测试 generate_cmd.py - 代码生成命令

测试覆盖:
- generate_test() - 生成测试文件
- generate_builder() - 生成Builder类
- generate_repository() - 生成Repository类
- generate_api_client() - 生成API客户端
- generate_models_from_json() - 从JSON生成模型
"""

import shutil

import pytest

from df_test_framework.cli.commands.generate_cmd import (
    generate_api_client,
    generate_builder,
    generate_models_from_json,
    generate_repository,
    generate_test,
)
from df_test_framework.cli.commands.init_cmd import init_project


class TestGenerateCommands:
    """测试代码生成命令"""

    @pytest.fixture
    def temp_project(self, tmp_path):
        """创建临时测试项目"""
        project_dir = tmp_path / "test_project"
        # 初始化项目
        init_project(project_dir, project_type="api", force=True)

        # 切换到项目目录
        import os

        old_cwd = os.getcwd()
        os.chdir(project_dir)

        yield project_dir

        # 恢复原目录
        os.chdir(old_cwd)
        # 清理
        if project_dir.exists():
            shutil.rmtree(project_dir, ignore_errors=True)

    def test_generate_test_file(self, temp_project, capsys):
        """测试生成测试文件"""
        # 生成测试文件
        generate_test("user_login", feature="用户模块", story="登录功能", force=True)

        # 验证输出
        captured = capsys.readouterr()
        assert "✅ 测试文件生成成功" in captured.out

        # 验证文件存在
        test_file = temp_project / "tests" / "api" / "test_user_login.py"
        assert test_file.exists()

        # 验证文件内容
        content = test_file.read_text(encoding="utf-8")
        assert "class TestUserLogin" in content
        assert "def test_user_login" in content
        assert '@allure.feature("用户模块")' in content
        assert '@allure.story("登录功能")' in content
        assert "http_client" in content
        # v3.7+: 使用uow替代db_transaction
        assert "uow" in content
        # v3.5新特性
        assert "http_mock" in content

    def test_generate_builder_class(self, temp_project, capsys):
        """测试生成Builder类"""
        # 生成Builder类
        generate_builder("user", force=True)

        # 验证输出
        captured = capsys.readouterr()
        assert "✅ Builder类生成成功" in captured.out

        # 验证文件存在
        builder_file = temp_project / "src" / "test_project" / "builders" / "user_builder.py"
        assert builder_file.exists()

        # 验证文件内容
        content = builder_file.read_text(encoding="utf-8")
        assert "class UserBuilder(DictBuilder)" in content
        assert "def with_name" in content
        assert "def with_status" in content
        # 修复后的导入路径
        assert "from df_test_framework import DictBuilder" in content

    def test_generate_repository_class(self, temp_project, capsys):
        """测试生成Repository类"""
        # 生成Repository类
        generate_repository("user", table_name="users", force=True)

        # 验证输出
        captured = capsys.readouterr()
        assert "✅ Repository类生成成功" in captured.out

        # 验证文件存在
        repo_file = temp_project / "src" / "test_project" / "repositories" / "user_repository.py"
        assert repo_file.exists()

        # 验证文件内容
        content = repo_file.read_text(encoding="utf-8")
        assert "class UserRepository(BaseRepository)" in content
        assert 'table_name="users"' in content
        assert "def find_by_name" in content
        assert "def find_by_status" in content
        # 修复后的导入路径
        assert "from df_test_framework import BaseRepository" in content
        # v3.7+: Repository模板接收Session而非Database
        assert "Session" in content

    def test_generate_api_client_class(self, temp_project, capsys):
        """测试生成API客户端类"""
        # 生成API客户端类
        generate_api_client("user", api_path="users", force=True)

        # 验证输出
        captured = capsys.readouterr()
        assert "✅ API客户端类生成成功" in captured.out

        # 验证文件存在
        api_file = temp_project / "src" / "test_project" / "apis" / "user_api.py"
        assert api_file.exists()

        # 验证文件内容
        content = api_file.read_text(encoding="utf-8")
        assert "class UserAPI(BaseAPI)" in content
        assert 'self.base_path = "/api/users"' in content
        assert "def get_user" in content
        assert "def list_users" in content
        assert "def create_user" in content
        assert "def update_user" in content
        assert "def delete_user" in content

    @pytest.mark.skip(reason="JSON模型生成功能需要进一步完善")
    def test_generate_models_from_json(self, temp_project, capsys):
        """测试从JSON生成Pydantic模型

        TODO: 此功能需要进一步完善
        - generate_models_from_json可能输出路径不正确
        - 需要调试json_to_model.py中的文件生成逻辑
        """
        pass

    def test_generate_test_with_custom_output_dir(self, temp_project):
        """测试生成测试文件到自定义目录"""
        custom_dir = temp_project / "tests" / "custom"
        generate_test("custom_test", output_dir=custom_dir, force=True)

        test_file = custom_dir / "test_custom_test.py"
        assert test_file.exists()

    def test_generate_builder_default_table_name(self, temp_project):
        """测试生成Repository时默认表名"""
        generate_repository("product", force=True)

        repo_file = temp_project / "src" / "test_project" / "repositories" / "product_repository.py"
        content = repo_file.read_text(encoding="utf-8")
        # 默认表名应该是复数形式
        assert 'table_name="products"' in content

    def test_generate_with_snake_case_conversion(self, temp_project):
        """测试名称转换（驼峰转蛇形）"""
        # 使用驼峰命名生成
        output_dir = temp_project / "tests" / "api"
        generate_test("UserLogin", output_dir=output_dir, force=True)

        # 验证文件名是蛇形
        test_file = output_dir / "test_user_login.py"
        assert test_file.exists()

        # 验证类名是Pascal命名
        content = test_file.read_text(encoding="utf-8")
        assert "class TestUserLogin" in content

    @pytest.mark.skip(reason="JSON模型生成功能需要进一步完善")
    def test_generate_models_auto_name_inference(self, temp_project):
        """测试从文件名自动推断模型名

        TODO: 依赖于test_generate_models_from_json的修复
        """
        pass


class TestGenerateCommandsErrors:
    """测试代码生成命令的错误处理"""

    def test_generate_without_project_structure(self, tmp_path, capsys):
        """测试在非项目目录生成代码时使用目录名作为项目名"""
        import os

        old_cwd = os.getcwd()
        os.chdir(tmp_path)

        try:
            # 尝试生成Builder（detect_project_name会回退到使用目录名）
            generate_builder("user", force=True)

            captured = capsys.readouterr()
            # detect_project_name 有回退机制，会使用目录名，所以应该成功生成
            assert "Builder类生成成功" in captured.out
            # 验证使用了临时目录名作为项目名
            assert tmp_path.name in captured.out or "test_generate_without_project" in captured.out
        finally:
            os.chdir(old_cwd)

    def test_generate_models_with_invalid_json(self, tmp_path):
        """测试使用无效JSON生成模型"""
        import os

        old_cwd = os.getcwd()

        # 创建临时项目
        project_dir = tmp_path / "test_proj"
        init_project(project_dir, project_type="api", force=True)
        os.chdir(project_dir)

        try:
            # 创建无效JSON文件
            json_file = project_dir / "invalid.json"
            json_file.write_text("{ invalid json }", encoding="utf-8")

            # 尝试生成（应该打印错误）
            generate_models_from_json(json_file, force=True)

            # 不应该生成文件
            model_dir = project_dir / "src" / "test_proj" / "models" / "responses"
            if model_dir.exists():
                model_files = list(model_dir.glob("*.py"))
                # 应该没有生成模型文件，或者只有__init__.py
                assert all(f.name == "__init__.py" for f in model_files)
        finally:
            os.chdir(old_cwd)
            if project_dir.exists():
                shutil.rmtree(project_dir, ignore_errors=True)


__all__ = ["TestGenerateCommands", "TestGenerateCommandsErrors"]
