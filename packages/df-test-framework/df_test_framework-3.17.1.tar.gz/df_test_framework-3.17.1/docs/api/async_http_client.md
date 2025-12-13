# AsyncHttpClient API 参考

## 类定义

```python
class AsyncHttpClient:
    """异步 HTTP 客户端

    基于 httpx.AsyncClient 的封装，提供完整的 async/await 支持。
    """
```

## 构造函数

### `__init__()`

```python
def __init__(
    self,
    base_url: str,
    timeout: int = 30,
    headers: dict[str, str] | None = None,
    verify_ssl: bool = True,
    max_connections: int = 100,
    max_keepalive_connections: int = 20,
    http2: bool = True,
    config: HTTPConfig | None = None,
)
```

初始化异步 HTTP 客户端。

**参数：**

- `base_url` (str): API 基础 URL
- `timeout` (int): 请求超时时间（秒），默认 30
- `headers` (dict[str, str] | None): 默认请求头，默认 None
- `verify_ssl` (bool): 是否验证 SSL 证书，默认 True
- `max_connections` (int): 最大并发连接数，默认 100
- `max_keepalive_connections` (int): Keep-Alive 连接数，默认 20
- `http2` (bool): 是否启用 HTTP/2，默认 True
- `config` (HTTPConfig | None): HTTPConfig 配置对象，默认 None

**示例：**

```python
# 基础初始化
client = AsyncHttpClient("https://api.example.com")

# 自定义配置
client = AsyncHttpClient(
    base_url="https://api.example.com",
    timeout=60,
    headers={"X-API-Key": "xxx"},
    max_connections=200,
    http2=True
)

# 使用 HTTPConfig
config = HTTPConfig(timeout=60, interceptors=[...])
client = AsyncHttpClient("https://api.example.com", config=config)
```

## HTTP 方法

### `get()`

```python
async def get(self, url: str, **kwargs) -> Response
```

发起异步 GET 请求。

**参数：**

- `url` (str): 请求路径（相对于 base_url）
- `**kwargs`: httpx 支持的参数（params, headers 等）

**返回：**

- `Response`: 响应对象

**示例：**

```python
response = await client.get("/users")
response = await client.get("/users/1")
response = await client.get("/search", params={"q": "python"})
response = await client.get("/data", headers={"X-Token": "abc"})
```

### `post()`

```python
async def post(self, url: str, **kwargs) -> Response
```

发起异步 POST 请求。

**参数：**

- `url` (str): 请求路径
- `**kwargs`: httpx 支持的参数（json, data, headers 等）

**返回：**

- `Response`: 响应对象

**示例：**

```python
response = await client.post("/users", json={"name": "Alice"})
response = await client.post("/login", data={"user": "admin"})
response = await client.post("/upload", files={"file": open("test.txt", "rb")})
```

### `put()`

```python
async def put(self, url: str, **kwargs) -> Response
```

发起异步 PUT 请求。

**参数：**

- `url` (str): 请求路径
- `**kwargs`: httpx 支持的参数

**返回：**

- `Response`: 响应对象

**示例：**

```python
response = await client.put("/users/1", json={"name": "Bob"})
```

### `delete()`

```python
async def delete(self, url: str, **kwargs) -> Response
```

发起异步 DELETE 请求。

**参数：**

- `url` (str): 请求路径
- `**kwargs`: httpx 支持的参数

**返回：**

- `Response`: 响应对象

**示例：**

```python
response = await client.delete("/users/1")
```

### `patch()`

```python
async def patch(self, url: str, **kwargs) -> Response
```

发起异步 PATCH 请求。

**参数：**

- `url` (str): 请求路径
- `**kwargs`: httpx 支持的参数

**返回：**

- `Response`: 响应对象

**示例：**

```python
response = await client.patch("/users/1", json={"age": 30})
```

### `request()`

```python
async def request(self, method: str, url: str, **kwargs) -> Response
```

通用异步请求方法。

**参数：**

- `method` (str): HTTP 方法（GET/POST/PUT/DELETE/PATCH）
- `url` (str): 请求路径
- `**kwargs`: httpx 支持的参数

**返回：**

- `Response`: 响应对象

**异常：**

- `httpx.HTTPError`: HTTP 请求错误
- `httpx.TimeoutException`: 请求超时
- `httpx.NetworkError`: 网络错误

