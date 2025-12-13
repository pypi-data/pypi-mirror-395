"""constants/error_codes.py 常量模块模板"""

CONSTANTS_ERROR_CODES_TEMPLATE = """\"\"\"错误码常量定义

定义项目中使用的错误码常量。
\"\"\"

# 成功码
SUCCESS = 200

# 客户端错误 (4xx)
BAD_REQUEST = 400
UNAUTHORIZED = 401
FORBIDDEN = 403
NOT_FOUND = 404
METHOD_NOT_ALLOWED = 405
CONFLICT = 409
UNPROCESSABLE_ENTITY = 422

# 服务器错误 (5xx)
INTERNAL_SERVER_ERROR = 500
SERVICE_UNAVAILABLE = 503
GATEWAY_TIMEOUT = 504

# 业务错误码（示例）
USER_NOT_FOUND = 10001
USER_ALREADY_EXISTS = 10002
INVALID_PASSWORD = 10003
TOKEN_EXPIRED = 10004
PERMISSION_DENIED = 10005

# 错误码描述映射
ERROR_MESSAGES = {
    SUCCESS: "成功",
    BAD_REQUEST: "请求参数错误",
    UNAUTHORIZED: "未授权",
    FORBIDDEN: "禁止访问",
    NOT_FOUND: "资源不存在",
    USER_NOT_FOUND: "用户不存在",
    USER_ALREADY_EXISTS: "用户已存在",
    INVALID_PASSWORD: "密码错误",
    TOKEN_EXPIRED: "Token已过期",
    PERMISSION_DENIED: "权限不足",
}


def get_error_message(code: int) -> str:
    \"\"\"获取错误码对应的描述

    Args:
        code: 错误码

    Returns:
        str: 错误描述
    \"\"\"
    return ERROR_MESSAGES.get(code, f"未知错误({code})")


__all__ = [
    "SUCCESS",
    "BAD_REQUEST",
    "UNAUTHORIZED",
    "FORBIDDEN",
    "NOT_FOUND",
    "USER_NOT_FOUND",
    "USER_ALREADY_EXISTS",
    "INVALID_PASSWORD",
    "TOKEN_EXPIRED",
    "PERMISSION_DENIED",
    "ERROR_MESSAGES",
    "get_error_message",
]
"""

__all__ = ["CONSTANTS_ERROR_CODES_TEMPLATE"]
