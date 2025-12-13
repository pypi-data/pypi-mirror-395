"""HTTP请求对象（不可变）

设计理念:
- 不可变对象，避免拦截器互相影响
- 易于调试（每个拦截器的输入输出都清晰）
- 支持并发（未来）
"""

from dataclasses import dataclass, field, replace
from typing import Any


@dataclass(frozen=True)
class Request:
    """HTTP请求对象（不可变）

    使用dataclass(frozen=True)实现不可变性
    拦截器通过返回新对象来修改请求

    Example:
        >>> request = Request(method="GET", url="/users")
        >>> # 添加header（返回新对象）
        >>> new_request = request.with_header("X-Token", "abc123")
        >>> # 原对象不变
        >>> assert "X-Token" not in request.headers
        >>> assert "X-Token" in new_request.headers
    """

    method: str
    url: str
    headers: dict[str, str] = field(default_factory=dict)
    params: dict[str, Any] = field(default_factory=dict)
    json: dict[str, Any] | None = None
    data: Any | None = None

    # 上下文（拦截器间传递数据）
    context: dict[str, Any] = field(default_factory=dict)

    @property
    def path(self) -> str:
        """获取请求路径（用于路径匹配）

        从url中提取路径部分（去除query参数）

        Returns:
            请求路径

        Example:
            >>> Request(method="GET", url="/api/users?id=1").path
            '/api/users'
            >>> Request(method="GET", url="/api/users").path
            '/api/users'
        """
        # 如果url包含query参数，去除它
        if "?" in self.url:
            return self.url.split("?")[0]
        return self.url

    def with_header(self, key: str, value: str) -> "Request":
        """返回添加了新header的Request对象

        Args:
            key: Header键
            value: Header值

        Returns:
            新的Request对象
        """
        new_headers = {**self.headers, key: value}
        return replace(self, headers=new_headers)

    def with_headers(self, headers: dict[str, str]) -> "Request":
        """返回合并了headers的Request对象

        Args:
            headers: 要合并的headers字典

        Returns:
            新的Request对象
        """
        new_headers = {**self.headers, **headers}
        return replace(self, headers=new_headers)

    def with_param(self, key: str, value: Any) -> "Request":
        """返回添加了新参数的Request对象

        Args:
            key: 参数键
            value: 参数值

        Returns:
            新的Request对象
        """
        new_params = {**self.params, key: value}
        return replace(self, params=new_params)

    def with_params(self, params: dict[str, Any]) -> "Request":
        """返回合并了params的Request对象

        Args:
            params: 要合并的params字典

        Returns:
            新的Request对象
        """
        new_params = {**self.params, **params}
        return replace(self, params=new_params)

    def with_json(self, json_data: dict[str, Any]) -> "Request":
        """返回设置了json的Request对象

        Args:
            json_data: JSON数据

        Returns:
            新的Request对象
        """
        return replace(self, json=json_data)

    def with_context(self, key: str, value: Any) -> "Request":
        """在context中设置值

        Args:
            key: 上下文键
            value: 上下文值

        Returns:
            新的Request对象
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
