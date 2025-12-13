# Prometheus 指标监控

DF Test Framework 提供了完整的 Prometheus 指标收集功能，支持自动化测试中的性能监控、系统状态跟踪和可观测性增强。

## 功能特性

- **多种指标类型**: Counter, Gauge, Histogram, Summary
- **自动收集**: HTTP 请求和数据库查询指标自动收集
- **装饰器支持**: 通过装饰器轻松添加指标
- **零配置模式**: 无需安装 prometheus_client 即可使用
- **Grafana 集成**: 支持 Prometheus exporter 和 Pushgateway

## 快速开始

### 基础使用

```python
from df_test_framework.infrastructure.metrics import (
    MetricsManager,
    MetricsConfig,
    get_metrics_manager,
)

# 1. 初始化指标管理器
manager = MetricsManager(service_name="my-test-service")
manager.init()

# 2. 创建指标
requests_total = manager.counter(
    "http_requests_total",
    "Total HTTP requests",
    labels=["method", "status"]
)

response_time = manager.histogram(
    "http_response_seconds",
    "HTTP response time in seconds"
)

active_connections = manager.gauge(
    "db_connections_active",
    "Active database connections"
)

# 3. 使用指标
requests_total.labels(method="GET", status="200").inc()
response_time.observe(0.345)
active_connections.set(5)

# 4. 收集所有指标
metrics_data = manager.collect()
print(metrics_data)
```

### 使用全局管理器

```python
from df_test_framework.infrastructure.metrics import get_metrics_manager

# 获取全局管理器（自动初始化）
manager = get_metrics_manager()

# 创建和使用指标
counter = manager.counter("test_counter", "Test counter")
counter.inc()
```

## 指标类型详解

### Counter (计数器)

只能递增的指标，用于统计事件发生次数。

```python
# 创建计数器
requests = manager.counter(
    "api_requests_total",
    "Total API requests",
    labels=["endpoint", "method", "status"]
)

# 增加计数
requests.labels(endpoint="/users", method="GET", status="200").inc()
requests.labels(endpoint="/orders", method="POST", status="201").inc(5)

# 获取当前值
current_value = requests.labels(endpoint="/users", method="GET", status="200").get()
print(f"Total requests: {current_value}")
```

**最佳实践**:
- 使用 Counter 统计请求数、错误数、处理任务数等
- 标签用于区分不同维度（如 HTTP 方法、状态码）
- 避免使用高基数标签（如用户 ID、请求 ID）

### Gauge (仪表盘)

可增可减的指标，用于表示当前状态。

```python
# 创建仪表盘
connections = manager.gauge(
    "database_connections_active",
    "Active database connections",
    labels=["database"]
)

# 设置值
connections.labels(database="postgres").set(10)

# 增加/减少
connections.labels(database="postgres").inc(5)  # 增加到 15
connections.labels(database="postgres").dec(3)  # 减少到 12

# 追踪进行中的操作
with connections.labels(database="redis").track_inprogress():
    # 在这个上下文中，gauge 会自动 +1
    perform_redis_operation()
    # 退出时自动 -1
```

**最佳实践**:
- 使用 Gauge 追踪并发请求、连接池大小、队列长度等
- 使用 `track_inprogress()` 上下文管理器自动追踪

### Histogram (直方图)

统计值的分布，自动计算 bucket。

```python
# 创建直方图
request_duration = manager.histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    labels=["method", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)
)

# 记录观测值
request_duration.labels(method="GET", endpoint="/api/users").observe(0.123)
request_duration.labels(method="POST", endpoint="/api/orders").observe(0.456)

# 使用计时上下文管理器
with request_duration.labels(method="GET", endpoint="/api/products").time():
    # 自动计时这个代码块的执行时间
    result = call_api()

# 获取样本统计
sample_count = request_duration.get_sample_count()
sample_sum = request_duration.get_sample_sum()
print(f"平均响应时间: {sample_sum / sample_count if sample_count > 0 else 0:.3f}s")
```

