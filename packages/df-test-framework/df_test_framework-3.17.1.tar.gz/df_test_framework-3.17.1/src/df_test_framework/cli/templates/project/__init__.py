"""项目初始化模板

包含创建测试项目时使用的所有文件模板。
"""

# 基础配置文件模板
from .base_api import BASE_API_TEMPLATE
from .conftest import CONFTEST_TEMPLATE
from .constants import CONSTANTS_ERROR_CODES_TEMPLATE
from .data_cleaners import DATA_CLEANERS_TEMPLATE
from .docs_api import DOCS_API_TEMPLATE
from .enhanced_gitignore import ENHANCED_GITIGNORE_TEMPLATE
from .env import ENV_TEMPLATE
from .fixtures_init import FIXTURES_INIT_TEMPLATE
from .gitignore import GITIGNORE_TEMPLATE
from .pyproject_toml import PYPROJECT_TOML_TEMPLATE
from .readme import README_TEMPLATE
from .script_run_tests import SCRIPT_RUN_TESTS_TEMPLATE

# API项目专用模板
from .settings import SETTINGS_TEMPLATE
from .test_example import TEST_EXAMPLE_TEMPLATE
from .ui_conftest import UI_CONFTEST_TEMPLATE
from .ui_fixtures_init import UI_FIXTURES_INIT_TEMPLATE
from .ui_page_object import UI_PAGE_OBJECT_TEMPLATE

# UI项目专用模板
from .ui_settings import UI_SETTINGS_TEMPLATE
from .ui_test_example import UI_TEST_EXAMPLE_TEMPLATE
from .uow import UOW_TEMPLATE  # v3.7.0+
from .utils_converters import UTILS_CONVERTERS_TEMPLATE

# 增强功能模板
from .utils_validators import UTILS_VALIDATORS_TEMPLATE

__all__ = [
    # 基础配置文件
    "ENV_TEMPLATE",
    "GITIGNORE_TEMPLATE",
    "README_TEMPLATE",
    "PYPROJECT_TOML_TEMPLATE",
    # API项目模板
    "SETTINGS_TEMPLATE",
    "CONFTEST_TEMPLATE",
    "FIXTURES_INIT_TEMPLATE",
    "BASE_API_TEMPLATE",
    "DATA_CLEANERS_TEMPLATE",
    "TEST_EXAMPLE_TEMPLATE",
    "UOW_TEMPLATE",  # v3.7.0+
    # UI项目模板
    "UI_SETTINGS_TEMPLATE",
    "UI_CONFTEST_TEMPLATE",
    "UI_PAGE_OBJECT_TEMPLATE",
    "UI_TEST_EXAMPLE_TEMPLATE",
    "UI_FIXTURES_INIT_TEMPLATE",
    # 增强功能模板
    "UTILS_VALIDATORS_TEMPLATE",
    "UTILS_CONVERTERS_TEMPLATE",
    "CONSTANTS_ERROR_CODES_TEMPLATE",
    "ENHANCED_GITIGNORE_TEMPLATE",
    "SCRIPT_RUN_TESTS_TEMPLATE",
    "DOCS_API_TEMPLATE",
]
