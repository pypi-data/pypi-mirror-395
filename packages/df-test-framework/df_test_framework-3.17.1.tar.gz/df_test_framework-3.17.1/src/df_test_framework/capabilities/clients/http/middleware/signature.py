"""
签名中间件

自动为 HTTP 请求添加签名。
"""

import hashlib
import hmac
import time
from typing import Any, Literal

from df_test_framework.capabilities.clients.http.core.request import Request
from df_test_framework.capabilities.clients.http.core.response import Response
from df_test_framework.core.middleware import BaseMiddleware


class SignatureMiddleware(BaseMiddleware[Request, Response]):
    """签名中间件

    自动为请求添加签名 Header。

    支持的签名算法：
    - md5: MD5 签名
    - sha256: SHA256 签名
    - hmac-sha256: HMAC-SHA256 签名

    签名计算方式：
    1. 收集参数和请求体
    2. 按键名排序
    3. 拼接值和密钥
    4. 计算哈希

    示例:
        middleware = SignatureMiddleware(
            secret="my_secret",
            algorithm="hmac-sha256",
            header_name="X-Signature",
        )

        client.use(middleware)
    """

    def __init__(
        self,
        secret: str,
        algorithm: Literal["md5", "sha256", "hmac-sha256"] = "md5",
        header_name: str = "X-Sign",
        timestamp_header: str | None = "X-Timestamp",
        include_params: bool = True,
        include_body: bool = True,
        priority: int = 10,
    ):
        """初始化签名中间件

        Args:
            secret: 签名密钥
            algorithm: 签名算法
            header_name: 签名 Header 名称
            timestamp_header: 时间戳 Header 名称（None 表示不添加）
            include_params: 是否包含 URL 参数
            include_body: 是否包含请求体
            priority: 优先级
        """
        super().__init__(name="SignatureMiddleware", priority=priority)
        self.secret = secret
        self.algorithm = algorithm
        self.header_name = header_name
        self.timestamp_header = timestamp_header
        self.include_params = include_params
        self.include_body = include_body

    async def __call__(
        self,
        request: Request,
        call_next,
    ) -> Response:
        """执行签名"""
        # 收集签名数据
        data: dict[str, Any] = {}

        if self.include_params and request.params:
            data.update(request.params)

        if self.include_body and request.json:
            data.update(request.json)

        # 添加时间戳 (秒级) - 只添加到header，不参与签名
        timestamp = str(int(time.time()))
        if self.timestamp_header:
            request = request.with_header(self.timestamp_header, timestamp)
            # 注意：timestamp 不应参与签名计算（与Java后端一致）
            # data["timestamp"] = timestamp

        # 生成签名
        signature = self._sign(data)

        # 添加签名头
        request = request.with_header(self.header_name, signature)

        return await call_next(request)

    def _sign(self, data: dict[str, Any]) -> str:
        """计算签名（与Java后端SignatureUtil.java对齐）

        签名算法：
        1. 参数按key排序
        2. 只拼接value值（不包含key）
        3. 追加密钥
        4. MD5/SHA256加密

        Args:
            data: 要签名的数据

        Returns:
            签名字符串
        """
        # 按键名排序
        sorted_items = sorted(data.items(), key=lambda x: x[0])
        # 只拼接value值（与Java后端一致）
        values = "".join(str(v) for k, v in sorted_items if v is not None and str(v) != "")
        sign_string = f"{values}{self.secret}"

        match self.algorithm:
            case "md5":
                return hashlib.md5(sign_string.encode()).hexdigest()
            case "sha256":
                return hashlib.sha256(sign_string.encode()).hexdigest()
            case "hmac-sha256":
                return hmac.new(
                    self.secret.encode(),
                    values.encode(),
                    "sha256",
                ).hexdigest()
            case _:
                raise ValueError(f"Unknown algorithm: {self.algorithm}")
