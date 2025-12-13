# AsyncHttpClient 使用指南

## 概述

`AsyncHttpClient` 是 DF 测试框架提供的异步 HTTP 客户端，基于 `httpx.AsyncClient` 实现，支持完整的 async/await 语法，在并发测试场景下性能提升 10-50 倍。

## 快速开始

### 基础使用

```python
import asyncio
from df_test_framework import AsyncHttpClient

async def test_basic():
    # 使用 async with 自动管理资源
    async with AsyncHttpClient("https://api.example.com") as client:
        # 发起 GET 请求
        response = await client.get("/users/1")

        assert response.status_code == 200
        assert response.json_data["id"] == 1

# 运行异步测试
asyncio.run(test_basic())
```

### pytest 异步测试

```python
import pytest
from df_test_framework import AsyncHttpClient

@pytest.mark.asyncio
async def test_with_pytest():
    """使用 pytest-asyncio 插件"""
    async with AsyncHttpClient("https://api.example.com") as client:
        response = await client.get("/users")
        assert response.status_code == 200
```

## 核心功能

### 1. HTTP 方法

```python
async with AsyncHttpClient("https://api.example.com") as client:
    # GET 请求
    response = await client.get("/users")
    response = await client.get("/users", params={"page": 1, "size": 10})

    # POST 请求
    response = await client.post("/users", json={"name": "Alice", "age": 30})

    # PUT 请求
    response = await client.put("/users/1", json={"name": "Bob"})

    # DELETE 请求
    response = await client.delete("/users/1")

    # PATCH 请求
    response = await client.patch("/users/1", json={"age": 31})
```

### 2. 并发请求

**这是异步客户端的核心优势！**

```python
import asyncio
from df_test_framework import AsyncHttpClient

async def test_concurrent():
    async with AsyncHttpClient("https://api.example.com") as client:
        # 创建 100 个请求任务
        tasks = [
            client.get(f"/users/{i}")
            for i in range(1, 101)
        ]

        # 并发执行所有请求
        responses = await asyncio.gather(*tasks)

        # 验证所有响应
        assert len(responses) == 100
        for response in responses:
            assert response.status_code == 200

# 性能对比:
# - 同步 HttpClient: 100 * 200ms = 20 秒
# - 异步 AsyncHttpClient: ~500ms (40倍提升!)
```

### 3. 配置选项

```python
from df_test_framework import AsyncHttpClient

async with AsyncHttpClient(
    base_url="https://api.example.com",
    timeout=60,                    # 超时时间（秒）
    headers={"X-API-Key": "xxx"},  # 默认请求头
    verify_ssl=True,               # SSL 证书验证
    max_connections=200,           # 最大并发连接数
    max_keepalive_connections=40,  # Keep-Alive 连接数
    http2=True,                    # 启用 HTTP/2（推荐）
) as client:
    response = await client.get("/users")
```

#### 配置优先级 (v3.9.0+)

当同时提供构造函数参数和 `HTTPConfig` 时，遵循以下优先级：

**显式参数 > HTTPConfig > 默认值**

```python
from df_test_framework import AsyncHttpClient
from df_test_framework.infrastructure import HTTPConfig

# HTTPConfig 提供默认配置
config = HTTPConfig(
    base_url="https://default.example.com",
    timeout=30,
    verify_ssl=True,
    max_connections=100,
)

# 显式参数会覆盖 HTTPConfig 中的配置
async with AsyncHttpClient(
    base_url="https://override.example.com",  # 覆盖 config.base_url
    timeout=60,                                # 覆盖 config.timeout
    # verify_ssl 未指定，使用 config.verify_ssl = True
    # max_connections 未指定，使用 config.max_connections = 100
    config=config,
) as client:
    # 实际配置:
    # - base_url: "https://override.example.com" (显式参数)
    # - timeout: 60 (显式参数)
    # - verify_ssl: True (来自 HTTPConfig)
    # - max_connections: 100 (来自 HTTPConfig)
    response = await client.get("/users")
```

这种设计使得：
- **HTTPConfig** 可以作为项目级别的默认配置
- **显式参数** 可以在特定场景下覆盖默认配置
- 测试代码更灵活，减少重复配置

### 4. 认证 Token

```python
async with AsyncHttpClient("https://api.example.com") as client:
    # 设置 Bearer Token
    client.set_auth_token("your_token_here", token_type="Bearer")

    # 后续所有请求自动携带 Authorization header
    response = await client.get("/protected/resource")
    # Authorization: Bearer your_token_here
```

### 5. 拦截器集成

所有同步拦截器都可以在异步客户端中使用！

