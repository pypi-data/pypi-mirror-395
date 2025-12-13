"""
存储客户端使用示例

演示如何使用DF Test Framework的存储客户端（本地文件、S3、阿里云OSS）。
"""

import tempfile
from pathlib import Path

from df_test_framework import Bootstrap, FrameworkSettings
from df_test_framework.infrastructure.config import StorageConfig
from df_test_framework.storages import LocalFileConfig, OSSConfig, S3Config


class LocalStorageSettings(FrameworkSettings):
    """本地存储示例配置"""

    storage: StorageConfig = StorageConfig(
        local_file=LocalFileConfig(
            base_path=str(Path(tempfile.gettempdir()) / "df-storage-example"),
            auto_create_dirs=True,
            max_file_size=10 * 1024 * 1024,  # 10MB
        )
    )


class S3StorageSettings(FrameworkSettings):
    """S3存储示例配置（MinIO）"""

    storage: StorageConfig = StorageConfig(
        s3=S3Config(
            endpoint_url="http://localhost:9000",  # MinIO本地服务
            access_key="minioadmin",
            secret_key="minioadmin",
            bucket_name="test-bucket",
            region="us-east-1",
        )
    )


class OSSStorageSettings(FrameworkSettings):
    """阿里云OSS存储示例配置"""

    storage: StorageConfig = StorageConfig(
        oss=OSSConfig(
            access_key_id="LTAI5t...",  # 替换为实际的 AccessKey ID
            access_key_secret="xxx...",  # 替换为实际的 AccessKey Secret
            bucket_name="my-test-bucket",
            endpoint="oss-cn-hangzhou.aliyuncs.com",
        )
    )


def example_local_file_basic():
    """示例1: 本地文件存储基础操作"""
    print("\n" + "=" * 60)
    print("示例1: 本地文件存储 - 基础操作")
    print("=" * 60)

    # 初始化框架
    app = Bootstrap().with_settings(LocalStorageSettings).build()
    runtime = app.run()
    storage = runtime.local_file()

    # 1. 上传文件
    test_content = b"Hello, DF Test Framework!"
    result = storage.upload("test.txt", test_content)
    print(f"✅ 文件已上传: {result['path']}")
    print(f"   文件大小: {result['size']} bytes")

    # 2. 下载文件
    content = storage.download("test.txt")
    print(f"✅ 文件已下载: {content.decode('utf-8')}")

    # 3. 检查文件是否存在
    exists = storage.exists("test.txt")
    print(f"✅ 文件存在性检查: {exists}")

    # 4. 获取文件信息
    info = storage.get_file_info("test.txt")
    print(f"✅ 文件信息: 大小={info['size']} bytes, 最后修改={info['modified_at']}")

    # 5. 列出文件
    files = storage.list_files()
    print(f"✅ 文件列表: {files}")

    # 6. 删除文件
    storage.delete("test.txt")
    print("✅ 文件已删除")

    # 清理
    runtime.close()


def example_local_file_advanced():
    """示例2: 本地文件存储高级操作"""
    print("\n" + "=" * 60)
    print("示例2: 本地文件存储 - 高级操作")
    print("=" * 60)

    app = Bootstrap().with_settings(LocalStorageSettings).build()
    runtime = app.run()
    storage = runtime.local_file()

    # 1. 上传带元数据的文件
    metadata = {"author": "张三", "category": "测试"}
    result = storage.upload("doc.txt", b"Document content", metadata=metadata)
    print(f"✅ 文件已上传（带元数据）: {result['path']}")
    print(f"   元数据: {result.get('metadata', {})}")

    # 2. 复制文件
    storage.copy("doc.txt", "doc-copy.txt")
    print("✅ 文件已复制: doc.txt -> doc-copy.txt")

    # 3. 移动文件
    storage.move("doc-copy.txt", "archive/doc.txt")
    print("✅ 文件已移动: doc-copy.txt -> archive/doc.txt")

    # 4. 列出特定目录的文件
    archive_files = storage.list_files(directory="archive")
    print(f"✅ archive/ 目录下的文件: {archive_files}")

    # 5. 批量清理
    storage.clear(directory="archive")
    print("✅ archive/ 目录已清空")

    # 清理
    storage.clear()
    runtime.close()


def example_s3_config():
    """示例3: S3存储配置示例（MinIO）"""
    print("\n" + "=" * 60)
    print("示例3: S3存储配置（需要MinIO服务）")
    print("=" * 60)

    print("""
⚠️ 此示例需要运行MinIO服务，启动命令:
docker run -p 9000:9000 -p 9001:9001 \\
  -e MINIO_ROOT_USER=minioadmin \\
  -e MINIO_ROOT_PASSWORD=minioadmin \\
  minio/minio server /data --console-address ":9001"

配置示例:
""")

    print("""
from df_test_framework import FrameworkSettings
from df_test_framework.storages import S3Config

class MySettings(FrameworkSettings):
    storage: StorageConfig = StorageConfig(
        s3=S3Config(
            endpoint_url="http://localhost:9000",
            access_key="minioadmin",
            secret_key="minioadmin",
            bucket_name="test-bucket",
            region="us-east-1",
        )
    )

# 使用
runtime = Bootstrap().with_settings(MySettings).build().run()
s3 = runtime.s3()

# 上传文件
s3.upload("test.txt", b"Hello S3")

# 下载文件
content = s3.download("test.txt")

# 生成预签名URL（5分钟有效）
url = s3.generate_presigned_url("test.txt", expiration=300)
    """)


