"""文件存储能力层 - Layer 1

提供文件上传/下载/管理能力
按存储类型组织：
- object/: 对象存储（AWS S3、阿里云 OSS、MinIO 等）
- file/: 文件系统（本地文件、NFS、HDFS等）
- blob/: Blob存储（Azure Blob等）
"""

from .file import LocalFileClient, LocalFileConfig
from .object import OSSClient, OSSConfig, S3Client, S3Config

__all__ = [
    # 本地文件系统
    "LocalFileClient",
    "LocalFileConfig",
    # AWS S3 对象存储
    "S3Client",
    "S3Config",
    # 阿里云 OSS 对象存储
    "OSSClient",
    "OSSConfig",
]
