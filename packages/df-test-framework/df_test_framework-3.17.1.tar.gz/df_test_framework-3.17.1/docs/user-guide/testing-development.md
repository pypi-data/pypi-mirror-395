# 测试开发指南

本指南旨在帮助开发者为 DF Test Framework 编写高质量的单元测试和集成测试。

## 📋 目录

- [概述](#概述)
- [测试策略](#测试策略)
- [测试环境配置](#测试环境配置)
- [单元测试](#单元测试)
- [集成测试](#集成测试)
- [覆盖率管理](#覆盖率管理)
- [常见测试模式](#常见测试模式)
- [故障排查](#故障排查)

---

## 📖 概述

### 测试框架技术栈

- **pytest**: 测试运行框架
- **pytest-cov**: 测试覆盖率工具
- **pytest-mock**: Mock 和 fixture 支持
- **unittest.mock**: Python 标准库 Mock
- **pytest-xdist**: 并行测试执行

### 测试目标

- 🎯 **覆盖率目标**: 80%
- ✅ **质量保证**: 确保代码变更不引入回归
- 📝 **文档化**: 测试即文档，清晰展示功能用法
- 🚀 **快速反馈**: 快速发现和定位问题

---

## 🎯 测试策略

### 测试金字塔

```
        /\
       /  \        E2E Tests (少量)
      /----\       - 完整业务流程测试
     /      \      - 关键路径验证
    /--------\
   / Integration \  Integration Tests (适量)
  /--------------\  - 多模块协作
 /   Unit Tests   \ - 组件间交互
/------------------\
     Unit Tests      Unit Tests (大量)
                     - 单个函数/类
                     - 快速执行
                     - 高覆盖率
```

### 测试分类

| 类型 | 目的 | 范围 | 速度 | 数量 |
|------|------|------|------|------|
| **单元测试** | 测试单个函数/类 | 最小 | 快 | 多 |
| **集成测试** | 测试模块间交互 | 中等 | 中等 | 适量 |
| **端到端测试** | 测试完整流程 | 最大 | 慢 | 少 |

---

## ⚙️ 测试环境配置

### 项目配置文件

测试配置在 `pyproject.toml` 中：

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-v",                    # 详细输出
    "--strict-markers",      # 严格标记模式
    "--tb=short",           # 简短回溯
]
markers = [
    "smoke: 冒烟测试",
    "regression: 回归测试",
    "integration: 集成测试",
    "e2e: 端到端测试",
    "slow: 慢速测试",
    "performance: 性能测试",
]
timeout = 30
timeout_method = "thread"

[tool.coverage.run]
source = ["src/df_test_framework"]
omit = [
    "*/tests/*",
    "*/__init__.py",
    "*/conftest.py",
]
branch = true

[tool.coverage.report]
fail_under = 80
precision = 2
show_missing = true
skip_covered = false
```

### 运行测试命令

```bash
# 基本测试运行
pytest                              # 运行所有测试
pytest -v                           # 详细输出
pytest -x                           # 第一个失败后停止
pytest -k "test_name"               # 运行匹配名称的测试
pytest tests/utils/                 # 运行指定目录的测试
pytest tests/utils/test_common.py   # 运行指定文件

# 使用标记
pytest -m smoke                     # 只运行冒烟测试
pytest -m "not slow"                # 排除慢速测试
pytest -m "smoke or regression"     # 运行多种标记

# 并行执行
pytest -n auto                      # 自动检测CPU核心数并行执行
pytest -n 4                         # 使用4个进程并行

# 覆盖率测试
pytest --cov=src/df_test_framework              # 生成覆盖率
pytest --cov=src/df_test_framework --cov-report=term-missing  # 显示未覆盖行
pytest --cov=src/df_test_framework --cov-report=html          # 生成HTML报告
```

---

## 🧪 单元测试

### 单元测试结构

```python
"""测试 module_name.py - 模块说明

测试覆盖:
- 功能1
- 功能2
- 边界条件
- 异常处理
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from df_test_framework.module import ClassName


class TestClassName:
    """测试 ClassName 类"""

    @pytest.fixture
    def instance(self):
        """创建测试实例"""
        return ClassName(param="value")

    @pytest.fixture
    def mock_dependency(self):
        """Mock外部依赖"""
        return Mock()

    def test_init_with_defaults(self):
        """测试使用默认参数初始化"""
        instance = ClassName()
        assert instance.attr == "default_value"

    def test_method_success_scenario(self, instance):
        """测试方法成功场景"""
        result = instance.method("input")
        assert result == "expected"

    def test_method_with_invalid_input(self, instance):
        """测试方法异常场景"""
        with pytest.raises(ValueError, match="Invalid input"):
            instance.method(None)

    @patch('df_test_framework.module.external_call')
    def test_method_with_external_dependency(self, mock_call, instance):
        """测试依赖外部调用的方法"""
        mock_call.return_value = "mocked"

        result = instance.method_using_external()

        assert result == "expected"
        mock_call.assert_called_once_with("arg")


__all__ = [
    "TestClassName",
]
```

### 单元测试示例

#### 1. 测试普通函数

```python
from df_test_framework.utils.common import random_string


class TestRandomString:
    """测试 random_string 函数"""

    def test_default_length(self):
        """测试默认长度"""
        result = random_string()
        assert len(result) == 10

    def test_custom_length(self):
        """测试自定义长度"""
        result = random_string(length=20)
        assert len(result) == 20

    def test_custom_chars(self):
        """测试自定义字符集"""
        result = random_string(length=10, chars="ABC")
        assert len(result) == 10
        assert all(c in "ABC" for c in result)

    def test_empty_length(self):
        """测试空字符串"""
        result = random_string(length=0)
        assert result == ""
```

#### 2. 测试类方法

```python
from df_test_framework.utils.data_generator import DataGenerator


class TestDataGenerator:
    """测试 DataGenerator 类"""

    @pytest.fixture
    def generator(self):
        """数据生成器实例"""
        return DataGenerator()

    def test_random_int_default_range(self, generator):
        """测试生成默认范围的随机整数"""
        result = generator.random_int()
        assert isinstance(result, int)
        assert 0 <= result <= 100

    def test_random_int_custom_range(self, generator):
        """测试生成自定义范围的随机整数"""
        result = generator.random_int(min_value=50, max_value=100)
        assert 50 <= result <= 100
```

#### 3. 测试异常处理

```python
from df_test_framework.utils.common import load_json


class TestLoadJson:
    """测试 load_json 函数"""

    def test_file_not_found(self):
        """测试文件不存在时抛出异常"""
        with pytest.raises(FileNotFoundError, match="文件不存在"):
            load_json("nonexistent.json")

    def test_invalid_json(self, tmp_path):
        """测试无效JSON时抛出异常"""
        json_file = tmp_path / "invalid.json"
        json_file.write_text("{ invalid json }")

        with pytest.raises(json.JSONDecodeError):
            load_json(str(json_file))
```

#### 4. 使用 Mock

```python
from unittest.mock import Mock, patch
from df_test_framework.clients.http.interceptors.logging import LoggingInterceptor


class TestLoggingInterceptor:
    """测试 LoggingInterceptor"""

    @pytest.fixture
    def interceptor(self):
        """拦截器实例"""
        return LoggingInterceptor()

    @pytest.fixture
    def mock_request(self):
        """Mock请求对象"""
        request = Mock()
        request.method = "GET"
        request.url = "https://api.example.com/users"
        request.headers = {"Content-Type": "application/json"}
        return request

    @patch('df_test_framework.clients.http.interceptors.logging.logger')
    def test_before_request_logs_request(self, mock_logger, interceptor, mock_request):
        """测试请求日志记录"""
        interceptor.before_request(mock_request)

        # 验证logger被调用
        mock_logger.log.assert_called_once()
        call_args = mock_logger.log.call_args

        # 验证日志级别和内容
        assert call_args[0][0] == "INFO"
        assert "GET" in call_args[0][1]
```

---

## 🔗 集成测试

### 集成测试特点

- 测试多个模块间的交互
- 可能需要真实的外部依赖（数据库、Redis等）
- 执行时间较长
- 使用 `@pytest.mark.integration` 标记

### 集成测试示例

#### HTTP客户端集成测试

```python
import pytest
from df_test_framework import Bootstrap, FrameworkSettings
from df_test_framework.clients.http import HTTPClient


@pytest.mark.integration
class TestHTTPClientIntegration:
    """HTTP客户端集成测试"""

    @pytest.fixture
    def runtime(self):
        """创建运行时环境"""
        return (
            Bootstrap()
            .with_settings(FrameworkSettings)
            .build()
            .run()
        )

    @pytest.fixture
    def http_client(self, runtime):
        """获取HTTP客户端"""
        return runtime.http_client()

    def test_get_request_with_real_api(self, http_client):
        """测试真实API请求"""
        response = http_client.get("https://jsonplaceholder.typicode.com/users/1")

        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["id"] == 1
```

---

## 📊 覆盖率管理

### 查看覆盖率

```bash
# 生成覆盖率报告
pytest --cov=src/df_test_framework --cov-report=term-missing

# 示例输出
Name                                          Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------------------------------------
src/df_test_framework/utils/common.py           42      0     12      0   100%
src/df_test_framework/utils/assertion.py        58      0     16      0   100%
src/df_test_framework/cli/utils.py              47      1     10      1    97%   89
-----------------------------------------------------------------------------------------
TOTAL                                          2456    945    456     89    61.62%
```

### 生成HTML报告

```bash
pytest --cov=src/df_test_framework --cov-report=html

# 报告位置: reports/coverage/index.html
```

### 查看特定模块覆盖率

```bash
# 只测试特定模块并查看覆盖率
pytest tests/utils/ --cov=src/df_test_framework/utils --cov-report=term-missing
```

### 覆盖率配置

`pyproject.toml` 中的覆盖率配置：

```toml
[tool.coverage.run]
source = ["src/df_test_framework"]  # 覆盖率源目录
omit = [
    "*/tests/*",                    # 排除测试文件
    "*/__init__.py",                # 排除__init__.py
    "*/conftest.py",                # 排除conftest.py
]
branch = true                       # 启用分支覆盖率

[tool.coverage.report]
fail_under = 80                     # 最低覆盖率要求
precision = 2                       # 覆盖率精度
show_missing = true                 # 显示未覆盖的行
skip_covered = false                # 不跳过已覆盖的文件

[tool.coverage.html]
directory = "reports/coverage"      # HTML报告目录
```

### 提升覆盖率策略

1. **识别未覆盖代码**
   ```bash
   pytest --cov=src/df_test_framework --cov-report=term-missing | grep "Missing"
   ```

2. **优先级排序**
   - P0: 核心功能模块（clients、databases、infrastructure）
   - P1: 工具类（utils、testing/fixtures）
   - P2: 辅助功能（extensions、debug工具）

3. **编写针对性测试**
   - 针对未覆盖的代码行编写测试
   - 覆盖所有分支条件
   - 测试异常处理路径

4. **持续监控**
   - 每次PR检查覆盖率变化
   - 确保新代码有相应测试
   - 逐步提升整体覆盖率

---

## 🎨 常见测试模式

### 1. 使用 pytest fixtures

```python
import pytest


@pytest.fixture
def sample_data():
    """共享测试数据"""
    return {"name": "Alice", "age": 25}


@pytest.fixture
def temp_file(tmp_path):
    """临时文件fixture"""
    file_path = tmp_path / "test.txt"
    file_path.write_text("test content")
    yield file_path
    # 清理会自动进行（tmp_path会被清理）


def test_with_fixture(sample_data):
    """使用fixture的测试"""
    assert sample_data["name"] == "Alice"
```

### 2. 参数化测试

```python
@pytest.mark.parametrize("input,expected", [
    ("my-test", "my_test"),
    ("UserLogin", "user_login"),
    ("HTTPClient", "http_client"),
])
def test_to_snake_case(input, expected):
    """测试命名转换"""
    assert to_snake_case(input) == expected
```

### 3. 测试临时文件

```python
import json


def test_load_json_file(tmp_path):
    """测试加载JSON文件"""
    # 创建临时JSON文件
    json_file = tmp_path / "test.json"
    data = {"name": "Alice", "age": 25}
    json_file.write_text(json.dumps(data))

    # 测试加载
    result = load_json(str(json_file))
    assert result == data
```

### 4. Mock外部依赖

```python
from unittest.mock import Mock, patch


@patch('httpx.Client')
def test_http_request_with_mock(mock_client):
    """测试HTTP请求（使用Mock）"""
    # 配置Mock返回值
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True}
    mock_client.return_value.get.return_value = mock_response

    # 执行测试
    client = HTTPClient()
    response = client.get("/users")

    # 验证
    assert response.status_code == 200
    assert response.json()["success"] is True
```

### 5. 测试异步代码

```python
import pytest


@pytest.mark.asyncio
async def test_async_function():
    """测试异步函数"""
    result = await async_function()
    assert result == "expected"
```

### 6. 测试上下文管理器

```python
def test_context_manager():
    """测试上下文管理器"""
    with ContextManager() as cm:
        assert cm.is_open is True
    assert cm.is_open is False
```

---

## 🔍 故障排查

### 常见测试问题

#### 1. 测试失败：ImportError

**问题**: 无法导入模块
```
ImportError: cannot import name 'ClassName' from 'module'
```

**解决方案**:
```bash
# 确保安装了开发依赖
uv pip install -e ".[dev]"

# 检查Python路径
echo $PYTHONPATH

# 重新安装
uv pip uninstall df-test-framework
uv pip install -e ".[dev]"
```

#### 2. 测试失败：Fixture not found

**问题**: pytest找不到fixture
```
fixture 'http_client' not found
```

**解决方案**:
- 检查 `conftest.py` 文件位置
- 确保fixture定义在正确的作用域
- 检查fixture名称拼写

#### 3. Coverage报告不准确

**问题**: 覆盖率显示为0%或异常

**解决方案**:
```bash
# 清理缓存
rm -rf .pytest_cache __pycache__ .coverage reports/coverage

# 重新运行
pytest --cov=src/df_test_framework --cov-report=html
```

#### 4. Mock不生效

**问题**: Mock对象没有按预期工作

**解决方案**:
```python
# 确保patch路径正确（使用对象被引用的位置，而非定义的位置）
# ❌ 错误
@patch('httpx.Client')

# ✅ 正确
@patch('df_test_framework.clients.http.rest.httpx_client.httpx.Client')
```

#### 5. 测试超时

**问题**: 测试运行超过配置的超时时间

**解决方案**:
```python
# 方法1: 增加特定测试的超时时间
@pytest.mark.timeout(60)
def test_slow_operation():
    pass

# 方法2: 标记为慢速测试
@pytest.mark.slow
def test_slow_operation():
    pass

# 运行时排除慢速测试
pytest -m "not slow"
```

### 调试测试

```bash
# 在第一个失败处停止
pytest -x

# 显示完整回溯
pytest --tb=long

# 显示print输出
pytest -s

# 进入调试器
pytest --pdb

# 详细输出
pytest -vv
```

---

## 📚 参考资源

### 内部文档
- [CONTRIBUTING.md](../../CONTRIBUTING.md) - 贡献指南
- [API参考](../api-reference/README.md) - API文档
- [示例代码](../../examples/) - 示例项目

### 外部资源
- [pytest官方文档](https://docs.pytest.org/)
- [pytest-cov文档](https://pytest-cov.readthedocs.io/)
- [unittest.mock文档](https://docs.python.org/3/library/unittest.mock.html)

---

## ✅ 最佳实践总结

1. ✅ **保持测试独立**: 每个测试应该独立运行
2. ✅ **使用清晰命名**: 测试名称应描述测试场景
3. ✅ **遵循AAA模式**: Arrange-Act-Assert
4. ✅ **一个测试一个断言**: 每个测试只验证一个行为
5. ✅ **使用fixtures共享设置**: 避免重复代码
6. ✅ **Mock外部依赖**: 保持测试快速和稳定
7. ✅ **测试边界条件**: 覆盖正常、异常和边界情况
8. ✅ **保持覆盖率**: 维持80%以上的代码覆盖率
9. ✅ **定期重构测试**: 保持测试代码质量
10. ✅ **持续集成**: 每次提交都运行测试

---

**最后更新**: 2025-11-10
