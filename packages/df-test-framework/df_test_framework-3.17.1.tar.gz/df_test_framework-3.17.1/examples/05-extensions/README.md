# 扩展系统示例

本目录包含DF Test Framework v2.0扩展系统的各种实用示例，展示如何创建和使用自定义扩展。

> 📚 **相关文档**: [扩展系统使用指南](../../docs/user-guide/extensions.md)

---

## 📋 示例列表

### 1. custom_extension.py - 基础扩展示例
**难度**: ⭐ 入门

演示扩展系统的基本概念和用法。

**包含内容**:
- 请求日志扩展
- 性能追踪扩展
- 请求验证扩展
- 缓存扩展
- 错误处理扩展
- 多个扩展组合使用

**适合人群**: 初学者，快速了解扩展系统

**运行示例**:
```bash
python examples/05-extensions/custom_extension.py
```

**学习要点**:
- 使用 `@hookimpl` 装饰器
- 实现 `before_http_request` 和 `after_http_response` Hook
- 组合多个扩展

---

### 2. monitoring_extension.py - 监控扩展示例 ⭐ 新增
**难度**: ⭐⭐ 中级

演示如何创建生产级的监控扩展，追踪API性能和数据库慢查询。

**包含内容**:
- APIPerformanceTracker - API性能追踪器
- DatabaseMonitor - 数据库慢查询监控
- 性能统计报告
- 慢查询报告

**适合人群**: 需要监控测试性能的QA工程师

**运行示例**:
```bash
python examples/05-extensions/monitoring_extension.py
```

**学习要点**:
- 实现 `df_providers` Hook注册Provider
- 实现 `df_post_bootstrap` Hook进行初始化
- 使用SingletonProvider管理生命周期
- 生成详细的性能统计报告

**关键特性**:
- ⏱️ 自动追踪API调用耗时
- ⚠️ 检测超过阈值的慢请求
- 📊 生成详细的统计报告
- 🔍 监控数据库慢查询

---

### 3. data_factory_extension.py - 测试数据工厂扩展 ⭐ 新增
**难度**: ⭐⭐ 中级

演示如何创建测试数据工厂，快速生成各种业务测试数据。

**包含内容**:
- 用户数据生成（使用Faker）
- 订单数据生成
- 商品数据生成
- 评论、支付、地址数据
- 完整业务场景数据

**适合人群**: 需要快速准备测试数据的测试工程师

**运行示例**:
```bash
pip install faker  # 首次需要安装faker
python examples/05-extensions/data_factory_extension.py
```

**学习要点**:
- 使用Faker库生成随机数据
- 支持字段覆盖（**overrides）
- 批量创建数据
- 创建完整业务场景数据

**使用场景**:
- 🏭 快速生成大量测试数据
- 🎲 数据随机化但可重现（固定种子）
- 🔧 灵活覆盖特定字段
- 📦 创建完整业务流程数据

---

### 4. environment_validator_extension.py - 环境验证扩展 ⭐ 新增
**难度**: ⭐⭐⭐ 高级

演示如何创建环境验证扩展，确保测试环境符合要求。

**包含内容**:
- 环境变量验证
- Python版本验证
- 网络连通性验证
- 数据库连接验证
- Redis连接验证
- 条件验证（根据环境类型）

**适合人群**: DevOps工程师，需要确保环境一致性

**运行示例**:
```bash
python examples/05-extensions/environment_validator_extension.py
```

**学习要点**:
- 在 `df_post_bootstrap` Hook中执行验证
- 验证失败时中断测试（sys.exit）
- 记录详细的验证日志
- 根据环境类型执行不同验证

**验证项目**:
- ✅ 必需的环境变量
- ✅ Python版本检查
- ✅ 网络连通性检查
- ✅ 数据库/Redis连接检查
- ✅ 服务健康检查

---

## 🚀 快速开始

### 前置条件

```bash
# 确保已安装框架
pip install df-test-framework

# 部分示例需要额外依赖
pip install faker  # data_factory_extension.py需要
```

### 运行所有示例

```bash
# 1. 基础扩展
python examples/05-extensions/custom_extension.py

# 2. 监控扩展
python examples/05-extensions/monitoring_extension.py

# 3. 数据工厂
pip install faker
python examples/05-extensions/data_factory_extension.py

# 4. 环境验证
python examples/05-extensions/environment_validator_extension.py
```

---

## 📖 扩展开发最佳实践

### 1. 选择合适的Hook点

