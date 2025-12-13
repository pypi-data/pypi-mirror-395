"""交互式代码生成命令

提供友好的交互式问答界面，降低命令行参数记忆负担。
"""

from __future__ import annotations

from pathlib import Path

try:
    import questionary
    from questionary import Style

    QUESTIONARY_AVAILABLE = True

    # 自定义样式
    CUSTOM_STYLE = Style(
        [
            ("qmark", "fg:#673ab7 bold"),  # 问题标记
            ("question", "bold"),  # 问题文本
            ("answer", "fg:#f44336 bold"),  # 答案
            ("pointer", "fg:#673ab7 bold"),  # 指针
            ("highlighted", "fg:#673ab7 bold"),  # 高亮
            ("selected", "fg:#cc5454"),  # 选中
            ("separator", "fg:#cc5454"),  # 分隔符
            ("instruction", ""),  # 指示
            ("text", ""),  # 文本
            ("disabled", "fg:#858585 italic"),  # 禁用
        ]
    )
except ImportError:
    QUESTIONARY_AVAILABLE = False
    questionary = None
    CUSTOM_STYLE = None

from .generate_cmd import (
    generate_api_client,
    generate_builder,
    generate_repository,
    generate_settings,
    generate_test,
)


def interactive_generate() -> None:
    """交互式代码生成主函数

    提供友好的问答界面，引导用户生成测试代码。

    Example:
        >>> interactive_generate()
        🎯 df-test 代码生成向导
        ═══════════════════════════════════════
        📝 请选择要生成的内容：
        ...
    """
    if not QUESTIONARY_AVAILABLE:
        print("❌ 错误: 交互式功能需要安装 questionary 库")
        print("   请运行: pip install questionary")
        return

    # 打印欢迎信息
    print("\n" + "=" * 60)
    print("🎯 df-test 代码生成向导".center(60))
    print("=" * 60)
    print()

    # 检查 OpenAPI 功能是否可用
    from ..generators.openapi_parser import OPENAPI_AVAILABLE

    # 选择生成类型
    choices = [
        questionary.Choice("测试用例（Test Case）", value="test"),
        questionary.Choice(
            "完整测试套件（Test Suite - Builder + Repository + API）", value="suite"
        ),
        questionary.Choice("配置文件（Settings + .env）", value="settings"),
    ]

    # 如果 OpenAPI 可用，添加从 Swagger 生成选项
    if OPENAPI_AVAILABLE:
        choices.insert(
            2, questionary.Choice("从 Swagger/OpenAPI 生成（所有）✨ 推荐", value="swagger")
        )

    choices.extend(
        [
            questionary.Choice("Builder类", value="builder"),
            questionary.Choice("Repository类", value="repository"),
            questionary.Choice("API客户端类", value="api"),
            questionary.Choice("退出", value="exit"),
        ]
    )

    gen_type = questionary.select(
        "📝 请选择要生成的内容：",
        choices=choices,
        style=CUSTOM_STYLE,
    ).ask()

    if gen_type == "exit" or gen_type is None:
        print("\n👋 再见！")
        return

    # 根据类型分发
    if gen_type == "test":
        _interactive_test()
    elif gen_type == "suite":
        _interactive_suite()
    elif gen_type == "settings":
        _interactive_settings()
    elif gen_type == "swagger":
        _interactive_swagger()
    elif gen_type == "builder":
        _interactive_builder()
    elif gen_type == "repository":
        _interactive_repository()
    elif gen_type == "api":
        _interactive_api()


