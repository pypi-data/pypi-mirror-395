"""测试 resilience.py - 熔断器功能

测试覆盖:
- 熔断器基础功能(状态转换、失败计数)
- 熔断触发机制(连续失败N次)
- 熔断恢复机制(超时后HALF_OPEN状态)
- 装饰器使用
- 异常白名单
- 线程安全
- 边界条件
- 错误处理
"""

import threading
import time

import pytest

from df_test_framework.utils.resilience import (
    CircuitBreaker,
    CircuitOpenError,
    CircuitState,
    circuit_breaker,
)


class TestCircuitBreakerBasic:
    """测试熔断器基础功能"""

    def test_initial_state_is_closed(self):
        """测试初始状态为CLOSED"""
        breaker = CircuitBreaker()
        assert breaker.state == CircuitState.CLOSED
        assert breaker.is_closed
        assert not breaker.is_open
        assert not breaker.is_half_open

    def test_successful_call(self):
        """测试成功调用"""
        breaker = CircuitBreaker()

        def success_func():
            return "success"

        result = breaker.call(success_func)
        assert result == "success"
        assert breaker.state == CircuitState.CLOSED
        assert breaker.failure_count == 0

    def test_failed_call_increments_failure_count(self):
        """测试失败调用增加失败计数"""
        breaker = CircuitBreaker(failure_threshold=5)

        def failing_func():
            raise RuntimeError("失败")

        # 第一次失败
        with pytest.raises(RuntimeError):
            breaker.call(failing_func)

        assert breaker.failure_count == 1
        assert breaker.state == CircuitState.CLOSED

        # 第二次失败
        with pytest.raises(RuntimeError):
            breaker.call(failing_func)

        assert breaker.failure_count == 2
        assert breaker.state == CircuitState.CLOSED

    def test_call_with_args_and_kwargs(self):
        """测试带参数调用"""
        breaker = CircuitBreaker()

        def add_numbers(a, b, c=0):
            return a + b + c

        result = breaker.call(add_numbers, 1, 2, c=3)
        assert result == 6


class TestCircuitBreakerStateTransitions:
    """测试熔断器状态转换"""

    def test_closed_to_open_on_failure_threshold(self):
        """测试连续失败达到阈值后转为OPEN"""
        breaker = CircuitBreaker(failure_threshold=3)

        def failing_func():
            raise RuntimeError("失败")

        # 连续失败3次
        for i in range(3):
            with pytest.raises(RuntimeError):
                breaker.call(failing_func)

        # 验证状态转为OPEN
        assert breaker.state == CircuitState.OPEN
        assert breaker.is_open
        assert breaker.failure_count == 3

    def test_open_circuit_blocks_calls(self):
        """测试OPEN状态阻止调用"""
        breaker = CircuitBreaker(failure_threshold=2, timeout=10)

        def failing_func():
            raise RuntimeError("失败")

        # 触发熔断
        for i in range(2):
            with pytest.raises(RuntimeError):
                breaker.call(failing_func)

        assert breaker.state == CircuitState.OPEN

        # 验证阻止调用
        with pytest.raises(CircuitOpenError, match="熔断器已打开"):
            breaker.call(lambda: "should not execute")

    def test_open_to_half_open_after_timeout(self):
        """测试超时后转为HALF_OPEN状态"""
        breaker = CircuitBreaker(failure_threshold=2, timeout=1)

        def failing_func():
            raise RuntimeError("失败")

        # 触发熔断
        for i in range(2):
            with pytest.raises(RuntimeError):
                breaker.call(failing_func)

        assert breaker.state == CircuitState.OPEN

        # 等待超时
        time.sleep(1.1)

        # 下次调用应该转为HALF_OPEN
        result = breaker.call(lambda: "success")
        assert result == "success"
        assert breaker.state == CircuitState.HALF_OPEN

    def test_half_open_to_closed_on_success(self):
        """测试HALF_OPEN状态连续成功后转为CLOSED"""
        breaker = CircuitBreaker(failure_threshold=2, success_threshold=2, timeout=1)

        def failing_func():
            raise RuntimeError("失败")

        # 触发熔断
        for i in range(2):
            with pytest.raises(RuntimeError):
                breaker.call(failing_func)

        assert breaker.state == CircuitState.OPEN

        # 等待超时
        time.sleep(1.1)

        # 第一次成功 -> HALF_OPEN
        breaker.call(lambda: "success1")
        assert breaker.state == CircuitState.HALF_OPEN
        assert breaker.success_count == 1

        # 第二次成功 -> CLOSED
        breaker.call(lambda: "success2")
        assert breaker.state == CircuitState.CLOSED
        assert breaker.success_count == 0

    def test_half_open_to_open_on_failure(self):
        """测试HALF_OPEN状态失败后重新打开"""
        breaker = CircuitBreaker(failure_threshold=2, timeout=1)

        def failing_func():
            raise RuntimeError("失败")

        # 触发熔断
        for i in range(2):
            with pytest.raises(RuntimeError):
                breaker.call(failing_func)

        assert breaker.state == CircuitState.OPEN

        # 等待超时
        time.sleep(1.1)

        # 半开状态失败
        with pytest.raises(RuntimeError):
            breaker.call(failing_func)

        # 应该重新打开
        assert breaker.state == CircuitState.OPEN