框架提供3个Hook点：

| Hook | 触发时机 | 使用场景 |
|------|---------|---------|
| `df_config_sources` | 配置加载前 | 添加远程配置源、自定义配置 |
| `df_providers` | Runtime组装时 | 注册自定义服务、Provider |
| `df_post_bootstrap` | Runtime创建后 | 环境验证、初始化、注册pytest插件 |

### 2. 扩展命名规范

```python
# ✅ 好的命名
my_project.extensions.monitoring
my_project.extensions.data_factory

# ❌ 不好的命名
my_project.ext
my_project.plugin1
```

### 3. 使用Provider管理资源

```python
from df_test_framework.infrastructure.providers import SingletonProvider

@hookimpl
def df_providers(settings, logger):
    return {
        # 单例Provider - 整个测试会话只创建一次
        "my_service": SingletonProvider(
            lambda ctx: MyService(settings.api_url)
        )
    }
```

### 4. 优雅的错误处理

```python
@hookimpl
def df_post_bootstrap(self, runtime):
    try:
        self._validate(runtime)
    except Exception as e:
        runtime.logger.error("=" * 60)
        runtime.logger.error(f"验证失败: {e}")
        runtime.logger.error("请检查环境配置")
        runtime.logger.error("=" * 60)
        sys.exit(1)
```

---

## 🎯 实战应用

### 场景1: 性能监控

```python
# 1. 在conftest.py中注册监控扩展
from examples.extensions.monitoring_extension import MonitoringExtension

@pytest.fixture(scope="session")
def runtime():
    monitoring = MonitoringExtension(slow_api_threshold_ms=300)
    return (
        Bootstrap()
        .with_settings(MySettings)
        .with_extensions([monitoring])
        .build()
        .run()
    )

# 2. 在测试中使用
def test_api(runtime):
    tracker = runtime.get("api_performance_tracker")

    tracker.start_tracking("用户登录")
    response = http.post("/login", ...)
    tracker.end_tracking("用户登录")

    # 测试结束后查看报告
    tracker.print_stats()
```

### 场景2: 测试数据准备

```python
# 1. 注册数据工厂
from examples.extensions.data_factory_extension import DataFactoryExtension

@pytest.fixture(scope="session")
def runtime():
    return (
        Bootstrap()
        .with_settings(MySettings)
        .with_extensions([DataFactoryExtension()])
        .build()
        .run()
    )

# 2. 在测试中使用
def test_create_user(runtime):
    factory = runtime.get("data_factory")

    # 快速生成测试数据
    user_data = factory.create_user(age=25, city="北京")

    # 调用API
    response = http.post("/users", json=user_data)
    assert response.status_code == 201
```

### 场景3: 环境验证

```python
# 1. CI/CD环境中启用验证
from examples.extensions.environment_validator_extension import EnvironmentValidator

@pytest.fixture(scope="session")
def runtime():
    validator = EnvironmentValidator(
        required_envs=["API_KEY", "DATABASE_URL"],
        min_python_version=(3, 10)
    )

    return (
        Bootstrap()
        .with_settings(MySettings)
        .with_extensions([validator])
        .build()
        .run()
    )

# 2. 测试运行前自动验证环境
# 如果验证失败，测试将不会运行
```

---

## 🔗 相关资源

- **📚 用户指南**: [扩展系统使用指南](../../docs/user-guide/extensions.md)
- **📖 API文档**: [Extensions API参考](../../docs/api-reference/extensions.md)
- **🏗️ 架构文档**: [扩展点设计](../../docs/architecture/extension-points.md)
- **🔌 pluggy文档**: [pluggy官方文档](https://pluggy.readthedocs.io/)

---

## 💡 下一步

1. **学习基础**: 从 `custom_extension.py` 开始
2. **实战应用**: 根据需求选择合适的示例
3. **自定义开发**: 参考示例创建自己的扩展
4. **分享复用**: 将通用扩展打包为独立模块

---

## 🤝 贡献

欢迎贡献更多实用的扩展示例！

**建议的新示例**:
- [ ] Allure增强扩展（自动添加环境信息）
- [ ] 消息队列扩展（RabbitMQ/Kafka）
- [ ] UI测试扩展（Selenium/Playwright）
- [ ] 数据库备份/恢复扩展
- [ ] 通知扩展（钉钉/企业微信/Slack）

---

**返回**: [示例代码首页](../README.md) | [文档中心](../../docs/README.md)
