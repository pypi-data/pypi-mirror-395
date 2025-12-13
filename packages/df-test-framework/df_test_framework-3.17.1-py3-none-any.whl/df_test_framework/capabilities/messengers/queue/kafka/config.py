"""Kafka配置模型

定义KafkaClient的配置参数。

v3.9.0新增 - 基于confluent-kafka (librdkafka) 实现

版本说明 (v3.10.0+): 使用 confluent-kafka>=2.12.0
- Windows 预编译 wheel 支持，Python 3.12+ 可直接安装
- SSL 问题说明: 2.0+ 版本在某些环境可能遇到 SSL_HANDSHAKE 错误
  → 使用 KafkaSSLConfig 的 workaround 配置可解决（见下方 KafkaSSLConfig 类）
"""

from typing import Any

from pydantic import BaseModel, Field, SecretStr


class KafkaProducerConfig(BaseModel):
    """Kafka Producer配置

    基于confluent-kafka的Producer配置。
    配置项对应librdkafka的配置参数。

    注意: librdkafka使用的配置键名与Java客户端不同:
    - batch.size -> batch.num.messages
    - buffer.memory -> queue.buffering.max.kbytes
    - linger.ms -> queue.buffering.max.ms (librdkafka也支持linger.ms别名)
    - max.in.flight.requests.per.connection -> max.in.flight
    """

    # 核心配置
    acks: str = Field(default="all", description="消息确认模式: 0, 1, all/-1")
    retries: int = Field(
        default=3, description="失败重试次数 (librdkafka: message.send.max.retries)"
    )

    # 性能配置 (字段名保持Java风格便于理解，转换时映射到librdkafka键名)
    compression_type: str | None = Field(
        default=None, description="压缩类型: gzip, snappy, lz4, zstd, none"
    )
    batch_num_messages: int = Field(
        default=10000, description="批量发送消息数 (librdkafka: batch.num.messages)"
    )
    queue_buffering_max_ms: int = Field(
        default=5, description="批量等待时间(毫秒) (librdkafka: queue.buffering.max.ms)"
    )
    queue_buffering_max_kbytes: int = Field(
        default=1048576, description="缓冲区大小(KB) (librdkafka: queue.buffering.max.kbytes)"
    )
    max_request_size: int = Field(default=1048576, description="单条消息最大大小(字节)")

    # 可靠性配置
    max_in_flight: int = Field(
        default=5, description="未确认请求的最大数量 (librdkafka: max.in.flight)"
    )
    enable_idempotence: bool = Field(default=False, description="是否启用幂等性")

    # 自定义配置 - 支持所有librdkafka配置
    extra_config: dict[str, Any] = Field(default_factory=dict, description="额外的librdkafka配置")

    def to_confluent_dict(self) -> dict[str, Any]:
        """转换为confluent-kafka配置字典

        使用librdkafka原生配置键名，确保与confluent-kafka兼容。
        参考: https://github.com/confluentinc/librdkafka/blob/master/CONFIGURATION.md
        """
        config = {}

        # acks映射: confluent-kafka使用数字
        if self.acks == "all" or self.acks == "-1":
            config["acks"] = -1
        else:
            config["acks"] = int(self.acks)

        # 使用librdkafka原生配置键名
        config["message.send.max.retries"] = self.retries
        config["batch.num.messages"] = self.batch_num_messages
        config["queue.buffering.max.ms"] = self.queue_buffering_max_ms
        config["queue.buffering.max.kbytes"] = self.queue_buffering_max_kbytes
        config["max.in.flight"] = self.max_in_flight
        config["message.max.bytes"] = self.max_request_size
        config["enable.idempotence"] = self.enable_idempotence

        if self.compression_type:
            config["compression.type"] = self.compression_type

        # 合并额外配置
        config.update(self.extra_config)

        return config


