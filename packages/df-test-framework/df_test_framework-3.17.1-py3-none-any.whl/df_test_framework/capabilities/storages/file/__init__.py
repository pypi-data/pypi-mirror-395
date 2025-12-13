"""文件系统存储客户端.

提供本地文件系统和网络文件系统的访问能力
"""

from .local import LocalFileClient, LocalFileConfig

__all__ = [
    "LocalFileClient",
    "LocalFileConfig",
]
