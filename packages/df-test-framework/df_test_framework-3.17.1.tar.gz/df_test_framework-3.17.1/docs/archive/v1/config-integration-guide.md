# 配置中心集成指南（v2）

## 概述

v2 对配置系统进行了彻底重写：`FrameworkSettings` 仍然是类型安全的核心模型，但现在通过 `ConfigPipeline` + `ConfigSource` 组合构建； Bootstrap / pytest 插件负责在启动阶段注册配置类、加载 `.env`/环境变量/命令行覆盖项，并把最终的 `settings` 注入 RuntimeContext。

核心特性：

- ✅ **声明式注册**：项目定义 `FrameworkSettings` 子类，调用 `configure_settings()`（或在 pytest 中使用 `--df-settings-class`/`df_settings_class`）。
- ✅ **可组合的配置源**：内置 `.env`、环境变量、命令行（`DF_SETTINGS_CLASS`、`DF_PLUGINS`）等 source；插件也可以新增 `ConfigSource`。
- ✅ **多命名空间**：同一进程可以通过 namespace 管理多套配置实例。
- ✅ **与 Bootstrap/Runtime 解耦**：无论是 CLI、pytest 还是手动调用，配置加载流程保持一致。

---

## 1. 定义配置模型

```python
# config/settings.py
from decimal import Decimal
from pydantic import Field
from df_test_framework import FrameworkSettings


class BusinessConfig(BaseModel):
    default_amount: Decimal = Field(default=Decimal("100.00"))
    template_id: str = "TMPL_001"


class ProjectSettings(FrameworkSettings):
    business: BusinessConfig = Field(default_factory=BusinessConfig)
```

> `FrameworkSettings` 内置 `http/db/redis/test/logging/extras` 等字段，可按需覆盖默认值；也可以通过 `extras` namespace 扩展临时配置。

---

## 2. 注册与启动

### 方式 A：显式 Bootstrap

```python
from df_test_framework import Bootstrap
from config.settings import ProjectSettings

runtime = (
    Bootstrap()
    .with_settings(ProjectSettings)
    .with_plugin("my_project.plugins.metrics")  # 可选
    .build()
    .run()
)

settings = runtime.settings
```

### 方式 B：pytest 集成

在 `tests/conftest.py` 中启用官方插件：

```python
pytest_plugins = ["df_test_framework.fixtures.core"]
```

在命令行或 `pytest.ini` 中声明配置类与插件：

```bash
pytest --df-settings-class=config.settings.ProjectSettings \
       --df-plugin my_project.plugins.metrics
```

```ini
# pytest.ini
[pytest]
df_settings_class = config.settings.ProjectSettings
df_plugins = my_project.plugins.metrics
```

> 也可以通过环境变量 `DF_SETTINGS_CLASS`、`DF_PLUGINS` 设置，方便 CI/CD。

---

## 3. 配置源优先级

默认 `ConfigPipeline` 加载顺序：

```
1. .env
2. .env.{ENV}   （ENV 由 APP_ENV 或 ENV 环境变量确定，默认为 test）
3. .env.local
4. 环境变量（APP_*）
5. 命令行参数（--df-settings-class / --df-plugin / 其它显式覆盖）
```

插件可以通过 `df_config_sources` hook 追加自定义 `ConfigSource`，优先级位于默认 source 之后。

---

## 4. 多环境配置示例

```
your-project/
├── .env
├── .env.test
├── .env.staging
├── .env.prod
├── .env.local       # 不提交
└── .env.example
```

`.env`（基础配置）
```bash
APP_HTTP__TIMEOUT=30
APP_HTTP__MAX_RETRIES=3
APP_DB__POOL_SIZE=10
```

`.env.test`
```bash
ENV=test
APP_HTTP__BASE_URL=http://test-api.example.com
APP_DB__HOST=test-db
APP_DB__USER=test_user
APP_DB__PASSWORD=test_pass
```

`.env.prod`
```bash
ENV=prod
APP_HTTP__BASE_URL=https://api.example.com
# 敏感信息请通过 CI/CD 或密钥管理注入 APP_DB__PASSWORD 等
```

运行测试：
```bash
ENV=test pytest
ENV=prod DF_SETTINGS_CLASS=config.settings.ProjectSettings pytest
```

---

## 5. 临时覆盖与测试辅助

- **环境变量**：在 CI/CD 流水线或容器中设置 `APP_*` 环境变量。
- **命令行**：可以追加自定义 `ConfigSource`，或在测试中调用 `create_settings(settings_cls=..., overrides={...})` 创建私有实例。

```python
from config.settings import ProjectSettings
from df_test_framework.config import create_settings

settings = create_settings(
    settings_cls=ProjectSettings,
    overrides={
        "http": {"base_url": "http://mock-api"},
        "business": {"default_amount": "42.00"},
    },
)
```

---

## 6. 与扩展配合

插件可以实现 `df_providers`、`df_post_bootstrap`，并读取 `settings`：

```python
from df_test_framework.extensions import hookimpl


@hookimpl
def df_post_bootstrap(runtime):
    runtime.logger.info("Running in %s", runtime.settings.env)
```

在 pytest 中通过 `--df-plugin` 或 `df_plugins` 启用即可。

---

## 总结

- 统一通过 `Bootstrap`/pytest 插件加载配置。
- `.env` / 环境变量 / 命令行的优先级保持一致，但可以通过插件进一步扩展。
- 测试项目只需维护自己的 `FrameworkSettings` 子类，并在入口处注册即可共享所有框架能力。
