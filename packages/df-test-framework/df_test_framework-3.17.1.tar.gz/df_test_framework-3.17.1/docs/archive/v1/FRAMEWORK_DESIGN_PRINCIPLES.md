# 框架设计原则与职责边界

> **文档版本**: v1.3.0  
> **最后更新**: 2025-10-30  
> ⚠️ **Legacy**: 本文档概述的是 v1.x 架构原则，供历史对照。规划 v2 及以后的设计时，请参考最新的 [DF 测试框架 v2 架构改造方案](../migration/rearchitecture_plan.md)。

## 📋 目录

1. [框架定位](#框架定位)
2. [职责边界](#职责边界)
3. [设计原则](#设计原则)
4. [模块分类](#模块分类)
5. [使用指南](#使用指南)

---

## 框架定位

**df-test-framework** 是一个**现代化的、可复用的Python测试自动化框架**,支持API和UI测试。

### 核心定位

- ✅ **通用基础设施** - 提供可复用的测试基础能力
- ✅ **设计模式支持** - 提供经典设计模式的实现
- ✅ **插件化扩展** - 支持测试项目根据业务需求扩展
- ❌ **非业务框架** - 不包含任何业务相关的逻辑

---

## 职责边界

### ✅ 框架应该包含的内容

#### 1. 核心基础设施
- HTTP客户端封装
- 数据库连接管理
- Redis连接管理
- 日志系统
- 配置管理

#### 2. 设计模式基类
- Repository基类 - `BaseRepository`
- Builder基类 - `BaseBuilder`, `DictBuilder`
- Cleaner基类 - `BaseTestDataCleaner`, `GenericTestDataCleaner`

#### 3. 通用工具
- 装饰器(缓存、性能监控等)
- 断言辅助
- 数据生成工具
- 性能监控工具

#### 4. Pytest集成
- 通用fixtures
- 通用plugins
- Markers定义

#### 5. 示例代码
- **仅用于参考** - 在 `使用示例.md` 文件中
- **不被框架直接使用** - 测试项目根据需要参考

---

### ❌ 框架不应该包含的内容

#### 1. 业务相关实现
```python
# ❌ 不应该在框架中
class CardRepository(BaseRepository):
    def find_by_card_no(self, card_no: str):
        ...  # 卡片是业务概念

# ❌ 不应该在框架中
@pytest.fixture
def auto_cleanup_cards(db):
    ...  # 清理卡片是业务逻辑

# ❌ 不应该在框架中
class CardRequestBuilder(BaseBuilder):
    def with_card_no(self, card_no: str):
        ...  # 卡片请求是业务模型
```

#### 2. 业务相关的fixtures
```python
# ❌ 不应该在框架中
@pytest.fixture
def card_cleaner(db):
    ...  # 卡片清理是业务相关

@pytest.fixture
def master_card_api(http_client):
    ...  # 具体API是业务相关
```

#### 3. 业务模型和Schema
```python
# ❌ 不应该在框架中
class CardModel(BaseModel):
    card_no: str
    ...  # 卡片模型是业务相关

class OrderResponse(BaseModel):
    order_id: str
    ...  # 订单响应是业务相关
```

---

## 设计原则

### 1. 开放封闭原则 (OCP)
- **对扩展开放**: 提供基类和抽象,允许测试项目扩展
- **对修改封闭**: 框架核心代码不应因业务需求而修改

### 2. 依赖倒置原则 (DIP)
- 依赖于抽象,不依赖于具体实现
- 提供接口和基类,具体实现在测试项目中

### 3. 单一职责原则 (SRP)
- 每个模块只负责一个职责
- 框架只负责提供通用基础设施

### 4. 最少知识原则 (LoD)
- 框架不应该知道业务细节
- 测试项目不应该修改框架核心代码

---

## 模块分类

### 核心模块 (通用基础设施)

| 模块 | 职责 | 是否包含业务 |
|------|------|--------------|
| `core/` | HTTP、数据库、Redis核心能力 | ❌ 无 |
| `config/` | 配置管理 | ❌ 无 |
| `utils/` | 通用工具函数 | ❌ 无 |
| `monitoring/` | 性能监控 | ❌ 无 |

### 设计模式模块 (基础设施 + 示例)

| 模块 | 基础设施 | 示例代码 |
|------|----------|----------|
| `repositories/` | `BaseRepository` | `examples.py` (仅参考) |
| `builders/` | `BaseBuilder`, `DictBuilder` | `examples.py` (仅参考) |
| `fixtures/cleanup.py` | `BaseTestDataCleaner` | `cleanup_examples.py` (仅参考) |

### Fixtures模块 (通用 + 项目特定)

| Fixture | 类型 | 说明 |
|---------|------|------|
| `generic_data_cleaner` | ✅ 通用 | 基于回调的清理器 |
| `api_performance_tracker` | ✅ 通用 | API性能追踪 |
| `slow_query_monitor` | ✅ 通用 | 慢查询监控 |
| `http_client_fixture` | ✅ 通用 | HTTP客户端 |
| `db_fixture` | ✅ 通用 | 数据库连接 |

---

## 使用指南

### 正确的使用方式

#### 1. 在测试项目中创建业务相关的Repository

```python
# your-test-project/repositories/card_repository.py

from df_test_framework.repositories import BaseRepository

class CardRepository(BaseRepository):
    '''卡片Repository - 业务相关,属于测试项目'''

    def __init__(self, db):
        super().__init__(db, table_name="card_inventory")

    def find_by_card_no(self, card_no: str):
        return self.find_one({"card_no": card_no})
```

#### 2. 在测试项目中创建业务相关的Builder

```python
# your-test-project/builders/card_builder.py

from df_test_framework.builders import BaseBuilder

class CardRequestBuilder(BaseBuilder):
    '''卡片请求Builder - 业务相关,属于测试项目'''

    def __init__(self):
        self._card_no = "CARD001"
        self._user_id = "user_001"

    def with_card_no(self, card_no: str):
        self._card_no = card_no
        return self

    def build(self):
        return CardCreateRequest(
            card_no=self._card_no,
            user_id=self._user_id
        )
```

#### 3. 在测试项目中创建业务相关的Cleaner

```python
# your-test-project/cleaners/card_cleaner.py

from df_test_framework.fixtures.cleanup import BaseTestDataCleaner

class CardTestDataCleaner(BaseTestDataCleaner):
    '''卡片数据清理器 - 业务相关,属于测试项目'''

    def cleanup(self):
        # 清理卡片
        if self.resources.get("card_nos"):
            self.db.execute(
                "DELETE FROM card_inventory WHERE card_no IN :ids",
                {"ids": tuple(self.resources["card_nos"])}
            )
```

#### 4. 在测试项目的conftest.py中创建fixtures

```python
# your-test-project/conftest.py

import pytest
from repositories.card_repository import CardRepository
from cleaners.card_cleaner import CardTestDataCleaner

@pytest.fixture
def card_repo(db):
    '''卡片Repository fixture - 业务相关,属于测试项目'''
    return CardRepository(db)

@pytest.fixture
def card_cleaner(db):
    '''卡片清理器fixture - 业务相关,属于测试项目'''
    cleaner = CardTestDataCleaner(db)
    yield cleaner
    cleaner.cleanup()
```

#### 5. 在测试中使用

```python
# your-test-project/tests/test_cards.py

def test_create_card(master_card_api, card_repo, card_cleaner):
    # 调用API创建卡片
    response = master_card_api.create_cards(request)

    # 使用Repository验证
    card = card_repo.find_by_card_no(response.data.card_nos[0])
    assert card is not None

    # 注册清理
    card_cleaner.register("card_nos", response.data.card_nos[0])
```

---

## 项目结构推荐

### 框架结构 (df-test-framework)

```
df-test-framework/
├── src/df_test_framework/
│   ├── core/              # ✅ 核心基础设施
│   ├── config/            # ✅ 配置管理
│   ├── utils/             # ✅ 通用工具
│   ├── repositories/      # ✅ Repository基类 + 示例
│   │   ├── base_repository.py   # 基类
│   │   └── examples.py          # 示例(仅参考)
│   ├── builders/          # ✅ Builder基类 + 示例
│   │   ├── base_builder.py      # 基类
│   │   └── examples.py          # 示例(仅参考)
│   ├── fixtures/          # ✅ 通用fixtures
│   │   ├── cleanup.py           # 基类
│   │   └── cleanup_examples.py  # 示例(仅参考)
│   └── monitoring/        # ✅ 性能监控
```

### 测试项目结构 (gift-card-test)

```
gift-card-test/
├── repositories/          # ❌ 业务Repository实现
│   ├── card_repository.py
│   └── order_repository.py
├── builders/              # ❌ 业务Builder实现
│   ├── card_builder.py
│   └── order_builder.py
├── cleaners/              # ❌ 业务Cleaner实现
│   └── data_cleaner.py
├── api/                   # ❌ 业务API实现
│   ├── master_card_api.py
│   └── order_api.py
├── models/                # ❌ 业务模型
│   ├── request.py
│   └── response.py
├── tests/                 # 测试用例
├── conftest.py            # ❌ 业务相关的fixtures
└── config.py              # ❌ 业务配置
```

---

## 重构说明 (v1.3.0)

### 重构内容

为了保持框架的通用性和可复用性,在v1.3.0中进行了以下重构:

#### 1. cleanup.py 重构 ✅

**之前 (v1.2.0)**:
```python
# ❌ 包含业务相关的实现
class TestDataCleaner:
    def register_card(self, card_no: str):  # 卡片是业务概念
        ...

    def _cleanup_cards(self):  # 清理卡片是业务逻辑
        ...
```

**现在 (v1.3.0)**:
```python
# ✅ 只提供通用基类
class BaseTestDataCleaner(ABC):
    def register(self, resource_type: str, resource_id: Any):
        ...  # 通用的注册方法

    @abstractmethod
    def cleanup(self):
        ...  # 子类实现具体清理逻辑

# ✅ 提供基于回调的通用实现
class GenericTestDataCleaner(BaseTestDataCleaner):
    def add_cleanup_callback(self, resource_type, callback):
        ...  # 通过回调支持任意清理逻辑
```

**业务实现示例**:
- 移到 `cleanup_examples.py` 作为参考
- 测试项目根据需要自行实现

#### 2. Repository/Builder examples ✅

**保持方式**:
- `examples.py` 文件明确标注为**示例代码**
- 文件开头说明**仅供参考,不应被框架直接使用**
- 测试项目应根据自己的业务创建实现

---

## 最佳实践

### ✅ DO (推荐)

1. **使用框架的基类** - 继承BaseRepository, BaseBuilder等
2. **在测试项目中实现业务逻辑** - Repository, Builder, Cleaner等
3. **参考examples.py** - 了解如何使用,但不要直接复制
4. **创建项目特定的fixtures** - 在测试项目的conftest.py中
5. **保持框架通用性** - 向框架贡献时,确保是通用能力

### ❌ DON'T (避免)

1. **在框架中添加业务逻辑** - 卡片、订单等业务概念
2. **在框架中创建业务fixtures** - card_cleaner, order_repo等
3. **直接使用examples.py中的代码** - 示例代码不是生产代码
4. **修改框架核心代码** - 除非是通用能力增强
5. **在框架中硬编码业务配置** - 表名、字段名等

---

## 总结

### 框架的价值

1. **提供通用基础设施** - 让测试项目专注于业务测试
2. **提供设计模式支持** - 引导良好的代码组织
3. **提供示例参考** - 帮助快速上手
4. **保持可复用性** - 可以在多个项目中使用

### 测试项目的职责

1. **实现业务相关逻辑** - Repository, Builder, Cleaner等
2. **创建业务fixtures** - 在conftest.py中
3. **定义业务模型** - Request, Response等
4. **实现业务API** - 具体的API类

### 设计哲学

**框架应该是一个工具箱,而不是一个应用。**

- 工具箱提供各种工具(基类、工具函数、设计模式支持)
- 应用使用这些工具来构建具体功能(业务Repository, Builder等)
- 工具箱不应该预设应用的具体业务逻辑

---

**文档版本**: v1.3.0
**最后更新**: 2025-10-30
**作者**: Claude (AI Assistant)
