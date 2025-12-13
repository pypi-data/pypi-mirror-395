"""示例02: Profile环境配置

v3.5.0核心特性：多环境配置管理

演示内容:
1. 创建多环境配置文件（.env.dev, .env.test, .env.prod）
2. 通过ENV环境变量自动加载配置
3. 配置优先级：profile参数 > ENV变量 > 默认值
4. .env.local本地覆盖
5. 在代码中显式指定profile

运行方式:
    # 使用dev环境
    ENV=dev python examples/07-v35-features/02_profile_configuration.py

    # 使用test环境
    ENV=test python examples/07-v35-features/02_profile_configuration.py

    # 使用prod环境
    ENV=prod python examples/07-v35-features/02_profile_configuration.py
"""

import os
import tempfile
from pathlib import Path
from typing import Self

from dotenv import load_dotenv
from pydantic import Field, model_validator

from df_test_framework import Bootstrap, FrameworkSettings, HTTPConfig
from df_test_framework.infrastructure.config import SignatureInterceptorConfig

# ============================================================
# 示例1: 基础Profile配置
# ============================================================

def setup_demo_env_files(base_dir: Path):
    """创建演示用的环境配置文件"""

    # .env - 基础配置（所有环境共享）
    env_base = base_dir / ".env"
    env_base.write_text("""
# 基础配置（所有环境共享）
APP_NAME=demo-app
APP_VERSION=1.0.0

# HTTP配置默认值
APP_HTTP__TIMEOUT=30
APP_HTTP__MAX_RETRIES=3

# 日志配置
APP_LOGGING__LEVEL=INFO
APP_LOGGING__ENABLE_OBSERVABILITY=false
""".strip())

    # .env.dev - 开发环境配置
    env_dev = base_dir / ".env.dev"
    env_dev.write_text("""
# 开发环境配置
APP_HTTP__BASE_URL=https://dev-api.example.com
APP_DEBUG=true
APP_LOGGING__LEVEL=DEBUG
APP_LOGGING__ENABLE_OBSERVABILITY=true

# 开发环境签名密钥（可以公开）
APP_SECRET=dev_secret_12345
""".strip())

    # .env.test - 测试环境配置
    env_test = base_dir / ".env.test"
    env_test.write_text("""
# 测试环境配置
APP_HTTP__BASE_URL=https://test-api.example.com
APP_DEBUG=false
APP_LOGGING__LEVEL=INFO
APP_LOGGING__ENABLE_OBSERVABILITY=true

# 测试环境签名密钥
APP_SECRET=test_secret_67890
""".strip())

    # .env.prod - 生产环境配置
    env_prod = base_dir / ".env.prod"
    env_prod.write_text("""
# 生产环境配置
APP_HTTP__BASE_URL=https://api.example.com
APP_DEBUG=false
APP_LOGGING__LEVEL=WARNING
APP_LOGGING__ENABLE_OBSERVABILITY=false

# 生产环境签名密钥（从环境变量获取，不硬编码）
APP_SECRET=${PROD_SECRET}
""".strip())

    # .env.local - 本地覆盖配置（不提交git）
    env_local = base_dir / ".env.local"
    env_local.write_text("""
# 本地配置覆盖（不提交git）
# 这里可以覆盖任何环境的配置

# 例如：覆盖API地址为本地mock服务器
APP_HTTP__BASE_URL=http://localhost:3000

# 例如：启用详细日志
APP_LOGGING__LEVEL=DEBUG
""".strip())

    print(f"\n✅ 环境配置文件已创建在: {base_dir}")
    print("  - .env (基础配置)")
    print("  - .env.dev (开发环境)")
    print("  - .env.test (测试环境)")
    print("  - .env.prod (生产环境)")
    print("  - .env.local (本地覆盖)")


def _create_http_config() -> HTTPConfig:
    """创建HTTP配置（从环境变量读取）"""
    return HTTPConfig(
        base_url=os.getenv("APP_HTTP__BASE_URL", "https://jsonplaceholder.typicode.com"),
        timeout=int(os.getenv("APP_HTTP__TIMEOUT", "30")),
        max_retries=int(os.getenv("APP_HTTP__MAX_RETRIES", "3")),
        interceptors=[
            SignatureInterceptorConfig(
                type="signature",
                enabled=True,
                priority=10,
                algorithm="md5",
                secret=os.getenv("APP_SECRET", "default_secret"),
                header_name="X-Sign",
                include_paths=["/**"],
            ),
        ]
    )


class ProfileSettings(FrameworkSettings):
    """支持Profile的Settings"""

    app_name: str = Field(default_factory=lambda: os.getenv("APP_NAME", "unknown"))
    app_version: str = Field(default_factory=lambda: os.getenv("APP_VERSION", "0.0.0"))

    @model_validator(mode='after')
    def _setup_interceptors(self) -> Self:
        """设置HTTP拦截器"""
        self.http = _create_http_config()
        return self


