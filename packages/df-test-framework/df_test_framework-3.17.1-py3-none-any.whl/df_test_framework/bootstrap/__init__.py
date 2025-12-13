"""
Bootstrap 层 (Layer 4) - 框架引导和组装

职责:
- 框架初始化入口
- 服务工厂注册（Providers）
- 运行时上下文管理（RuntimeContext）

依赖规则:
- 可依赖 Layer 0-3 全部（引导层特权）
- 其他层不应依赖 bootstrap/

v3.16.0 架构重构:
- 从 infrastructure/ 提升为独立的 Layer 4
- 解决 infrastructure/ → capabilities/ 的依赖违规问题
"""

from .bootstrap import Bootstrap, BootstrapApp
from .providers import (
    Provider,
    ProviderRegistry,
    SingletonProvider,
    default_providers,
)
from .runtime import RuntimeBuilder, RuntimeContext

__all__ = [
    # Bootstrap
    "Bootstrap",
    "BootstrapApp",
    # Runtime
    "RuntimeContext",
    "RuntimeBuilder",
    # Providers
    "Provider",
    "SingletonProvider",
    "ProviderRegistry",
    "default_providers",
]
