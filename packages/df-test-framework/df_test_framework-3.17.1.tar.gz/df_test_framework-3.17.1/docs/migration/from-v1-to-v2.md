# v1 到 v2 迁移指南

本文档帮助您将现有的v1测试代码迁移到v2版本。

## 🎯 迁移概述

### 主要变更

1. **目录结构重组**: 扁平化模块结构
2. **导入路径简化**: 统一从顶层导入
3. **配置系统升级**: 使用Pydantic v2
4. **类型安全增强**: 更完善的类型注解
5. **扩展系统重构**: 基于pluggy的Hook机制

### 兼容性

- ✅ Python 3.10+
- ✅ 大部分v1 API保持兼容
- ⚠️ 部分配置项需要调整
- ⚠️ 扩展系统完全重构

## 📝 迁移步骤

### 1. 更新依赖

```bash
# 卸载旧版本
pip uninstall df-test-framework

# 安装新版本
uv pip install df-test-framework>=2.0.0
```

### 2. 更新导入路径

#### v1 导入方式 (已废弃)
```python
# ❌ v1 - 深层导入
from df_test_framework.infrastructure.bootstrap.bootstrap import Bootstrap
from df_test_framework.infrastructure.runtime.runtime import RuntimeContext
from df_test_framework.core.http.http_client import HttpClient
from df_test_framework.builders.dict_builder import DictBuilder
```

#### v2 导入方式 (推荐)
```python
# ✅ v2 - 顶层导入
from df_test_framework import (
    Bootstrap,
    RuntimeContext,
    HttpClient,
    DictBuilder,
)
```

### 3. 更新配置定义

#### v1 配置方式
```python
# ❌ v1
from df_test_framework.infrastructure.config.settings import FrameworkSettings

class MySettings(FrameworkSettings):
    api_url: str = "https://api.example.com"

    class Config:
        env_prefix = "APP_"
```

#### v2 配置方式
```python
# ✅ v2 - 使用Pydantic v2
from df_test_framework import FrameworkSettings
from pydantic import Field

class MySettings(FrameworkSettings):
    api_url: str = Field(default="https://api.example.com")

    model_config = {
        "env_prefix": "APP_"
    }
```

### 4. 更新Bootstrap初始化

#### v1 初始化方式
```python
# ❌ v1
from df_test_framework.infrastructure.bootstrap import Bootstrap

bootstrap = Bootstrap(settings=MySettings())
runtime = bootstrap.initialize()
```

#### v2 初始化方式
```python
# ✅ v2 - 链式调用
from df_test_framework import Bootstrap

app = Bootstrap().with_settings(MySettings).build()
runtime = app.run()
```

### 5. 更新扩展系统

#### v1 扩展方式 (已废弃)
```python
# ❌ v1 - 旧的监控系统
from df_test_framework.monitoring import register_monitor

@register_monitor
class MyMonitor:
    def on_request(self, request):
        pass
```

#### v2 扩展方式
```python
# ✅ v2 - pluggy Hook系统
from df_test_framework.extensions import hookimpl

class MyExtension:
    @hookimpl
    def before_http_request(self, request):
        # 在请求前执行
        pass

    @hookimpl
    def after_http_response(self, response):
        # 在响应后执行
        pass

# 注册扩展
app = Bootstrap().with_extensions([MyExtension()]).build()
```

### 6. 更新Fixture使用

#### v1 Fixture
```python
# ❌ v1 - 手动创建
import pytest

@pytest.fixture
def http_client():
    from df_test_framework.core.http import HttpClient
    return HttpClient(base_url="https://api.example.com")
```

#### v2 Fixture
```python
# ✅ v2 - 使用内置fixture
def test_api(http_client):
    # http_client自动注入
    response = http_client.get("/users")
    assert response.status_code == 200
```

## 🔄 API对照表

### 核心类

| v1 | v2 | 说明 |
|----|----|----|
| `Bootstrap(settings=...)` | `Bootstrap().with_settings(...).build()` | 链式调用 |
| `runtime.get_http_client()` | `runtime.http_client()` | 简化方法名 |
| `runtime.get_database()` | `runtime.database()` | 简化方法名 |
| `TestConfig` | `TestExecutionConfig` | 重命名 |

### 配置项

| v1 | v2 | 说明 |
|----|----|----|
| `class Config: env_prefix` | `model_config = {"env_prefix": ...}` | Pydantic v2语法 |
| `HTTPConfig` | `HTTPConfig` | 保持不变 |
| `DatabaseConfig` | `DatabaseConfig` | 保持不变 |

