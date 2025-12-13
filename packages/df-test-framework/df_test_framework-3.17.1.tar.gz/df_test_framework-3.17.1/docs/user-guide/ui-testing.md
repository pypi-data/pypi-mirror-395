# UI测试指南

本文档介绍如何使用DF Test Framework进行Web UI自动化测试。

## 📋 目录

- [快速开始](#快速开始)
- [浏览器管理](#浏览器管理)
- [页面对象模式](#页面对象模式)
- [元素定位](#元素定位)
- [等待策略](#等待策略)
- [测试Fixtures](#测试fixtures)
- [最佳实践](#最佳实践)

## 🚀 快速开始

### 安装依赖

```bash
# 安装Playwright
pip install playwright

# 安装浏览器驱动
playwright install
```

### 第一个UI测试

```python
def test_first_ui_test(page):
    """最简单的UI测试"""
    # 访问页面
    page.goto("https://example.com")

    # 验证标题
    assert page.title() == "Example Domain"

    # 查找元素并验证
    heading = page.locator("h1")
    assert "Example Domain" in heading.text_content()
```

运行测试：

```bash
pytest your_test.py
```

## 🌐 浏览器管理

### 使用BrowserManager

```python
from df_test_framework.ui import BrowserManager, BrowserType

# 创建浏览器管理器
manager = BrowserManager(
    browser_type=BrowserType.CHROMIUM,
    headless=True,
    timeout=30000,
    viewport={"width": 1920, "height": 1080}
)

# 启动浏览器
browser, context, page = manager.start()

# 使用页面
page.goto("https://example.com")

# 关闭浏览器
manager.stop()
```

### 使用上下文管理器

```python
with BrowserManager() as (browser, context, page):
    page.goto("https://example.com")
    # 自动清理资源
```

### 支持的浏览器

```python
from df_test_framework.ui import BrowserType

# Chromium（推荐）
BrowserType.CHROMIUM

# Firefox
BrowserType.FIREFOX

# WebKit (Safari引擎)
BrowserType.WEBKIT
```

## 📄 页面对象模式

### 创建页面对象

```python
from df_test_framework.ui import BasePage

class LoginPage(BasePage):
    """登录页面对象"""

    def __init__(self, page):
        super().__init__(page, url="/login")

        # 定义页面元素
        self.username_input = "#username"
        self.password_input = "#password"
        self.login_button = "button[type='submit']"
        self.error_message = ".error-message"

    def wait_for_page_load(self):
        """等待页面加载完成"""
        self.wait_for_selector(self.login_button)

    def login(self, username: str, password: str):
        """执行登录"""
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.login_button)

    def get_error_message(self) -> str:
        """获取错误消息"""
        if self.is_visible(self.error_message):
            return self.get_text(self.error_message)
        return ""

    def is_error_displayed(self) -> bool:
        """检查是否显示错误"""
        return self.is_visible(self.error_message)
```

### 使用页面对象

```python
def test_login_success(page):
    """测试成功登录"""
    # 创建页面对象
    login_page = LoginPage(page)

    # 导航到登录页
    login_page.goto()

    # 执行登录
    login_page.login("testuser", "password123")

    # 验证跳转
    login_page.wait_for_url("**/dashboard")

def test_login_with_invalid_credentials(page):
    """测试无效凭证登录"""
    login_page = LoginPage(page)
    login_page.goto()

    login_page.login("invalid", "invalid")

    # 验证错误消息
    assert login_page.is_error_displayed()
    assert "Invalid credentials" in login_page.get_error_message()
```

### BasePage提供的方法

#### 页面导航

```python
# 导航到页面
page_object.goto("/path")

# 刷新页面
page_object.reload()

# 返回/前进
page_object.go_back()
page_object.go_forward()
```

#### 元素操作

```python
# 点击
page_object.click("#submit-btn")

# 填充输入框
page_object.fill("#input", "value")

# 选择下拉框
page_object.select_option("select", "option1")

# 勾选复选框
page_object.check("#checkbox")
page_object.uncheck("#checkbox")

# 鼠标悬停
page_object.hover("#menu-item")
```

#### 元素查询

```python
# 获取文本
text = page_object.get_text("h1")

# 获取属性
href = page_object.get_attribute("a", "href")

# 获取输入框值
value = page_object.get_value("#input")

# 检查元素状态
is_visible = page_object.is_visible("#element")
is_enabled = page_object.is_enabled("#button")
is_checked = page_object.is_checked("#checkbox")
```

#### 等待策略

```python
# 等待元素出现
page_object.wait_for_selector("#element", state="visible")

# 等待URL变化
page_object.wait_for_url("**/dashboard")

# 等待页面加载状态
page_object.wait_for_load_state("networkidle")
```

#### 截图

```python
# 全页面截图
page_object.screenshot("page.png")

# 元素截图
page_object.screenshot_element("#element", "element.png")
```

## 🎯 元素定位

### 多种定位方式

```python
from df_test_framework.ui import BasePage

class MyPage(BasePage):
    def demo_locators(self):
        # CSS选择器
        element = self.locator("#id")
        element = self.locator(".class")

        # 通过文本
        button = self.get_by_text("Click me")

        # 通过role
        link = self.get_by_role("link", name="Home")

        # 通过label
        input_field = self.get_by_label("Username")

        # 通过placeholder
        search = self.get_by_placeholder("Search...")

        # 通过test-id
        btn = self.get_by_test_id("submit-button")
```

### 使用ElementLocator

```python
from df_test_framework.ui import ElementLocator

# 创建定位器
username_locator = ElementLocator.id("username")
submit_locator = ElementLocator.css("button[type='submit']")
link_locator = ElementLocator.text("Click here")

# 在页面中使用
element = username_locator.get_locator(page)
element.fill("testuser")
```

## ⏰ 等待策略

### 使用WaitHelper

```python
from df_test_framework.ui import WaitHelper

def test_with_wait_helper(page):
    wait = WaitHelper(page, default_timeout=30000)

    page.goto("https://example.com")

    # 等待元素可见
    wait.for_visible("#submit-button")

    # 等待URL包含特定字符串
    wait.for_url_contains("/dashboard")

    # 等待标题
    wait.for_title("Dashboard")

    # 等待网络空闲
    wait.for_network_idle()

    # 等待文本出现
    wait.for_text_visible("Welcome")

    # 等待元素数量
    wait.for_count(".item", 5)
```

### 等待自定义条件

```python
def test_custom_wait(page):
    wait = WaitHelper(page)

    # 等待自定义条件
    result = wait.for_condition(
        lambda: page.locator(".item").count() > 10,
        timeout=5000
    )
```

## 🧪 测试Fixtures

### 使用内置Fixtures

```python
# page fixture - 最常用
def test_with_page(page):
    page.goto("https://example.com")
    assert page.title() == "Example Domain"

# context fixture - 需要多页面
def test_multiple_pages(context):
    page1 = context.new_page()
    page2 = context.new_page()

    page1.goto("https://example.com")
    page2.goto("https://google.com")

# browser fixture - 需要浏览器级别操作
def test_with_browser(browser):
    context = browser.new_context()
    page = context.new_page()
    # ...

# browser_manager fixture - 完整管理器
def test_with_manager(browser_manager):
    page = browser_manager.page
    page.goto("https://example.com")
```

### 便捷Fixtures

```python
# goto fixture
def test_with_goto(goto):
    page = goto("https://example.com")
    assert page.title() == "Example Domain"

# screenshot fixture
def test_with_screenshot(page, screenshot):
    page.goto("https://example.com")
    screenshot("example.png")
```

### 自定义配置

在`conftest.py`中重写配置fixtures：

```python
import pytest
from df_test_framework.ui import BrowserType

@pytest.fixture(scope="session")
def browser_type():
    """使用Firefox浏览器"""
    return BrowserType.FIREFOX

@pytest.fixture(scope="session")
def browser_headless():
    """显示浏览器窗口"""
    return False

@pytest.fixture(scope="session")
def browser_viewport():
    """设置1920x1080分辨率"""
    return {"width": 1920, "height": 1080}

@pytest.fixture(scope="session")
def browser_timeout():
    """设置60秒超时"""
    return 60000
```

### 命令行选项

```bash
# 显示浏览器
pytest --headed

# 选择浏览器
pytest --browser firefox

# 操作延迟（调试用）
pytest --slowmo 1000
```

## 💡 最佳实践

### 1. 使用页面对象模式

**推荐** ✅:
```python
class ProductPage(BasePage):
    def add_to_cart(self, product_id):
        self.click(f"#product-{product_id} .add-to-cart")
        self.wait_for_text_visible("Added to cart")

def test_add_product(page):
    product_page = ProductPage(page)
    product_page.goto()
    product_page.add_to_cart(123)
```

**不推荐** ❌:
```python
def test_add_product(page):
    page.goto("/products")
    page.click("#product-123 .add-to-cart")
    # ...
```

### 2. 显式等待

**推荐** ✅:
```python
page.wait_for_selector("#result", state="visible")
result = page.locator("#result").text_content()
```

**不推荐** ❌:
```python
import time
time.sleep(2)  # 固定等待
result = page.locator("#result").text_content()
```

### 3. 独立测试

**推荐** ✅:
```python
def test_login(page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("user", "pass")
    # 完整的独立测试

def test_checkout(page):
    # 每个测试独立设置数据
    setup_test_user()
    login_page = LoginPage(page)
    # ...
```

**不推荐** ❌:
```python
# 依赖其他测试的状态
def test_1_login(page):
    # ...

def test_2_add_to_cart(page):
    # 依赖test_1的登录状态
    # ...
```

### 4. 清晰的元素定位

**推荐** ✅:
```python
# 使用data-testid
<button data-testid="submit-btn">Submit</button>

page.get_by_test_id("submit-btn").click()
```

**不推荐** ❌:
```python
# 使用脆弱的选择器
page.click("body > div > div.container > button:nth-child(3)")
```

### 5. 失败自动截图

在`conftest.py`中配置：

```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            page.screenshot(path=f"screenshots/{item.name}_failure.png")
```

## 🔧 常见场景

### 登录测试

```python
class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page, url="/login")
        self.username = "#username"
        self.password = "#password"
        self.submit = "button[type='submit']"

    def wait_for_page_load(self):
        self.wait_for_selector(self.submit)

    def login(self, username, password):
        self.fill(self.username, username)
        self.fill(self.password, password)
        self.click(self.submit)

def test_successful_login(page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("testuser", "password123")

    # 验证登录成功
    page.wait_for_url("**/dashboard")
    assert "Dashboard" in page.title()
```

### 表单填写测试

```python
def test_submit_form(page):
    form_page = FormPage(page)
    form_page.goto()

    # 填写表单
    form_page.fill_text_field("name", "John Doe")
    form_page.select_dropdown("country", "US")
    form_page.check_checkbox("terms")
    form_page.submit()

    # 验证提交成功
    assert form_page.is_success_message_displayed()
```

### 多步骤流程测试

```python
def test_checkout_flow(page):
    # 步骤1: 登录
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("user", "pass")

    # 步骤2: 添加商品
    product_page = ProductPage(page)
    product_page.goto()
    product_page.add_to_cart(product_id=123)

    # 步骤3: 结账
    cart_page = CartPage(page)
    cart_page.goto()
    cart_page.proceed_to_checkout()

    # 步骤4: 验证订单
    checkout_page = CheckoutPage(page)
    checkout_page.fill_shipping_info(...)
    checkout_page.complete_order()

    # 验证
    assert checkout_page.is_order_confirmed()
```

## 🔗 相关资源

- [BasePage API文档](../api-reference/ui.md)
- [测试类型支持](../architecture/test-type-support.md#ui测试支持)
- [UI测试示例](../../examples/06-ui-testing/)
- [Playwright官方文档](https://playwright.dev/python/)

---

**返回**: [用户指南首页](README.md) | [文档首页](../README.md)