class KafkaConsumerConfig(BaseModel):
    """Kafka Consumer配置

    基于confluent-kafka的Consumer配置。
    """

    # 核心配置
    group_id: str = Field(description="消费者组ID")
    auto_offset_reset: str = Field(
        default="latest", description="offset重置策略: earliest, latest, error"
    )

    # 自动提交配置
    enable_auto_commit: bool = Field(default=True, description="是否自动提交offset")
    auto_commit_interval_ms: int = Field(default=5000, description="自动提交间隔(毫秒)")

    # 轮询配置
    max_poll_interval_ms: int = Field(default=300000, description="poll调用最大间隔(毫秒)")
    session_timeout_ms: int = Field(default=10000, description="会话超时时间(毫秒)")
    heartbeat_interval_ms: int = Field(default=3000, description="心跳间隔(毫秒)")

    # 性能配置
    fetch_min_bytes: int = Field(default=1, description="最小拉取字节数")
    fetch_max_wait_ms: int = Field(default=500, description="最大等待时间(毫秒)")
    max_partition_fetch_bytes: int = Field(default=1048576, description="单个分区最大拉取字节数")

    # 自定义配置
    extra_config: dict[str, Any] = Field(default_factory=dict, description="额外的librdkafka配置")

    def to_confluent_dict(self) -> dict[str, Any]:
        """转换为confluent-kafka配置字典"""
        config = {
            "group.id": self.group_id,
            "auto.offset.reset": self.auto_offset_reset,
            "enable.auto.commit": self.enable_auto_commit,
            "auto.commit.interval.ms": self.auto_commit_interval_ms,
            "max.poll.interval.ms": self.max_poll_interval_ms,
            "session.timeout.ms": self.session_timeout_ms,
            "heartbeat.interval.ms": self.heartbeat_interval_ms,
            "fetch.min.bytes": self.fetch_min_bytes,
            "fetch.max.wait.ms": self.fetch_max_wait_ms,
            "max.partition.fetch.bytes": self.max_partition_fetch_bytes,
        }

        # 合并额外配置
        config.update(self.extra_config)

        return config


class KafkaSSLConfig(BaseModel):
    """Kafka SSL配置

    用于配置Kafka的SSL/TLS连接。

    SSL 问题 Workaround:
    - confluent-kafka 2.0+ 在某些环境可能遇到 SSL_HANDSHAKE 错误
    - 解决方案: 使用下方的 workaround 配置项
    - 关键: enable_ssl_certificate_verification 必须是**字符串**（"true"/"false"），不是布尔值
    """

    # 安全协议
    security_protocol: str = Field(
        default="PLAINTEXT", description="安全协议: PLAINTEXT, SSL, SASL_PLAINTEXT, SASL_SSL"
    )

    # SSL证书配置
    ssl_ca_location: str | None = Field(default=None, description="CA证书文件路径")
    ssl_certificate_location: str | None = Field(default=None, description="客户端证书文件路径")
    ssl_key_location: str | None = Field(default=None, description="客户端私钥文件路径")
    ssl_key_password: str | None = Field(default=None, description="私钥密码")

    # SSL验证配置 (v2.0+ workaround)
    enable_ssl_certificate_verification: str | None = Field(
        default=None,
        description='SSL证书验证: "true" 或 "false" (字符串,不是布尔值!仅测试环境使用false)',
    )
    ssl_endpoint_identification_algorithm: str | None = Field(
        default=None, description='端点识别算法: "https" 或 "none" (仅测试环境使用none)'
    )

    # SASL配置
    sasl_mechanism: str | None = Field(
        default=None, description="SASL机制: PLAIN, SCRAM-SHA-256, SCRAM-SHA-512, GSSAPI"
    )
    sasl_username: str | None = Field(default=None, description="SASL用户名")
    sasl_password: SecretStr | None = Field(default=None, description="SASL密码")

    def to_confluent_dict(self) -> dict[str, Any]:
        """转换为confluent-kafka SSL配置字典"""
        config = {
            "security.protocol": self.security_protocol,
        }

        # SSL证书配置
        if self.ssl_ca_location:
            config["ssl.ca.location"] = self.ssl_ca_location
        if self.ssl_certificate_location:
            config["ssl.certificate.location"] = self.ssl_certificate_location
        if self.ssl_key_location:
            config["ssl.key.location"] = self.ssl_key_location
        if self.ssl_key_password:
            config["ssl.key.password"] = self.ssl_key_password

        # SSL验证配置 (v2.0+ workaround)
        if self.enable_ssl_certificate_verification is not None:
            config["enable.ssl.certificate.verification"] = self.enable_ssl_certificate_verification
        if self.ssl_endpoint_identification_algorithm is not None:
            config["ssl.endpoint.identification.algorithm"] = (
                self.ssl_endpoint_identification_algorithm
            )

        # SASL配置
        if self.sasl_mechanism:
            config["sasl.mechanism"] = self.sasl_mechanism
        if self.sasl_username:
            config["sasl.username"] = self.sasl_username
        if self.sasl_password:
            config["sasl.password"] = self.sasl_password.get_secret_value()

        return config


