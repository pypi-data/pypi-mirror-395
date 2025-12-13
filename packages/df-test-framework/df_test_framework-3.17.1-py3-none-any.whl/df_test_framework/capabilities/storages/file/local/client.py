"""本地文件系统客户端

提供本地文件的上传、下载、删除、列表等操作
"""

import shutil
from pathlib import Path
from typing import Any, BinaryIO

from loguru import logger

from df_test_framework.core.exceptions import ResourceError, ValidationError

from .config import LocalFileConfig


class LocalFileClient:
    """本地文件系统客户端

    提供本地文件操作的统一接口

    Example:
        >>> config = LocalFileConfig(base_path="/tmp/test-data")
        >>> client = LocalFileClient(config)
        >>>
        >>> # 上传文件
        >>> client.upload("file.txt", b"Hello World")
        >>>
        >>> # 下载文件
        >>> content = client.download("file.txt")
        >>>
        >>> # 删除文件
        >>> client.delete("file.txt")
    """

    def __init__(self, config: LocalFileConfig):
        """初始化客户端

        Args:
            config: 本地文件系统配置

        Raises:
            ValidationError: 基础目录不存在且未启用自动创建
        """
        self.config = config
        self.base_path = config.get_base_path()

        # 检查或创建基础目录
        if not self.base_path.exists():
            if config.auto_create_dirs:
                self.base_path.mkdir(parents=True, exist_ok=True)
            else:
                raise ValidationError(f"基础目录不存在: {self.base_path}")

        logger.info(f"本地文件系统客户端已初始化: {self.base_path}")

    def _get_full_path(self, file_path: str) -> Path:
        """获取完整路径

        Args:
            file_path: 相对路径

        Returns:
            完整路径

        Raises:
            ValidationError: 路径不安全（超出基础目录）
        """
        full_path = (self.base_path / file_path).resolve()

        # 安全检查：确保路径在基础目录内
        try:
            full_path.relative_to(self.base_path.resolve())
        except ValueError as e:
            raise ValidationError(f"不安全的文件路径: {file_path} (超出基础目录)") from e

        return full_path

    def _validate_file_size(self, size: int) -> None:
        """验证文件大小

        Args:
            size: 文件大小（字节）

        Raises:
            ValidationError: 文件大小超过限制
        """
        if size > self.config.max_file_size:
            raise ValidationError(
                f"文件大小 ({size} bytes) 超过限制 ({self.config.max_file_size} bytes)"
            )

    def _validate_extension(self, file_path: str) -> None:
        """验证文件扩展名

        Args:
            file_path: 文件路径

        Raises:
            ValidationError: 文件扩展名不允许
        """
        if self.config.allowed_extensions is None:
            return

        ext = Path(file_path).suffix.lower()
        if ext not in self.config.allowed_extensions:
            raise ValidationError(
                f"文件扩展名 {ext} 不在允许列表中: {self.config.allowed_extensions}"
            )

    def upload(
        self, file_path: str, content: bytes | BinaryIO, metadata: dict | None = None
    ) -> dict:
        """上传文件

        Args:
            file_path: 文件路径（相对于基础目录）
            content: 文件内容（字节或文件对象）
            metadata: 元数据（可选）

        Returns:
            上传结果字典，包含 path, size, metadata, created_at, modified_at

        Raises:
            ValidationError: 文件大小超限、扩展名不允许、覆盖被禁止

        Example:
            >>> client.upload("test.txt", b"Hello")
            {'path': 'test.txt', 'size': 5, 'metadata': None, 'created_at': ..., 'modified_at': ...}
        """
        full_path = self._get_full_path(file_path)

        # 验证扩展名
        self._validate_extension(file_path)

        # 检查文件是否存在
        if full_path.exists() and not self.config.allow_overwrite:
            raise ValidationError(f"文件已存在且不允许覆盖: {file_path}")

        # 获取内容
        if isinstance(content, bytes):
            data = content
        else:
            data = content.read()

        # 验证文件大小
        self._validate_file_size(len(data))

        # 创建父目录
        if self.config.auto_create_dirs:
            full_path.parent.mkdir(parents=True, exist_ok=True)

        # 写入文件
        full_path.write_bytes(data)

        logger.info(f"文件上传成功: {file_path} ({len(data)} bytes)")

        # 获取文件时间戳
        stat = full_path.stat()

        return {
            "path": file_path,
            "size": len(data),
            "metadata": metadata,
            "created_at": stat.st_ctime,
            "modified_at": stat.st_mtime,
        }

    def download(self, file_path: str) -> bytes:
        """下载文件

        Args:
            file_path: 文件路径（相对于基础目录）

        Returns:
            文件内容（字节）

        Raises:
            ResourceError: 文件不存在

        Example:
            >>> content = client.download("test.txt")
        """
        full_path = self._get_full_path(file_path)

        if not full_path.exists():
            raise ResourceError(f"文件不存在: {file_path}")

        if not full_path.is_file():
            raise ResourceError(f"路径不是文件: {file_path}")

        content = full_path.read_bytes()
        logger.debug(f"文件下载成功: {file_path} ({len(content)} bytes)")

        return content

    def delete(self, file_path: str, missing_ok: bool = False) -> bool:
        """删除文件

        Args:
            file_path: 文件路径（相对于基础目录）
            missing_ok: 文件不存在时是否报错（True则忽略）

        Returns:
            是否删除成功

        Raises:
            ResourceError: 文件不存在（missing_ok=False时）

        Example:
            >>> client.delete("test.txt")
            True
        """
        full_path = self._get_full_path(file_path)

        if not full_path.exists():
            if missing_ok:
                logger.debug(f"文件不存在，跳过删除: {file_path}")
                return False
            raise ResourceError(f"文件不存在: {file_path}")

        if full_path.is_file():
            full_path.unlink()
            logger.info(f"文件删除成功: {file_path}")
            return True
        else:
            raise ResourceError(f"路径不是文件: {file_path}")

    def exists(self, file_path: str) -> bool:
        """检查文件是否存在

        Args:
            file_path: 文件路径（相对于基础目录）

        Returns:
            是否存在

        Example:
            >>> client.exists("test.txt")
            True
        """
        full_path = self._get_full_path(file_path)
        return full_path.exists() and full_path.is_file()

    def list_files(
        self, directory: str = "", pattern: str = "*", recursive: bool = False
    ) -> list[str]:
        """列出文件

        Args:
            directory: 目录路径（相对于基础目录，空字符串表示基础目录）
            pattern: 文件名模式（支持通配符）
            recursive: 是否递归列出子目录

        Returns:
            文件路径列表（相对于基础目录）

        Example:
            >>> client.list_files(pattern="*.txt")
            ['file1.txt', 'file2.txt']
        """
        dir_path = self._get_full_path(directory)

        if not dir_path.exists():
            return []

        if not dir_path.is_dir():
            raise ResourceError(f"路径不是目录: {directory}")

        # 解析真实路径以处理符号链接（特别是 macOS 的 /var -> /private/var）
        resolved_base = self.base_path.resolve()
        resolved_dir = dir_path.resolve()

        # 使用 glob 或 rglob
        glob_func = resolved_dir.rglob if recursive else resolved_dir.glob
        files = [
            str(p.resolve().relative_to(resolved_base)).replace("\\", "/")  # 统一使用正斜杠
            for p in glob_func(pattern)
            if p.is_file()
        ]

        return sorted(files)

    def get_file_info(self, file_path: str) -> dict:
        """获取文件信息

        Args:
            file_path: 文件路径（相对于基础目录）

        Returns:
            文件信息字典（size, created_at, modified_at, metadata）

        Raises:
            ResourceError: 文件不存在

        Example:
            >>> info = client.get_file_info("test.txt")
            >>> info['size']
            1024
        """
        full_path = self._get_full_path(file_path)

        if not full_path.exists():
            raise ResourceError(f"文件不存在: {file_path}")

        stat = full_path.stat()

        # 尝试读取元数据（如果存在）
        # 注意：本地文件系统不原生支持元数据，这里返回空字典
        # 如果需要持久化元数据，可以考虑使用扩展属性或额外的元数据文件
        metadata: dict[str, Any] = {}

        return {
            "path": file_path,
            "size": stat.st_size,
            "created_at": stat.st_ctime,
            "modified_at": stat.st_mtime,
            "metadata": metadata,
            "is_file": full_path.is_file(),
            "is_dir": full_path.is_dir(),
        }

    def copy(self, src_path: str, dest_path: str, overwrite: bool = True) -> dict:
        """复制文件

        Args:
            src_path: 源文件路径
            dest_path: 目标文件路径
            overwrite: 是否覆盖已存在的文件

        Returns:
            复制结果字典

        Raises:
            ResourceError: 源文件不存在
            ValidationError: 目标文件已存在且不允许覆盖

        Example:
            >>> client.copy("source.txt", "dest.txt")
        """
        src_full = self._get_full_path(src_path)
        dest_full = self._get_full_path(dest_path)

        if not src_full.exists():
            raise ResourceError(f"源文件不存在: {src_path}")

        if dest_full.exists() and not overwrite:
            raise ValidationError(f"目标文件已存在: {dest_path}")

        # 创建目标目录
        if self.config.auto_create_dirs:
            dest_full.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(src_full, dest_full)

        logger.info(f"文件复制成功: {src_path} -> {dest_path}")

        return self.get_file_info(dest_path)

    def move(self, src_path: str, dest_path: str, overwrite: bool = True) -> dict:
        """移动文件

        Args:
            src_path: 源文件路径
            dest_path: 目标文件路径
            overwrite: 是否覆盖已存在的文件

        Returns:
            移动结果字典

        Raises:
            ResourceError: 源文件不存在、目标文件已存在且不允许覆盖

        Example:
            >>> client.move("old.txt", "new.txt")
        """
        src_full = self._get_full_path(src_path)
        dest_full = self._get_full_path(dest_path)

        if not src_full.exists():
            raise ResourceError(f"源文件不存在: {src_path}")

        if dest_full.exists() and not overwrite:
            raise ResourceError(f"目标文件已存在: {dest_path}")

        # 创建目标目录
        if self.config.auto_create_dirs:
            dest_full.parent.mkdir(parents=True, exist_ok=True)

        shutil.move(str(src_full), str(dest_full))

        logger.info(f"文件移动成功: {src_path} -> {dest_path}")

        return self.get_file_info(dest_path)

    def clear(self, directory: str = "") -> int:
        """清空目录（删除所有文件和子目录）

        Args:
            directory: 目录路径（空字符串表示基础目录）

        Returns:
            删除的项目数量（文件+目录）

        Example:
            >>> count = client.clear()
            >>> print(f"删除了 {count} 个项目")
        """
        dir_path = self._get_full_path(directory)

        if not dir_path.exists():
            return 0

        count = 0
        # 先收集所有要删除的项目
        items_to_delete = list(dir_path.iterdir())

        for item in items_to_delete:
            if item.is_file():
                item.unlink()
                count += 1
            elif item.is_dir():
                # 递归计数目录中的所有文件
                count += len([f for f in item.rglob("*") if f.is_file()])
                shutil.rmtree(item)

        logger.info(f"目录清空完成: {directory} ({count} 个项目)")

        return count

    def close(self) -> None:
        """关闭客户端（清理资源）"""
        logger.debug("本地文件系统客户端已关闭")


__all__ = ["LocalFileClient"]
