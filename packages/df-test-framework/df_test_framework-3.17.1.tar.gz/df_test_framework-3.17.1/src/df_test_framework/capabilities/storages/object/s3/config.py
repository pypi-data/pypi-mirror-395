"""对象存储配置

S3、MinIO、OSS 等对象存储的配置定义
"""

from pydantic import BaseModel, Field, field_validator


class S3Config(BaseModel):
    """S3 对象存储配置

    支持 AWS S3、MinIO 等兼容 S3 协议的对象存储

    Example:
        >>> # AWS S3
        >>> config = S3Config(
        ...     endpoint_url="https://s3.amazonaws.com",
        ...     access_key="YOUR_ACCESS_KEY",
        ...     secret_key="YOUR_SECRET_KEY",
        ...     bucket_name="test-bucket",
        ...     region="us-west-2"
        ... )
        >>>
        >>> # MinIO (本地测试)
        >>> config = S3Config(
        ...     endpoint_url="http://localhost:9000",
        ...     access_key="minioadmin",
        ...     secret_key="minioadmin",
        ...     bucket_name="test-bucket"
        ... )
    """

    endpoint_url: str | None = Field(
        default=None,
        description="S3 端点 URL（AWS S3 可省略，MinIO/OSS 必需）",
    )
    access_key: str = Field(..., description="访问密钥 ID (Access Key ID)")
    secret_key: str = Field(..., description="秘密访问密钥 (Secret Access Key)")
    bucket_name: str = Field(..., description="存储桶名称")
    region: str | None = Field(default=None, description="区域名称（如 us-west-2）")
    use_ssl: bool = Field(default=True, description="是否使用 HTTPS")
    verify_ssl: bool = Field(default=True, description="是否验证 SSL 证书")
    max_pool_connections: int = Field(default=10, description="连接池最大连接数")
    connect_timeout: int = Field(default=60, description="连接超时（秒）")
    read_timeout: int = Field(default=60, description="读取超时（秒）")

    # 上传下载配置
    multipart_threshold: int = Field(
        default=8 * 1024 * 1024,  # 8MB
        description="分片上传阈值（字节）",
    )
    multipart_chunksize: int = Field(
        default=8 * 1024 * 1024,  # 8MB
        description="分片大小（字节）",
    )
    max_concurrency: int = Field(default=10, description="并发上传/下载的最大线程数")

    @field_validator("access_key", "secret_key", "bucket_name")
    @classmethod
    def validate_required_fields(cls, v: str) -> str:
        """验证必需字段"""
        if not v:
            raise ValueError("field cannot be empty")
        return v

    @field_validator("max_pool_connections", "max_concurrency")
    @classmethod
    def validate_positive_int(cls, v: int) -> int:
        """验证正整数"""
        if v <= 0:
            raise ValueError("value must be positive")
        return v


__all__ = ["S3Config"]