class TestCircuitBreakerExceptionWhitelist:
    """测试异常白名单"""

    def test_whitelist_exceptions_not_counted_as_failure(self):
        """测试白名单异常不计入失败"""
        breaker = CircuitBreaker(failure_threshold=3, exception_whitelist=(ValueError, TypeError))

        # ValueError 不计入失败
        with pytest.raises(ValueError):
            breaker.call(lambda: (_ for _ in ()).throw(ValueError("test")))

        assert breaker.failure_count == 0
        assert breaker.state == CircuitState.CLOSED

        # TypeError 不计入失败
        with pytest.raises(TypeError):
            breaker.call(lambda: (_ for _ in ()).throw(TypeError("test")))

        assert breaker.failure_count == 0

        # RuntimeError 计入失败
        with pytest.raises(RuntimeError):
            breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("test")))

        assert breaker.failure_count == 1

    def test_whitelist_multiple_exception_types(self):
        """测试多种白名单异常类型"""
        breaker = CircuitBreaker(
            failure_threshold=2,
            exception_whitelist=(ValueError, TypeError, KeyError),
        )

        # 所有白名单异常都不计入失败
        exceptions = [ValueError("v"), TypeError("t"), KeyError("k")]

        for exc in exceptions:
            with pytest.raises(type(exc)):
                breaker.call(lambda: (_ for _ in ()).throw(exc))

        assert breaker.failure_count == 0
        assert breaker.state == CircuitState.CLOSED


class TestCircuitBreakerReset:
    """测试熔断器重置"""

    def test_manual_reset(self):
        """测试手动重置熔断器"""
        breaker = CircuitBreaker(failure_threshold=2)

        # 触发熔断
        for i in range(2):
            with pytest.raises(RuntimeError):
                breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("fail")))

        assert breaker.state == CircuitState.OPEN
        assert breaker.failure_count == 2

        # 手动重置
        breaker.reset()

        assert breaker.state == CircuitState.CLOSED
        assert breaker.failure_count == 0
        assert breaker.success_count == 0
        assert breaker.last_failure_time is None

    def test_success_resets_failure_count(self):
        """测试成功调用重置失败计数"""
        breaker = CircuitBreaker(failure_threshold=3)

        # 失败2次
        for i in range(2):
            with pytest.raises(RuntimeError):
                breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("fail")))

        assert breaker.failure_count == 2

        # 成功1次
        breaker.call(lambda: "success")

        # 失败计数应该重置
        assert breaker.failure_count == 0
        assert breaker.state == CircuitState.CLOSED


class TestCircuitBreakerDecorator:
    """测试熔断器装饰器"""

    def test_decorator_basic_usage(self):
        """测试装饰器基本使用"""

        @circuit_breaker(failure_threshold=2, timeout=1)
        def protected_func():
            return "success"

        result = protected_func()
        assert result == "success"

    def test_decorator_triggers_circuit(self):
        """测试装饰器触发熔断"""

        @circuit_breaker(failure_threshold=2, timeout=10)
        def failing_func():
            raise RuntimeError("失败")

        # 触发熔断
        for i in range(2):
            with pytest.raises(RuntimeError):
                failing_func()

        # 验证熔断
        with pytest.raises(CircuitOpenError):
            failing_func()

    def test_decorator_with_arguments(self):
        """测试装饰器保留函数参数"""

        @circuit_breaker(failure_threshold=3)
        def add(a, b):
            return a + b

        result = add(2, 3)
        assert result == 5

    def test_decorator_preserves_function_metadata(self):
        """测试装饰器保留函数元数据"""

        @circuit_breaker()
        def documented_func():
            """这是一个有文档的函数"""
            pass

        assert documented_func.__name__ == "documented_func"
        assert documented_func.__doc__ == "这是一个有文档的函数"

    def test_decorator_breaker_attribute(self):
        """测试装饰器附加的breaker属性"""

        @circuit_breaker(failure_threshold=3)
        def func():
            return "ok"

        # 验证breaker属性存在
        assert hasattr(func, "breaker")
        assert isinstance(func.breaker, CircuitBreaker)
        assert func.breaker.failure_threshold == 3


