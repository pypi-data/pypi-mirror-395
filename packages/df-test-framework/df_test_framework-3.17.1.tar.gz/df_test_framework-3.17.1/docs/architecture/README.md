# 架构设计文档

深入了解DF Test Framework架构设计和实现原理。

## 📚 v3.0 架构文档（当前版本）

### 核心文档
1. **[V3 架构设计](V3_ARCHITECTURE.md)** ⭐ - v3.0核心架构方案
   - 核心设计决策
   - 按交互模式分类的能力层
   - databases扁平化设计
   - 能力层与测试类型层解耦
   - 扩展性验证

2. **[V3 实施指南](V3_IMPLEMENTATION.md)** - v3.0实施步骤
   - Phase-by-Phase实施计划
   - 目录结构对照表
   - 验证清单
   - 常见问题处理

3. **[v2 → v3 迁移指南](../migration/v2-to-v3.md)** - 用户迁移文档
   - 导入路径变更
   - 迁移步骤
   - 代码示例

### 质量保证文档
4. **[架构审计报告](ARCHITECTURE_AUDIT.md)** - 文档与代码一致性审计
   - 9个不一致问题发现
   - P0/P1/P2优先级分类
   - 修正建议和验证

5. **[审计验证报告](../reports/AUDIT_VERIFICATION_REPORT.md)** - 最终验证确认
   - 所有审计问题逐项验证
   - 100%一致性确认
   - 测试通过验证

6. **[完整重构报告](../reports/V3_REFACTORING_COMPLETE.md)** - v3重构全过程总结
   - 重构目标与成果
   - 核心架构突破
   - 实施过程记录
   - 质量保证数据

### 未来规划
7. **[未来增强功能](FUTURE_ENHANCEMENTS.md)** - 基于v3架构的后续增强
   - 早期遗漏点重新评估
   - P2优先级增强建议
   - 实施计划和检查清单

### 演进过程归档
- **[archive/](archive/)** - v3架构演进过程文档（已归档）

---

## 📚 v2.x 架构文档（历史版本）

1. **[架构总览](overview.md)** - 框架整体架构设计
   - 分层架构
   - 核心组件
   - 依赖关系
   - 设计模式

## 🏗️ 架构原则

### 1. 分层架构

框架采用清晰的分层设计：

```
┌─────────────────────────────────────┐
│   Testing Layer (测试支持层)        │
│   - Fixtures                        │
│   - Plugins                         │
├─────────────────────────────────────┤
│   Patterns Layer (设计模式层)       │
│   - Builders                        │
│   - Repositories                    │
├─────────────────────────────────────┤
│   Core Layer (核心功能层)           │
│   - HTTP / Database / Redis         │
├─────────────────────────────────────┤
│   Infrastructure Layer (基础设施层)  │
│   - Bootstrap / Runtime / Config    │
└─────────────────────────────────────┘
```

### 2. 核心设计模式

- **Builder模式**: 构建测试数据
- **Repository模式**: 数据访问抽象
- **Provider模式**: 依赖注入
- **Plugin模式**: 功能扩展
- **Hook模式**: 生命周期管理

### 3. 设计原则

- **单一职责**: 每个模块只负责一件事
- **依赖倒置**: 依赖抽象而非具体实现
- **开闭原则**: 对扩展开放，对修改关闭
- **接口隔离**: 使用协议和抽象基类
- **显式优于隐式**: 配置和行为明确可见

## 🔑 核心概念

### Bootstrap启动流程

```python
Bootstrap()
  .with_settings(Settings)      # 1. 加载配置
  .with_providers(providers)    # 2. 注册提供者
  .with_logger(logger)          # 3. 配置日志
  .with_extensions(extensions)  # 4. 加载扩展
  .build()                      # 5. 构建应用
  .run()                        # 6. 创建运行时
```

### RuntimeContext依赖管理

RuntimeContext通过Provider模式管理所有资源：

```python
runtime.http_client()    # 获取HTTP客户端
runtime.database()       # 获取数据库连接
runtime.redis_client()   # 获取Redis客户端
```

### Extension扩展机制

通过pluggy的Hook系统实现：

```python
@hookimpl
def before_http_request(request):
    # 在HTTP请求前执行
    pass

@hookimpl
def after_http_response(response):
    # 在HTTP响应后执行
    pass
```

## 📊 模块依赖关系

```
┌─────────────┐
│  Bootstrap  │
└──────┬──────┘
       │
       ├──→ Settings (配置)
       ├──→ Providers (提供者)
       ├──→ Logger (日志)
       └──→ Extensions (扩展)
              │
              ├──→ Core (HTTP/DB/Redis)
              ├──→ Patterns (Builder/Repo)
              └──→ Testing (Fixtures/Plugins)
```

## 🎯 技术选型

### 核心依赖

- **httpx**: 现代异步HTTP客户端
- **pydantic**: 数据验证和配置管理
- **sqlalchemy**: 数据库ORM
- **redis**: Redis客户端
- **loguru**: 结构化日志
- **pluggy**: 插件系统
- **pytest**: 测试框架

### 为什么选择这些技术？

- **httpx vs requests**: 支持异步、HTTP/2、更现代的API
- **pydantic**: 类型安全、自动验证、环境变量支持
- **loguru**: 简单易用、结构化日志、自动颜色
- **pluggy**: pytest使用的插件系统，成熟稳定

## 🔗 相关资源

- [架构总览](overview.md)
- [API参考](../api-reference/README.md)
- [用户指南](../user-guide/README.md)

---

**返回**: [文档首页](../README.md)
