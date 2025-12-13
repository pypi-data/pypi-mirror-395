# 未来 Allure 集成方案规划

> **文档版本**: v1.0
> **创建日期**: 2025-12-08
> **状态**: 📋 规划文档（供将来参考）
> **当前实施**: 方案 A（Fixture 模式）
> **本文档目的**: 记录未来可能的架构演进方向

---

## 📌 当前决策（v3.18.0）

**采用方案 A**：废弃 AllurePlugin，统一使用 Pytest Fixture 模式

**理由**：
- ✅ 符合能力层优化计划的设计意图
- ✅ 当前实现已经完善且运行稳定
- ✅ 简单直接，降低维护成本
- ✅ 测试隔离性强

**实施计划**：
- v3.18.0: 标记 AllurePlugin 为 DEPRECATED
- v4.0.0: 完全移除 AllurePlugin

---

## 🚀 未来演进方案

以下方案记录了框架未来可能的架构演进方向，供将来参考。

### 方案时机判断

| 方案 | 触发条件 | 优先级 |
|------|---------|--------|
| **方案 B** - 两种模式并存 | 出现非 pytest 场景需求 | 中 |
| **方案 C** - 纯 Plugin 模式 | 框架定位转向通用测试平台 | 低 |

---

## 方案 B：两种模式并存（混合架构）

### 适用场景

当框架需要支持以下场景时考虑实施：

1. **非 pytest 场景**
   - 直接运行 Python 脚本（不使用 pytest）
   - 应用程序监控（长期运行的服务）
   - 命令行工具集成

2. **多种报告格式**
   - 同时支持 Allure、JUnit XML、HTML 等
   - 可插拔的报告系统
   - 用户自定义报告格式

3. **企业级灵活性**
   - 不同团队使用不同集成方式
   - 配置驱动的报告选择

### 架构设计

```
┌────────────────────────────────────────────────────┐
│              用户场景决策树                         │
├────────────────────────────────────────────────────┤
│                                                    │
│  使用 pytest？                                      │
│    ├─ 是 ──→ Fixture 模式（自动）                  │
│    │         └─ 测试级 EventBus + AllureObserver   │
│    │                                               │
│    └─ 否 ──→ Plugin 模式（手动）                   │
│              └─ 全局 EventBus + AllurePlugin       │
│                                                    │
└────────────────────────────────────────────────────┘
```

### 核心组件

#### 1. AllurePlugin（通用核心）

```python
# src/df_test_framework/plugins/builtin/reporting/allure_plugin.py

class AllurePlugin:
    """通用 Allure 报告插件（可用于任何场景）"""

    def __init__(self, enabled: bool = True):
        self._enabled = enabled
        self._allure_available = self._check_allure()

    def attach_to_event_bus(self, event_bus: EventBus) -> None:
        """附加到任意 EventBus（测试级或全局）

        这是两种模式的桥接方法。
        """
        if not self._allure_available or not self._enabled:
            return

        # 创建并订阅所有事件处理器
        handlers = self._create_handlers(event_bus)
        # 处理器已通过 @event_bus.on() 装饰器自动注册

    def _create_handlers(self, event_bus: EventBus) -> list:
        """创建所有能力层事件处理器

        支持的事件：
        - HTTP: HttpRequestEndEvent, HttpRequestErrorEvent
        - Database: DatabaseQueryEndEvent, DatabaseQueryErrorEvent
        - Redis: CacheOperationEndEvent, CacheOperationErrorEvent
        - MQ: MessagePublishEvent, MessageConsumeEvent
        - Storage: StorageOperationEndEvent, StorageOperationErrorEvent
        """
        # ... 完整实现（已在当前代码中）

    @hookimpl
    def df_event_handlers(self, event_bus: EventBus) -> list:
        """Pluggy Hook：注册到全局 EventBus"""
        return self._create_handlers(event_bus)
```

#### 2. Pytest Fixture（智能桥接）

