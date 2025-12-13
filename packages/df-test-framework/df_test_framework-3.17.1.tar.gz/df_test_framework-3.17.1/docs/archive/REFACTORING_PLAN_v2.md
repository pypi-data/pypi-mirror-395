# DF Test Framework v2.0 完全重构方案

> 执行时间：2025-10-31
> 方案类型：方案B - 完全重构（不保留向后兼容）
> 执行者：Claude Code

---

## 一、重构目标

### 🎯 核心目标
1. **现代化架构**：完全采用v2架构，清除所有v1遗留代码
2. **清晰的模块分层**：基础设施、核心功能、设计模式、测试支持分离
3. **最佳实践**：符合Python项目组织最佳实践
4. **文档完善**：结构化文档、完整示例、清晰的API参考

### 🚫 不兼容声明
- **不保留v1接口**：所有v1遗留接口完全移除
- **导入路径变更**：所有模块导入路径将重新组织
- **gift-card-test需要适配**：测试项目需要重新适配新框架

---

## 二、新的目录结构

### 📁 源码结构
```
src/df_test_framework/
├── __init__.py                     # 精简的顶级导出
│
├── infrastructure/                 # 基础设施层
│   ├── __init__.py
│   ├── bootstrap/                  # 启动引导
│   │   ├── __init__.py
│   │   └── bootstrap.py
│   ├── runtime/                    # 运行时上下文
│   │   ├── __init__.py
│   │   └── context.py
│   ├── config/                     # 配置系统
│   │   ├── __init__.py
│   │   ├── schema.py               # 配置模型
│   │   ├── pipeline.py             # 配置管线
│   │   ├── sources.py              # 配置源
│   │   └── manager.py              # 配置管理器
│   ├── logging/                    # 日志系统
│   │   ├── __init__.py
│   │   ├── logger.py               # 日志实现
│   │   └── strategies.py           # 日志策略
│   └── providers/                  # 资源提供者
│       ├── __init__.py
│       └── registry.py
│
├── core/                           # 核心功能层
│   ├── __init__.py
│   ├── http/                       # HTTP客户端
│   │   ├── __init__.py
│   │   ├── client.py               # 重命名：http_client.py → client.py
│   │   └── base_api.py
│   ├── database/                   # 数据库
│   │   ├── __init__.py
│   │   └── database.py
│   └── redis/                      # Redis
│       ├── __init__.py
│       └── client.py
│
├── patterns/                       # 设计模式层
│   ├── __init__.py
│   ├── builders/                   # Builder模式
│   │   ├── __init__.py
│   │   └── base.py
│   └── repositories/               # Repository模式
│       ├── __init__.py
│       ├── base.py
│       └── query_builder.py
│
├── testing/                        # 测试支持层
│   ├── __init__.py
│   ├── fixtures/                   # Pytest Fixtures
│   │   ├── __init__.py
│   │   ├── core.py
│   │   ├── cleanup.py
│   │   └── monitoring.py
│   ├── plugins/                    # Pytest插件
│   │   ├── __init__.py
│   │   ├── allure.py
│   │   └── markers.py
│   └── assertions/                 # 断言辅助（新增）
│       ├── __init__.py
│       └── helpers.py
│
├── extensions/                     # 扩展系统
│   ├── __init__.py
│   ├── core/                       # 扩展核心
│   │   ├── __init__.py
│   │   ├── hooks.py
│   │   └── manager.py
│   └── builtin/                    # 内置扩展
│       ├── __init__.py
│       └── monitoring/
│           ├── __init__.py
│           ├── api_tracker.py
│           └── db_monitor.py
│
├── models/                         # 数据模型
│   ├── __init__.py
│   ├── base.py
│   └── types.py
│
├── utils/                          # 工具函数
│   ├── __init__.py
│   ├── decorator.py
│   ├── performance.py
│   ├── data_generator.py
│   ├── assertion.py
│   └── common.py
│
├── ui/                             # UI测试（预留）
│   ├── __init__.py
│   ├── base_page.py
│   ├── browser_manager.py
│   └── locators.py
│
└── cli/                            # CLI工具
    ├── __init__.py
    └── commands.py
```

