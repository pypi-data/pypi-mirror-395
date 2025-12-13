"""测试 cleanup.py - 测试数据清理模块

测试覆盖:
- should_keep_test_data 配置检查函数
- CleanupManager 清理管理器基类
- SimpleCleanupManager 回调函数模式清理器
- ListCleanup 列表式清理器

v3.11.1 重写测试
"""

from unittest.mock import Mock, patch

import pytest

from df_test_framework.testing.fixtures.cleanup import (
    CleanupManager,
    ListCleanup,
    SimpleCleanupManager,
    should_keep_test_data,
)

# ============================================================
# should_keep_test_data 测试
# ============================================================


class TestShouldKeepTestData:
    """测试 should_keep_test_data 函数"""

    @pytest.fixture
    def mock_request(self):
        """创建 mock request 对象"""
        request = Mock()
        request.node.get_closest_marker.return_value = None
        request.config.option = Mock()
        request.config.option.keep_test_data = False
        return request

    @pytest.fixture
    def mock_settings(self):
        """创建 mock settings 对象"""
        settings = Mock()
        settings.test = Mock()
        settings.test.keep_test_data = False
        return settings

    def test_returns_false_by_default(self, mock_request, mock_settings):
        """默认返回 False（执行清理）"""
        with patch(
            "df_test_framework.infrastructure.config.get_settings",
            return_value=mock_settings,
        ):
            result = should_keep_test_data(mock_request)
            assert result is False

    def test_returns_true_with_marker(self, mock_request):
        """检测到 @pytest.mark.keep_data 标记时返回 True"""
        mock_request.node.get_closest_marker.return_value = Mock()
        result = should_keep_test_data(mock_request)
        assert result is True

    def test_returns_true_with_cli_option(self, mock_request):
        """检测到 --keep-test-data 参数时返回 True"""
        mock_request.config.option.keep_test_data = True
        result = should_keep_test_data(mock_request)
        assert result is True

    def test_returns_true_with_settings_config(self, mock_request, mock_settings):
        """检测到 Settings 配置 keep_test_data=True 时返回 True"""
        mock_settings.test.keep_test_data = True
        with patch(
            "df_test_framework.infrastructure.config.get_settings",
            return_value=mock_settings,
        ):
            result = should_keep_test_data(mock_request)
            assert result is True

    def test_returns_false_with_settings_config_false(self, mock_request, mock_settings):
        """Settings 配置 keep_test_data=False 时返回 False"""
        mock_settings.test.keep_test_data = False
        with patch(
            "df_test_framework.infrastructure.config.get_settings",
            return_value=mock_settings,
        ):
            result = should_keep_test_data(mock_request)
            assert result is False

    def test_marker_has_highest_priority(self, mock_request, mock_settings):
        """标记优先级最高"""
        mock_request.node.get_closest_marker.return_value = Mock()
        mock_request.config.option.keep_test_data = False
        mock_settings.test.keep_test_data = False
        with patch(
            "df_test_framework.infrastructure.config.get_settings",
            return_value=mock_settings,
        ):
            result = should_keep_test_data(mock_request)
            assert result is True

    def test_cli_option_priority_over_settings(self, mock_request, mock_settings):
        """命令行参数优先级高于 Settings 配置"""
        mock_request.config.option.keep_test_data = True
        mock_settings.test.keep_test_data = False
        with patch(
            "df_test_framework.infrastructure.config.get_settings",
            return_value=mock_settings,
        ):
            result = should_keep_test_data(mock_request)
            assert result is True


# ============================================================
# CleanupManager 测试
# ============================================================


class ConcreteCleanupManager(CleanupManager):
    """CleanupManager 的具体实现，用于测试"""

    def __init__(self, request, db=None):
        super().__init__(request, db)
        self.cleanup_called = False
        self.cleanup_items = {}

    def _do_cleanup(self):
        """记录清理被调用"""
        self.cleanup_called = True
        self.cleanup_items = self.all_items()