```python
# src/df_test_framework/testing/fixtures/allure.py

from df_test_framework.testing.config import AllureIntegrationMode, get_allure_mode

@pytest.fixture(autouse=True)
def _auto_allure_observer(request, runtime):
    """智能 Allure 集成 fixture

    根据配置自动选择集成模式：
    - Plugin 模式：桥接到 AllurePlugin
    - Fixture 模式：创建 AllureObserver（默认）
    """

    # 1. 创建测试级 EventBus（测试隔离）
    test_event_bus = EventBus()
    set_test_event_bus(test_event_bus)

    # 2. 检测集成模式
    mode = get_allure_mode()

    if mode == AllureIntegrationMode.PLUGIN:
        # Plugin 模式：桥接到 AllurePlugin
        allure_plugin = _get_allure_plugin_from_runtime(runtime)
        if allure_plugin:
            # 将 Plugin 连接到测试级 EventBus
            allure_plugin.attach_to_event_bus(test_event_bus)
            observer = None  # Plugin 模式不使用 AllureObserver
        else:
            # 未找到插件，回退到 Fixture 模式
            observer = _create_observer_and_subscribe(test_event_bus, request)
    else:
        # Fixture 模式（默认）：创建 AllureObserver
        observer = _create_observer_and_subscribe(test_event_bus, request)

    yield observer or allure_plugin

    # 3. 清理
    if observer:
        observer.cleanup()
    test_event_bus.clear()
    set_test_event_bus(None)

def _get_allure_plugin_from_runtime(runtime) -> AllurePlugin | None:
    """从 runtime.extensions 获取 AllurePlugin 实例"""
    if not runtime or not hasattr(runtime, 'extensions'):
        return None

    for plugin in runtime.extensions.get_plugins():
        if isinstance(plugin, AllurePlugin):
            return plugin
    return None

def _create_observer_and_subscribe(test_event_bus, request) -> AllureObserver:
    """创建 AllureObserver 并订阅所有事件（Fixture 模式）"""
    observer = AllureObserver(test_name=request.node.name)

    # 订阅所有能力层事件
    test_event_bus.subscribe(HttpRequestEndEvent, observer.handle_http_request_end_event)
    test_event_bus.subscribe(DatabaseQueryEndEvent, observer.handle_database_query_end_event)
    test_event_bus.subscribe(CacheOperationEndEvent, observer.handle_cache_operation_end_event)
    test_event_bus.subscribe(MessagePublishEvent, observer.handle_message_publish_event)
    test_event_bus.subscribe(StorageOperationEndEvent, observer.handle_storage_operation_end_event)
    # ... 订阅其他事件

    return observer
```

#### 3. 模式配置

```python
# src/df_test_framework/testing/config.py

from enum import Enum
import os

class AllureIntegrationMode(Enum):
    """Allure 集成模式"""
    FIXTURE = "fixture"  # 默认：Fixture 模式（测试隔离）
    PLUGIN = "plugin"    # Plugin 模式（通用）
    AUTO = "auto"        # 自动检测

def get_allure_mode() -> AllureIntegrationMode:
    """获取 Allure 集成模式

    优先级：
    1. 环境变量 DF_ALLURE_MODE
    2. pytest.ini 配置 df_allure_mode
    3. 自动检测：如果配置了 df_plugins 包含 allure_plugin，使用 plugin 模式
    4. 默认：fixture 模式
    """
    # 1. 环境变量
    env_mode = os.getenv("DF_ALLURE_MODE", "").lower()
    if env_mode:
        try:
            return AllureIntegrationMode(env_mode)
        except ValueError:
            pass

    # 2. pytest.ini 配置
    config_mode = _read_pytest_config("df_allure_mode")
    if config_mode:
        try:
            return AllureIntegrationMode(config_mode)
        except ValueError:
            pass

    # 3. 自动检测
    if _has_allure_plugin_in_config():
        return AllureIntegrationMode.PLUGIN

    # 4. 默认
    return AllureIntegrationMode.FIXTURE

def _read_pytest_config(key: str) -> str | None:
    """读取 pytest.ini 配置"""
    # 实现省略
    pass

def _has_allure_plugin_in_config() -> bool:
    """检查是否配置了 AllurePlugin"""
    # 检查 pyproject.toml 中的 df_plugins
    # 实现省略
    pass
```

### 用户配置示例

#### 配置 1：使用 Fixture 模式（默认，推荐）

```toml
# pyproject.toml
# 无需任何配置，框架自动使用 Fixture 模式
```

#### 配置 2：使用 Plugin 模式

```toml
# pyproject.toml
[tool.pytest.ini_options]
df_plugins = "df_test_framework.plugins.builtin.reporting.allure_plugin"
df_allure_mode = "plugin"  # 显式指定 Plugin 模式
```

