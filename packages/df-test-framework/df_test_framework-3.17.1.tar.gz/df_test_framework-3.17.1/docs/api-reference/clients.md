# Clients API 参考

> 📖 **能力层1: Clients** - 请求-响应交互模式
>
> 适用场景: HTTP API、RPC服务、GraphQL等请求-响应式通信

---

## 🎯 模块概述

**clients/** 模块提供请求-响应式交互能力，当前支持:

| 子模块 | 交互协议 | 实现 | 状态 |
|--------|---------|------|------|
| `clients/http/rest/httpx/` | HTTP REST | httpx | ✅ 已实现 |
| `clients/http/graphql/` | GraphQL | - | 🔄 规划中 |
| `clients/rpc/grpc/` | gRPC | - | 🔄 规划中 |

---

## 📦 导入方式

### 推荐导入（顶层）

```python
from df_test_framework import HttpClient, BaseAPI, BusinessError
```

### 完整路径导入

```python
from df_test_framework.clients.http.rest.httpx import (
    HttpClient,
    BaseAPI,
    BusinessError,
)
```

---

## 🌐 HttpClient - HTTP REST客户端

### 功能特性

- ✅ 基于httpx实现，支持HTTP/1.1和HTTP/2
- ✅ 自动重试机制（超时和5xx错误）
- ✅ 请求/响应拦截器
- ✅ 认证管理（Bearer/Basic）
- ✅ 连接池管理
- ✅ URL敏感参数自动脱敏

### 快速开始

```python
from df_test_framework import HttpClient

# 创建客户端
client = HttpClient(
    base_url="https://api.example.com",
    timeout=30,
    max_retries=3
)

# 发送请求
response = client.get("/users/1")
assert response.status_code == 200

user = response.json()
print(f"用户名: {user['name']}")
```

### 核心方法

#### 请求方法
- `get(url, params=None, **kwargs)` - GET请求
- `post(url, json=None, data=None, **kwargs)` - POST请求
- `put(url, json=None, **kwargs)` - PUT请求
- `patch(url, json=None, **kwargs)` - PATCH请求
- `delete(url, **kwargs)` - DELETE请求
- `request(method, url, **kwargs)` - 通用请求方法

#### 认证方法
- `set_auth_token(token, token_type="Bearer")` - 设置认证Token

#### 管理方法
- `close()` - 关闭客户端连接

### 完整文档

详细API文档请参考: [core.md#HttpClient](core.md#httpclient)

---

## 🎨 BaseAPI - REST API基类

### 功能特性

- ✅ 封装HttpClient
- ✅ 请求/响应拦截器（支持链式调用）
- ✅ 统一错误处理
- ✅ 业务异常封装
- ✅ 自动解析为Pydantic模型
- ✅ HTTP状态码检查

> ⭐ **已验证**: BaseAPI的设计模式已通过gift-card-test项目验证。详见 [已验证最佳实践](../user-guide/VERIFIED_BEST_PRACTICES.md#1-baseapi最佳实践)

### 快速开始

**推荐模式**：继承项目基类（已重写业务错误检查）

```python
from df_test_framework import HttpClient, BaseAPI, BusinessError
from typing import Dict, Any


# 步骤1: 创建项目基类
class MyProjectBaseAPI(BaseAPI):
    """项目API基类

    统一业务错误检查逻辑
    """

    def _check_business_error(self, response_data: Dict[str, Any]) -> None:
        """检查业务错误

        业务响应格式:
        {
            "code": 200,
            "message": "成功",
            "data": {...}
        }
        """
        if response_data.get("code") != 200:
            raise BusinessError(
                message=response_data.get("message", "业务错误"),
                code=response_data.get("code")
            )


# 步骤2: 具体API类继承项目基类
class UserAPI(MyProjectBaseAPI):
    """用户API"""

    def __init__(self, http_client: HttpClient):
        super().__init__(http_client)
        self.base_path = "/users"

    def get_user(self, user_id: int) -> UserResponse:
        """获取用户信息

        Args:
            user_id: 用户ID

        Returns:
            UserResponse: 用户信息（自动解析为Pydantic模型）

        Raises:
            BusinessError: 业务错误（code != 200时自动抛出）
        """
        return self.get(
            endpoint=f"{self.base_path}/{user_id}",
            model=UserResponse  # 自动解析为模型
        )

    def create_user(self, request: UserCreateRequest) -> UserResponse:
        """创建用户"""
        data = {
            "name": request.name,
            "email": request.email,
        }
        return self.post(
            endpoint=self.base_path,
            model=UserResponse,
            json=data
        )


# 使用
api = UserAPI(http_client)
user = api.get_user(1)  # 返回UserResponse实例
```

### 核心方法

#### HTTP请求方法
- `get(endpoint, model=None, params=None, **kwargs)` - GET请求
- `post(endpoint, model=None, json=None, **kwargs)` - POST请求
- `put(endpoint, model=None, json=None, **kwargs)` - PUT请求
- `patch(endpoint, model=None, json=None, **kwargs)` - PATCH请求
- `delete(endpoint, model=None, **kwargs)` - DELETE请求

**参数说明**:
- `endpoint`: 接口路径（相对于base_url）
- `model`: Pydantic模型类（可选），指定后自动解析响应
- 其他参数透传给HttpClient

#### 拦截器方法
- `request_interceptors: List[RequestInterceptor]` - 请求拦截器列表
- `response_interceptors: List[ResponseInterceptor]` - 响应拦截器列表
- `_apply_request_interceptors(method, url, **kwargs)` - 应用请求拦截器（内部方法）
- `_apply_response_interceptors(response)` - 应用响应拦截器（内部方法）

**拦截器特性**（已验证）:
- ✅ **深度合并**: 后面的拦截器不会覆盖前面的修改
- ✅ **容错机制**: 单个拦截器失败不影响其他拦截器
- ✅ **链式调用**: 支持多个拦截器顺序执行

#### 业务错误检查
- `_check_business_error(response_data)` - 检查业务错误（需在子类重写）

### 实际验证案例

以下是经过gift-card-test项目验证的完整示例：

```python
# 来自: gift-card-test/src/gift_card_test/apis/admin_template_api.py

class AdminTemplateAPI(GiftCardBaseAPI):
    """Admin管理端卡模板API

    对应后端Controller: CardTemplateController.java

    已验证特性:
    - ✅ 自动业务错误检查
    - ✅ 自动解析为Pydantic模型
    - ✅ HTTP自动重试
    - ✅ 拦截器支持（签名）
    """

    def __init__(self, http_client: HttpClient):
        super().__init__(http_client)
        self.base_path = "/admin/card-templates"

    def query_templates(
        self,
        request: AdminTemplateQueryRequest
    ) -> AdminTemplatesResponse:
        """分页查询卡模板

        对应后端接口: GET /admin/card-templates

        ✅ 已验证:
        - 正确处理camelCase参数映射
        - 自动解析分页响应
        - 业务错误自动抛出BusinessError

        Args:
            request: 查询请求
                - template_id: 模板编号(可选)
                - name: 模板名称(可选)
                - status: 状态(可选)
                - current: 当前页码
                - size: 每页大小

        Returns:
            AdminTemplatesResponse: 分页数据

        Raises:
            BusinessError: 业务错误(code != 200时自动抛出)
        """
        params = {
            "current": request.current,
            "size": request.size,
        }
        # camelCase映射
        if request.template_id:
            params["templateId"] = request.template_id
        if request.name:
            params["name"] = request.name
        if request.status is not None:
            params["status"] = request.status

        return self.get(
            endpoint=self.base_path,
            model=AdminTemplatesResponse,
            params=params
        )
```

### 完整文档

- 详细用法: [已验证最佳实践](../user-guide/VERIFIED_BEST_PRACTICES.md#1-baseapi最佳实践)
- 拦截器机制: [已验证最佳实践](../user-guide/VERIFIED_BEST_PRACTICES.md#2-拦截器机制最佳实践)

---

## 🚨 BusinessError - 业务异常

### 功能特性

- ✅ 封装业务错误信息
- ✅ 携带HTTP响应对象
- ✅ 支持错误码和消息

### 快速开始

```python
from df_test_framework import BusinessError

try:
    response = client.post("/users", json={"name": ""})
    if response.status_code == 400:
        raise BusinessError(
            "参数验证失败",
            code="VALIDATION_ERROR",
            response=response
        )
except BusinessError as e:
    print(f"业务错误: {e.message}")
    print(f"错误码: {e.code}")
    print(f"HTTP状态: {e.response.status_code}")
```

---

## 🔗 相关文档

### 架构设计
- [v3架构设计](../architecture/V3_ARCHITECTURE.md) - 能力层设计理念
- [交互模式分类](../architecture/V3_ARCHITECTURE.md#交互模式) - 为什么按交互模式分类

### 其他能力层
- [Databases API](databases.md) - 数据访问模式
- [Drivers API](drivers.md) - 会话式交互模式

### 测试支持
- [Testing API](testing.md) - Fixtures和测试工具
- [Infrastructure API](infrastructure.md) - Bootstrap和Runtime

### v2兼容
- [Core API](core.md) - v2版HttpClient文档（向后兼容）

---

**返回**: [API参考首页](README.md) | [文档首页](../README.md)
