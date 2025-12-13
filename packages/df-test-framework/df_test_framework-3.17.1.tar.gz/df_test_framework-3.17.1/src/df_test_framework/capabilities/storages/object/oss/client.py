"""阿里云 OSS 对象存储客户端

基于阿里云官方 SDK (oss2) 实现
提供完整的 OSS 功能支持
"""

from io import BytesIO
from pathlib import Path
from typing import Any, BinaryIO

from loguru import logger

from df_test_framework.core.exceptions import ConfigurationError, ResourceError

from .config import OSSConfig

# oss2 是可选依赖
try:
    import oss2
    from oss2.exceptions import NoSuchKey, RequestError

    OSS2_AVAILABLE = True
except ImportError:
    OSS2_AVAILABLE = False
    oss2 = None  # type: ignore
    NoSuchKey = Exception  # type: ignore
    RequestError = Exception  # type: ignore


class OSSClient:
    """阿里云 OSS 对象存储客户端

    基于 oss2 SDK 实现，提供 OSS 对象的上传、下载、删除等操作

    Example:
        >>> # 初始化客户端
        >>> config = OSSConfig(
        ...     access_key_id="LTAI5t...",
        ...     access_key_secret="xxx...",
        ...     bucket_name="my-bucket",
        ...     endpoint="oss-cn-hangzhou.aliyuncs.com"
        ... )
        >>> client = OSSClient(config)
        >>>
        >>> # 上传文件
        >>> client.upload("test.txt", b"Hello OSS")
        >>>
        >>> # 下载文件
        >>> content = client.download("test.txt")
        >>>
        >>> # 删除文件
        >>> client.delete("test.txt")
        >>>
        >>> # 关闭客户端
        >>> client.close()
    """

    def __init__(self, config: OSSConfig):
        """初始化 OSS 客户端

        Args:
            config: OSS 配置对象

        Raises:
            ConfigurationError: oss2 未安装或配置错误
        """
        if not OSS2_AVAILABLE:
            raise ConfigurationError(
                "oss2 未安装。请安装: pip install oss2\n"
                "或安装完整存储支持: pip install df-test-framework[storage-all]"
            )

        self.config = config

        try:
            # 创建认证对象
            if config.security_token:
                # 使用 STS 临时凭证
                auth = oss2.StsAuth(
                    config.access_key_id,
                    config.access_key_secret,
                    config.security_token,
                )
            else:
                # 使用永久凭证
                auth = oss2.Auth(config.access_key_id, config.access_key_secret)

            # 创建 Bucket 对象
            self.bucket = oss2.Bucket(
                auth,
                config.endpoint,
                config.bucket_name,
                connect_timeout=config.connect_timeout,
                enable_crc=config.enable_crc,
            )

            # 验证 bucket 是否存在
            if not self.bucket.bucket_exists():
                logger.warning(f"Bucket '{config.bucket_name}' 不存在，尝试创建...")
                # OSS 不支持自动创建 bucket，需要用户手动创建或使用控制台
                raise ConfigurationError(
                    f"Bucket '{config.bucket_name}' 不存在。请先在阿里云控制台创建 Bucket"
                )

            logger.info(
                f"OSS 客户端初始化成功: bucket={config.bucket_name}, endpoint={config.endpoint}"
            )

        except Exception as e:
            if isinstance(e, ConfigurationError):
                raise
            raise ConfigurationError(f"OSS 客户端初始化失败: {e}") from e

    def upload(
        self,
        key: str,
        data: bytes | BinaryIO | str | Path,
        content_type: str | None = None,
        metadata: dict[str, str] | None = None,
        **kwargs,
    ) -> dict[str, Any]:
        """上传对象到 OSS

        Args:
            key: 对象键（路径）
            data: 要上传的数据（字节、文件对象、文件路径）
            content_type: Content-Type（可选）
            metadata: 用户自定义元数据（可选）
            **kwargs: 其他 oss2 参数

        Returns:
            上传结果信息字典

        Raises:
            ResourceError: 上传失败

        Example:
            >>> # 上传字节
            >>> client.upload("test.txt", b"Hello")
            >>>
            >>> # 上传文件
            >>> client.upload("test.txt", Path("/path/to/file"))
            >>>
            >>> # 上传带元数据
            >>> client.upload(
            ...     "test.txt",
            ...     b"Hello",
            ...     content_type="text/plain",
            ...     metadata={"author": "test"}
            ... )
        """
        try:
            # 准备 headers
            headers = {}
            if content_type:
                headers["Content-Type"] = content_type
            if metadata:
                # OSS 元数据需要 x-oss-meta- 前缀
                for k, v in metadata.items():
                    headers[f"x-oss-meta-{k}"] = v

            # 处理不同类型的 data
            if isinstance(data, (str, Path)):
                # 文件路径
                file_path = Path(data)
                if not file_path.exists():
                    raise ResourceError(f"文件不存在: {file_path}")

                # 大文件使用断点续传
                file_size = file_path.stat().st_size
                if file_size >= self.config.multipart_threshold:
                    result = oss2.resumable_upload(
                        self.bucket,
                        key,
                        str(file_path),
                        headers=headers,
                        part_size=self.config.part_size,
                        **kwargs,
                    )
                else:
                    result = self.bucket.put_object_from_file(
                        key, str(file_path), headers=headers, **kwargs
                    )
            elif isinstance(data, bytes):
                # 字节数据
                data_stream = BytesIO(data)
                result = self.bucket.put_object(key, data_stream, headers=headers, **kwargs)
            else:
                # 文件对象
                result = self.bucket.put_object(key, data, headers=headers, **kwargs)

            logger.info(f"OSS 上传成功: key={key}, etag={result.etag}")

            return {
                "key": key,
                "bucket": self.config.bucket_name,
                "etag": result.etag,
                "request_id": result.request_id,
            }

        except Exception as e:
            logger.error(f"OSS 上传失败: key={key}, error={e}")
            raise ResourceError(f"上传失败: {e}") from e

    def download(self, key: str, **kwargs) -> bytes:
        """从 OSS 下载对象

        Args:
            key: 对象键（路径）
            **kwargs: 其他 oss2 参数

        Returns:
            对象内容（字节）

        Raises:
            ResourceError: 下载失败或对象不存在

        Example:
            >>> content = client.download("test.txt")
            >>> print(content.decode())
        """
        try:
            result = self.bucket.get_object(key, **kwargs)
            content = result.read()

            logger.info(f"OSS 下载成功: key={key}, size={len(content)}")
            return content

        except NoSuchKey:
            raise ResourceError(f"对象不存在: {key}")
        except Exception as e:
            logger.error(f"OSS 下载失败: key={key}, error={e}")
            raise ResourceError(f"下载失败: {e}") from e

    def download_to_file(self, key: str, file_path: str | Path, **kwargs) -> None:
        """下载对象到本地文件

        Args:
            key: 对象键（路径）
            file_path: 本地文件路径
            **kwargs: 其他 oss2 参数

        Raises:
            ResourceError: 下载失败

        Example:
            >>> client.download_to_file("test.txt", "/tmp/test.txt")
        """
        try:
            self.bucket.get_object_to_file(key, str(file_path), **kwargs)
            logger.info(f"OSS 下载到文件成功: key={key}, file={file_path}")

        except NoSuchKey:
            raise ResourceError(f"对象不存在: {key}")
        except Exception as e:
            logger.error(f"OSS 下载到文件失败: key={key}, error={e}")
            raise ResourceError(f"下载失败: {e}") from e

    def delete(self, key: str, missing_ok: bool = False) -> bool:
        """删除 OSS 对象

        Args:
            key: 对象键（路径）
            missing_ok: 对象不存在时是否报错

        Returns:
            是否成功删除

        Raises:
            ResourceError: 删除失败（当 missing_ok=False 且对象不存在时）

        Example:
            >>> client.delete("test.txt")
            >>> client.delete("nonexistent.txt", missing_ok=True)
        """
        try:
            # 检查对象是否存在
            if not self.exists(key):
                if missing_ok:
                    logger.debug(f"OSS 对象不存在（已忽略）: key={key}")
                    return False
                raise ResourceError(f"对象不存在: {key}")

            # 删除对象
            self.bucket.delete_object(key)
            logger.info(f"OSS 删除成功: key={key}")
            return True

        except ResourceError:
            raise
        except Exception as e:
            logger.error(f"OSS 删除失败: key={key}, error={e}")
            raise ResourceError(f"删除失败: {e}") from e

    def exists(self, key: str) -> bool:
        """检查对象是否存在

        Args:
            key: 对象键（路径）

        Returns:
            对象是否存在

        Example:
            >>> if client.exists("test.txt"):
            ...     print("文件存在")
        """
        try:
            self.bucket.head_object(key)
            return True
        except NoSuchKey:
            return False
        except Exception as e:
            logger.error(f"OSS 检查对象存在失败: key={key}, error={e}")
            return False

    def list_objects(self, prefix: str = "", max_keys: int = 100, **kwargs) -> list[dict[str, Any]]:
        """列出对象

        Args:
            prefix: 对象键前缀
            max_keys: 最多返回的对象数量
            **kwargs: 其他 oss2 参数

        Returns:
            对象信息列表

        Example:
            >>> objects = client.list_objects(prefix="test/")
            >>> for obj in objects:
            ...     print(obj["key"], obj["size"])
        """
        try:
            objects = []
            for obj in oss2.ObjectIterator(self.bucket, prefix=prefix, max_keys=max_keys, **kwargs):
                objects.append(
                    {
                        "key": obj.key,
                        "size": obj.size,
                        "last_modified": obj.last_modified,
                        "etag": obj.etag,
                        "type": obj.type,
                    }
                )

            logger.info(f"OSS 列出对象成功: prefix={prefix}, count={len(objects)}")
            return objects

        except Exception as e:
            logger.error(f"OSS 列出对象失败: prefix={prefix}, error={e}")
            raise ResourceError(f"列出对象失败: {e}") from e

    def get_object_info(self, key: str) -> dict[str, Any]:
        """获取对象元信息

        Args:
            key: 对象键（路径）

        Returns:
            对象元信息

        Raises:
            ResourceError: 对象不存在或获取失败

        Example:
            >>> info = client.get_object_info("test.txt")
            >>> print(info["size"], info["content_type"])
        """
        try:
            meta = self.bucket.head_object(key)

            # 提取用户元数据
            user_metadata = {}
            for k, v in meta.headers.items():
                if k.startswith("x-oss-meta-"):
                    user_key = k.replace("x-oss-meta-", "")
                    user_metadata[user_key] = v

            return {
                "key": key,
                "size": meta.content_length,
                "content_type": meta.content_type,
                "last_modified": meta.last_modified,
                "etag": meta.etag,
                "metadata": user_metadata,
            }

        except NoSuchKey:
            raise ResourceError(f"对象不存在: {key}")
        except Exception as e:
            logger.error(f"OSS 获取对象信息失败: key={key}, error={e}")
            raise ResourceError(f"获取对象信息失败: {e}") from e

    def copy(self, source_key: str, dest_key: str, **kwargs) -> dict[str, Any]:
        """复制对象

        Args:
            source_key: 源对象键
            dest_key: 目标对象键
            **kwargs: 其他 oss2 参数

        Returns:
            复制结果信息

        Raises:
            ResourceError: 复制失败

        Example:
            >>> client.copy("source.txt", "dest.txt")
        """
        try:
            result = self.bucket.copy_object(
                self.config.bucket_name, source_key, dest_key, **kwargs
            )

            logger.info(f"OSS 复制成功: {source_key} -> {dest_key}")

            return {
                "source_key": source_key,
                "dest_key": dest_key,
                "etag": result.etag,
            }

        except NoSuchKey:
            raise ResourceError(f"源对象不存在: {source_key}")
        except Exception as e:
            logger.error(f"OSS 复制失败: {source_key} -> {dest_key}, error={e}")
            raise ResourceError(f"复制失败: {e}") from e

    def generate_presigned_url(self, key: str, expiration: int = 3600, method: str = "GET") -> str:
        """生成预签名 URL

        Args:
            key: 对象键（路径）
            expiration: 过期时间（秒）
            method: HTTP 方法（GET/PUT/POST/DELETE）

        Returns:
            预签名 URL

        Example:
            >>> # 生成下载链接（1小时有效）
            >>> url = client.generate_presigned_url("test.txt", expiration=3600)
            >>>
            >>> # 生成上传链接
            >>> url = client.generate_presigned_url("test.txt", method="PUT")
        """
        try:
            url = self.bucket.sign_url(method, key, expiration)
            logger.info(f"OSS 生成预签名 URL 成功: key={key}, expiration={expiration}s")
            return url

        except Exception as e:
            logger.error(f"OSS 生成预签名 URL 失败: key={key}, error={e}")
            raise ResourceError(f"生成预签名 URL 失败: {e}") from e

    def clear(self, prefix: str = "") -> int:
        """批量删除对象

        Args:
            prefix: 对象键前缀（为空则删除所有对象）

        Returns:
            删除的对象数量

        Example:
            >>> # 删除指定前缀的对象
            >>> count = client.clear(prefix="test/")
            >>> print(f"已删除 {count} 个对象")
        """
        try:
            # 列出所有对象
            keys_to_delete = []
            for obj in oss2.ObjectIterator(self.bucket, prefix=prefix):
                keys_to_delete.append(obj.key)

            if not keys_to_delete:
                logger.info(f"OSS 没有需要删除的对象: prefix={prefix}")
                return 0

            # 批量删除（每次最多 1000 个）
            deleted_count = 0
            batch_size = 1000

            for i in range(0, len(keys_to_delete), batch_size):
                batch = keys_to_delete[i : i + batch_size]
                result = self.bucket.batch_delete_objects(batch)
                deleted_count += len(result.deleted_keys)

            logger.info(f"OSS 批量删除成功: prefix={prefix}, count={deleted_count}")
            return deleted_count

        except Exception as e:
            logger.error(f"OSS 批量删除失败: prefix={prefix}, error={e}")
            raise ResourceError(f"批量删除失败: {e}") from e

    def close(self) -> None:
        """关闭客户端

        OSS 客户端无需显式关闭，此方法用于接口统一
        """
        logger.debug("OSS 客户端关闭（无操作）")


__all__ = ["OSSClient"]
