# 测试目录结构说明

本目录结构镜像 `src/df_test_framework/` 的四层架构设计。

## 目录结构

```
tests/
├── core/                    # Layer 0 - 核心抽象层测试
│   ├── test_middleware.py   # 中间件系统测试
│   ├── test_events.py       # 事件总线测试
│   └── test_context.py      # 上下文传播测试
│
├── infrastructure/          # Layer 1 - 基础设施层测试
│   ├── test_bootstrap.py    # 引导程序测试
│   ├── test_config.py       # 配置管理测试
│   ├── test_logging.py      # 日志系统测试
│   ├── test_providers.py    # Provider 测试
│   └── test_runtime.py      # 运行时测试
│
├── capabilities/            # Layer 2 - 能力层测试
│   ├── clients/             # HTTP/GraphQL/gRPC 客户端测试
│   ├── databases/           # 数据库相关测试
│   ├── messengers/          # 消息队列测试（Kafka/RabbitMQ/RocketMQ）
│   ├── drivers/             # UI 驱动测试（Playwright/Selenium）
│   └── storages/            # 存储测试（S3/OSS）
│
├── plugins/                 # 横切关注点 - 插件测试
│   └── builtin/             # 内置插件测试
│
├── testing/                 # Layer 3 - 测试工具层测试
│   └── fixtures/            # Fixtures 测试
│
├── cli/                     # CLI 工具测试
│   └── test_init.py         # 脚手架测试
│
└── unit/                    # 遗留的单元测试（待重组）
```

## 测试分类

### Layer 0 - 核心抽象层 (core/)
测试纯抽象、协议定义、类型系统：
- 中间件系统（MiddlewareChain、BaseMiddleware）
- 事件类型和事件总线
- 上下文传播机制
- 异常体系

### Layer 1 - 基础设施层 (infrastructure/)
测试框架基础设施：
- Bootstrap 和 Runtime
- 配置管理（ConfigManager、ConfigSource）
- 日志系统
- Provider 和依赖注入
- 插件管理系统

### Layer 2 - 能力层 (capabilities/)
测试具体能力模块：
- **clients/**: HTTP、GraphQL、gRPC 客户端
- **databases/**: MySQL、Redis、Repository、UoW
- **messengers/**: Kafka、RabbitMQ、RocketMQ
- **drivers/**: Playwright、Selenium WebDriver
- **storages/**: S3、OSS 存储

### 横切关注点 (plugins/)
测试插件系统和内置插件：
- 日志插件
- 指标插件
- 追踪插件

### Layer 3 - 测试工具层 (testing/)
测试 pytest fixtures、数据生成器、调试工具

## 命名规范

- 测试文件名：`test_*.py`
- 测试类名：`Test<ClassName>`
- 测试方法名：`test_<描述性名称>`

## 运行测试

```bash
# 运行所有测试
uv run pytest -v

# 运行特定层的测试
uv run pytest tests/core/ -v           # 核心层
uv run pytest tests/infrastructure/ -v  # 基础设施层
uv run pytest tests/capabilities/ -v    # 能力层

# 运行特定模块的测试
uv run pytest tests/capabilities/clients/ -v
uv run pytest tests/capabilities/databases/ -v

# 排除需要外部服务的测试
uv run pytest -v --ignore=tests/capabilities/messengers/
```

## 依赖规则

测试遵循与源代码相同的依赖规则：
- Layer N 的测试只依赖 Layer 0 到 Layer N-1 的功能
- 能力层测试不依赖测试工具层（除 fixtures 外）
- 插件测试可以依赖任何层（横切关注点）

## 迁移说明

v3.14.0 重组了测试目录以镜像新的架构。旧的测试文件位置：
- `tests/test_infrastructure/` → `tests/infrastructure/`
- `tests/test_messengers/` → `tests/capabilities/messengers/`
- `tests/clients/` → `tests/capabilities/clients/`
- `tests/databases/` → `tests/capabilities/databases/`

旧目录保留以确保向后兼容，将在 v3.16.0 移除。
