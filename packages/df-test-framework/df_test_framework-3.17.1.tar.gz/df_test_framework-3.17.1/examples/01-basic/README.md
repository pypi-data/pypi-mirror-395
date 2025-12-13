# 基础功能示例

本目录包含DF Test Framework的基础功能使用示例。

## 📋 示例列表

### 1. HTTP客户端 (`http_client_usage.py`)
演示如何使用HttpClient发送HTTP请求。

**功能展示**:
- GET/POST/PUT/DELETE请求
- 请求头和参数设置
- JSON数据发送
- 响应处理

**运行**:
```bash
python examples/01-basic/http_client_usage.py
```

### 2. 数据库操作 (`database_operations.py`)
演示如何使用Database进行数据库操作。

**功能展示**:
- 执行SQL查询
- 参数化查询
- 事务管理
- ORM操作

**运行**:
```bash
python examples/01-basic/database_operations.py
```

### 3. Redis缓存 (`redis_cache.py`)
演示如何使用RedisClient进行缓存操作。

**功能展示**:
- 键值存储
- 过期时间设置
- 数据序列化
- 常用操作

**运行**:
```bash
python examples/01-basic/redis_cache.py
```

### 4. 存储客户端 (`storage_usage.py`) ⭐ v3.10+
演示如何使用存储客户端进行文件存储操作。

**功能展示**:
- LocalFileClient - 本地文件系统存储
- S3Client - AWS S3 对象存储（支持 MinIO）
- OSSClient - 阿里云 OSS 对象存储
- 文件上传/下载/删除/列表
- 元数据管理
- 预签名URL生成
- 最佳实践指南

**运行**:
```bash
python examples/01-basic/storage_usage.py
```

**配置示例**:
```python
from df_test_framework import FrameworkSettings
from df_test_framework.storages import OSSConfig

class MySettings(FrameworkSettings):
    storage: StorageConfig = StorageConfig(
        oss=OSSConfig(
            access_key_id="LTAI5t...",
            access_key_secret="xxx...",
            bucket_name="my-bucket",
            endpoint="oss-cn-hangzhou.aliyuncs.com"
        )
    )
```

## 🎯 学习路径

1. 先运行HTTP客户端示例了解基础用法
2. 再看数据库操作示例学习数据持久化
3. 学习Redis缓存示例了解缓存策略
4. 最后看存储客户端示例学习文件存储（v3.10+）

## 📚 相关文档

- [用户指南 - 使用示例](../../docs/user-guide/examples.md)
- [存储客户端使用指南](../../docs/guides/storage.md) ⭐
- [API参考](../../docs/api-reference/README.md)

---

**返回**: [示例首页](../README.md)
