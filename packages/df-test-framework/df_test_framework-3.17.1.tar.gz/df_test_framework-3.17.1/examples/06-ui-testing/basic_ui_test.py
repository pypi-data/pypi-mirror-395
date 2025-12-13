"""基础UI测试示例

演示如何使用DF Test Framework进行Web UI测试
"""

import pytest


class TestBasicUI:
    """基础UI测试示例"""

    def test_page_navigation(self, page):
        """测试页面导航"""
        # 访问网页
        page.goto("https://example.com")

        # 验证页面标题
        assert page.title() == "Example Domain"

        # 验证URL
        assert "example.com" in page.url

    def test_element_interaction(self, page):
        """测试元素交互"""
        page.goto("https://www.google.com")

        # 查找搜索框
        search_box = page.locator('[name="q"]')

        # 输入文本
        search_box.fill("Playwright")

        # 验证输入值
        assert search_box.input_value() == "Playwright"

    def test_element_click(self, page):
        """测试元素点击"""
        page.goto("https://example.com")

        # 查找链接并点击
        link = page.get_by_text("More information")

        if link.is_visible():
            # 点击前截图
            page.screenshot(path="before_click.png")

            link.click()

            # 等待页面加载
            page.wait_for_load_state("networkidle")

            # 点击后截图
            page.screenshot(path="after_click.png")

    def test_wait_for_element(self, page):
        """测试等待元素"""
        page.goto("https://example.com")

        # 等待元素出现
        page.wait_for_selector("h1", state="visible")

        # 获取元素文本
        heading = page.locator("h1")
        assert "Example Domain" in heading.text_content()

    def test_multiple_elements(self, page):
        """测试多个元素"""
        page.goto("https://example.com")

        # 查找所有段落
        paragraphs = page.locator("p")

        # 验证段落数量
        count = paragraphs.count()
        assert count > 0

        # 遍历段落
        for i in range(count):
            p = paragraphs.nth(i)
            print(f"段落 {i + 1}: {p.text_content()}")

    def test_screenshot(self, page):
        """测试截图功能"""
        page.goto("https://example.com")

        # 全页面截图
        page.screenshot(path="full_page.png", full_page=True)

        # 元素截图
        heading = page.locator("h1")
        heading.screenshot(path="heading.png")

    def test_execute_javascript(self, page):
        """测试执行JavaScript"""
        page.goto("https://example.com")

        # 执行JavaScript
        title = page.evaluate("() => document.title")
        assert title == "Example Domain"

        # 滚动到底部
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    def test_get_attribute(self, page):
        """测试获取元素属性"""
        page.goto("https://example.com")

        # 获取链接的href属性
        link = page.get_by_text("More information")

        if link.is_visible():
            href = link.get_attribute("href")
            assert href is not None
            print(f"链接地址: {href}")


class TestFormInteraction:
    """表单交互测试"""

    def test_input_field(self, page):
        """测试输入框"""
        page.goto("https://www.google.com")

        # 填充输入框
        page.fill('[name="q"]', "Test Framework")

        # 清空输入框
        page.fill('[name="q"]', "")

        # 逐字输入（模拟键盘）
        page.type('[name="q"]', "Python", delay=100)

    def test_checkbox(self, page):
        """测试复选框（示例）"""
        # 注意: 这个示例需要实际的表单页面
        # page.goto("https://your-form-url.com")

        # 勾选复选框
        # page.check("#agree-checkbox")

        # 验证已勾选
        # assert page.is_checked("#agree-checkbox")

        # 取消勾选
        # page.uncheck("#agree-checkbox")

        # 验证未勾选
        # assert not page.is_checked("#agree-checkbox")
        pass

    def test_dropdown(self, page):
        """测试下拉框（示例）"""
        # 注意: 这个示例需要实际的表单页面
        # page.goto("https://your-form-url.com")

        # 选择下拉框选项
        # page.select_option("select#country", "CN")

        # 或通过label选择
        # page.select_option("select#country", label="China")
        pass


class TestAdvancedFeatures:
    """高级特性测试"""

    def test_hover(self, page):
        """测试鼠标悬停"""
        page.goto("https://example.com")

        # 悬停到元素上
        heading = page.locator("h1")
        heading.hover()

    def test_double_click(self, page):
        """测试双击（示例）"""
        # page.goto("https://your-url.com")
        # page.dblclick("#element")
        pass

    def test_drag_and_drop(self, page):
        """测试拖放（示例）"""
        # page.goto("https://your-url.com")
        # page.drag_and_drop("#source", "#target")
        pass

    def test_multiple_pages(self, context):
        """测试多页面"""
        # 创建第一个页面
        page1 = context.new_page()
        page1.goto("https://example.com")

        # 创建第二个页面
        page2 = context.new_page()
        page2.goto("https://www.google.com")

        # 在不同页面间切换
        assert "example.com" in page1.url
        assert "google.com" in page2.url

        # 关闭页面
        page1.close()
        page2.close()

    def test_wait_for_url_change(self, page):
        """测试等待URL变化"""
        page.goto("https://example.com")

        # 点击链接
        link = page.get_by_text("More information")

        if link.is_visible():
            with page.expect_navigation():
                link.click()

            # URL已改变
            assert page.url != "https://example.com"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
