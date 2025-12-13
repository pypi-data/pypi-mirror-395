"""pyproject.toml配置文件模板"""

PYPROJECT_TOML_TEMPLATE = """[project]
name = "{project_name}"
version = "1.0.0"
description = "基于 df-test-framework v3.13.0 的自动化测试项目"
requires-python = ">=3.12"
dependencies = [
    {framework_dependency},
    "pytest>=8.0.0",
    "allure-pytest>=2.13.0",
    "pydantic>=2.0.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest-cov>=5.0.0",
    "ruff>=0.6.0",
    "mypy>=1.11.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.metadata]
allow-direct-references = true

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
addopts = ["-v", "--strict-markers", "--tb=short"]
markers = [
    "smoke: 冒烟测试",
    "regression: 回归测试",
    "integration: 集成测试",
    # 注意: keep_data marker 由框架自动注册，无需在此定义
]
# v3.13.0: pytest-asyncio 配置（支持 async def test_xxx）
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
# df_settings_class 指定框架使用的 Settings 类
df_settings_class = "{project_name}.config.{ProjectName}Settings"

[tool.ruff]
line-length = 120
target-version = "py312"
select = ["E", "F", "I", "N", "W", "UP"]

[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
"""

__all__ = ["PYPROJECT_TOML_TEMPLATE"]