### 📚 文档结构
```
docs/
├── README.md                       # 文档导航
│
├── getting-started/                # 入门文档
│   ├── README.md
│   ├── installation.md             # 安装指南
│   ├── quickstart.md               # 快速开始（10分钟）
│   └── tutorial.md                 # 完整教程（30分钟）
│
├── user-guide/                     # 用户指南（重命名：guides → user-guide）
│   ├── README.md
│   ├── configuration.md            # 配置管理
│   ├── http-client.md              # HTTP客户端使用
│   ├── database.md                 # 数据库操作
│   ├── patterns.md                 # 设计模式
│   ├── testing.md                  # 测试编写
│   ├── extensions.md               # 扩展开发
│   └── best-practices.md           # 最佳实践
│
├── api-reference/                  # API参考
│   ├── README.md
│   ├── infrastructure.md           # 基础设施API
│   ├── core.md                     # 核心功能API
│   ├── patterns.md                 # 模式API
│   ├── testing.md                  # 测试API
│   └── extensions.md               # 扩展API
│
├── architecture/                   # 架构文档
│   ├── README.md
│   ├── overview.md                 # 架构总览
│   ├── design-principles.md        # 设计原则
│   ├── bootstrap-flow.md           # 启动流程
│   ├── provider-system.md          # Provider体系
│   └── extension-system.md         # 扩展系统
│
├── migration/                      # 迁移指南
│   ├── README.md
│   └── from-v1-to-v2.md           # v1到v2迁移
│
└── archive/                        # 历史文档归档（重命名：history → archive）
    ├── README.md
    ├── v1/
    │   ├── architecture.md
    │   ├── best-practices.md
    │   ├── optimization-report.md
    │   └── issues-summary.md
    └── changelog-v1.md
```

### 📝 示例代码
```
examples/
├── README.md                       # 示例索引
│
├── 01-basic/                       # 基础示例
│   ├── README.md
│   ├── http_client_usage.py        # HTTP客户端
│   ├── database_operations.py      # 数据库操作
│   └── redis_cache.py              # Redis缓存
│
├── 02-bootstrap/                   # Bootstrap示例
│   ├── README.md
│   ├── minimal_bootstrap.py        # 最小配置
│   ├── custom_providers.py         # 自定义Provider
│   └── with_plugins.py             # 使用插件
│
├── 03-testing/                     # 测试示例
│   ├── README.md
│   ├── conftest.py                 # Pytest配置
│   ├── test_api.py                 # API测试
│   ├── test_database.py            # 数据库测试
│   └── test_with_fixtures.py       # Fixture使用
│
├── 04-patterns/                    # 设计模式示例
│   ├── README.md
│   ├── repository_pattern.py       # Repository模式
│   ├── builder_pattern.py          # Builder模式
│   └── combined_patterns.py        # 组合使用
│
└── 05-extensions/                  # 扩展示例
    ├── README.md
    ├── custom_extension.py         # 自定义扩展
    ├── monitoring_extension.py     # 监控扩展
    └── custom_provider.py          # 自定义Provider
```

---

## 三、关键变更

### 🔄 模块重命名映射

