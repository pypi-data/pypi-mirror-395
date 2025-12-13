# 项目开发最佳实践

> **文档版本**: v1.3.1
> **最后更新**: 2025-10-30
> **面向人群**: 实际开发测试项目的工程师
> **参考项目**: gift-card-test（真实生产项目）
> **框架状态**: ✅ v1.3.1 生产就绪
> ⚠️ **Legacy**: 本文档描述的是 v1.x 使用模式，仅供历史归档。v2 项目最佳实践请结合 [30分钟快速上手指南](../guides/30分钟快速上手指南.md) 与新框架示例。

### 重要更新 (v1.3.1)
本文档已更新支持：
- ✅ **Repository模式** (v1.3.0) - 推荐用于数据访问层
- ✅ **Builder模式** (v1.3.0) - 推荐用于构建测试数据
- ✅ **性能监控** (v1.3.0) - 推荐用于性能追踪
- ✅ **配置集成** (v1.3.1) - 与Fixtures完全集成

---

## 🎯 本指南目标

指导你开发**生产级别**的测试项目，包含完整的项目组织、设计模式、最佳实践和真实案例。

**本指南涵盖**:
- ✅ 项目目录结构设计（详细说明）
- ✅ 数据模型分层组织
- ✅ API封装的两种响应解析模式
- ✅ conftest.py完整配置案例
- ✅ E2E测试编写指南
- ✅ 真实项目案例解读（gift-card-test）

---

## 📚 目录