#### 配置 3：环境变量控制

```bash
# 使用 Plugin 模式运行测试
DF_ALLURE_MODE=plugin pytest tests/

# 使用 Fixture 模式运行测试（默认）
DF_ALLURE_MODE=fixture pytest tests/
```

### 非 pytest 场景使用

```python
# standalone_script.py - 独立脚本示例

from df_test_framework import Bootstrap
from df_test_framework.plugins.builtin.reporting.allure_plugin import AllurePlugin

# 1. 初始化框架
runtime = Bootstrap().with_logging(NoOpStrategy()).build().run()

# 2. 创建并启用 AllurePlugin
allure_plugin = AllurePlugin()
# 将插件附加到全局 EventBus
from df_test_framework.infrastructure.events import get_event_bus
allure_plugin.attach_to_event_bus(get_event_bus())

# 3. 使用能力层客户端（事件会自动记录到 Allure）
http_client = runtime.http_client()
response = http_client.get("https://api.example.com/users")

db = runtime.database()
db.query_one("SELECT * FROM users WHERE id = :id", {"id": 1})

# 4. Allure 报告会自动生成
```

### 实施路线图

```
v3.18.0 (当前)
  ├─ 标记 AllurePlugin 为 DEPRECATED
  └─ 保持 Fixture 模式为唯一官方方式

v3.19.0 (如果需要支持非 pytest 场景)
  ├─ 移除 DEPRECATED 标记
  ├─ 实现智能桥接 fixture
  ├─ 添加 AllureIntegrationMode 配置
  └─ 更新文档说明两种模式

v4.0.0
  └─ 两种模式正式共存
```

### 优势与权衡

| 维度 | 优势 | 权衡 |
|------|------|------|
| **灵活性** | ✅ 支持多种场景 | ⚠️ 架构复杂度增加 |
| **扩展性** | ✅ 易于添加新报告格式 | ⚠️ 需要维护两套代码 |
| **向后兼容** | ✅ 不影响现有用户 | ⚠️ 配置选项增加 |
| **测试隔离** | ✅ 两种模式都支持 | ⚠️ 实现复杂度增加 |

---

## 方案 C：纯 Plugin 模式（架构优雅）

### 适用场景

当框架演进到以下阶段时考虑：

1. **框架定位转变**
   - 从"测试框架"转向"通用测试平台"
   - 支持多种测试运行器（pytest、unittest、自定义）
   - 提供测试基础设施即服务

2. **插件生态成熟**
   - 多个第三方插件
   - 标准的插件开发规范
   - 丰富的插件市场

3. **架构重构时机**
   - 主版本升级（v5.0.0）
   - 全面架构重构
   - 不担心破坏向后兼容性

### 架构设计

```
┌────────────────────────────────────────────────────┐
│             纯插件驱动架构                          │
├────────────────────────────────────────────────────┤
│                                                    │
│  Bootstrap                                         │
│    ├─ PluginManager.load_plugins()                │
│    │   ├─ AllurePlugin (报告)                     │
│    │   ├─ PrometheusPlugin (监控)                 │
│    │   └─ CustomPlugin (自定义)                   │
│    │                                               │
│    └─ 每个插件注册到 EventBus                      │
│                                                    │
│  Pytest Fixture（简化为桥接层）                    │
│    └─ 仅负责测试级 EventBus 创建                   │
│        └─ 将测试 EventBus 桥接给所有插件           │
│                                                    │
└────────────────────────────────────────────────────┘
```

### 核心变更

#### 1. AllurePlugin 成为唯一实现

```python
# src/df_test_framework/plugins/builtin/reporting/allure_plugin.py

class AllurePlugin:
    """Allure 报告插件（唯一实现）

    v5.0.0: 替代 AllureObserver，成为唯一 Allure 集成方式
    """

    def __init__(self):
        self._event_bus = None
        self._context_stack = []  # 管理测试上下文状态

    def attach_to_event_bus(self, event_bus: EventBus, context: dict = None):
        """附加到 EventBus（支持测试级和全局）

        Args:
            event_bus: EventBus 实例
            context: 可选的上下文信息（如 test_name）
        """
        self._event_bus = event_bus
        if context:
            self._context_stack.append(context)

        # 创建并订阅事件处理器
        self._create_handlers(event_bus)

    def detach_from_event_bus(self):
        """分离 EventBus 并清理上下文"""
        if self._context_stack:
            context = self._context_stack.pop()
            self._cleanup_context(context)
        self._event_bus = None
```

