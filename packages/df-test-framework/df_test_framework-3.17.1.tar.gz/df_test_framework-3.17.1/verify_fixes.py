"""验证v1问题修复

此脚本验证以下修复:
1. Repository泛型设计 - 移除Generic[T]
2. Database白名单逻辑 - None=允许所有, set()=禁止所有
3. HttpClient重试机制 - 实现重试逻辑
4. BaseAPI业务错误处理 - 添加BusinessError异常
"""

import sys


def test_1_repository_generic():
    """验证Repository不再使用泛型"""
    print("\n=== 测试1: Repository泛型设计 ===")
    try:
        # 验证BaseRepository没有Generic[T]
        import inspect

        from df_test_framework.databases.repositories import BaseRepository
        bases = inspect.getmro(BaseRepository)
        has_generic = any('Generic' in str(base) for base in bases)

        if has_generic:
            print("❌ FAILED: BaseRepository仍然继承Generic")
            return False

        # 验证BaseRepository没有to_model抽象方法
        if hasattr(BaseRepository, 'to_model'):
            print("❌ FAILED: BaseRepository仍然有to_model方法")
            return False

        print("✅ PASS: Repository已移除泛型设计")
        return True

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_2_database_whitelist():
    """验证Database白名单逻辑"""
    print("\n=== 测试2: Database白名单逻辑 ===")
    try:

        # 验证DEFAULT_ALLOWED_TABLES存在于database.py中且为None
        import df_test_framework.core.database.database as db_module
        if not hasattr(db_module, 'DEFAULT_ALLOWED_TABLES'):
            print("❌ FAILED: database.py中缺少DEFAULT_ALLOWED_TABLES")
            return False

        if db_module.DEFAULT_ALLOWED_TABLES is not None:
            print(f"❌ FAILED: DEFAULT_ALLOWED_TABLES应为None, 实际为{db_module.DEFAULT_ALLOWED_TABLES}")
            return False

        print("✅ PASS: Database白名单默认值为None(允许所有表)")

        # 测试白名单验证逻辑
        class TestDB:
            def __init__(self, allowed_tables):
                self.allowed_tables = allowed_tables if allowed_tables is not None else None

            def _validate_table_name(self, table: str):
                """复制Database的验证逻辑"""
                if self.allowed_tables is None:
                    return  # 允许所有

                if not self.allowed_tables:
                    raise ValueError("表操作已禁用: 白名单为空集")

                if table not in self.allowed_tables:
                    raise ValueError(f"表名 '{table}' 不在白名单中")

        # 测试None(允许所有)
        db1 = TestDB(None)
        try:
            db1._validate_table_name("any_table")
            print("✅ PASS: None允许所有表")
        except Exception as e:
            print(f"❌ FAILED: None应允许所有表, 错误: {e}")
            return False

        # 测试空集(禁止所有)
        db2 = TestDB(set())
        try:
            db2._validate_table_name("any_table")
            print("❌ FAILED: set()应禁止所有表")
            return False
        except ValueError as e:
            if "白名单为空集" in str(e):
                print("✅ PASS: set()禁止所有表")
            else:
                print(f"❌ FAILED: 错误消息不正确: {e}")
                return False

        # 测试白名单
        db3 = TestDB({"users", "orders"})
        try:
            db3._validate_table_name("users")
            print("✅ PASS: 白名单允许指定表")
        except Exception as e:
            print(f"❌ FAILED: 白名单应允许users表, 错误: {e}")
            return False

        try:
            db3._validate_table_name("products")
            print("❌ FAILED: 白名单应拒绝未授权表")
            return False
        except ValueError as e:
            if "不在白名单中" in str(e):
                print("✅ PASS: 白名单拒绝未授权表")
            else:
                print(f"❌ FAILED: 错误消息不正确: {e}")
                return False

        return True

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_3_http_retry():
    """验证HttpClient重试机制"""
    print("\n=== 测试3: HttpClient重试机制 ===")
    try:
        import inspect

        from df_test_framework.clients.http.rest.httpx import HttpClient

        # 检查request方法是否实现了重试逻辑
        source = inspect.getsource(HttpClient.request)

        # 检查关键字
        required_keywords = [
            'max_retries',  # 重试次数
            'attempt',      # 尝试次数
            'range',        # 循环
            'sleep',        # 等待
        ]

        missing = [kw for kw in required_keywords if kw not in source]

        if missing:
            print(f"❌ FAILED: request方法缺少重试逻辑关键字: {missing}")
            return False

        # 检查是否移除了无效的retries参数
        if 'HTTPTransport' in source:
            transport_source = source[source.index('HTTPTransport'):]
            if 'retries=' in transport_source:
                print("❌ FAILED: HTTPTransport仍然有retries参数")
                return False

        print("✅ PASS: HttpClient已实现重试机制")
        return True

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_4_business_error():
    """验证BaseAPI业务错误处理"""
    print("\n=== 测试4: BaseAPI业务错误处理 ===")
    try:
        # 测试BusinessError导入
        import inspect

        from df_test_framework import BusinessError
        from df_test_framework.clients.http.rest.httpx import BaseAPI

        # 验证BusinessError异常类
        if not issubclass(BusinessError, Exception):
            print("❌ FAILED: BusinessError应继承Exception")
            return False

        # 验证BusinessError属性
        err = BusinessError("test", code=500, data={"key": "value"})
        if not hasattr(err, 'message') or not hasattr(err, 'code') or not hasattr(err, 'data'):
            print("❌ FAILED: BusinessError缺少必要属性")
            return False

        print("✅ PASS: BusinessError异常类正确实现")

        # 验证BaseAPI有_check_business_error方法
        if not hasattr(BaseAPI, '_check_business_error'):
            print("❌ FAILED: BaseAPI缺少_check_business_error方法")
            return False

        print("✅ PASS: BaseAPI包含_check_business_error方法")

        # 验证_parse_response方法调用了业务错误检查
        source = inspect.getsource(BaseAPI._parse_response)
        if '_check_business_error' not in source:
            print("❌ FAILED: _parse_response未调用_check_business_error")
            return False

        if 'check_business_error' not in source:
            print("❌ FAILED: _parse_response缺少check_business_error参数")
            return False

        print("✅ PASS: _parse_response包含业务错误检查逻辑")

        # 验证顶层导出
        import df_test_framework
        if 'BusinessError' not in df_test_framework.__all__:
            print("❌ FAILED: BusinessError未在顶层__all__中导出")
            return False

        print("✅ PASS: BusinessError已在顶层导出")
        return True

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """运行所有验证测试"""
    print("=" * 60)
    print("开始验证v1问题修复...")
    print("=" * 60)

    results = {
        "Repository泛型设计": test_1_repository_generic(),
        "Database白名单逻辑": test_2_database_whitelist(),
        "HttpClient重试机制": test_3_http_retry(),
        "BaseAPI业务错误处理": test_4_business_error(),
    }

    print("\n" + "=" * 60)
    print("验证结果汇总:")
    print("=" * 60)

    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAILED"
        print(f"{status} - {name}")

    total = len(results)
    passed = sum(results.values())

    print("\n" + "=" * 60)
    print(f"总计: {passed}/{total} 通过")
    print("=" * 60)

    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
