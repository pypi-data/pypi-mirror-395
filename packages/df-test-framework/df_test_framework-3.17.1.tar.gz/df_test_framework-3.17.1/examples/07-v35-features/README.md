# v3.5 新特性示例

> **框架版本**: df-test-framework v3.5.0
> **更新日期**: 2025-11-08

---

## 📚 示例列表

v3.5.0是完全重构的版本，引入了三大核心特性：

| 示例文件 | 特性 | 说明 |
|---------|------|------|
| **01_configurable_interceptors.py** | 配置化拦截器 | 零代码配置签名、Token、AdminAuth拦截器 |
| **02_profile_configuration.py** | Profile环境配置 | 多环境配置文件自动加载 |
| **03_runtime_overrides.py** | 运行时配置覆盖 | 测试隔离和临时配置修改 |
| **04_observability.py** | 可观测性集成 | 结构化日志和Allure报告集成 |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 使用uv（推荐）
pip install uv
uv pip install df-test-framework

# 或使用pip
pip install df-test-framework
```

### 2. 运行示例

```bash
# 进入示例目录
cd examples/07-v35-features

# 运行单个示例
python 01_configurable_interceptors.py

# 运行所有示例
python 01_configurable_interceptors.py
python 02_profile_configuration.py
python 03_runtime_overrides.py
python 04_observability.py
```

---

## 📖 示例详解

### 01_configurable_interceptors.py - 配置化拦截器

**核心价值**: 零代码配置HTTP拦截器，无需手写拦截逻辑

**演示内容**:
- ✅ 签名拦截器（SignatureInterceptor）- MD5/SHA256/HMAC-SHA256算法
- ✅ Bearer Token拦截器 - 自动登录和Token管理
- ✅ AdminAuth拦截器 - 管理员认证
- ✅ 路径模式匹配 - 通配符和正则表达式
- ✅ 拦截器优先级控制

**关键代码**:
```python
def _create_http_config() -> HTTPConfig:
    return HTTPConfig(
        base_url="https://api.example.com",
        interceptors=[
            SignatureInterceptorConfig(
                type="signature",
                enabled=True,
                priority=10,
                algorithm="md5",
                secret="my_secret",
                header_name="X-Sign",
                include_paths=["/api/**"],
                exclude_paths=["/health"],
            ),
            BearerTokenInterceptorConfig(
                type="bearer_token",
                enabled=True,
                priority=20,
                token_source="login",
                login_url="/admin/auth/login",
                login_credentials={
                    "username": "admin",
                    "password": "admin123"
                },
                token_field_path="data.token",
                include_paths=["/admin/**"],
            ),
        ]
    )
```

---

### 02_profile_configuration.py - Profile环境配置

**核心价值**: 多环境配置管理，轻松切换开发/测试/生产环境

**演示内容**:
- ✅ 创建多个环境配置文件（.env.dev, .env.test, .env.prod）
- ✅ 通过ENV环境变量切换配置
- ✅ 配置优先级：profile参数 > ENV变量 > 默认值
- ✅ .env.local本地配置覆盖

**关键代码**:
```python
# 通过环境变量切换环境
# ENV=dev python test.py    # 加载.env.dev
# ENV=test python test.py   # 加载.env.test
# ENV=prod python test.py   # 加载.env.prod

# 或在代码中指定
runtime = (
    Bootstrap()
    .with_settings(MySettings, profile="dev")  # 显式指定环境
    .build()
    .run()
)
```

**配置文件结构**:
```
project/
├── .env           # 基础配置
├── .env.dev       # 开发环境
├── .env.test      # 测试环境
├── .env.prod      # 生产环境
└── .env.local     # 本地配置（不提交git）
```

---

### 03_runtime_overrides.py - 运行时配置覆盖

**核心价值**: 测试隔离和临时配置修改，不影响全局配置

**演示内容**:
- ✅ 使用with_overrides()创建临时配置上下文
- ✅ 修改HTTP超时、重试次数等参数
- ✅ 原始配置保持不变（不可变设计）
- ✅ 测试间完全隔离
- ✅ 嵌套覆盖支持

**关键代码**:
```python
# 原始配置
runtime_ctx = Bootstrap().with_settings(MySettings).build().run()
assert runtime_ctx.settings.http.timeout == 30  # 默认30秒

# 创建临时配置（超时5秒）
test_ctx = runtime_ctx.with_overrides({
    "http.timeout": 5,
    "http.max_retries": 1,
})
assert test_ctx.settings.http.timeout == 5  # 临时修改为5秒