class TestCleanupManager:
    """测试 CleanupManager 基类"""

    @pytest.fixture
    def mock_request(self):
        """创建 mock request 对象"""
        request = Mock()
        request.node.get_closest_marker.return_value = None
        request.config.option = Mock()
        request.config.option.keep_test_data = False
        return request

    @pytest.fixture
    def manager(self, mock_request):
        """创建测试用 manager 实例"""
        return ConcreteCleanupManager(mock_request)

    def test_init(self, mock_request):
        """测试初始化"""
        db = Mock()
        manager = ConcreteCleanupManager(mock_request, db)
        assert manager.db == db
        assert manager.all_items() == {}

    def test_add_single_item(self, manager):
        """测试添加单个项目"""
        manager.add("orders", "ORD001")
        assert manager.get_items("orders") == ["ORD001"]

    def test_add_multiple_items_same_type(self, manager):
        """测试添加多个同类型项目"""
        manager.add("orders", "ORD001")
        manager.add("orders", "ORD002")
        manager.add("orders", "ORD003")
        assert len(manager.get_items("orders")) == 3

    def test_add_different_types(self, manager):
        """测试添加不同类型的项目"""
        manager.add("orders", "ORD001")
        manager.add("payments", "PAY001")
        manager.add("users", "USER001")
        assert len(manager.all_items()) == 3
        assert manager.get_items("orders") == ["ORD001"]
        assert manager.get_items("payments") == ["PAY001"]
        assert manager.get_items("users") == ["USER001"]

    def test_add_many(self, manager):
        """测试批量添加"""
        manager.add_many("orders", ["ORD001", "ORD002", "ORD003"])
        assert len(manager.get_items("orders")) == 3

    def test_get_items_nonexistent_type(self, manager):
        """测试获取不存在的类型"""
        result = manager.get_items("nonexistent")
        assert result == []

    def test_has_items_true(self, manager):
        """测试 has_items 有项目时返回 True"""
        manager.add("orders", "ORD001")
        assert manager.has_items() is True

    def test_has_items_false(self, manager):
        """测试 has_items 无项目时返回 False"""
        assert manager.has_items() is False

    def test_cleanup_executes_when_should_clean(self, manager):
        """测试正常情况下执行清理"""
        manager.add("orders", "ORD001")
        manager.cleanup()
        assert manager.cleanup_called is True

    def test_cleanup_skips_when_keep_data(self, mock_request):
        """测试 --keep-test-data 时跳过清理"""
        mock_request.config.option.keep_test_data = True
        manager = ConcreteCleanupManager(mock_request)
        manager.add("orders", "ORD001")
        manager.cleanup()
        assert manager.cleanup_called is False

    def test_cleanup_skips_when_no_items(self, manager):
        """测试无项目时不执行清理"""
        manager.cleanup()
        assert manager.cleanup_called is False


# ============================================================
# SimpleCleanupManager 测试
# ============================================================


class TestSimpleCleanupManager:
    """测试 SimpleCleanupManager 回调函数模式"""

    @pytest.fixture
    def mock_request(self):
        """创建 mock request 对象"""
        request = Mock()
        request.node.get_closest_marker.return_value = None
        request.config.option = Mock()
        request.config.option.keep_test_data = False
        return request

    @pytest.fixture
    def manager(self, mock_request):
        """创建测试用 manager 实例"""
        return SimpleCleanupManager(mock_request)

    def test_register_cleanup_and_execute(self, manager):
        """测试注册清理函数并执行"""
        mock_callback = Mock()
        manager.register_cleanup("orders", mock_callback)
        manager.add("orders", "ORD001")
        manager.add("orders", "ORD002")

        manager.cleanup()

        mock_callback.assert_called_once_with(["ORD001", "ORD002"])

    def test_cleanup_multiple_types(self, manager):
        """测试清理多种类型"""
        orders_callback = Mock()
        payments_callback = Mock()

        manager.register_cleanup("orders", orders_callback)
        manager.register_cleanup("payments", payments_callback)

        manager.add_many("orders", ["ORD001", "ORD002"])
        manager.add("payments", "PAY001")

        manager.cleanup()

        orders_callback.assert_called_once_with(["ORD001", "ORD002"])
        payments_callback.assert_called_once_with(["PAY001"])

    def test_cleanup_without_registered_function(self, manager):
        """测试未注册清理函数时的情况"""
        manager.add("orders", "ORD001")
        # 不应抛出异常
        manager.cleanup()

    def test_cleanup_with_callback_exception(self, manager):
        """测试回调抛出异常时继续清理"""
        failing_callback = Mock(side_effect=ValueError("清理失败"))
        success_callback = Mock()

        manager.register_cleanup("orders", failing_callback)
        manager.register_cleanup("payments", success_callback)

        manager.add("orders", "ORD001")
        manager.add("payments", "PAY001")

        # 不应抛出异常
        manager.cleanup()

        # 两个回调都被调用
        failing_callback.assert_called_once()
        success_callback.assert_called_once()

    def test_cleanup_skips_empty_items(self, manager):
        """测试跳过空项目列表"""
        mock_callback = Mock()
        manager.register_cleanup("orders", mock_callback)
        # 不添加任何项目

        manager.cleanup()

        mock_callback.assert_not_called()

    def test_cleanup_with_lambda(self, manager):
        """测试使用 lambda 作为回调"""
        result = []
        manager.register_cleanup("orders", lambda ids: result.extend(ids))
        manager.add_many("orders", ["ORD001", "ORD002"])

        manager.cleanup()

        assert result == ["ORD001", "ORD002"]


