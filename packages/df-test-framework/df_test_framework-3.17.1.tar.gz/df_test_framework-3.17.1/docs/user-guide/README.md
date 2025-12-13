# 用户指南

欢迎使用DF Test Framework用户指南！本指南提供完整的使用文档和最佳实践。

---

## 📚 文档目录

### 🚀 快速开始
- [快速参考](QUICK_REFERENCE.md) - 5分钟速查手册
- [使用手册](USER_MANUAL.md) - 完整使用手册
- [最佳实践](BEST_PRACTICES.md) - 最佳实践指南
- ⭐ [已验证最佳实践](VERIFIED_BEST_PRACTICES.md) - 基于真实项目验证（推荐）

### 📖 深入学习
- [配置管理](configuration.md) - 配置详解（待更新）
- [HTTP客户端](http-client.md) - HTTP客户端详解（待更新）
- [数据库操作](database.md) - 数据库操作详解（待更新）
- [扩展系统](extensions.md) - 扩展开发指南（待更新）

### 🎯 特定场景
- [API测试](api-testing.md) - API测试完整指南（待更新）
- [UI测试](ui-testing.md) - UI测试指南（待更新）
- [性能测试](performance-testing.md) - 性能测试指南（待更新）

---

## 🎓 学习路径

### 新手入门（第1-2天）

1. **快速开始** (30分钟)
   - 阅读 [快速参考](QUICK_REFERENCE.md)
   - 创建第一个测试项目
   - 运行示例测试

2. **基础使用** (2小时)
   - 阅读 [使用手册](USER_MANUAL.md)
   - 学习HTTP客户端使用
   - 学习数据库操作
   - 学习Fixtures使用

### 进阶学习（第3-5天）

3. **最佳实践** (3小时)
   - ⭐ **推荐**: 阅读 [已验证最佳实践](VERIFIED_BEST_PRACTICES.md)（100%准确）
   - 或阅读 [最佳实践](BEST_PRACTICES.md)（通用指南）
   - 学习项目结构规范
   - 学习API客户端封装
   - 学习测试数据管理

4. **设计模式** (2小时)
   - 学习Repository模式
   - 学习Builder模式
   - 学习Page Object模式（UI）

### 高级应用（第6-7天）

5. **扩展开发** (2小时)
   - 学习自定义扩展
   - 学习自定义中间件
   - 学习自定义插件

6. **性能优化** (1小时)
   - 学习并行测试
   - 学习资源复用
   - 学习性能调优

---

## 📊 文档速查

### 按主题查找

