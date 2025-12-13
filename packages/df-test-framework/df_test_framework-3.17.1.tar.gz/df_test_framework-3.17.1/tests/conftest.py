"""pytest配置文件

自动导入测试框架的fixtures,包括:
- Allure observer: _auto_allure_observer (autouse=True，自动启用)
"""

# 默认加载框架核心 + Allure fixtures，确保 http_client/http_mock 等可用
pytest_plugins = [
    "df_test_framework.testing.fixtures.core",
    "df_test_framework.testing.fixtures.allure",
]
