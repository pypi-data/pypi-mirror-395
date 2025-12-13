# Multi-Repo 管理指南

> DF QA 测试自动化项目 - 多仓库管理手册

---

## 📁 项目结构

```
D:\Git\DF\qa\  (本地工作目录,非Git仓库)
├── test-framework/        → 独立Git仓库 (核心框架)
│   ├── .git/
│   ├── src/df_test_framework/
│   └── README.md
│
├── gift-card-test/        → 独立Git仓库 (礼品卡测试)
│   ├── .git/
│   ├── tests/
│   └── README.md
│
├── scripts/               → 便利脚本(非Git)
│   ├── sync-all.sh        # 同步所有仓库
│   ├── test-all.sh        # 运行所有测试
│   ├── new-project.sh     # 创建新项目
│   ├── *.bat              # Windows版本
│   └── README.md
│
├── docs/                  → 共享文档(非Git)
│   ├── 架构设计文档.md
│   ├── QUICK_START.md
│   ├── CODE_REVIEW.md
│   └── ...
│
└── README.md              → 索引文档
```

---

## 🔑 核心概念

### Multi-Repo 优势

| 优势 | 说明 |
|------|------|
| 🔀 **职责分离** | 框架和测试项目完全解耦,独立演进 |
| 📦 **版本灵活** | 框架独立发版,测试项目自主选择版本 |
| 🚀 **CI/CD简单** | 每个项目独立流水线,构建快 |
| 👥 **权限清晰** | 可以给不同团队不同仓库权限 |
| 📈 **扩展性好** | 轻松添加新微服务的测试项目 |

### 仓库职责

**test-framework** (核心框架):
- HTTP客户端、数据库、Redis操作
- Pydantic数据模型基类
- 工具类(数据生成器、断言助手)
- pytest fixtures
- **独立版本**: v1.0.0, v1.1.0, v2.0.0
- **发布周期**: 按需发布,相对稳定

**gift-card-test** (测试项目):
- 礼品卡API封装
- 业务数据模型
- 测试用例
- **依赖框架**: 指定版本或使用latest
- **发布周期**: 持续更新,频繁提交

**未来项目** (order-test, user-test等):
- 各自独立的API和测试
- 依赖同一个test-framework
- 独立Git仓库和CI/CD

---

## 🚀 快速开始

### 1. 克隆所有仓库

```bash
# 假设远程仓库已配置
cd D:\Git\DF\qa

# 克隆框架
git clone <framework-repo-url> test-framework

# 克隆测试项目
git clone <gift-card-repo-url> gift-card-test
```

### 2. 安装依赖

```bash
# 框架 (如果需要开发)
cd test-framework
uv sync --all-extras

# 测试项目
cd ../gift-card-test
uv sync
```

### 3. 运行测试

```bash
# 单个项目
cd gift-card-test
ENV=dev uv run pytest -v

# 所有项目 (使用脚本)
cd ..
./scripts/test-all.sh dev
```

---

## 📦 版本管理

### 框架版本策略