**最佳实践**:
- 使用 Histogram 统计响应时间、请求大小、处理时长等
- 根据实际需求自定义 buckets
- 使用 `.time()` 上下文管理器自动计时

### Summary (摘要)

统计百分位数。

```python
# 创建摘要
request_size = manager.summary(
    "http_request_size_bytes",
    "HTTP request size in bytes",
    labels=["method"]
)

# 记录观测值
request_size.labels(method="POST").observe(1024)
request_size.labels(method="GET").observe(256)

# 使用计时
with request_size.labels(method="PUT").time():
    upload_data()
```

## 装饰器使用

### 计数装饰器

```python
from df_test_framework.infrastructure.metrics.decorators import count_calls

@count_calls("api_calls_total", description="Total API calls", labels=["endpoint"])
def call_api(endpoint: str):
    # 每次调用自动增加计数
    return requests.get(endpoint)

# 或使用固定标签
@count_calls("db_queries_total", label_values={"operation": "select"})
def query_users():
    return db.query("SELECT * FROM users")
```

### 计时装饰器

```python
from df_test_framework.infrastructure.metrics.decorators import time_calls, time_async_calls

# 同步函数计时
@time_calls("request_duration_seconds", description="Request duration")
def process_request():
    time.sleep(0.1)
    return "OK"

# 异步函数计时
@time_async_calls("async_task_duration_seconds")
async def async_task():
    await asyncio.sleep(0.1)
    return "Done"

# 自定义 buckets
@time_calls(
    "api_call_duration_seconds",
    buckets=(0.01, 0.05, 0.1, 0.5, 1.0, 5.0)
)
def call_external_api():
    return requests.get("https://api.example.com")
```

### 进行中追踪装饰器

```python
from df_test_framework.infrastructure.metrics.decorators import (
    track_in_progress,
    track_async_in_progress
)

# 追踪同步函数
@track_in_progress("tasks_in_progress", description="Tasks in progress")
def process_task():
    # 函数执行期间，gauge 自动 +1
    time.sleep(1)
    # 函数退出后，gauge 自动 -1
    return "Done"

# 追踪异步函数
@track_async_in_progress("async_jobs_in_progress")
async def async_job():
    await asyncio.sleep(1)
    return "Done"
```

### 组合装饰器

```python
from df_test_framework.infrastructure.metrics.decorators import (
    count_calls,
    time_calls,
    track_in_progress
)

@count_calls("api_requests_total")
@time_calls("api_request_duration_seconds")
@track_in_progress("api_requests_in_progress")
def api_request(endpoint: str):
    """
    这个函数会自动:
    - 计数调用次数
    - 记录执行时间
    - 追踪并发数
    """
    return requests.get(endpoint)
```

## HTTP 请求指标

自动收集 HTTP 客户端请求指标。

### 使用 HTTP 指标拦截器

```python
from df_test_framework.clients.http import HttpClient
from df_test_framework.infrastructure.metrics.integrations.http import HttpMetrics

# 创建 HTTP 指标收集器
http_metrics = HttpMetrics(
    prefix="test_http",  # 指标名称前缀
    include_path_label=True,  # 包含路径标签
    path_cardinality_limit=100  # 路径基数限制
)

# 添加到 HTTP 客户端
client = HttpClient()
client.add_interceptor(http_metrics.interceptor())

# 现在所有请求都会自动记录指标
response = await client.get("https://api.example.com/users")
```

### 手动记录 HTTP 指标

```python
from df_test_framework.infrastructure.metrics.integrations.http import HttpMetrics

http_metrics = HttpMetrics()

# 记录请求指标
http_metrics.record_request(
    method="GET",
    path="/api/users",
    status_code=200,
    duration=0.345,
    request_size=0,
    response_size=1024
)
```

### HTTP 指标说明

自动收集的 HTTP 指标：

