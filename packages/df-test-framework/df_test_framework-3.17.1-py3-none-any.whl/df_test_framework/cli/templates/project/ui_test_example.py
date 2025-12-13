"""UI测试示例模板"""

UI_TEST_EXAMPLE_TEMPLATE = """\"\"\"UI测试示例

演示如何使用页面对象模式进行UI测试。
\"\"\"

import pytest
from {project_name}.pages.home_page import HomePage


class TestHomePage:
    \"\"\"首页测试\"\"\"

    @pytest.mark.ui
    def test_page_title(self, page, base_url):
        \"\"\"测试页面标题\"\"\"
        # 创建页面对象
        home_page = HomePage(page, base_url=base_url)

        # 导航到页面
        home_page.goto()

        # 验证页面标题
        assert home_page.title != ""

        # 截图
        home_page.screenshot("reports/screenshots/homepage.png")

    @pytest.mark.ui
    def test_page_elements(self, page, base_url):
        \"\"\"测试页面元素\"\"\"
        home_page = HomePage(page, base_url=base_url)
        home_page.goto()

        # 验证元素可见
        assert home_page.is_visible(home_page.heading)

        # 获取元素文本
        heading_text = home_page.get_text(home_page.heading)
        assert len(heading_text) > 0


__all__ = ["TestHomePage"]
"""

__all__ = ["UI_TEST_EXAMPLE_TEMPLATE"]
