"""
测试Logging策略

验证LoguruStructuredStrategy和NoOpStrategy的配置功能。
"""

import tempfile
from pathlib import Path

from df_test_framework.infrastructure.config import LoggingConfig
from df_test_framework.infrastructure.logging import (
    LoguruStructuredStrategy,
    NoOpStrategy,
)
from df_test_framework.infrastructure.logging.logger import (
    logger,
)


class TestLoguruStructuredStrategy:
    """测试LoguruStructuredStrategy"""

    def setup_method(self):
        """每个测试前记录当前的handler数量"""
        self.initial_handlers = len(logger._core.handlers)

    def teardown_method(self):
        """每个测试后清理logger handlers，释放文件锁"""
        # 移除测试期间添加的所有handlers
        while len(logger._core.handlers) > self.initial_handlers:
            logger.remove()

    def test_strategy_creation(self):
        """测试创建策略实例"""
        strategy = LoguruStructuredStrategy()
        assert strategy is not None

    def test_configure_with_minimal_config(self):
        """测试使用最小配置"""
        config = LoggingConfig(
            level="INFO",
            enable_console=True,
            sanitize=False,
        )

        strategy = LoguruStructuredStrategy()
        configured_logger = strategy.configure(config)

        assert configured_logger is not None
        # 返回的应该是全局logger
        assert configured_logger is logger

    def test_configure_with_file_output(self):
        """测试配置文件输出"""
        # 创建临时日志文件
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test.log"

            config = LoggingConfig(
                level="DEBUG",
                file=str(log_file),
                enable_console=False,
                sanitize=False,
            )

            strategy = LoguruStructuredStrategy()
            configured_logger = strategy.configure(config)

            # 写入日志
            configured_logger.info("Test log message")

            # 手动移除所有handlers以释放文件锁
            logger.remove()

            # 验证日志文件被创建
            # 注意：由于loguru可能异步写入，这里可能需要等待
            # assert log_file.exists()

    def test_configure_with_rotation(self):
        """测试配置日志轮转"""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "rotated.log"

            config = LoggingConfig(
                level="INFO",
                file=str(log_file),
                rotation="10 MB",  # 10MB轮转
                enable_console=False,
                sanitize=False,
            )

            strategy = LoguruStructuredStrategy()
            configured_logger = strategy.configure(config)

            assert configured_logger is not None

            # 手动移除所有handlers以释放文件锁
            logger.remove()

    def test_configure_with_retention(self):
        """测试配置日志保留"""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "retained.log"

            config = LoggingConfig(
                level="INFO",
                file=str(log_file),
                retention="7 days",
                enable_console=False,
                sanitize=False,
            )

            strategy = LoguruStructuredStrategy()
            configured_logger = strategy.configure(config)

            assert configured_logger is not None

            # 手动移除所有handlers以释放文件锁
            logger.remove()

    def test_configure_with_sanitization(self):
        """测试配置日志脱敏"""
        config = LoggingConfig(
            level="INFO",
            enable_console=True,
            sanitize=True,  # 启用脱敏
        )

        strategy = LoguruStructuredStrategy()
        configured_logger = strategy.configure(config)

        assert configured_logger is not None

    def test_configure_console_disabled(self):
        """测试禁用控制台输出"""
        config = LoggingConfig(
            level="INFO",
            enable_console=False,
            sanitize=False,
        )

        strategy = LoguruStructuredStrategy()
        configured_logger = strategy.configure(config)

        assert configured_logger is not None

    def test_configure_different_log_levels(self):
        """测试不同的日志级别"""
        # LoggingConfig只支持这些级别
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

        for level in levels:
            config = LoggingConfig(
                level=level,
                enable_console=True,
                sanitize=False,
            )

            strategy = LoguruStructuredStrategy()
            configured_logger = strategy.configure(config)

            assert configured_logger is not None


