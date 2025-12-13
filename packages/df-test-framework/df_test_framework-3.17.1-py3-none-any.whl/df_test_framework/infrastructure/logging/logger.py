"""日志配置模块"""

import re
import sys
from pathlib import Path

from loguru import logger

_LOGGER_CONFIGURED = False


def sanitize_log(record: dict) -> bool:
    """
    敏感信息脱敏过滤器

    自动过滤日志中的敏感信息如密码、token、密钥等

    Args:
        record: loguru日志记录

    Returns:
        bool: 总是返回True以保留日志记录
    """
    # 敏感字段模式
    patterns = {
        "password": r'(password["\']?\s*[:=]\s*["\']?)([^"\'}\s]+)',
        "token": r'(token["\']?\s*[:=]\s*["\']?)([^"\'}\s]+)',
        "secret": r'(secret["\']?\s*[:=]\s*["\']?)([^"\'}\s]+)',
        "key": r'(api[_-]?key["\']?\s*[:=]\s*["\']?)([^"\'}\s]+)',
        "authorization": r'(authorization["\']?\s*[:=]\s*["\']?)([^"\'}\s]+)',
    }

    message = record["message"]

    # 应用所有脱敏模式
    for key, pattern in patterns.items():
        message = re.sub(pattern, r"\1******", message, flags=re.IGNORECASE)

    record["message"] = message
    return True


def setup_logger(
    log_level: str = "INFO",
    log_file: str | None = None,
    rotation: str = "100 MB",
    retention: str = "7 days",
    enable_console: bool = True,
    enable_sanitize: bool = True,
) -> None:
    """
    配置全局日志

    Args:
        log_level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: 日志文件路径,如果为None则只输出到控制台
        rotation: 日志轮转大小
        retention: 日志保留时间
        enable_console: 是否启用控制台输出
        enable_sanitize: 是否启用敏感信息脱敏
    """
    global _LOGGER_CONFIGURED

    # 移除默认handler
    logger.remove()

    # 控制台输出 - 带颜色
    if enable_console:
        logger.add(
            sys.stdout,
            level=log_level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan> | "
            "<level>{message}</level>",
            colorize=True,
            filter=sanitize_log if enable_sanitize else None,
        )

    # 文件输出 - 如果指定了文件路径
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # 常规日志文件
        logger.add(
            log_file,
            level=log_level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
            "{name}:{function}:{line} | {message}",
            rotation=rotation,
            retention=retention,
            compression="zip",  # 压缩旧日志
            encoding="utf-8",
            enqueue=True,  # 异步写入
            filter=sanitize_log if enable_sanitize else None,
        )

        # 错误日志单独文件
        error_log_file = log_path.parent / "error.log"
        logger.add(
            str(error_log_file),
            level="ERROR",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
            "{name}:{function}:{line} | {message}\n{exception}",
            rotation=rotation,
            retention=retention,
            compression="zip",
            encoding="utf-8",
            enqueue=True,
            backtrace=True,  # 完整堆栈跟踪
            diagnose=True,  # 变量诊断
            filter=sanitize_log if enable_sanitize else None,
        )

        logger.info(f"日志系统已初始化: {log_file}")

    _LOGGER_CONFIGURED = True


def is_logger_configured() -> bool:
    """
    判断是否已经由框架显式配置过日志.

    Returns:
        bool: True表示调用过setup_logger并替换了默认handler
    """
    return _LOGGER_CONFIGURED


__all__ = ["setup_logger", "is_logger_configured", "logger"]
