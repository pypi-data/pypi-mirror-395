# UI测试示例

本目录包含UI自动化测试的完整示例，展示如何使用DF Test Framework进行Web UI测试。

## 📋 示例列表

1. **basic_ui_test.py** - 基础UI测试示例
2. **page_object_example.py** - 页面对象模式示例
3. **advanced_ui_test.py** - 高级UI测试特性

## 🚀 快速开始

### 前提条件

安装Playwright：

```bash
pip install playwright
playwright install
```

### 运行示例

```bash
# 运行所有UI测试
pytest examples/06-ui-testing/

# 运行特定测试
pytest examples/06-ui-testing/basic_ui_test.py

# 显示浏览器（非无头模式）
pytest examples/06-ui-testing/ --headed

# 使用不同浏览器
pytest examples/06-ui-testing/ --browser firefox
```

## 📚 示例说明

### 1. basic_ui_test.py

演示：
- 使用page fixture进行基本测试
- 页面导航和元素操作
- 断言和截图

### 2. page_object_example.py

演示：
- 页面对象模式(POM)实现
- BasePage继承和封装
- 页面对象的测试用例

### 3. advanced_ui_test.py

演示：
- 等待策略
- 多页面操作
- JavaScript执行
- 高级元素定位

## 💡 最佳实践

1. **使用页面对象模式**: 将页面元素和操作封装到Page类中
2. **显式等待**: 使用WaitHelper或BasePage的等待方法
3. **独立测试**: 每个测试应该独立，不依赖其他测试
4. **清晰断言**: 使用清晰的断言消息
5. **截图调试**: 测试失败时自动截图

## 📖 相关文档

- [UI测试用户指南](../../docs/user-guide/ui-testing.md)
- [BasePage API文档](../../docs/api-reference/ui.md)
- [测试类型支持](../../docs/architecture/test-type-support.md#ui测试支持)