def _interactive_test() -> None:
    """交互式测试用例生成"""
    print("\n" + "-" * 60)
    print("📝 测试用例生成向导")
    print("-" * 60 + "\n")

    # 测试名称
    test_name = questionary.text(
        "测试名称（如: user_login, order_create）：",
        validate=lambda x: len(x) > 0 or "测试名称不能为空",
        style=CUSTOM_STYLE,
    ).ask()

    if test_name is None:
        print("\n❌ 已取消")
        return

    # 选择模板类型
    template = questionary.select(
        "选择模板类型：",
        choices=[
            questionary.Choice("基础模板（TODO占位符，适合熟悉框架的用户）", value="basic"),
            questionary.Choice("完整模板（实现示例，适合新手）✨ 推荐", value="complete"),
        ],
        default="complete",
        style=CUSTOM_STYLE,
    ).ask()

    if template is None:
        print("\n❌ 已取消")
        return

    # API路径
    api_path = questionary.text(
        "API路径（如: users, orders/items）（可选，按Enter跳过）：",
        default="",
        style=CUSTOM_STYLE,
    ).ask()

    if api_path is None:
        api_path = ""

    # Allure feature
    feature = questionary.text(
        "Allure Feature名称（如: 用户管理）（可选）：",
        default="",
        style=CUSTOM_STYLE,
    ).ask()

    if feature is None:
        feature = ""

    # Allure story
    story = questionary.text(
        "Allure Story名称（如: 创建用户）（可选）：",
        default="",
        style=CUSTOM_STYLE,
    ).ask()

    if story is None:
        story = ""

    # 输出目录
    output_dir = questionary.text(
        "输出目录（默认: tests/api/）：",
        default="tests/api",
        style=CUSTOM_STYLE,
    ).ask()

    if output_dir is None:
        output_dir = "tests/api"

    # 确认生成
    print("\n" + "-" * 60)
    print("📊 生成预览")
    print("-" * 60)
    print(f"  测试名称: {test_name}")
    print(f"  模板类型: {'完整模板' if template == 'complete' else '基础模板'}")
    if api_path:
        print(f"  API路径: {api_path}")
    if feature:
        print(f"  Feature: {feature}")
    if story:
        print(f"  Story: {story}")
    print(f"  输出目录: {output_dir}")
    print("-" * 60)

    confirm = questionary.confirm(
        "确认生成？",
        default=True,
        style=CUSTOM_STYLE,
    ).ask()

    if not confirm:
        print("\n❌ 已取消")
        return

    # 生成测试
    try:
        generate_test(
            test_name,
            feature=feature if feature else None,
            story=story if story else None,
            output_dir=Path(output_dir) if output_dir else None,
            force=False,
            template=template,
            api_path=api_path if api_path else None,
        )
        print("\n🎉 生成完成！")
    except Exception as e:
        print(f"\n❌ 生成失败: {e}")


def _interactive_suite() -> None:
    """交互式测试套件生成（Builder + Repository + API + Test）"""
    print("\n" + "-" * 60)
    print("📦 完整测试套件生成向导")
    print("-" * 60 + "\n")

    # 实体名称
    entity_name = questionary.text(
        "实体名称（如: user, order）：",
        validate=lambda x: len(x) > 0 or "实体名称不能为空",
        style=CUSTOM_STYLE,
    ).ask()

    if entity_name is None:
        print("\n❌ 已取消")
        return

    # 数据库表名
    table_name = questionary.text(
        f"数据库表名（默认: {entity_name}s）：",
        default=f"{entity_name}s",
        style=CUSTOM_STYLE,
    ).ask()

    if table_name is None:
        table_name = f"{entity_name}s"

    # API路径
    api_path = questionary.text(
        f"API路径（默认: {entity_name}s）：",
        default=f"{entity_name}s",
        style=CUSTOM_STYLE,
    ).ask()

    if api_path is None:
        api_path = f"{entity_name}s"

    # 确认生成
    print("\n" + "-" * 60)
    print("📊 生成预览")
    print("-" * 60)
    print("将生成以下文件：")
    print(f"  ✓ Builder类: src/<project>/builders/{entity_name}_builder.py")
    print(f"  ✓ Repository类: src/<project>/repositories/{entity_name}_repository.py")
    print(f"  ✓ API客户端: src/<project>/apis/{entity_name}_api.py")
    print(f"  ✓ 测试文件: tests/api/test_{entity_name}.py")
    print("-" * 60)

    confirm = questionary.confirm(
        "确认生成？",
        default=True,
        style=CUSTOM_STYLE,
    ).ask()

    if not confirm:
        print("\n❌ 已取消")
        return

    # 生成套件
    try:
        print("\n📝 生成 Builder...")
        generate_builder(entity_name, force=False)

        print("\n📝 生成 Repository...")
        generate_repository(entity_name, table_name=table_name, force=False)

        print("\n📝 生成 API客户端...")
        generate_api_client(entity_name, api_path=api_path, force=False)

        print("\n📝 生成测试文件...")
        generate_test(
            entity_name,
            feature=f"{entity_name.capitalize()}管理",
            story=f"{entity_name.capitalize()}操作",
            template="complete",
            api_path=api_path,
            force=False,
        )

        print("\n🎉 完整套件生成完成！")
    except Exception as e:
        print(f"\n❌ 生成失败: {e}")