| 指标名称 | 类型 | 描述 | 标签 |
|---------|------|------|------|
| `http_requests_total` | Counter | HTTP 请求总数 | method, path, status_code |
| `http_request_duration_seconds` | Histogram | HTTP 请求耗时 | method, path |
| `http_requests_in_flight` | Gauge | 进行中的 HTTP 请求数 | - |
| `http_request_size_bytes` | Histogram | HTTP 请求大小 | method, path |
| `http_response_size_bytes` | Histogram | HTTP 响应大小 | method, path |

## 数据库查询指标

自动收集数据库查询性能指标。

### 使用数据库指标包装器

```python
from df_test_framework.infrastructure.metrics.integrations.database import DatabaseMetrics

# 创建数据库指标收集器
db_metrics = DatabaseMetrics(
    prefix="test_db",  # 指标名称前缀
    include_table_label=True  # 包含表名标签
)

# 手动记录查询指标
db_metrics.record_query(
    operation="SELECT",
    table="users",
    duration=0.045,
    rows=100
)

db_metrics.record_query(
    operation="INSERT",
    table="orders",
    duration=0.023,
    rows=1
)
```

### 数据库指标说明

自动收集的数据库指标：

| 指标名称 | 类型 | 描述 | 标签 |
|---------|------|------|------|
| `db_queries_total` | Counter | 数据库查询总数 | operation, table |
| `db_query_duration_seconds` | Histogram | 查询耗时 | operation, table |
| `db_query_rows` | Histogram | 查询返回行数 | operation, table |
| `db_connections_active` | Gauge | 活跃连接数 | - |

## 高级配置

### 自定义配置

```python
from df_test_framework.infrastructure.metrics import MetricsManager, MetricsConfig

# 创建自定义配置
config = MetricsConfig(
    service_name="my-test-service",
    enabled=True,  # 启用指标收集
    use_prometheus=True,  # 使用 prometheus_client 库
    server_port=8000,  # Prometheus exporter 端口
    pushgateway_url="http://pushgateway:9091",  # Pushgateway URL
    push_interval=10.0,  # 推送间隔（秒）
    default_labels={  # 默认标签
        "environment": "test",
        "version": "1.0.0"
    }
)

# 使用配置创建管理器
manager = MetricsManager(config=config)
manager.init()
```

### 启动 Prometheus HTTP Server

```python
# 启动 HTTP server（需要安装 prometheus_client）
manager.start_server(port=8000)

# 现在可以从 http://localhost:8000/metrics 获取指标
```

### 推送到 Pushgateway

```python
# 单次推送
manager.push_to_gateway()

# 启动定期推送循环
manager.start_push_loop(interval=10.0)

# 在测试结束时关闭
manager.shutdown()
```

## 在pytest中使用

### Fixture 方式

```python
import pytest
from df_test_framework.infrastructure.metrics import MetricsManager, get_metrics_manager

@pytest.fixture(scope="session")
def metrics_manager():
    """全局指标管理器"""
    manager = MetricsManager(service_name="test-suite")
    manager.init()
    yield manager
    manager.shutdown()

@pytest.fixture
def test_counter(metrics_manager):
    """测试计数器"""
    return metrics_manager.counter("test_counter", "Test counter")

def test_with_metrics(test_counter):
    """使用指标的测试"""
    test_counter.inc()

    # 执行测试逻辑
    result = some_function()

    assert result == expected
    assert test_counter.get() == 1
```

### 装饰器方式

```python
from df_test_framework.infrastructure.metrics.decorators import (
    count_calls,
    time_calls
)

class TestAPI:
    @count_calls("api_test_calls_total")
    @time_calls("api_test_duration_seconds")
    def test_api_endpoint(self):
        """每次测试自动记录调用次数和耗时"""
        response = call_api("/users")
        assert response.status_code == 200
```

### conftest.py 配置

