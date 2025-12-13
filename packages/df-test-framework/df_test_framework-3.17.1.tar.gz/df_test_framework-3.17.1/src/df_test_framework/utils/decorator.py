"""装饰器工具集"""

import time
from collections.abc import Callable
from functools import wraps
from typing import Any

from loguru import logger


def retry_on_failure(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
):
    """
    失败重试装饰器

    当函数抛出指定异常时自动重试

    Args:
        max_retries: 最大重试次数
        delay: 初始延迟时间(秒)
        backoff: 延迟倍数(指数退避)
        exceptions: 需要重试的异常类型元组

    Returns:
        装饰器函数

    Example:
        @retry_on_failure(max_retries=3, delay=1, backoff=2)
        def unstable_api_call():
            return requests.get("https://api.example.com/data")
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries:
                        logger.error(f"{func.__name__} 重试{max_retries}次后仍然失败: {str(e)}")
                        raise

                    logger.warning(
                        f"{func.__name__} 第{attempt + 1}次失败,{current_delay}秒后重试: {str(e)}"
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff

        return wrapper

    return decorator


# timeout装饰器已移除
# Windows平台不支持signal.SIGALRM,建议使用以下替代方案:
#
# 方案1: 使用pytest-timeout插件(推荐)
#   安装: pip install pytest-timeout
#   使用: pytest --timeout=30  # 全局30秒超时
#   或在pytest.ini中配置: timeout = 30
#
# 方案2: 使用@pytest.mark.timeout装饰器
#   @pytest.mark.timeout(10)
#   def test_something():
#       pass
#
# 方案3: 使用threading.Timer实现跨平台超时(如有需要)
#   from threading import Timer, Event
#   def timeout_wrapper(seconds):
#       # 自行实现基于线程的超时控制


def log_execution(log_args: bool = True, log_result: bool = False):
    """
    记录函数执行的装饰器

    自动记录函数的调用参数和返回值

    Args:
        log_args: 是否记录参数
        log_result: 是否记录返回值

    Returns:
        装饰器函数

    Example:
        @log_execution(log_args=True, log_result=True)
        def process_data(data):
            return data * 2
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__

            # 记录调用
            if log_args:
                logger.debug(f"[执行] {func_name} - args={args}, kwargs={kwargs}")
            else:
                logger.debug(f"[执行] {func_name}")

            try:
                result = func(*args, **kwargs)

                # 记录结果
                if log_result:
                    logger.debug(f"[完成] {func_name} - result={result}")
                else:
                    logger.debug(f"[完成] {func_name}")

                return result

            except Exception as e:
                logger.error(f"[失败] {func_name} - error={str(e)}")
                raise

        return wrapper

    return decorator


def deprecated(message: str | None = None, version: str | None = None):
    """
    标记函数为已废弃

    调用时会记录警告日志

    Args:
        message: 废弃原因或替代方法说明
        version: 废弃版本号

    Returns:
        装饰器函数

    Example:
        @deprecated(message="请使用new_function替代", version="2.0.0")
        def old_function():
            pass
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            warning_msg = f"函数 {func.__name__} 已废弃"

            if version:
                warning_msg += f" (自版本 {version})"

            if message:
                warning_msg += f": {message}"

            logger.warning(warning_msg)

            return func(*args, **kwargs)

        return wrapper

    return decorator


def cache_result(ttl: float | None = None, maxsize: int = 128):
    """
    缓存函数结果

    使用LRU(最近最少使用)策略的内存缓存,适用于重复计算的函数

    Args:
        ttl: 缓存过期时间(秒),None表示永不过期
        maxsize: 最大缓存条目数,超出后删除最旧的缓存

    Returns:
        装饰器函数

    Example:
        @cache_result(ttl=60, maxsize=100)
        def expensive_calculation(n):
            return sum(range(n))

    Note:
        如果不需要ttl和maxsize控制,可以直接使用functools.lru_cache:
        from functools import lru_cache
        @lru_cache(maxsize=128)
        def my_function(x):
            return x * 2
    """
    from collections import OrderedDict

    cache: OrderedDict[str, Any] = OrderedDict()  # 保持插入顺序
    cache_time: dict[str, float] = {}

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = str(args) + str(sorted(kwargs.items()))

            # 清理过期缓存
            if ttl is not None:
                expired_keys = [
                    key for key, timestamp in cache_time.items() if time.time() - timestamp >= ttl
                ]
                for key in expired_keys:
                    cache.pop(key, None)
                    cache_time.pop(key, None)
                if expired_keys:
                    logger.debug(f"[缓存清理] {func.__name__} 清理了{len(expired_keys)}个过期缓存")

            # 检查缓存是否存在且未过期
            if cache_key in cache:
                if ttl is None:
                    # 移到末尾(LRU策略)
                    cache.move_to_end(cache_key)
                    logger.debug(f"[缓存命中] {func.__name__}")
                    return cache[cache_key]
                else:
                    elapsed = time.time() - cache_time[cache_key]
                    if elapsed < ttl:
                        # 移到末尾(LRU策略)
                        cache.move_to_end(cache_key)
                        logger.debug(f"[缓存命中] {func.__name__} (剩余{ttl - elapsed:.1f}秒)")
                        return cache[cache_key]
                    else:
                        # 已过期,删除
                        del cache[cache_key]
                        del cache_time[cache_key]

            # 执行函数
            result = func(*args, **kwargs)

            # 检查缓存大小限制
            if len(cache) >= maxsize:
                # 删除最旧的缓存(FIFO)
                oldest_key = next(iter(cache))
                del cache[oldest_key]
                cache_time.pop(oldest_key, None)
                logger.debug(f"[缓存淘汰] {func.__name__} 缓存已满,淘汰最旧条目")

            # 添加到缓存
            cache[cache_key] = result
            cache_time[cache_key] = time.time()

            logger.debug(f"[缓存更新] {func.__name__} (当前缓存数: {len(cache)}/{maxsize})")

            return result

        # 添加清除缓存的方法
        def clear_cache():
            cache.clear()
            cache_time.clear()
            logger.info(f"[缓存清除] {func.__name__} 缓存已清空")

        # 添加获取缓存统计的方法
        def get_cache_info():
            return {"size": len(cache), "maxsize": maxsize, "ttl": ttl, "keys": list(cache.keys())}

        wrapper.clear_cache = clear_cache
        wrapper.cache_info = get_cache_info

        return wrapper

    return decorator


__all__ = [
    "retry_on_failure",
    # "timeout",  # 已移除,请使用pytest-timeout
    "log_execution",
    "deprecated",
    "cache_result",
]