class KafkaConfig(BaseModel):
    """Kafka客户端配置

    基于confluent-kafka (librdkafka) 的完整配置。

    使用示例::

        # 基本配置
        config = KafkaConfig(
            bootstrap_servers=["localhost:9092"]
        )

        # SSL配置
        config = KafkaConfig(
            bootstrap_servers=["kafka.example.com:9093"],
            ssl=KafkaSSLConfig(
                security_protocol="SSL",
                ssl_ca_location="/path/to/ca-cert.pem",
                ssl_certificate_location="/path/to/client-cert.pem",
                ssl_key_location="/path/to/client-key.pem"
            )
        )

        # SSL禁用验证(仅测试环境!)
        config = KafkaConfig(
            bootstrap_servers=["kafka.example.com:9092"],
            ssl=KafkaSSLConfig(
                security_protocol="PLAINTEXT",  # 或使用SSL但禁用验证
                enable_ssl_certificate_verification="false",  # 字符串!
                ssl_endpoint_identification_algorithm="none"
            )
        )
    """

    # 核心配置
    bootstrap_servers: list[str] = Field(
        default=["localhost:9092"], description="Kafka服务器地址列表"
    )
    client_id: str | None = Field(default=None, description="客户端ID")

    # 超时配置
    request_timeout_ms: int = Field(default=30000, description="请求超时时间(毫秒)")

    # SSL/安全配置
    ssl: KafkaSSLConfig | None = Field(default=None, description="SSL配置")

    # Producer配置
    producer: KafkaProducerConfig | None = Field(default=None, description="Producer配置(可选)")

    # Consumer配置
    consumer: KafkaConsumerConfig | None = Field(default=None, description="Consumer配置(可选)")

    # 额外配置 - 支持所有librdkafka配置
    extra_config: dict[str, Any] = Field(default_factory=dict, description="额外的librdkafka配置")

    def to_confluent_dict(
        self, include_producer: bool = False, include_consumer: bool = False
    ) -> dict[str, Any]:
        """转换为confluent-kafka配置字典

        Args:
            include_producer: 是否包含Producer配置
            include_consumer: 是否包含Consumer配置

        Returns:
            confluent-kafka配置字典
        """
        config = {
            "bootstrap.servers": ",".join(self.bootstrap_servers),
            "request.timeout.ms": self.request_timeout_ms,
        }

        if self.client_id:
            config["client.id"] = self.client_id

        # SSL配置
        if self.ssl:
            config.update(self.ssl.to_confluent_dict())

        # Producer配置
        if include_producer and self.producer:
            config.update(self.producer.to_confluent_dict())

        # Consumer配置
        if include_consumer and self.consumer:
            config.update(self.consumer.to_confluent_dict())

        # 额外配置
        config.update(self.extra_config)

        return config


__all__ = [
    "KafkaConfig",
    "KafkaProducerConfig",
    "KafkaConsumerConfig",
    "KafkaSSLConfig",
]
