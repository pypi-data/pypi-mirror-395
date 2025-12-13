# DF Test Framework 示例代码

> **框架版本**: df-test-framework v3.7.0
> **最后更新**: 2025-11-24
> **示例总数**: 31个

---

## 📚 示例目录

### 01-basic/ - 基础用法
基础API使用示例，适合初学者。

| 示例文件 | 说明 | 关键API |
|---------|------|---------|
| **http_client_usage.py** | HTTP客户端基础用法 | `http_client()`, GET/POST/PUT/DELETE |
| **database_operations.py** | 数据库基础操作 | `database()`, query/insert/update/delete |
| **redis_cache.py** | Redis缓存操作 | `redis_client()`, set/get/delete |

**适用人群**: 初学者
**前置知识**: 无
**学习时间**: 20分钟

---

### 02-bootstrap/ - 框架启动和配置
框架初始化和配置相关示例。

| 示例文件 | 说明 | 关键API |
|---------|------|---------|
| **minimal_bootstrap.py** | 最小化启动配置 | `Bootstrap()`, `with_settings()` |
| **custom_settings.py** | 自定义Settings | `FrameworkSettings`, Pydantic字段 |
| **custom_providers.py** | 自定义Provider | `ProviderRegistry`, 依赖注入 |
| **with_extensions.py** | 使用扩展 | `Extension`, Pluggy hooks |

**适用人群**: 进阶用户
**前置知识**: 基础用法
**学习时间**: 30分钟

---

### 03-testing/ - 测试相关
Pytest测试编写示例。

| 示例文件 | 说明 | 关键API |
|---------|------|---------|
| **conftest.py** | Pytest配置 | pytest fixtures, 插件配置 |
| **test_api.py** | API测试示例 | `http_client` fixture |
| **test_database.py** | 数据库测试 | `database` fixture, 事务 |
| **test_with_fixtures.py** | 使用框架fixtures | `runtime_ctx`, `http_client`, `database` |

**适用人群**: 测试工程师
**前置知识**: Pytest基础
**学习时间**: 30分钟

---

### 04-patterns/ - 设计模式
常用设计模式实现示例。

| 示例文件 | 说明 | 关键API |
|---------|------|---------|
| **builder_pattern.py** | Builder模式 | `BaseBuilder`, 链式调用 |
| **repository_pattern.py** | Repository模式 | `BaseRepository`, 数据访问封装 |
| **combined_patterns.py** | 组合使用多种模式 | Builder + Repository |

**适用人群**: 进阶用户
**前置知识**: 设计模式基础
**学习时间**: 40分钟

---

### 05-extensions/ - 扩展系统
框架扩展开发示例。

| 示例文件 | 说明 | 关键API |
|---------|------|---------|
| **custom_extension.py** | 创建自定义扩展 | `Extension基类`, hook实现 |
| **monitoring_extension.py** | 监控扩展 | 性能追踪, 慢查询监控 |
| **data_factory_extension.py** | 数据工厂扩展 | 测试数据生成 |
| **environment_validator_extension.py** | 环境验证扩展 | 环境检查, 依赖验证 |

**适用人群**: 高级用户, 框架贡献者
**前置知识**: Pluggy插件系统
**学习时间**: 1小时

---

### 06-ui-testing/ - UI自动化测试
Playwright UI测试示例。

| 示例文件 | 说明 | 关键API |
|---------|------|---------|
| **basic_ui_test.py** | 基础UI测试 | `browser_manager()`, page操作 |
| **page_object_example.py** | Page Object模式 | 页面对象封装 |
| **conftest.py** | UI测试配置 | Playwright fixtures |

**适用人群**: UI测试工程师
**前置知识**: Playwright基础
**学习时间**: 30分钟

---

### 07-v35-features/ - v3.5新特性 ⭐
v3.5.0版本新特性完整示例。

