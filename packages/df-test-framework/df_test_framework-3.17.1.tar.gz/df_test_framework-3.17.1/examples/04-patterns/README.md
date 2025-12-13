# 设计模式示例

本目录包含Builder和Repository设计模式的使用示例。

## 📋 示例列表

### 1. Repository模式 (`repository_pattern.py`)
演示如何使用Repository模式封装数据访问。

**功能展示**:
- 继承BaseRepository
- 实现数据访问方法
- 封装查询逻辑

**运行**:
```bash
python examples/04-patterns/repository_pattern.py
```

### 2. Builder模式 (`builder_pattern.py`)
演示如何使用Builder模式构建测试数据。

**功能展示**:
- 使用DictBuilder
- 自定义Builder
- 链式调用

**运行**:
```bash
python examples/04-patterns/builder_pattern.py
```

### 3. 组合使用 (`combined_patterns.py`)
演示如何组合使用多种设计模式。

**功能展示**:
- Repository + Builder
- 完整的数据流
- 最佳实践

**运行**:
```bash
python examples/04-patterns/combined_patterns.py
```

## 🎯 学习路径

1. 先学习Builder模式构建数据
2. 再学习Repository模式封装数据访问
3. 最后看组合示例了解完整流程

## 📚 相关文档

- [用户指南 - 使用示例](../../docs/user-guide/examples.md)
- [架构设计](../../docs/architecture/overview.md)

---

**返回**: [示例首页](../README.md)