# 原始配置不受影响
assert runtime_ctx.settings.http.timeout == 30  # 仍然是30秒
```

---

### 04_observability.py - 可观测性集成

**核心价值**: 完整的可观测性支持，便于调试和问题排查

**演示内容**:
- ✅ ObservabilityLogger统一日志格式
- ✅ HTTP请求/响应自动记录
- ✅ 数据库操作自动记录
- ✅ Allure报告集成
- ✅ 配置开关控制
- ✅ 敏感信息自动脱敏

**关键代码**:
```python
class MySettings(FrameworkSettings):
    logging: LoggingConfig = Field(
        default_factory=lambda: LoggingConfig(
            level="INFO",
            enable_observability=True,     # 启用可观测性
            enable_http_logging=True,      # HTTP日志
            enable_db_logging=True,        # 数据库日志
            enable_allure_logging=True,    # Allure集成
        )
    )
```

**日志输出示例**:
```json
{
  "timestamp": "2025-11-08T10:30:45.123Z",
  "level": "INFO",
  "logger": "ObservabilityLogger",
  "event": "http_request",
  "method": "POST",
  "url": "/api/users",
  "duration_ms": 192.3,
  "status_code": 200
}
```

---

## 🔗 相关文档

- **[v3.5快速开始](../../docs/user-guide/QUICK_START_V3.5.md)** - 5分钟快速上手
- **[v3.4→v3.5迁移指南](../../docs/migration/v3.4-to-v3.5.md)** - 从v3.4升级
- **[拦截器配置最佳实践](../../docs/INTERCEPTOR_CONFIG_BEST_PRACTICES.md)** - 拦截器详细配置
- **[Phase 3用户指南](../../docs/user-guide/PHASE3_FEATURES.md)** - Profile和运行时覆盖详解
- **[v3.5最终总结](../../docs/V3.5_FINAL_SUMMARY.md)** - v3.5所有特性总览

---

## ❓ 常见问题

### Q1: 拦截器配置后不生效？

**原因**: Pydantic字段继承覆盖问题

**解决方案**: 使用辅助函数 + model_validator模式

```python
# ✅ 正确方式
def _create_http_config() -> HTTPConfig:
    return HTTPConfig(
        base_url=os.getenv("APP_HTTP__BASE_URL"),
        interceptors=[...]
    )

class MySettings(FrameworkSettings):
    @model_validator(mode='after')
    def _setup_interceptors(self) -> Self:
        self.http = _create_http_config()
        return self
```

### Q2: 如何调试拦截器？

```bash
# 启用DEBUG日志
APP_LOGGING__LEVEL=DEBUG python your_test.py

# 查看拦截器生效路径
APP_DEBUG=true python your_test.py
```

### Q3: Profile配置未加载？

**检查清单**:
1. ✅ 确认.env.{profile}文件存在
2. ✅ 确认ENV环境变量已设置：`export ENV=dev`
3. ✅ 确认settings.py中调用了`load_dotenv()`
4. ✅ 确认环境变量名称匹配（APP_HTTP__BASE_URL格式）

### Q4: with_overrides覆盖不生效？

**注意事项**:
- ✅ 使用返回的新context对象，而不是原始runtime_ctx
- ✅ 覆盖路径使用点号分隔：`"http.timeout"`（不是`"http__timeout"`）
- ✅ 值类型要匹配（int不能传str）

---

## 💡 最佳实践

1. **拦截器配置**
   - 使用辅助函数封装拦截器配置
   - 优先级：签名(10) < 认证(20) < 自定义(30+)
   - 路径匹配：先include后exclude

2. **环境配置**
   - .env.local用于本地覆盖（不提交git）
   - 敏感信息从环境变量读取，不硬编码
   - 使用dotenv-linter验证配置文件

3. **运行时覆盖**
   - 仅在测试中使用，避免在业务代码中使用
   - 覆盖值要合理（timeout不要设置为0）
   - 测试完成后不需要手动恢复（自动隔离）

4. **可观测性**
   - 生产环境：enable_observability=False（性能优先）
   - 测试环境：enable_observability=True（调试优先）
   - 使用Allure报告查看详细日志

---

## 🎯 学习路径建议

**新手**:
1. 先运行01_configurable_interceptors.py了解拦截器
2. 再运行02_profile_configuration.py学习环境配置
3. 最后运行03_runtime_overrides.py掌握测试隔离

**进阶**:
1. 阅读[拦截器配置最佳实践](../../docs/INTERCEPTOR_CONFIG_BEST_PRACTICES.md)
2. 阅读[Phase 3用户指南](../../docs/user-guide/PHASE3_FEATURES.md)
3. 查看[gift-card-test实际项目](../../../gift-card-test/)

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