| 示例文件 | 说明 | 关键特性 |
|---------|------|---------|
| **[01_configurable_interceptors.py](07-v35-features/01_configurable_interceptors.py)** ⭐ | 配置化拦截器 | 签名/Token/AdminAuth拦截器 |
| **[02_profile_configuration.py](07-v35-features/02_profile_configuration.py)** ⭐ | Profile环境配置 | .env.{profile}, 多环境管理 |
| **[03_runtime_overrides.py](07-v35-features/03_runtime_overrides.py)** ⭐ | 运行时配置覆盖 | `with_overrides()`, 测试隔离 |
| **[04_observability.py](07-v35-features/04_observability.py)** ⭐ | 可观测性集成 | ObservabilityLogger, 日志配置 |

**适用人群**: 所有用户（v3.5必看）
**前置知识**: 基础用法
**学习时间**: 1小时
**详细文档**: [07-v35-features/README.md](07-v35-features/README.md)

---

### 08-v37-features/ - v3.7新特性 🔥🆕
v3.7.0版本新特性完整示例 - Unit of Work模式。

| 示例文件 | 说明 | 关键特性 |
|---------|------|---------|
| **[01_unit_of_work_basics.py](08-v37-features/01_unit_of_work_basics.py)** 🔥 | UoW基础用法 | 事务管理、显式commit、自动rollback |
| **[02_repository_v37.py](08-v37-features/02_repository_v37.py)** 🔥 | Repository v3.7变更 | Session替代Database、迁移指南 |
| **[03_auto_rollback_testing.py](08-v37-features/03_auto_rollback_testing.py)** 🔥 | 自动数据回滚 | 测试隔离、零清理代码 |
| **[04_multi_repository_transactions.py](08-v37-features/04_multi_repository_transactions.py)** 🔥 | 多Repository事务 | 事务一致性、原子性保证 |
| **[05_project_uow.py](08-v37-features/05_project_uow.py)** 🔥 | 项目级UoW封装 | 最佳实践、类型安全、IDE自动补全 |
| **[06_exception_handling_with_uow.py](08-v37-features/06_exception_handling_with_uow.py)** 🔥 | 异常场景测试 | Repository直接修改状态、灵活测试 |

**适用人群**: 所有用户（v3.7必看！）
**前置知识**: 基础用法、v3.5特性
**学习时间**: 1-2小时
**详细文档**: [08-v37-features/README.md](08-v37-features/README.md)
**迁移指南**: [v3.6→v3.7迁移指南](../docs/migration/v3.6-to-v3.7.md)

---

## 🚀 快速开始

### 方式一：按主题学习（推荐新手）

1. **第一步：基础用法** (20分钟)
   ```bash
   # HTTP客户端
   python examples/01-basic/http_client_usage.py

   # 数据库操作
   python examples/01-basic/database_operations.py

   # Redis缓存
   python examples/01-basic/redis_cache.py
   ```

2. **第二步：v3.7新特性** 🔥🆕 (1-2小时) **推荐优先学习**
   ```bash
   # UoW基础用法
   python examples/08-v37-features/01_unit_of_work_basics.py

   # Repository v3.7变更
   python examples/08-v37-features/02_repository_v37.py

   # 自动数据回滚（最强特性）
   python examples/08-v37-features/03_auto_rollback_testing.py

   # 多Repository事务一致性
   python examples/08-v37-features/04_multi_repository_transactions.py

   # 项目级UoW封装（最佳实践）
   python examples/08-v37-features/05_project_uow.py

   # 异常场景测试
   python examples/08-v37-features/06_exception_handling_with_uow.py
   ```

3. **第三步：v3.5特性** ⭐ (1小时)
   ```bash
   # 配置化拦截器
   python examples/07-v35-features/01_configurable_interceptors.py

   # Profile环境配置
   ENV=dev python examples/07-v35-features/02_profile_configuration.py

   # 运行时配置覆盖
   python examples/07-v35-features/03_runtime_overrides.py

   # 可观测性
   APP_LOGGING__LEVEL=DEBUG python examples/07-v35-features/04_observability.py
   ```

4. **第四步：设计模式** (40分钟)
   ```bash
   # Repository模式
   python examples/04-patterns/repository_pattern.py

   # Builder模式
   python examples/04-patterns/builder_pattern.py
   ```