**执行流程：**

1. 准备 Request 对象
2. 执行拦截器链（before）
3. 发送异步 HTTP 请求
4. 解析响应
5. 执行拦截器链（after）
6. 返回 Response 对象

**示例：**

```python
response = await client.request("GET", "/users")
response = await client.request("POST", "/users", json={"name": "Alice"})
```

## 认证方法

### `set_auth_token()`

```python
def set_auth_token(self, token: str, token_type: str = "Bearer") -> None
```

设置认证 token。

**参数：**

- `token` (str): 认证令牌
- `token_type` (str): 令牌类型（Bearer, Basic 等），默认 "Bearer"

**示例：**

```python
client.set_auth_token("abc123", "Bearer")
# 后续请求会自动添加: Authorization: Bearer abc123
```

## 上下文管理器

### `__aenter__()`

```python
async def __aenter__(self) -> AsyncHttpClient
```

异步上下文管理器入口。

**返回：**

- `AsyncHttpClient`: 客户端实例

**示例：**

```python
async with AsyncHttpClient("https://api.example.com") as client:
    response = await client.get("/users")
```

### `__aexit__()`

```python
async def __aexit__(self, exc_type, exc_val, exc_tb) -> None
```

异步上下文管理器退出，自动关闭客户端。

**参数：**

- `exc_type`: 异常类型
- `exc_val`: 异常值
- `exc_tb`: 异常追踪

### `close()`

```python
async def close(self) -> None
```

关闭客户端，释放连接池资源。

**注意：**

- 使用 `async with` 时会自动调用，无需手动调用
- 手动管理资源时必须显式调用

**示例：**

```python
# 自动关闭（推荐）
async with AsyncHttpClient("https://api.example.com") as client:
    response = await client.get("/users")
# 自动调用 close()

# 手动关闭
client = AsyncHttpClient("https://api.example.com")
try:
    response = await client.get("/users")
finally:
    await client.close()  # 必须手动调用
```

## 属性

### `base_url`

```python
base_url: str
```

API 基础 URL。

### `timeout`

```python
timeout: int
```

请求超时时间（秒）。

### `http2`

```python
http2: bool
```

是否启用 HTTP/2。

### `interceptor_chain`

```python
interceptor_chain: InterceptorChain
```

拦截器链实例，用于添加拦截器。

**示例：**

```python
from df_test_framework.clients.http.interceptors import SignatureInterceptor

client = AsyncHttpClient("https://api.example.com")
client.interceptor_chain.add(SignatureInterceptor(algorithm="md5", secret="secret"))
```

### `client`

```python
client: httpx.AsyncClient
```

底层 httpx.AsyncClient 实例。

## Response 对象

所有 HTTP 方法返回 `Response` 对象：

```python
@dataclass(frozen=True)
class Response:
    status_code: int                      # HTTP 状态码
    headers: dict[str, str]               # 响应头
    body: str                             # 响应体（文本）
    json_data: dict[str, Any] | None      # JSON 数据（如果是 JSON 响应）
    context: dict[str, Any]               # 上下文数据
```

**属性：**

- `status_code` (int): HTTP 状态码（200, 404, 500 等）
- `headers` (dict): 响应头字典
- `body` (str): 响应体文本
- `json_data` (dict | None): JSON 数据（自动解析）
- `context` (dict): 上下文数据（拦截器可添加）

**方法：**

- `is_success` (bool): 是否成功（2xx）
- `is_client_error` (bool): 是否客户端错误（4xx）
- `is_server_error` (bool): 是否服务器错误（5xx）
- `with_context(key, value)`: 添加上下文数据（返回新对象）
- `get_context(key, default)`: 获取上下文数据

**示例：**

```python
response = await client.get("/users/1")

print(response.status_code)        # 200
print(response.headers)            # {"Content-Type": "application/json", ...}
print(response.body)               # '{"id": 1, "name": "Alice"}'
print(response.json_data)          # {"id": 1, "name": "Alice"}

if response.is_success:
    print("请求成功")

if response.is_client_error:
    print("客户端错误（4xx）")

if response.is_server_error:
    print("服务器错误（5xx）")
```

## 异常

### `httpx.HTTPError`

HTTP 请求相关的所有异常的基类。

### `httpx.TimeoutException`

请求超时异常。

**示例：**

