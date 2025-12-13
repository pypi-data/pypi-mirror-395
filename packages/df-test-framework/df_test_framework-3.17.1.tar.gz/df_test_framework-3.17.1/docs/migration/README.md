# 迁移指南

本文档是主迁移指南的快速链接。完整的迁移文档请参考：

## 📖 详细迁移指南

**[从v1.x迁移到v2.0](from-v1-to-v2.md)**

该文档包含：
- 主要变更概述
- 详细迁移步骤
- API对照表
- 完整示例对比
- 自动化迁移工具
- 常见问题解答

## ⚡ 快速参考

### 1. 更新导入

```python
# v1.x
from df_test_framework.infrastructure.bootstrap.bootstrap import Bootstrap
from df_test_framework.core.http.http_client import HttpClient

# v2.0
from df_test_framework import Bootstrap, HttpClient
```

### 2. 更新Bootstrap

```python
# v1.x
bootstrap = Bootstrap(settings=MySettings())
runtime = bootstrap.initialize()

# v2.0
app = Bootstrap().with_settings(MySettings).build()
runtime = app.run()
```

### 3. 更新配置

```python
# v1.x
class MySettings(FrameworkSettings):
    class Config:
        env_prefix = "APP_"

# v2.0
class MySettings(FrameworkSettings):
    model_config = {"env_prefix": "APP_"}
```

### 4. 更新扩展

```python
# v1.x
from df_test_framework.monitoring import register_monitor

@register_monitor
class MyMonitor:
    pass

# v2.0
from df_test_framework.extensions import hookimpl

class MyExtension:
    @hookimpl
    def before_http_request(self, request):
        pass
```

## 🔗 相关资源

- [完整迁移指南](from-v1-to-v2.md)
- [v2.0更新日志](../../CHANGELOG.md#200---2025-10-31)
- [v2.0架构概览](../architecture/overview.md)
- [快速入门](../getting-started/quickstart.md)

## 🆘 获取帮助

如果在迁移过程中遇到问题：

1. 查看[完整迁移指南](docs/migration/from-v1-to-v2.md)的常见问题部分
2. 查看[示例代码](examples/)了解正确用法
3. 提交[GitHub Issue](https://github.com/yourorg/test-framework/issues)

---

**返回**: [README](README.md) | [文档首页](docs/README.md)
