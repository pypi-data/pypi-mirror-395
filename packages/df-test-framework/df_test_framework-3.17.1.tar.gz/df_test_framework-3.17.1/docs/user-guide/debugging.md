# 调试工具使用指南

> 📚 **版本**: v2.0.0
> 🎯 **目标**: 使用内置调试工具快速定位和解决测试问题

---

## 📖 目录

- [简介](#简介)
- [HTTP调试工具](#http调试工具)
- [数据库调试工具](#数据库调试工具)
- [pytest调试插件](#pytest调试插件)
- [调试Fixtures](#调试fixtures)
- [实战示例](#实战示例)
- [最佳实践](#最佳实践)
- [常见问题](#常见问题)

---

## 简介

DF Test Framework v2.0 提供了强大的调试工具集，帮助您快速定位测试问题：

| 工具 | 用途 | 使用场景 |
|------|------|---------|
| **HTTPDebugger** | HTTP请求/响应调试 | API测试失败，需要查看请求详情 |
| **DBDebugger** | 数据库查询调试 | 慢查询分析，SQL优化 |
| **DebugPlugin** | pytest调试插件 | 测试失败自动收集环境信息 |
| **Fixtures** | 调试fixtures | 在测试中便捷使用调试工具 |

**核心优势**：
- 🔍 **自动记录**: 自动记录所有HTTP请求和数据库查询
- 📊 **统计分析**: 提供详细的性能统计和慢查询分析
- 🐛 **失败诊断**: 测试失败时自动保存环境信息
- ⚡ **零侵入**: 无需修改现有测试代码

---

## HTTP调试工具

### 基本用法

#### 方式1: 使用Fixture（推荐）

```python
def test_api(http_client, http_debugger):
    """测试API - 使用HTTP调试器"""
    # HTTP调试器自动启动
    response = http_client.get("/users/1")
    assert response.status_code == 200

    # 测试结束后自动打印调试信息
    http_debugger.print_summary()
```

#### 方式2: 手动使用

```python
from df_test_framework.testing import HTTPDebugger

def test_api_manual():
    """手动使用HTTP调试器"""
    debugger = HTTPDebugger()
    debugger.start()

    # 记录请求
    debugger.log_request("GET", "https://api.example.com/users/1")

    # 执行实际请求...

    # 记录响应
    debugger.log_response(200, body={"id": 1, "name": "John"})

    # 打印调试信息
    debugger.print_summary()
    debugger.stop()
```

#### 方式3: 全局调试器

```python
from df_test_framework.testing import enable_http_debug

# 在conftest.py中启用全局调试
@pytest.fixture(scope="session", autouse=True)
def enable_global_http_debug():
    debugger = enable_http_debug()
    yield
    # 所有测试结束后打印总结
    debugger.print_summary()
```

### HTTPDebugger API

| 方法 | 说明 | 示例 |
|------|------|------|
| `start()` | 启动调试 | `debugger.start()` |
| `stop()` | 停止调试 | `debugger.stop()` |
| `log_request()` | 记录请求 | `debugger.log_request("GET", "/users")` |
| `log_response()` | 记录响应 | `debugger.log_response(200, body={...})` |
| `log_error()` | 记录错误 | `debugger.log_error(exception)` |
| `get_requests()` | 获取所有请求 | `requests = debugger.get_requests()` |
| `get_failed_requests()` | 获取失败请求 | `failed = debugger.get_failed_requests()` |
| `print_summary()` | 打印摘要 | `debugger.print_summary()` |
| `clear()` | 清空记录 | `debugger.clear()` |

### 输出示例

```
================================================================================
📊 HTTP调试摘要
================================================================================

总请求数: 5
  成功: 4 ✅
  失败: 1 ❌

响应时间:
  平均: 245.67ms
  最快: 123.45ms
  最慢: 456.78ms

================================================================================
📋 请求详情:
================================================================================

1. ✅ GET https://api.example.com/users/1
   时间: 2025-11-02T10:30:45.123456
   耗时: 234.56ms
   状态: 200
   响应: {"id": 1, "name": "John"}

2. ❌ POST https://api.example.com/users
   时间: 2025-11-02T10:30:46.789012
   耗时: 345.67ms
   状态: 400
   响应: {"error": "Invalid request"}
================================================================================
```

---

## 数据库调试工具

### 基本用法

#### 方式1: 使用Fixture

```python
def test_database(database, db_debugger):
    """测试数据库 - 使用数据库调试器"""
    # 数据库调试器自动启动
    results = database.execute_query("SELECT * FROM users WHERE id = %s", (1,))
    assert len(results) > 0

    # 测试结束后打印调试信息
    db_debugger.print_summary()
```

#### 方式2: 手动使用

```python
from df_test_framework.testing import DBDebugger

def test_db_manual():
    """手动使用数据库调试器"""
    debugger = DBDebugger(slow_query_threshold_ms=100)
    debugger.start()

    # 记录查询开始
    debugger.log_query_start(
        "SELECT * FROM users WHERE status = %s",
        params=("active",)
    )

    # 执行实际查询...

    # 记录查询结束
    debugger.log_query_end(result_count=50)

    # 打印调试信息
    debugger.print_summary()
    debugger.stop()
```

### DBDebugger API

| 方法 | 说明 | 示例 |
|------|------|------|
| `start()` | 启动调试 | `debugger.start()` |
| `stop()` | 停止调试 | `debugger.stop()` |
| `log_query_start()` | 记录查询开始 | `debugger.log_query_start(sql, params)` |
| `log_query_end()` | 记录查询结束 | `debugger.log_query_end(result_count=10)` |
| `log_query_error()` | 记录查询错误 | `debugger.log_query_error(exception)` |
| `get_queries()` | 获取所有查询 | `queries = debugger.get_queries()` |
| `get_slow_queries()` | 获取慢查询 | `slow = debugger.get_slow_queries()` |
| `get_statistics()` | 获取统计信息 | `stats = debugger.get_statistics()` |
| `print_summary()` | 打印摘要 | `debugger.print_summary()` |

### 输出示例

```
================================================================================
📊 数据库查询摘要
================================================================================

总查询数: 10
  慢查询: 2 ⚠️
  失败: 0 ❌

查询耗时:
  平均: 45.67ms
  最快: 12.34ms
  最慢: 156.78ms
  总计: 456.70ms

================================================================================
🐌 慢查询详情 (阈值: 100ms):
================================================================================

1. SELECT o.*, u.name FROM orders o JOIN users u ON o.user_id = u.id WHERE o.created_at > '2025-01-01'...
   时间: 2025-11-02T10:30:45.123456
   耗时: 156.78ms
   参数: ('2025-01-01',)
   结果数: 500

2. SELECT * FROM products WHERE category = 'electronics' ORDER BY price DESC...
   时间: 2025-11-02T10:30:46.789012
   耗时: 123.45ms
   结果数: 200
================================================================================
```

---

## pytest调试插件

### 启用方式

#### 方式1: 命令行启用

```bash
# 启用调试模式
pytest --df-debug

# 指定调试信息保存目录
pytest --df-debug --df-debug-dir=custom/debug/path
```

#### 方式2: 环境变量启用

```bash
# 设置环境变量
export DF_DEBUG=1

# 运行测试
pytest -v
```

#### 方式3: pytest.ini配置

```ini
[pytest]
addopts = --df-debug --df-debug-dir=reports/debug
```

### 功能特性

#### 1. 自动保存失败信息

测试失败时自动保存JSON格式的调试信息：

```json
{
  "test_name": "tests/api/test_user.py::TestUser::test_create_user",
  "timestamp": "2025-11-02T10:30:45.123456",
  "failure_message": "AssertionError: assert 400 == 200",
  "environment": {
    "python_version": "3.10.0",
    "platform": "linux",
    "cwd": "/path/to/project",
    "env_vars": {
      "HTTP_BASE_URL": "https://api.example.com",
      "DB_HOST": "localhost"
    }
  },
  "test_metadata": {
    "file": "tests/api/test_user.py",
    "line": 45,
    "function": "test_create_user",
    "markers": ["smoke", "regression"],
    "fixtures": ["http_client", "database", "db_transaction"]
  }
}
```

#### 2. 自动打印调试信息

```
================================================================================
🐛 测试失败调试信息
================================================================================
测试: tests/api/test_user.py::TestUser::test_create_user
时间: 2025-11-02T10:30:45.123456

环境:
  Python: 3.10.0
  平台: linux
  工作目录: /path/to/project

相关环境变量:
  HTTP_BASE_URL: https://api.example.com
  DB_HOST: localhost
  DB_PORT: 3306
================================================================================
```

#### 3. 失败总结

所有测试完成后显示失败总结：

```
================================================================================
📊 测试失败总结: 3 个失败
================================================================================
1. tests/api/test_user.py::TestUser::test_create_user
2. tests/api/test_order.py::TestOrder::test_create_order
3. tests/api/test_payment.py::TestPayment::test_verify_payment
================================================================================
```

---

## 调试Fixtures

### 可用的Fixtures

| Fixture | Scope | 说明 |
|---------|-------|------|
| `http_debugger` | function | 函数级HTTP调试器 |
| `db_debugger` | function | 函数级数据库调试器 |
| `global_http_debugger` | session | 会话级HTTP调试器 |
| `global_db_debugger` | session | 会话级数据库调试器 |
| `auto_debug_on_failure` | function | 失败时自动打印调试信息 |

### 使用示例

#### 1. 函数级调试器

```python
def test_user_api(http_client, http_debugger):
    """每个测试独立的调试器"""
    response = http_client.get("/users/1")
    assert response.status_code == 200

    # 查看本测试的HTTP请求
    assert len(http_debugger.get_requests()) == 1
```

#### 2. 会话级调试器

```python
def test_user_list(http_client, global_http_debugger):
    """整个会话共享的调试器"""
    response = http_client.get("/users")
    assert response.status_code == 200

def test_user_detail(http_client, global_http_debugger):
    """使用同一个调试器"""
    response = http_client.get("/users/1")
    assert response.status_code == 200

    # 可以看到之前所有测试的HTTP请求
    assert len(global_http_debugger.get_requests()) >= 2
```

#### 3. 自动调试失败测试

```python
@pytest.mark.usefixtures("auto_debug_on_failure")
def test_with_auto_debug(http_client, database):
    """失败时自动打印HTTP和DB调试信息"""
    response = http_client.post("/users", json={"name": "test"})
    assert response.status_code == 201  # 如果失败，自动打印调试信息
```

---

## 实战示例

### 场景1: 调试API测试失败

```python
import pytest

class TestUserAPI:
    """用户API测试"""

    def test_create_user_debug(self, http_client, http_debugger, db_debugger):
        """创建用户测试 - 带调试"""
        # 准备测试数据
        user_data = {
            "name": "Test User",
            "email": "test@example.com"
        }

        # 调用API
        response = http_client.post("/users", json=user_data)

        # 断言失败时，可以查看详细的HTTP请求/响应
        assert response.status_code == 201, \
            f"创建用户失败: {http_debugger.get_requests()}"

        # 验证数据库
        user_id = response.json()["id"]
        result = database.execute_query(
            "SELECT * FROM users WHERE id = %s", (user_id,)
        )

        # 断言失败时，可以查看SQL查询
        assert len(result) == 1, \
            f"数据库验证失败: {db_debugger.get_queries()}"

        # 打印调试摘要
        print("\n--- HTTP调试信息 ---")
        http_debugger.print_summary()

        print("\n--- 数据库调试信息 ---")
        db_debugger.print_summary()
```

### 场景2: 分析慢查询

```python
def test_slow_query_analysis(database, db_debugger):
    """分析慢查询"""
    # 设置慢查询阈值为50ms
    db_debugger.slow_query_threshold_ms = 50

    # 执行多个查询
    database.execute_query("SELECT * FROM users")
    database.execute_query(
        "SELECT o.*, u.name FROM orders o JOIN users u ON o.user_id = u.id"
    )
    database.execute_query("SELECT * FROM products WHERE category = 'electronics'")

    # 获取慢查询
    slow_queries = db_debugger.get_slow_queries()

    if slow_queries:
        print(f"\n发现 {len(slow_queries)} 个慢查询:")
        for query in slow_queries:
            print(f"  - {query['sql'][:50]}... ({query['duration_ms']:.2f}ms)")

    # 打印完整的调试摘要
    db_debugger.print_summary()
```

### 场景3: 综合调试会话

```python
@pytest.fixture(scope="session")
def comprehensive_debug(global_http_debugger, global_db_debugger):
    """综合调试会话"""
    yield

    # 所有测试完成后打印完整的调试报告
    print("\n" + "=" * 80)
    print("📊 完整调试报告")
    print("=" * 80)

    print("\n【HTTP请求统计】")
    global_http_debugger.print_summary()

    print("\n【数据库查询统计】")
    global_db_debugger.print_summary()

    # 性能分析
    http_stats = global_http_debugger.get_requests()
    db_stats = global_db_debugger.get_statistics()

    print("\n【性能分析】")
    print(f"  总HTTP请求: {len(http_stats)}")
    print(f"  总数据库查询: {db_stats.get('total_queries', 0)}")
    print(f"  平均HTTP响应时间: {sum(r['duration_ms'] for r in http_stats if r['duration_ms']) / len(http_stats):.2f}ms")
    print(f"  平均数据库查询时间: {db_stats.get('avg_duration_ms', 0):.2f}ms")

# 使用综合调试
pytestmark = pytest.mark.usefixtures("comprehensive_debug")

class TestWithComprehensiveDebug:
    def test_user_flow(self, http_client, database):
        """用户流程测试"""
        # 所有HTTP和DB操作都会被记录
        pass
```

### 场景4: 失败时保存现场

```python
def test_with_failure_snapshot(http_client, database):
    """失败时保存现场信息"""
    # 启用调试插件（通过--df-debug）

    # 执行测试
    response = http_client.post("/complex-api", json={...})

    # 如果这里失败，调试插件会自动保存:
    # - 完整的环境信息
    # - 测试元数据
    # - 失败堆栈
    # 到 reports/debug/failure_*.json
    assert response.status_code == 200
```

---

## 最佳实践

### 1. 合理选择调试器作用域

```python
# ✅ 好的做法 - 针对性调试
def test_specific_api(http_debugger):
    """只调试这个测试"""
    # http_debugger是函数级别的
    pass

# ✅ 好的做法 - 全局监控
@pytest.fixture(scope="session", autouse=True)
def monitor_all_requests(global_http_debugger):
    """监控所有测试的HTTP请求"""
    yield
    # 测试结束后查看统计
    if global_http_debugger.get_failed_requests():
        print("⚠️  发现失败的HTTP请求")
        global_http_debugger.print_summary()
```

### 2. 条件启用调试

```python
import os

@pytest.fixture(scope="session")
def conditional_debug():
    """根据环境变量条件启用调试"""
    if os.getenv("DEBUG_HTTP") == "1":
        from df_test_framework.testing import enable_http_debug
        enable_http_debug()

    if os.getenv("DEBUG_DB") == "1":
        from df_test_framework.testing import enable_db_debug
        enable_db_debug(slow_query_threshold_ms=50)
```

### 3. 自定义调试报告

```python
def test_with_custom_report(http_debugger, db_debugger):
    """自定义调试报告"""
    # 执行测试...

    # 自定义报告格式
    http_requests = http_debugger.get_requests()
    slow_queries = db_debugger.get_slow_queries()

    report = {
        "total_http_requests": len(http_requests),
        "failed_http_requests": len(http_debugger.get_failed_requests()),
        "slow_queries_count": len(slow_queries),
        "slowest_query_ms": max(q['duration_ms'] for q in slow_queries) if slow_queries else 0,
    }

    # 保存到文件或发送到监控系统
    print(f"\n自定义报告: {report}")
```

### 4. 集成到CI/CD

```yaml
# .github/workflows/test.yml
name: Test with Debug

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Run tests with debug
        run: |
          pytest --df-debug --df-debug-dir=reports/debug
        env:
          DF_DEBUG: "1"

      - name: Upload debug reports
        if: failure()
        uses: actions/upload-artifact@v2
        with:
          name: debug-reports
          path: reports/debug/
```

### 5. 性能监控模式

```python
@pytest.fixture(scope="session")
def performance_monitor(global_http_debugger, global_db_debugger):
    """性能监控模式"""
    yield

    # 检查性能阈值
    http_requests = global_http_debugger.get_requests()
    slow_requests = [r for r in http_requests if r.get('duration_ms', 0) > 1000]

    db_stats = global_db_debugger.get_statistics()
    slow_queries = global_db_debugger.get_slow_queries()

    # 性能警告
    if slow_requests:
        print(f"\n⚠️  警告: 发现 {len(slow_requests)} 个慢HTTP请求 (>1s)")

    if len(slow_queries) > 10:
        print(f"\n⚠️  警告: 发现 {len(slow_queries)} 个慢查询")

    # 性能报告
    print(f"\n📊 性能报告:")
    print(f"  HTTP平均响应: {sum(r.get('duration_ms', 0) for r in http_requests) / len(http_requests):.2f}ms")
    print(f"  DB平均查询: {db_stats.get('avg_duration_ms', 0):.2f}ms")
```

---

## 常见问题

### Q1: 如何在所有测试中自动启用HTTP调试？

**方案**: 在`conftest.py`中使用session级fixture：

```python
# conftest.py
import pytest
from df_test_framework.testing import enable_http_debug

@pytest.fixture(scope="session", autouse=True)
def auto_http_debug():
    debugger = enable_http_debug()
    yield
    debugger.print_summary()
```

### Q2: 调试信息太多，如何过滤？

**方案**: 使用条件打印或自定义过滤：

```python
def test_example(http_debugger):
    # 执行测试...

    # 只打印失败的请求
    failed = http_debugger.get_failed_requests()
    if failed:
        print(f"\n失败的请求数: {len(failed)}")
        for req in failed:
            print(f"  - {req['method']} {req['url']}: {req['response']['status_code']}")
```

### Q3: 如何保存调试信息到文件？

**方案**: 手动保存或使用pytest插件：

```python
import json

def test_save_debug_info(http_debugger, db_debugger):
    # 执行测试...

    # 保存到文件
    debug_data = {
        "http_requests": http_debugger.get_requests(),
        "db_queries": db_debugger.get_queries(),
        "db_statistics": db_debugger.get_statistics(),
    }

    with open("debug_report.json", "w") as f:
        json.dump(debug_data, f, indent=2)
```

### Q4: 调试信息会影响测试性能吗？

**回答**: 影响很小，但可以优化：

- 使用`max_body_length`限制记录的body大小
- 只在失败时启用详细调试
- 使用条件调试（如只在CI环境启用）

```python
import os

# 只在CI环境启用详细调试
if os.getenv("CI"):
    debugger = HTTPDebugger(max_body_length=5000)
else:
    debugger = HTTPDebugger(max_body_length=100)
```

### Q5: 如何调试特定的URL或查询？

**方案**: 使用过滤功能：

```python
def test_filter_debug(http_debugger):
    # 执行测试...

    # 只查看特定URL的请求
    user_requests = [
        r for r in http_debugger.get_requests()
        if "/users" in r['url']
    ]

    print(f"\n用户API请求数: {len(user_requests)}")
```

### Q6: 测试失败时没有保存调试信息？

**检查项**:
1. 确保启用了调试插件（`--df-debug`或环境变量）
2. 检查调试目录权限
3. 查看pytest输出中的错误信息

```bash
# 启用详细输出
pytest -vv --df-debug --log-cli-level=DEBUG
```

### Q7: 如何在Allure报告中显示调试信息？

**方案**: 使用Allure的attach功能：

```python
import allure
import json

def test_with_allure(http_debugger):
    # 执行测试...

    # 附加调试信息到Allure报告
    debug_info = {
        "requests": http_debugger.get_requests(),
        "failed_requests": http_debugger.get_failed_requests(),
    }

    allure.attach(
        json.dumps(debug_info, indent=2, ensure_ascii=False),
        name="HTTP调试信息",
        attachment_type=allure.attachment_type.JSON
    )
```

### Q8: 如何清理调试记录？

**方案**: 使用`clear()`方法或管理调试文件：

```python
def test_with_cleanup(http_debugger):
    # 执行第一批测试
    http_debugger.clear()  # 清空之前的记录

    # 执行第二批测试
    pass
```

---

## 相关资源

- **📚 问题排查指南**: [troubleshooting/common-errors.md](../troubleshooting/common-errors.md)
- **📖 测试指南**: [getting-started/writing-first-test.md](../getting-started/writing-first-test.md)
- **🏗️ 架构文档**: [architecture/v2-architecture.md](../architecture/v2-architecture.md)
- **💡 示例代码**: [examples目录](../../examples/)

---

## 总结

调试工具帮助您：

1. **快速定位问题** - 自动记录请求和查询详情
2. **性能优化** - 识别慢请求和慢查询
3. **失败诊断** - 自动保存失败时的环境信息
4. **提升效率** - 无需手动添加日志即可调试

**开始使用**：

```python
# 1. 在测试中使用调试fixture
def test_example(http_client, http_debugger, db_debugger):
    pass

# 2. 启用pytest调试插件
# pytest --df-debug

# 3. 查看调试报告
# ls reports/debug/
```

---

**文档版本**: v2.0.0
**最后更新**: 2025-11-02
**维护者**: DF Test Framework Team
