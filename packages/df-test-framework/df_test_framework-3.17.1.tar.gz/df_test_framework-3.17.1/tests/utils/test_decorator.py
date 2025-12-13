"""装饰器工具单元测试"""

import time

import pytest

from df_test_framework.utils.decorator import (
    cache_result,
    deprecated,
    log_execution,
    retry_on_failure,
)


class TestRetryOnFailure:
    """retry_on_failure 装饰器测试"""

    def test_success_no_retry(self):
        """测试成功时不重试"""
        call_count = 0

        @retry_on_failure(max_retries=3)
        def always_success():
            nonlocal call_count
            call_count += 1
            return "success"

        result = always_success()
        assert result == "success"
        assert call_count == 1

    def test_retry_then_success(self):
        """测试重试后成功"""
        call_count = 0

        @retry_on_failure(max_retries=3, delay=0.01, backoff=1)
        def fail_twice():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Temporary failure")
            return "success"

        result = fail_twice()
        assert result == "success"
        assert call_count == 3

    def test_max_retries_exceeded(self):
        """测试超过最大重试次数"""
        call_count = 0

        @retry_on_failure(max_retries=2, delay=0.01, backoff=1)
        def always_fail():
            nonlocal call_count
            call_count += 1
            raise ValueError("Always fails")

        with pytest.raises(ValueError, match="Always fails"):
            always_fail()

        assert call_count == 3  # 1次初始 + 2次重试

    def test_specific_exception(self):
        """测试只捕获特定异常"""
        call_count = 0

        @retry_on_failure(max_retries=3, delay=0.01, exceptions=(ValueError,))
        def raise_type_error():
            nonlocal call_count
            call_count += 1
            raise TypeError("Not caught")

        with pytest.raises(TypeError):
            raise_type_error()

        assert call_count == 1  # 不重试

    def test_backoff_delay(self):
        """测试指数退避延迟"""
        call_count = 0
        start_time = time.time()

        @retry_on_failure(max_retries=2, delay=0.05, backoff=2)
        def fail_then_success():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Fail")
            return "success"

        result = fail_then_success()
        elapsed = time.time() - start_time

        assert result == "success"
        # 预期延迟: 0.05 + 0.1 = 0.15 秒
        assert elapsed >= 0.1  # 至少有一些延迟


class TestLogExecution:
    """log_execution 装饰器测试"""

    def test_log_execution_basic(self, caplog):
        """测试基本执行日志"""
        import logging

        caplog.set_level(logging.DEBUG)

        @log_execution()
        def simple_func():
            return "result"

        result = simple_func()
        assert result == "result"

    def test_log_args(self):
        """测试记录参数"""

        @log_execution(log_args=True)
        def func_with_args(a, b, c=None):
            return a + b

        result = func_with_args(1, 2, c=3)
        assert result == 3

    def test_log_result(self):
        """测试记录返回值"""

        @log_execution(log_result=True)
        def func_with_result():
            return {"data": "value"}

        result = func_with_result()
        assert result == {"data": "value"}

    def test_log_exception(self):
        """测试记录异常"""

        @log_execution()
        def raise_error():
            raise RuntimeError("Test error")

        with pytest.raises(RuntimeError, match="Test error"):
            raise_error()


class TestDeprecated:
    """deprecated 装饰器测试"""

    def test_deprecated_basic(self):
        """测试基本废弃警告"""

        @deprecated()
        def old_func():
            return "old"

        result = old_func()
        assert result == "old"

    def test_deprecated_with_message(self):
        """测试带消息的废弃警告"""

        @deprecated(message="请使用 new_func")
        def old_func():
            return "old"

        result = old_func()
        assert result == "old"

    def test_deprecated_with_version(self):
        """测试带版本的废弃警告"""

        @deprecated(version="2.0.0")
        def old_func():
            return "old"

        result = old_func()
        assert result == "old"

    def test_deprecated_with_all(self):
        """测试完整废弃警告"""

        @deprecated(message="Use new_func instead", version="3.0.0")
        def old_func():
            return "old"

        result = old_func()
        assert result == "old"


class TestCacheResult:
    """cache_result 装饰器测试"""

    def test_cache_basic(self):
        """测试基本缓存功能"""
        call_count = 0

        @cache_result()
        def expensive_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        # 首次调用
        result1 = expensive_func(5)
        assert result1 == 10
        assert call_count == 1

        # 缓存命中
        result2 = expensive_func(5)
        assert result2 == 10
        assert call_count == 1  # 不增加

        # 不同参数
        result3 = expensive_func(10)
        assert result3 == 20
        assert call_count == 2

    def test_cache_with_kwargs(self):
        """测试带关键字参数的缓存"""
        call_count = 0

        @cache_result()
        def func_with_kwargs(a, b=1):
            nonlocal call_count
            call_count += 1
            return a + b

        result1 = func_with_kwargs(1, b=2)
        result2 = func_with_kwargs(1, b=2)

        assert result1 == result2 == 3
        assert call_count == 1

    def test_cache_ttl_expiry(self):
        """测试 TTL 过期"""
        call_count = 0

        @cache_result(ttl=0.1)
        def ttl_func(x):
            nonlocal call_count
            call_count += 1
            return x

        # 首次调用
        ttl_func(1)
        assert call_count == 1

        # 立即调用（缓存命中）
        ttl_func(1)
        assert call_count == 1

        # 等待过期
        time.sleep(0.15)

        # 过期后调用
        ttl_func(1)
        assert call_count == 2

    def test_cache_maxsize(self):
        """测试最大缓存大小"""
        call_count = 0

        @cache_result(maxsize=2)
        def sized_func(x):
            nonlocal call_count
            call_count += 1
            return x

        # 填满缓存
        sized_func(1)  # call_count = 1
        sized_func(2)  # call_count = 2

        # 添加第三个，淘汰第一个
        sized_func(3)  # call_count = 3

        # 再次调用第一个，需要重新计算
        sized_func(1)  # call_count = 4
        assert call_count == 4

    def test_cache_clear(self):
        """测试清除缓存"""
        call_count = 0

        @cache_result()
        def clearable_func(x):
            nonlocal call_count
            call_count += 1
            return x

        clearable_func(1)
        clearable_func(1)  # 缓存命中
        assert call_count == 1

        # 清除缓存
        clearable_func.clear_cache()

        clearable_func(1)  # 重新计算
        assert call_count == 2

    def test_cache_info(self):
        """测试缓存信息"""

        @cache_result(maxsize=10, ttl=60)
        def info_func(x):
            return x

        info_func(1)
        info_func(2)

        info = info_func.cache_info()
        assert info["size"] == 2
        assert info["maxsize"] == 10
        assert info["ttl"] == 60


class TestDecoratorPreservation:
    """测试装饰器保留函数元信息"""

    def test_retry_preserves_name(self):
        """测试 retry 保留函数名"""

        @retry_on_failure()
        def my_func():
            pass

        assert my_func.__name__ == "my_func"

    def test_log_preserves_name(self):
        """测试 log_execution 保留函数名"""

        @log_execution()
        def my_func():
            pass

        assert my_func.__name__ == "my_func"

    def test_deprecated_preserves_name(self):
        """测试 deprecated 保留函数名"""

        @deprecated()
        def my_func():
            pass

        assert my_func.__name__ == "my_func"

    def test_cache_preserves_name(self):
        """测试 cache_result 保留函数名"""

        @cache_result()
        def my_func():
            pass

        assert my_func.__name__ == "my_func"
