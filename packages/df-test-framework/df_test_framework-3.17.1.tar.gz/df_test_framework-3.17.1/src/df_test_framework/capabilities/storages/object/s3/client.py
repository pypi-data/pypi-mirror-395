"""S3 对象存储客户端

提供 S3 兼容对象存储的上传、下载、删除等操作
"""

from io import BytesIO
from typing import Any, BinaryIO

from loguru import logger

from df_test_framework.core.exceptions import ConfigurationError, ResourceError

from .config import S3Config

# boto3 是可选依赖
try:
    import boto3
    from botocore.client import Config
    from botocore.exceptions import BotoCoreError, ClientError

    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False
    boto3 = None  # type: ignore
    Config = None  # type: ignore
    BotoCoreError = Exception  # type: ignore
    ClientError = Exception  # type: ignore


class S3Client:
    """S3 对象存储客户端

    支持 AWS S3、MinIO、阿里云 OSS 等兼容 S3 协议的对象存储

    Example:
        >>> config = S3Config(
        ...     endpoint_url="http://localhost:9000",
        ...     access_key="minioadmin",
        ...     secret_key="minioadmin",
        ...     bucket_name="test-bucket"
        ... )
        >>> client = S3Client(config)
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

    def __init__(self, config: S3Config):
        """初始化客户端

        Args:
            config: S3 配置

        Raises:
            ConfigurationError: boto3 未安装
        """
        if not BOTO3_AVAILABLE:
            raise ConfigurationError(
                "boto3 未安装，无法使用 S3 客户端\n"
                "请安装: pip install boto3\n"
                "或: uv pip install boto3"
            )

        self.config = config

        # 创建 boto3 配置
        boto_config = Config(
            max_pool_connections=config.max_pool_connections,
            connect_timeout=config.connect_timeout,
            read_timeout=config.read_timeout,
            retries={"max_attempts": 3, "mode": "standard"},
        )

        # 创建 S3 客户端
        client_kwargs: dict[str, Any] = {
            "service_name": "s3",
            "aws_access_key_id": config.access_key,
            "aws_secret_access_key": config.secret_key,
            "config": boto_config,
            "use_ssl": config.use_ssl,
            "verify": config.verify_ssl,
        }

        if config.endpoint_url:
            client_kwargs["endpoint_url"] = config.endpoint_url

        if config.region:
            client_kwargs["region_name"] = config.region

        self._client = boto3.client(**client_kwargs)
        self._bucket = config.bucket_name

        logger.info(f"S3 客户端已初始化: bucket={self._bucket}")

        # 确保 bucket 存在
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self) -> None:
        """确保 bucket 存在，不存在则创建"""
        try:
            self._client.head_bucket(Bucket=self._bucket)
            logger.debug(f"Bucket 已存在: {self._bucket}")
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "")
            if error_code == "404":
                # Bucket 不存在，创建它
                logger.info(f"创建 Bucket: {self._bucket}")
                try:
                    if self.config.region:
                        self._client.create_bucket(
                            Bucket=self._bucket,
                            CreateBucketConfiguration={"LocationConstraint": self.config.region},
                        )
                    else:
                        self._client.create_bucket(Bucket=self._bucket)
                except ClientError as create_error:
                    raise ResourceError(f"创建 Bucket 失败: {create_error}") from create_error
            else:
                raise ResourceError(f"检查 Bucket 失败: {e}") from e

    def upload(
        self,
        key: str,
        content: bytes | BinaryIO,
        metadata: dict[str, str] | None = None,
        content_type: str | None = None,
    ) -> dict:
        """上传文件到 S3

        Args:
            key: 对象键（文件路径）
            content: 文件内容（字节或文件对象）
            metadata: 自定义元数据
            content_type: 内容类型（如 'text/plain'）

        Returns:
            上传结果字典

        Raises:
            ResourceError: 上传失败

        Example:
            >>> client.upload("test.txt", b"Hello")
            {'key': 'test.txt', 'bucket': 'test-bucket', 'size': 5}
        """
        try:
            # 准备上传参数
            extra_args: dict[str, Any] = {}

            if metadata:
                extra_args["Metadata"] = metadata

            if content_type:
                extra_args["ContentType"] = content_type

            # 转换为文件对象
            if isinstance(content, bytes):
                file_obj = BytesIO(content)
                size = len(content)
            else:
                file_obj = content
                # 获取文件大小
                pos = file_obj.tell()
                file_obj.seek(0, 2)  # 移动到文件末尾
                size = file_obj.tell()
                file_obj.seek(pos)  # 恢复位置

            # 上传文件
            self._client.upload_fileobj(
                Fileobj=file_obj, Bucket=self._bucket, Key=key, ExtraArgs=extra_args
            )

            logger.info(f"文件上传成功: {key} ({size} bytes)")

            return {"key": key, "bucket": self._bucket, "size": size}

        except (BotoCoreError, ClientError) as e:
            raise ResourceError(f"上传文件失败: {e}") from e

    def download(self, key: str) -> bytes:
        """从 S3 下载文件

        Args:
            key: 对象键（文件路径）

        Returns:
            文件内容（字节）

        Raises:
            ResourceError: 下载失败、文件不存在

        Example:
            >>> content = client.download("test.txt")
        """
        try:
            response = self._client.get_object(Bucket=self._bucket, Key=key)
            content = response["Body"].read()

            logger.debug(f"文件下载成功: {key} ({len(content)} bytes)")

            return content

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "")
            if error_code == "NoSuchKey":
                raise ResourceError(f"文件不存在: {key}") from e
            raise ResourceError(f"下载文件失败: {e}") from e
        except BotoCoreError as e:
            raise ResourceError(f"下载文件失败: {e}") from e

    def delete(self, key: str, missing_ok: bool = False) -> bool:
        """删除 S3 对象

        Args:
            key: 对象键（文件路径）
            missing_ok: 文件不存在时是否报错

        Returns:
            是否删除成功

        Raises:
            ResourceError: 删除失败

        Example:
            >>> client.delete("test.txt")
            True
        """
        try:
            # 先检查文件是否存在
            if not self.exists(key):
                if missing_ok:
                    logger.debug(f"文件不存在，跳过删除: {key}")
                    return False
                raise ResourceError(f"文件不存在: {key}")

            self._client.delete_object(Bucket=self._bucket, Key=key)

            logger.info(f"文件删除成功: {key}")

            return True

        except (BotoCoreError, ClientError) as e:
            raise ResourceError(f"删除文件失败: {e}") from e

    def exists(self, key: str) -> bool:
        """检查对象是否存在

        Args:
            key: 对象键（文件路径）

        Returns:
            是否存在

        Example:
            >>> client.exists("test.txt")
            True
        """
        try:
            self._client.head_object(Bucket=self._bucket, Key=key)
            return True
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "")
            if error_code in ("404", "NoSuchKey"):
                return False
            # 其他错误则抛出
            raise ResourceError(f"检查文件存在性失败: {e}") from e

    def list_objects(
        self, prefix: str = "", max_keys: int = 1000, delimiter: str = ""
    ) -> list[dict]:
        """列出对象

        Args:
            prefix: 前缀过滤
            max_keys: 最大返回数量
            delimiter: 分隔符（用于实现"目录"效果）

        Returns:
            对象列表，每个对象包含 key, size, last_modified

        Example:
            >>> objects = client.list_objects(prefix="test/")
            >>> for obj in objects:
            ...     print(obj['key'], obj['size'])
        """
        try:
            kwargs: dict[str, Any] = {
                "Bucket": self._bucket,
                "Prefix": prefix,
                "MaxKeys": max_keys,
            }

            if delimiter:
                kwargs["Delimiter"] = delimiter

            response = self._client.list_objects_v2(**kwargs)

            objects = []
            for item in response.get("Contents", []):
                objects.append(
                    {
                        "key": item["Key"],
                        "size": item["Size"],
                        "last_modified": item["LastModified"],
                        "etag": item["ETag"],
                    }
                )

            return objects

        except (BotoCoreError, ClientError) as e:
            raise ResourceError(f"列出对象失败: {e}") from e

    def get_object_info(self, key: str) -> dict:
        """获取对象信息

        Args:
            key: 对象键

        Returns:
            对象信息字典

        Raises:
            ResourceError: 对象不存在

        Example:
            >>> info = client.get_object_info("test.txt")
            >>> print(info['size'], info['content_type'])
        """
        try:
            response = self._client.head_object(Bucket=self._bucket, Key=key)

            return {
                "key": key,
                "size": response["ContentLength"],
                "content_type": response.get("ContentType", ""),
                "last_modified": response["LastModified"],
                "etag": response["ETag"],
                "metadata": response.get("Metadata", {}),
            }

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "")
            if error_code == "404":
                raise ResourceError(f"对象不存在: {key}") from e
            raise ResourceError(f"获取对象信息失败: {e}") from e

    def copy(self, src_key: str, dest_key: str, src_bucket: str | None = None) -> dict:
        """复制对象

        Args:
            src_key: 源对象键
            dest_key: 目标对象键
            src_bucket: 源 bucket（None 表示同一 bucket）

        Returns:
            复制结果字典

        Raises:
            ResourceError: 复制失败

        Example:
            >>> client.copy("source.txt", "dest.txt")
        """
        try:
            copy_source = {
                "Bucket": src_bucket or self._bucket,
                "Key": src_key,
            }

            self._client.copy_object(CopySource=copy_source, Bucket=self._bucket, Key=dest_key)

            logger.info(f"对象复制成功: {src_key} -> {dest_key}")

            return self.get_object_info(dest_key)

        except (BotoCoreError, ClientError) as e:
            raise ResourceError(f"复制对象失败: {e}") from e

    def generate_presigned_url(
        self, key: str, expiration: int = 3600, http_method: str = "GET"
    ) -> str:
        """生成预签名 URL

        Args:
            key: 对象键
            expiration: 过期时间（秒）
            http_method: HTTP 方法（GET 或 PUT）

        Returns:
            预签名 URL

        Example:
            >>> url = client.generate_presigned_url("test.txt", expiration=300)
            >>> # 使用 URL 直接访问文件
        """
        try:
            method_map = {"GET": "get_object", "PUT": "put_object"}
            client_method = method_map.get(http_method.upper(), "get_object")

            url = self._client.generate_presigned_url(
                ClientMethod=client_method,
                Params={"Bucket": self._bucket, "Key": key},
                ExpiresIn=expiration,
            )

            logger.debug(f"生成预签名 URL: {key} (有效期 {expiration}秒)")

            return url

        except (BotoCoreError, ClientError) as e:
            raise ResourceError(f"生成预签名 URL 失败: {e}") from e

    def clear(self, prefix: str = "") -> int:
        """清空 bucket 或指定前缀下的所有对象

        Args:
            prefix: 前缀（空字符串表示清空整个 bucket）

        Returns:
            删除的对象数量

        Example:
            >>> count = client.clear(prefix="test/")
            >>> print(f"删除了 {count} 个对象")
        """
        objects = self.list_objects(prefix=prefix, max_keys=1000)

        if not objects:
            return 0

        # 批量删除
        delete_keys = [{"Key": obj["key"]} for obj in objects]

        try:
            response = self._client.delete_objects(
                Bucket=self._bucket, Delete={"Objects": delete_keys}
            )

            deleted_count = len(response.get("Deleted", []))

            logger.info(f"清空完成: prefix={prefix} ({deleted_count} 个对象)")

            return deleted_count

        except (BotoCoreError, ClientError) as e:
            raise ResourceError(f"清空对象失败: {e}") from e

    def close(self) -> None:
        """关闭客户端"""
        if hasattr(self, "_client"):
            # boto3 客户端会自动管理连接池
            logger.debug("S3 客户端已关闭")


__all__ = ["S3Client"]