**test-framework** 遵循 [语义化版本](https://semver.org/lang/zh-CN/):

```
v主版本.次版本.修订号

v1.0.0 → v1.0.1  # Bug修复
v1.0.1 → v1.1.0  # 新功能,向后兼容
v1.1.0 → v2.0.0  # 破坏性变更
```

**示例**:
- `v1.0.0` - 初始版本
- `v1.1.0` - 添加性能测试支持
- `v1.2.0` - 添加UI测试支持
- `v2.0.0` - 重构HTTP客户端(破坏性变更)

### 测试项目版本策略

**gift-card-test** 可以使用简单版本:

```
v日期 或 v递增号

v2025.10.29  # 日期版本
v1, v2, v3   # 简单递增
```

**或者不打版本** (测试项目通常不需要版本)

---

## 🔄 工作流程

### 场景1: 框架开发新功能

```bash
# 1. 进入框架仓库
cd test-framework

# 2. 创建功能分支
git checkout -b feature/add-retry-mechanism

# 3. 开发功能
# ... 编写代码 ...

# 4. 本地测试
uv run pytest tests/

# 5. 提交代码
git add .
git commit -m "feat: 添加HTTP重试机制"
git push origin feature/add-retry-mechanism

# 6. 创建PR,合并到main

# 7. 发布新版本
git checkout main
git pull
git tag v1.1.0 -m "Release v1.1.0: 添加HTTP重试机制"
git push origin v1.1.0
```

### 场景2: 测试项目使用新框架版本

```bash
# 1. 进入测试项目
cd gift-card-test

# 2. 更新依赖 (方式一: 本地开发,自动使用最新)
# 本地路径依赖会自动使用最新代码,无需操作

# 3. 更新依赖 (方式二: 固定版本)
# 编辑 pyproject.toml
# dependencies = [
#     "df-test-framework @ git+https://github.com/yourorg/df-test-framework.git@v1.1.0"
# ]

# 4. 同步依赖
uv sync

# 5. 运行测试验证
ENV=dev uv run pytest -v

# 6. 提交更新
git add pyproject.toml
git commit -m "chore: 升级test-framework到v1.1.0"
git push
```

### 场景3: 编写新测试用例

```bash
# 1. 进入测试项目
cd gift-card-test

# 2. 创建功能分支
git checkout -b feature/add-activate-test

# 3. 编写测试
# tests/api/test_gift_card/test_activate.py

# 4. 本地运行
ENV=dev uv run pytest tests/api/test_gift_card/test_activate.py -v

# 5. 提交代码
git add tests/
git commit -m "test: 添加礼品卡激活测试用例"
git push origin feature/add-activate-test

# 6. 创建PR,合并到main
```

### 场景4: 创建新测试项目

```bash
# 1. 使用脚本快速创建
cd D:\Git\DF\qa
./scripts/new-project.sh order-test "订单系统测试"

# 2. 配置新项目
cd order-test
cp .env.example .env.dev
# 编辑 .env.dev

# 3. 编写API封装和测试
# api/order_api.py
# tests/api/test_order/...

# 4. 运行测试
ENV=dev uv run pytest -v

# 5. 推送到远程
git remote add origin <remote-url>
git push -u origin main
```

---

## 🛠️ 便利脚本

### sync-all.sh / sync-all.bat

**功能**: 同步所有Git仓库

```bash
# Linux/Mac
./scripts/sync-all.sh

# Windows
scripts\sync-all.bat
```

**作用**:
- 自动检测所有Git仓库
- 执行 `git pull`
- 报告同步状态

### test-all.sh / test-all.bat

**功能**: 运行所有测试项目

```bash
# Linux/Mac
./scripts/test-all.sh dev

# Windows
scripts\test-all.bat dev
```

**作用**:
- 遍历所有测试项目
- 运行冒烟测试
- 汇总测试结果

### new-project.sh

**功能**: 快速创建新测试项目

```bash
./scripts/new-project.sh order-test "订单系统测试"
```

**作用**:
- 复制gift-card-test作为模板
- 自动更新项目配置
- 初始化Git仓库
- 清空测试代码

---

## 🌐 CI/CD 集成

### GitHub Actions 配置

**test-framework/.github/workflows/ci.yml**:
```yaml
name: Framework CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Install dependencies
        run: uv sync --all-extras

      - name: Run tests
        run: uv run pytest tests/ -v

      - name: Code check
        run: |
          uv run ruff check .
          uv run mypy src/

  release:
    needs: test
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build
        run: uv build

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*
```

**gift-card-test/.github/workflows/test.yml**:
```yaml
name: Gift Card Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'  # 每天凌晨2点

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        env: [dev, test]

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Update framework dependency
        run: |
          # 使用Git URL替换本地路径
          sed -i 's|file:///../test-framework|git+https://github.com/yourorg/df-test-framework.git@v1.0.0|' pyproject.toml

      - name: Install dependencies
        run: uv sync

      - name: Run tests
        env:
          ENV: ${{ matrix.env }}
        run: uv run pytest -v -m smoke

      - name: Generate Allure Report
        if: always()
        uses: simple-elf/allure-report-action@master
        with:
          allure_results: reports/allure-results
```

### 环境变量切换

**本地开发**: 使用相对路径
```toml
dependencies = [
    "df-test-framework @ file:///../test-framework",
]
```

**CI/CD环境**: 使用Git URL
```toml
dependencies = [
    "df-test-framework @ git+https://github.com/yourorg/df-test-framework.git@v1.0.0",
]
```

**自动切换脚本**:
```bash
# CI环境自动替换
if [ "$CI" = "true" ]; then
    sed -i 's|file:///../test-framework|git+https://github.com/yourorg/df-test-framework.git@v1.0.0|' pyproject.toml
fi
```

---

## 📝 日常操作

### 查看所有仓库状态

```bash
cd D:\Git\DF\qa

for dir in test-framework gift-card-test; do
    echo "=== $dir ==="
    cd $dir
    git status -s
    cd ..
    echo ""
done
```

### 更新所有仓库

```bash
# 使用脚本
./scripts/sync-all.sh

# 或手动
cd test-framework && git pull && cd ..
cd gift-card-test && git pull && cd ..
```

### 查看框架版本

```bash
cd test-framework
git tag -l
git describe --tags
```

### 切换框架版本

```bash
# 测试项目中
cd gift-card-test

# 编辑 pyproject.toml, 修改版本号
# "df-test-framework @ git+...@v1.2.0"

uv sync
```

---

## 🔐 权限管理

### GitHub 仓库权限

**test-framework** (核心框架):
- **Admin**: 框架核心开发者 (2-3人)
- **Write**: 框架贡献者
- **Read**: 所有测试开发者

**gift-card-test** (测试项目):
- **Admin**: 测试负责人
- **Write**: 测试开发者
- **Read**: 相关开发者

### 分支保护

**test-framework**:
- main分支保护
- 需要PR review
- 需要CI通过
- 不允许force push

**gift-card-test**:
- main分支保护
- 需要CI通过
- 允许直接提交(小改动)

---

## 🆘 常见问题

### Q1: 本地框架修改后,测试项目怎么立即生效?

**A**: 使用本地路径依赖时会自动生效:
```toml
dependencies = [
    "df-test-framework @ file:///../test-framework",
]
```

修改框架后,测试项目无需重新安装,直接运行即可。

### Q2: 如何固定框架版本?

**A**: 修改 pyproject.toml:
```toml
dependencies = [
    "df-test-framework @ git+https://github.com/yourorg/df-test-framework.git@v1.1.0",
]
```

然后 `uv sync`

### Q3: 多个测试项目如何共享配置?

**A**:
1. 在父目录创建 `shared/` 文件夹
2. 各项目软链接: `ln -s ../shared/common.py .`
3. 或复制到各项目

### Q4: 如何快速创建新项目?

**A**: 使用脚本:
```bash
./scripts/new-project.sh order-test "订单系统测试"
```

### Q5: CI/CD 如何处理本地路径依赖?

**A**: CI中自动替换为Git URL:
```bash
sed -i 's|file:///../test-framework|git+https://github.com/yourorg/df-test-framework.git@v1.0.0|' pyproject.toml
```

---

## 📊 项目清单

### 当前仓库

| 仓库 | 类型 | Git | 远程 | 状态 |
|------|------|-----|------|------|
| test-framework | 框架 | ✅ | 待配置 | ✅ 已初始化 |
| gift-card-test | 测试 | ✅ | 待配置 | ✅ 已初始化 |

### 计划仓库

| 仓库 | 类型 | 描述 | 优先级 |
|------|------|------|--------|
| order-test | 测试 | 订单系统测试 | 中 |
| user-test | 测试 | 用户系统测试 | 中 |
| payment-test | 测试 | 支付系统测试 | 低 |

---

## 🎯 最佳实践

### 1. 版本管理

- ✅ 框架使用语义化版本
- ✅ 破坏性变更升级主版本
- ✅ 新功能升级次版本
- ✅ Bug修复升级修订号

### 2. 分支策略

- ✅ main分支保护,不直接提交
- ✅ 功能开发使用feature分支
- ✅ PR合并前需要review
- ✅ CI必须通过才能合并

### 3. 依赖管理

- ✅ 本地开发用相对路径
- ✅ CI/CD用Git URL
- ✅ 生产环境用PyPI版本
- ✅ 定期更新框架版本

### 4. 文档维护

- ✅ 每个仓库独立README
- ✅ 父目录保留索引文档
- ✅ 重大变更更新文档
- ✅ 示例代码保持最新

---

## 📚 相关文档

- [架构设计](../archive/v1/architecture.md) - v1.x架构设计文档
- [快速开始指南](../getting-started/quickstart.md) - 5分钟上手指南
- [最佳实践](../archive/v1/best-practices.md) - v1.x最佳实践指南
- [框架使用文档](../../README.md) - 主README文档
- [测试项目文档](../../../gift-card-test/README.md) - Gift Card测试项目

---

## 🔄 更新日志

### 2025-10-29

- ✅ 初始化 test-framework Git仓库 (v1.0.0)
- ✅ 初始化 gift-card-test Git仓库
- ✅ 创建便利脚本 (sync-all, test-all, new-project)
- ✅ 编写 Multi-Repo 管理文档
- ✅ 完成架构优化方案设计
- ✅ 补充安全加固和性能优化指南

---

## 💡 最佳实践更新

基于最新的架构优化方案,建议在所有测试项目中实施以下最佳实践:

### 安全性

1. **使用参数化查询** - 所有数据库操作必须使用参数化查询,防止SQL注入
2. **敏感信息管理** - .env文件加入.gitignore,生产环境使用密钥管理服务
3. **日志脱敏** - 自动过滤日志中的密码、token等敏感信息

### 资源管理

1. **HTTP客户端** - 使用上下文管理器或fixture自动清理连接
2. **数据库连接** - Session级别的连接池,测试级别的事务隔离
3. **配置管理** - 使用工厂模式而非全局单例

### 测试质量

1. **类型安全** - 使用Literal或Enum替代字符串常量
2. **超时控制** - 为所有测试设置合理的超时时间
3. **性能监控** - 关键操作添加性能跟踪
4. **代码覆盖率** - 保持80%以上的测试覆盖率

> 📖 更多最佳实践请参考: [最佳实践指南](../archive/v1/best-practices.md) 和 [架构设计文档](../archive/v1/architecture.md)

---

**维护者**: DF QA Team
**文档版本**: v1.1
**最后更新**: 2025-10-29
