# 存储客户端使用指南

> DF Test Framework v3.10.0+ 存储能力

本指南介绍如何使用 DF Test Framework 的存储客户端功能，支持本地文件系统、AWS S3 和阿里云 OSS。

## 目录

- [概述](#概述)
- [本地文件系统](#本地文件系统)
- [AWS S3 对象存储](#aws-s3-对象存储)
- [阿里云 OSS 对象存储](#阿里云-oss-对象存储)
- [集成到测试](#集成到测试)
- [高级用法](#高级用法)
- [最佳实践](#最佳实践)

---

## 概述

DF Test Framework 提供了统一的存储客户端接口，支持：

- **本地文件系统** (`LocalFileClient`): 用于本地文件上传、下载、管理
- **AWS S3 对象存储** (`S3Client`): 支持 AWS S3、MinIO 等兼容 S3 协议的对象存储（基于 boto3）
- **阿里云 OSS 对象存储** (`OSSClient`): 专为阿里云 OSS 优化，使用官方 oss2 SDK

**核心特性:**

- 零配置启动（本地文件系统）
- 统一的 API 接口
- 各存储服务使用最优 SDK
- 自动路径安全检查
- 文件大小和扩展名验证
- pytest fixtures 开箱即用
- 依赖注入集成

---

## 本地文件系统

### 基本配置

```python
from df_test_framework.storages.file import LocalFileClient, LocalFileConfig

# 默认配置（./test-data 目录）
config = LocalFileConfig()
client = LocalFileClient(config)

# 自定义配置
config = LocalFileConfig(
    base_path="/tmp/my-test-data",      # 基础路径
    auto_create_dirs=True,              # 自动创建目录
    allow_overwrite=True,               # 允许覆盖文件
    max_file_size=100 * 1024 * 1024,    # 最大文件大小 (100MB)
    allowed_extensions=[".txt", ".json", ".csv"]  # 允许的扩展名
)
client = LocalFileClient(config)
```

### 基本操作

#### 上传文件

```python
# 上传字节内容
result = client.upload("test.txt", b"Hello World")
print(result)
# {'path': 'test.txt', 'size': 11, 'metadata': None, 'created_at': ..., 'modified_at': ...}

# 上传文件对象
from io import BytesIO

file_obj = BytesIO(b"File content")
result = client.upload("data/file.csv", file_obj)

# 带元数据上传（元数据仅存储在内存中，不持久化）
metadata = {"author": "test_user", "version": "1.0"}
result = client.upload("report.json", content, metadata=metadata)
```

#### 下载文件

```python
# 下载文件
content = client.download("test.txt")
print(content)  # b'Hello World'

# 检查文件是否存在
if client.exists("test.txt"):
    content = client.download("test.txt")
```

#### 列出文件

```python
# 列出所有文件（非递归）
files = client.list_files()
print(files)  # ['file1.txt', 'file2.txt']

# 递归列出所有文件
files = client.list_files(recursive=True)
print(files)  # ['file1.txt', 'file2.txt', 'subdir/file3.txt']

# 模式匹配
txt_files = client.list_files(pattern="*.txt")
json_files = client.list_files(directory="data", pattern="*.json")
```

#### 文件操作

```python
# 获取文件信息
info = client.get_file_info("test.txt")
print(info)
# {
#   'path': 'test.txt',
#   'size': 1024,
#   'created_at': 1234567890.0,
#   'modified_at': 1234567890.0,
#   'metadata': {},
#   'is_file': True,
#   'is_dir': False
# }

# 复制文件
result = client.copy("source.txt", "backup/source.txt")

# 移动文件
result = client.move("old.txt", "new.txt")

# 删除文件
client.delete("test.txt")

# 清空目录
count = client.clear()  # 清空所有文件
count = client.clear(directory="tmp")  # 清空指定目录
```

### 安全特性

```python
# 路径遍历攻击防护
try:
    client.upload("../../../etc/passwd", b"hack")
except ValidationError as e:
    print(f"安全检查失败: {e}")

# 文件大小限制
config = LocalFileConfig(max_file_size=1024)  # 1KB 限制
client = LocalFileClient(config)

try:
    client.upload("large.bin", b"x" * 2048)
except ValidationError as e:
    print(f"文件过大: {e}")

# 扩展名白名单
config = LocalFileConfig(allowed_extensions=[".txt", ".json"])
client = LocalFileClient(config)

try:
    client.upload("malware.exe", b"...")
except ValidationError as e:
    print(f"扩展名不允许: {e}")
```

---

## AWS S3 对象存储

### 安装依赖

S3 客户端需要 boto3 库:

```bash
# 使用 uv
uv pip install boto3

# 或使用 pip
pip install boto3

# 或安装完整存储支持
pip install df-test-framework[storage-all]
```

### 基本配置

```python
from df_test_framework.storages.object import S3Client, S3Config

# AWS S3 配置
config = S3Config(
    endpoint_url="https://s3.amazonaws.com",  # AWS S3 可省略
    access_key="YOUR_ACCESS_KEY",
    secret_key="YOUR_SECRET_KEY",
    bucket_name="my-test-bucket",
    region="us-west-2"
)
client = S3Client(config)

# MinIO 配置（本地开发/测试）
config = S3Config(
    endpoint_url="http://localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    bucket_name="test-bucket",
    use_ssl=False,
    verify_ssl=False
)
client = S3Client(config)
```

### 基本操作

#### 上传对象

```python
# 上传字节内容
result = client.upload("test.txt", b"Hello S3")
print(result)
# {'key': 'test.txt', 'bucket': 'my-bucket', 'size': 8}

# 上传文件对象
from io import BytesIO

file_obj = BytesIO(b"File content")
result = client.upload("data/file.csv", file_obj)

# 带元数据和内容类型
metadata = {"author": "test", "version": "1.0"}
result = client.upload(
    "report.json",
    b'{"data": []}',
    metadata=metadata,
    content_type="application/json"
)
```

#### 下载对象

```python
# 下载对象
content = client.download("test.txt")
print(content)  # b'Hello S3'

# 检查对象是否存在
if client.exists("test.txt"):
    content = client.download("test.txt")
```

#### 列出对象

```python
# 列出所有对象
objects = client.list_objects()
for obj in objects:
    print(f"{obj['key']}: {obj['size']} bytes")

# 按前缀过滤
objects = client.list_objects(prefix="data/")

# 限制返回数量
objects = client.list_objects(max_keys=10)
```

#### 对象操作

```python
# 获取对象信息
info = client.get_object_info("test.txt")
print(info)
# {
#   'key': 'test.txt',
#   'size': 1024,
#   'content_type': 'text/plain',
#   'last_modified': datetime(...),
#   'etag': '...',
#   'metadata': {'author': 'test'}
# }

# 复制对象
result = client.copy("source.txt", "backup/source.txt")

# 跨 bucket 复制
result = client.copy("source.txt", "dest.txt", src_bucket="other-bucket")

# 删除对象
client.delete("test.txt")

# 清空 bucket 或前缀
count = client.clear(prefix="tmp/")  # 清空 tmp/ 下所有对象
```

### 高级功能

#### 预签名 URL

```python
# 生成预签名 GET URL（有效期 5 分钟）
url = client.generate_presigned_url("test.txt", expiration=300)
print(f"下载链接: {url}")

# 生成预签名 PUT URL（用于直接上传）
url = client.generate_presigned_url(
    "upload.txt",
    expiration=600,
    http_method="PUT"
)
print(f"上传链接: {url}")
```

#### 大文件上传

S3Client 自动处理分片上传:

```python
# 配置分片上传
config = S3Config(
    # ... 其他配置 ...
    multipart_threshold=8 * 1024 * 1024,  # 8MB 阈值
    multipart_chunksize=8 * 1024 * 1024,  # 8MB 分片大小
    max_concurrency=10                    # 最大并发数
)

client = S3Client(config)

# 上传大文件（自动分片）
with open("large_file.bin", "rb") as f:
    client.upload("large_file.bin", f)
```

---

## 阿里云 OSS 对象存储

### 安装依赖

OSS 客户端需要阿里云官方 SDK oss2:

```bash
# 使用 uv
uv pip install oss2

# 或使用 pip
pip install oss2

# 或安装完整存储支持
pip install df-test-framework[storage-all]
```

### 基本配置

```python
from df_test_framework.storages.object import OSSClient, OSSConfig

# 基本配置（公网访问）
config = OSSConfig(
    access_key_id="LTAI5t...",           # AccessKey ID
    access_key_secret="xxx...",          # AccessKey Secret
    bucket_name="my-bucket",             # Bucket 名称
    endpoint="oss-cn-hangzhou.aliyuncs.com"  # Endpoint
)
client = OSSClient(config)

# 内网访问配置（ECS 内网免流量费）
config = OSSConfig(
    access_key_id="LTAI5t...",
    access_key_secret="xxx...",
    bucket_name="my-bucket",
    endpoint="oss-cn-hangzhou-internal.aliyuncs.com"  # 内网 Endpoint
)
client = OSSClient(config)

# STS 临时凭证配置
config = OSSConfig(
    access_key_id="STS.xxx",
    access_key_secret="xxx...",
    security_token="CAI...",             # STS Token
    bucket_name="my-bucket",
    endpoint="oss-cn-shanghai.aliyuncs.com"
)
client = OSSClient(config)
```

**常用区域 Endpoint:**

| 区域 | Endpoint（公网） | Endpoint（内网） |
|------|-----------------|-----------------|
| 华东1（杭州） | `oss-cn-hangzhou.aliyuncs.com` | `oss-cn-hangzhou-internal.aliyuncs.com` |
| 华东2（上海） | `oss-cn-shanghai.aliyuncs.com` | `oss-cn-shanghai-internal.aliyuncs.com` |
| 华北2（北京） | `oss-cn-beijing.aliyuncs.com` | `oss-cn-beijing-internal.aliyuncs.com` |
| 华南1（深圳） | `oss-cn-shenzhen.aliyuncs.com` | `oss-cn-shenzhen-internal.aliyuncs.com` |
| 华南2（广州） | `oss-cn-guangzhou.aliyuncs.com` | `oss-cn-guangzhou-internal.aliyuncs.com` |
| 西南1（成都） | `oss-cn-chengdu.aliyuncs.com` | `oss-cn-chengdu-internal.aliyuncs.com` |
| 中国香港 | `oss-cn-hongkong.aliyuncs.com` | `oss-cn-hongkong-internal.aliyuncs.com` |

### 基本操作

#### 上传对象

```python
# 上传字节内容
result = client.upload("test.txt", b"Hello OSS")
print(result)
# {'key': 'test.txt', 'bucket': 'my-bucket', 'etag': '...', 'request_id': '...'}

# 上传文件
from pathlib import Path

result = client.upload("data/report.pdf", Path("/path/to/report.pdf"))

# 上传文件对象
from io import BytesIO

file_obj = BytesIO(b"File content")
result = client.upload("data/file.csv", file_obj)

# 带元数据和内容类型
metadata = {"author": "test", "version": "1.0"}
result = client.upload(
    "report.json",
    b'{"data": []}',
    metadata=metadata,
    content_type="application/json"
)
```

#### 下载对象

```python
# 下载到内存
content = client.download("test.txt")
print(content)  # b'Hello OSS'

# 下载到文件
client.download_to_file("test.txt", "/tmp/test.txt")

# 检查对象是否存在
if client.exists("test.txt"):
    content = client.download("test.txt")
```

#### 列出对象

```python
# 列出所有对象
objects = client.list_objects()
for obj in objects:
    print(f"{obj['key']}: {obj['size']} bytes")

# 按前缀过滤
objects = client.list_objects(prefix="data/")

# 限制返回数量
objects = client.list_objects(max_keys=10)
```

#### 对象操作

```python
# 获取对象信息
info = client.get_object_info("test.txt")
print(info)
# {
#   'key': 'test.txt',
#   'size': 1024,
#   'content_type': 'text/plain',
#   'last_modified': ...,
#   'etag': '...',
#   'metadata': {'author': 'test'}
# }

# 复制对象
result = client.copy("source.txt", "backup/source.txt")

# 删除对象
client.delete("test.txt")

# 删除不存在的对象（不报错）
client.delete("nonexistent.txt", missing_ok=True)

# 批量删除（清空前缀）
count = client.clear(prefix="tmp/")  # 清空 tmp/ 下所有对象
print(f"已删除 {count} 个对象")
```

### 高级功能

#### 生成预签名 URL

```python
# 生成下载链接（1小时有效）
url = client.generate_presigned_url("test.txt", expiration=3600)
print(url)  # https://my-bucket.oss-cn-hangzhou.aliyuncs.com/test.txt?signature=...

# 生成上传链接
url = client.generate_presigned_url("upload.txt", expiration=600, method="PUT")
```

#### 大文件上传

```python
# 大文件自动使用分片上传
from pathlib import Path

# 超过 multipart_threshold (默认 10MB) 自动分片
result = client.upload("large_file.bin", Path("/path/to/large_file.bin"))
```

#### CRC64 校验

```python
# 默认启用 CRC64 校验
config = OSSConfig(
    access_key_id="LTAI5t...",
    access_key_secret="xxx...",
    bucket_name="my-bucket",
    endpoint="oss-cn-hangzhou.aliyuncs.com",
    enable_crc=True  # 默认值
)
client = OSSClient(config)

# 上传和下载时自动进行 CRC64 校验
```

### 最佳实践

#### 1. 使用内网 Endpoint（ECS 内网免流量费）

如果你的应用运行在阿里云 ECS 上，强烈推荐使用内网 Endpoint:

```python
config = OSSConfig(
    access_key_id="LTAI5t...",
    access_key_secret="xxx...",
    bucket_name="my-bucket",
    endpoint="oss-cn-hangzhou-internal.aliyuncs.com"  # 内网 Endpoint
)
```

**优势:**
- 流量免费
- 速度更快
- 更安全

#### 2. 使用 STS 临时凭证（推荐）

生产环境推荐使用 STS 临时凭证而非长期密钥:

```python
# 1. 从 STS 获取临时凭证
# 2. 使用临时凭证初始化客户端
config = OSSConfig(
    access_key_id=sts_credentials.access_key_id,
    access_key_secret=sts_credentials.access_key_secret,
    security_token=sts_credentials.security_token,
    bucket_name="my-bucket",
    endpoint="oss-cn-hangzhou.aliyuncs.com"
)
client = OSSClient(config)
```

#### 3. 配置合理的分片大小

根据网络环境调整分片大小:

```python
config = OSSConfig(
    access_key_id="LTAI5t...",
    access_key_secret="xxx...",
    bucket_name="my-bucket",
    endpoint="oss-cn-hangzhou.aliyuncs.com",
    part_size=10 * 1024 * 1024,  # 10MB（默认值）
    multipart_threshold=10 * 1024 * 1024  # 10MB（默认值）
)
```

**建议:**
- 内网环境: 可以使用更大的分片（如 20MB）
- 公网环境: 使用默认值（10MB）或更小（5MB）

#### 4. 启用 CRC64 校验

保持 CRC64 校验开启，确保数据完整性:

```python
config = OSSConfig(
    # ... 其他配置 ...
    enable_crc=True  # 默认开启，强烈建议保持
)
```

---

## 集成到测试

### 使用 pytest Fixtures

DF Test Framework 提供了开箱即用的 pytest fixtures:

```python
# tests/test_storage.py

def test_local_file_upload(local_file_client):
    """测试本地文件上传"""
    # local_file_client 是自动注入的 LocalFileClient 实例
    result = local_file_client.upload("test.txt", b"Test Data")

    assert result["size"] == 9
    assert local_file_client.exists("test.txt")

    # 清理
    local_file_client.delete("test.txt")


def test_s3_upload(s3_client):
    """测试 S3 上传"""
    # s3_client 是自动注入的 S3Client 实例
    result = s3_client.upload("test.txt", b"S3 Test Data")

    assert result["size"] == 12
    assert s3_client.exists("test.txt")

    # 清理
    s3_client.delete("test.txt")
```

### 配置存储客户端

在项目配置中启用存储客户端:

```python
# conftest.py 或 settings.py

from df_test_framework import FrameworkSettings
from df_test_framework.storages import LocalFileConfig, S3Config, StorageConfig

class MySettings(FrameworkSettings):
    storage: StorageConfig = StorageConfig(
        # 本地文件配置
        local_file=LocalFileConfig(
            base_path="./test-data",
            auto_create_dirs=True,
            max_file_size=50 * 1024 * 1024
        ),

        # S3 配置（可选，仅在需要时配置）
        s3=S3Config(
            endpoint_url="http://localhost:9000",
            access_key="minioadmin",
            secret_key="minioadmin",
            bucket_name="test-bucket"
        )
    )
```

### 使用环境变量

支持通过环境变量配置:

```bash
# 本地文件配置
export APP_STORAGE__LOCAL_FILE__BASE_PATH="/tmp/test-data"
export APP_STORAGE__LOCAL_FILE__MAX_FILE_SIZE=104857600

# S3 配置
export APP_STORAGE__S3__ENDPOINT_URL="http://localhost:9000"
export APP_STORAGE__S3__ACCESS_KEY="minioadmin"
export APP_STORAGE__S3__SECRET_KEY="minioadmin"
export APP_STORAGE__S3__BUCKET_NAME="test-bucket"
```

### 临时配置覆盖

在测试中临时修改配置:

```python
def test_with_custom_config(runtime):
    """测试时临时修改配置"""
    # 创建带有自定义配置的运行时上下文
    custom_runtime = runtime.with_overrides({
        "storage": {
            "local_file": {
                "base_path": "/tmp/custom-test-data"
            }
        }
    })

    client = custom_runtime.local_file()
    client.upload("test.txt", b"Custom Config Test")
```

---

## 高级用法

### 依赖注入集成

存储客户端通过 Provider 模式集成到框架:

```python
from df_test_framework.infrastructure import RuntimeContext

# 获取运行时上下文
runtime: RuntimeContext = ...

# 获取客户端
local_file_client = runtime.local_file()
s3_client = runtime.s3()
```

### 自定义 Provider

扩展存储 Provider:

```python
from df_test_framework.infrastructure.providers import SingletonProvider
from df_test_framework.storages import LocalFileClient, LocalFileConfig

def custom_local_file_factory(context):
    """自定义本地文件客户端工厂"""
    config = LocalFileConfig(
        base_path="/custom/path",
        allowed_extensions=[".txt", ".json", ".xml"]
    )
    return LocalFileClient(config)

# 注册自定义 Provider
providers.register("local_file", SingletonProvider(custom_local_file_factory))
```

### 多实例管理

同时使用多个存储客户端:

```python
# 创建多个配置
config_temp = LocalFileConfig(base_path="/tmp/temp-files")
config_backup = LocalFileConfig(base_path="/backup/files")

temp_client = LocalFileClient(config_temp)
backup_client = LocalFileClient(config_backup)

# 使用不同的客户端
temp_client.upload("temp.txt", b"Temporary")
backup_client.upload("backup.txt", b"Backup Data")
```

### 条件化存储

根据环境选择存储后端:

```python
import os
from df_test_framework.storages import LocalFileClient, S3Client

def get_storage_client():
    """根据环境获取存储客户端"""
    if os.getenv("ENV") == "prod":
        # 生产环境使用 S3
        config = S3Config(
            access_key=os.getenv("AWS_ACCESS_KEY"),
            secret_key=os.getenv("AWS_SECRET_KEY"),
            bucket_name="prod-bucket"
        )
        return S3Client(config)
    else:
        # 开发/测试环境使用本地文件
        config = LocalFileConfig(base_path="./test-data")
        return LocalFileClient(config)

# 在测试中使用
def test_storage(runtime):
    client = get_storage_client()
    client.upload("test.txt", b"Data")
```

---

## 最佳实践

### 1. 测试数据清理

始终在测试后清理数据:

```python
import pytest

@pytest.fixture
def clean_storage(local_file_client):
    """自动清理 fixture"""
    yield local_file_client
    # 测试结束后清理
    local_file_client.clear()


def test_with_cleanup(clean_storage):
    clean_storage.upload("test.txt", b"Data")
    # 测试逻辑...
    # 自动清理（不需要手动删除）
```

### 2. 路径组织

使用明确的路径结构:

```python
# 按测试模块组织
test_module = "test_orders"
client.upload(f"{test_module}/order_001.json", data)

# 按日期组织
from datetime import datetime
date = datetime.now().strftime("%Y%m%d")
client.upload(f"reports/{date}/report.csv", data)

# 按用户组织
user_id = "user123"
client.upload(f"users/{user_id}/profile.json", data)
```

### 3. 错误处理

正确处理存储异常:

```python
from df_test_framework.common.exceptions import ResourceError, ValidationError

def safe_upload(client, key, content):
    """安全上传函数"""
    try:
        return client.upload(key, content)
    except ValidationError as e:
        print(f"验证失败: {e}")
        return None
    except ResourceError as e:
        print(f"资源错误: {e}")
        return None
    except Exception as e:
        print(f"未知错误: {e}")
        raise
```

### 4. 性能优化

批量操作优化:

```python
# ❌ 不推荐：逐个上传
for i in range(100):
    client.upload(f"file_{i}.txt", f"Data {i}".encode())

# ✅ 推荐：使用并发（如果框架支持）
from concurrent.futures import ThreadPoolExecutor

def upload_file(i):
    return client.upload(f"file_{i}.txt", f"Data {i}".encode())

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(upload_file, range(100)))
```

### 5. 配置管理

集中管理配置:

```python
# config/storage.py

from df_test_framework.storages import LocalFileConfig, S3Config

class StorageSettings:
    """存储配置类"""

    LOCAL_FILE = LocalFileConfig(
        base_path="./test-data",
        max_file_size=100 * 1024 * 1024,
        allowed_extensions=[".txt", ".json", ".csv", ".xml"]
    )

    S3_DEV = S3Config(
        endpoint_url="http://localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        bucket_name="dev-bucket"
    )

    S3_PROD = S3Config(
        endpoint_url="https://s3.amazonaws.com",
        access_key=os.getenv("AWS_ACCESS_KEY"),
        secret_key=os.getenv("AWS_SECRET_KEY"),
        bucket_name="prod-bucket",
        region="us-west-2"
    )
```

### 6. 日志记录

启用详细日志以便调试:

```python
from loguru import logger

# 配置日志级别
logger.level("DEBUG")

# 存储客户端会自动记录操作日志
client.upload("test.txt", b"Data")
# 输出: [INFO] 文件上传成功: test.txt (4 bytes)

client.download("test.txt")
# 输出: [DEBUG] 文件下载成功: test.txt (4 bytes)
```

---

## 故障排查

### 常见问题

#### 1. boto3 未安装

```
ConfigurationError: boto3 未安装，无法使用 S3 客户端
请安装: pip install boto3
```

**解决方案:**
```bash
uv pip install boto3
```

#### 2. Bucket 不存在

S3Client 会自动创建 bucket，如果创建失败:

```python
# 检查权限和配置
config = S3Config(...)
client = S3Client(config)  # 自动创建 bucket
```

#### 3. 路径安全检查失败

```
ValidationError: 不安全的文件路径: ../../../etc/passwd (超出基础目录)
```

**解决方案:** 使用相对路径，不要使用 `../`:
```python
# ❌ 错误
client.upload("../sensitive.txt", data)

# ✅ 正确
client.upload("backup/sensitive.txt", data)
```

#### 4. 文件大小超限

```
ValidationError: 文件大小 (200000000 bytes) 超过限制 (100000000 bytes)
```

**解决方案:** 调整配置或分片上传:
```python
config = LocalFileConfig(max_file_size=200 * 1024 * 1024)
```

---

## 参考

### API 文档

- [LocalFileClient API](../api/storages/local_file.md)
- [S3Client API](../api/storages/s3.md)

### 相关指南

- [测试数据管理](./test_data.md)
- [配置管理](./configuration.md)
- [Fixture 使用](./fixtures.md)

### 外部资源

- [boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [MinIO Python Client](https://min.io/docs/minio/linux/developers/python/API.html)
- [AWS S3 Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/best-practices.html)

---

**版本:** v3.10.0
**最后更新:** 2025-11-26
