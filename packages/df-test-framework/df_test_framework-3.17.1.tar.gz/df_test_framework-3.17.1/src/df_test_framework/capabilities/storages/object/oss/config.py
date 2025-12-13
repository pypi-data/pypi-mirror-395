"""阿里云 OSS 配置

基于阿里云 OSS 官方 SDK 的配置定义
"""

from pydantic import BaseModel, Field, field_validator


class OSSConfig(BaseModel):
    """阿里云 OSS 对象存储配置

    支持阿里云 OSS 的完整功能

    Example:
        >>> # 公网访问（杭州）
        >>> config = OSSConfig(
        ...     access_key_id="LTAI5t...",
        ...     access_key_secret="xxx...",
        ...     bucket_name="my-bucket",
        ...     endpoint="oss-cn-hangzhou.aliyuncs.com"
        ... )
        >>>
        >>> # 内网访问（ECS 内网免流量费）
        >>> config = OSSConfig(
        ...     access_key_id="LTAI5t...",
        ...     access_key_secret="xxx...",
        ...     bucket_name="my-bucket",
        ...     endpoint="oss-cn-hangzhou-internal.aliyuncs.com"
        ... )
        >>>
        >>> # 使用 STS 临时凭证
        >>> config = OSSConfig(
        ...     access_key_id="STS.xxx",
        ...     access_key_secret="xxx",
        ...     security_token="CAI...",
        ...     bucket_name="my-bucket",
        ...     endpoint="oss-cn-shanghai.aliyuncs.com"
        ... )

    常用区域 Endpoint:
        - 华东1（杭州）: oss-cn-hangzhou.aliyuncs.com
        - 华东2（上海）: oss-cn-shanghai.aliyuncs.com
        - 华北2（北京）: oss-cn-beijing.aliyuncs.com
        - 华南1（深圳）: oss-cn-shenzhen.aliyuncs.com
        - 华南2（广州）: oss-cn-guangzhou.aliyuncs.com
        - 西南1（成都）: oss-cn-chengdu.aliyuncs.com
        - 中国香港: oss-cn-hongkong.aliyuncs.com

    内网 Endpoint（添加 -internal 后缀）:
        - 华东1（杭州）: oss-cn-hangzhou-internal.aliyuncs.com
        - ...
    """

    access_key_id: str = Field(..., description="AccessKey ID")
    access_key_secret: str = Field(..., description="AccessKey Secret")
    bucket_name: str = Field(..., description="Bucket 名称")
    endpoint: str = Field(..., description="OSS Endpoint（如 oss-cn-hangzhou.aliyuncs.com）")

    # STS 临时凭证（可选）
    security_token: str | None = Field(
        default=None, description="STS 安全令牌（使用临时凭证时必需）"
    )

    # 连接配置
    connect_timeout: int = Field(default=60, description="连接超时（秒）")

    # 上传下载配置
    multipart_threshold: int = Field(
        default=10 * 1024 * 1024,  # 10MB（OSS 推荐值）
        description="分片上传阈值（字节）",
    )
    part_size: int = Field(
        default=10 * 1024 * 1024,  # 10MB
        description="分片大小（字节，范围: 100KB - 5GB）",
    )
    max_retries: int = Field(default=3, description="最大重试次数")

    # 其他配置
    enable_crc: bool = Field(default=True, description="是否启用 CRC64 校验")

    @field_validator("access_key_id", "access_key_secret", "bucket_name", "endpoint")
    @classmethod
    def validate_required_fields(cls, v: str) -> str:
        """验证必需字段"""
        if not v or not v.strip():
            raise ValueError("field cannot be empty")
        return v.strip()

    @field_validator("part_size")
    @classmethod
    def validate_part_size(cls, v: int) -> int:
        """验证分片大小

        OSS 要求: 100KB <= part_size <= 5GB
        """
        min_size = 100 * 1024  # 100KB
        max_size = 5 * 1024 * 1024 * 1024  # 5GB
        if v < min_size or v > max_size:
            raise ValueError(f"part_size must be between {min_size} and {max_size} bytes")
        return v

    @field_validator("connect_timeout", "max_retries")
    @classmethod
    def validate_positive_int(cls, v: int) -> int:
        """验证正整数"""
        if v <= 0:
            raise ValueError("value must be positive")
        return v


__all__ = ["OSSConfig"]
