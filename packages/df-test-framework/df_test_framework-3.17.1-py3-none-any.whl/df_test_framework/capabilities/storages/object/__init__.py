"""对象存储客户端

支持多种对象存储服务:
- AWS S3 (s3/)
- 阿里云 OSS (oss/)
- MinIO (兼容 S3 协议，可使用 s3/)
"""

from .oss import OSSClient, OSSConfig
from .s3 import S3Client, S3Config

__all__ = [
    # AWS S3
    "S3Client",
    "S3Config",
    # 阿里云 OSS
    "OSSClient",
    "OSSConfig",
]