def _interactive_settings() -> None:
    """交互式配置文件生成"""
    print("\n" + "-" * 60)
    print("⚙️  配置文件生成向导")
    print("-" * 60 + "\n")

    # 是否包含拦截器配置
    with_interceptors = questionary.confirm(
        "包含v3.5拦截器配置（签名、Token认证）？",
        default=True,
        style=CUSTOM_STYLE,
    ).ask()

    if with_interceptors is None:
        with_interceptors = True

    # 是否生成Profile配置
    with_profile = questionary.confirm(
        "生成Profile环境配置（.env.dev/.env.test/.env.prod）？",
        default=True,
        style=CUSTOM_STYLE,
    ).ask()

    if with_profile is None:
        with_profile = True

    # 确认生成
    print("\n" + "-" * 60)
    print("📊 生成预览")
    print("-" * 60)
    print("将生成以下文件：")
    print("  ✓ settings.py - 项目配置类")
    if with_interceptors:
        print("    └─ 包含拦截器配置示例")
    if with_profile:
        print("  ✓ .env - 基础配置")
        print("  ✓ .env.dev - 开发环境")
        print("  ✓ .env.test - 测试环境")
        print("  ✓ .env.prod - 生产环境")
        print("  ✓ .env.example - 配置示例")
    print("-" * 60)

    confirm = questionary.confirm(
        "确认生成？",
        default=True,
        style=CUSTOM_STYLE,
    ).ask()

    if not confirm:
        print("\n❌ 已取消")
        return

    # 生成配置
    try:
        generate_settings(
            with_interceptors=with_interceptors,
            with_profile=with_profile,
            force=False,
        )
        print("\n🎉 配置文件生成完成！")
    except Exception as e:
        print(f"\n❌ 生成失败: {e}")


def _interactive_builder() -> None:
    """交互式Builder生成"""
    print("\n" + "-" * 60)
    print("🏗️  Builder类生成向导")
    print("-" * 60 + "\n")

    # 实体名称
    entity_name = questionary.text(
        "实体名称（如: user, order）：",
        validate=lambda x: len(x) > 0 or "实体名称不能为空",
        style=CUSTOM_STYLE,
    ).ask()

    if entity_name is None:
        print("\n❌ 已取消")
        return

    # 生成
    try:
        generate_builder(entity_name, force=False)
        print("\n🎉 生成完成！")
    except Exception as e:
        print(f"\n❌ 生成失败: {e}")


def _interactive_repository() -> None:
    """交互式Repository生成"""
    print("\n" + "-" * 60)
    print("💾 Repository类生成向导")
    print("-" * 60 + "\n")

    # 实体名称
    entity_name = questionary.text(
        "实体名称（如: user, order）：",
        validate=lambda x: len(x) > 0 or "实体名称不能为空",
        style=CUSTOM_STYLE,
    ).ask()

    if entity_name is None:
        print("\n❌ 已取消")
        return

    # 数据库表名
    table_name = questionary.text(
        f"数据库表名（默认: {entity_name}s）：",
        default=f"{entity_name}s",
        style=CUSTOM_STYLE,
    ).ask()

    if table_name is None:
        table_name = f"{entity_name}s"

    # 生成
    try:
        generate_repository(entity_name, table_name=table_name, force=False)
        print("\n🎉 生成完成！")
    except Exception as e:
        print(f"\n❌ 生成失败: {e}")


