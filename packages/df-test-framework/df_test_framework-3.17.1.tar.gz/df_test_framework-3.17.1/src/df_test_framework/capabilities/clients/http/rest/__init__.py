"""REST API客户端

支持多种HTTP客户端实现（httpx、requests等）
通过Factory模式提供统一接口
"""

# 协议定义
# 工厂类
from .factory import RestClientFactory
from .httpx.base_api import BaseAPI, BusinessError

# 默认实现（httpx）
from .httpx.client import HttpClient
from .protocols import BaseAPIProtocol, RestClientProtocol

__all__ = [
    # 协议
    "RestClientProtocol",
    "BaseAPIProtocol",
    # 工厂
    "RestClientFactory",
    # 默认实现
    "HttpClient",
    "BaseAPI",
    "BusinessError",
]