```python
from df_test_framework import AsyncHttpClient
from df_test_framework.clients.http.interceptors import (
    SignatureInterceptor,
    BearerTokenInterceptor,
    LoggingInterceptor,
)

async with AsyncHttpClient("https://api.example.com") as client:
    # 添加签名拦截器
    client.interceptor_chain.add(
        SignatureInterceptor(
            algorithm="md5",
            secret="my_secret",
            header_name="X-Sign",
            priority=10,
        )
    )

    # 添加 Token 拦截器
    client.interceptor_chain.add(
        BearerTokenInterceptor(
            token_source="static",
            static_token="my_token",
            priority=20,
        )
    )

    # 添加日志拦截器
    client.interceptor_chain.add(
        LoggingInterceptor(priority=100)
    )

    # 所有请求都会经过这些拦截器
    response = await client.post("/api/users", json={"name": "Alice"})
```

### 6. Pydantic 模型支持

```python
from pydantic import BaseModel
from df_test_framework import AsyncHttpClient

class User(BaseModel):
    name: str
    age: int
    email: str

async with AsyncHttpClient("https://api.example.com") as client:
    # Pydantic 模型自动序列化
    user = User(name="Alice", age=30, email="alice@example.com")
    response = await client.post("/users", json=user)

    # 等价于:
    # response = await client.post("/users", json={
    #     "name": "Alice",
    #     "age": 30,
    #     "email": "alice@example.com"
    # })
```

## 常见场景

### 场景 1: 批量创建数据

```python
import asyncio
from df_test_framework import AsyncHttpClient

async def batch_create_users():
    """批量创建 1000 个用户"""
    async with AsyncHttpClient("https://api.example.com") as client:
        # 准备 1000 个创建任务
        tasks = [
            client.post("/users", json={"name": f"User_{i}", "age": 20 + i % 50})
            for i in range(1000)
        ]

        # 并发执行（分批控制并发数）
        batch_size = 50
        for i in range(0, len(tasks), batch_size):
            batch = tasks[i:i + batch_size]
            responses = await asyncio.gather(*batch)
            print(f"批次 {i//batch_size + 1}: 创建 {len(responses)} 个用户")

asyncio.run(batch_create_users())
```

### 场景 2: 压力测试

```python
import asyncio
import time
from df_test_framework import AsyncHttpClient

async def stress_test(qps: int, duration_seconds: int):
    """压力测试

    Args:
        qps: 每秒请求数
        duration_seconds: 持续时间（秒）
    """
    async with AsyncHttpClient("https://api.example.com") as client:
        start_time = time.time()
        total_requests = 0
        total_errors = 0

        while time.time() - start_time < duration_seconds:
            # 每秒发送 qps 个请求
            tasks = [client.get("/health") for _ in range(qps)]

            try:
                responses = await asyncio.gather(*tasks, return_exceptions=True)

                # 统计结果
                for response in responses:
                    total_requests += 1
                    if isinstance(response, Exception) or response.status_code != 200:
                        total_errors += 1

            except Exception as e:
                print(f"批次失败: {e}")

            # 等待 1 秒（维持 QPS）
            await asyncio.sleep(1)

        # 输出结果
        print(f"总请求: {total_requests}")
        print(f"失败数: {total_errors}")
        print(f"成功率: {(total_requests - total_errors) / total_requests * 100:.2f}%")

# 执行: 100 QPS，持续 60 秒
asyncio.run(stress_test(qps=100, duration_seconds=60))
```

### 场景 3: 依赖接口调用

```python
import asyncio
from df_test_framework import AsyncHttpClient

async def create_user_with_posts():
    """创建用户并发布 10 篇文章"""
    async with AsyncHttpClient("https://api.example.com") as client:
        # 1. 创建用户
        user_response = await client.post("/users", json={"name": "Alice"})
        user_id = user_response.json_data["id"]

        # 2. 并发发布 10 篇文章
        post_tasks = [
            client.post("/posts", json={
                "user_id": user_id,
                "title": f"Post {i}",
                "content": f"Content {i}"
            })
            for i in range(10)
        ]

        post_responses = await asyncio.gather(*post_tasks)

        print(f"用户 {user_id} 发布了 {len(post_responses)} 篇文章")

asyncio.run(create_user_with_posts())
```

### 场景 4: 错误处理

```python
import asyncio
import httpx
from df_test_framework import AsyncHttpClient

async def handle_errors():
    """处理各种错误情况"""
    async with AsyncHttpClient("https://api.example.com", timeout=5) as client:
        try:
            response = await client.get("/users/999")

            # 检查 HTTP 状态码
            if response.status_code == 404:
                print("用户不存在")
            elif response.status_code == 500:
                print("服务器错误")

        except httpx.TimeoutException:
            print("请求超时")

        except httpx.NetworkError as e:
            print(f"网络错误: {e}")

        except httpx.HTTPError as e:
            print(f"HTTP 错误: {e}")

        except Exception as e:
            print(f"未知错误: {e}")

asyncio.run(handle_errors())
```

### 场景 5: 配置化拦截器