def demo_basic_profile():
    """演示基础Profile配置"""
    print("\n" + "="*60)
    print("示例1: 基础Profile配置")
    print("="*60)

    # 创建临时目录存放配置文件
    with tempfile.TemporaryDirectory() as tmpdir:
        base_dir = Path(tmpdir)
        setup_demo_env_files(base_dir)

        # 切换到临时目录
        original_cwd = os.getcwd()
        os.chdir(base_dir)

        try:
            # 获取当前环境
            current_env = os.getenv("ENV", "dev")
            print(f"\n当前环境: {current_env}")

            # 加载对应环境的配置
            load_dotenv(f".env.{current_env}")
            load_dotenv(".env")  # 加载基础配置
            load_dotenv(".env.local", override=True)  # 本地配置覆盖

            # 创建运行时
            runtime = (
                Bootstrap()
                .with_settings(ProfileSettings)
                .build()
                .run()
            )

            # 打印配置信息
            settings = runtime.settings
            print("\n配置信息:")
            print(f"  应用名称: {settings.app_name}")
            print(f"  应用版本: {settings.app_version}")
            print(f"  API地址: {settings.http.base_url}")
            print(f"  超时时间: {settings.http.timeout}s")
            print(f"  日志级别: {settings.logging.level}")
            print(f"  Debug模式: {os.getenv('APP_DEBUG', 'false')}")

            # 发送测试请求
            runtime.http_client()
            print("\n发送测试请求...")
            # 注意：由于配置了.env.local覆盖为localhost，实际请求可能失败
            # 这里仅演示配置加载流程

        finally:
            # 恢复原始工作目录
            os.chdir(original_cwd)

    print("\n✅ Profile配置演示完成")


# ============================================================
# 示例2: 配置优先级演示
# ============================================================

def demo_config_priority():
    """演示配置优先级

    优先级（从高到低）:
    1. 环境变量
    2. .env.local
    3. .env.{profile}
    4. .env
    5. 代码默认值
    """
    print("\n" + "="*60)
    print("示例2: 配置优先级")
    print("="*60)

    with tempfile.TemporaryDirectory() as tmpdir:
        base_dir = Path(tmpdir)
        os.chdir(base_dir)

        # 创建配置文件
        (base_dir / ".env").write_text("APP_HTTP__TIMEOUT=30")
        (base_dir / ".env.dev").write_text("APP_HTTP__TIMEOUT=60")
        (base_dir / ".env.local").write_text("APP_HTTP__TIMEOUT=90")

        print("\n配置文件内容:")
        print("  .env:       APP_HTTP__TIMEOUT=30")
        print("  .env.dev:   APP_HTTP__TIMEOUT=60")
        print("  .env.local: APP_HTTP__TIMEOUT=90")

        # 场景1: 不设置环境变量
        print("\n场景1: 不设置环境变量")
        load_dotenv(".env.dev")
        load_dotenv(".env")
        load_dotenv(".env.local", override=True)
        timeout = int(os.getenv("APP_HTTP__TIMEOUT", "10"))
        print(f"  结果: timeout = {timeout}s (来自 .env.local)")

        # 场景2: 设置环境变量（最高优先级）
        print("\n场景2: 设置环境变量")
        os.environ["APP_HTTP__TIMEOUT"] = "120"
        timeout = int(os.getenv("APP_HTTP__TIMEOUT", "10"))
        print(f"  结果: timeout = {timeout}s (来自环境变量)")

        # 清理环境变量
        del os.environ["APP_HTTP__TIMEOUT"]

    print("\n✅ 配置优先级演示完成")


# ============================================================
# 示例3: 在代码中显式指定Profile
# ============================================================

def demo_explicit_profile():
    """演示在代码中显式指定Profile"""
    print("\n" + "="*60)
    print("示例3: 显式指定Profile")
    print("="*60)

    with tempfile.TemporaryDirectory() as tmpdir:
        base_dir = Path(tmpdir)
        setup_demo_env_files(base_dir)
        os.chdir(base_dir)

        # 场景1: 使用dev环境
        print("\n场景1: 显式指定dev环境")
        load_dotenv(".env.dev")
        load_dotenv(".env")

        runtime_dev = (
            Bootstrap()
            .with_settings(ProfileSettings)
            .build()
            .run()
        )
        print(f"  dev环境 API地址: {runtime_dev.settings.http.base_url}")

        # 清除环境变量
        for key in list(os.environ.keys()):
            if key.startswith("APP_"):
                del os.environ[key]

        # 场景2: 使用test环境
        print("\n场景2: 显式指定test环境")
        load_dotenv(".env.test")
        load_dotenv(".env")

        runtime_test = (
            Bootstrap()
            .with_settings(ProfileSettings)
            .build()
            .run()
        )
        print(f"  test环境 API地址: {runtime_test.settings.http.base_url}")

    print("\n✅ 显式Profile演示完成")


# ============================================================
# 示例4: 多环境切换实战
# ============================================================

