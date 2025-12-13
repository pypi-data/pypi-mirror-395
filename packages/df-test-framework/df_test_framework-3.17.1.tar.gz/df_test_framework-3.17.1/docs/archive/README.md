# 文档归档

本目录存放框架历史文档和问题记录。

## 📁 目录结构

```
archive/
├── README.md              # 本文件
├── v1/                    # v1版本相关文档
│   ├── README.md
│   ├── architecture.md    # v1架构设计
│   ├── best-practices.md  # v1最佳实践
│   ├── optimization-report.md
│   └── ...
├── reports/               # 历史评审与修复报告
└── issues/                # 历史问题记录
    ├── README.md
    └── summary.md         # 问题汇总
```

## 📚 归档内容

### v1版本文档

v1版本的架构设计、最佳实践和优化报告等历史文档。

- [v1 架构设计](v1/architecture.md)
- [v1 最佳实践](v1/best-practices.md)
- [优化报告](v1/optimization-report.md)

这些文档记录了框架的演进历史，对理解v2的设计决策有参考价值。

### 问题记录

框架开发过程中遇到的问题和解决方案记录。

- [问题汇总](issues/summary.md)

包含：
- 循环导入问题
- 类型检查问题
- 性能优化问题
- 配置管理问题

### 历史报告

框架在 v2/v3 重构期间形成的评审、修复报告等总结材料。

- [代码审查报告](reports/CODE_REVIEW_REPORT.md)
- [修复总结](reports/FIX_SUMMARY.md)
- [功能实现审计](reports/FEATURE_IMPLEMENTATION_AUDIT.md)
- [HTTP 调试集成修复记录](reports/HTTP_DEBUG_INTEGRATION_FIX.md)
- [DB 调试集成修复记录](reports/DB_DEBUG_INTEGRATION_FIX.md)

这类文档记录了决策背景、问题修复过程以及落地验证，供日后追溯质量基线。

## 🎯 使用场景

### 1. 了解演进历史

查看v1文档了解框架如何演进到当前版本：

```
v1 (2023-2024) → v2 (2025+)
- 目录重组
- 配置系统升级
- 扩展系统重构
```

### 2. 问题排查参考

遇到问题时查看历史问题记录：

```
问题: 循环导入错误
解决: 使用TYPE_CHECKING条件导入
文档: issues/summary.md
```

### 3. 迁移参考

从v1迁移到v2时参考架构对比：

```
v1/architecture.md    # 旧架构
↓
../architecture/v2-design.md  # 新架构
↓
../migration/from-v1-to-v2.md  # 迁移指南
```

## 📖 文档说明

### v1文档状态

- ⚠️ **已过时**: v1文档仅供参考，不建议在新项目中使用
- 📚 **历史价值**: 记录了架构演进和设计决策
- 🔗 **交叉引用**: v2文档会引用v1中的相关内容

### 问题记录状态

- ✅ **已解决**: 大部分问题已在v2中修复
- 📝 **持续更新**: 新问题会继续记录
- 🔍 **可搜索**: 按问题类型和关键字查找

## 🔗 相关资源

### 当前文档
- [v2架构设计](../architecture/overview.md)
- [迁移指南](../migration/from-v1-to-v2.md)
- [API参考](../api-reference/README.md)

### 历史文档
- [v1架构](v1/README.md)
- [问题汇总](issues/README.md)

## 📌 注意事项

1. **不要基于v1文档开发**: 使用最新的v2文档
2. **问题已修复**: 历史问题大多已在v2中解决
3. **仅供参考**: 归档文档用于了解历史，不作为规范

---

**返回**: [文档首页](../README.md)
