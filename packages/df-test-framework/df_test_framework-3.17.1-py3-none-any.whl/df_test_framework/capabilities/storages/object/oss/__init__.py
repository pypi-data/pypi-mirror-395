"""阿里云 OSS 对象存储客户端

基于阿里云官方 SDK (oss2) 实现
提供完整的 OSS 功能支持
"""

from .client import OSSClient
from .config import OSSConfig

__all__ = [
    "OSSClient",
    "OSSConfig",
]