```python
from df_test_framework import AsyncHttpClient
from df_test_framework.infrastructure import HTTPConfig, SignatureConfig

# 使用 HTTPConfig 配置
config = HTTPConfig(
    timeout=60,
    verify_ssl=True,
    interceptors=[
        # 签名拦截器配置
        SignatureConfig(
            algorithm="md5",
            secret="my_secret",
            header_name="X-Sign",
            paths=["/api/**"],  # 只对 /api/** 路径生效
            priority=10,
        )
    ]
)

async with AsyncHttpClient("https://api.example.com", config=config) as client:
    # /api/** 路径会自动签名
    response = await client.post("/api/users", json={"name": "Alice"})

    # /other/** 路径不会签名
    response = await client.get("/other/health")
```

## 性能优化建议

### 1. 控制并发数

```python
import asyncio
from df_test_framework import AsyncHttpClient

async def controlled_concurrency():
    """使用 Semaphore 控制并发数"""
    async with AsyncHttpClient("https://api.example.com") as client:
        # 最多同时 10 个并发请求
        semaphore = asyncio.Semaphore(10)

        async def fetch_with_semaphore(user_id):
            async with semaphore:
                return await client.get(f"/users/{user_id}")

        # 创建 100 个任务，但最多同时 10 个
        tasks = [fetch_with_semaphore(i) for i in range(100)]
        responses = await asyncio.gather(*tasks)

        print(f"完成 {len(responses)} 个请求")

asyncio.run(controlled_concurrency())
```

### 2. 连接池配置

```python
# 高并发场景：增大连接池
async with AsyncHttpClient(
    "https://api.example.com",
    max_connections=500,           # 最大连接数
    max_keepalive_connections=100, # Keep-Alive 连接数
) as client:
    # 可以支持更高的并发
    tasks = [client.get(f"/users/{i}") for i in range(500)]
    responses = await asyncio.gather(*tasks)
```

### 3. HTTP/2 优势

```python
# 启用 HTTP/2（默认已启用）
async with AsyncHttpClient(
    "https://api.example.com",
    http2=True,  # 启用 HTTP/2
) as client:
    # HTTP/2 优势:
    # 1. 多路复用（一个连接多个请求）
    # 2. 头部压缩（减少传输量）
    # 3. 服务器推送
    # 4. 二进制协议（更高效）

    tasks = [client.get(f"/users/{i}") for i in range(100)]
    responses = await asyncio.gather(*tasks)
```

### 4. 复用客户端实例

```python
# ❌ 错误：每次请求创建新客户端
async def bad_example():
    for i in range(100):
        async with AsyncHttpClient("https://api.example.com") as client:
            await client.get(f"/users/{i}")

# ✅ 正确：复用客户端实例
async def good_example():
    async with AsyncHttpClient("https://api.example.com") as client:
        tasks = [client.get(f"/users/{i}") for i in range(100)]
        await asyncio.gather(*tasks)
```

## 与同步 HttpClient 对比

| 特性 | HttpClient | AsyncHttpClient |
|------|-----------|-----------------|
| 语法 | 同步 | async/await |
| 单个请求性能 | 200ms | 200ms（相同） |
| 100 个串行请求 | 20 秒 | 20 秒（相同） |
| 100 个并发请求 | 20 秒 | 0.5 秒（**40x**） |
| 拦截器支持 | ✅ | ✅（完全兼容） |
| Pydantic 支持 | ✅ | ✅ |
| HTTP/2 支持 | ❌ | ✅ |
| 连接池 | ❌ | ✅ |
| 适用场景 | 简单测试 | 并发测试、压力测试 |

## 注意事项

### 1. 必须使用 async/await

```python
# ❌ 错误：忘记 await
async def wrong():
    async with AsyncHttpClient("https://api.example.com") as client:
        response = client.get("/users")  # 返回 coroutine，不是 Response
        print(response.status_code)      # AttributeError

# ✅ 正确
async def correct():
    async with AsyncHttpClient("https://api.example.com") as client:
        response = await client.get("/users")  # await 等待结果
        print(response.status_code)            # OK
```

### 2. 资源管理

```python
# ✅ 推荐：使用 async with（自动关闭）
async def recommended():
    async with AsyncHttpClient("https://api.example.com") as client:
        await client.get("/users")
    # 自动调用 client.close()

# ⚠️ 手动管理（需要显式关闭）
async def manual():
    client = AsyncHttpClient("https://api.example.com")
    try:
        await client.get("/users")
    finally:
        await client.close()  # 必须手动关闭
```

### 3. pytest 配置

需要安装 `pytest-asyncio`：

```bash
uv pip install pytest-asyncio
```

配置 `pyproject.toml`：

```toml
[tool.pytest.ini_options]
markers = [
    "asyncio: 异步测试",
]
```

## 更多资源

- [架构设计文档](../async_http_client_design.md) - 详细设计决策和性能分析
- [拦截器使用指南](./interceptors.md) - 拦截器详细说明
- [API 参考](../api/async_http_client.md) - 完整 API 文档