def demo_multi_env_workflow():
    """演示多环境切换工作流"""
    print("\n" + "="*60)
    print("示例4: 多环境切换工作流")
    print("="*60)

    with tempfile.TemporaryDirectory() as tmpdir:
        base_dir = Path(tmpdir)
        setup_demo_env_files(base_dir)
        os.chdir(base_dir)

        # 模拟不同环境的工作流
        environments = ["dev", "test", "prod"]

        for env in environments:
            print(f"\n{'='*40}")
            print(f"环境: {env.upper()}")
            print(f"{'='*40}")

            # 清除之前的环境变量
            for key in list(os.environ.keys()):
                if key.startswith("APP_"):
                    del os.environ[key]

            # 加载环境配置
            load_dotenv(f".env.{env}")
            load_dotenv(".env")

            # 创建运行时
            runtime = (
                Bootstrap()
                .with_settings(ProfileSettings)
                .build()
                .run()
            )

            # 打印配置
            settings = runtime.settings
            print(f"API地址: {settings.http.base_url}")
            print(f"日志级别: {settings.logging.level}")
            print(f"Debug模式: {os.getenv('APP_DEBUG', 'false')}")
            print(f"签名密钥: {os.getenv('APP_SECRET', 'N/A')}")

    print("\n✅ 多环境切换演示完成")


# ============================================================
# 示例5: .env.local本地覆盖
# ============================================================

def demo_local_override():
    """演示.env.local本地覆盖"""
    print("\n" + "="*60)
    print("示例5: .env.local本地覆盖")
    print("="*60)

    with tempfile.TemporaryDirectory() as tmpdir:
        base_dir = Path(tmpdir)
        os.chdir(base_dir)

        # 创建配置文件
        (base_dir / ".env.dev").write_text("""
APP_HTTP__BASE_URL=https://dev-api.example.com
APP_HTTP__TIMEOUT=30
APP_DEBUG=true
""".strip())

        (base_dir / ".env.local").write_text("""
# 本地覆盖：使用本地mock服务器
APP_HTTP__BASE_URL=http://localhost:3000

# 本地覆盖：延长超时时间方便调试
APP_HTTP__TIMEOUT=300
""".strip())

        print("\n场景: 开发时使用本地mock服务器")
        print("\n配置文件:")
        print("  .env.dev:")
        print("    APP_HTTP__BASE_URL=https://dev-api.example.com")
        print("    APP_HTTP__TIMEOUT=30")
        print("\n  .env.local:")
        print("    APP_HTTP__BASE_URL=http://localhost:3000")
        print("    APP_HTTP__TIMEOUT=300")

        # 加载配置
        load_dotenv(".env.dev")
        load_dotenv(".env.local", override=True)  # 覆盖dev配置

        # 创建运行时
        class LocalSettings(FrameworkSettings):
            @model_validator(mode='after')
            def _setup_interceptors(self) -> Self:
                self.http = _create_http_config()
                return self

        runtime = (
            Bootstrap()
            .with_settings(LocalSettings)
            .build()
            .run()
        )

        # 打印最终配置
        print("\n最终配置:")
        print(f"  API地址: {runtime.settings.http.base_url} (来自 .env.local)")
        print(f"  超时时间: {runtime.settings.http.timeout}s (来自 .env.local)")
        print(f"  Debug模式: {os.getenv('APP_DEBUG')} (来自 .env.dev)")

        print("\n💡 提示:")
        print("  .env.local通常用于:")
        print("  - 覆盖API地址为本地mock服务器")
        print("  - 调整超时时间方便调试")
        print("  - 启用详细日志")
        print("  - 使用本地数据库")
        print("\n  .env.local应加入.gitignore，不提交到git")

    print("\n✅ .env.local覆盖演示完成")


# ============================================================
# 主函数
# ============================================================

def main():
    """运行所有示例"""
    print("\n" + "🚀 v3.5 Profile环境配置示例".center(60, "="))

    try:
        # 示例1: 基础Profile配置
        demo_basic_profile()

        # 示例2: 配置优先级
        demo_config_priority()

        # 示例3: 显式指定Profile
        demo_explicit_profile()

        # 示例4: 多环境切换工作流
        demo_multi_env_workflow()

        # 示例5: .env.local本地覆盖
        demo_local_override()

        print("\n" + "✅ 所有示例运行完成！".center(60, "="))

        print("\n💡 关键要点:")
        print("  1. 配置优先级: 环境变量 > .env.local > .env.{profile} > .env > 默认值")
        print("  2. .env.local用于本地覆盖，不提交git")
        print("  3. 通过ENV环境变量切换环境: ENV=dev/test/prod")
        print("  4. 所有配置都从环境变量读取，便于CI/CD集成")
        print("  5. 使用dotenv-linter验证配置文件格式")

        print("\n📁 推荐的配置文件结构:")
        print("  project/")
        print("  ├── .env              # 基础配置（提交git）")
        print("  ├── .env.dev          # 开发环境（提交git）")
        print("  ├── .env.test         # 测试环境（提交git）")
        print("  ├── .env.prod         # 生产环境（提交git，敏感信息用占位符）")
        print("  ├── .env.local        # 本地覆盖（不提交git）")
        print("  └── .env.example      # 配置模板（提交git）")

        print("\n📚 下一步:")
        print("  - 查看 03_runtime_overrides.py 学习运行时配置覆盖")
        print("  - 查看 docs/user-guide/PHASE3_FEATURES.md 了解Profile详细用法")

    except Exception as e:
        print(f"\n❌ 示例运行失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
