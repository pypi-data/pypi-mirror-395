"""
客户端协议定义

定义 HTTP、Database、Redis 等客户端的接口协议。
"""

from typing import Any, Protocol


class IHttpClient(Protocol):
    """HTTP 客户端协议"""

    @property
    def base_url(self) -> str:
        """基础 URL"""
        ...

    async def request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> "IHttpResponse":
        """发送 HTTP 请求"""
        ...

    async def get(self, path: str, **kwargs: Any) -> "IHttpResponse":
        """GET 请求"""
        ...

    async def post(self, path: str, **kwargs: Any) -> "IHttpResponse":
        """POST 请求"""
        ...

    async def put(self, path: str, **kwargs: Any) -> "IHttpResponse":
        """PUT 请求"""
        ...

    async def patch(self, path: str, **kwargs: Any) -> "IHttpResponse":
        """PATCH 请求"""
        ...

    async def delete(self, path: str, **kwargs: Any) -> "IHttpResponse":
        """DELETE 请求"""
        ...


class IHttpResponse(Protocol):
    """HTTP 响应协议"""

    @property
    def status_code(self) -> int:
        """状态码"""
        ...

    @property
    def headers(self) -> dict[str, str]:
        """响应头"""
        ...

    @property
    def body(self) -> bytes:
        """响应体（字节）"""
        ...

    @property
    def text(self) -> str:
        """响应体（文本）"""
        ...

    @property
    def json(self) -> dict[str, Any]:
        """响应体（JSON）"""
        ...

    @property
    def is_success(self) -> bool:
        """是否成功（2xx）"""
        ...

    @property
    def elapsed(self) -> float:
        """耗时（秒）"""
        ...


class IDatabaseClient(Protocol):
    """数据库客户端协议"""

    def session_factory(self) -> Any:
        """获取 Session 工厂"""
        ...

    def execute(self, sql: str, params: dict[str, Any] | None = None) -> Any:
        """执行 SQL"""
        ...


class IRedisClient(Protocol):
    """Redis 客户端协议"""

    async def get(self, key: str) -> str | None:
        """获取值"""
        ...

    async def set(
        self,
        key: str,
        value: str,
        ex: int | None = None,
    ) -> bool:
        """设置值"""
        ...

    async def delete(self, key: str) -> int:
        """删除键"""
        ...

    async def exists(self, key: str) -> bool:
        """检查键是否存在"""
        ...