def _interactive_api() -> None:
    """交互式API客户端生成"""
    print("\n" + "-" * 60)
    print("🌐 API客户端生成向导")
    print("-" * 60 + "\n")

    # API名称
    api_name = questionary.text(
        "API名称（如: user, order）：",
        validate=lambda x: len(x) > 0 or "API名称不能为空",
        style=CUSTOM_STYLE,
    ).ask()

    if api_name is None:
        print("\n❌ 已取消")
        return

    # API路径
    api_path = questionary.text(
        f"API路径前缀（默认: {api_name}s）：",
        default=f"{api_name}s",
        style=CUSTOM_STYLE,
    ).ask()

    if api_path is None:
        api_path = f"{api_name}s"

    # 生成
    try:
        generate_api_client(api_name, api_path=api_path, force=False)
        print("\n🎉 生成完成！")
    except Exception as e:
        print(f"\n❌ 生成失败: {e}")


def _interactive_swagger() -> None:
    """交互式 Swagger/OpenAPI 生成"""
    from ..generators.openapi_generator import generate_from_openapi

    print("\n" + "-" * 60)
    print("📜 Swagger/OpenAPI 生成向导")
    print("-" * 60 + "\n")

    # 规范文件路径
    spec_path = questionary.text(
        "OpenAPI 规范文件路径或 URL：\n（如: swagger.json, https://api.example.com/swagger.json）",
        validate=lambda x: len(x) > 0 or "规范文件路径不能为空",
        style=CUSTOM_STYLE,
    ).ask()

    if spec_path is None:
        print("\n❌ 已取消")
        return

    # 选择生成内容
    generate_options = questionary.checkbox(
        "选择要生成的内容（空格选择，Enter确认）：",
        choices=[
            questionary.Choice("测试用例", value="tests", checked=True),
            questionary.Choice("API 客户端", value="clients", checked=True),
            questionary.Choice("Pydantic 模型", value="models", checked=True),
        ],
        style=CUSTOM_STYLE,
    ).ask()

    if generate_options is None or not generate_options:
        print("\n❌ 至少需要选择一项")
        return

    # 标签过滤（可选）
    use_tags = questionary.confirm(
        "是否只生成特定标签的 API？",
        default=False,
        style=CUSTOM_STYLE,
    ).ask()

    tags = None
    if use_tags:
        tags_input = questionary.text(
            "输入标签（多个标签用空格分隔）：",
            style=CUSTOM_STYLE,
        ).ask()
        if tags_input:
            tags = tags_input.split()

    # 确认生成
    print("\n" + "-" * 60)
    print("📊 生成预览")
    print("-" * 60)
    print(f"  规范文件: {spec_path}")
    print("  生成内容:")
    if "tests" in generate_options:
        print("    ✓ 测试用例")
    if "clients" in generate_options:
        print("    ✓ API 客户端")
    if "models" in generate_options:
        print("    ✓ Pydantic 模型")
    if tags:
        print(f"  标签过滤: {', '.join(tags)}")
    print("-" * 60)

    confirm = questionary.confirm(
        "确认生成？",
        default=True,
        style=CUSTOM_STYLE,
    ).ask()

    if not confirm:
        print("\n❌ 已取消")
        return

    # 生成
    try:
        generate_from_openapi(
            spec_path,
            generate_tests="tests" in generate_options,
            generate_clients="clients" in generate_options,
            generate_models="models" in generate_options,
            tags=tags,
            force=False,
        )
        print("\n🎉 生成完成！")
    except Exception as e:
        print(f"\n❌ 生成失败: {e}")


__all__ = ["interactive_generate"]