### Builder和Repository

| v1 | v2 | 说明 |
|----|----|----|
| `DictBuilder` | `DictBuilder` | 保持不变 |
| `BaseBuilder` | `BaseBuilder[T]` | 添加泛型支持 |
| `BaseRepository` | `BaseRepository[T]` | 添加泛型支持 |

## ⚠️ 废弃功能

### 已移除

1. **QueryBuilder**: 使用SQLAlchemy原生查询
2. **旧监控系统**: 使用新的Extension系统
3. **全局Logger实例**: 使用loguru直接导入

### 替代方案

#### QueryBuilder → SQLAlchemy
```python
# ❌ v1 - QueryBuilder
from df_test_framework.builders import QueryBuilder
query = QueryBuilder().select("*").from_table("users").build()

# ✅ v2 - 原生SQLAlchemy
from sqlalchemy import select, table
users_table = table("users")
query = select(users_table)
```

#### 旧监控 → Extension
```python
# ❌ v1
from df_test_framework.monitoring import APIMonitor

# ✅ v2
from df_test_framework.extensions.builtin import APIPerformanceTracker
app = Bootstrap().with_extensions([APIPerformanceTracker()]).build()
```

## 🧪 测试迁移示例

### 完整示例对比

#### v1 测试代码
```python
# ❌ v1
from df_test_framework.infrastructure.bootstrap.bootstrap import Bootstrap
from df_test_framework.infrastructure.config.settings import FrameworkSettings
from df_test_framework.core.http.http_client import HttpClient

class MySettings(FrameworkSettings):
    api_url: str = "https://api.example.com"

def test_user_api():
    bootstrap = Bootstrap(settings=MySettings())
    runtime = bootstrap.initialize()
    http = runtime.get_http_client()

    response = http.get("/users/1")
    assert response.status_code == 200
```

#### v2 测试代码
```python
# ✅ v2
from df_test_framework import Bootstrap, FrameworkSettings
from pydantic import Field

class MySettings(FrameworkSettings):
    api_url: str = Field(default="https://api.example.com")

def test_user_api(http_client):  # 自动注入
    response = http_client.get("/users/1")
    assert response.status_code == 200
```

## 🔧 自动化迁移工具

我们提供了迁移脚本帮助批量更新导入路径：

```python
# migrate_imports.py
import re
from pathlib import Path

def migrate_file(file_path: Path):
    content = file_path.read_text(encoding="utf-8")

    # 替换导入路径
    patterns = {
        r"from df_test_framework\.infrastructure\.bootstrap\.bootstrap import":
            "from df_test_framework import",
        r"from df_test_framework\.infrastructure\.runtime\.runtime import":
            "from df_test_framework import",
        r"from df_test_framework\.core\.http\.http_client import":
            "from df_test_framework import",
        r"from df_test_framework\.builders\.dict_builder import":
            "from df_test_framework import",
    }

    for old, new in patterns.items():
        content = re.sub(old, new, content)

    file_path.write_text(content, encoding="utf-8")

# 批量迁移
for test_file in Path("tests").rglob("test_*.py"):
    migrate_file(test_file)
```

## 📋 迁移检查清单

- [ ] 更新依赖到v2.0+
- [ ] 更新所有导入路径
- [ ] 更新配置类定义（Pydantic v2）
- [ ] 更新Bootstrap初始化代码
- [ ] 迁移扩展到新Hook系统
- [ ] 更新Fixture使用
- [ ] 移除废弃功能
- [ ] 运行测试验证
- [ ] 更新CI/CD配置

## 🆘 常见问题

### Q: v1和v2可以共存吗？
A: 不建议。框架使用相同的包名，建议完整迁移。

### Q: 迁移需要多长时间？
A: 小型项目（<100个测试）约1-2小时，大型项目建议分批迁移。

### Q: 性能会有提升吗？
A: 是的，v2使用了更高效的连接池管理和缓存策略。

### Q: 遇到问题怎么办？
A: 查看[问题归档](../archive/issues/summary.md)或提交Issue。

## 🔗 相关资源

- [v2.0架构详解](../architecture/v2-architecture.md)
- [API参考](../api-reference/README.md)
- [示例代码](../../examples/)
- [扩展点设计](../architecture/extension-points.md)
- [快速上手指南](../getting-started/quickstart.md)

---

**返回**: [文档首页](../README.md)
