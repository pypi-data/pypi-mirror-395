"""
环境验证扩展示例

演示如何创建环境验证扩展，确保测试环境符合要求。
与docs/user-guide/extensions.md中的自定义扩展开发对应。
"""

import os
import socket
import sys
from urllib.parse import urlparse

from pydantic import Field

from df_test_framework import Bootstrap, FrameworkSettings, hookimpl


class EnvironmentValidator:
    """环境验证扩展 - 确保测试环境符合要求"""

    def __init__(self, required_envs: list[str] = None, min_python_version: tuple = (3, 10)):
        """
        初始化环境验证器

        Args:
            required_envs: 必需的环境变量列表
            min_python_version: 最小Python版本
        """
        self.required_envs = required_envs or []
        self.min_python_version = min_python_version
        self.validation_errors: list[str] = []

    @hookimpl
    def df_post_bootstrap(self, runtime):
        """Bootstrap后执行环境验证"""
        logger = runtime.logger
        settings = runtime.settings

        logger.info("=" * 60)
        logger.info("🔍 开始环境验证...")
        logger.info("=" * 60)

        # 1. 验证环境变量
        self._validate_environment_variables(logger)

        # 2. 验证Python版本
        self._validate_python_version(logger)

        # 3. 验证网络连通性
        self._validate_network_connectivity(logger, settings.http.base_url)

        # 4. 验证数据库连接
        self._validate_database_connection(logger, runtime)

        # 5. 验证Redis连接
        self._validate_redis_connection(logger, runtime)

        # 总结验证结果
        if self.validation_errors:
            logger.error("=" * 60)
            logger.error("❌ 环境验证失败")
            logger.error("=" * 60)
            for i, error in enumerate(self.validation_errors, 1):
                logger.error(f"  {i}. {error}")
            logger.error("=" * 60)
            logger.error("请修复以上问题后重新运行测试")
            sys.exit(1)
        else:
            logger.info("=" * 60)
            logger.info("✅ 环境验证通过！")
            logger.info("=" * 60)

    def _validate_environment_variables(self, logger):
        """验证必需的环境变量"""
        if not self.required_envs:
            logger.info("⏭️  跳过环境变量检查（未配置required_envs）")
            return

        logger.info(f"📝 检查环境变量 (需要 {len(self.required_envs)} 个)...")
        missing = []

        for env_var in self.required_envs:
            value = os.getenv(env_var)
            if not value:
                missing.append(env_var)
                logger.warning(f"   ❌ {env_var}: 未设置")
            else:
                # 脱敏显示
                display_value = value if len(value) < 20 else value[:10] + "..." + value[-5:]
                logger.info(f"   ✅ {env_var}: {display_value}")

        if missing:
            error = f"缺少环境变量: {', '.join(missing)}"
            self.validation_errors.append(error)
            logger.error(f"❌ {error}")
        else:
            logger.info("✅ 所有环境变量已设置")

    def _validate_python_version(self, logger):
        """验证Python版本"""
        logger.info(f"\n🐍 检查Python版本 (需要 >= {'.'.join(map(str, self.min_python_version))})...")
        current_version = sys.version_info[:2]
        version_str = f"{current_version[0]}.{current_version[1]}"

        if current_version < self.min_python_version:
            error = f"Python版本过低: {version_str}, 需要 >= {'.'.join(map(str, self.min_python_version))}"
            self.validation_errors.append(error)
            logger.error(f"   ❌ {error}")
        else:
            logger.info(f"   ✅ Python {version_str}")

    def _validate_network_connectivity(self, logger, base_url: str):
        """验证网络连通性"""
        logger.info("\n🌐 检查网络连通性...")
        logger.info(f"   目标: {base_url}")

        try:
            parsed = urlparse(base_url)
            hostname = parsed.hostname or parsed.path

            # 尝试解析主机名
            ip = socket.gethostbyname(hostname)
            logger.info(f"   ✅ DNS解析成功: {hostname} -> {ip}")

            # 尝试建立连接（如果有端口）
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((hostname, port))
            sock.close()

            if result == 0:
                logger.info(f"   ✅ 端口 {port} 可访问")
            else:
                logger.warning(f"   ⚠️ 端口 {port} 不可访问（可能是防火墙）")

        except socket.gaierror:
            error = f"无法解析主机名: {base_url}"
            self.validation_errors.append(error)
            logger.error(f"   ❌ {error}")
        except Exception as e:
            logger.warning(f"   ⚠️  网络检查警告: {e}")

    def _validate_database_connection(self, logger, runtime):
        """验证数据库连接"""
        logger.info("\n💾 检查数据库连接...")

        try:
            db = runtime.database()
            result = db.execute_query("SELECT 1 as test")
            if result and len(result) > 0:
                logger.info("   ✅ 数据库连接正常")
                logger.info(f"   主机: {runtime.settings.database.host}")
                logger.info(f"   数据库: {runtime.settings.database.database}")
            else:
                logger.warning("   ⚠️  查询返回空结果")
        except Exception as e:
            error = f"数据库连接失败: {e}"
            self.validation_errors.append(error)
            logger.error(f"   ❌ {error}")

    def _validate_redis_connection(self, logger, runtime):
        """验证Redis连接"""
        logger.info("\n📮 检查Redis连接...")

        try:
            redis = runtime.redis_client()
            redis.ping()
            logger.info("   ✅ Redis连接正常")
            logger.info(f"   主机: {runtime.settings.redis.host}:{runtime.settings.redis.port}")

            # 测试读写
            test_key = "__framework_test__"
            redis.set(test_key, "test_value", ex=5)
            value = redis.get(test_key)
            if value == "test_value":
                logger.info("   ✅ Redis读写正常")
            else:
                logger.warning("   ⚠️  Redis读写异常")

        except Exception as e:
            error = f"Redis连接失败: {e}"
            self.validation_errors.append(error)
            logger.error(f"   ❌ {error}")