def example_oss_config():
    """示例4: 阿里云OSS存储配置示例"""
    print("\n" + "=" * 60)
    print("示例4: 阿里云OSS存储配置")
    print("=" * 60)

    print("""
⚠️ 此示例需要阿里云OSS账号和Bucket

配置示例 - 基础配置:
""")

    print("""
from df_test_framework import FrameworkSettings
from df_test_framework.storages import OSSConfig

class MySettings(FrameworkSettings):
    storage: StorageConfig = StorageConfig(
        oss=OSSConfig(
            access_key_id="LTAI5t...",        # 替换为实际值
            access_key_secret="xxx...",       # 替换为实际值
            bucket_name="my-bucket",
            endpoint="oss-cn-hangzhou.aliyuncs.com"
        )
    )

# 使用
runtime = Bootstrap().with_settings(MySettings).build().run()
oss = runtime.oss()

# 上传文件
oss.upload("test.txt", b"Hello OSS")

# 下载文件
content = oss.download("test.txt")

# 生成预签名URL（5分钟有效）
url = oss.generate_presigned_url("test.txt", expiration=300)
    """)

    print("\n配置示例 - 高级配置（内网访问+CRC校验）:")
    print("""
oss=OSSConfig(
    access_key_id="LTAI5t...",
    access_key_secret="xxx...",
    bucket_name="my-bucket",
    endpoint="oss-cn-hangzhou-internal.aliyuncs.com",  # 内网Endpoint
    enable_crc=True,              # 启用CRC64校验
    part_size=10 * 1024 * 1024,  # 分片大小10MB
    connect_timeout=60,           # 连接超时60秒
)
    """)

    print("\n配置示例 - STS临时凭证:")
    print("""
oss=OSSConfig(
    access_key_id="STS.xxx...",
    access_key_secret="xxx...",
    security_token="CAISxxx...",  # STS Token
    bucket_name="my-bucket",
    endpoint="oss-cn-hangzhou.aliyuncs.com"
)
    """)


def example_oss_common_regions():
    """示例5: 阿里云OSS常用区域Endpoint"""
    print("\n" + "=" * 60)
    print("示例5: 阿里云OSS常用区域Endpoint")
    print("=" * 60)

    regions = {
        "华东1（杭州）": {
            "公网": "oss-cn-hangzhou.aliyuncs.com",
            "内网（ECS）": "oss-cn-hangzhou-internal.aliyuncs.com",
        },
        "华北2（北京）": {
            "公网": "oss-cn-beijing.aliyuncs.com",
            "内网（ECS）": "oss-cn-beijing-internal.aliyuncs.com",
        },
        "华东2（上海）": {
            "公网": "oss-cn-shanghai.aliyuncs.com",
            "内网（ECS）": "oss-cn-shanghai-internal.aliyuncs.com",
        },
        "华南1（深圳）": {
            "公网": "oss-cn-shenzhen.aliyuncs.com",
            "内网（ECS）": "oss-cn-shenzhen-internal.aliyuncs.com",
        },
    }

    for region, endpoints in regions.items():
        print(f"\n{region}:")
        print(f"  公网访问: {endpoints['公网']}")
        print(f"  内网访问: {endpoints['内网（ECS）']}")

    print("\n💡 最佳实践:")
    print("  - 在阿里云ECS上运行测试时，使用内网Endpoint可节省流量费用")
    print("  - 内网访问速度更快，延迟更低")
    print("  - 生产环境推荐使用STS临时凭证提高安全性")


def example_storage_best_practices():
    """示例6: 存储使用最佳实践"""
    print("\n" + "=" * 60)
    print("示例6: 存储使用最佳实践")
    print("=" * 60)

    print("""
1. 选择合适的存储类型
   - 本地文件: 适用于单机测试、小文件、临时文件
   - S3: 适用于AWS环境、需要S3兼容性（如MinIO）
   - OSS: 适用于阿里云环境、生产环境推荐

2. 安全性
   - 生产环境使用STS临时凭证，不要硬编码AccessKey
   - 使用环境变量或密钥管理服务存储敏感信息
   - 定期轮换访问密钥

3. 性能优化
   - 大文件（>5MB）自动使用分片上传
   - ECS环境使用内网Endpoint（OSS）
   - 启用CRC64校验确保数据完整性

4. 成本优化
   - 测试后及时清理临时文件
   - 使用合适的存储类型（标准/低频/归档）
   - 设置生命周期规则自动清理过期数据

5. 错误处理
   - 使用 missing_ok=True 避免删除不存在文件时报错
   - 捕获并处理网络异常
   - 实现重试机制处理临时故障
    """)


if __name__ == "__main__":
    print("\n" + "🚀 存储客户端使用示例")
    print("=" * 60)

    # 运行本地文件存储示例（实际执行）
    example_local_file_basic()
    example_local_file_advanced()

    # 运行配置示例（仅展示配置）
    example_s3_config()
    example_oss_config()
    example_oss_common_regions()
    example_storage_best_practices()

    print("\n" + "=" * 60)
    print("✅ 所有示例执行完成!")
    print("=" * 60)
