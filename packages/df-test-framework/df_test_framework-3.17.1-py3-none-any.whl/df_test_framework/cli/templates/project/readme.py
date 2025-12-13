"""README模板

参考 gift-card-test 项目风格，关注项目本身而非框架特性。
"""

README_TEMPLATE = """# {ProjectName}

{ProjectName} 的 API 自动化测试项目，基于 df-test-framework 构建。

## 覆盖系统

| 系统 | 说明 | 测试目录 |
|------|------|----------|
| API | 核心 API 接口测试 | `tests/api/` |

## 快速开始

### 1. 安装依赖

```bash
# 使用 uv（推荐）
uv sync

# 或使用 pip
pip install -e .
```

### 2. 配置环境

```bash
cp .env.example .env
# 编辑 .env 填写 API 地址、数据库配置等
```

### 3. 运行测试

```bash
# 运行所有测试
uv run pytest tests/ -v

# 运行冒烟测试
uv run pytest -m smoke -v

# 生成 Allure 报告
uv run pytest tests/ --alluredir=reports/allure-results
allure serve reports/allure-results
```

## 项目结构

```
{project_name}/
├── src/{project_name}/
│   ├── apis/                    # API 客户端封装
│   ├── models/                  # Pydantic 数据模型
│   │   ├── requests/            # 请求模型
│   │   └── responses/           # 响应模型
│   ├── repositories/            # 数据库仓储层
│   ├── builders/                # 测试数据构建器
│   ├── fixtures/                # 项目 Fixtures
│   ├── config/settings.py       # 配置（含中间件）
│   └── uow.py                   # Unit of Work
├── tests/
│   ├── api/                     # API 测试
│   └── conftest.py              # Fixtures 定义
├── .env                         # 环境配置
└── pytest.ini                   # Pytest 配置
```

## 编写测试

### 核心 Fixtures

| Fixture | 说明 |
|---------|------|
| `http_client` | HTTP 客户端（自动签名/Token） |
| `uow` | Unit of Work（数据库操作，自动回滚） |
| `settings` | 配置对象 |
| `cleanup_api_data` | API 测试数据清理 |

### 数据清理机制

测试数据有两种来源，清理方式不同：

#### 1. Repository 直接创建的数据

通过 `uow` 直接操作数据库创建的数据，**自动回滚**：

```python
def test_example(uow):
    # 直接通过 Repository 创建
    uow.users.create({{"name": "test_user", ...}})
    # ✅ 测试结束后自动回滚，无需手动清理
```

#### 2. API 创建的数据（重要）

通过 API 调用创建的数据由后端事务提交，**需要显式清理**：

```python
from df_test_framework import DataGenerator

def test_example(http_client, cleanup_api_data):
    # 生成测试订单号
    order_no = DataGenerator.test_id("TEST_ORD")

    # 通过 API 创建数据
    response = http_client.post("/orders", json={{"order_no": order_no}})
    assert response.status_code == 200

    # ✅ 记录订单号，测试结束后自动清理
    cleanup_api_data.add("orders", order_no)
```

### 示例测试

```python
import allure
import pytest
from df_test_framework import DataGenerator
from df_test_framework.testing.plugins import attach_json, step


@allure.feature("订单管理")
@allure.story("创建订单")
class TestOrderCreate:

    @allure.title("创建订单-成功")
    @pytest.mark.smoke
    def test_create_order_success(self, http_client, settings, cleanup_api_data):
        \"\"\"测试创建订单\"\"\"

        with step("准备测试数据"):
            order_no = DataGenerator.test_id("TEST_ORD")
            request_data = {{
                "order_no": order_no,
                "user_id": "test_user_001",
                "amount": 100.00
            }}
            attach_json(request_data, name="请求数据")

        with step("调用创建订单 API"):
            response = http_client.post("/orders", json=request_data)
            attach_json(response.json(), name="响应数据")

        with step("验证响应"):
            assert response.status_code == 200
            assert response.json()["code"] == 200

        # 记录需要清理的订单号
        cleanup_api_data.add("orders", order_no)
```

## 运行测试

### 常用命令

```bash
# 详细输出
uv run pytest tests/ -v

# 失败时停止
uv run pytest tests/ -x

# 按标记运行
uv run pytest -m smoke           # 冒烟测试
uv run pytest -m "not slow"      # 排除慢速测试

# 保留测试数据（调试用）
uv run pytest --keep-test-data
```

### 测试标记

| 标记 | 说明 |
|------|------|
| `@pytest.mark.smoke` | 冒烟测试 |
| `@pytest.mark.regression` | 回归测试 |
| `@pytest.mark.slow` | 慢速测试 |
| `@pytest.mark.keep_data` | 保留该测试的数据 |

## 配置说明

### 环境变量 (.env)

```bash
# 环境
ENV=dev

# HTTP 配置
APP_HTTP__BASE_URL=https://api.example.com
APP_HTTP__TIMEOUT=30

# 签名配置（如需要）
APP_SIGNATURE__ENABLED=true
APP_SIGNATURE__SECRET=your_secret

# 数据库
APP_DB__HOST=localhost
APP_DB__PORT=3306
APP_DB__USER=root
APP_DB__PASSWORD=password
APP_DB__DATABASE=test_db
```

## 常见问题

### Q: API 创建的数据没有清理

使用 `cleanup_api_data` fixture 并调用 `cleanup_api_data.add("type", id)`。

### Q: 订单号重复错误

使用 `DataGenerator.test_id("TEST_ORD")` 生成唯一订单号。

### Q: 数据库连接失败

检查 `.env` 中的数据库配置是否正确。

### Q: 签名验证失败

检查 `.env` 中的 `APP_SIGNATURE__SECRET` 是否与服务端一致。

### Q: 调试时想保留测试数据

```bash
# 方式1: 命令行参数
uv run pytest --keep-test-data

# 方式2: 环境变量
KEEP_TEST_DATA=1 uv run pytest

# 方式3: 测试标记
@pytest.mark.keep_data
def test_debug():
    ...
```
"""

__all__ = ["README_TEMPLATE"]