```python
# conftest.py
import pytest
from df_test_framework.infrastructure.metrics import (
    MetricsManager,
    set_metrics_manager
)

def pytest_configure(config):
    """pytest 启动时初始化指标管理器"""
    manager = MetricsManager(service_name="pytest-suite")
    manager.init()
    set_metrics_manager(manager)

def pytest_unconfigure(config):
    """pytest 结束时收集并导出指标"""
    from df_test_framework.infrastructure.metrics import get_metrics_manager

    manager = get_metrics_manager()
    metrics = manager.collect()

    # 导出到文件
    import json
    with open("test_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    manager.shutdown()
```

## 与 Grafana 集成

### 1. 配置 Prometheus

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'test-framework'
    static_configs:
      - targets: ['localhost:8000']
        labels:
          service: 'df-test-framework'
```

### 2. 启动 Metrics Server

```python
from df_test_framework.infrastructure.metrics import get_metrics_manager

manager = get_metrics_manager()
manager.start_server(port=8000)

# 运行测试...

manager.shutdown()
```

### 3. Grafana Dashboard 示例

推荐的监控面板：

- **HTTP 请求监控**:
  - 请求速率: `rate(http_requests_total[5m])`
  - 平均响应时间: `rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])`
  - P95 响应时间: `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))`

- **数据库查询监控**:
  - 查询速率: `rate(db_queries_total[5m])`
  - 平均查询时间: `rate(db_query_duration_seconds_sum[5m]) / rate(db_query_duration_seconds_count[5m])`
  - 活跃连接数: `db_connections_active`

## 最佳实践

### 1. 指标命名规范

```python
# 好的命名
manager.counter("http_requests_total", ...)       # 明确的单位和类型
manager.histogram("request_duration_seconds", ...)  # 带单位
manager.gauge("connections_active", ...)          # 描述性名称

# 避免
manager.counter("requests", ...)                   # 不够明确
manager.histogram("duration", ...)                 # 缺少单位
manager.gauge("conn", ...)                         # 缩写不清晰
```

### 2. 标签使用

```python
# 好的标签
requests.labels(
    method="GET",           # 低基数
    status_code="200",     # 低基数
    endpoint="/api/users"  # 受限基数
)

# 避免高基数标签
requests.labels(
    user_id="12345",       # 高基数！
    request_id="abc123",   # 高基数！
    timestamp="2024-01-01" # 高基数！
)
```

### 3. 资源清理

```python
def setup_module():
    manager = MetricsManager(service_name="test")
    manager.init()

def teardown_module():
    from df_test_framework.infrastructure.metrics import get_metrics_manager
    manager = get_metrics_manager()
    manager.shutdown()
```

### 4. 条件启用

```python
import os

# 只在 CI 环境中启用指标
config = MetricsConfig(
    enabled=os.getenv("CI") == "true",
    pushgateway_url=os.getenv("PUSHGATEWAY_URL")
)
```

## 故障排查

### 指标未记录

```python
# 检查管理器是否初始化
manager = get_metrics_manager()
print(f"Is initialized: {manager.is_initialized}")
print(f"Is enabled: {manager.is_enabled}")

# 检查指标是否注册
metrics = manager.list_metrics()
print(f"Registered metrics: {metrics}")
```

### Prometheus Client 未安装

框架提供零配置模式，无需安装 `prometheus_client` 即可使用：

```python
# 使用内存存储（不需要 prometheus_client）
config = MetricsConfig(use_prometheus=False)
manager = MetricsManager(config=config)
```

### 端口冲突

```python
# 更改默认端口
manager.start_server(port=9090)
```

## 参考资料

- [Prometheus 文档](https://prometheus.io/docs/)
- [Prometheus 最佳实践](https://prometheus.io/docs/practices/)
- [Grafana 文档](https://grafana.com/docs/)

## 相关文档

- [分布式追踪指南](distributed_tracing.md)
- [日志系统配置](logging_best_practices.md)
- [性能测试](performance_testing.md)