1. [项目目录结构设计](#1-项目目录结构设计)
2. [数据模型组织最佳实践](#2-数据模型组织最佳实践)
3. [API封装的两种响应解析模式](#3-api封装的两种响应解析模式)
4. [conftest.py完整配置](#4-conftest完整配置)
5. [E2E测试编写指南](#5-e2e测试编写指南)
6. [真实项目案例解读](#6-真实项目案例解读)
7. [常见问题和最佳实践](#7-常见问题和最佳实践)

---

## 1. 项目目录结构设计

### 1.1 推荐的目录结构

以 `gift-card-test` 项目为例的**生产级**目录结构：

```
gift-card-test/                      # 项目根目录
├── api/                             # API封装层（关键目录）
│   ├── __init__.py
│   ├── master_card_api.py          # Master系统API
│   ├── h5_card_api.py              # H5用户端API
│   └── admin_consumption_api.py    # Admin管理端API
│
├── models/                          # 数据模型层（关键目录）
│   ├── __init__.py
│   ├── request/                    # 请求模型（按系统分类）
│   │   ├── __init__.py
│   │   ├── master_card.py         # Master系统请求模型
│   │   ├── h5_card.py             # H5系统请求模型
│   │   └── admin_consumption.py   # Admin系统请求模型
│   └── response/                   # 响应模型
│       ├── __init__.py
│       └── card_models.py         # 通用卡片响应模型
│
├── tests/                          # 测试用例层（关键目录）
│   ├── __init__.py
│   ├── conftest.py                # Pytest全局配置（核心文件）
│   ├── api/                       # API测试
│   │   ├── __init__.py
│   │   ├── test_master_card/     # Master系统测试
│   │   │   ├── __init__.py
│   │   │   └── test_create_cards.py
│   │   ├── test_h5_card/         # H5系统测试
│   │   │   ├── __init__.py
│   │   │   ├── test_user_cards.py
│   │   │   ├── test_payment.py
│   │   │   └── test_consumption_records.py
│   │   ├── test_admin_consumption/  # Admin系统测试
│   │   │   ├── __init__.py
│   │   │   └── test_query_records.py
│   │   └── test_e2e/             # E2E端到端测试
│   │       ├── __init__.py
│   │       └── test_complete_flow.py
│   └── ui/                        # UI测试（预留）
│       └── __init__.py
│
├── config/                         # 配置层
│   ├── __init__.py
│   └── settings.py                # 配置类（pydantic-settings）
│
├── utils/                          # 工具层（可选）
│   ├── __init__.py
│   ├── data_helper.py             # 数据处理工具
│   └── db_helper.py               # 数据库操作工具
│
├── reports/                        # 测试报告（自动生成）
│   ├── logs/                      # 日志文件
│   ├── allure/                    # Allure原始数据
│   ├── allure-report/            # Allure HTML报告
│   └── report.html               # pytest-html报告
│
├── docs/                           # 项目文档（可选）
│   ├── API接口文档.md
│   └── 测试计划.md
│
├── .env                            # 环境配置（敏感信息，不提交）
├── .env.test                       # 测试环境配置
├── .env.dev                        # 开发环境配置
├── .env.prod                       # 生产环境配置
├── .env.example                    # 配置示例文件
├── .gitignore                      # Git忽略文件（包含.env）
├── pyproject.toml                  # 项目配置（uv管理）
├── uv.lock                         # 依赖锁定文件
├── pytest.ini                      # pytest配置
└── README.md                       # 项目说明
```

### 1.2 目录职责说明

| 目录 | 职责 | 重要性 | 说明 |
|------|------|--------|------|
| **api/** | API封装 | ⭐⭐⭐⭐⭐ | 封装所有HTTP API，使用BaseAPI基类 |
| **models/request/** | 请求模型 | ⭐⭐⭐⭐⭐ | 定义所有请求参数模型（Pydantic） |
| **models/response/** | 响应模型 | ⭐⭐⭐⭐⭐ | 定义所有响应数据模型（Pydantic） |
| **tests/** | 测试用例 | ⭐⭐⭐⭐⭐ | 所有测试代码，按系统/功能分类 |
| **tests/conftest.py** | 全局配置 | ⭐⭐⭐⭐⭐ | Pytest fixtures和hooks（最重要） |
| **config/** | 配置管理 | ⭐⭐⭐⭐ | 环境配置文件，支持多环境 |
| **utils/** | 工具函数 | ⭐⭐⭐ | 通用工具函数（可选） |
| **reports/** | 测试报告 | ⭐⭐ | 自动生成，通常加入.gitignore |

### 1.3 目录组织原则

#### ✅ 按系统/模块分类

**推荐**（如gift-card-test）:
```
tests/api/
├── test_master_card/      # Master系统的测试
├── test_h5_card/         # H5系统的测试
└── test_admin_consumption/  # Admin系统的测试
```

**不推荐**:
```
tests/api/
├── test_create.py        # 难以知道是哪个系统的创建
├── test_query.py         # 难以知道是哪个系统的查询
└── test_payment.py       # 难以知道是哪个系统的支付
```

#### ✅ 模型与API对应

**推荐**:
```
models/request/
├── master_card.py        # Master系统请求模型
└── h5_card.py           # H5系统请求模型

api/
├── master_card_api.py   # 使用 master_card.py 的模型
└── h5_card_api.py       # 使用 h5_card.py 的模型
```

#### ✅ 单一职责原则

**推荐**: 一个API类只负责一个系统/模块
```python
class MasterCardAPI(BaseAPI):
    """只负责Master系统的礼品卡API"""
    pass

class H5CardAPI(BaseAPI):
    """只负责H5系统的礼品卡API"""
    pass
```

**不推荐**: 一个API类包含多个系统
```python
class CardAPI(BaseAPI):
    """同时包含Master、H5、Admin的API - 太庞大"""
    pass
```

---

## 2. 数据模型组织最佳实践

### 2.1 请求模型设计

#### 基本原则

1. **一个接口一个请求模型**
2. **使用Pydantic的验证功能**
3. **字段名与API文档一致**
4. **添加清晰的文档字符串**

#### 示例：gift-card-test 的请求模型

```python
# models/request/master_card.py
from pydantic import BaseModel, Field, field_validator


class MasterCardCreateRequest(BaseModel):
    """Master系统创建礼品卡请求

    对应接口: POST /master/card/create
    """

    customer_order_no: str = Field(..., description="订单号（必填）")
    user_id: str = Field(..., description="用户ID（必填）")
    template_id: str = Field(..., description="礼品卡模板ID（必填）")
    quantity: int = Field(..., ge=1, le=100, description="创建数量（1-100）")

    @field_validator("customer_order_no")
    @classmethod
    def validate_order_no(cls, v: str) -> str:
        """验证订单号格式"""
        if not v or len(v) < 3:
            raise ValueError("订单号长度至少3个字符")
        return v

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, v: int) -> int:
        """验证数量范围"""
        if v < 1 or v > 100:
            raise ValueError("数量必须在1-100之间")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "customer_order_no": "ORD20251029001",
                "user_id": "test_user_001",
                "template_id": "TMPL_001",
                "quantity": 5
            }
        }
```

**关键点**:
- ✅ 使用 `Field()` 添加验证和文档
- ✅ 使用 `field_validator` 添加自定义验证
- ✅ 使用 `json_schema_extra` 提供示例
- ✅ 清晰的类文档字符串

### 2.2 响应模型设计

#### 基本原则

1. **嵌套模型分层定义**
2. **使用 `extra = "ignore"` 忽略额外字段**
3. **可选字段使用 `Optional`**
4. **复杂响应拆分成多个模型**

#### 示例：多层嵌套响应模型

```python
# models/response/card_models.py
from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal


class MasterCardCreateData(BaseModel):
    """创建礼品卡响应数据"""
    card_nos: List[str]  # 卡号列表
    quantity: int        # 创建数量
    customer_order_no: str  # 订单号

    class Config:
        extra = "ignore"  # 忽略API返回的其他字段


class MasterCardCreateResponse(BaseModel):
    """Master系统创建礼品卡响应

    统一响应格式:
    {
        "code": 0,
        "message": "success",
        "data": {...}
    }
    """
    code: int
    message: str
    data: Optional[MasterCardCreateData] = None

    @property
    def success(self) -> bool:
        """判断请求是否成功"""
        return self.code == 0

    class Config:
        extra = "ignore"


class CardInfo(BaseModel):
    """单张卡片信息"""
    card_no: str
    user_id: str
    template_id: str
    balance: Decimal
    status: int
    created_at: str

    class Config:
        extra = "ignore"


class H5MyCardsData(BaseModel):
    """我的礼品卡数据"""
    cards: List[CardInfo]  # 卡片列表
    total_balance: Decimal  # 总余额
    available_card_count: int  # 可用卡片数

    class Config:
        extra = "ignore"


class H5MyCardsResponse(BaseModel):
    """H5查询我的礼品卡响应"""
    code: int
    message: str
    data: Optional[H5MyCardsData] = None

    @property
    def success(self) -> bool:
        return self.code == 0

    class Config:
        extra = "ignore"
```

**关键点**:
- ✅ 嵌套模型独立定义（`CardInfo`、`MasterCardCreateData`）
- ✅ 添加 `@property` 方便使用（`success`）
- ✅ 使用 `Decimal` 处理金额（避免精度问题）
- ✅ 使用 `Optional` 标记可选字段

### 2.3 模型组织策略

#### 策略1: 按系统分类（推荐用于大项目）

```
models/
├── request/
│   ├── master_card.py      # Master系统所有请求模型
│   ├── h5_card.py          # H5系统所有请求模型
│   └── admin_consumption.py  # Admin系统所有请求模型
└── response/
    ├── master_card.py      # Master系统所有响应模型
    ├── h5_card.py          # H5系统所有响应模型
    └── admin_consumption.py  # Admin系统所有响应模型
```

#### 策略2: 通用模型共享（推荐用于gift-card-test）

```
models/
├── request/
│   ├── master_card.py
│   ├── h5_card.py
│   └── admin_consumption.py
└── response/
    └── card_models.py      # 所有系统共享的响应模型（CardInfo等）
```

**选择建议**:
- 小项目（< 20个接口）: 策略2，简单直接
- 大项目（> 50个接口）: 策略1，便于维护

---

## 3. API封装的两种响应解析模式

### 3.1 模式对比

| 模式 | 使用场景 | 优点 | 缺点 |
|------|---------|------|------|
| **框架方法** `_parse_response()` | 标准RESTful API | 统一错误处理、代码简洁 | 需要适配特殊格式 |
| **直接解析** `**response.json()` | 非标准API、特殊格式 | 灵活、完全控制 | 需要手动错误处理 |

### 3.2 模式1: 使用框架方法（推荐用于标准API）

```python
# api/user_api.py
from df_test_framework import BaseAPI, HttpClient
from models.response.user_response import UserResponse


class UserAPI(BaseAPI):
    """用户API - 使用框架方法"""

    def __init__(self, http_client: HttpClient):
        super().__init__(http_client)
        self.base_path = "/users"

    def get_user(self, user_id: int) -> UserResponse:
        """获取用户信息

        使用 _parse_response() 统一解析
        """
        response = self.client.get(f"{self.base_path}/{user_id}")

        # 框架方法: 自动处理HTTP错误、解析JSON、验证模型
        return self._parse_response(response, UserResponse)
```

**优势**:
- ✅ 自动处理HTTP状态码错误（4xx、5xx）
- ✅ 自动解析JSON
- ✅ 自动验证Pydantic模型
- ✅ 统一的错误日志

**适用场景**:
- RESTful API
- 标准JSON响应
- 不需要特殊处理的接口

### 3.3 模式2: 直接解析（gift-card-test实际使用）

```python
# api/master_card_api.py
from df_test_framework import BaseAPI, HttpClient
from models.request.master_card import MasterCardCreateRequest
from models.response.card_models import MasterCardCreateResponse


class MasterCardAPI(BaseAPI):
    """Master系统礼品卡API - 直接解析"""

    def __init__(self, http_client: HttpClient):
        super().__init__(http_client)
        self.base_path = "/master/card"

    def create_cards(self, request: MasterCardCreateRequest) -> MasterCardCreateResponse:
        """批量创建礼品卡

        直接解析响应
        """
        endpoint = f"{self.base_path}/create"

        # 发送请求
        response = self.client.post(
            endpoint,
            data={  # 注意: 使用 data 而非 json（后端需要 form data）
                "customerOrderNo": request.customer_order_no,
                "userId": request.user_id,
                "templateId": request.template_id,
                "quantity": request.quantity,
            }
        )

        # 直接解析: 完全控制解析过程
        return MasterCardCreateResponse(**response.json())
```

**优势**:
- ✅ 完全控制解析流程
- ✅ 可以处理特殊响应格式
- ✅ 可以在解析前做额外处理
- ✅ 灵活性最高

**适用场景**:
- 非标准响应格式
- 需要特殊字段映射
- 需要在解析前预处理数据

### 3.4 为什么gift-card-test使用直接解析？

**原因分析**:

1. **后端使用form data而非JSON**
```python
# 需要用 data= 而非 json=
response = self.client.post(endpoint, data={...})
```

2. **字段名需要转换**
```python
# Python风格: snake_case
customer_order_no: str

# 后端需要: camelCase
"customerOrderNo": request.customer_order_no
```

3. **统一响应格式可以自定义验证**
```python
@property
def success(self) -> bool:
    return self.code == 0  # 业务成功判断
```

### 3.5 最佳实践建议

```python
# ✅ 推荐: 两种模式混合使用
class MixedAPI(BaseAPI):
    """混合使用两种模式"""

    def get_user(self, user_id: int) -> UserResponse:
        """标准接口 - 使用框架方法"""
        response = self.client.get(f"/users/{user_id}")
        return self._parse_response(response, UserResponse)

    def special_api(self, data: dict) -> CustomResponse:
        """特殊接口 - 直接解析"""
        response = self.client.post("/special", data=data)

        # 预处理
        json_data = response.json()
        if json_data.get("需要特殊处理"):
            json_data["特殊字段"] = self._process(json_data["特殊字段"])

        return CustomResponse(**json_data)
```

---

## 4. conftest完整配置

### 4.1 conftest.py的作用

`conftest.py` 是pytest的**核心配置文件**，作用：

1. ✅ 定义fixtures（测试前置条件）
2. ✅ 配置pytest hooks（生命周期钩子）
3. ✅ 全局配置（日志、Allure等）
4. ✅ 自定义标记（smoke、regression等）

### 4.2 生产级conftest.py模板

基于 `gift-card-test` 的完整案例：

```python
# tests/conftest.py
"""Pytest全局配置和fixtures

v1.1.0 新特性集成:
- 使用配置工厂模式管理配置
- 日志自动脱敏和轮转
- Allure增强插件集成
- 环境标记插件集成
"""

import pytest
from pathlib import Path
from decimal import Decimal
from df_test_framework import HttpClient, Database, setup_logger, get_settings
from df_test_framework.utils import DataGenerator
from df_test_framework.plugins import AllureHelper
from config.settings import settings
from api.master_card_api import MasterCardAPI
from api.h5_card_api import H5CardAPI
from api.admin_consumption_api import AdminConsumptionAPI


# ========== 日志配置 (v1.1.0 增强) ==========

# 确保日志目录存在
log_dir = Path("reports/logs")
log_dir.mkdir(parents=True, exist_ok=True)

setup_logger(
    log_level=settings.log_level,
    log_file=str(log_dir / f"test_{settings.env}.log"),
    rotation="100 MB",  # v1.1.0: 日志轮转
    retention="7 days",  # v1.1.0: 保留7天
    enable_sanitize=True,  # v1.1.0: 敏感信息脱敏
)


# ========== HTTP客户端 Fixtures ==========

@pytest.fixture(scope="session")
def http_client() -> HttpClient:
    """提供HTTP客户端 (session级别)

    作用域: session - 整个测试会话只创建一次
    优势: 所有测试共享连接池，性能最优

    Yields:
        HttpClient: HTTP客户端实例
    """
    client = HttpClient(
        base_url=settings.api_base_url,
        timeout=settings.api_timeout,
    )
    yield client
    client.close()


# ========== 数据库 Fixtures ==========

@pytest.fixture(scope="session")
def db() -> Database:
    """提供数据库实例 (session级别)

    作用域: session - 整个测试会话只创建一次
    用途: 数据验证、测试数据准备

    Yields:
        Database: 数据库实例
    """
    database = Database(settings.db_connection_string)
    yield database
    database.close()


@pytest.fixture(scope="function")
def db_session(db):
    """提供数据库会话 (function级别,自动回滚)

    作用域: function - 每个测试独立
    特点: 测试结束自动回滚，不污染数据库

    Yields:
        Session: SQLAlchemy会话
    """
    with db.session() as session:
        yield session
        session.rollback()  # 自动回滚


# ========== API Fixtures ==========
# 所有API fixtures使用依赖注入模式,共享session级别的http_client
# 优势:
# 1. 共享连接池,性能更好
# 2. 资源利用率高,减少连接开销
# 3. 符合框架设计理念
# 4. 便于测试时mock HttpClient

@pytest.fixture(scope="function")
def master_card_api(http_client) -> MasterCardAPI:
    """提供Master系统礼品卡API实例

    作用域: function - 每个测试独立
    注入: session级别的http_client,多个API实例共享连接池

    Args:
        http_client: session级别的HTTP客户端

    Returns:
        MasterCardAPI: Master系统API实例
    """
    return MasterCardAPI(http_client)


@pytest.fixture(scope="function")
def h5_card_api(http_client) -> H5CardAPI:
    """提供H5用户端礼品卡API实例

    作用域: function - 每个测试独立
    注入: session级别的http_client,多个API实例共享连接池

    Args:
        http_client: session级别的HTTP客户端

    Returns:
        H5CardAPI: H5系统API实例
    """
    return H5CardAPI(http_client)


@pytest.fixture(scope="function")
def admin_consumption_api(http_client) -> AdminConsumptionAPI:
    """提供Admin管理端消费记录API实例

    作用域: function - 每个测试独立
    注入: session级别的http_client,多个API实例共享连接池

    Args:
        http_client: session级别的HTTP客户端

    Returns:
        AdminConsumptionAPI: Admin系统API实例
    """
    return AdminConsumptionAPI(http_client)


# ========== 数据生成器 Fixtures ==========

@pytest.fixture(scope="session")
def data_gen() -> DataGenerator:
    """提供数据生成器

    作用域: session
    用途: 生成测试数据（随机字符串、数字等）

    Returns:
        DataGenerator: 数据生成器实例
    """
    return DataGenerator(locale="zh_CN")


# ========== Pytest Hooks ==========

def pytest_configure(config):
    """
    Pytest配置钩子

    执行时机: pytest启动时
    作用: 添加自定义标记、Allure环境信息等

    v1.1.0: 添加Allure环境信息
    """
    # 添加自定义标记
    config.addinivalue_line("markers", "smoke: 冒烟测试")
    config.addinivalue_line("markers", "regression: 回归测试")
    config.addinivalue_line("markers", "slow: 慢速测试")

    # v1.1.0: 添加Allure环境信息
    AllureHelper.add_environment_info({
        "环境": settings.env,
        "API地址": settings.api_base_url,
        "Python版本": "3.11+",
        "框架版本": "1.1.0",
        "测试类型": "礼品卡API测试",
    })


def pytest_collection_modifyitems(items):
    """修改测试项

    执行时机: 收集完测试用例后
    作用: 动态修改测试项（添加标记、修改名称等）

    Args:
        items: 收集到的测试项列表
    """
    for item in items:
        # 为特定路径的测试添加标签
        if "test_gift_card" in str(item.fspath):
            item.add_marker(pytest.mark.allure_label("feature", "礼品卡管理"))
```

### 4.3 conftest关键设计点

#### 🔑 设计点1: Fixture作用域

```python
# ✅ 正确: http_client是session级别
@pytest.fixture(scope="session")
def http_client():
    """所有测试共享，只创建一次"""
    pass

# ✅ 正确: API是function级别
@pytest.fixture(scope="function")
def user_api(http_client):
    """每个测试独立，但共享http_client"""
    return UserAPI(http_client)
```

**为什么这样设计？**
- `http_client` session级别 → 连接池复用 → 性能最优
- API function级别 → 测试隔离 → 互不影响

#### 🔑 设计点2: 依赖注入

```python
# ✅ 正确: 注入http_client
@pytest.fixture(scope="function")
def user_api(http_client):
    return UserAPI(http_client)

# ❌ 错误: 在fixture内部创建http_client
@pytest.fixture(scope="function")
def user_api():
    client = HttpClient(...)  # 每个测试都创建新连接
    return UserAPI(client)
```

#### 🔑 设计点3: 自动清理

```python
# ✅ 使用yield自动清理
@pytest.fixture(scope="session")
def http_client():
    client = HttpClient(...)
    yield client
    client.close()  # 自动清理

# ✅ 使用上下文管理器
@pytest.fixture(scope="function")
def db_session(db):
    with db.session() as session:
        yield session
        session.rollback()  # 自动回滚
```

---

## 5. 配置管理最佳实践

### 5.1 配置方式对比

| 配置方式 | 优点 | 缺点 | 适用场景 |
|---------|------|------|---------|
| **pydantic-settings + .env** | 类型安全、自动验证、环境变量支持 | 需要定义Settings类 | ✅ **推荐**（gift-card-test使用） |
| **YAML文件** | 可读性好、支持复杂结构 | 需要手动解析、无类型检查 | 配置复杂时 |
| **JSON文件** | 标准格式、工具支持好 | 不支持注释、可读性差 | 不推荐 |
| **环境变量only** | 简单直接、云原生 | 大量配置难管理 | 简单场景 |

### 5.2 推荐方案：pydantic-settings + .env

**为什么推荐？**
1. ✅ **类型安全** - Pydantic自动验证配置类型
2. ✅ **优先级清晰** - 环境变量 > .env文件 > 默认值
3. ✅ **多环境支持** - .env.test、.env.dev、.env.prod
4. ✅ **敏感信息隔离** - .env文件不提交到git
5. ✅ **IDE支持** - 完整的类型提示和自动补全

### 5.3 完整实现示例（基于gift-card-test）

#### 步骤1: 创建 config/settings.py

```python
# config/settings.py
import os
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """项目配置类

    配置优先级:
    1. 环境变量（最高优先级）
    2. .env文件
    3. 默认值
    """

    # ========== 环境配置 ==========
    env: Literal["dev", "test", "prod"] = "test"

    # ========== API配置 ==========
    api_base_url: str = "http://localhost:8080"
    api_timeout: int = 30

    # ========== 数据库配置 ==========
    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str = "test_db"
    db_user: str = "root"
    db_password: str = "password"
    db_charset: str = "utf8mb4"

    @property
    def db_connection_string(self) -> str:
        """构建数据库连接字符串"""
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
            f"?charset={self.db_charset}"
        )

    # ========== Redis配置 ==========
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""

    # ========== 测试配置 ==========
    parallel_workers: int = 4
    retry_times: int = 2
    log_level: str = "INFO"

    # ========== 业务配置 ==========
    default_card_amount: str = "100.00"
    test_user_id: str = "test_user_001"
    test_template_id: str = "TMPL_001"

    model_config = SettingsConfigDict(
        env_file=".env",  # 从.env文件读取
        env_file_encoding="utf-8",
        case_sensitive=False,  # 环境变量不区分大小写
        extra="ignore",  # 忽略额外字段
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 根据ENV环境变量自动加载对应的.env文件
        env = os.getenv("ENV", self.env)
        env_file = f".env.{env}"

        if os.path.exists(env_file):
            self.model_config["env_file"] = env_file


# 全局配置实例
settings = Settings()
```

#### 步骤2: 创建 .env.example（模板文件）

```bash
# .env.example - 配置模板（提交到git）
# 复制此文件为 .env.dev, .env.test, .env.prod 并修改相应配置

# ========== 环境 ==========
ENV=test

# ========== API配置 ==========
API_BASE_URL=http://localhost:8080
API_TIMEOUT=30

# ========== 数据库配置 ==========
DB_HOST=localhost
DB_PORT=3306
DB_NAME=gift_card_test
DB_USER=root
DB_PASSWORD=password
DB_CHARSET=utf8mb4

# ========== Redis配置 ==========
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# ========== 测试配置 ==========
PARALLEL_WORKERS=4
RETRY_TIMES=2
LOG_LEVEL=INFO

# ========== 业务配置 ==========
DEFAULT_CARD_AMOUNT=100.00
TEST_USER_ID=test_user_001
TEST_TEMPLATE_ID=TMPL_001
```

#### 步骤3: 创建不同环境的配置文件

```bash
# .env.test - 测试环境（不提交到git）
ENV=test
API_BASE_URL=http://test-api.example.com
API_TIMEOUT=30
DB_HOST=test-db.example.com
DB_PASSWORD=test_password
LOG_LEVEL=DEBUG
```

```bash
# .env.prod - 生产环境（不提交到git）
ENV=prod
API_BASE_URL=http://api.example.com
API_TIMEOUT=60
DB_HOST=prod-db.example.com
DB_PASSWORD=prod_password
LOG_LEVEL=INFO
```

#### 步骤4: 配置 .gitignore

```gitignore
# .gitignore
# 环境配置文件（包含敏感信息）
.env
.env.test
.env.dev
.env.prod

# 但保留模板文件
!.env.example
```

### 5.4 使用配置

#### 在测试代码中使用

```python
# tests/conftest.py
from config.settings import settings

@pytest.fixture(scope="session")
def http_client() -> HttpClient:
    """使用配置创建HTTP客户端"""
    client = HttpClient(
        base_url=settings.api_base_url,  # 从配置读取
        timeout=settings.api_timeout,     # 从配置读取
    )
    yield client
    client.close()

@pytest.fixture(scope="session")
def db() -> Database:
    """使用配置创建数据库连接"""
    database = Database(settings.db_connection_string)  # 使用@property
    yield database
    database.close()
```

#### 在API类中使用

```python
# api/user_api.py
from config.settings import settings

class UserAPI(BaseAPI):
    def create_user(self, name: str):
        # 可以使用业务配置
        default_age = settings.default_user_age
        return self.post("/users", json={"name": name, "age": default_age})
```

### 5.5 环境切换

#### 方式1: 通过ENV环境变量切换

```bash
# 使用测试环境（自动加载.env.test）
ENV=test uv run pytest

# 使用开发环境（自动加载.env.dev）
ENV=dev uv run pytest

# 使用生产环境（自动加载.env.prod）
ENV=prod uv run pytest
```

#### 方式2: 通过环境变量覆盖配置

```bash
# 临时覆盖API地址
API_BASE_URL=http://another-api.com uv run pytest

# 临时覆盖日志级别
LOG_LEVEL=DEBUG uv run pytest

# 同时覆盖多个配置
API_BASE_URL=http://api.com LOG_LEVEL=DEBUG uv run pytest
```

#### 方式3: 在CI/CD中使用

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Run tests
        env:
          ENV: test
          API_BASE_URL: ${{ secrets.TEST_API_URL }}
          DB_PASSWORD: ${{ secrets.TEST_DB_PASSWORD }}
        run: |
          uv run pytest
```

### 5.6 配置最佳实践

#### ✅ DO - 推荐做法

```python
# ✅ 使用类型提示
api_timeout: int = 30  # IDE可以检查类型

# ✅ 使用 Literal 限制枚举值
env: Literal["dev", "test", "prod"] = "test"

# ✅ 使用 @property 计算属性
@property
def db_connection_string(self) -> str:
    return f"mysql+pymysql://..."

# ✅ 提供合理的默认值
log_level: str = "INFO"

# ✅ 使用描述性的配置名
api_base_url: str  # 清晰明确
```

#### ❌ DON'T - 避免的做法

```python
# ❌ 硬编码敏感信息
api_key = "sk_live_xxx"  # 应该从环境变量读取

# ❌ 配置名不清晰
url: str  # 什么URL？改为 api_base_url

# ❌ 没有默认值
timeout: int  # 应该提供默认值

# ❌ 没有类型提示
api_url = "..."  # 应该 api_url: str = "..."
```

### 5.7 常见问题

#### Q: 为什么不用YAML配置？

**A**: YAML适合复杂嵌套配置，但缺点明显：
- ❌ 无类型检查
- ❌ 需要手动解析
- ❌ 没有IDE支持
- ❌ 不支持环境变量覆盖

**pydantic-settings的优势**:
- ✅ 类型安全
- ✅ 自动验证
- ✅ IDE支持
- ✅ 环境变量优先级

#### Q: 敏感信息如何管理？

**A**: 使用 .env 文件 + .gitignore
```gitignore
# .gitignore
.env
.env.test
.env.prod
```

**生产环境**:
- 使用环境变量（Docker、K8s）
- 使用密钥管理服务（AWS Secrets Manager、Azure Key Vault）

#### Q: 如何在不同环境使用不同配置？

**A**: 创建多个 .env 文件
```bash
.env.dev   # 开发环境
.env.test  # 测试环境
.env.prod  # 生产环境
```

通过 `ENV` 环境变量切换:
```bash
ENV=prod uv run pytest  # 自动加载 .env.prod
```

---

## 6. E2E测试编写指南

### 6.1 什么是E2E测试？

**E2E (End-to-End)** 测试模拟完整的业务流程，验证多个系统协同工作。

**示例**: 礼品卡完整流程
```
Master创建卡 → H5查询卡 → H5支付 → 查询支付结果 → 查询消费记录 → Admin管理查询 → H5退款
```

### 6.2 E2E测试编写模板

基于 `gift-card-test/tests/api/test_e2e/test_complete_flow.py` 的最佳实践：

```python
# tests/api/test_e2e/test_complete_flow.py
"""E2E完整流程测试

测试礼品卡系统的完整业务流程:
Master创建卡 -> H5用户查询 -> H5支付 -> 查询支付结果 -> 查询消费记录 -> Admin查询管理 -> H5退款
"""

import pytest
import allure
from decimal import Decimal
from df_test_framework.plugins import attach_json, step
from models.request.master_card import MasterCardCreateRequest
from models.request.h5_card import H5MyCardsRequest, H5PaymentRequest
from config.settings import settings


@allure.epic("礼品卡系统")
@allure.feature("E2E端到端测试")
@allure.story("完整业务流程")
class TestCompleteFlow:
    """礼品卡系统完整业务流程测试"""

    @allure.title("完整流程:创建->查询->支付->查询结果->消费记录->退款")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_complete_gift_card_flow(
        self,
        master_card_api,  # Master系统API
        h5_card_api,      # H5系统API
        admin_consumption_api,  # Admin系统API
        db  # 数据库（用于验证）
    ):
        """测试礼品卡完整业务流程

        业务流程:
        1. Master系统批量创建礼品卡
        2. H5用户查询自己的礼品卡
        3. H5用户使用礼品卡支付
        4. H5查询支付结果
        5. H5查询消费记录
        6. Admin管理端查询消费记录
        7. H5用户退款
        8. 验证退款后余额恢复
        """
        test_user_id = f"E2E_USER_{settings.test_user_id}"
        create_order_no = f"E2E_CREATE_{settings.test_user_id}"
        payment_order_no = f"E2E_PAY_{settings.test_user_id}"
        payment_amount = Decimal("70.00")

        # ========== 步骤1: Master创建礼品卡 ==========
        with step("步骤1: Master系统批量创建2张礼品卡"):
            create_request = MasterCardCreateRequest(
                customer_order_no=create_order_no,
                user_id=test_user_id,
                template_id=settings.test_template_id,
                quantity=2
            )
            create_response = master_card_api.create_cards(create_request)
            attach_json(create_response.model_dump(), name="1-创建礼品卡响应")

            # 验证创建成功
            assert create_response.success, f"创建失败: {create_response.message}"
            assert create_response.data.quantity == 2
            assert len(create_response.data.card_nos) == 2

            card_no_1 = create_response.data.card_nos[0]
            card_no_2 = create_response.data.card_nos[1]

            # Allure报告附件
            allure.attach(
                f"创建的卡号: {card_no_1}, {card_no_2}",
                name="卡号信息",
                attachment_type=allure.attachment_type.TEXT
            )

        # ========== 步骤2: H5查询用户礼品卡 ==========
        with step("步骤2: H5用户查询自己的礼品卡列表"):
            query_request = H5MyCardsRequest(user_id=test_user_id)
            query_response = h5_card_api.get_my_cards(query_request)
            attach_json(query_response.model_dump(), name="2-查询礼品卡响应")

            # 验证查询成功
            assert query_response.success
            assert query_response.data.available_card_count >= 2
            assert query_response.data.total_balance >= Decimal("200.00")

            # 验证创建的卡都在列表中
            card_nos_in_list = [card.card_no for card in query_response.data.cards]
            assert card_no_1 in card_nos_in_list
            assert card_no_2 in card_nos_in_list

        # ========== 步骤3: H5支付 ==========
        with step(f"步骤3: H5用户使用礼品卡支付{payment_amount}元"):
            payment_request = H5PaymentRequest(
                user_id=test_user_id,
                customer_order_no=payment_order_no,
                total_amount=payment_amount,
                card_list=f"{card_no_1},{card_no_2}"  # 使用两张卡支付
            )
            payment_response = h5_card_api.pay(payment_request)
            attach_json(payment_response.model_dump(), name="3-支付响应")

            # 验证支付成功
            assert payment_response.success, f"支付失败: {payment_response.message}"
            assert payment_response.data.total_amount == payment_amount
            payment_no = payment_response.data.payment_no

        # ... 后续步骤（查询支付结果、消费记录、退款等）

        # 测试总结
        allure.attach(
            "E2E完整流程测试通过!\\n"
            "流程: 创建卡 -> 查询卡 -> 支付 -> 查询结果 -> 消费记录 -> Admin管理 -> 退款 -> 余额恢复",
            name="测试总结",
            attachment_type=allure.attachment_type.TEXT
        )
```

### 6.3 E2E测试最佳实践

#### ✅ 实践1: 使用 `step()` 清晰划分步骤

```python
from df_test_framework.plugins import step

with step("步骤1: 创建礼品卡"):
    # 步骤1的代码

with step("步骤2: 查询礼品卡"):
    # 步骤2的代码
```

**优势**:
- 报告中清晰显示每个步骤
- 失败时快速定位到具体步骤
- 代码结构清晰

#### ✅ 实践2: 使用 `attach_json()` 附加响应

```python
from df_test_framework.plugins import attach_json

response = api.create_card(...)
attach_json(response.model_dump(), name="创建响应")
```

**优势**:
- Allure报告中可查看完整响应
- 便于问题排查
- 自动格式化JSON

#### ✅ 实践3: 逐步验证，失败快速定位

```python
# ✅ 推荐: 每步都验证
with step("步骤1: 创建"):
    response = api.create()
    assert response.success  # 立即验证

with step("步骤2: 查询"):
    result = api.query()
    assert result is not None  # 立即验证

# ❌ 不推荐: 所有步骤执行完再验证
response1 = api.create()
response2 = api.query()
assert response1.success  # 失败时不知道是步骤1还是步骤2的问题
assert response2.success
```

#### ✅ 实践4: 使用唯一标识避免数据冲突

```python
# ✅ 推荐: 使用唯一ID
test_user_id = f"E2E_USER_{settings.test_user_id}_{uuid.uuid4()}"

# ❌ 不推荐: 固定ID
test_user_id = "E2E_USER_001"  # 并发测试时会冲突
```

---

## 7. 真实项目案例解读

### 7.1 gift-card-test 项目概览

**项目地址**: `D:\Git\DF\qa\gift-card-test`

**项目特点**:
- ✅ 生产级测试项目
- ✅ 完整的依赖注入模式
- ✅ 清晰的分层架构
- ✅ 完整的E2E测试
- ✅ 使用框架v1.1.0所有特性

### 7.2 关键文件解读

#### 📄 tests/conftest.py - 核心配置

**路径**: `gift-card-test/tests/conftest.py`

**关键代码解析**:
```python
# 第39-47行: session级别的http_client
@pytest.fixture(scope="session")
def http_client() -> HttpClient:
    """所有测试共享一个HTTP客户端"""
    client = HttpClient(
        base_url=settings.api_base_url,
        timeout=settings.api_timeout,
    )
    yield client
    client.close()

# 第76-82行: function级别的API
@pytest.fixture(scope="function")
def master_card_api(http_client) -> MasterCardAPI:
    """每个测试独立API实例，但共享http_client"""
    return MasterCardAPI(http_client)
```

**设计亮点**:
- ✅ session + function 的完美组合
- ✅ 性能最优（连接池复用）
- ✅ 测试隔离（独立API实例）

#### 📄 api/master_card_api.py - API封装

**路径**: `gift-card-test/api/master_card_api.py`

**关键代码解析**:
```python
# 第43-44行: 使用装饰器
@track_performance(threshold_ms=500)  # 性能监控
@retry_on_failure(max_retries=2, delay=1)  # 自动重试
def create_cards(self, request: MasterCardCreateRequest):
    """框架v1.1.0的新特性"""
    pass

# 第78-86行: 字段映射
response = self.client.post(
    endpoint,
    data={  # 注意: 使用data而非json
        "customerOrderNo": request.customer_order_no,  # 字段名转换
        "userId": request.user_id,
        "templateId": request.template_id,
        "quantity": request.quantity,
    }
)
```

**设计亮点**:
- ✅ 使用装饰器增强功能
- ✅ 正确处理form data
- ✅ 字段名自动转换

#### 📄 tests/api/test_e2e/test_complete_flow.py - E2E测试

**路径**: `gift-card-test/tests/api/test_e2e/test_complete_flow.py`

**关键代码解析**:
```python
# 第37-43行: 使用多个API fixture
def test_complete_gift_card_flow(
    self,
    master_card_api,  # Master系统
    h5_card_api,      # H5系统
    admin_consumption_api,  # Admin系统
    db  # 数据库
):
    """3个API实例，共享1个http_client，性能最优"""
    pass

# 第62-82行: 使用step划分步骤
with step("步骤1: Master系统批量创建2张礼品卡"):
    create_request = MasterCardCreateRequest(...)
    create_response = master_card_api.create_cards(create_request)
    attach_json(create_response.model_dump(), name="1-创建礼品卡响应")

    assert create_response.success
    # ... 详细验证
```

**设计亮点**:
- ✅ 完整的业务流程覆盖
- ✅ 清晰的步骤划分
- ✅ 详细的Allure报告

### 7.3 项目亮点总结

| 亮点 | 说明 | 参考文件 |
|------|------|---------|
| **依赖注入** | session级http_client + function级API | `conftest.py:39-82` |
| **性能优化** | 连接池复用、装饰器监控 | `master_card_api.py:43-44` |
| **E2E测试** | 完整业务流程、清晰步骤 | `test_complete_flow.py` |
| **数据模型** | Pydantic验证、清晰分层 | `models/` 目录 |
| **Allure增强** | step、attach_json | 所有测试文件 |

---

## 8. 常见问题和最佳实践

### 8.1 常见问题

#### ❓ Q1: 为什么要分request和response目录？

**A**: 职责分离，便于维护

```
models/
├── request/      # 我发送的数据（我控制）
└── response/     # API返回的数据（API控制）
```

**优势**:
- 清晰知道哪些是输入，哪些是输出
- 请求模型可以有严格验证
- 响应模型需要宽松解析（`extra="ignore"`）

#### ❓ Q2: API类应该放在哪个作用域？

**A**: function级别（推荐）

```python
# ✅ 推荐: function级别
@pytest.fixture(scope="function")
def user_api(http_client):
    return UserAPI(http_client)

# ❌ 不推荐: session级别
@pytest.fixture(scope="session")
def user_api(http_client):
    return UserAPI(http_client)  # 所有测试共享，可能相互影响
```

**原因**:
- function级别: 测试隔离，不会相互影响
- session级别: 可能有状态污染

#### ❓ Q3: 何时使用数据库fixture？

**A**: 只在需要数据验证时使用

```python
# 场景1: 验证数据是否正确写入数据库
def test_create_user(user_api, db):
    user = user_api.create_user(name="张三")

    # 数据库验证
    db_user = db.query_user_by_id(user.id)
    assert db_user.name == "张三"

# 场景2: 纯API测试，不需要数据库
def test_get_user(user_api):
    user = user_api.get_user(1)
    assert user.name is not None
```

#### ❓ Q4: conftest.py可以有多个吗？

**A**: 可以，按目录分层

```
tests/
├── conftest.py              # 全局配置
├── api/
│   ├── conftest.py         # API测试专用
│   └── test_user.py
└── ui/
    ├── conftest.py         # UI测试专用
    └── test_login.py
```

**原则**:
- 全局配置放根目录
- 特定模块配置放子目录

#### ❓ Q5: 如何处理测试数据依赖？

**A**: 使用fixture链式依赖

```python
@pytest.fixture
def user(user_api):
    """创建测试用户"""
    return user_api.create_user(name="张三")

@pytest.fixture
def order(order_api, user):
    """创建测试订单（依赖user）"""
    return order_api.create_order(user_id=user.id, amount=100)

def test_order_payment(order, payment_api):
    """测试支付（自动创建user和order）"""
    result = payment_api.pay(order.id)
    assert result.success
```

### 8.2 最佳实践清单

#### ✅ 项目结构

- [ ] 按系统/模块组织目录
- [ ] request和response分离
- [ ] API类和测试类对应
- [ ] 使用清晰的命名规则

#### ✅ 数据模型

- [ ] 使用Pydantic进行验证
- [ ] 响应模型使用 `extra="ignore"`
- [ ] 请求模型添加严格验证
- [ ] 添加清晰的文档字符串

#### ✅ API封装

- [ ] 继承BaseAPI
- [ ] 使用依赖注入
- [ ] 选择合适的响应解析模式
- [ ] 添加装饰器（性能、重试）

#### ✅ 测试编写

- [ ] 使用pytest fixtures
- [ ] E2E测试使用step
- [ ] 添加Allure标注
- [ ] 逐步验证，快速定位

#### ✅ conftest配置

- [ ] http_client使用session级别
- [ ] API使用function级别
- [ ] 添加必要的hooks
- [ ] 清晰的注释说明

---

## 🎓 总结

### 本指南核心要点

1. **项目结构** - 按系统分类、职责清晰
2. **数据模型** - request/response分离、Pydantic验证
3. **API封装** - 依赖注入、两种解析模式
4. **conftest配置** - session+function组合
5. **E2E测试** - step划分、逐步验证
6. **真实案例** - gift-card-test完整参考

### 推荐学习路径

1. ✅ 阅读本文档，理解设计理念
2. ✅ 查看 gift-card-test 项目源码
3. ✅ 跟着 [30分钟快速上手指南](../guides/30分钟快速上手指南.md) 创建项目
4. ✅ 参考本文档完善项目结构
5. ✅ 阅读 [BaseAPI最佳实践](./BaseAPI最佳实践指南.md) 深入学习

### 参考资料

- [30分钟快速上手指南](../guides/30分钟快速上手指南.md) - 快速开始
- [使用示例](../guides/使用示例.md) - API参考
- [BaseAPI最佳实践](./BaseAPI最佳实践指南.md) - 设计模式
- [为什么选择测试框架](./为什么选择测试框架.md) - 框架价值
- [架构设计文档](./架构设计文档.md) - 深入架构

---

**祝你开发出高质量的测试项目！** 🚀