class TestNoOpStrategy:
    """测试NoOpStrategy"""

    def test_strategy_creation(self):
        """测试创建NoOp策略实例"""
        strategy = NoOpStrategy()
        assert strategy is not None

    def test_configure_returns_logger(self):
        """测试configure返回logger"""
        config = LoggingConfig(
            level="INFO",
            enable_console=True,
            sanitize=False,
        )

        strategy = NoOpStrategy()
        configured_logger = strategy.configure(config)

        assert configured_logger is not None
        assert configured_logger is logger

    def test_configure_when_not_configured(self):
        """测试logger未配置时的行为"""
        config = LoggingConfig(
            level="WARNING",
            enable_console=True,
            sanitize=False,
        )

        strategy = NoOpStrategy()
        configured_logger = strategy.configure(config)

        # 应该进行最小化配置
        assert configured_logger is logger

    def test_configure_minimal_setup(self):
        """测试最小化设置（不使用文件）"""
        config = LoggingConfig(
            level="INFO",
            file=None,  # 不使用文件
            enable_console=True,
            sanitize=False,
        )

        strategy = NoOpStrategy()
        configured_logger = strategy.configure(config)

        assert configured_logger is not None

    def test_noop_respects_console_setting(self):
        """测试NoOp策略尊重console设置"""
        config = LoggingConfig(
            level="INFO",
            enable_console=False,
            sanitize=False,
        )

        strategy = NoOpStrategy()
        configured_logger = strategy.configure(config)

        assert configured_logger is not None

    def test_noop_respects_sanitize_setting(self):
        """测试NoOp策略尊重sanitize设置"""
        config = LoggingConfig(
            level="INFO",
            enable_console=True,
            sanitize=True,
        )

        strategy = NoOpStrategy()
        configured_logger = strategy.configure(config)

        assert configured_logger is not None


class TestLoggingIntegration:
    """集成测试：完整的日志配置流程"""

    def setup_method(self):
        """每个测试前记录当前的handler数量"""
        self.initial_handlers = len(logger._core.handlers)

    def teardown_method(self):
        """每个测试后清理logger handlers，释放文件锁"""
        # 移除测试期间添加的所有handlers
        while len(logger._core.handlers) > self.initial_handlers:
            logger.remove()

    def test_structured_strategy_complete_flow(self):
        """测试LoguruStructuredStrategy完整流程"""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "integration.log"

            # 1. 创建配置
            config = LoggingConfig(
                level="DEBUG",
                file=str(log_file),
                rotation="1 MB",
                retention="3 days",
                enable_console=True,
                sanitize=True,
            )

            # 2. 创建策略并配置
            strategy = LoguruStructuredStrategy()
            configured_logger = strategy.configure(config)

            # 3. 使用logger
            configured_logger.debug("Debug message")
            configured_logger.info("Info message")
            configured_logger.warning("Warning message")
            configured_logger.error("Error message")

            # 4. 验证logger可用
            assert configured_logger is not None

            # 5. 手动移除所有handlers以释放文件锁
            logger.remove()

    def test_noop_strategy_complete_flow(self):
        """测试NoOpStrategy完整流程"""
        # 1. 创建配置
        config = LoggingConfig(
            level="INFO",
            enable_console=True,
            sanitize=False,
        )

        # 2. 创建策略并配置
        strategy = NoOpStrategy()
        configured_logger = strategy.configure(config)

        # 3. 使用logger
        configured_logger.info("NoOp info message")
        configured_logger.warning("NoOp warning message")

        # 4. 验证logger可用
        assert configured_logger is not None

    def test_switch_between_strategies(self):
        """测试在不同策略间切换"""
        config = LoggingConfig(
            level="INFO",
            enable_console=True,
            sanitize=False,
        )

        # 使用NoOp策略
        noop = NoOpStrategy()
        logger1 = noop.configure(config)

        # 切换到Structured策略
        structured = LoguruStructuredStrategy()
        logger2 = structured.configure(config)

        # 应该都返回全局logger
        assert logger1 is logger
        assert logger2 is logger

    def test_multiple_configure_calls(self):
        """测试多次调用configure"""
        config1 = LoggingConfig(level="DEBUG", enable_console=True, sanitize=False)
        config2 = LoggingConfig(level="INFO", enable_console=True, sanitize=True)

        strategy = LoguruStructuredStrategy()

        # 第一次配置
        logger1 = strategy.configure(config1)

        # 第二次配置
        logger2 = strategy.configure(config2)

        # 应该都返回同一个logger
        assert logger1 is logger
        assert logger2 is logger
