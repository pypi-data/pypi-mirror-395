# 快速开始指南

欢迎使用DF Test Framework v2.0！本节将帮助您快速上手。

## 📚 文档列表

1. **[安装指南](installation.md)** - 如何安装和配置框架
   - 系统要求
   - 安装步骤
   - 配置验证

2. **[快速入门](quickstart.md)** - 5分钟上手指南
   - 创建第一个测试
   - 运行测试
   - 查看结果

3. **[30分钟教程](tutorial.md)** - 完整的入门教程
   - 框架核心概念
   - 实战示例
   - 最佳实践

## 🚀 快速开始

### 1. 安装框架

```bash
# 使用uv（推荐）
uv pip install df-test-framework

# 或使用pip
pip install df-test-framework
```

### 2. 创建第一个测试

```python
from df_test_framework import Bootstrap

# 初始化框架
app = Bootstrap().build()
runtime = app.run()

# 使用HTTP客户端
http_client = runtime.http_client()
response = http_client.get("/api/users")

# 断言
assert response.status_code == 200
```

### 3. 下一步

- 查看[完整教程](tutorial.md)了解更多功能
- 浏览[使用示例](../user-guide/examples.md)学习常见模式
- 阅读[架构设计](../architecture/overview.md)深入了解框架

---

**返回**: [文档首页](../README.md)