class QuickValidator:
    """快速验证器 - 只验证关键服务"""

    @hookimpl
    def df_post_bootstrap(self, runtime):
        """快速验证"""
        logger = runtime.logger
        logger.info("\n⚡ 快速环境验证...")

        # 只验证HTTP服务
        try:
            http = runtime.http_client()
            response = http.get("/health", timeout=3)
            if response.status_code == 200:
                logger.info("✅ API服务健康")
            else:
                logger.warning(f"⚠️  API健康检查返回: {response.status_code}")
        except Exception as e:
            logger.warning(f"⚠️  API服务检查失败: {e}")


# 配置类
class Settings(FrameworkSettings):
    """示例配置"""
    api_base_url: str = Field(default="https://jsonplaceholder.typicode.com")


# ================== 示例代码 ==================

def example_full_validation():
    """示例1: 完整环境验证"""
    print("\n" + "=" * 70)
    print("示例1: 完整环境验证")
    print("=" * 70)

    # 创建验证器
    validator = EnvironmentValidator(
        required_envs=[],  # 不检查环境变量，避免示例失败
        min_python_version=(3, 10)
    )

    # 启动应用
    try:
        app = Bootstrap().with_settings(Settings).with_extensions([validator]).build()
        app.run()
        print("\n✅ 应用启动成功，环境验证通过!")
    except SystemExit:
        print("\n❌ 环境验证失败，应用退出")


def example_quick_validation():
    """示例2: 快速验证"""
    print("\n" + "=" * 70)
    print("示例2: 快速环境验证")
    print("=" * 70)

    validator = QuickValidator()

    app = Bootstrap().with_settings(Settings).with_extensions([validator]).build()
    app.run()

    print("\n✅ 快速验证完成!")


def example_custom_validation():
    """示例3: 自定义验证逻辑"""
    print("\n" + "=" * 70)
    print("示例3: 自定义验证逻辑")
    print("=" * 70)

    class CustomValidator:
        """自定义验证器"""

        @hookimpl
        def df_post_bootstrap(self, runtime):
            logger = runtime.logger

            logger.info("\n🔧 自定义环境验证...")

            # 1. 检查配置
            if not runtime.settings.http.base_url:
                logger.error("❌ 未配置API地址")
                sys.exit(1)

            logger.info(f"✅ API地址: {runtime.settings.http.base_url}")

            # 2. 检查环境类型
            env = runtime.settings.environment
            logger.info(f"✅ 当前环境: {env.value}")

            if env.value == "production":
                logger.warning("⚠️  警告：正在生产环境中运行测试！")

            # 3. 检查特定配置
            extras = runtime.settings.extras
            if not extras or "project_name" not in extras:
                logger.warning("⚠️  未设置项目名称")
            else:
                logger.info(f"✅ 项目: {extras['project_name']}")

            logger.info("✅ 自定义验证完成")

    validator = CustomValidator()
    app = Bootstrap().with_settings(Settings).with_extensions([validator]).build()
    app.run()

    print("\n✅ 自定义验证完成!")


def example_conditional_validation():
    """示例4: 条件验证（根据环境决定）"""
    print("\n" + "=" * 70)
    print("示例4: 条件验证")
    print("=" * 70)

    class ConditionalValidator:
        """条件验证器"""

        @hookimpl
        def df_post_bootstrap(self, runtime):
            logger = runtime.logger
            env = runtime.settings.environment.value

            logger.info(f"\n🎯 根据环境执行验证 (当前: {env})...")

            if env == "production":
                logger.info("生产环境 - 执行严格验证")
                # 生产环境执行更严格的验证
                logger.info("  ✓ 检查备份策略")
                logger.info("  ✓ 检查监控配置")
                logger.info("  ✓ 检查日志级别")

            elif env == "staging":
                logger.info("预发布环境 - 执行标准验证")
                logger.info("  ✓ 检查数据库连接")
                logger.info("  ✓ 检查缓存服务")

            else:
                logger.info("开发/测试环境 - 执行基础验证")
                logger.info("  ✓ 检查基本配置")

            logger.info("✅ 条件验证完成")

    validator = ConditionalValidator()
    app = Bootstrap().with_settings(Settings).with_extensions([validator]).build()
    app.run()

    print("\n✅ 条件验证完成!")


if __name__ == "__main__":
    print("\n🔍 环境验证扩展示例")
    print("=" * 70)
    print("演示如何创建环境验证扩展，确保测试环境符合要求")
    print("=" * 70)

    # 运行示例
    example_quick_validation()
    example_custom_validation()
    example_conditional_validation()
    example_full_validation()  # 放最后，因为可能会失败

    print("\n" + "=" * 70)
    print("✅ 示例演示完成!")
    print("=" * 70)
    print("\n💡 使用建议:")
    print("  1. 在CI/CD中使用环境验证确保环境正确")
    print("  2. 根据环境类型(dev/staging/prod)执行不同级别的验证")
    print("  3. 验证失败时使用sys.exit(1)中断测试")
    print("  4. 记录详细的验证日志便于问题排查")
    print("  5. 结合健康检查API验证服务可用性")
