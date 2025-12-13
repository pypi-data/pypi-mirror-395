# v2.x → v3.0 迁移指南

> 从v2.x升级到v3.0的完整迁移指南

## 📋 概述

v3.0引入了架构重构，采用**基于交互模式的分类方式**，而不是技术栈分类。这使得框架更加语义化、易于理解和扩展。

**关键原则**: v3.0 **不向后兼容** v2.x，但迁移过程简单直接。

---

## 🎯 主要变更

### 1. 导入路径变更

| 功能 | v2.x 导入路径 | v3.0 导入路径 |
|------|--------------|--------------|
| **HTTP客户端** | `from df_test_framework.core.http import HttpClient` | `from df_test_framework.clients.http.rest.httpx import HttpClient` |
| **BaseAPI** | `from df_test_framework.core.http import BaseAPI` | `from df_test_framework.clients.http.rest.httpx import BaseAPI` |
| **BusinessError** | `from df_test_framework.core.http import BusinessError` | `from df_test_framework.clients.http.rest.httpx import BusinessError` |
| **Database** | `from df_test_framework.core.database import Database` | `from df_test_framework.databases.database import Database` |
| **RedisClient** | `from df_test_framework.core.redis import RedisClient` | `from df_test_framework.databases.redis.redis_client import RedisClient` |
| **BaseRepository** | `from df_test_framework.patterns import BaseRepository` | `from df_test_framework.databases.repositories import BaseRepository` |
| **QuerySpec** | `from df_test_framework.patterns import QuerySpec` | `from df_test_framework.databases.repositories import QuerySpec` |
| **BaseBuilder** | `from df_test_framework.patterns import BaseBuilder` | `from df_test_framework.testing.data.builders import BaseBuilder` |
| **DictBuilder** | `from df_test_framework.patterns import DictBuilder` | `from df_test_framework.testing.data.builders import DictBuilder` |
| **BrowserManager** | `from df_test_framework.ui import BrowserManager` | `from df_test_framework.drivers.web import BrowserManager` |
| **BasePage** | `from df_test_framework.ui import BasePage` | `from df_test_framework.drivers.web import BasePage` |

### 2. 顶层导入仍然有效

**好消息**: 如果你使用顶层导入，大部分代码无需修改！

```python
# ✅ 这些导入在v3.0中仍然有效
from df_test_framework import (
    HttpClient,
    BaseAPI,
    BusinessError,
    Database,
    RedisClient,
    BaseRepository,
    QuerySpec,
    BaseBuilder,
    DictBuilder,
    BrowserManager,
    BasePage,
)
```

---

## 🔧 迁移步骤

### Step 1: 全局搜索替换

在你的项目中执行以下替换：

```bash
# 1. HTTP客户端
from df_test_framework.core.http import
→ from df_test_framework.clients.http.rest.httpx import

# 2. 数据库
from df_test_framework.core.database import
→ from df_test_framework.databases.database import

# 3. Redis
from df_test_framework.core.redis import
→ from df_test_framework.databases.redis.redis_client import

# 4. Repository
from df_test_framework.patterns import BaseRepository
→ from df_test_framework.databases.repositories import BaseRepository

from df_test_framework.patterns import QuerySpec
→ from df_test_framework.databases.repositories import QuerySpec

# 5. Builder
from df_test_framework.patterns import BaseBuilder
→ from df_test_framework.testing.data.builders import BaseBuilder

from df_test_framework.patterns import DictBuilder
→ from df_test_framework.testing.data.builders import DictBuilder

# 6. UI驱动
from df_test_framework.ui import
→ from df_test_framework.drivers.web import
```

### Step 2: 更新依赖版本

```bash
# pyproject.toml 或 requirements.txt
df-test-framework = "^3.0.0"  # 更新版本号
```

### Step 3: 运行测试

```bash
# 运行测试确保一切正常
pytest tests/
```

---

## 💡 迁移示例

### 示例1: API测试类

**Before (v2.x)**:
```python
from df_test_framework.core.http import BaseAPI, BusinessError

class UserAPI(BaseAPI):
    def get_user(self, user_id: str):
        return self.request("GET", f"/users/{user_id}")
```

**After (v3.0)** - 方式1（使用具体路径）:
```python
from df_test_framework.clients.http.rest.httpx import BaseAPI, BusinessError

class UserAPI(BaseAPI):
    def get_user(self, user_id: str):
        return self.request("GET", f"/users/{user_id}")
```

**After (v3.0)** - 方式2（使用顶层导入，推荐）:
```python
from df_test_framework import BaseAPI, BusinessError

class UserAPI(BaseAPI):
    def get_user(self, user_id: str):
        return self.request("GET", f"/users/{user_id}")
```

### 示例2: Repository类