**配置相关**
- [快速参考 - 配置示例](QUICK_REFERENCE.md#⚙️-配置示例)
- [使用手册 - 配置管理](USER_MANUAL.md#3-配置管理)
- [最佳实践 - 配置管理](BEST_PRACTICES.md#2-配置管理最佳实践)

**HTTP客户端**
- [快速参考 - HTTP客户端](QUICK_REFERENCE.md#🌐-http客户端)
- [使用手册 - HTTP客户端](USER_MANUAL.md#4-http客户端)
- [最佳实践 - HTTP客户端](BEST_PRACTICES.md#3-http客户端使用最佳实践)

**数据库操作**
- [快速参考 - 数据库操作](QUICK_REFERENCE.md#💾-数据库操作)
- [使用手册 - 数据库操作](USER_MANUAL.md#5-数据库操作)
- [最佳实践 - 数据库操作](BEST_PRACTICES.md#4-数据库操作最佳实践)

**测试数据管理**
- [快速参考 - Builder模式](QUICK_REFERENCE.md#🏗️-builder模式)
- [使用手册 - 测试数据管理](USER_MANUAL.md#7-测试数据管理)
- [最佳实践 - 测试数据管理](BEST_PRACTICES.md#5-测试数据管理最佳实践)

**Fixtures**
- [快速参考 - Pytest Fixtures](QUICK_REFERENCE.md#🧪-pytest-fixtures)
- [使用手册 - Fixtures使用](USER_MANUAL.md#8-fixtures使用)
- [最佳实践 - Fixtures使用](BEST_PRACTICES.md#6-fixtures使用最佳实践)

**Allure报告**
- [快速参考 - Allure报告](QUICK_REFERENCE.md#📊-allure报告)
- [使用手册 - Allure报告](USER_MANUAL.md#11-allure报告)
- [最佳实践 - 测试用例组织](BEST_PRACTICES.md#9-测试用例组织最佳实践)

---

## 🎯 常见任务

### 我想...

**创建新项目**
→ [快速参考 - 快速开始](QUICK_REFERENCE.md#🚀-快速开始)

**封装API客户端**
→ [最佳实践 - HTTP客户端](BEST_PRACTICES.md#3-http客户端使用最佳实践)

**避免测试数据污染**
→ [最佳实践 - 测试数据管理](BEST_PRACTICES.md#5-测试数据管理最佳实践)

**添加认证Token**
→ [快速参考 - 添加认证](QUICK_REFERENCE.md#添加认证)

**使用数据库事务**
→ [快速参考 - 事务自动回滚](QUICK_REFERENCE.md#事务自动回滚推荐)

**构建测试数据**
→ [快速参考 - Builder模式](QUICK_REFERENCE.md#🏗️-builder模式)

**生成测试报告**
→ [快速参考 - 常用命令](QUICK_REFERENCE.md#⚡-常用命令)

**调试测试**
→ [快速参考 - 调试](QUICK_REFERENCE.md#🔍-调试)

---

## 📋 文档说明

### 文档定位

| 文档 | 目标读者 | 预计阅读时间 | 用途 |
|------|---------|-------------|------|
| [快速参考](QUICK_REFERENCE.md) | 所有用户 | 5-10分钟 | 快速查询、速查手册 |
| [使用手册](USER_MANUAL.md) | 初学者 | 1-2小时 | 系统学习、完整教程 |
| [最佳实践](BEST_PRACTICES.md) | 有经验用户 | 2-3小时 | 提升质量、规范代码 |
| ⭐ [已验证最佳实践](VERIFIED_BEST_PRACTICES.md) | 所有用户 | 1-2小时 | 实战案例、100%准确 |

### 版本说明

- **v1.0** (2025-11-04) - 初始版本，覆盖v3.0.0框架核心功能

### 更新计划

以下文档计划在后续版本补充：

- [ ] configuration.md - 配置详解
- [ ] http-client.md - HTTP客户端详解
- [ ] database.md - 数据库操作详解
- [ ] extensions.md - 扩展开发
- [ ] api-testing.md - API测试指南
- [ ] ui-testing.md - UI测试指南
- [ ] performance-testing.md - 性能测试指南

---

## 🔗 相关资源

### 框架文档
- [V3架构设计](../architecture/V3_ARCHITECTURE.md) - 核心架构
- [V3实施指南](../architecture/V3_IMPLEMENTATION.md) - 实施步骤
- [v2→v3迁移](../migration/v2-to-v3.md) - 迁移指南

### API文档
- [API参考](../api-reference/README.md) - 完整API文档

### 示例代码
- [基础示例](../../examples/01-basic/) - HTTP、数据库、Redis
- [Bootstrap示例](../../examples/02-bootstrap/) - 启动配置
- [测试示例](../../examples/03-testing/) - Pytest测试

### 快速入门
- [安装指南](../getting-started/installation.md)
- [快速开始](../getting-started/quickstart.md)
- [30分钟教程](../getting-started/tutorial.md)

---

## 💡 反馈建议

如果您在使用过程中遇到问题或有改进建议：

1. 查看 [常见问题](USER_MANUAL.md#12-常见问题)
2. 查阅 [API参考文档](../api-reference/README.md)
3. 提交 [GitHub Issue](https://github.com/yourorg/test-framework/issues)

---

**DF QA Team** © 2025
