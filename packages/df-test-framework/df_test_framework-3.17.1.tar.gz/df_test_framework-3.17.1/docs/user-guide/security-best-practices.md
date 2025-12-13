# 安全最佳实践指南

> **版本**: v3.7.0
> **最后更新**: 2025-11-25
> **目标读者**: 测试开发工程师、QA工程师
>
> 本文档提供 df-test-framework 安全使用指南，帮助您编写安全的测试代码。

---

## 📋 目录

1. [敏感信息管理](#1-敏感信息管理)
2. [SQL注入防护](#2-sql注入防护)
3. [API签名验证](#3-api签名验证)
4. [HTTPS验证](#4-https验证)
5. [认证授权](#5-认证授权)
6. [日志安全](#6-日志安全)
7. [依赖安全](#7-依赖安全)
8. [数据加密](#8-数据加密)
9. [安全检查清单](#9-安全检查清单)
10. [安全事件响应](#10-安全事件响应)
11. [参考资源](#11-参考资源)

---

## 1. 敏感信息管理

### 1.1 禁止硬编码密码 🚫

**❌ 错误示例**:
```python
# 危险！密码硬编码在代码中
from my_project.config import MySettings

settings = MySettings(
    db_password="MyP@ssw0rd123",  # ❌ 硬编码密码
    api_secret="secret_key_123",   # ❌ 硬编码密钥
    redis_password="redis123"      # ❌ 硬编码密码
)
```

**✅ 正确示例**:
```python
# 使用环境变量
from pydantic import SecretStr, Field
from df_test_framework import FrameworkSettings

class MySettings(FrameworkSettings):
    """项目配置 - 所有敏感信息从环境变量读取"""

    db_password: SecretStr = Field(..., description="数据库密码")
    api_secret: SecretStr = Field(..., description="API密钥")
    redis_password: SecretStr = Field(..., description="Redis密码")

# .env文件
# DB_PASSWORD=MyP@ssw0rd123
# API_SECRET=secret_key_123
# REDIS_PASSWORD=redis123

# 配置自动从环境变量读取
settings = MySettings()
```

**为什么重要**:
- ✅ 密码不会被提交到Git仓库
- ✅ 不同环境可使用不同密码
- ✅ SecretStr自动脱敏日志输出

---

### 1.2 .env文件管理

**推荐的项目结构**:

```
project/
├── .env                # ❌ 不提交 (本地配置)
├── .env.example        # ✅ 提交 (配置模板)
├── .env.dev            # ✅ 提交 (开发环境默认值)
├── .env.test           # ✅ 提交 (测试环境默认值)
├── .env.prod           # ✅ 提交 (生产环境默认值，值为占位符)
├── .env.local          # ❌ 不提交 (本地覆盖)
└── .gitignore          # ✅ 排除 .env 和 .env.local
```

**.env.example** (模板文件):
```bash
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USERNAME=root
DB_PASSWORD=<请填写密码>

# API配置
API_BASE_URL=https://api.example.com
API_SECRET=<请填写密钥>

# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=<请填写密码>
```

**.env.dev** (开发环境):
```bash
DB_HOST=localhost
DB_PORT=3306
DB_USERNAME=dev_user
DB_PASSWORD=dev_password_123

API_BASE_URL=https://dev-api.example.com
API_SECRET=dev_secret_key

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=dev_redis_123
```

**.gitignore配置**:
```gitignore
# 排除本地环境配置
.env
.env.local
.env.*.local

# 排除敏感日志
*.log
logs/
reports/logs/

# 排除临时文件
*.tmp
.pytest_cache/
```

**使用方式**:
```bash
# 1. 首次克隆项目后
cp .env.example .env
# 编辑 .env 填入真实密码

# 2. 覆盖环境配置
cp .env.dev .env
# 然后创建 .env.local 覆盖个别配置

# 3. 加载特定环境配置
export ENV_FILE=.env.test
pytest tests/
```

---

### 1.3 密钥管理服务

**生产环境建议使用密钥管理服务**:

#### AWS Secrets Manager
```python
import boto3
from botocore.exceptions import ClientError

def get_secret(secret_name: str, region_name: str = "us-east-1") -> dict:
    """从AWS Secrets Manager获取密钥"""
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except ClientError as e:
        raise Exception(f"获取密钥失败: {e}")

# 使用示例
secrets = get_secret("prod/db-credentials")
settings = MySettings(
    db_password=secrets["password"],
    db_username=secrets["username"]
)
```

#### Azure Key Vault
```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def get_secret_from_azure(vault_url: str, secret_name: str) -> str:
    """从Azure Key Vault获取密钥"""
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)

    secret = client.get_secret(secret_name)
    return secret.value

# 使用示例
db_password = get_secret_from_azure(
    vault_url="https://my-vault.vault.azure.net",
    secret_name="db-password"
)
```

**推荐的密钥管理服务**:
- **AWS Secrets Manager** - 适合AWS生态
- **Azure Key Vault** - 适合Azure生态
- **HashiCorp Vault** - 跨平台方案
- **阿里云密钥管理服务(KMS)** - 适合阿里云

---

## 2. SQL注入防护

### 2.1 使用参数化查询 ✅

**❌ 错误示例** (SQL注入风险):
```python
from df_test_framework.databases import Database

# 危险！字符串拼接SQL
def get_user_by_id_unsafe(user_id: str):
    db = Database(connection_string="...")

    # ❌ 攻击者可以输入: "1 OR 1=1" 返回所有用户
    sql = f"SELECT * FROM users WHERE id = {user_id}"
    result = db.query_all(sql)

    return result

# 攻击示例
user_id = "1 OR 1=1"  # 恶意输入
users = get_user_by_id_unsafe(user_id)
# 结果: 返回所有用户数据！
```

**✅ 正确示例**:
```python
from df_test_framework.databases import Database

def get_user_by_id_safe(user_id: str):
    db = Database(connection_string="...")

    # ✅ 参数化查询，自动转义
    sql = "SELECT * FROM users WHERE id = :user_id"
    result = db.query_all(sql, {"user_id": user_id})

    return result

# 安全示例
user_id = "1 OR 1=1"  # 恶意输入被转义
users = get_user_by_id_safe(user_id)
# 结果: 查询 WHERE id = '1 OR 1=1'，不会返回所有用户
```

**为什么参数化查询安全**:
- ✅ 数据库驱动自动转义特殊字符
- ✅ 输入被当作数据而非SQL代码
- ✅ 防止所有类型的SQL注入攻击

---

### 2.2 使用Repository模式

**推荐方式** (最安全):
```python
from df_test_framework.databases.repositories import BaseRepository
from sqlalchemy.orm import Session

class UserRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session, table_name="users")

    def find_by_id(self, user_id: str):
        """安全的查询方法"""
        # BaseRepository内部使用参数化查询
        return super().find_by_id(user_id)

    def find_by_username(self, username: str):
        """安全的条件查询"""
        return self.find_one({"username": username})

# 使用示例
with uow:
    user_repo = uow.repository(UserRepository)

    # ✅ 所有查询都是安全的
    user = user_repo.find_by_id("1 OR 1=1")  # 安全
    user = user_repo.find_by_username("admin' OR '1'='1")  # 安全
```

---

### 2.3 输入验证

**额外防护层**:
```python
from pydantic import BaseModel, Field, validator

class UserQueryRequest(BaseModel):
    """用户查询请求模型"""

    user_id: str = Field(..., max_length=36, description="用户ID")

    @validator('user_id')
    def validate_user_id(cls, v):
        """验证user_id格式"""
        # 只允许字母数字和连字符
        if not v.replace('-', '').isalnum():
            raise ValueError('user_id只能包含字母、数字和连字符')
        return v

# 使用示例
try:
    request = UserQueryRequest(user_id="1 OR 1=1")
except ValueError as e:
    print(f"输入验证失败: {e}")
    # 输出: 输入验证失败: user_id只能包含字母、数字和连字符
```

---

## 3. API签名验证

### 3.1 签名中间件配置

**HMAC-SHA256签名** (推荐):
```python
from df_test_framework import FrameworkSettings
from df_test_framework.clients.http.config import HTTPConfig
from df_test_framework.clients.http.middlewares.config import SignatureMiddlewareConfig

class MySettings(FrameworkSettings):
    http: HTTPConfig = HTTPConfig(
        base_url="https://api.example.com",
        middlewares=[
            SignatureMiddlewareConfig(
                type="signature",
                algorithm="hmac_sha256",  # ✅ 推荐：HMAC-SHA256
                secret="${API_SECRET_KEY}",  # 从环境变量读取
                header="X-Signature",
                timestamp_header="X-Timestamp",
                include_paths=["/api/**"],  # 包含路径
                exclude_paths=["/api/health"]  # 排除健康检查
            )
        ]
    )

# .env文件
# API_SECRET_KEY=your-256-bit-secret-key-here
```

**签名生成逻辑**:
```python
import hmac
import hashlib
import time

def generate_signature(secret: str, timestamp: str, body: str) -> str:
    """生成HMAC-SHA256签名"""
    message = f"{timestamp}{body}"
    signature = hmac.new(
        secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return signature

# 使用示例
secret = "your-secret-key"
timestamp = str(int(time.time()))
body = '{"user_id": 123}'

signature = generate_signature(secret, timestamp, body)
print(f"Signature: {signature}")
```

---

### 3.2 签名策略选择

| 算法 | 安全性 | 性能 | 密钥长度 | 推荐场景 |
|------|--------|------|---------|---------|
| **MD5** | ⚠️ 低 | 极高 | 128位 | 非安全场景 (已淘汰) |
| **SHA256** | ✅ 中 | 高 | 256位 | 一般场景 |
| **HMAC-SHA256** | ⭐⭐⭐⭐⭐ 高 | 中 | 256位 | **生产环境推荐** |
| **RSA签名** | ⭐⭐⭐⭐⭐ 极高 | 低 | 2048位+ | 高安全场景 |

**推荐顺序**:
1. ⭐ **HMAC-SHA256** - 平衡安全性和性能
2. RSA签名 - 需要非对称加密时
3. SHA256 - 简单场景
4. ❌ MD5 - 不推荐

---

### 3.3 时间戳防重放攻击

```python
from df_test_framework.clients.http.middlewares.config import SignatureMiddlewareConfig

SignatureMiddlewareConfig(
    type="signature",
    algorithm="hmac_sha256",
    secret="${API_SECRET_KEY}",
    header="X-Signature",
    timestamp_header="X-Timestamp",
    timestamp_tolerance=300,  # ✅ 5分钟内有效，防止重放攻击
)
```

---

## 4. HTTPS验证

### 4.1 强制HTTPS

**✅ 正确配置**:
```python
from df_test_framework.clients.http.config import HTTPConfig

# 生产环境配置
http = HTTPConfig(
    base_url="https://api.example.com",  # ✅ 使用HTTPS
    verify_ssl=True,  # ✅ 验证SSL证书
    timeout=30
)
```

**❌ 错误配置**:
```python
# 危险！HTTP明文传输
http = HTTPConfig(
    base_url="http://api.example.com",  # ❌ HTTP不加密
    verify_ssl=False,  # ❌ 不验证证书
)
```

---

### 4.2 自签名证书处理

**开发环境临时方案**:
```python
from df_test_framework import FrameworkSettings

class DevSettings(FrameworkSettings):
    """开发环境配置"""

    env: str = "dev"

    @property
    def http_config(self):
        if self.env == "dev":
            # ⚠️ 仅开发环境可以禁用SSL验证
            return HTTPConfig(
                base_url="https://dev-api.example.com",
                verify_ssl=False,  # 开发环境允许
            )
        else:
            # ✅ 生产环境必须验证
            return HTTPConfig(
                base_url="https://api.example.com",
                verify_ssl=True,
            )
```

**推荐方案** (使用自定义CA证书):
```python
http = HTTPConfig(
    base_url="https://dev-api.example.com",
    verify_ssl="/path/to/custom-ca.crt",  # ✅ 指定自定义CA证书
)
```

---

## 5. 认证授权

### 5.1 Bearer Token自动刷新

**自动登录配置**:
```python
from df_test_framework.clients.http.middlewares.config import BearerTokenMiddlewareConfig

BearerTokenMiddlewareConfig(
    type="bearer_token",
    token_source="login",  # 自动登录获取token
    login_url="/auth/login",
    login_credentials={
        "username": "${ADMIN_USERNAME}",  # ✅ 从环境变量读取
        "password": "${ADMIN_PASSWORD}"   # ✅ 从环境变量读取
    },
    token_field_path="data.access_token",  # Token在响应中的路径
    refresh_on_401=True,  # ✅ Token过期自动刷新
    cache_token=True  # ✅ 缓存token避免重复登录
)
```

---

### 5.2 多环境认证配置

**.env.dev** (开发环境):
```bash
ADMIN_USERNAME=dev_admin
ADMIN_PASSWORD=dev_password_123
```

**.env.test** (测试环境):
```bash
ADMIN_USERNAME=test_admin
ADMIN_PASSWORD=test_password_456
```

**.env.prod** (生产环境):
```bash
ADMIN_USERNAME=prod_admin
ADMIN_PASSWORD=***hidden***  # ⚠️ 使用密钥管理服务
```

---

### 5.3 Token过期处理

```python
from df_test_framework.clients.http import HttpClient

# 框架自动处理token过期
client = HttpClient(config=http_config)

# 第一次请求：自动登录获取token
response1 = client.get("/api/users")

# ... 30分钟后 token过期

# 第二次请求：检测到401，自动刷新token并重试
response2 = client.get("/api/orders")  # ✅ 自动刷新成功
```

---

## 6. 日志安全

### 6.1 敏感信息自动脱敏

框架**自动脱敏**以下字段:

```python
# 自动脱敏字段列表
SENSITIVE_FIELDS = [
    "password", "passwd", "pwd",
    "token", "access_token", "refresh_token",
    "secret", "secret_key", "api_key",
    "authorization", "auth",
    "card_no", "card_number",
    "id_card", "id_number",
    "phone", "mobile",
    "email"
]
```

**示例**:
```python
from loguru import logger

# 敏感数据
user = {
    "username": "admin",
    "password": "MyP@ssw0rd123",
    "email": "admin@example.com"
}

logger.info(f"用户登录: {user}")
# 输出: 用户登录: {"username": "admin", "password": "****", "email": "ad***@example.com"}
```

---

### 6.2 禁止记录完整请求体

**❌ 错误示例**:
```python
# 危险！完整记录请求体可能泄露敏感信息
logger.info(f"请求体: {request.body}")
# 输出: 请求体: {"username": "admin", "password": "secret123"}
```

**✅ 正确示例**:
```python
# 只记录非敏感字段
logger.info(f"请求: user_id={request.user_id}, action={request.action}")
# 输出: 请求: user_id=123, action=login
```

---

### 6.3 生产环境日志级别

```python
from df_test_framework import FrameworkSettings

class ProdSettings(FrameworkSettings):
    """生产环境配置"""

    log_level: str = "INFO"  # ✅ 生产环境使用INFO
    # log_level: str = "DEBUG"  # ❌ 不要在生产使用DEBUG
```

**日志级别建议**:
- **开发环境**: DEBUG
- **测试环境**: INFO
- **生产环境**: WARNING 或 INFO

---

## 7. 依赖安全

### 7.1 定期更新依赖

```bash
# 1. 检查过时的依赖
pip list --outdated

# 2. 更新特定依赖
pip install --upgrade package-name

# 3. 更新所有依赖 (谨慎使用)
pip install --upgrade -r requirements.txt
```

---

### 7.2 漏洞扫描

**使用 safety 扫描**:
```bash
# 安装safety
pip install safety

# 扫描依赖漏洞
safety check

# 生成JSON报告
safety check --json > security-report.json
```

**CI/CD集成示例**:
```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: 安装依赖
        run: |
          pip install safety
          pip install -r requirements.txt

      - name: 安全扫描
        run: safety check --json
```

---

### 7.3 固定依赖版本

**requirements.txt** (固定版本):
```txt
# ✅ 推荐：固定版本号
pytest==8.0.0
httpx==0.27.0
pydantic==2.5.0

# ❌ 不推荐：不固定版本
# pytest>=8.0.0  # 可能引入breaking changes
# httpx  # 可能安装不兼容版本
```

**使用 pip freeze**:
```bash
# 生成精确版本锁定文件
pip freeze > requirements-lock.txt
```

---

## 8. 数据加密

### 8.1 加密敏感字段

```python
from cryptography.fernet import Fernet
from pydantic import BaseModel

class CryptoHelper:
    """加密工具类"""

    def __init__(self, key: bytes):
        self.cipher = Fernet(key)

    def encrypt(self, plaintext: str) -> str:
        """加密"""
        return self.cipher.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext: str) -> str:
        """解密"""
        return self.cipher.decrypt(ciphertext.encode()).decode()

# 使用示例
key = Fernet.generate_key()
crypto = CryptoHelper(key)

# 加密敏感数据
card_no = "6222021234567890"
encrypted_card_no = crypto.encrypt(card_no)

# 存储到数据库
db.execute(
    "INSERT INTO orders (card_no) VALUES (:card_no)",
    {"card_no": encrypted_card_no}
)

# 从数据库读取并解密
result = db.query_one("SELECT card_no FROM orders WHERE id = 1")
decrypted_card_no = crypto.decrypt(result["card_no"])
```

---

### 8.2 密钥管理

**生成加密密钥**:
```python
from cryptography.fernet import Fernet

# 生成密钥
key = Fernet.generate_key()
print(key.decode())
# 输出: b'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='
```

**存储密钥** (.env):
```bash
# 加密密钥（Fernet key）
ENCRYPTION_KEY=ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg=
```

**使用密钥**:
```python
from pydantic import Field
from df_test_framework import FrameworkSettings

class MySettings(FrameworkSettings):
    encryption_key: str = Field(..., description="数据加密密钥")

settings = MySettings()
crypto = CryptoHelper(settings.encryption_key.encode())
```

---

## 9. 安全检查清单

测试代码提交前，请检查以下项目:

### 代码安全 ✅

- [ ] **无硬编码密码/Token**
  - 检查代码中是否有密码、API密钥等敏感信息
  - 所有敏感信息使用环境变量或密钥管理服务

- [ ] **.env.local已添加到.gitignore**
  - 确保本地配置文件不会被提交
  - 验证.gitignore包含`.env`和`.env.local`

- [ ] **使用参数化查询**
  - 所有数据库查询使用参数化方式
  - 不使用字符串拼接构建SQL

### 配置安全 ✅

- [ ] **生产环境启用HTTPS**
  - base_url使用`https://`
  - 不使用HTTP明文传输

- [ ] **启用SSL证书验证**
  - `verify_ssl=True`
  - 不在生产环境禁用SSL验证

- [ ] **敏感日志已脱敏**
  - 不记录完整请求体
  - 敏感字段自动脱敏

### 依赖安全 ✅

- [ ] **依赖无已知漏洞**
  - 运行`safety check`通过
  - 及时更新有漏洞的依赖

- [ ] **依赖版本已固定**
  - requirements.txt使用精确版本号
  - 避免使用`>=`范围版本

### 数据安全 ✅

- [ ] **敏感字段已加密**
  - 银行卡号、身份证号等使用加密存储
  - 使用Fernet或AES加密

---

## 10. 安全事件响应

### 10.1 密钥泄露处理流程

如果密钥/密码泄露，立即执行以下步骤:

**第1步: 紧急响应** (0-1小时)
```bash
# 1. 🚨 立即轮换密钥
# 登录密钥管理服务，生成新密钥

# 2. 🔒 撤销旧密钥
# 禁用已泄露的密钥访问权限

# 3. 📝 记录事件
# 记录泄露时间、影响范围、响应措施
```

**第2步: 影响评估** (1-4小时)
```bash
# 1. 🔍 审计日志，查找异常访问
grep "FAILED_LOGIN" /var/log/auth.log
grep "UNAUTHORIZED" /var/log/app.log

# 2. 📊 评估影响范围
# - 哪些系统受影响？
# - 数据是否被访问？
# - 是否有数据泄露？
```

**第3步: 修复部署** (4-24小时)
```bash
# 1. 🔄 更新配置
# 更新 .env 文件，使用新密钥

# 2. 🚀 重新部署
git add .env.prod
git commit -m "security: 轮换密钥 (事件响应)"
# 部署到生产环境

# 3. ✅ 验证新密钥
# 测试所有功能正常
```

**第4步: 总结改进** (1-3天)
```bash
# 1. 📢 通知相关人员
# 邮件通知团队成员

# 2. 📝 编写事故报告
# 记录根本原因、影响范围、改进措施

# 3. 🔧 改进措施
# - 启用密钥自动轮换
# - 加强访问控制
# - 培训开发人员
```

---

### 10.2 安全漏洞报告

**发现安全漏洞时**:

1. **邮箱报告**: security@example.com
2. **响应时间**: 24小时内回复
3. **修复周期**: 7天内发布补丁（严重漏洞48小时）
4. **奖励机制**: 根据漏洞等级提供奖励

**漏洞等级**:
- **严重**: 远程代码执行、SQL注入、认证绕过
- **高危**: 权限提升、敏感信息泄露
- **中危**: CSRF、XSS、信息泄露
- **低危**: 配置问题、轻微信息泄露

---

### 10.3 应急联系方式

```
安全团队: security@example.com
24小时热线: +86-xxx-xxxx-xxxx
Slack频道: #security-incidents
值班表: 查看内部Wiki
```

---

## 11. 参考资源

### 安全标准

- **[OWASP Top 10](https://owasp.org/www-project-top-ten/)** - Web应用十大安全风险
- **[CWE Top 25](https://cwe.mitre.org/top25/)** - 最危险的软件弱点
- **[NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)** - 网络安全框架

### Python安全

- **[Python Security Best Practices](https://python.org/dev/security/)** - Python官方安全指南
- **[Bandit](https://github.com/PyCQA/bandit)** - Python代码安全审计工具
- **[Safety](https://github.com/pyupio/safety)** - Python依赖漏洞扫描

### 加密工具

- **[Cryptography](https://cryptography.io/)** - Python加密库
- **[PyNaCl](https://pynacl.readthedocs.io/)** - libsodium Python绑定

### 学习资源

- **[PortSwigger Web Security Academy](https://portswigger.net/web-security)** - 免费Web安全学习平台
- **[HackTheBox](https://www.hackthebox.com/)** - 安全训练平台
- **[OWASP WebGoat](https://owasp.org/www-project-webgoat/)** - Web安全实践项目

---

## 📞 支持与反馈

**遇到安全问题?**
- 📧 邮箱: security@example.com
- 💬 GitHub Issues: [报告问题](https://github.com/example/df-test-framework/issues)
- 📚 文档: [查看更多文档](../README.md)

---

**最后更新**: 2025-11-25
**版本**: v3.7.0
**维护者**: DF Test Framework Team
