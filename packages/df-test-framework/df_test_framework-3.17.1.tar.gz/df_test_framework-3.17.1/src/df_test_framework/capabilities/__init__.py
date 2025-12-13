"""
能力层 (Layer 2)

与外部系统交互的能力，包括：
- clients/: HTTP/GraphQL/gRPC 客户端
- databases/: SQL/Redis/Repository/UoW
- messengers/: Kafka/RabbitMQ/RocketMQ
- storages/: S3/OSS
- drivers/: Playwright/Selenium

v3.14.0 重组：原顶级目录统一移动到 capabilities/ 下。
"""

# 重导出现有模块（兼容层）
# 用户可以通过以下方式导入：
# from df_test_framework.capabilities.clients.http import HttpClient
# 或直接：
# from df_test_framework import HttpClient

__all__ = [
    "clients",
    "databases",
    "messengers",
    "storages",
    "drivers",
]