class TestCircuitBreakerThreadSafety:
    """测试熔断器线程安全"""

    def test_concurrent_calls(self):
        """测试并发调用的线程安全性"""
        breaker = CircuitBreaker(failure_threshold=10)
        success_count = [0]
        lock = threading.Lock()

        def safe_increment():
            with lock:
                success_count[0] += 1
            return "success"

        def concurrent_call():
            try:
                breaker.call(safe_increment)
            except Exception:
                pass

        # 创建10个线程并发调用
        threads = [threading.Thread(target=concurrent_call) for _ in range(10)]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        # 验证所有调用都成功
        assert success_count[0] == 10
        assert breaker.failure_count == 0


class TestCircuitBreakerEdgeCases:
    """测试边界条件"""

    def test_invalid_failure_threshold(self):
        """测试无效的失败阈值"""
        with pytest.raises(ValueError, match="failure_threshold必须大于0"):
            CircuitBreaker(failure_threshold=0)

        with pytest.raises(ValueError, match="failure_threshold必须大于0"):
            CircuitBreaker(failure_threshold=-1)

    def test_invalid_success_threshold(self):
        """测试无效的成功阈值"""
        with pytest.raises(ValueError, match="success_threshold必须大于0"):
            CircuitBreaker(success_threshold=0)

    def test_invalid_timeout(self):
        """测试无效的超时时间"""
        with pytest.raises(ValueError, match="timeout必须大于0"):
            CircuitBreaker(timeout=0)

        with pytest.raises(ValueError, match="timeout必须大于0"):
            CircuitBreaker(timeout=-1)

    def test_get_reset_time_before_failure(self):
        """测试未失败前获取重置时间"""
        breaker = CircuitBreaker()
        # last_failure_time为None时应该返回"未知"
        assert breaker._get_reset_time() == "未知"

    def test_get_reset_time_after_timeout(self):
        """测试超时后获取重置时间"""
        breaker = CircuitBreaker(failure_threshold=1, timeout=1)

        # 触发失败
        with pytest.raises(RuntimeError):
            breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("fail")))

        # 等待超时
        time.sleep(1.1)

        # 应该返回"即将恢复"
        assert breaker._get_reset_time() == "即将恢复"


class TestCircuitBreakerIntegration:
    """测试熔断器集成场景"""

    def test_realistic_api_call_scenario(self):
        """测试真实的API调用场景"""
        breaker = CircuitBreaker(failure_threshold=3, timeout=2)

        # 模拟API调用
        api_call_count = [0]

        def mock_api_call():
            api_call_count[0] += 1
            if api_call_count[0] <= 3:
                raise RuntimeError("API服务故障")
            return {"status": "ok"}

        # 前3次失败，触发熔断
        for i in range(3):
            with pytest.raises(RuntimeError):
                breaker.call(mock_api_call)

        assert breaker.state == CircuitState.OPEN
        assert api_call_count[0] == 3

        # 熔断期间调用被阻止
        with pytest.raises(CircuitOpenError):
            breaker.call(mock_api_call)

        # API没有被调用
        assert api_call_count[0] == 3

        # 等待超时
        time.sleep(2.1)

        # 恢复后成功
        result = breaker.call(mock_api_call)
        assert result == {"status": "ok"}
        assert api_call_count[0] == 4

    def test_partial_recovery_scenario(self):
        """测试部分恢复场景"""
        breaker = CircuitBreaker(failure_threshold=2, success_threshold=3, timeout=1)

        # 触发熔断
        for i in range(2):
            with pytest.raises(RuntimeError):
                breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("fail")))

        assert breaker.state == CircuitState.OPEN

        # 等待超时
        time.sleep(1.1)

        # 半开状态成功2次
        breaker.call(lambda: "success1")
        assert breaker.state == CircuitState.HALF_OPEN

        breaker.call(lambda: "success2")
        assert breaker.state == CircuitState.HALF_OPEN
        assert breaker.success_count == 2

        # 第3次才完全恢复
        breaker.call(lambda: "success3")
        assert breaker.state == CircuitState.CLOSED
        assert breaker.success_count == 0


__all__ = [
    "TestCircuitBreakerBasic",
    "TestCircuitBreakerStateTransitions",
    "TestCircuitBreakerExceptionWhitelist",
    "TestCircuitBreakerReset",
    "TestCircuitBreakerDecorator",
    "TestCircuitBreakerThreadSafety",
    "TestCircuitBreakerEdgeCases",
    "TestCircuitBreakerIntegration",
]
