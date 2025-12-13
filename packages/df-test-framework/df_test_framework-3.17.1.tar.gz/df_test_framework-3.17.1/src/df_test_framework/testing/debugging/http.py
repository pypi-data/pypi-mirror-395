"""HTTP请求/响应调试工具

自动记录HTTP请求和响应详情，帮助调试API测试问题。
"""

from __future__ import annotations

import json
import logging
import time
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class HTTPDebugger:
    """HTTP调试器

    记录所有HTTP请求和响应，提供详细的调试信息。

    Example:
        >>> debugger = HTTPDebugger()
        >>> debugger.start()
        >>> # 执行HTTP请求
        >>> debugger.log_request("GET", "https://api.example.com/users/1")
        >>> debugger.log_response(200, {"id": 1, "name": "John"})
        >>> debugger.stop()
        >>> debugger.print_summary()
    """

    def __init__(self, enabled: bool = True, max_body_length: int = 1000):
        """初始化HTTP调试器

        Args:
            enabled: 是否启用调试
            max_body_length: 最大记录的body长度（超过会截断）
        """
        self.enabled = enabled
        self.max_body_length = max_body_length
        self.requests: list[dict[str, Any]] = []
        self.current_request: dict[str, Any] | None = None
        self._start_time: float | None = None

    def start(self):
        """启动调试"""
        self.enabled = True
        logger.info("🔍 HTTP调试已启用")

    def stop(self):
        """停止调试"""
        self.enabled = False
        logger.info("⏹️  HTTP调试已停止")

    def clear(self):
        """清空调试记录"""
        self.requests.clear()
        self.current_request = None

    def log_request(
        self,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        body: Any | None = None,
        params: dict[str, Any] | None = None,
    ):
        """记录HTTP请求

        Args:
            method: HTTP方法
            url: 请求URL
            headers: 请求头
            body: 请求体
            params: 查询参数
        """
        if not self.enabled:
            return

        self._start_time = time.time()
        self.current_request = {
            "timestamp": datetime.now().isoformat(),
            "method": method,
            "url": url,
            "headers": self._truncate_dict(headers or {}),
            "params": params,
            "body": self._truncate_body(body),
            "response": None,
            "duration_ms": None,
        }

        # v3: 同时输出到stdout (pytest -s可见) 和logger
        print(f"[HTTP DEBUG] {method} {url}")
        if params:
            print(f"[HTTP DEBUG] Params: {params}")
        if headers:
            # 打印认证相关headers (包括自定义签名头)
            key_headers = {}
            for k, v in headers.items():
                k_lower = k.lower()
                # 只打印认证相关和内容类型headers
                if k_lower in ["content-type", "authorization", "x-sign", "x-token", "x-api-key"]:
                    # 脱敏长token值
                    if (
                        isinstance(v, str)
                        and len(v) > 20
                        and k_lower in ["authorization", "x-sign", "x-token"]
                    ):
                        key_headers[k] = v[:10] + "..." + v[-8:]
                    else:
                        key_headers[k] = v
            if key_headers:
                print(f"[HTTP DEBUG] Headers: {key_headers}")
        if body:
            print(f"[HTTP DEBUG] Body: {self._truncate_body(body)}")

        logger.debug(f"➡️  {method} {url}")

    def log_response(
        self,
        status_code: int,
        headers: dict[str, str] | None = None,
        body: Any | None = None,
    ):
        """记录HTTP响应

        Args:
            status_code: 状态码
            headers: 响应头
            body: 响应体
        """
        if not self.enabled or not self.current_request:
            return

        duration_ms = (time.time() - self._start_time) * 1000 if self._start_time else 0

        self.current_request["response"] = {
            "status_code": status_code,
            "headers": self._truncate_dict(headers or {}),
            "body": self._truncate_body(body),
        }
        self.current_request["duration_ms"] = duration_ms

        self.requests.append(self.current_request.copy())

        # v3: 同时输出到stdout (pytest -s可见) 和logger
        status_icon = "✅" if status_code < 400 else ("⚠️" if status_code < 500 else "❌")
        print(f"[HTTP DEBUG] Response: {status_code} {status_icon} in {duration_ms:.2f}ms")
        if body:
            print(f"[HTTP DEBUG] Response Body: {self._truncate_body(body)}")

        # 根据状态码使用不同的日志级别
        if status_code >= 500:
            logger.error(f"⬅️  {status_code} ({duration_ms:.2f}ms) ❌")
        elif status_code >= 400:
            logger.warning(f"⬅️  {status_code} ({duration_ms:.2f}ms) ⚠️")
        else:
            logger.debug(f"⬅️  {status_code} ({duration_ms:.2f}ms) ✅")

        self.current_request = None
        self._start_time = None

    def log_error(self, error: Exception):
        """记录请求错误

        Args:
            error: 异常对象
        """
        if not self.enabled or not self.current_request:
            return

        duration_ms = (time.time() - self._start_time) * 1000 if self._start_time else 0

        self.current_request["response"] = {
            "error": str(error),
            "error_type": type(error).__name__,
        }
        self.current_request["duration_ms"] = duration_ms

        self.requests.append(self.current_request.copy())
        logger.error(f"⬅️  ERROR: {error} ({duration_ms:.2f}ms) 💥")

        self.current_request = None
        self._start_time = None

    def get_requests(self) -> list[dict[str, Any]]:
        """获取所有请求记录

        Returns:
            List[Dict]: 请求记录列表
        """
        return self.requests.copy()

    def get_failed_requests(self) -> list[dict[str, Any]]:
        """获取失败的请求（状态码>=400或有错误）

        Returns:
            List[Dict]: 失败的请求列表
        """
        failed = []
        for req in self.requests:
            if req["response"]:
                if "error" in req["response"]:
                    failed.append(req)
                elif req["response"].get("status_code", 0) >= 400:
                    failed.append(req)
        return failed

    def print_summary(self):
        """打印调试摘要"""
        if not self.requests:
            print("\n📊 HTTP调试摘要: 无请求记录")
            return

        print("\n" + "=" * 80)
        print("📊 HTTP调试摘要")
        print("=" * 80)

        total = len(self.requests)
        failed = len(self.get_failed_requests())
        success = total - failed

        print(f"\n总请求数: {total}")
        print(f"  成功: {success} ✅")
        print(f"  失败: {failed} ❌")

        if self.requests:
            durations = [r["duration_ms"] for r in self.requests if r["duration_ms"]]
            if durations:
                avg_duration = sum(durations) / len(durations)
                max_duration = max(durations)
                min_duration = min(durations)
                print("\n响应时间:")
                print(f"  平均: {avg_duration:.2f}ms")
                print(f"  最快: {min_duration:.2f}ms")
                print(f"  最慢: {max_duration:.2f}ms")

        print("\n" + "=" * 80)
        print("📋 请求详情:")
        print("=" * 80)

        for i, req in enumerate(self.requests, 1):
            self._print_request_detail(i, req)

        print("=" * 80)

    def _print_request_detail(self, index: int, req: dict[str, Any]):
        """打印单个请求详情"""
        status_icon = "✅"
        if req["response"]:
            if "error" in req["response"]:
                status_icon = "💥"
            elif req["response"].get("status_code", 0) >= 400:
                status_icon = "❌"

        print(f"\n{index}. {status_icon} {req['method']} {req['url']}")
        print(f"   时间: {req['timestamp']}")

        if req.get("params"):
            print(f"   参数: {req['params']}")

        if req.get("duration_ms"):
            print(f"   耗时: {req['duration_ms']:.2f}ms")

        if req["response"]:
            if "error" in req["response"]:
                print(f"   错误: {req['response']['error']}")
            else:
                status_code = req["response"].get("status_code")
                print(f"   状态: {status_code}")

                body = req["response"].get("body")
                if body:
                    body_str = str(body)
                    if len(body_str) > 100:
                        body_str = body_str[:100] + "..."
                    print(f"   响应: {body_str}")

    def _truncate_body(self, body: Any) -> Any:
        """截断body（如果太长）"""
        if body is None:
            return None

        if isinstance(body, dict):
            body_str = json.dumps(body, ensure_ascii=False)
        else:
            body_str = str(body)

        if len(body_str) > self.max_body_length:
            return body_str[: self.max_body_length] + "... (truncated)"

        return body

    def _truncate_dict(self, data: dict[str, Any]) -> dict[str, Any]:
        """截断字典中的长值"""
        result = {}
        for key, value in data.items():
            if isinstance(value, str) and len(value) > 200:
                result[key] = value[:200] + "..."
            else:
                result[key] = value
        return result


# 全局调试器实例
_global_debugger: HTTPDebugger | None = None


def enable_http_debug(max_body_length: int = 1000) -> HTTPDebugger:
    """启用全局HTTP调试

    Args:
        max_body_length: 最大记录的body长度

    Returns:
        HTTPDebugger: 调试器实例

    Example:
        >>> debugger = enable_http_debug()
        >>> # 执行测试
        >>> debugger.print_summary()
    """
    global _global_debugger
    if _global_debugger is None:
        _global_debugger = HTTPDebugger(enabled=True, max_body_length=max_body_length)
    else:
        _global_debugger.start()
    return _global_debugger


def disable_http_debug():
    """禁用全局HTTP调试"""
    global _global_debugger
    if _global_debugger:
        _global_debugger.stop()


def get_global_debugger() -> HTTPDebugger | None:
    """获取全局调试器实例"""
    return _global_debugger


__all__ = [
    "HTTPDebugger",
    "enable_http_debug",
    "disable_http_debug",
    "get_global_debugger",
]
