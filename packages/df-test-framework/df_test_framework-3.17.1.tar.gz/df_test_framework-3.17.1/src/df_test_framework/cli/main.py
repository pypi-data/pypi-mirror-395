"""CLI主程序

定义命令行参数解析和命令分发。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# 修复 Windows 平台的 UTF-8 编码问题
if sys.platform == "win32":
    import io

    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")
    if isinstance(sys.stderr, io.TextIOWrapper):
        sys.stderr.reconfigure(encoding="utf-8")

from .commands import (
    OPENAPI_GENERATOR_AVAILABLE,
    generate_api_client,
    generate_builder,
    generate_from_openapi,
    generate_models_from_json,
    generate_repository,
    generate_settings,
    generate_test,
    init_project,
    interactive_generate,
)


def main(argv: list[str] | None = None) -> None:
    """CLI主函数

    Args:
        argv: 命令行参数列表，None表示使用sys.argv

    Example:
        >>> main(["init", "my-project"])
        ✅ 项目初始化成功！
        ...
        >>> main(["gen", "test", "user_login"])
        ✅ 测试文件生成成功！
        ...
    """
    parser = argparse.ArgumentParser(
        prog="df-test",
        description="DF Test Framework 命令行工具",
        epilog="参考文档: https://github.com/your-org/df-test-framework",
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help="可用命令")

    # ========== init命令 ==========
    init_parser = subparsers.add_parser("init", help="初始化新的测试项目脚手架")
    init_parser.add_argument("path", type=str, help="项目目录路径")
    init_parser.add_argument(
        "--type",
        type=str,
        choices=["api", "ui", "full"],
        default="api",
        help="项目类型: api=API测试, ui=UI测试, full=API+UI混合（默认: api）",
    )
    init_parser.add_argument(
        "--ci",
        type=str,
        choices=["github-actions", "gitlab-ci", "jenkins", "all", "none"],
        default="none",
        help="CI/CD平台: github-actions, gitlab-ci, jenkins, all, none（默认: none）",
    )
    init_parser.add_argument("--force", action="store_true", help="强制覆盖已存在的文件")

    # ========== generate命令（别名: gen） ==========
    gen_parser = subparsers.add_parser("gen", aliases=["generate"], help="生成测试代码文件")
    gen_subparsers = gen_parser.add_subparsers(dest="gen_type", required=True, help="生成类型")

    # gen test - 生成测试文件
    test_parser = gen_subparsers.add_parser("test", help="生成API测试文件")
    test_parser.add_argument("name", type=str, help="测试名称（如: user_login）")
    test_parser.add_argument("--feature", type=str, help="Allure feature名称")
    test_parser.add_argument("--story", type=str, help="Allure story名称")
    test_parser.add_argument("--output-dir", type=str, help="输出目录（默认: tests/api/）")
    test_parser.add_argument("--force", action="store_true", help="强制覆盖已存在的文件")
    test_parser.add_argument(
        "--template",
        type=str,
        choices=["basic", "complete"],
        default="basic",
        help="模板类型: basic=基础模板（TODO占位符），complete=完整模板（实现示例）（默认: basic）",
    )
    test_parser.add_argument("--api-path", type=str, help="API路径（如: users）")

    # gen builder - 生成Builder类
    builder_parser = gen_subparsers.add_parser("builder", help="生成Builder类")
    builder_parser.add_argument("name", type=str, help="实体名称（如: user）")
    builder_parser.add_argument("--output-dir", type=str, help="输出目录")
    builder_parser.add_argument("--force", action="store_true", help="强制覆盖已存在的文件")

    # gen repo - 生成Repository类
    repo_parser = gen_subparsers.add_parser("repo", aliases=["repository"], help="生成Repository类")
    repo_parser.add_argument("name", type=str, help="实体名称（如: user）")
    repo_parser.add_argument("--table-name", type=str, help="数据库表名（默认与name相同）")
    repo_parser.add_argument("--output-dir", type=str, help="输出目录")
    repo_parser.add_argument("--force", action="store_true", help="强制覆盖已存在的文件")

    # gen api - 生成API客户端类
    api_parser = gen_subparsers.add_parser("api", help="生成API客户端类")
    api_parser.add_argument("name", type=str, help="API名称（如: user）")
    api_parser.add_argument("--api-path", type=str, help="API路径前缀（默认与name相同）")
    api_parser.add_argument("--output-dir", type=str, help="输出目录")
    api_parser.add_argument("--force", action="store_true", help="强制覆盖已存在的文件")

    # gen models - 从JSON生成Pydantic模型
    models_parser = gen_subparsers.add_parser("models", help="从JSON响应生成Pydantic模型")
    models_parser.add_argument("json_file", type=str, help="JSON文件路径（如: response.json）")
    models_parser.add_argument("--name", type=str, help="模型名称（默认根据文件名生成）")
    models_parser.add_argument(
        "--output-dir", type=str, help="输出目录（默认: src/<project>/models/responses/）"
    )
    models_parser.add_argument("--force", action="store_true", help="强制覆盖已存在的文件")

    # gen settings - 生成项目配置
    settings_parser = gen_subparsers.add_parser(
        "settings", help="生成项目配置文件（settings.py和.env）"
    )
    settings_parser.add_argument(
        "--with-interceptors",
        action="store_true",
        default=True,
        help="包含拦截器配置（默认: True）",
    )
    settings_parser.add_argument(
        "--with-profile",
        action="store_true",
        default=True,
        help="生成Profile环境配置文件（.env.dev/.env.test/.env.prod）（默认: True）",
    )
    settings_parser.add_argument("--output-dir", type=str, help="输出目录（默认: src/<project>/）")
    settings_parser.add_argument("--force", action="store_true", help="强制覆盖已存在的文件")

    # gen interactive - 交互式生成（别名: gen -i）
    _ = gen_subparsers.add_parser(
        "interactive", aliases=["i"], help="交互式代码生成向导（类似 npm init）"
    )
    # interactive 命令不需要额外参数

    # gen from-swagger - 从 OpenAPI/Swagger 生成
    swagger_parser = gen_subparsers.add_parser(
        "from-swagger", aliases=["swagger", "openapi"], help="从 OpenAPI/Swagger 规范生成测试代码"
    )
    swagger_parser.add_argument(
        "spec_path",
        type=str,
        help="OpenAPI规范文件路径或URL（如: swagger.json, https://api.example.com/swagger.json）",
    )
    swagger_parser.add_argument(
        "--tests", action="store_true", default=True, help="生成测试用例（默认: True）"
    )
    swagger_parser.add_argument(
        "--clients", action="store_true", default=True, help="生成API客户端（默认: True）"
    )
    swagger_parser.add_argument(
        "--models", action="store_true", default=True, help="生成Pydantic模型（默认: True）"
    )
    swagger_parser.add_argument("--tags", type=str, nargs="+", help="只生成指定标签的API（可选）")
    swagger_parser.add_argument("--output-dir", type=str, help="输出目录（默认: 当前目录）")
    swagger_parser.add_argument("--force", action="store_true", help="强制覆盖已存在的文件")

    # 解析参数
    args = parser.parse_args(argv)

    # 执行命令
    if args.command == "init":
        target = Path(args.path).resolve()
        init_project(target, project_type=args.type, ci_platform=args.ci, force=args.force)

    elif args.command in ("gen", "generate"):
        output_dir = (
            Path(args.output_dir) if hasattr(args, "output_dir") and args.output_dir else None
        )

        if args.gen_type == "test":
            generate_test(
                args.name,
                feature=args.feature,
                story=args.story,
                output_dir=output_dir,
                force=args.force,
                template=args.template if hasattr(args, "template") else "basic",
                api_path=args.api_path if hasattr(args, "api_path") else None,
            )

        elif args.gen_type == "builder":
            generate_builder(
                args.name,
                output_dir=output_dir,
                force=args.force,
            )

        elif args.gen_type in ("repo", "repository"):
            generate_repository(
                args.name,
                table_name=args.table_name if hasattr(args, "table_name") else None,
                output_dir=output_dir,
                force=args.force,
            )

        elif args.gen_type == "api":
            generate_api_client(
                args.name,
                api_path=args.api_path if hasattr(args, "api_path") else None,
                output_dir=output_dir,
                force=args.force,
            )

        elif args.gen_type == "models":
            json_file = Path(args.json_file).resolve()
            generate_models_from_json(
                json_file,
                model_name=args.name if hasattr(args, "name") and args.name else None,
                output_dir=output_dir,
                force=args.force,
            )

        elif args.gen_type == "settings":
            generate_settings(
                with_interceptors=args.with_interceptors
                if hasattr(args, "with_interceptors")
                else True,
                with_profile=args.with_profile if hasattr(args, "with_profile") else True,
                output_dir=output_dir,
                force=args.force,
            )

        elif args.gen_type in ("interactive", "i"):
            interactive_generate()

        elif args.gen_type in ("from-swagger", "swagger", "openapi"):
            if not OPENAPI_GENERATOR_AVAILABLE:
                print("❌ 错误: OpenAPI 功能需要安装 prance 和 pyyaml 库")
                print("   请运行: pip install 'prance[osv]' pyyaml")
                return

            generate_from_openapi(
                args.spec_path,
                output_dir=output_dir,
                generate_tests=args.tests if hasattr(args, "tests") else True,
                generate_clients=args.clients if hasattr(args, "clients") else True,
                generate_models=args.models if hasattr(args, "models") else True,
                tags=args.tags if hasattr(args, "tags") and args.tags else None,
                force=args.force,
            )


__all__ = ["main"]
