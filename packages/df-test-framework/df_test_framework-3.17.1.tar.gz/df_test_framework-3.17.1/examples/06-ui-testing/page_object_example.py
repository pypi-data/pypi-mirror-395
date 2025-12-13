"""页面对象模式示例

演示如何使用BasePage实现页面对象模式(POM)
"""

import pytest
from df_test_framework.ui import BasePage, WaitHelper

# ========== 页面对象定义 ==========


class GoogleHomePage(BasePage):
    """Google首页"""

    def __init__(self, page):
        super().__init__(page, url="https://www.google.com")

        # 定义页面元素
        self.search_box = '[name="q"]'
        self.search_button = '[name="btnK"]'
        self.feeling_lucky_button = '[name="btnI"]'

    def wait_for_page_load(self):
        """等待页面加载完成"""
        self.wait_for_selector(self.search_box, state="visible")

    def search(self, query: str):
        """
        执行搜索

        Args:
            query: 搜索关键词
        """
        self.fill(self.search_box, query)
        self.page.keyboard.press("Enter")

        # 返回搜索结果页
        return GoogleSearchResultsPage(self.page)

    def is_search_box_visible(self) -> bool:
        """检查搜索框是否可见"""
        return self.is_visible(self.search_box)


class GoogleSearchResultsPage(BasePage):
    """Google搜索结果页"""

    def __init__(self, page):
        super().__init__(page)

        # 定义页面元素
        self.results_container = "#search"
        self.result_items = ".g"
        self.search_box = '[name="q"]'

    def wait_for_page_load(self):
        """等待搜索结果加载"""
        self.wait_for_selector(self.results_container, state="visible")

    def get_results_count(self) -> int:
        """获取搜索结果数量"""
        return self.count(self.result_items)

    def get_search_query(self) -> str:
        """获取搜索关键词"""
        return self.get_value(self.search_box)

    def has_results(self) -> bool:
        """检查是否有搜索结果"""
        return self.get_results_count() > 0


class ExampleDomainPage(BasePage):
    """Example.com示例页面"""

    def __init__(self, page):
        super().__init__(page, url="https://example.com")

        # 定义页面元素
        self.heading = "h1"
        self.description = "p"
        self.more_info_link = 'a[href*="iana"]'

    def wait_for_page_load(self):
        """等待页面加载完成"""
        self.wait_for_selector(self.heading, state="visible")

    def get_heading_text(self) -> str:
        """获取标题文本"""
        return self.get_text(self.heading)

    def get_description_text(self) -> str:
        """获取描述文本"""
        return self.get_text(self.description)

    def click_more_info(self):
        """点击"More information"链接"""
        self.click(self.more_info_link)

    def has_more_info_link(self) -> bool:
        """检查是否有"More information"链接"""
        return self.is_visible(self.more_info_link)


# ========== 测试用例 ==========


class TestPageObjectPattern:
    """页面对象模式测试"""

    def test_google_search(self, page):
        """测试Google搜索"""
        # 创建首页对象
        home_page = GoogleHomePage(page)

        # 导航到首页
        home_page.goto()

        # 验证搜索框可见
        assert home_page.is_search_box_visible()

        # 执行搜索
        results_page = home_page.search("Playwright Python")

        # 验证搜索结果页加载
        assert results_page.has_results()
        assert results_page.get_search_query() == "Playwright Python"

        # 截图
        results_page.screenshot("search_results.png")

    def test_example_domain_page(self, page):
        """测试Example.com页面"""
        # 创建页面对象
        example_page = ExampleDomainPage(page)

        # 导航到页面
        example_page.goto()

        # 验证页面内容
        assert "Example Domain" in example_page.get_heading_text()
        assert len(example_page.get_description_text()) > 0

        # 验证链接存在
        assert example_page.has_more_info_link()

    def test_page_navigation(self, page):
        """测试页面导航"""
        # 创建页面对象
        example_page = ExampleDomainPage(page)

        # 导航到页面
        example_page.goto()

        # 验证URL
        assert "example.com" in example_page.current_url

        # 验证标题
        assert "Example Domain" in example_page.title


class TestWithWaitHelper:
    """使用WaitHelper的测试"""

    def test_wait_for_elements(self, page):
        """测试等待元素"""
        # 创建等待助手
        wait = WaitHelper(page, default_timeout=30000)

        # 访问页面
        page.goto("https://example.com")

        # 等待元素可见
        wait.for_visible("h1")

        # 等待页面加载完成
        wait.for_load_state("networkidle")

        # 验证页面标题
        wait.for_title("Example Domain")

    def test_wait_for_url(self, page):
        """测试等待URL"""
        wait = WaitHelper(page)

        page.goto("https://example.com")

        # 等待URL包含特定字符串
        wait.for_url_contains("example")

    def test_wait_for_text(self, page):
        """测试等待文本"""
        wait = WaitHelper(page)

        page.goto("https://example.com")

        # 等待包含特定文本的元素可见
        wait.for_text_visible("Example Domain")


class TestAdvancedPageObject:
    """高级页面对象测试"""

    def test_page_interaction_chain(self, page):
        """测试页面交互链"""
        # 创建页面对象
        example_page = ExampleDomainPage(page)

        # 链式操作
        example_page.goto()
        example_page.wait_for_page_load()

        # 滚动到底部
        example_page.scroll_to_bottom()

        # 等待
        example_page.wait_for_timeout(1000)

        # 滚动到顶部
        example_page.scroll_to_top()

    def test_element_state_check(self, page):
        """测试元素状态检查"""
        example_page = ExampleDomainPage(page)
        example_page.goto()

        # 检查元素可见性
        assert example_page.is_visible(example_page.heading)

        # 检查元素可用性
        if example_page.has_more_info_link():
            assert example_page.is_enabled(example_page.more_info_link)

    def test_javascript_execution(self, page):
        """测试JavaScript执行"""
        example_page = ExampleDomainPage(page)
        example_page.goto()

        # 执行JavaScript获取信息
        page_height = example_page.evaluate("document.body.scrollHeight")
        assert page_height > 0

        # 修改页面元素
        example_page.evaluate(
            """
            document.querySelector('h1').style.color = 'red';
        """
        )


class TestMultiplePages:
    """多页面测试"""

    def test_switch_between_pages(self, context):
        """测试在多个页面间切换"""
        # 创建多个页面
        page1 = context.new_page()
        page2 = context.new_page()

        # 不同页面加载不同内容
        example_page1 = ExampleDomainPage(page1)
        example_page1.goto()

        google_page = GoogleHomePage(page2)
        google_page.goto()

        # 验证两个页面
        assert "example.com" in example_page1.current_url
        assert "google.com" in google_page.current_url

        # 关闭页面
        page1.close()
        page2.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