#### 2. Pytest Fixture 简化为桥接

```python
# src/df_test_framework/testing/fixtures/allure.py

@pytest.fixture(autouse=True)
def _setup_test_event_bus(request, runtime):
    """为每个测试创建隔离的 EventBus 并桥接插件"""

    # 1. 创建测试级 EventBus
    test_event_bus = EventBus()
    set_test_event_bus(test_event_bus)

    # 2. 将所有已注册的插件桥接到测试 EventBus
    plugins = runtime.extensions.get_plugins()
    for plugin in plugins:
        if hasattr(plugin, 'attach_to_event_bus'):
            context = {"test_name": request.node.name}
            plugin.attach_to_event_bus(test_event_bus, context)

    yield test_event_bus

    # 3. 清理：分离插件
    for plugin in plugins:
        if hasattr(plugin, 'detach_from_event_bus'):
            plugin.detach_from_event_bus()

    test_event_bus.clear()
    set_test_event_bus(None)
```

#### 3. 删除 AllureObserver

```python
# src/df_test_framework/testing/reporting/allure/observer.py
# ❌ 整个文件删除，功能完全由 AllurePlugin 提供
```

### 配置示例

```toml
# pyproject.toml
[tool.pytest.ini_options]
df_plugins = [
    "df_test_framework.plugins.builtin.reporting.allure_plugin",
    "df_test_framework.plugins.builtin.monitoring.prometheus_plugin",
    "custom_plugins.my_custom_plugin",
]
```

### 优势

| 优势 | 说明 |
|------|------|
| ✅ **架构纯粹** | 单一实现，无冗余代码 |
| ✅ **符合 SOLID** | 完全符合设计原则 |
| ✅ **高度可扩展** | 插件生态系统 |
| ✅ **统一接口** | 所有报告插件使用相同模式 |

### 权衡

| 权衡 | 说明 |
|------|------|
| ⚠️ **破坏兼容性** | 需要主版本升级 |
| ⚠️ **迁移成本** | 用户需要修改配置 |
| ⚠️ **实现复杂** | 插件需要管理状态 |

### 实施路线图

```
v5.0.0 (主版本升级)
  ├─ 删除 AllureObserver
  ├─ AllurePlugin 成为唯一实现
  ├─ Pytest Fixture 简化为桥接层
  └─ 全面的迁移指南
```

---

## 📊 三种方案对比总结

| 维度 | 方案 A<br>（当前） | 方案 B<br>（混合） | 方案 C<br>（纯插件） |
|------|------------------|------------------|-------------------|
| **实施时机** | v3.18.0 ✅ | v3.19.0+ | v5.0.0+ |
| **架构复杂度** | ⭐ 低 | ⭐⭐⭐ 高 | ⭐⭐ 中 |
| **适用场景** | 仅 pytest | pytest + 非 pytest | 所有场景 |
| **向后兼容** | ✅ 完全兼容 | ✅ 完全兼容 | ❌ 破坏兼容 |
| **扩展性** | ⚠️ 有限 | ✅ 强 | ✅ 最强 |
| **维护成本** | ⭐ 低 | ⭐⭐⭐ 高 | ⭐⭐ 中 |

---

## 🎯 决策建议

### 当前阶段（v3.x）

**采用方案 A** - 除非出现明确的非 pytest 场景需求

### 中期演进（v4.x）

**考虑方案 B** - 如果满足以下条件：
- 有真实的非 pytest 使用场景
- 需要支持多种报告格式
- 团队有足够资源维护

### 长期规划（v5.x+）

**考虑方案 C** - 如果框架定位转向通用平台：
- 插件生态成熟
- 主版本升级时机
- 不担心破坏向后兼容性

---

## 📝 相关文档

- [Allure 集成架构分析](./allure_integration_modes.md)
- [能力层优化计划对比](./capability_plan_vs_current.md)
- [能力层集成优化计划](../plans/CAPABILITY_LAYER_OPTIMIZATION.md)

---

**文档维护者**: @Claude Code
**最后更新**: 2025-12-08
