# DF Test Framework v3 - 完整架构重构方案

> 完整的架构设计方案（包含所有讨论的细节）
>
> 日期: 2025-11-02
> 版本: v3.0.0（最终版）
> 状态: 待实施

## 🎉 核心突破

经过深度讨论，我们实现了**两个关键架构突破**：

### 突破1: 三层能力对称架构
- `clients/` - API通信能力
- `drivers/` - UI交互能力
- `engines/` - 数据处理能力

### 突破2: 测试类型与能力层解耦
- **能力层（Layer 1）**: 定义"测试什么"（API/UI/数据）
- **测试类型层（Layer 3）**: 定义"怎么测"（功能/性能/安全）
- **关键**: 任何测试类型都可以使用任何能力

---

## 📖 目录

1. [设计目标](#设计目标)
2. [架构原则](#架构原则)
3. [核心架构设计](#核心架构设计)
4. [完整目录结构](#完整目录结构)
5. [分层架构详解](#分层架构详解)
6. [核心设计](#核心设计)
7. [API验证机制](#api验证机制)
8. [易用性设计](#易用性设计)
9. [扩展性验证](#扩展性验证)
10. [实施计划](#实施计划)
11. [迁移指南](#迁移指南)
12. [扩展指南](#扩展指南)

---

## 🎯 设计目标

### 核心目标

1. **对称性架构**: `clients/`（API客户端）和 `drivers/`（UI驱动）对称设计
2. **可插拔实现**: 支持多种实现方式（Playwright/Selenium、httpx/requests等）
3. **高扩展性**: 易于扩展新协议（GraphQL/gRPC）、新驱动（Appium）、新测试类型（性能/安全）
4. **优秀易用性**: 通过顶层导出和fixtures简化用户使用，降低导入层级
5. **清晰分层**: 职责明确，依赖方向清晰（自下而上）
6. **完整的测试支持**: 数据管理、验证、Mock、性能、安全、报告等全方位支持

### 解决的核心问题

| 问题 | 现状 | 解决方案 |
|------|------|----------|
| **目录混乱** | exceptions.py在顶层 | 移到common/ |
| **概念不清** | patterns/混合了Repository和Builder | 拆分到core/和testing/ |
| **不可扩展** | 硬编码Playwright | Protocol+Adapter模式 |
| **UI/API不对称** | core/http vs ui/ | clients/ vs drivers/ 对称 |
| **缺少验证** | 没有API验证机制 | 新增testing/validation/ |
| **数据管理弱** | 只有Builder | 新增Factory/Loader/Cleaner/Snapshot |
| **测试类型少** | 只有功能测试 | 新增性能/安全/Mock等 |
| **易用性差** | 导入层级深 | 顶层导出+fixtures |

---

## 🏛️ 架构原则

### 1. 分层原则（Layered Architecture）

```
Layer 0: common/              # 共享基础（被所有层依赖）
           ↑
Layer 1: clients/ + drivers/ + core/  # 能力层（提供核心能力）
           ↑
Layer 2: infrastructure/      # 基础设施（配置、日志、启动）
           ↑
Layer 3: testing/             # 测试支持（fixtures、验证、数据管理）
           ↑
Layer 4: extensions/ + utils/ + cli/  # 扩展和工具
```

**依赖规则**: 只能依赖下层，不能依赖同层或上层

### 2. 对称性原则（Symmetry）

```
clients/                    drivers/
├── rest/                   ├── web/
│   ├── protocols.py        │   ├── protocols.py
│   ├── httpx/              │   ├── playwright/
│   └── requests/           │   └── selenium/
├── graphql/                └── mobile/
└── grpc/                       └── appium/
```

**对称设计**: API客户端和UI驱动采用相同的架构模式

### 3. 可插拔原则（Pluggable）

通过 **Protocol（接口） + Adapter（适配器） + Factory（工厂）** 实现可插拔：

```python
# 1. 定义Protocol
class RestClientProtocol(Protocol):
    def get(self, url: str, **kwargs) -> Response: ...

# 2. 实现Adapter
class HttpxRestClient:  # 实现RestClientProtocol
    def get(self, url: str, **kwargs): ...

class RequestsRestClient:  # 实现RestClientProtocol
    def get(self, url: str, **kwargs): ...

# 3. Factory选择实现
class RestClientFactory:
    def create(client_type: str) -> RestClientProtocol:
        if client_type == "httpx":
            return HttpxRestClient()
        elif client_type == "requests":
            return RequestsRestClient()
```

### 4. 易用性原则（Usability）

**顶层导出**:
```python
# ✅ 用户代码：简洁
from df_test_framework import BaseAPI, BasePage, Database

# ❌ 避免深层导入
from df_test_framework.clients.rest.httpx.client import HttpxRestClient
```

**Fixtures隔离**:
```python
# ✅ 用户测试：不关心具体实现
def test_api(rest_client):  # rest_client可能是httpx或requests
    api = UserAPI(rest_client)
```

---

## 🗂️ 完整目录结构

```
src/df_test_framework/
│
├── __init__.py                      # 顶层导出（简化用户导入）
│
├── common/                          # Layer 0: 共享内核层
│   ├── __init__.py
│   ├── exceptions.py                # ✅ 异常定义（从顶层移入）
│   ├── types.py                     # ✅ 类型定义（从models/types.py移入）
│   └── protocols.py                 # ✅ 通用Protocol定义（新增）
│
├── clients/                         # Layer 1a: API客户端层
│   ├── __init__.py
│   │
│   ├── rest/                        # REST客户端
│   │   ├── __init__.py
│   │   ├── protocols.py             # ✅ RestClientProtocol（新增）
│   │   ├── base_api.py              # ✅ BaseAPI（从core/http/移入）
│   │   ├── models.py                # ✅ Request/Response模型（从models/base.py移入）
│   │   ├── factory.py               # ✅ RestClientFactory（新增）
│   │   │
│   │   ├── httpx/                   # httpx实现（默认）
│   │   │   ├── __init__.py
│   │   │   ├── client.py            # ✅ HttpxRestClient（从core/http/client.py移入并改造）
│   │   │   └── interceptors.py      # ✅ 拦截器（新增）
│   │   │
│   │   └── requests/                # requests实现（备选）
│   │       ├── __init__.py
│   │       └── client.py            # ✅ RequestsRestClient（新增）
│   │
│   ├── graphql/                     # GraphQL客户端（预留扩展）
│   │   ├── __init__.py
│   │   ├── protocols.py             # ✅ GraphQLClientProtocol
│   │   ├── base_api.py              # ✅ BaseGraphQLAPI
│   │   ├── factory.py               # ✅ GraphQLClientFactory
│   │   │
│   │   ├── gql/                     # gql库实现
│   │   │   ├── __init__.py
│   │   │   └── client.py            # ✅ GqlGraphQLClient
│   │   │
│   │   └── httpx/                   # httpx直接实现
│   │       ├── __init__.py
│   │       └── client.py            # ✅ HttpxGraphQLClient
│   │
│   ├── grpc/                        # gRPC客户端（预留扩展）
│   │   ├── __init__.py
│   │   ├── protocols.py             # ✅ GrpcClientProtocol
│   │   ├── base_stub.py             # ✅ BaseStub
│   │   └── client.py                # ✅ GrpcClient
│   │
│   └── websocket/                   # WebSocket客户端（预留扩展）
│       ├── __init__.py
│       ├── protocols.py             # ✅ WebSocketClientProtocol
│       ├── client.py                # ✅ WebSocketClient
│       └── message_handler.py       # ✅ 消息处理器
│
├── drivers/                         # Layer 1b: UI驱动层
│   ├── __init__.py
│   │
│   ├── web/                         # Web UI驱动
│   │   ├── __init__.py
│   │   ├── protocols.py             # ✅ WebDriverProtocol、PageProtocol（新增）
│   │   ├── base_page.py             # ✅ BasePage通用基类（新增）
│   │   ├── types.py                 # ✅ BrowserType等枚举（新增）
│   │   ├── factory.py               # ✅ WebDriverFactory（新增）
│   │   │
│   │   ├── playwright/              # Playwright实现（默认）
│   │   │   ├── __init__.py
│   │   │   ├── manager.py           # ✅ PlaywrightBrowserManager（从ui/browser_manager.py移入并改造）
│   │   │   ├── page.py              # ✅ PlaywrightPage（从ui/base_page.py移入并改造）
│   │   │   └── locator.py           # ✅ PlaywrightLocator（从ui/element_locator.py移入）
│   │   │
│   │   └── selenium/                # Selenium实现（备选）
│   │       ├── __init__.py
│   │       ├── manager.py           # ✅ SeleniumBrowserManager（新增）
│   │       └── page.py              # ✅ SeleniumPage（新增）
│   │
│   └── mobile/                      # Mobile UI驱动（预留扩展）
│       ├── __init__.py
│       ├── protocols.py             # ✅ MobileDriverProtocol
│       ├── base_screen.py           # ✅ BaseScreen
│       ├── factory.py               # ✅ MobileDriverFactory
│       │
│       └── appium/                  # Appium实现
│           ├── __init__.py
│           ├── manager.py           # ✅ AppiumDeviceManager
│           ├── screen.py            # ✅ AppiumScreen
│           └── gestures.py          # ✅ 手势操作
│
├── core/                            # Layer 1c: 核心业务层
│   ├── __init__.py
│   │
│   ├── database/                    # 数据库能力
│   │   ├── __init__.py
│   │   ├── database.py              # ✅ Database（保持）
│   │   ├── repository.py            # ✅ BaseRepository（从patterns/repositories/base.py移入）
│   │   └── query_builder.py         # ✅ QuerySpec（从patterns/repositories/query_builder.py移入）
│   │
│   └── redis/                       # Redis能力
│       ├── __init__.py
│       └── client.py                # ✅ RedisClient（保持）
│
├── infrastructure/                  # Layer 2: 基础设施层
│   ├── __init__.py
│   │
│   ├── bootstrap/                   # 启动管理
│   │   ├── __init__.py
│   │   └── bootstrap.py             # ✅ Bootstrap、BootstrapApp（保持）
│   │
│   ├── config/                      # 配置管理
│   │   ├── __init__.py
│   │   ├── schema.py                # ✅ FrameworkSettings（保持+扩展）
│   │   ├── manager.py               # ✅ ConfigManager（保持）
│   │   ├── sources.py               # ✅ 配置源（保持）
│   │   ├── pipeline.py              # ✅ 配置管道（保持）
│   │   │
│   │   └── environments/            # ✅ 环境管理（新增）
│   │       ├── __init__.py
│   │       ├── base.py              # 环境基类
│   │       ├── dev.py               # 开发环境
│   │       ├── test.py              # 测试环境
│   │       ├── staging.py           # 预发布环境
│   │       ├── prod.py              # 生产环境
│   │       └── manager.py           # EnvironmentManager
│   │
│   ├── logging/                     # 日志系统
│   │   ├── __init__.py
│   │   ├── logger.py                # ✅ Logger（保持）
│   │   └── strategies.py            # ✅ LoggerStrategy（保持）
│   │
│   ├── providers/                   # 依赖注入
│   │   ├── __init__.py
│   │   └── registry.py              # ✅ ProviderRegistry（保持）
│   │
│   ├── runtime/                     # 运行时上下文
│   │   ├── __init__.py
│   │   └── context.py               # ✅ RuntimeContext（保持）
│   │
│   └── execution/                   # ✅ 执行管理（新增）
│       ├── __init__.py
│       ├── parallel/                # 并发执行
│       │   ├── __init__.py
│       │   ├── worker_manager.py    # Worker管理
│       │   └── resource_lock.py     # 资源锁
│       │
│       ├── distributed/             # 分布式执行
│       │   ├── __init__.py
│       │   ├── master.py            # Master节点
│       │   └── worker.py            # Worker节点
│       │
│       └── isolation/               # 测试隔离
│           ├── __init__.py
│           ├── db_isolation.py      # 数据库隔离
│           └── cache_isolation.py   # 缓存隔离
│
├── testing/                         # Layer 3: 测试支持层
│   ├── __init__.py
│   │
│   ├── fixtures/                    # Pytest Fixtures
│   │   ├── __init__.py
│   │   ├── core.py                  # ✅ runtime、database、redis（保持）
│   │   ├── api_fixtures.py          # ✅ rest_client、graphql_client等（新增）
│   │   ├── web_fixtures.py          # ✅ browser、page（从ui_fixtures.py重命名）
│   │   ├── mobile_fixtures.py       # ✅ device、screen（新增）
│   │   ├── cleanup.py               # ✅ 数据清理fixtures（保持）
│   │   ├── debug.py                 # ✅ 调试fixtures（保持）
│   │   └── monitoring.py            # ✅ 监控fixtures（保持）
│   │
│   ├── data/                        # ✅ 测试数据管理（重组）
│   │   ├── __init__.py
│   │   │
│   │   ├── builders/                # 数据构建器
│   │   │   ├── __init__.py
│   │   │   ├── base.py              # ✅ BaseBuilder（从patterns/builders/移入）
│   │   │   └── dict_builder.py      # ✅ DictBuilder（从patterns/builders/移入）
│   │   │
│   │   ├── factories/               # ✅ 数据工厂（新增）
│   │   │   ├── __init__.py
│   │   │   ├── base_factory.py      # 数据工厂基类
│   │   │   ├── faker_factory.py     # 基于Faker的工厂
│   │   │   └── model_factory.py     # 模型工厂
│   │   │
│   │   ├── loaders/                 # ✅ 数据加载器（新增）
│   │   │   ├── __init__.py
│   │   │   ├── base_loader.py       # 加载器基类
│   │   │   ├── json_loader.py       # JSON数据加载
│   │   │   ├── csv_loader.py        # CSV数据加载
│   │   │   ├── excel_loader.py      # Excel数据加载
│   │   │   └── yaml_loader.py       # YAML数据加载
│   │   │
│   │   ├── cleaners/                # ✅ 数据清理器（新增）
│   │   │   ├── __init__.py
│   │   │   ├── base_cleaner.py      # BaseTestDataCleaner（从fixtures/cleanup.py移入）
│   │   │   └── generic_cleaner.py   # GenericTestDataCleaner
│   │   │
│   │   └── snapshots/               # ✅ 数据快照（新增）
│   │       ├── __init__.py
│   │       ├── db_snapshot.py       # 数据库快照
│   │       └── file_snapshot.py     # 文件快照
│   │
│   ├── validation/                  # ✅ 接口验证（新增，详见后文）
│   │   ├── __init__.py
│   │   ├── base_validator.py        # 验证器基类
│   │   ├── json_validator.py        # JSON Schema验证
│   │   ├── response_validator.py    # 响应验证器
│   │   ├── assertions.py            # 断言辅助
│   │   └── matchers.py              # 匹配器（类似hamcrest）
│   │
│   ├── mocks/                       # ✅ Mock支持（新增）
│   │   ├── __init__.py
│   │   │
│   │   ├── http/                    # HTTP Mock
│   │   │   ├── __init__.py
│   │   │   ├── mock_server.py       # Mock HTTP服务器
│   │   │   └── responses_mock.py    # 基于responses库
│   │   │
│   │   ├── database/                # 数据库Mock
│   │   │   ├── __init__.py
│   │   │   └── in_memory_db.py      # 内存数据库
│   │   │
│   │   ├── time/                    # 时间Mock
│   │   │   ├── __init__.py
│   │   │   └── freezer.py           # 冻结时间
│   │   │
│   │   └── fixtures.py              # Mock fixtures
│   │
│   ├── performance/                 # ✅ 性能测试（新增）
│   │   ├── __init__.py
│   │   │
│   │   ├── collectors/              # 性能指标收集器
│   │   │   ├── __init__.py
│   │   │   ├── base_collector.py    # 收集器基类
│   │   │   ├── api_collector.py     # API性能收集
│   │   │   ├── ui_collector.py      # UI性能收集
│   │   │   └── database_collector.py # 数据库性能收集
│   │   │
│   │   ├── load/                    # 压力测试
│   │   │   ├── __init__.py
│   │   │   ├── locust_runner.py     # Locust集成
│   │   │   └── jmeter_runner.py     # JMeter集成
│   │   │
│   │   ├── reporters/               # 性能报告
│   │   │   ├── __init__.py
│   │   │   ├── base_reporter.py     # 报告基类
│   │   │   └── html_reporter.py     # HTML报告
│   │   │
│   │   └── fixtures.py              # 性能测试fixtures
│   │
│   ├── security/                    # ✅ 安全测试（新增）
│   │   ├── __init__.py
│   │   │
│   │   ├── scanners/                # 安全扫描器
│   │   │   ├── __init__.py
│   │   │   ├── base_scanner.py      # 扫描器基类
│   │   │   ├── sql_injection.py     # SQL注入扫描
│   │   │   ├── xss_scanner.py       # XSS扫描
│   │   │   └── auth_scanner.py      # 认证扫描
│   │   │
│   │   └── fixtures.py              # 安全测试fixtures
│   │
│   ├── reporting/                   # ✅ 报告系统（新增）
│   │   ├── __init__.py
│   │   │
│   │   ├── allure/                  # Allure报告
│   │   │   ├── __init__.py
│   │   │   ├── helper.py            # AllureHelper（保持）
│   │   │   └── attachments.py       # 附件处理
│   │   │
│   │   ├── html/                    # HTML报告
│   │   │   ├── __init__.py
│   │   │   └── generator.py         # HTML报告生成器
│   │   │
│   │   ├── coverage/                # 覆盖率报告
│   │   │   ├── __init__.py
│   │   │   └── reporter.py          # 覆盖率报告
│   │   │
│   │   ├── screenshots/             # 截图管理
│   │   │   ├── __init__.py
│   │   │   ├── auto_screenshot.py   # 失败自动截图
│   │   │   └── screenshot_hook.py   # pytest hook
│   │   │
│   │   └── videos/                  # 视频录制
│   │       ├── __init__.py
│   │       └── recorder.py          # 失败录制视频
│   │
│   ├── plugins/                     # Pytest插件
│   │   ├── __init__.py
│   │   ├── allure.py                # ✅ Allure集成（保持）
│   │   ├── markers.py               # ✅ 环境标记（保持）
│   │   └── debug.py                 # ✅ 调试插件（保持）
│   │
│   └── debug/                       # 调试工具
│       ├── __init__.py
│       ├── http_debugger.py         # ✅ HTTPDebugger（保持）
│       └── db_debugger.py           # ✅ DBDebugger（保持）
│
├── extensions/                      # Layer 4: 扩展系统
│   ├── __init__.py
│   │
│   ├── core/                        # Hook定义
│   │   ├── __init__.py
│   │   ├── hooks.py                 # ✅ Hook规范（保持）
│   │   └── manager.py               # ✅ ExtensionManager（保持）
│   │
│   └── builtin/                     # 内置扩展
│       ├── __init__.py
│       └── monitoring/              # ✅ 监控扩展（保持）
│           ├── __init__.py
│           ├── api_tracker.py
│           ├── db_monitor.py
│           └── plugin.py
│
├── utils/                           # Layer 4: 工具函数
│   ├── __init__.py
│   ├── assertion.py                 # ✅ assert_that（保持）
│   ├── common.py                    # ✅ 通用工具（保持）
│   ├── data_generator.py            # ✅ DataGenerator（保持）
│   ├── decorator.py                 # ✅ 装饰器（保持）
│   └── performance.py               # ✅ 性能工具（保持）
│
└── cli/                             # Layer 4: 命令行工具
    ├── __init__.py
    ├── __main__.py                  # ✅ CLI入口（保持）
    ├── main.py                      # ✅ 主程序（保持）
    ├── utils.py                     # ✅ CLI工具（保持）
    │
    ├── commands/                    # 命令实现
    │   ├── __init__.py
    │   ├── init_cmd.py              # ✅ 项目初始化（保持）
    │   ├── generate_cmd.py          # ✅ 代码生成（保持）
    │   ├── cicd.py                  # ✅ CI/CD集成（保持）
    │   ├── docker.py                # ✅ Docker命令（新增）
    │   └── pipeline.py              # ✅ Pipeline生成（新增）
    │
    └── templates/                   # 模板文件
        ├── __init__.py
        │
        ├── project/                 # 项目模板
        │   ├── __init__.py
        │   ├── base_api.py          # ✅ （保持）
        │   ├── conftest.py          # ✅ （保持）
        │   └── ...                  # 其他模板文件
        │
        ├── generators/              # 代码生成器
        │   ├── __init__.py
        │   ├── api_client.py        # ✅ （保持）
        │   ├── builder.py           # ✅ （保持）
        │   ├── repository.py        # ✅ （保持）
        │   └── test.py              # ✅ （保持）
        │
        ├── docker/                  # ✅ Docker模板（新增）
        │   ├── Dockerfile
        │   ├── docker-compose.yml
        │   └── .dockerignore
        │
        └── pipelines/               # ✅ Pipeline模板（新增）
            ├── jenkins.groovy
            ├── gitlab-ci.yml
            └── github-actions.yml
```

---

## 📐 分层架构详解

### Layer 0: common/ - 共享内核层

**职责**: 提供所有层共享的基础定义

**内容**:
- `exceptions.py` - 异常体系（FrameworkError、ConfigurationError等）
- `types.py` - 类型定义（Enum、TypeAlias等）
- `protocols.py` - 通用Protocol定义

**依赖**: 无（最底层）

**被依赖**: 所有层

---

### Layer 1a: clients/ - API客户端层

**职责**: 提供各种API协议的客户端实现

**设计模式**: Protocol + Adapter + Factory

**REST客户端**:
```python
# clients/rest/protocols.py
class RestClientProtocol(Protocol):
    """REST客户端协议"""
    def get(self, url: str, **kwargs) -> Response: ...
    def post(self, url: str, **kwargs) -> Response: ...
    # ... 其他HTTP方法

# clients/rest/httpx/client.py
class HttpxRestClient:
    """基于httpx的REST客户端（实现RestClientProtocol）"""
    def __init__(self, base_url: str = "", timeout: int = 30):
        self.client = httpx.Client(base_url=base_url, timeout=timeout)

    def get(self, url: str, **kwargs):
        return self.client.get(url, **kwargs)
    # ...

# clients/rest/requests/client.py
class RequestsRestClient:
    """基于requests的REST客户端（实现RestClientProtocol）"""
    def __init__(self, base_url: str = "", timeout: int = 30):
        self.session = requests.Session()
        self.base_url = base_url
        self.timeout = timeout

    def get(self, url: str, **kwargs):
        full_url = f"{self.base_url}{url}"
        return self.session.get(full_url, timeout=self.timeout, **kwargs)
    # ...

# clients/rest/factory.py
class RestClientFactory:
    """REST客户端工厂"""
    _adapters = {
        "httpx": HttpxRestClient,
        "requests": RequestsRestClient,
    }

    @classmethod
    def create(cls, client_type: str = "httpx", **options) -> RestClientProtocol:
        adapter_class = cls._adapters[client_type]
        return adapter_class(**options)
```

**GraphQL客户端**（同样的模式）:
```python
# clients/graphql/protocols.py
class GraphQLClientProtocol(Protocol):
    def query(self, query: str, variables: dict = None) -> dict: ...
    def mutate(self, mutation: str, variables: dict = None) -> dict: ...

# clients/graphql/gql/client.py
class GqlGraphQLClient: ...

# clients/graphql/factory.py
class GraphQLClientFactory: ...
```

---

### Layer 1b: drivers/ - UI驱动层

**职责**: 提供各种UI驱动的实现（Web、Mobile）

**设计模式**: Protocol + Adapter + Factory（与clients/对称）

**Web驱动**:
```python
# drivers/web/protocols.py
class WebDriverProtocol(Protocol):
    """Web驱动协议"""
    def start(self) -> 'BrowserContext': ...
    def stop(self) -> None: ...
    def new_page(self) -> 'PageProtocol': ...

class PageProtocol(Protocol):
    """页面操作协议"""
    def goto(self, url: str) -> None: ...
    def click(self, selector: str) -> None: ...
    def fill(self, selector: str, value: str) -> None: ...
    # ... 其他操作

# drivers/web/playwright/manager.py
class PlaywrightBrowserManager:
    """Playwright浏览器管理器（实现WebDriverProtocol）"""
    def start(self):
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=self.headless)
        return self._browser
    # ...

# drivers/web/selenium/manager.py
class SeleniumBrowserManager:
    """Selenium浏览器管理器（实现WebDriverProtocol）"""
    def start(self):
        options = webdriver.ChromeOptions()
        self._driver = webdriver.Chrome(options=options)
        return self._driver
    # ...

# drivers/web/factory.py
class WebDriverFactory:
    """Web驱动工厂"""
    _adapters = {
        "playwright": PlaywrightBrowserManager,
        "selenium": SeleniumBrowserManager,
    }

    @classmethod
    def create(cls, driver_type: str = "playwright", **options) -> WebDriverProtocol:
        adapter_class = cls._adapters[driver_type]
        return adapter_class(**options)
```

---

### Layer 1c: core/ - 核心业务层

**职责**: 提供数据库、Redis等核心业务能力

**内容**:
- `database/` - 数据库操作（Database、Repository、QuerySpec）
- `redis/` - Redis操作（RedisClient）

**为什么数据库和Redis在core而不在clients?**
- Database和Redis是**状态存储**，不是"客户端"
- 它们提供的是**业务能力**（数据持久化），不是协议通信
- 通常与测试框架深度集成（事务、清理等）

---

### Layer 2: infrastructure/ - 基础设施层

**职责**: 提供配置、日志、启动、运行时等基础设施

**内容**:
- `bootstrap/` - 框架启动管理
- `config/` - 配置管理（Schema、Source、Pipeline、Environment）
- `logging/` - 日志系统
- `providers/` - 依赖注入
- `runtime/` - 运行时上下文
- `execution/` - 执行管理（并发、分布式、隔离）

---

### Layer 3: testing/ - 测试支持层

**职责**: 提供测试所需的各种支持功能

**核心子模块**:

#### 3.1 fixtures/ - Pytest Fixtures

提供各种pytest fixture：
```python
# testing/fixtures/api_fixtures.py
@pytest.fixture
def rest_client():
    """REST客户端（根据配置自动选择httpx或requests）"""
    settings = get_settings()
    client = RestClientFactory.create(
        client_type=settings.rest.client_type,
        base_url=settings.rest.base_url,
    )
    yield client
    client.close()

# testing/fixtures/web_fixtures.py
@pytest.fixture
def browser():
    """浏览器（根据配置自动选择playwright或selenium）"""
    settings = get_settings()
    manager = WebDriverFactory.create(
        driver_type=settings.web.driver_type,
        headless=settings.web.headless,
    )
    manager.start()
    yield manager.browser
    manager.stop()
```

#### 3.2 data/ - 测试数据管理

完整的测试数据管理体系：

**builders/** - 数据构建器:
```python
# testing/data/builders/dict_builder.py
class DictBuilder(BaseBuilder):
    """字典构建器"""
    def __init__(self):
        self._data = {}

    def set(self, key, value):
        """设置键值"""
        self._data[key] = value
        return self  # 链式调用

    def build(self):
        """构建字典"""
        return self._data.copy()

# 使用
user = DictBuilder().set("name", "张三").set("age", 30).build()
```

**factories/** - 数据工厂:
```python
# testing/data/factories/faker_factory.py
from faker import Faker

class FakerFactory:
    """基于Faker的数据工厂"""
    def __init__(self, locale='zh_CN'):
        self.faker = Faker(locale)

    def create_user(self, **overrides):
        """创建用户数据"""
        user = {
            "name": self.faker.name(),
            "email": self.faker.email(),
            "phone": self.faker.phone_number(),
            "address": self.faker.address(),
        }
        user.update(overrides)
        return user

# 使用
factory = FakerFactory()
users = [factory.create_user() for _ in range(10)]
```

**loaders/** - 数据加载器:
```python
# testing/data/loaders/json_loader.py
class JsonDataLoader:
    """JSON数据加载器"""
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

    def load(self, filename: str):
        """加载JSON文件"""
        with open(self.data_dir / filename, 'r', encoding='utf-8') as f:
            return json.load(f)

# 使用
loader = JsonDataLoader(Path("tests/data"))
test_data = loader.load("users.json")
```

**cleaners/** - 数据清理器:
```python
# testing/data/cleaners/generic_cleaner.py
class GenericTestDataCleaner(BaseTestDataCleaner):
    """通用数据清理器"""
    def __init__(self, database: Database):
        self.database = database
        self.created_records = []

    def track_created(self, table: str, record_id: int):
        """记录创建的数据"""
        self.created_records.append((table, record_id))

    def cleanup(self):
        """清理所有记录的数据"""
        for table, record_id in reversed(self.created_records):
            self.database.execute(f"DELETE FROM {table} WHERE id = :id", {"id": record_id})

# 使用
@pytest.fixture
def data_cleaner(database):
    cleaner = GenericTestDataCleaner(database)
    yield cleaner
    cleaner.cleanup()
```

**snapshots/** - 数据快照:
```python
# testing/data/snapshots/db_snapshot.py
class DatabaseSnapshot:
    """数据库快照"""
    def __init__(self, database: Database):
        self.database = database

    def create_snapshot(self, tables: list):
        """创建快照"""
        snapshot = {}
        for table in tables:
            snapshot[table] = self.database.query_all(f"SELECT * FROM {table}")
        return snapshot

    def restore_snapshot(self, snapshot: dict):
        """恢复快照"""
        for table, records in snapshot.items():
            self.database.execute(f"DELETE FROM {table}")
            for record in records:
                self.database.insert(table, record)

# 使用
@pytest.fixture
def db_snapshot(database):
    snapshot_mgr = DatabaseSnapshot(database)
    snapshot = snapshot_mgr.create_snapshot(["users", "orders"])
    yield snapshot_mgr
    snapshot_mgr.restore_snapshot(snapshot)
```

#### 3.3 validation/ - 接口验证

详见后文"API验证机制"章节

#### 3.4 mocks/ - Mock支持

提供各种Mock功能：

**HTTP Mock**:
```python
# testing/mocks/http/mock_server.py
import responses

class HttpMockServer:
    """HTTP Mock服务器"""
    def __init__(self):
        self.responses = responses.RequestsMock()

    def mock_get(self, url: str, json_data: dict, status: int = 200):
        """Mock GET请求"""
        self.responses.add(responses.GET, url, json=json_data, status=status)

    def start(self):
        self.responses.start()

    def stop(self):
        self.responses.stop()

# 使用
@pytest.fixture
def http_mock():
    mock = HttpMockServer()
    mock.start()
    yield mock
    mock.stop()
```

**时间Mock**:
```python
# testing/mocks/time/freezer.py
from freezegun import freeze_time

class TimeFreezer:
    """时间冻结器"""
    @staticmethod
    def freeze(frozen_time: str):
        """冻结时间"""
        return freeze_time(frozen_time)

# 使用
@pytest.fixture
def frozen_time():
    with TimeFreezer.freeze("2025-01-01 00:00:00"):
        yield
```

#### 3.5 performance/ - 性能测试

**性能收集器**:
```python
# testing/performance/collectors/api_collector.py
class APIPerformanceCollector:
    """API性能收集器"""
    def __init__(self):
        self.metrics = []

    def record(self, endpoint: str, duration: float, status_code: int):
        """记录性能指标"""
        self.metrics.append({
            "endpoint": endpoint,
            "duration": duration,
            "status_code": status_code,
            "timestamp": datetime.now(),
        })

    def get_stats(self):
        """获取统计信息"""
        return {
            "avg_duration": sum(m["duration"] for m in self.metrics) / len(self.metrics),
            "max_duration": max(m["duration"] for m in self.metrics),
            "total_requests": len(self.metrics),
        }
```

**压力测试**:
```python
# testing/performance/load/locust_runner.py
from locust import HttpUser, task, between

class LocustRunner:
    """Locust压力测试运行器"""
    @staticmethod
    def create_user_class(base_url: str):
        """创建Locust用户类"""
        class APIUser(HttpUser):
            host = base_url
            wait_time = between(1, 2)

            @task
            def test_endpoint(self):
                self.client.get("/api/users")

        return APIUser
```

#### 3.6 security/ - 安全测试

**SQL注入扫描**:
```python
# testing/security/scanners/sql_injection.py
class SQLInjectionScanner:
    """SQL注入扫描器"""
    SQL_PAYLOADS = [
        "' OR '1'='1",
        "'; DROP TABLE users--",
        "' UNION SELECT * FROM users--",
    ]

    def scan(self, rest_client, endpoint: str, params: dict):
        """扫描SQL注入漏洞"""
        vulnerabilities = []
        for param_name in params.keys():
            for payload in self.SQL_PAYLOADS:
                test_params = params.copy()
                test_params[param_name] = payload

                response = rest_client.get(endpoint, params=test_params)
                if self._is_vulnerable(response):
                    vulnerabilities.append({
                        "param": param_name,
                        "payload": payload,
                        "response": response.text[:100],
                    })

        return vulnerabilities
```

#### 3.7 reporting/ - 报告系统

**自动截图**:
```python
# testing/reporting/screenshots/auto_screenshot.py
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试失败时自动截图"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        if "page" in item.fixturenames:
            page = item.funcargs["page"]
            screenshot_path = f"screenshots/{item.nodeid}.png"
            page.screenshot(path=screenshot_path)

            # 附加到Allure
            allure.attach.file(screenshot_path, name="失败截图",
                              attachment_type=allure.attachment_type.PNG)
```

---

### Layer 4: extensions/ + utils/ + cli/

**extensions/** - 扩展系统:
- 基于pluggy的Hook机制
- 内置扩展（监控、性能追踪等）

**utils/** - 工具函数:
- 断言、装饰器、性能工具、数据生成器等

**cli/** - 命令行工具:
- 项目初始化、代码生成、CI/CD集成
- Docker、Pipeline模板生成

---

## 🔐 API验证机制

### 设计目标

提供完整的API接口验证能力：
1. 响应状态码验证
2. JSON Schema验证
3. 响应体断言
4. 响应时间断言
5. 链式断言（Fluent API）

### 架构设计

```
testing/validation/
├── __init__.py
├── base_validator.py        # 验证器基类
├── json_validator.py        # JSON Schema验证
├── response_validator.py    # 响应验证器
├── assertions.py            # 断言辅助
└── matchers.py              # 匹配器
```

### 详细实现

#### 1. 响应验证器

```python
# testing/validation/response_validator.py
from typing import Any, Callable
import jsonschema

class ResponseValidator:
    """响应验证器（链式调用）"""

    def __init__(self, response):
        self.response = response
        self._errors = []

    def status_code(self, expected: int):
        """验证状态码"""
        if self.response.status_code != expected:
            self._errors.append(
                f"Expected status code {expected}, got {self.response.status_code}"
            )
        return self

    def status_is_success(self):
        """验证状态码为2xx"""
        if not (200 <= self.response.status_code < 300):
            self._errors.append(
                f"Expected success status code (2xx), got {self.response.status_code}"
            )
        return self

    def json_schema(self, schema: dict):
        """验证JSON Schema"""
        try:
            jsonschema.validate(instance=self.response.json(), schema=schema)
        except jsonschema.ValidationError as e:
            self._errors.append(f"JSON Schema validation failed: {e.message}")
        return self

    def json_path(self, path: str, expected_value: Any = None, matcher: Callable = None):
        """验证JSON路径的值"""
        from jsonpath_ng import parse

        jsonpath_expr = parse(path)
        matches = [match.value for match in jsonpath_expr.find(self.response.json())]

        if not matches:
            self._errors.append(f"JSON path '{path}' not found in response")
            return self

        actual_value = matches[0]

        if expected_value is not None:
            if actual_value != expected_value:
                self._errors.append(
                    f"JSON path '{path}': expected {expected_value}, got {actual_value}"
                )

        if matcher is not None:
            if not matcher(actual_value):
                self._errors.append(
                    f"JSON path '{path}': value {actual_value} did not match condition"
                )

        return self

    def header(self, name: str, expected_value: str = None):
        """验证响应头"""
        actual_value = self.response.headers.get(name)

        if actual_value is None:
            self._errors.append(f"Header '{name}' not found in response")
        elif expected_value is not None and actual_value != expected_value:
            self._errors.append(
                f"Header '{name}': expected '{expected_value}', got '{actual_value}'"
            )

        return self

    def response_time_less_than(self, max_ms: int):
        """验证响应时间"""
        elapsed_ms = self.response.elapsed.total_seconds() * 1000
        if elapsed_ms > max_ms:
            self._errors.append(
                f"Response time {elapsed_ms:.0f}ms exceeds limit {max_ms}ms"
            )
        return self

    def assert_valid(self):
        """断言所有验证通过"""
        if self._errors:
            raise AssertionError("\n".join(self._errors))

    def is_valid(self) -> bool:
        """检查是否所有验证通过"""
        return len(self._errors) == 0
```

#### 2. JSON Schema验证器

```python
# testing/validation/json_validator.py
import jsonschema

class JsonValidator:
    """JSON Schema验证器"""

    @staticmethod
    def validate(data: dict, schema: dict) -> tuple[bool, str]:
        """
        验证JSON数据

        Returns:
            (is_valid, error_message)
        """
        try:
            jsonschema.validate(instance=data, schema=schema)
            return True, ""
        except jsonschema.ValidationError as e:
            return False, e.message

    @staticmethod
    def create_schema(
        properties: dict,
        required: list = None,
        additional_properties: bool = True
    ) -> dict:
        """
        创建JSON Schema

        Examples:
            >>> schema = JsonValidator.create_schema(
            ...     properties={
            ...         "id": {"type": "integer"},
            ...         "name": {"type": "string"},
            ...         "email": {"type": "string", "format": "email"}
            ...     },
            ...     required=["id", "name"]
            ... )
        """
        schema = {
            "type": "object",
            "properties": properties,
            "additionalProperties": additional_properties,
        }
        if required:
            schema["required"] = required

        return schema
```

#### 3. 断言辅助函数

```python
# testing/validation/assertions.py

def assert_status(response, expected_status: int):
    """断言状态码"""
    assert response.status_code == expected_status, \
        f"Expected status {expected_status}, got {response.status_code}"

def assert_json_schema(response, schema: dict):
    """断言JSON Schema"""
    from jsonschema import validate, ValidationError
    try:
        validate(instance=response.json(), schema=schema)
    except ValidationError as e:
        raise AssertionError(f"JSON Schema validation failed: {e.message}")

def assert_json_equals(response, expected: dict):
    """断言JSON内容相等"""
    actual = response.json()
    assert actual == expected, f"Expected {expected}, got {actual}"

def assert_json_contains(response, **kwargs):
    """断言JSON包含指定键值对"""
    actual = response.json()
    for key, expected_value in kwargs.items():
        actual_value = actual.get(key)
        assert actual_value == expected_value, \
            f"Expected {key}={expected_value}, got {key}={actual_value}"

def assert_response_time(response, max_ms: int):
    """断言响应时间"""
    elapsed_ms = response.elapsed.total_seconds() * 1000
    assert elapsed_ms <= max_ms, \
        f"Response time {elapsed_ms:.0f}ms exceeds limit {max_ms}ms"
```

#### 4. 匹配器（类似Hamcrest）

```python
# testing/validation/matchers.py

class Matcher:
    """匹配器基类"""
    def matches(self, actual) -> bool:
        raise NotImplementedError

    def describe(self) -> str:
        raise NotImplementedError

class EqualTo(Matcher):
    """等于"""
    def __init__(self, expected):
        self.expected = expected

    def matches(self, actual) -> bool:
        return actual == self.expected

    def describe(self) -> str:
        return f"equal to {self.expected}"

class GreaterThan(Matcher):
    """大于"""
    def __init__(self, threshold):
        self.threshold = threshold

    def matches(self, actual) -> bool:
        return actual > self.threshold

    def describe(self) -> str:
        return f"greater than {self.threshold}"

class Contains(Matcher):
    """包含"""
    def __init__(self, item):
        self.item = item

    def matches(self, actual) -> bool:
        return self.item in actual

    def describe(self) -> str:
        return f"contains {self.item}"

class HasLength(Matcher):
    """长度等于"""
    def __init__(self, length):
        self.length = length

    def matches(self, actual) -> bool:
        return len(actual) == self.length

    def describe(self) -> str:
        return f"has length {self.length}"

# 便捷函数
def equal_to(expected):
    return EqualTo(expected)

def greater_than(threshold):
    return GreaterThan(threshold)

def contains(item):
    return Contains(item)

def has_length(length):
    return HasLength(length)
```

### 使用示例

#### 示例1: 链式验证

```python
from df_test_framework import ResponseValidator

def test_get_user(rest_client):
    response = rest_client.get("/api/users/1")

    # 链式验证
    (ResponseValidator(response)
     .status_code(200)
     .json_path("$.id", expected_value=1)
     .json_path("$.name", matcher=lambda x: len(x) > 0)
     .header("Content-Type", "application/json")
     .response_time_less_than(500)
     .assert_valid())
```

#### 示例2: JSON Schema验证

```python
from df_test_framework import JsonValidator, ResponseValidator

def test_user_schema(rest_client):
    # 定义Schema
    user_schema = JsonValidator.create_schema(
        properties={
            "id": {"type": "integer"},
            "name": {"type": "string", "minLength": 1},
            "email": {"type": "string", "format": "email"},
            "age": {"type": "integer", "minimum": 0, "maximum": 150}
        },
        required=["id", "name", "email"]
    )

    response = rest_client.get("/api/users/1")

    (ResponseValidator(response)
     .status_code(200)
     .json_schema(user_schema)
     .assert_valid())
```

#### 示例3: 简单断言

```python
from df_test_framework.testing.validation import assert_status, assert_json_contains

def test_create_user(rest_client):
    response = rest_client.post("/api/users", json={
        "name": "张三",
        "email": "zhangsan@test.com"
    })

    assert_status(response, 201)
    assert_json_contains(response, name="张三", email="zhangsan@test.com")
```

#### 示例4: 使用匹配器

```python
from df_test_framework.testing.validation import ResponseValidator
from df_test_framework.testing.validation.matchers import greater_than, has_length

def test_get_users_list(rest_client):
    response = rest_client.get("/api/users")

    (ResponseValidator(response)
     .status_code(200)
     .json_path("$.total", matcher=greater_than(0))
     .json_path("$.items", matcher=has_length(10))
     .assert_valid())
```

---

## 🎨 易用性设计

### 问题：导入层级过深

**问题示例**:
```python
# ❌ 深层导入（用户体验差）
from df_test_framework.clients.rest.httpx.client import HttpxRestClient
from df_test_framework.drivers.web.playwright.manager import PlaywrightBrowserManager
from df_test_framework.testing.data.builders.dict_builder import DictBuilder
```

### 解决方案1: 顶层导出

**顶层__init__.py统一导出**:
```python
# src/df_test_framework/__init__.py

# API客户端
from .clients.rest import BaseAPI, BaseRequest, BaseResponse

# UI驱动
from .drivers.web import BasePage, BrowserType

# 核心业务
from .core.database import Database, BaseRepository, QuerySpec
from .core.redis import RedisClient

# 测试支持
from .testing.data.builders import BaseBuilder, DictBuilder
from .testing.validation import ResponseValidator, assert_status

# ... 更多导出
```

**用户使用**:
```python
# ✅ 简洁导入
from df_test_framework import (
    BaseAPI,
    BasePage,
    Database,
    DictBuilder,
    ResponseValidator,
)
```

### 解决方案2: 通过Fixtures隔离实现

**用户不直接使用具体实现**:
```python
# ✅ 用户测试代码（通过fixture）
def test_api(rest_client):  # rest_client可能是httpx或requests
    """用户不关心rest_client的具体实现"""
    response = rest_client.get("/api/users/1")
    assert response.status_code == 200

def test_ui(page):  # page可能来自playwright或selenium
    """用户不关心page的具体实现"""
    page.goto("https://example.com")
    page.click("#login")
```

**Fixture内部处理实现选择**:
```python
# testing/fixtures/api_fixtures.py
@pytest.fixture
def rest_client():
    """REST客户端（根据配置自动选择）"""
    settings = get_settings()

    # 🔥 根据配置选择实现（用户通过配置文件切换）
    client = RestClientFactory.create(
        client_type=settings.rest.client_type,  # "httpx" or "requests"
        base_url=settings.rest.base_url,
    )

    yield client
    client.close()
```

### 解决方案3: 配置驱动

**用户通过配置文件切换实现**:
```yaml
# config.yaml

# REST客户端配置
rest:
  client_type: httpx  # 或 requests（切换实现只需改这里）
  base_url: https://api.example.com
  timeout: 30

# Web驱动配置
web:
  driver_type: playwright  # 或 selenium（切换实现只需改这里）
  headless: true
  timeout: 30000
```

**用户代码完全不变**:
```python
# 同样的测试代码，适用于httpx或requests
def test_api(rest_client):
    response = rest_client.get("/api/users/1")
    assert response.status_code == 200

# 同样的测试代码，适用于playwright或selenium
def test_ui(page):
    page.goto("https://example.com")
    page.click("#login")
```

---

## 📋 实施计划

### 阶段划分

#### 阶段1: 核心架构重构 ✅ (P0 - 必须实现)

**时间**: 1-2周

**内容**:
1. 创建新的目录结构
2. 移动现有文件到新位置
3. 更新所有导入路径
4. 实现核心功能：
   - ✅ `clients/rest/httpx/` - REST客户端（httpx实现）
   - ✅ `clients/rest/` - BaseAPI、models
   - ✅ `drivers/web/playwright/` - Web驱动（playwright实现）
   - ✅ `drivers/web/` - BasePage、protocols
   - ✅ `common/` - exceptions、types、protocols
   - ✅ `testing/validation/` - 完整的验证机制
   - ✅ `testing/data/cleaners/` - 数据清理器
5. 更新顶层__init__.py导出
6. 运行测试验证

**成功标准**:
- 所有现有测试通过
- 用户导入路径简化
- 框架可正常运行

---

#### 阶段2: 备选实现 ✅ (P1 - 重要)

**时间**: 1周

**内容**:
1. 实现备选REST客户端：
   - ✅ `clients/rest/requests/` - requests实现
2. 实现备选Web驱动：
   - ✅ `drivers/web/selenium/` - selenium实现
3. 实现工厂类：
   - ✅ `clients/rest/factory.py`
   - ✅ `drivers/web/factory.py`
4. 配置支持：
   - ✅ 扩展`FrameworkSettings`支持多实现选择
5. Fixtures更新：
   - ✅ 通过工厂创建实例

**成功标准**:
- 可通过配置切换httpx/requests
- 可通过配置切换playwright/selenium
- 切换实现不影响用户代码

---

#### 阶段3: 数据管理增强 ✅ (P1 - 重要)

**时间**: 1周

**内容**:
1. ✅ `testing/data/factories/` - 数据工厂实现
2. ✅ `testing/data/loaders/` - 数据加载器实现
3. ✅ `testing/data/snapshots/` - 数据快照实现
4. ✅ 完善`testing/data/builders/`

**成功标准**:
- 数据工厂可生成随机测试数据
- 数据加载器可加载JSON/CSV/Excel等格式
- 数据快照可保存和恢复数据库状态

---

#### 阶段4: 扩展协议支持 ✅ (P2 - 可选)

**时间**: 1-2周

**内容**:
1. ✅ `clients/graphql/` - GraphQL客户端完整实现
2. ✅ `clients/grpc/` - gRPC客户端完整实现
3. ✅ `clients/websocket/` - WebSocket客户端完整实现
4. ✅ 相应的fixtures和示例

**成功标准**:
- GraphQL客户端可执行Query/Mutation/Subscription
- gRPC客户端可调用gRPC服务
- WebSocket客户端可收发消息

---

#### 阶段5: 移动端支持 ✅ (P2 - 可选)

**时间**: 1-2周

**内容**:
1. ✅ `drivers/mobile/appium/` - Appium驱动实现
2. ✅ `drivers/mobile/` - BaseScreen、protocols
3. ✅ `testing/fixtures/mobile_fixtures.py`

**成功标准**:
- 可启动和控制Android/iOS设备
- 可执行移动端UI自动化测试

---

#### 阶段6: 高级测试功能 ✅ (P2 - 可选)

**时间**: 2-3周

**内容**:
1. ✅ `testing/mocks/` - Mock支持完整实现
2. ✅ `testing/performance/` - 性能测试完整实现
3. ✅ `testing/security/` - 安全测试完整实现
4. ✅ `testing/reporting/` - 报告系统完整实现
5. ✅ `infrastructure/execution/` - 并发和分布式执行

**成功标准**:
- Mock可隔离外部依赖
- 性能测试可执行压力测试并生成报告
- 安全测试可扫描常见漏洞
- 失败自动截图和录制视频
- 支持并发和分布式执行

---

#### 阶段7: CLI增强 ✅ (P2 - 可选)

**时间**: 1周

**内容**:
1. ✅ `cli/commands/docker.py` - Docker支持
2. ✅ `cli/commands/pipeline.py` - Pipeline生成
3. ✅ `cli/templates/docker/` - Docker模板
4. ✅ `cli/templates/pipelines/` - CI/CD Pipeline模板

**成功标准**:
- 可生成Docker配置
- 可生成Jenkins/GitLab CI/GitHub Actions配置

---

### 迁移步骤

#### Step 1: 备份

```bash
git checkout -b refactoring-v3
git commit -am "backup: before v3 refactoring"
```

#### Step 2: 创建新目录结构

```bash
# 执行脚本创建所有目录和__init__.py
python scripts/create_v3_structure.py
```

#### Step 3: 移动现有文件

```bash
# 执行迁移脚本
python scripts/migrate_files.py
```

#### Step 4: 更新导入

```bash
# 批量更新导入（使用IDE或脚本）
python scripts/update_imports.py
```

#### Step 5: 运行测试

```bash
pytest tests/ -v
```

#### Step 6: 更新文档

```bash
# 更新所有文档中的导入示例
python scripts/update_docs.py
```

---

## 🔄 迁移指南

### 用户项目迁移

#### 迁移前（v2）

```python
# 旧的导入方式
from df_test_framework.exceptions import FrameworkError
from df_test_framework.core.http import HttpClient
from df_test_framework.ui import BasePage
from df_test_framework.patterns.builders import DictBuilder
from df_test_framework.patterns.repositories import BaseRepository

# 旧的测试代码
def test_api(http_client):
    response = http_client.get("/api/users/1")
    assert response.status_code == 200
```

#### 迁移后（v3）

```python
# ✅ 新的导入方式（更简洁）
from df_test_framework import (
    FrameworkError,      # 从common/
    BaseAPI,             # 从clients/rest/
    BasePage,            # 从drivers/web/
    DictBuilder,         # 从testing/data/builders/
    BaseRepository,      # 从core/database/
    ResponseValidator,   # 新增：从testing/validation/
)

# ✅ 新的测试代码（fixture名称变化）
def test_api(rest_client):  # http_client → rest_client
    response = rest_client.get("/api/users/1")

    # 新增：链式验证
    (ResponseValidator(response)
     .status_code(200)
     .json_path("$.id", expected_value=1)
     .assert_valid())
```

#### 兼容性策略

**阶段1: 双重导出（过渡期）**
```python
# src/df_test_framework/__init__.py

# 新的导出
from .clients.rest import BaseAPI
from .clients.rest.httpx import HttpxRestClient as RestClient

# 旧的别名（兼容性）
from .clients.rest.httpx import HttpxRestClient as HttpClient  # 兼容旧名称

__all__ = [
    "BaseAPI",
    "RestClient",  # 新名称
    "HttpClient",  # 旧名称（过渡期保留）
]
```

**阶段2: 弃用警告**
```python
import warnings

class HttpClient(HttpxRestClient):
    """@deprecated: Use RestClient instead"""
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "HttpClient is deprecated, use RestClient instead",
            DeprecationWarning,
            stacklevel=2
        )
        super().__init__(*args, **kwargs)
```

**阶段3: 移除旧API（v4.0）**

---

## 🚀 扩展指南

### 如何添加新的API协议

以添加**JSON-RPC**客户端为例：

#### Step 1: 创建目录结构

```bash
mkdir -p src/df_test_framework/clients/jsonrpc
touch src/df_test_framework/clients/jsonrpc/__init__.py
```

#### Step 2: 定义Protocol

```python
# src/df_test_framework/clients/jsonrpc/protocols.py
from typing import Protocol, Any

class JsonRpcClientProtocol(Protocol):
    """JSON-RPC客户端协议"""

    def call(self, method: str, params: list | dict = None) -> Any:
        """调用JSON-RPC方法"""
        ...

    def notify(self, method: str, params: list | dict = None) -> None:
        """发送JSON-RPC通知（不等待响应）"""
        ...
```

#### Step 3: 实现客户端

```python
# src/df_test_framework/clients/jsonrpc/client.py
import requests
import json

class JsonRpcClient:
    """JSON-RPC客户端"""

    def __init__(self, url: str):
        self.url = url
        self.request_id = 0

    def call(self, method: str, params: list | dict = None):
        """调用JSON-RPC方法"""
        self.request_id += 1

        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or [],
            "id": self.request_id,
        }

        response = requests.post(self.url, json=payload)
        result = response.json()

        if "error" in result:
            raise Exception(result["error"])

        return result.get("result")

    def notify(self, method: str, params: list | dict = None):
        """发送通知"""
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or [],
        }

        requests.post(self.url, json=payload)
```

#### Step 4: 创建Factory

```python
# src/df_test_framework/clients/jsonrpc/factory.py
class JsonRpcClientFactory:
    """JSON-RPC客户端工厂"""

    @classmethod
    def create(cls, url: str) -> JsonRpcClient:
        return JsonRpcClient(url)
```

#### Step 5: 添加Fixture

```python
# src/df_test_framework/testing/fixtures/api_fixtures.py

@pytest.fixture
def jsonrpc_client():
    """JSON-RPC客户端"""
    settings = get_settings()
    client = JsonRpcClientFactory.create(url=settings.jsonrpc.url)
    yield client
```

#### Step 6: 顶层导出

```python
# src/df_test_framework/__init__.py

from .clients.jsonrpc import JsonRpcClient

__all__ = [
    # ... 其他导出
    "JsonRpcClient",
]
```

#### Step 7: 使用

```python
# 用户测试代码
def test_jsonrpc(jsonrpc_client):
    result = jsonrpc_client.call("add", [2, 3])
    assert result == 5
```

---

### 如何添加新的UI驱动

以添加**Cypress**驱动为例（虽然Cypress是JS，这里假设有Python绑定）：

#### Step 1: 创建目录

```bash
mkdir -p src/df_test_framework/drivers/web/cypress
```

#### Step 2: 实现驱动

```python
# src/df_test_framework/drivers/web/cypress/manager.py

class CypressBrowserManager:
    """Cypress浏览器管理器"""

    def __init__(self, headless: bool = True):
        self.headless = headless

    def start(self):
        # 启动Cypress
        pass

    def stop(self):
        # 关闭Cypress
        pass
```

#### Step 3: 注册到Factory

```python
# src/df_test_framework/drivers/web/factory.py

class WebDriverFactory:
    _adapters = {
        "playwright": PlaywrightBrowserManager,
        "selenium": SeleniumBrowserManager,
        "cypress": CypressBrowserManager,  # ✅ 新增
    }
```

#### Step 4: 配置支持

```yaml
# config.yaml
web:
  driver_type: cypress  # ✅ 新驱动
  headless: true
```

---

## 📊 总结

### 核心改进

| 方面 | v2 | v3 |
|------|----|----|
| **目录数量** | 10个顶层 | 7个顶层（优化30%） |
| **API客户端** | core/http（单一） | clients/（多协议） |
| **UI驱动** | ui/（单一） | drivers/（多驱动） |
| **对称性** | 无 | clients ↔ drivers |
| **可插拔** | 硬编码 | Protocol+Adapter+Factory |
| **验证机制** | 无 | testing/validation/ |
| **数据管理** | 只有Builder | Factory+Loader+Cleaner+Snapshot |
| **测试类型** | 功能测试 | 功能+性能+安全+Mock |
| **易用性** | 深层导入 | 顶层导出+Fixtures |

### 架构优势

1. ✅ **对称性**: clients/和drivers/对称设计
2. ✅ **可插拔**: 多种实现可切换（httpx/requests、playwright/selenium）
3. ✅ **可扩展**: 易于添加新协议（GraphQL/gRPC）、新驱动（Appium）
4. ✅ **易用性**: 顶层导出、Fixtures隔离实现
5. ✅ **完整性**: 数据管理、验证、Mock、性能、安全全覆盖
6. ✅ **清晰性**: 分层清晰、职责明确
7. ✅ **可维护性**: 目录减少、结构优化

### 实施优先级

- **P0（必须）**: 阶段1 - 核心架构重构
- **P1（重要）**: 阶段2 - 备选实现、阶段3 - 数据管理增强
- **P2（可选）**: 阶段4-7 - 扩展功能

---

**文档版本**: v1.0
**最后更新**: 2025-11-02
**负责人**: DF QA Team
