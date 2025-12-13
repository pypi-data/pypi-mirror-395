# 30分钟快速上手指南

> **文档版本**: v2.0.0
> **最后更新**: 2026-01-15
> **预计用时**: 30分钟
> **适用人群**: 首次使用 df-test-framework 的测试工程师

---

## 🎯 目标

30 分钟内完成以下事项：

- 安装框架并初始化项目骨架
- 定义 `FrameworkSettings` 子类并加载配置
- 编写一个简单的 API 封装与测试用例
- 使用 pytest 执行测试并生成报告

---

## ⏱️ 时间规划

| 步骤 | 内容 | 预计用时 |
|------|------|---------|
| 1 | 环境准备与安装 | 5 分钟 |
| 2 | 生成项目脚手架 | 5 分钟 |
| 3 | 配置与引导 | 10 分钟 |
| 4 | 编写 API 封装与测试 | 7 分钟 |
| 5 | 运行测试与查看报告 | 3 分钟 |

---

## 📋 步骤 1：环境准备（5 分钟）

### 1.1 检查 Python 版本

```bash
python --version
# 要求：Python 3.11+
```

### 1.2 安装包管理工具（推荐 uv）

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

uv --version
```

### 1.3 安装 df-test-framework

```bash
uv tool install df-test-framework  # 或者使用 pip install df-test-framework

> 如需更新本地源码依赖，可执行 `uv sync --reinstall-package df-test-framework`。
> 也可以在 `pyproject.toml` 中添加：
> ```toml
> [tool.uv.sources]
> df-test-framework = { path = "../test-framework", develop = true }
> ```
> 随后运行 `uv sync` 即可自动使用最新源码。
```

> 如果需要开发版本，可将源码目录添加为 extra index：`uv add "/path/to/test-framework"`。

---

## 🏗️ 步骤 2：生成项目脚手架（5 分钟）

使用 CLI 一键生成项目结构：

```bash
mkdir my-api-test && cd my-api-test

df-test init .
```

目录结构示例：

```
my-api-test/
├── config/
│   └── settings.py          # 自定义 FrameworkSettings 子类
├── tests/
│   └── conftest.py          # 已启用官方 pytest 插件
├── .env.example             # 配置示例
├── pyproject.toml           # uv / pip 项目配置
└── pytest.ini               # pytest 配置（可选）
```

> CLI 生成的 `settings.py` 已包含 `register_settings()` 示例；`tests/conftest.py` 默认启用 `df_test_framework.fixtures.core`。

---

## ⚙️ 步骤 3：配置与引导（10 分钟）

### 3.1 定义业务配置

在 `config/settings.py` 中扩展 `FrameworkSettings`：

```python
from decimal import Decimal
from pydantic import BaseModel, Field
from df_test_framework import FrameworkSettings


class BusinessConfig(BaseModel):
    default_amount: Decimal = Field(default=Decimal("100.00"))
    template_id: str = "TMPL_001"


class ProjectSettings(FrameworkSettings):
    business: BusinessConfig = Field(default_factory=BusinessConfig)
```

### 3.2 注册配置类

仍在 `config/settings.py` 中：

```python
from df_test_framework import configure_settings


def register_settings():
    configure_settings(ProjectSettings)
```

### 3.3 创建 `.env` 配置

```bash
cp .env.example .env
# 编辑 .env，例如：
# APP_HTTP__BASE_URL=http://localhost:8000/api
# APP_DB__HOST=localhost
```

### 3.4 启用 pytest 插件

`tests/conftest.py` 已包含：

```python
pytest_plugins = ["df_test_framework.fixtures.core"]

from config.settings import get_settings


@pytest.fixture(scope="session")
def settings():
    return get_settings()
```

在 `pytest.ini` 中声明配置类：

```ini
[pytest]
df_settings_class = config.settings.ProjectSettings
```

（或通过命令行）

```bash
pytest --df-settings-class=config.settings.ProjectSettings
```

---

## 🧪 步骤 4：编写 API 封装与测试（7 分钟）

### 4.1 API 封装（`api/user_api.py`）

```python
from df_test_framework import BaseAPI, HttpClient


class UserAPI(BaseAPI):
    def __init__(self, client: HttpClient):
        super().__init__(client)
        self.prefix = "/users"

    def get_detail(self, user_id: int):
        return self.get(f"{self.prefix}/{user_id}")
```

### 4.2 测试用例（`tests/api/test_user.py`）

```python
import pytest

from api.user_api import UserAPI


@pytest.fixture(scope="session")
def user_api(http_client):
    return UserAPI(http_client)


def test_get_user_success(user_api):
    response = user_api.get_detail(1)
    assert response.status_code == 200
    assert response.json()["id"] == 1
```

> `http_client` fixture 由官方插件提供，基于 `settings.http` 自动构建。

---

## 🚀 步骤 5：运行测试与查看报告（3 分钟）

### 5.1 运行测试

```bash
pytest -v
```

如需启用 Allure：

```bash
pytest --alluredir=reports/allure-results
```

### 5.2 启动 Allure 报告

```bash
allure serve reports/allure-results
```

> 若尚未安装 Allure，可参考官方文档或使用 `brew install allure`（macOS）。

---

## ✅ 成果回顾

- 项目使用 `FrameworkSettings` + `.env` 管理配置
- pytest 自动加载配置类并提供 `runtime/http_client/database` 等 fixture
- 通过 CLI/Bootstrap 可以扩展插件（`--df-plugin`）并注入业务自定义能力

下一步可参考：

- [使用示例](../user-guide/examples.md)
- [扩展系统使用指南](../user-guide/extensions.md)
- [迁移指南](../migration/from-v1-to-v2.md)

祝使用愉快！