5. **第五步：测试编写** (30分钟)
   ```bash
   cd examples/03-testing
   pytest -v
   ```

### 方式二：按角色学习

#### 测试工程师路径
1. `01-basic/` - 基础API使用
2. `07-v35-features/` - v3.5新特性（必看）
3. `03-testing/` - 测试编写
4. `04-patterns/` - 设计模式

#### UI测试工程师路径
1. `01-basic/http_client_usage.py` - HTTP基础
2. `07-v35-features/` - v3.5新特性（必看）
3. `06-ui-testing/` - UI测试
4. `03-testing/` - 测试框架集成

#### 框架开发者路径
1. `02-bootstrap/` - 框架启动
2. `07-v35-features/` - v3.5新特性（必看）
3. `05-extensions/` - 扩展系统
4. `04-patterns/` - 设计模式

---

## 📖 示例代码约定

### 目录命名规范
- `01-basic/` - 基础示例
- `02-bootstrap/` - 启动配置
- `03-testing/` - 测试相关
- `04-patterns/` - 设计模式
- `05-extensions/` - 扩展系统
- `06-ui-testing/` - UI测试
- `07-v35-features/` - v3.5新特性

### 文件命名规范
- 使用小写和下划线：`http_client_usage.py`
- v3.5示例使用数字前缀：`01_configurable_interceptors.py`

### 代码风格
- 每个示例都是独立可运行的Python文件
- 包含详细的中文注释
- 使用`if __name__ == "__main__"`包装
- 输出清晰的示例说明

---

## ⚙️ 运行要求

### 环境要求
- Python 3.12+
- df-test-framework v3.5.0+

### 安装依赖
```bash
# 使用uv（推荐）
pip install uv
uv pip install df-test-framework

# 或使用pip
pip install df-test-framework
```

### 运行示例
```bash
# 直接运行单个示例
python examples/01-basic/http_client_usage.py

# 运行测试示例
cd examples/03-testing
pytest -v

# 运行UI测试示例（需要安装Playwright）
playwright install
pytest examples/06-ui-testing -v
```

---

## 💡 学习建议

### 新手学习路径（总计~3小时）

**Day 1: 基础入门** (1.5小时)
1. 阅读[5分钟快速开始](../docs/user-guide/QUICK_START_V3.5.md)
2. 运行`01-basic/`所有示例
3. 运行`07-v35-features/`所有示例 ⭐

**Day 2: 测试实践** (1小时)
1. 阅读`03-testing/conftest.py`
2. 运行`03-testing/`所有测试
3. 尝试修改测试代码

**Day 3: 进阶使用** (30分钟)
1. 学习`04-patterns/`设计模式
2. 了解`05-extensions/`扩展系统

### 进阶学习路径

**掌握v3.5新特性** (必修)
- 配置化拦截器 - 零代码配置签名/Token/AdminAuth
- Profile环境配置 - 多环境管理
- 运行时配置覆盖 - 测试隔离
- 可观测性集成 - 日志和监控

**深入扩展系统** (选修)
- 自定义扩展开发
- Pluggy hooks机制
- 监控和数据工厂扩展

---

## 🔍 按功能查找示例

### HTTP客户端
- **基础用法**: `01-basic/http_client_usage.py`
- **拦截器配置**: `07-v35-features/01_configurable_interceptors.py` ⭐
- **签名验证**: `07-v35-features/01_configurable_interceptors.py` (示例1)
- **Token认证**: `07-v35-features/01_configurable_interceptors.py` (示例2)

### 配置管理
- **基础配置**: `02-bootstrap/custom_settings.py`
- **环境配置**: `07-v35-features/02_profile_configuration.py` ⭐
- **运行时覆盖**: `07-v35-features/03_runtime_overrides.py` ⭐
- **配置验证**: `02-bootstrap/custom_settings.py`

### 数据库
- **基础操作**: `01-basic/database_operations.py`
- **Repository模式**: `04-patterns/repository_pattern.py`
- **事务管理**: `03-testing/test_database.py`

