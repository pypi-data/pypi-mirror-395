"""S3 兼容对象存储客户端

支持所有兼容 S3 协议的对象存储服务:
- AWS S3
- MinIO (开源对象存储)
- 阿里云 OSS
- 腾讯云 COS
- 华为云 OBS
"""

from .client import S3Client
from .config import S3Config

__all__ = [
    "S3Client",
    "S3Config",
]