```python
try:
    response = await client.get("/slow-endpoint")
except httpx.TimeoutException:
    print("请求超时")
```

### `httpx.NetworkError`

网络错误异常（连接失败、DNS 解析失败等）。

**示例：**

```python
try:
    response = await client.get("/users")
except httpx.NetworkError as e:
    print(f"网络错误: {e}")
```

### `httpx.HTTPStatusError`

HTTP 状态码错误（4xx, 5xx）。

**注意：** 默认情况下不会抛出此异常，需要手动调用 `response.raise_for_status()`。

## 并发工具

### `asyncio.gather()`

并发执行多个异步任务。

**示例：**

```python
import asyncio

async with AsyncHttpClient("https://api.example.com") as client:
    tasks = [
        client.get("/users/1"),
        client.get("/users/2"),
        client.get("/users/3"),
    ]

    # 并发执行
    responses = await asyncio.gather(*tasks)

    # 处理结果
    for response in responses:
        print(response.json_data)
```

### `asyncio.Semaphore()`

控制并发数。

**示例：**

```python
import asyncio

async with AsyncHttpClient("https://api.example.com") as client:
    semaphore = asyncio.Semaphore(10)  # 最多 10 个并发

    async def fetch_with_limit(user_id):
        async with semaphore:
            return await client.get(f"/users/{user_id}")

    tasks = [fetch_with_limit(i) for i in range(100)]
    responses = await asyncio.gather(*tasks)
```

## 类型提示

```python
from typing import Any
from df_test_framework import AsyncHttpClient
from df_test_framework.clients.http.core import Response

async def example() -> None:
    async with AsyncHttpClient("https://api.example.com") as client:
        # client 类型: AsyncHttpClient
        response: Response = await client.get("/users")

        # response.json_data 类型: dict[str, Any] | None
        data: dict[str, Any] | None = response.json_data

        if data:
            user_id: int = data["id"]
            user_name: str = data["name"]
```

## 性能指标

| 指标 | 值 |
|------|---|
| 单个请求延迟 | ~200ms（与网络相关） |
| 并发连接数 | 100（默认，可配置到 500+） |
| Keep-Alive 连接数 | 20（默认，可配置到 100+） |
| HTTP/2 支持 | ✅ 默认启用 |
| 连接复用 | ✅ 自动 |
| 并发性能提升 | 10-50x（相比同步版本） |

## 最佳实践

### 1. 使用上下文管理器

```python
# ✅ 推荐
async with AsyncHttpClient("https://api.example.com") as client:
    await client.get("/users")

# ❌ 不推荐
client = AsyncHttpClient("https://api.example.com")
await client.get("/users")
await client.close()  # 容易忘记
```

### 2. 复用客户端实例

```python
# ✅ 推荐：复用一个客户端
async with AsyncHttpClient("https://api.example.com") as client:
    for i in range(100):
        await client.get(f"/users/{i}")

# ❌ 不推荐：每次创建新客户端
for i in range(100):
    async with AsyncHttpClient("https://api.example.com") as client:
        await client.get(f"/users/{i}")
```

### 3. 并发而非串行

```python
# ✅ 推荐：并发执行
async with AsyncHttpClient("https://api.example.com") as client:
    tasks = [client.get(f"/users/{i}") for i in range(100)]
    responses = await asyncio.gather(*tasks)

# ❌ 不推荐：串行执行
async with AsyncHttpClient("https://api.example.com") as client:
    responses = []
    for i in range(100):
        response = await client.get(f"/users/{i}")
        responses.append(response)
```

### 4. 控制并发数

```python
# ✅ 推荐：使用 Semaphore 控制并发
semaphore = asyncio.Semaphore(10)

async def fetch(user_id):
    async with semaphore:
        return await client.get(f"/users/{user_id}")

tasks = [fetch(i) for i in range(1000)]
responses = await asyncio.gather(*tasks)

# ❌ 不推荐：无限制并发（可能导致资源耗尽）
tasks = [client.get(f"/users/{i}") for i in range(1000)]
responses = await asyncio.gather(*tasks)
```

## 更多信息

- [使用指南](../guides/async_http_client.md) - 详细使用示例
- [架构设计](../async_http_client_design.md) - 设计决策和性能分析
- [httpx 文档](https://www.python-httpx.org/) - 底层库文档