# ============================================================
# ListCleanup 测试
# ============================================================


class TestListCleanup:
    """测试 ListCleanup 列表式清理器"""

    @pytest.fixture
    def mock_request(self):
        """创建 mock request 对象"""
        request = Mock()
        request.node.get_closest_marker.return_value = None
        request.config.option = Mock()
        request.config.option.keep_test_data = False
        return request

    @pytest.fixture
    def cleanup_list(self, mock_request):
        """创建测试用 ListCleanup 实例"""
        return ListCleanup(mock_request)

    def test_inherits_from_list(self, cleanup_list):
        """测试继承自 list"""
        assert isinstance(cleanup_list, list)

    def test_append_and_iterate(self, cleanup_list):
        """测试添加和迭代"""
        cleanup_list.append("ORD001")
        cleanup_list.append("ORD002")
        assert list(cleanup_list) == ["ORD001", "ORD002"]

    def test_extend(self, cleanup_list):
        """测试 extend 方法"""
        cleanup_list.extend(["ORD001", "ORD002", "ORD003"])
        assert len(cleanup_list) == 3

    def test_should_keep_false_by_default(self, cleanup_list):
        """测试默认 should_keep 返回 False"""
        assert cleanup_list.should_keep() is False

    def test_should_keep_true_with_option(self, mock_request):
        """测试 --keep-test-data 时返回 True"""
        mock_request.config.option.keep_test_data = True
        cleanup_list = ListCleanup(mock_request)
        assert cleanup_list.should_keep() is True

    def test_should_do_cleanup_true_by_default(self, cleanup_list):
        """测试默认 should_do_cleanup 返回 True"""
        assert cleanup_list.should_do_cleanup() is True

    def test_should_do_cleanup_false_with_option(self, mock_request):
        """测试 --keep-test-data 时返回 False"""
        mock_request.config.option.keep_test_data = True
        cleanup_list = ListCleanup(mock_request)
        cleanup_list.append("ORD001")
        assert cleanup_list.should_do_cleanup() is False

    def test_should_do_cleanup_logs_only_once(self, mock_request):
        """测试 should_do_cleanup 只打印一次日志（通过内部状态验证）"""
        mock_request.config.option.keep_test_data = True
        cleanup_list = ListCleanup(mock_request)
        cleanup_list.append("ORD001")

        # 验证初始状态
        assert cleanup_list._keep_logged is False

        # 调用多次
        cleanup_list.should_do_cleanup()
        assert cleanup_list._keep_logged is True  # 第一次调用后变为 True

        cleanup_list.should_do_cleanup()
        cleanup_list.should_do_cleanup()
        # 内部标志保持为 True，确保日志只打印一次
        assert cleanup_list._keep_logged is True

    def test_should_do_cleanup_no_log_when_empty(self, mock_request):
        """测试列表为空时不设置日志标志"""
        mock_request.config.option.keep_test_data = True
        cleanup_list = ListCleanup(mock_request)
        # 不添加任何项目

        cleanup_list.should_do_cleanup()

        # 列表为空时不设置日志标志
        assert cleanup_list._keep_logged is False


__all__ = [
    "TestShouldKeepTestData",
    "TestCleanupManager",
    "TestSimpleCleanupManager",
    "TestListCleanup",
]
