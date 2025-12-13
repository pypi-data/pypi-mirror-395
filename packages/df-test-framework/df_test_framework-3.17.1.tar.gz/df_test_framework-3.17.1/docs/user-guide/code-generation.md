# 代码生成工具使用指南

> 📚 **版本**: v2.0.0
> 🎯 **目标**: 使用代码生成工具快速创建测试代码，提升开发效率

---

## 📖 目录

- [简介](#简介)
- [快速开始](#快速开始)
- [生成命令详解](#生成命令详解)
  - [生成测试文件](#生成测试文件)
  - [生成Builder类](#生成builder类)
  - [生成Repository类](#生成repository类)
  - [生成API客户端类](#生成api客户端类)
- [实战示例](#实战示例)
- [最佳实践](#最佳实践)
- [常见问题](#常见问题)

---

## 简介

DF Test Framework v2.0 提供了强大的代码生成工具 (`df-test gen`)，可以快速生成：

| 类型 | 命令 | 用途 |
|------|------|------|
| **测试文件** | `df-test gen test` | 生成标准的API测试文件 |
| **Builder类** | `df-test gen builder` | 生成数据构造器类 |
| **Repository类** | `df-test gen repo` | 生成数据仓库类 |
| **API客户端** | `df-test gen api` | 生成API调用封装类 |

**优势**：
- ⚡ **快速**: 秒级生成标准代码模板
- 📦 **规范**: 遵循框架最佳实践
- 🔧 **可定制**: 支持自定义参数
- ✅ **即用**: 生成的代码可直接运行

---

## 快速开始

### 前提条件

#### 1. 创建项目（如果还没有）

使用 `df-test init` 命令创建测试项目：

```bash
# 创建API测试项目（默认）
df-test init my-project

# 或指定项目类型
df-test init my-project --type api     # API测试项目
df-test init my-project --type ui      # UI测试项目（基于Playwright）
df-test init my-project --type full    # 完整项目（API + UI）
```

生成的项目结构：

```bash
my-project/
├── src/my_project/
│   ├── apis/              # API客户端层
│   ├── builders/          # Builder层
│   ├── repositories/      # Repository层
│   ├── models/            # 数据模型
│   ├── utils/             # 工具函数
│   ├── constants/         # 常量定义
│   └── config/            # 配置
├── tests/
│   ├── api/               # API测试
│   └── data/              # 测试数据
├── docs/                  # 文档
├── scripts/               # 脚本
└── reports/               # 测试报告
```

#### 2. 确保在项目根目录下运行

代码生成命令需要在项目根目录（包含`src/`目录）下执行：

```bash
cd my-project
df-test gen test user_login  # ✅ 正确
```

### 基本用法

```bash
# 查看帮助
df-test gen --help

# 生成测试文件
df-test gen test user_login

# 生成Builder类
df-test gen builder user

# 生成Repository类
df-test gen repo user

# 生成API客户端类
df-test gen api user
```

---

## 生成命令详解

### 生成测试文件

#### 命令格式

```bash
df-test gen test <名称> [选项]
```

#### 参数说明

| 参数 | 类型 | 必需 | 说明 | 默认值 |
|------|------|------|------|--------|
| `<名称>` | string | ✅ | 测试名称（如：user_login） | - |
| `--feature` | string | ❌ | Allure feature名称 | 根据名称生成 |
| `--story` | string | ❌ | Allure story名称 | 根据名称生成 |
| `--output-dir` | string | ❌ | 输出目录 | `tests/api/` |
| `--force` | flag | ❌ | 强制覆盖已存在的文件 | `false` |

#### 使用示例

```bash
# 基本用法
df-test gen test user_login

# 指定Allure信息
df-test gen test user_login --feature "用户模块" --story "登录功能"

# 指定输出目录
df-test gen test payment_refund --output-dir tests/api/payment/

# 强制覆盖
df-test gen test user_login --force
```

#### 生成的文件内容

```python
"""测试文件: user_login

使用框架的核心features进行API测试。
"""

import pytest
import allure
from df_test_framework.testing.plugins import attach_json, step


@allure.feature("UserLogin")
@allure.story("UserLogin功能")
class TestUserLogin:
    """UserLogin测试类"""

    @allure.title("测试user login")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_user_login(self, http_client, db_transaction):
        """测试user login

        使用db_transaction确保数据自动回滚清理。
        """
        with step("准备测试数据"):
            # TODO: 准备测试数据
            pass

        with step("调用API"):
            # TODO: 调用API
            # response = http_client.get("/api/path")
            # assert response.status_code == 200
            pass

        with step("验证响应"):
            # TODO: 验证响应数据
            # data = response.json()
            # attach_json(data, name="响应数据")
            # assert data["code"] == 200
            pass

        with step("验证数据库"):
            # TODO: 验证数据库状态
            # 使用db_transaction，测试结束后自动回滚
            pass


__all__ = ["TestUserLogin"]
```

---

### 生成Builder类

#### 命令格式

```bash
df-test gen builder <实体名称> [选项]
```

#### 参数说明

| 参数 | 类型 | 必需 | 说明 | 默认值 |
|------|------|------|------|--------|
| `<实体名称>` | string | ✅ | 实体名称（如：user） | - |
| `--output-dir` | string | ❌ | 输出目录 | `src/<project>/builders/` |
| `--force` | flag | ❌ | 强制覆盖 | `false` |

#### 使用示例

```bash
# 生成用户Builder
df-test gen builder user

# 生成订单Builder
df-test gen builder order

# 指定输出目录
df-test gen builder product --output-dir src/my_project/custom/
```

#### 生成的文件内容

```python
"""Builder: user

使用Builder模式构建user测试数据。
"""

from df_test_framework.patterns import DictBuilder
from typing import Any, Dict


class UserBuilder(DictBuilder):
    """User数据构建器

    使用链式调用构建user数据。

    Example:
        >>> builder = UserBuilder()
        >>> data = (
        ...     builder
        ...     .with_name("示例名称")
        ...     .with_status("active")
        ...     .build()
        ... )
    """

    def __init__(self):
        """初始化Builder，设置默认值"""
        super().__init__()
        self._data = {
            "name": "user_default",
            "status": "active",
            "created_at": None,
            "updated_at": None,
        }

    def with_name(self, name: str) -> "UserBuilder":
        """设置名称

        Args:
            name: 名称

        Returns:
            self: 支持链式调用
        """
        self._data["name"] = name
        return self

    def with_status(self, status: str) -> "UserBuilder":
        """设置状态

        Args:
            status: 状态（如: active, inactive）

        Returns:
            self: 支持链式调用
        """
        self._data["status"] = status
        return self

    # TODO: 添加更多字段的设置方法
    # def with_xxx(self, xxx: Any) -> "UserBuilder":
    #     """设置xxx"""
    #     self._data["xxx"] = xxx
    #     return self


__all__ = ["UserBuilder"]
```

---

### 生成Repository类

#### 命令格式

```bash
df-test gen repo <实体名称> [选项]
```

#### 参数说明

| 参数 | 类型 | 必需 | 说明 | 默认值 |
|------|------|------|------|--------|
| `<实体名称>` | string | ✅ | 实体名称（如：user） | - |
| `--table-name` | string | ❌ | 数据库表名 | `<实体名称>s` |
| `--output-dir` | string | ❌ | 输出目录 | `src/<project>/repositories/` |
| `--force` | flag | ❌ | 强制覆盖 | `false` |

#### 使用示例

```bash
# 基本用法（表名默认为users）
df-test gen repo user

# 指定表名
df-test gen repo user --table-name sys_user

# 生成订单Repository（表名为orders）
df-test gen repo order --table-name orders
```

#### 生成的文件内容

```python
"""Repository: user

使用Repository模式封装user的数据库操作。
"""

from df_test_framework.patterns import BaseRepository, QuerySpec
from typing import List, Optional, Dict, Any


class UserRepository(BaseRepository):
    """User数据仓库

    封装user的数据库CRUD操作。

    Example:
        >>> repo = UserRepository(database)
        >>> # 查询
        >>> item = repo.find_by_id(1)
        >>> items = repo.find_all()
        >>> # 创建
        >>> new_id = repo.create({"name": "test"})
        >>> # 更新
        >>> repo.update(1, {"status": "inactive"})
        >>> # 删除
        >>> repo.delete(1)
    """

    def __init__(self, database):
        """初始化Repository

        Args:
            database: Database对象
        """
        super().__init__(database, table_name="users")

    def find_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """根据名称查询

        Args:
            name: 名称

        Returns:
            Dict或None: 查询结果
        """
        query = QuerySpec().where("name = %s", name).limit(1)
        results = self.query(query)
        return results[0] if results else None

    def find_by_status(self, status: str) -> List[Dict[str, Any]]:
        """根据状态查询

        Args:
            status: 状态

        Returns:
            List[Dict]: 查询结果列表
        """
        query = QuerySpec().where("status = %s", status)
        return self.query(query)

    def count_by_status(self, status: str) -> int:
        """统计指定状态的数量

        Args:
            status: 状态

        Returns:
            int: 数量
        """
        query = QuerySpec().where("status = %s", status)
        return self.count(query)

    # TODO: 添加更多业务查询方法


__all__ = ["UserRepository"]
```

---

### 生成API客户端类

#### 命令格式

```bash
df-test gen api <API名称> [选项]
```

#### 参数说明

| 参数 | 类型 | 必需 | 说明 | 默认值 |
|------|------|------|------|--------|
| `<API名称>` | string | ✅ | API名称（如：user） | - |
| `--api-path` | string | ❌ | API路径前缀 | `<API名称>s` |
| `--output-dir` | string | ❌ | 输出目录 | `src/<project>/apis/` |
| `--force` | flag | ❌ | 强制覆盖 | `false` |

#### 使用示例

```bash
# 基本用法（API路径为/api/users）
df-test gen api user

# 指定API路径
df-test gen api user --api-path admin/users

# 生成支付API
df-test gen api payment --api-path payments
```

#### 生成的文件内容

```python
"""API客户端: user

封装user相关的API调用。
"""

from df_test_framework import BaseAPI, HttpClient
from df_test_framework.core.http import BusinessError
from typing import Dict, Any, List


class UserAPI(BaseAPI):
    """User API客户端

    封装user相关的HTTP API调用。

    Example:
        >>> api = UserAPI(http_client)
        >>> # GET请求
        >>> result = api.get_user(item_id)
        >>> # POST请求
        >>> result = api.create_user(data)
        >>> # PUT请求
        >>> result = api.update_user(item_id, data)
        >>> # DELETE请求
        >>> api.delete_user(item_id)
    """

    def __init__(self, http_client: HttpClient):
        """初始化API客户端

        Args:
            http_client: HTTP客户端
        """
        super().__init__(http_client)
        self.base_path = "/api/users"

    def get_user(self, user_id: int) -> Dict[str, Any]:
        """获取单个user

        Args:
            user_id: user ID

        Returns:
            Dict: user数据

        Raises:
            BusinessError: 业务错误
        """
        response = self.http_client.get(f"{self.base_path}/{user_id}")
        data = response.json()
        self._check_business_error(data)
        return data

    def list_users(self, page: int = 1, size: int = 10) -> List[Dict[str, Any]]:
        """获取user列表

        Args:
            page: 页码
            size: 每页数量

        Returns:
            List[Dict]: user列表
        """
        response = self.http_client.get(
            self.base_path,
            params={"page": page, "size": size}
        )
        data = response.json()
        self._check_business_error(data)
        return data.get("data", [])

    def create_user(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建user

        Args:
            request_data: 请求数据

        Returns:
            Dict: 创建结果
        """
        response = self.http_client.post(self.base_path, json=request_data)
        data = response.json()
        self._check_business_error(data)
        return data

    def update_user(self, user_id: int, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新user

        Args:
            user_id: user ID
            request_data: 请求数据

        Returns:
            Dict: 更新结果
        """
        response = self.http_client.put(
            f"{self.base_path}/{user_id}",
            json=request_data
        )
        data = response.json()
        self._check_business_error(data)
        return data

    def delete_user(self, user_id: int) -> None:
        """删除user

        Args:
            user_id: user ID
        """
        response = self.http_client.delete(f"{self.base_path}/{user_id}")
        data = response.json()
        self._check_business_error(data)

    def _check_business_error(self, response_data: dict) -> None:
        """检查业务错误

        Args:
            response_data: 响应数据

        Raises:
            BusinessError: 业务错误
        """
        code = response_data.get("code")
        if code != 200:
            message = response_data.get("message", "未知错误")
            raise BusinessError(f"[{code}] {message}")


__all__ = ["UserAPI"]
```

---

## 实战示例

### 场景1: 快速开发用户管理测试

```bash
# 1. 生成用户相关代码
df-test gen builder user
df-test gen repo user --table-name sys_user
df-test gen api user --api-path users
df-test gen test user_create --feature "用户管理" --story "创建用户"

# 2. 编辑测试文件
vim tests/api/test_user_create.py
```

**完善后的测试代码**：

```python
"""测试文件: user_create"""

import pytest
import allure
from df_test_framework.testing.plugins import attach_json, step
from my_project.builders import UserBuilder
from my_project.apis import UserAPI
from my_project.repositories import UserRepository


@allure.feature("用户管理")
@allure.story("创建用户")
class TestUserCreate:
    """UserCreate测试类"""

    @allure.title("测试创建用户")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_user_create(self, http_client, db_transaction):
        """测试创建用户"""
        # 准备测试数据
        with step("准备测试数据"):
            user_data = (
                UserBuilder()
                .with_name("测试用户")
                .with_status("active")
                .build()
            )
            attach_json(user_data, name="请求数据")

        # 调用API
        with step("调用创建用户API"):
            api = UserAPI(http_client)
            result = api.create_user(user_data)
            attach_json(result, name="响应数据")
            assert result["code"] == 200

        # 验证数据库
        with step("验证数据库"):
            user_id = result["data"]["user_id"]
            repo = UserRepository(db_transaction)
            user = repo.find_by_id(user_id)
            assert user is not None
            assert user["name"] == "测试用户"
            # ✅ 测试结束后自动回滚，无需手动清理
```

### 场景2: 批量生成订单相关代码

```bash
# 批量生成订单模块代码
df-test gen builder order
df-test gen repo order --table-name orders
df-test gen api order --api-path orders
df-test gen test order_create --feature "订单管理" --story "创建订单"
df-test gen test order_cancel --feature "订单管理" --story "取消订单"
```

### 场景3: 自定义输出目录

```bash
# 为不同环境生成不同的API客户端
df-test gen api user --api-path admin/users --output-dir src/my_project/apis/admin/
df-test gen api user --api-path h5/users --output-dir src/my_project/apis/h5/
```

---

## 最佳实践

### 1. 命名规范

#### 测试文件命名

```bash
# ✅ 好的命名（使用下划线分隔）
df-test gen test user_login
df-test gen test order_create
df-test gen test payment_verify

# ❌ 不好的命名
df-test gen test UserLogin    # 避免驼峰命名
df-test gen test test_user    # 避免test前缀（会自动添加）
```

#### 实体命名

```bash
# ✅ 好的命名（单数形式）
df-test gen builder user
df-test gen repo order

# ❌ 不好的命名
df-test gen builder users   # 避免复数
df-test gen repo Orders     # 避免首字母大写
```

### 2. 目录组织

#### 推荐的项目结构

```
my_project/
├── src/my_project/
│   ├── apis/              # API客户端
│   │   ├── user_api.py
│   │   └── order_api.py
│   ├── builders/          # 数据构造器
│   │   ├── user_builder.py
│   │   └── order_builder.py
│   └── repositories/      # 数据仓库
│       ├── user_repository.py
│       └── order_repository.py
└── tests/
    └── api/              # API测试
        ├── user/
        │   ├── test_user_create.py
        │   └── test_user_login.py
        └── order/
            └── test_order_create.py
```

#### 按模块组织测试

```bash
# 创建模块目录
mkdir -p tests/api/user tests/api/order

# 生成测试到指定模块
df-test gen test user_login --output-dir tests/api/user/
df-test gen test user_register --output-dir tests/api/user/
df-test gen test order_create --output-dir tests/api/order/
```

### 3. 代码复用

#### 生成后立即完善

生成代码后，立即根据实际需求完善：

```python
# 生成的Builder（基础版本）
class UserBuilder(DictBuilder):
    def with_name(self, name: str) -> "UserBuilder":
        self._data["name"] = name
        return self

# 完善后的Builder（添加业务字段）
class UserBuilder(DictBuilder):
    def with_name(self, name: str) -> "UserBuilder":
        self._data["name"] = name
        return self

    def with_email(self, email: str) -> "UserBuilder":
        """设置邮箱"""
        self._data["email"] = email
        return self

    def with_phone(self, phone: str) -> "UserBuilder":
        """设置手机号"""
        self._data["phone"] = phone
        return self

    def with_age(self, age: int) -> "UserBuilder":
        """设置年龄"""
        self._data["age"] = age
        return self
```

#### 创建基类复用

对于相似的实体，可以创建基类：

```python
# src/my_project/builders/base_entity_builder.py
class BaseEntityBuilder(DictBuilder):
    """实体Builder基类"""

    def with_status(self, status: str):
        """设置状态"""
        self._data["status"] = status
        return self

    def with_remark(self, remark: str):
        """设置备注"""
        self._data["remark"] = remark
        return self

# 其他Builder继承基类
class UserBuilder(BaseEntityBuilder):
    def with_name(self, name: str):
        self._data["name"] = name
        return self
```

### 4. 版本控制

#### 提交生成的代码

```bash
# 生成代码后提交
df-test gen builder user
git add src/my_project/builders/user_builder.py
git commit -m "feat: 添加UserBuilder数据构造器"
```

#### 使用`.gitignore`排除临时文件

```gitignore
# .gitignore
*.pyc
__pycache__/
*.log
```

---

## 常见问题

### Q1: 生成代码时提示"无法检测项目名称"？

**原因**: 不在项目根目录下运行，或项目结构不标准。

**解决方案**:

```bash
# 确保在项目根目录下运行
cd /path/to/my-project

# 确保存在src/<project_name>/目录
ls src/
# 应该显示项目目录，如: my_project/

# 如果没有，需要先初始化项目
df-test init my-project
```

### Q2: 如何自定义生成的模板？

**方案1**: 生成后手动修改

```bash
# 先生成标准模板
df-test gen builder user

# 然后根据需求修改
vim src/my_project/builders/user_builder.py
```

**方案2**: 创建自己的代码片段

使用编辑器的代码片段功能（如VSCode的snippets）。

### Q3: 生成的文件已存在如何处理？

**方案1**: 使用`--force`强制覆盖

```bash
df-test gen test user_login --force
```

**方案2**: 备份后生成

```bash
# 备份现有文件
cp tests/api/test_user_login.py tests/api/test_user_login.py.bak

# 重新生成
df-test gen test user_login --force
```

### Q4: 如何生成到自定义目录？

使用`--output-dir`参数：

```bash
# 生成测试到自定义目录
df-test gen test payment --output-dir tests/api/payment/

# 生成Builder到自定义目录
df-test gen builder user --output-dir src/my_project/custom/builders/
```

### Q5: 生成的Repository表名不对如何修改？

**生成时指定**:

```bash
df-test gen repo user --table-name sys_user
```

**生成后修改**:

```python
# 修改 __init__ 方法中的 table_name
def __init__(self, database):
    super().__init__(database, table_name="sys_user")  # 修改这里
```

### Q6: 如何批量生成多个文件？

**方案1**: 使用Shell脚本

```bash
#!/bin/bash
# gen_all.sh

entities=("user" "order" "product" "payment")

for entity in "${entities[@]}"; do
    df-test gen builder "$entity"
    df-test gen repo "$entity"
    df-test gen api "$entity"
done
```

**方案2**: 逐个生成

```bash
df-test gen builder user && \
df-test gen repo user && \
df-test gen api user && \
df-test gen test user_create
```

### Q7: 生成的代码如何符合团队规范？

**方案1**: 生成后使用代码格式化工具

```bash
# 使用black格式化
black src/my_project/builders/user_builder.py

# 使用ruff检查
ruff check src/my_project/builders/user_builder.py
```

**方案2**: 配置pre-commit钩子

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.0.0
    hooks:
      - id: black
```

### Q8: 如何查看生成的文件？

**方案1**: 使用编辑器打开

```bash
df-test gen test user_login && code tests/api/test_user_login.py
```

**方案2**: 使用cat查看

```bash
df-test gen builder user && cat src/my_project/builders/user_builder.py
```

---

## 相关资源

- **📖 API文档**: [Testing API参考](../api-reference/testing.md)
- **📚 模式文档**: [Builder & Repository模式](../api-reference/patterns.md)
- **🏗️ 架构文档**: [v2.0架构设计](../architecture/v2-architecture.md)
- **💡 示例代码**: [examples目录](../../examples/)

---

## 反馈与贡献

如果您有任何建议或发现问题，欢迎：

- 📝 提交Issue: [GitHub Issues](https://github.com/your-org/df-test-framework/issues)
- 💬 参与讨论: [GitHub Discussions](https://github.com/your-org/df-test-framework/discussions)

---

**文档版本**: v2.0.0
**最后更新**: 2025-11-02
**维护者**: DF Test Framework Team
