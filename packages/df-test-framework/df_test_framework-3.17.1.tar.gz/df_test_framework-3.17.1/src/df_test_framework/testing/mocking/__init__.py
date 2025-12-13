"""测试Mock工具集

提供HTTP、时间、数据库、Redis等Mock功能，实现完全的测试隔离

v3.5新增:
- HTTP Mock: MockInterceptor + HttpMocker
- Time Mock: TimeMocker (基于freezegun)

v3.11新增:
- Database Mock: DatabaseMocker
- Redis Mock: RedisMocker (基于fakeredis，可降级到简单mock)
"""

from .database_mock import DatabaseMocker
from .http_mock import (
    HTTPX_MOCK_AVAILABLE,
    HttpMocker,
    MockInterceptor,
    MockResponse,
    MockRule,
)
from .redis_mock import FAKEREDIS_AVAILABLE, RedisMocker
from .time_mock import (
    FREEZEGUN_AVAILABLE,
    TimeMocker,
    freeze_time_at,
)

__all__ = [
    # HTTP Mock
    "MockRule",
    "MockInterceptor",
    "MockResponse",
    "HttpMocker",
    "HTTPX_MOCK_AVAILABLE",
    # Time Mock
    "TimeMocker",
    "freeze_time_at",
    "FREEZEGUN_AVAILABLE",
    # Database Mock
    "DatabaseMocker",
    # Redis Mock
    "RedisMocker",
    "FAKEREDIS_AVAILABLE",
]