**Before (v2.x)**:
```python
from df_test_framework.patterns import BaseRepository, QuerySpec
from df_test_framework.core.database import Database

class UserRepository(BaseRepository):
    def __init__(self, db: Database):
        super().__init__(db, table_name="users")

    def find_active_users(self):
        spec = QuerySpec.where("status", "==", "active")
        return self.find_all_by_spec(spec)
```

**After (v3.0)** - 方式1（使用具体路径）:
```python
from df_test_framework.databases.repositories import BaseRepository, QuerySpec
from df_test_framework.databases.database import Database

class UserRepository(BaseRepository):
    def __init__(self, db: Database):
        super().__init__(db, table_name="users")

    def find_active_users(self):
        spec = QuerySpec.where("status", "==", "active")
        return self.find_all_by_spec(spec)
```

**After (v3.0)** - 方式2（使用顶层导入，推荐）:
```python
from df_test_framework import BaseRepository, QuerySpec, Database

class UserRepository(BaseRepository):
    def __init__(self, db: Database):
        super().__init__(db, table_name="users")

    def find_active_users(self):
        spec = QuerySpec.where("status", "==", "active")
        return self.find_all_by_spec(spec)
```

### 示例3: UI测试类

**Before (v2.x)**:
```python
from df_test_framework.ui import BasePage, BrowserManager

class LoginPage(BasePage):
    def login(self, username: str, password: str):
        self.fill("#username", username)
        self.fill("#password", password)
        self.click("#login-btn")
```

**After (v3.0)** - 方式1（使用具体路径）:
```python
from df_test_framework.drivers.web import BasePage, BrowserManager

class LoginPage(BasePage):
    def login(self, username: str, password: str):
        self.fill("#username", username)
        self.fill("#password", password)
        self.click("#login-btn")
```

**After (v3.0)** - 方式2（使用顶层导入，推荐）:
```python
from df_test_framework import BasePage, BrowserManager

class LoginPage(BasePage):
    def login(self, username: str, password: str):
        self.fill("#username", username)
        self.fill("#password", password)
        self.click("#login-btn")
```

---

## 🆕 新功能

v3.0带来了许多新特性，你可以逐步采用：

### 1. Factory模式

```python
# 使用Factory创建客户端
from df_test_framework.clients.http.rest import RestClientFactory

# 创建httpx客户端
client = RestClientFactory.create("httpx", config=http_config)

# 未来可轻松切换到requests
# client = RestClientFactory.create("requests", config=http_config)
```

### 2. Protocol定义

```python
# 使用Protocol确保类型安全
from df_test_framework.clients.http.rest.protocols import RestClientProtocol

def use_client(client: RestClientProtocol):
    # 任何符合RestClientProtocol的客户端都可以
    response = client.get("/api/users")
```

### 3. 数据库Factory

```python
from df_test_framework.databases import DatabaseFactory

# 便捷方法创建MySQL数据库
db = DatabaseFactory.create_mysql(
    connection_string="mysql://user:pass@localhost/db"
)

# 创建Redis客户端
redis = DatabaseFactory.create_redis(host="localhost", port=6379)
```

---

## ⚠️ 注意事项

### 1. 不再支持的模块

以下模块路径在v3.0中已废弃：

- ❌ `df_test_framework.core.http`
- ❌ `df_test_framework.core.database`
- ❌ `df_test_framework.core.redis`
- ❌ `df_test_framework.patterns.repositories`
- ❌ `df_test_framework.patterns.builders`
- ❌ `df_test_framework.ui`

### 2. 目录结构变更

如果你的代码直接依赖文件路径（不推荐），需要注意：

```
v2.x                          v3.0
─────────────────────────────────────────────────
engines/sql/              →  databases/
engines/nosql/            →  databases/
clients/rest/             →  clients/http/rest/
ui/                       →  drivers/web/
```

### 3. 测试文件路径

如果你在测试中使用了模块路径字符串（如动态导入），需要更新：

```python
# Before
importlib.import_module("df_test_framework.core.http")

# After
importlib.import_module("df_test_framework.clients.http.rest.httpx")
```

---

## 📚 更多资源

- [v3.0架构文档](../architecture/REFACTORING_PLAN_V3_REVISED.md)
- [API参考](../api-reference/README.md)
- [快速开始](../user-guide/getting-started.md)

---

## 💬 获取帮助

如果迁移过程中遇到问题：

1. 查看 [FAQ](../faq.md)
2. 提交 [Issue](https://github.com/yourorg/test-framework/issues)
3. 联系维护团队

---

## ✅ 迁移检查清单

使用这个检查清单确保迁移完整：

- [ ] 更新所有 `from df_test_framework.core.*` 导入
- [ ] 更新所有 `from df_test_framework.patterns.*` 导入
- [ ] 更新所有 `from df_test_framework.ui.*` 导入
- [ ] 更新 `pyproject.toml` 或 `requirements.txt` 版本号
- [ ] 运行全部测试并确保通过
- [ ] 更新CI/CD配置（如有）
- [ ] 更新团队文档（如有）

恭喜！迁移完成 🎉
