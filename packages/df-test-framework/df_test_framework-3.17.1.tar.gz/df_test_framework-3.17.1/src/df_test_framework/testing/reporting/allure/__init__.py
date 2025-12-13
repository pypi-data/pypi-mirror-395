"""Allure 测试报告集成

提供零配置的 Allure 测试报告功能：
- AllureObserver - 观察者模式，自动记录测试操作
- AllureHelper - 工具类，手动添加附件和步骤
- Fixtures - pytest fixtures，自动注入

使用方式：
    # 完全自动，无需任何配置
    def test_api(http_client):
        response = http_client.post("/api/users", json={"name": "Alice"})
        assert response.status_code == 201

    # 生成报告
    # pytest --alluredir=./allure-results
    # allure serve ./allure-results

手动添加附件：
    from df_test_framework.testing.reporting.allure import attach_json

    def test_api(http_client):
        attach_json({"custom": "data"}, name="自定义数据")
"""

from .helper import (
    AllureHelper,
    attach_json,
    attach_log,
    attach_screenshot,
    step,
)
from .observer import (
    ALLURE_AVAILABLE,
    AllureObserver,
    get_current_observer,
    is_allure_enabled,
    set_current_observer,
)

__all__ = [
    # Observer
    "AllureObserver",
    "get_current_observer",
    "set_current_observer",
    "ALLURE_AVAILABLE",
    "is_allure_enabled",
    # Helper
    "AllureHelper",
    "attach_log",
    "attach_json",
    "attach_screenshot",
    "step",
]
