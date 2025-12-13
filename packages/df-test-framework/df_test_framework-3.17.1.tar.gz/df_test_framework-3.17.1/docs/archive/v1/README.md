# v1 版本文档归档

本目录存放DF Test Framework v1版本的历史文档。

## 📋 文档列表

### 架构设计

1. **[架构设计文档](architecture.md)**
   - v1版本的整体架构设计
   - 模块划分和职责
   - 设计模式应用

### 开发指南

2. **[项目开发最佳实践](best-practices.md)**
   - v1版本的最佳实践
   - 代码规范
   - 测试策略

### 性能优化

3. **[优化报告](optimization-report.md)**
   - v1版本的性能优化记录
   - 优化方案和效果
   - 性能指标

### 其他文档

4. **[循环引用问题修复](circular-import-fix.md)**
   - 循环导入问题分析
   - 解决方案

5. **[缺失导入修复](missing-imports-fix.md)**
   - 导入路径修复记录

## 🔄 v1 → v2 主要变更

### 1. 目录结构

#### v1 结构
```
src/df_test_framework/
├── infrastructure/
│   ├── bootstrap/
│   │   └── bootstrap.py
│   ├── runtime/
│   │   └── runtime.py
│   └── ...
├── core/
│   ├── http/
│   │   └── http_client.py
│   └── ...
└── ...
```

#### v2 结构
```
src/df_test_framework/
├── infrastructure/
│   ├── bootstrap.py     # 扁平化
│   ├── runtime.py
│   └── ...
├── core/
│   ├── http.py          # 扁平化
│   └── ...
└── ...
```

### 2. 导入路径

#### v1 导入
```python
from df_test_framework.infrastructure.bootstrap.bootstrap import Bootstrap
```

#### v2 导入
```python
from df_test_framework import Bootstrap
```

### 3. 配置系统

#### v1 配置
```python
class Config:
    env_prefix = "APP_"
```

#### v2 配置
```python
model_config = {
    "env_prefix": "APP_"
}
```

### 4. 扩展系统

#### v1 扩展
- 基于装饰器的监控系统
- 紧耦合的扩展机制

#### v2 扩展
- 基于pluggy的Hook系统
- 松耦合的插件机制

## 📊 版本对比

| 特性 | v1 | v2 |
|------|----|----|
| Python版本 | 3.8+ | 3.10+ |
| Pydantic | v1 | v2 |
| 目录深度 | 3-4层 | 2层 |
| 导入复杂度 | 高 | 低 |
| 扩展系统 | 装饰器 | Pluggy |
| 类型安全 | 部分 | 完整 |
| 文档完整度 | 中等 | 高 |

## 🎯 为什么升级到v2？

### v1存在的问题

1. **导入路径过深**: 影响开发效率
2. **配置系统老旧**: Pydantic v1已过时
3. **扩展机制复杂**: 难以维护和测试
4. **类型检查不完善**: 运行时错误较多
5. **文档分散**: 难以查找

### v2的改进

1. ✅ **简化导入**: 统一从顶层导入
2. ✅ **现代化配置**: Pydantic v2
3. ✅ **标准化扩展**: pluggy插件系统
4. ✅ **完整类型注解**: 减少运行时错误
5. ✅ **结构化文档**: 清晰的文档组织

## 🔗 相关资源

### 当前文档
- [v2架构设计](../../architecture/overview.md)
- [迁移指南](../../migration/from-v1-to-v2.md)
- [快速入门](../../getting-started/quickstart.md)

### 历史参考
- [v1架构设计](architecture.md)
- [v1最佳实践](best-practices.md)
- [问题汇总](../issues/summary.md)

## 📌 使用建议

1. **新项目**: 直接使用v2，不要参考v1文档
2. **旧项目迁移**: 参考[迁移指南](../../migration/from-v1-to-v2.md)
3. **了解历史**: 查看v1文档了解演进原因

---

**返回**: [归档首页](../README.md) | [文档首页](../../README.md)
