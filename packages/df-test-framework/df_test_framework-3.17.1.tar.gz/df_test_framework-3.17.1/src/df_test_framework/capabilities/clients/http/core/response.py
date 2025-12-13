"""HTTP响应对象（不可变）"""

from dataclasses import dataclass, field, replace
from typing import Any


@dataclass(frozen=True)
class Response:
    """HTTP响应对象（不可变）

    Example:
        >>> response = Response(status_code=200, headers={}, body="...")
        >>> # 在context中设置值（返回新对象）
        >>> new_response = response.with_context("duration", 1.5)
    """

    status_code: int
    headers: dict[str, str]
    body: str
    json_data: dict[str, Any] | None = None

    # 继承request的context
    context: dict[str, Any] = field(default_factory=dict)

    def with_context(self, key: str, value: Any) -> "Response":
        """在context中设置值

        Args:
            key: 上下文键
            value: 上下文值

        Returns:
            新的Response对象
        """
        new_context = {**self.context, key: value}
        return replace(self, context=new_context)

    def get_context(self, key: str, default: Any = None) -> Any:
        """从context中获取值

        Args:
            key: 上下文键
            default: 默认值

        Returns:
            上下文值
        """
        return self.context.get(key, default)

    @property
    def is_success(self) -> bool:
        """是否成功（2xx）"""
        return 200 <= self.status_code < 300

    @property
    def is_client_error(self) -> bool:
        """是否客户端错误（4xx）"""
        return 400 <= self.status_code < 500

    @property
    def is_server_error(self) -> bool:
        """是否服务器错误（5xx）"""
        return 500 <= self.status_code < 600
