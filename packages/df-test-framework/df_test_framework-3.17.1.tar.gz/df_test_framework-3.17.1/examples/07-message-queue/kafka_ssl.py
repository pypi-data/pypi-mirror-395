"""Kafka SSL/TLS 配置示例

演示如何配置Kafka的SSL/TLS连接。

技术栈: confluent-kafka 1.9.2
- 使用 1.9.2 版本避免 2.0+ 的 SSL_HANDSHAKE 公网连接问题

前置条件:
1. 安装依赖: pip install 'df-test-framework[kafka]'
2. 准备SSL证书文件 (CA证书、客户端证书、私钥)
"""

from df_test_framework.messengers.queue.kafka import (
    KafkaClient,
    KafkaConfig,
    KafkaProducerConfig,
    KafkaSSLConfig,
)


def example_ssl_with_certificates():
    """示例1: 使用证书的SSL连接(生产环境推荐)"""
    print("=== 示例1: SSL with Certificates ===\n")

    config = KafkaConfig(
        bootstrap_servers=["kafka.example.com:9093"],
        producer=KafkaProducerConfig(),
        ssl=KafkaSSLConfig(
            security_protocol="SSL",
            ssl_ca_location="/path/to/ca-cert.pem",  # CA证书
            ssl_certificate_location="/path/to/client-cert.pem",  # 客户端证书
            ssl_key_location="/path/to/client-key.pem",  # 客户端私钥
            ssl_key_password="your-key-password",  # 私钥密码(可选)
        ),
    )

    client = KafkaClient(config)

    # 发送测试消息
    try:
        result = client.send_sync(
            "test-topic", {"message": "Hello from SSL client"}, timeout=10.0
        )
        print(f"✅ SSL消息发送成功: {result}")
    except Exception as e:
        print(f"❌ SSL连接失败: {e}")
    finally:
        client.close()


def example_sasl_authentication():
    """示例2: SASL认证"""
    print("\n=== 示例2: SASL Authentication ===\n")

    config = KafkaConfig(
        bootstrap_servers=["kafka.example.com:9093"],
        producer=KafkaProducerConfig(),
        ssl=KafkaSSLConfig(
            security_protocol="SASL_SSL",
            sasl_mechanism="PLAIN",  # 或 SCRAM-SHA-256, SCRAM-SHA-512
            sasl_username="your-username",
            sasl_password="your-password",
            ssl_ca_location="/path/to/ca-cert.pem",
        ),
    )

    client = KafkaClient(config)

    try:
        result = client.send_sync(
            "test-topic", {"message": "Hello from SASL client"}, timeout=10.0
        )
        print(f"✅ SASL消息发送成功: {result}")
    except Exception as e:
        print(f"❌ SASL连接失败: {e}")
    finally:
        client.close()


def example_disable_ssl_verification():
    """示例3: 禁用SSL验证(仅测试环境!)"""
    print("\n=== 示例3: Disable SSL Verification (Testing Only!) ===\n")
    print("⚠️  警告: 生产环境切勿禁用SSL验证!\n")

    config = KafkaConfig(
        bootstrap_servers=["kafka-test.example.com:9092"],
        producer=KafkaProducerConfig(),
        ssl=KafkaSSLConfig(
            security_protocol="PLAINTEXT",  # 或 "SSL"
            # 针对 2.0+ 版本的 workaround (1.9.2 通常不需要)
            enable_ssl_certificate_verification="false",  # 注意: 必须是字符串!
            ssl_endpoint_identification_algorithm="none",
        ),
    )

    client = KafkaClient(config)

    try:
        result = client.send_sync(
            "test-topic", {"message": "Hello from no-verify client"}, timeout=10.0
        )
        print(f"✅ 消息发送成功: {result}")
    except Exception as e:
        print(f"❌ 连接失败: {e}")
    finally:
        client.close()


def example_plaintext():
    """示例4: PLAINTEXT连接(无加密)"""
    print("\n=== 示例4: PLAINTEXT (No Encryption) ===\n")

    config = KafkaConfig(
        bootstrap_servers=["localhost:9092"],
        producer=KafkaProducerConfig(),
        # 默认就是 PLAINTEXT,可以不指定 ssl
    )

    client = KafkaClient(config)

    try:
        result = client.send_sync(
            "test-topic", {"message": "Hello from plaintext client"}, timeout=10.0
        )
        print(f"✅ 消息发送成功: {result}")
    except Exception as e:
        print(f"❌ 连接失败: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    print("Kafka SSL/TLS 配置示例\n")
    print("=" * 50)

    # 选择要运行的示例
    print("\n请根据您的环境选择示例:")
    print("1. SSL with Certificates (生产环境)")
    print("2. SASL Authentication")
    print("3. Disable SSL Verification (仅测试!)")
    print("4. PLAINTEXT (本地开发)")

    try:
        choice = input("\n请输入选项 (1-4): ").strip()

        if choice == "1":
            example_ssl_with_certificates()
        elif choice == "2":
            example_sasl_authentication()
        elif choice == "3":
            example_disable_ssl_verification()
        elif choice == "4":
            example_plaintext()
        else:
            print("无效选项")

    except KeyboardInterrupt:
        print("\n\n👋 退出")
    except ImportError as e:
        print(f"\n❌ 导入错误: {e}")
        print("请运行: pip install 'df-test-framework[kafka]'")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