### 可观测性
- **日志配置**: `07-v35-features/04_observability.py` ⭐
- **HTTP日志**: `07-v35-features/04_observability.py` (示例4)
- **敏感信息脱敏**: `07-v35-features/04_observability.py` (示例5)

### 测试编写
- **API测试**: `03-testing/test_api.py`
- **数据库测试**: `03-testing/test_database.py`
- **Fixtures使用**: `03-testing/test_with_fixtures.py`
- **UI测试**: `06-ui-testing/basic_ui_test.py`

### 扩展开发
- **自定义扩展**: `05-extensions/custom_extension.py`
- **监控扩展**: `05-extensions/monitoring_extension.py`
- **数据工厂**: `05-extensions/data_factory_extension.py`

---

## 📝 贡献示例代码

欢迎贡献新的示例代码！请遵循以下规范：

### 提交清单
- [ ] 代码独立可运行
- [ ] 包含详细中文注释
- [ ] 遵循命名规范
- [ ] 更新本README索引
- [ ] 添加目录README（如果是新目录）

### 示例模板
```python
"""
示例标题

简要说明示例的目的和演示内容。
"""

from df_test_framework import Bootstrap, FrameworkSettings

def example_function():
    """示例函数说明"""
    print("\\n" + "="*60)
    print("示例1: 功能演示")
    print("="*60)

    # 示例代码
    pass

if __name__ == "__main__":
    print("\\n" + "🚀 示例标题")
    print("="*60)

    example_function()

    print("\\n" + "="*60)
    print("✅ 示例执行完成!")
```

---

## 📚 相关文档

### 核心文档
- **[5分钟快速开始](../docs/user-guide/QUICK_START_V3.5.md)** - 新手入门
- **[完整用户手册](../docs/user-guide/USER_MANUAL.md)** - 详细文档
- **[v3.5新特性总结](../docs/V3.5_FINAL_SUMMARY.md)** - v3.5特性总览

### 专题文档
- **[拦截器配置最佳实践](../docs/INTERCEPTOR_CONFIG_BEST_PRACTICES.md)** - 拦截器详解
- **[Phase 3用户指南](../docs/user-guide/PHASE3_FEATURES.md)** - Profile和运行时覆盖
- **[最佳实践](../docs/user-guide/VERIFIED_BEST_PRACTICES.md)** - 验证过的最佳实践

### 迁移文档
- **[v3.4→v3.5迁移指南](../docs/migration/v3.4-to-v3.5.md)** - 升级指南

---

## ❓ 常见问题

### Q1: 示例运行失败？

**检查清单**:
1. ✅ Python版本 >= 3.12
2. ✅ 框架版本 >= v3.5.0
3. ✅ 依赖已安装：`uv pip install df-test-framework`
4. ✅ 工作目录正确

### Q2: v3.5新特性示例在哪？

查看`07-v35-features/`目录，包含4个完整示例：
- 配置化拦截器
- Profile环境配置
- 运行时配置覆盖
- 可观测性集成

### Q3: 如何运行测试示例？

```bash
# 进入测试目录
cd examples/03-testing

# 运行所有测试
pytest -v

# 运行单个测试文件
pytest test_api.py -v
```

### Q4: 示例代码可以直接用于生产吗？

示例代码是教学用途，生产使用需要：
- 添加错误处理
- 配置生产环境参数
- 添加日志和监控
- 遵循安全最佳实践

---

## 🎯 总结

- **25个示例代码**，覆盖框架所有核心功能
- **v3.5新特性** 完整演示（`07-v35-features/`）⭐
- **多种学习路径**，适合不同角色和经验
- **独立可运行**，每个示例都可以直接执行
- **详细注释**，便于理解和学习

**下一步**:
1. 从[5分钟快速开始](../docs/user-guide/QUICK_START_V3.5.md)开始
2. 运行`01-basic/`基础示例
3. 学习`07-v35-features/` v3.5新特性 ⭐
4. 查阅[完整用户手册](../docs/user-guide/USER_MANUAL.md)

---

**示例代码版本**: v3.5.0
**最后更新**: 2025-11-08
**维护者**: df-test-framework团队

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
