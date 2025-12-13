"""文件存储配置

本地文件系统和网络文件系统的配置定义
"""

from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class LocalFileConfig(BaseModel):
    """本地文件系统配置

    Example:
        >>> config = LocalFileConfig(
        ...     base_path="/tmp/test-data",
        ...     auto_create_dirs=True
        ... )
    """

    base_path: str = Field(default="./test-data", description="基础路径（所有操作的根目录）")
    auto_create_dirs: bool = Field(default=True, description="自动创建不存在的目录")
    allow_overwrite: bool = Field(default=True, description="允许覆盖已存在的文件")
    max_file_size: int = Field(
        default=100 * 1024 * 1024,  # 100MB
        description="单个文件最大大小（字节）",
    )
    allowed_extensions: list[str] | None = Field(
        default=None, description="允许的文件扩展名列表（None表示不限制）"
    )

    @field_validator("base_path")
    @classmethod
    def validate_base_path(cls, v: str) -> str:
        """验证基础路径"""
        if not v:
            raise ValueError("base_path cannot be empty")
        return v

    @field_validator("max_file_size")
    @classmethod
    def validate_max_file_size(cls, v: int) -> int:
        """验证文件大小限制"""
        if v <= 0:
            raise ValueError("max_file_size must be positive")
        if v > 1024 * 1024 * 1024:  # 1GB
            raise ValueError("max_file_size cannot exceed 1GB")
        return v

    def get_base_path(self) -> Path:
        """获取 Path 对象"""
        return Path(self.base_path)


__all__ = ["LocalFileConfig"]