| 旧路径 | 新路径 | 说明 |
|--------|--------|------|
| `df_test_framework.core.logger` | `df_test_framework.infrastructure.logging.logger` | 移入基础设施层 |
| `df_test_framework.core.http_client` | `df_test_framework.core.http.client` | 重组为子模块 |
| `df_test_framework.core.database` | `df_test_framework.core.database.database` | 重组为子模块 |
| `df_test_framework.core.redis_client` | `df_test_framework.core.redis.client` | 重组为子模块 |
| `df_test_framework.builders` | `df_test_framework.patterns.builders` | 移入patterns层 |
| `df_test_framework.repositories` | `df_test_framework.patterns.repositories` | 移入patterns层 |
| `df_test_framework.monitoring` | `df_test_framework.extensions.builtin.monitoring` | 移入扩展层 |
| `df_test_framework.plugins` | `df_test_framework.testing.plugins` | 移入testing层 |
| `df_test_framework.config` | `df_test_framework.infrastructure.config` | 移入基础设施层 |
| `df_test_framework.logging` | `df_test_framework.infrastructure.logging` | 移入基础设施层 |
| `df_test_framework.bootstrap` | `df_test_framework.infrastructure.bootstrap` | 移入基础设施层 |
| `df_test_framework.runtime` | `df_test_framework.infrastructure.runtime` | 移入基础设施层 |
| `df_test_framework.providers` | `df_test_framework.infrastructure.providers` | 移入基础设施层 |
| `df_test_framework.extensions` | `df_test_framework.extensions.core` | 区分core和builtin |
| `df_test_framework.fixtures` | `df_test_framework.testing.fixtures` | 移入testing层 |

### ❌ 移除的接口

1. **v1遗留函数**：
   - `setup_logger()` - 使用 `LoguruStructuredStrategy` 替代

2. **已废弃的模块**：
   - 所有标记为deprecated的接口

3. **清理的文件**：
   - `__pycache__/` 所有缓存
   - `.pyc` 编译文件

---

## 四、执行步骤

### Phase 1: 准备工作
- [x] 创建重构方案文档
- [ ] 创建详细任务清单
- [ ] 备份当前代码（git commit）

### Phase 2: 源码重组
- [ ] 创建新的目录结构
- [ ] 移动模块到新位置
- [ ] 重命名文件
- [ ] 更新所有 `__init__.py`

### Phase 3: 更新导入
- [ ] 更新模块内部导入
- [ ] 更新测试代码导入
- [ ] 更新顶级 `__init__.py` 导出

### Phase 4: 清理遗留
- [ ] 删除旧目录
- [ ] 删除v1接口
- [ ] 清理缓存文件

### Phase 5: 文档重组
- [ ] 重组文档目录
- [ ] 移动文档到新位置
- [ ] 创建新的导航文档

### Phase 6: 创建示例
- [ ] 创建基础示例
- [ ] 创建Bootstrap示例
- [ ] 创建测试示例
- [ ] 创建模式示例
- [ ] 创建扩展示例

### Phase 7: 更新主文档
- [ ] 更新 README.md
- [ ] 更新 CHANGELOG.md
- [ ] 创建 MIGRATION.md
- [ ] 更新 pyproject.toml

### Phase 8: 验证
- [ ] 运行框架自身测试
- [ ] 检查所有导入
- [ ] 验证文档链接
- [ ] 生成API文档

---

## 五、注意事项

### ⚠️ 破坏性变更
1. **所有导入路径变更**
2. **移除setup_logger等v1接口**
3. **gift-card-test需要完全重写导入**

### ✅ 测试策略
1. 先完成重构
2. 确保框架自身可用
3. 再适配gift-card-test

### 📋 后续工作
1. 适配gift-card-test项目
2. 更新CI/CD配置
3. 发布v2.0.0正式版

---

## 六、预期结果

### 🎯 重构完成后
- ✅ 清晰的模块分层
- ✅ 现代化的目录结构
- ✅ 完整的文档体系
- ✅ 丰富的示例代码
- ✅ 纯粹的v2架构

### 📊 质量指标
- 模块职责单一性：⭐⭐⭐⭐⭐
- 代码可维护性：⭐⭐⭐⭐⭐
- 文档完整性：⭐⭐⭐⭐⭐
- 新手友好度：⭐⭐⭐⭐⭐

---

**执行批准**: 已确认，立即执行完全重构
**风险接受**: 不保留向后兼容，gift-card-test将重新适配
