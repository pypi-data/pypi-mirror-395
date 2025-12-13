"""
插件实现（横切关注点）

v3.14.0 将插件从 extensions/ 迁移到 plugins/。

结构:
- builtin/: 内置插件
  - monitoring/: 监控插件
  - reporting/: 报告插件
- contrib/: 社区贡献插件

插件开发示例:
    from df_test_framework.infrastructure.plugins import hookimpl

    class MyPlugin:
        @hookimpl
        def df_providers(self, settings, logger):
            return {"my_service": MyService()}

        @hookimpl
        def df_http_middlewares(self, settings):
            return [MyMiddleware()]
"""

__all__: list[str] = []
