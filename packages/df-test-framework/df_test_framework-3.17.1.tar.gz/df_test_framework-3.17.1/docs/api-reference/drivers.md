# Drivers API 参考

> 📖 **能力层2: Drivers** - 会话式交互模式
>
> 适用场景: 浏览器自动化、移动端自动化等需要保持会话状态的交互

---

## 🎯 模块概述

**drivers/** 模块提供会话式交互能力，当前支持:

| 子模块 | 驱动类型 | 实现 | 状态 |
|--------|---------|------|------|
| `drivers/web/playwright/` | Web自动化 | Playwright | ✅ 已实现 |
| `drivers/mobile/appium/` | 移动端自动化 | Appium | 🔄 规划中 |

### 为什么叫"Drivers"？

**命名理念**:
- ✅ **drivers/**: 强调"驱动"外部应用（浏览器/App）
- ✅ **会话式**: 需要维持长时间会话状态
- ❌ 不叫"ui/": UI是前端概念，不准确

**与clients的区别**:
| 维度 | clients/ | drivers/ |
|------|---------|----------|
| 交互模式 | 请求-响应 | 会话式 |
| 状态管理 | 无状态 | 有状态 |
| 典型场景 | API调用 | 浏览器操作 |
| 生命周期 | 短暂 | 长期 |

---

## 📦 导入方式

### 推荐导入（顶层）

```python
from df_test_framework import (
    BrowserManager,
    BasePage,
    ElementLocator,
    LocatorType,
    WaitHelper,
    BrowserType,
)
```

### 完整路径导入

```python
from df_test_framework.drivers.web.playwright import (
    BrowserManager,
    BasePage,
    ElementLocator,
)
```

---

## 🌐 BrowserManager - 浏览器管理器

### 功能特性

- ✅ 基于Playwright实现
- ✅ 支持Chromium、Firefox、WebKit
- ✅ 自动启动和关闭浏览器
- ✅ 上下文管理
- ✅ 页面管理
- ✅ 截图和录制

### 快速开始

```python
from df_test_framework import BrowserManager, BrowserType

# 创建浏览器管理器
browser_mgr = BrowserManager(
    browser_type=BrowserType.CHROMIUM,
    headless=False
)

# 启动浏览器
browser_mgr.start()

# 创建页面
page = browser_mgr.new_page()
page.goto("https://example.com")

# 操作页面
page.fill("#username", "zhangsan")
page.click("button[type='submit']")

# 截图
page.screenshot(path="screenshot.png")

# 关闭浏览器
browser_mgr.close()
```

### 核心方法

#### 生命周期管理
- `start()` - 启动浏览器
- `close()` - 关闭浏览器
- `new_page()` - 创建新页面
- `new_context(**kwargs)` - 创建新上下文

#### 页面管理
- `get_page(index=0)` - 获取页面
- `get_pages()` - 获取所有页面
- `close_page(page)` - 关闭页面

### 配置选项

```python
browser_mgr = BrowserManager(
    browser_type=BrowserType.CHROMIUM,  # 浏览器类型
    headless=False,                      # 是否无头模式
    slow_mo=0,                          # 操作延迟（ms）
    viewport={"width": 1920, "height": 1080},  # 视口大小
    locale="zh-CN",                     # 语言
    timezone_id="Asia/Shanghai",        # 时区
)
```

---

## 📄 BasePage - 页面对象基类

### 功能特性

- ✅ Page Object模式封装
- ✅ 元素定位封装
- ✅ 等待机制
- ✅ 截图和日志

### 快速开始

```python
from df_test_framework import BasePage, ElementLocator, LocatorType

class LoginPage(BasePage):
    """登录页面"""

    def __init__(self, page):
        super().__init__(page)
        self.username_input = ElementLocator(LocatorType.CSS, "#username")
        self.password_input = ElementLocator(LocatorType.CSS, "#password")
        self.submit_button = ElementLocator(LocatorType.CSS, "button[type='submit']")

    def login(self, username: str, password: str):
        """执行登录"""
        self.page.goto("https://example.com/login")
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.submit_button)

    def is_login_successful(self) -> bool:
        """检查登录是否成功"""
        return self.is_visible(ElementLocator(LocatorType.CSS, ".dashboard"))

# 使用
browser_mgr = BrowserManager()
browser_mgr.start()
page = browser_mgr.new_page()

login_page = LoginPage(page)
login_page.login("zhangsan", "password123")
assert login_page.is_login_successful()
```

### 核心方法

#### 导航方法
- `goto(url)` - 导航到URL
- `go_back()` - 后退
- `go_forward()` - 前进
- `reload()` - 刷新

#### 元素操作
- `click(locator)` - 点击元素
- `fill(locator, value)` - 填充输入框
- `select(locator, value)` - 选择下拉框
- `check(locator)` - 勾选复选框
- `uncheck(locator)` - 取消勾选

#### 元素查询
- `is_visible(locator)` - 是否可见
- `is_enabled(locator)` - 是否可用
- `is_checked(locator)` - 是否已勾选
- `get_text(locator)` - 获取文本
- `get_attribute(locator, name)` - 获取属性

#### 等待方法
- `wait_for_selector(locator, timeout=30000)` - 等待元素出现
- `wait_for_url(url, timeout=30000)` - 等待URL
- `wait_for_load_state(state="load")` - 等待加载状态

#### 截图方法
- `screenshot(path=None)` - 截图
- `screenshot_element(locator, path)` - 元素截图

---

## 🔍 ElementLocator - 元素定位器

### 功能特性

- ✅ 统一的定位器封装
- ✅ 支持多种定位策略
- ✅ 类型安全

### 定位类型

```python
from df_test_framework import LocatorType

# CSS选择器
locator = ElementLocator(LocatorType.CSS, "#username")

# XPath
locator = ElementLocator(LocatorType.XPATH, "//input[@id='username']")

# 文本
locator = ElementLocator(LocatorType.TEXT, "登录")

# 测试ID
locator = ElementLocator(LocatorType.TEST_ID, "login-button")

# 角色
locator = ElementLocator(LocatorType.ROLE, "button")
```

### 支持的定位类型

- `CSS` - CSS选择器
- `XPATH` - XPath表达式
- `TEXT` - 文本内容
- `TEST_ID` - data-testid属性
- `ROLE` - ARIA角色
- `LABEL` - Label标签
- `PLACEHOLDER` - Placeholder文本

---

## ⏱️ WaitHelper - 等待助手

### 功能特性

- ✅ 灵活的等待策略
- ✅ 自定义等待条件
- ✅ 超时控制

### 快速开始

```python
from df_test_framework import WaitHelper

# 等待元素可见
WaitHelper.wait_for_visible(page, locator, timeout=10000)

# 等待元素消失
WaitHelper.wait_for_hidden(page, locator, timeout=5000)

# 等待条件满足
def is_ready():
    return page.locator(".loading").count() == 0

WaitHelper.wait_until(is_ready, timeout=30000)
```

### 核心方法

- `wait_for_visible(page, locator, timeout)` - 等待可见
- `wait_for_hidden(page, locator, timeout)` - 等待隐藏
- `wait_for_enabled(page, locator, timeout)` - 等待可用
- `wait_until(condition, timeout, interval)` - 等待条件

---

## 🎯 完整示例

### E2E测试示例

```python
from df_test_framework import BrowserManager, BasePage, ElementLocator, LocatorType
import pytest

class HomePage(BasePage):
    """首页"""

    def __init__(self, page):
        super().__init__(page)
        self.search_input = ElementLocator(LocatorType.CSS, "#search")
        self.search_button = ElementLocator(LocatorType.CSS, "button[type='submit']")

    def search(self, keyword: str):
        """搜索"""
        self.fill(self.search_input, keyword)
        self.click(self.search_button)
        self.wait_for_load_state("networkidle")

class SearchResultsPage(BasePage):
    """搜索结果页"""

    def __init__(self, page):
        super().__init__(page)
        self.results = ElementLocator(LocatorType.CSS, ".search-result")

    def get_result_count(self) -> int:
        """获取结果数量"""
        return self.page.locator(self.results.value).count()

@pytest.fixture
def browser():
    """浏览器fixture"""
    browser_mgr = BrowserManager(headless=True)
    browser_mgr.start()
    yield browser_mgr
    browser_mgr.close()

def test_search_functionality(browser):
    """测试搜索功能"""
    page = browser.new_page()

    # 访问首页
    home_page = HomePage(page)
    home_page.goto("https://example.com")

    # 执行搜索
    home_page.search("pytest")

    # 验证结果
    results_page = SearchResultsPage(page)
    assert results_page.get_result_count() > 0

    # 截图
    results_page.screenshot("search_results.png")
```

---

## 🔗 相关文档

### 架构设计
- [v3架构设计](../architecture/V3_ARCHITECTURE.md) - drivers命名理念
- [会话式交互](../architecture/V3_ARCHITECTURE.md#会话式交互) - 为什么叫drivers

### 其他能力层
- [Clients API](clients.md) - 请求-响应模式
- [Databases API](databases.md) - 数据访问模式

### 测试支持
- [Testing API](testing.md) - UI Fixtures
- [Infrastructure API](infrastructure.md) - UI配置

### 更多资源
- [Playwright官方文档](https://playwright.dev/python/) - Playwright Python API
- [测试最佳实践](../user-guide/testing-best-practices.md) - UI测试最佳实践

---

**返回**: [API参考首页](README.md) | [文档首页](../README.md)
