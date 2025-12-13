# BaseAPI最佳实践指南

> **版本**: v1.3.1
> **作者**: df-test-framework团队
> **更新日期**: 2025-10-30
> **框架状态**: ✅ 生产就绪
> ⚠️ **Legacy**: 本指南基于 v1.x BaseAPI 模式，归档供参考。v2 推荐优先阅读最新的 [使用示例](../guides/使用示例.md) 和扩展文档。

## 📚 目录

- [概述](#概述)
- [核心设计理念](#核心设计理念)
- [设计模式对比](#设计模式对比)
- [最佳实践](#最佳实践)
- [实战案例](#实战案例)
- [常见问题](#常见问题)
- [性能优化](#性能优化)

---

## 概述

`BaseAPI`是df-test-framework的核心基类,所有API封装类都应该继承它。本文档详细说明了如何正确使用BaseAPI,以及为什么要这样设计。

### BaseAPI的设计哲学

```python
class BaseAPI:
    """API基类 - 使用依赖注入模式"""

    def __init__(self, http_client: HttpClient):
        """
        Args:
            http_client: HTTP客户端实例(由外部注入)
        """
        self.client = http_client
```

**核心原则**: BaseAPI采用**依赖注入(Dependency Injection)**模式,不自己创建依赖,而是接受外部传入的依赖。

---

## 核心设计理念

### 为什么使用依赖注入?

#### 1. 资源共享与性能优化

```python
# ✅ 正确: 多个API共享一个HttpClient
http_client = HttpClient(base_url="http://api.example.com", timeout=30)

api1 = UserAPI(http_client)      # 共享连接池
api2 = OrderAPI(http_client)     # 共享连接池
api3 = ProductAPI(http_client)   # 共享连接池

# 结果: 3个API实例,1个连接池,性能最优
```

```python
# ❌ 错误: 每个API创建自己的HttpClient
class UserAPI(BaseAPI):
    def __init__(self, base_url: str):
        # 不好的做法: 内部创建HttpClient
        http_client = HttpClient(base_url=base_url)
        super().__init__(http_client)

api1 = UserAPI("http://api.example.com")   # 连接池1
api2 = OrderAPI("http://api.example.com")  # 连接池2
api3 = ProductAPI("http://api.example.com") # 连接池3

# 结果: 3个API实例,3个连接池,资源浪费
```

**性能对比**:

| 方式 | HttpClient数量 | 连接池数量 | TCP连接数 | 性能 |
|------|---------------|-----------|----------|------|
| 依赖注入 | 1 | 1 | 复用 | ⚡⚡⚡ 优秀 |
| 内部创建 | N | N | 重复创建 | ❌ 差 |

#### 2. 测试友好性

```python
# ✅ 容易mock
def test_user_api():
    # 创建mock HttpClient
    mock_client = Mock(spec=HttpClient)
    mock_client.get.return_value = Mock(status_code=200, json=lambda: {"data": []})

    # 注入mock对象
    api = UserAPI(mock_client)

    # 测试API逻辑,不依赖真实网络
    result = api.get_users()
    assert result.success
```

```python
# ❌ 难以mock
class UserAPI(BaseAPI):
    def __init__(self, base_url: str):
        # 内部创建,无法注入mock
        http_client = HttpClient(base_url=base_url)
        super().__init__(http_client)

# 无法mock内部创建的HttpClient,测试困难
```

#### 3. 灵活性与可扩展性

```python
# ✅ 可以注入带不同配置的HttpClient

# 场景1: 需要认证的API
authenticated_client = HttpClient(
    base_url="http://api.example.com",
    headers={"Authorization": "Bearer token123"}
)
api = UserAPI(authenticated_client)

# 场景2: 需要自定义超时的API
slow_client = HttpClient(
    base_url="http://slow-api.example.com",
    timeout=120  # 2分钟超时
)
api = ReportAPI(slow_client)

# 场景3: 需要代理的API
proxy_client = HttpClient(
    base_url="http://api.example.com",
    proxies={"http": "http://proxy.com:8080"}
)
api = ExternalAPI(proxy_client)
```

#### 4. 符合SOLID原则

- **S**ingle Responsibility: API类只负责API调用逻辑,不负责创建HttpClient
- **O**pen/Closed: 对扩展开放(可以注入任何HttpClient),对修改关闭
- **L**iskov Substitution: 可以注入HttpClient的任何子类
- **I**nterface Segregation: API类只依赖HttpClient接口,不依赖具体实现
- **D**ependency Inversion: 依赖抽象(HttpClient),不依赖具体创建过程

---

## 设计模式对比

### 模式1: 依赖注入 (推荐) ✅

```python
class GiftCardAPI(BaseAPI):
    """正确的实现方式"""

    def __init__(self, http_client: HttpClient):
        """注入HttpClient依赖"""
        super().__init__(http_client)
        self.base_path = "/api/gift-card"

    def create_card(self, request: CreateCardRequest):
        response = self.client.post(f"{self.base_path}/create", json=request.dict())
        return response
```

**优点总结**:
- ✅ 资源共享,性能优秀
- ✅ 易于测试和mock
- ✅ 灵活性高,可扩展
- ✅ 符合框架设计
- ✅ 遵循SOLID原则

**使用方式**:
```python
# 创建共享的HttpClient
http_client = HttpClient(base_url="http://api.example.com", timeout=30)

# 创建多个API实例,共享连接
api1 = GiftCardAPI(http_client)
api2 = OrderAPI(http_client)
api3 = UserAPI(http_client)
```

### 模式2: 工厂模式 (不推荐) ❌

```python
class GiftCardAPI(BaseAPI):
    """不推荐的实现方式"""

    def __init__(self, base_url: str, timeout: int = 30):
        """内部创建HttpClient"""
        # ❌ 问题: 每次创建API都会创建新的HttpClient
        http_client = HttpClient(base_url=base_url, timeout=timeout)
        super().__init__(http_client)
        self.base_path = "/api/gift-card"
```

**缺点总结**:
- ❌ 资源浪费,每个API一个连接池
- ❌ 难以测试和mock
- ❌ 灵活性差,无法自定义HttpClient
- ❌ 违反框架设计意图
- ❌ 不符合SOLID原则

### 模式3: 混合模式 (折中方案) ⚠️

```python
class GiftCardAPI(BaseAPI):
    """折中方案: 支持两种方式"""

    def __init__(self, http_client: HttpClient = None,
                 base_url: str = None, timeout: int = 30):
        """既可以注入,也可以自动创建"""
        if http_client is None:
            if base_url is None:
                raise ValueError("必须提供http_client或base_url")
            http_client = HttpClient(base_url=base_url, timeout=timeout)

        super().__init__(http_client)
```

**评价**:
- ⚠️ 使用方便,但容易被误用
- ⚠️ 接口复杂,增加维护成本
- ⚠️ 不鼓励使用,除非有特殊需求

---

## 最佳实践

### 实践1: 在pytest中使用fixtures

这是**最推荐**的使用方式,适用于自动化测试项目。

```python
# tests/conftest.py

import pytest
from df_test_framework import HttpClient
from api.gift_card_api import GiftCardAPI
from api.order_api import OrderAPI
from config.settings import settings

# ========== HttpClient Fixture (session级别) ==========

@pytest.fixture(scope="session")
def http_client() -> HttpClient:
    """
    提供共享的HTTP客户端

    - scope="session": 整个测试会话只创建一次
    - 所有测试共享,性能最优
    - 会话结束时自动关闭
    """
    client = HttpClient(
        base_url=settings.api_base_url,
        timeout=settings.api_timeout,
    )
    yield client
    client.close()  # 清理资源


# ========== API Fixtures (function级别) ==========

@pytest.fixture(scope="function")
def gift_card_api(http_client) -> GiftCardAPI:
    """
    提供GiftCardAPI实例

    - scope="function": 每个测试函数都有独立实例
    - 注入session级别的http_client,共享连接池
    - 测试隔离 + 资源共享 = 最佳实践
    """
    return GiftCardAPI(http_client)


@pytest.fixture(scope="function")
def order_api(http_client) -> OrderAPI:
    """提供OrderAPI实例,共享http_client"""
    return OrderAPI(http_client)
```

**在测试中使用**:

```python
# tests/test_gift_card.py

def test_create_card(gift_card_api):
    """
    fixture自动注入,开箱即用
    gift_card_api已经配置好,直接使用
    """
    request = CreateCardRequest(amount=100.0)
    response = gift_card_api.create_card(request)
    assert response.success


def test_create_and_query(gift_card_api, order_api):
    """
    多个API同时使用,共享底层连接
    gift_card_api.client is order_api.client  # True
    """
    # 创建卡片
    card = gift_card_api.create_card(CreateCardRequest(amount=100.0))

    # 创建订单(使用同一个http_client)
    order = order_api.create_order(OrderRequest(card_id=card.id))

    assert card.success
    assert order.success
```

**关键点**:
- `http_client`: session级别,只创建一次
- `gift_card_api`: function级别,每个测试独立实例
- 结果: 测试隔离 + 连接池共享 = 完美平衡

### 实践2: 在脚本中使用

适用于独立脚本、数据初始化、手动测试等场景。

```python
# scripts/init_data.py

from df_test_framework import HttpClient
from api.gift_card_api import GiftCardAPI
from api.order_api import OrderAPI
from config.settings import settings

def main():
    # 创建HttpClient
    http_client = HttpClient(
        base_url=settings.api_base_url,
        timeout=settings.api_timeout
    )

    try:
        # 创建API实例,注入http_client
        gift_card_api = GiftCardAPI(http_client)
        order_api = OrderAPI(http_client)

        # 使用API
        print("初始化礼品卡数据...")
        for i in range(10):
            card = gift_card_api.create_card(
                CreateCardRequest(amount=100.0, code=f"CARD{i:03d}")
            )
            print(f"创建卡片: {card.data.code}")

        print("初始化完成!")

    finally:
        # 确保关闭连接
        http_client.close()
        print("连接已关闭")

if __name__ == "__main__":
    main()
```

### 实践3: 在类中组合多个API

适用于复杂的业务场景,需要协调多个API。

```python
# services/gift_card_service.py

from df_test_framework import HttpClient
from api.gift_card_api import GiftCardAPI
from api.order_api import OrderAPI
from api.payment_api import PaymentAPI

class GiftCardService:
    """礼品卡业务服务,组合多个API"""

    def __init__(self, http_client: HttpClient):
        """注入HttpClient,所有API共享"""
        self.gift_card_api = GiftCardAPI(http_client)
        self.order_api = OrderAPI(http_client)
        self.payment_api = PaymentAPI(http_client)

    def purchase_gift_card(self, amount: float, user_id: str):
        """购买礼品卡的完整流程"""
        # 1. 创建订单
        order = self.order_api.create_order(
            OrderRequest(type="gift_card", amount=amount, user_id=user_id)
        )

        # 2. 支付
        payment = self.payment_api.pay(
            PaymentRequest(order_id=order.data.id, amount=amount)
        )

        # 3. 创建礼品卡
        card = self.gift_card_api.create_card(
            CreateCardRequest(amount=amount, order_id=order.data.id)
        )

        return {
            "order": order.data,
            "payment": payment.data,
            "card": card.data
        }

# 使用
http_client = HttpClient(base_url="http://api.example.com")
service = GiftCardService(http_client)

result = service.purchase_gift_card(amount=100.0, user_id="user123")
print(f"购买成功: {result['card'].code}")

http_client.close()
```

---

## 实战案例

### 案例1: 礼品卡系统测试项目

**项目背景**:
- 真实后端有3个子系统: Master/H5/Admin
- 需要测试8个核心API接口
- 包含25+个测试用例

**实现方案**:

```python
# api/master_card_api.py
class MasterCardAPI(BaseAPI):
    """Master系统API - 批量创建礼品卡"""

    def __init__(self, http_client: HttpClient):
        super().__init__(http_client)
        self.base_path = "/master/card"

# api/h5_card_api.py
class H5CardAPI(BaseAPI):
    """H5用户端API - 查询/支付/退款"""

    def __init__(self, http_client: HttpClient):
        super().__init__(http_client)
        self.base_path = "/h5/card"

# api/admin_consumption_api.py
class AdminConsumptionAPI(BaseAPI):
    """Admin管理端API - 消费记录管理"""

    def __init__(self, http_client: HttpClient):
        super().__init__(http_client)
        self.base_path = "/admin/consumption"
```

```python
# tests/conftest.py
@pytest.fixture(scope="session")
def http_client() -> HttpClient:
    """共享的HttpClient"""
    client = HttpClient(base_url="http://47.94.57.99:8088/api", timeout=30)
    yield client
    client.close()

@pytest.fixture(scope="function")
def master_card_api(http_client) -> MasterCardAPI:
    return MasterCardAPI(http_client)

@pytest.fixture(scope="function")
def h5_card_api(http_client) -> H5CardAPI:
    return H5CardAPI(http_client)

@pytest.fixture(scope="function")
def admin_consumption_api(http_client) -> AdminConsumptionAPI:
    return AdminConsumptionAPI(http_client)
```

```python
# tests/test_e2e/test_complete_flow.py
def test_complete_flow(master_card_api, h5_card_api, admin_consumption_api):
    """完整流程: 创建->支付->查询->退款"""

    # 1. Master创建卡片
    create_resp = master_card_api.create_cards(
        MasterCardCreateRequest(order_no="ORD001", quantity=2)
    )
    assert create_resp.success

    # 2. H5用户支付
    payment_resp = h5_card_api.pay(
        H5PaymentRequest(user_id="user001", amount=50.0)
    )
    assert payment_resp.success

    # 3. Admin查询记录
    records = admin_consumption_api.query_records(
        AdminQueryRequest(card_no=create_resp.data.card_nos[0])
    )
    assert records.success

    # 4. H5退款
    refund_resp = h5_card_api.refund(
        CardRefundRequest(payment_no=payment_resp.data.payment_no)
    )
    assert refund_resp.success
```

**优势体现**:
- ✅ 3个API共享1个HttpClient
- ✅ 25个测试用例共享1个连接池
- ✅ 测试执行速度快
- ✅ 资源占用低

### 案例2: 跨环境测试

```python
# tests/conftest.py

@pytest.fixture(scope="session")
def http_client(request) -> HttpClient:
    """根据环境创建不同配置的HttpClient"""
    env = request.config.getoption("--env", default="test")

    config_map = {
        "test": {
            "base_url": "http://test-api.example.com",
            "timeout": 30,
        },
        "staging": {
            "base_url": "http://staging-api.example.com",
            "timeout": 60,
            "headers": {"X-Environment": "staging"}
        },
        "prod": {
            "base_url": "http://api.example.com",
            "timeout": 120,
            "headers": {"X-Environment": "production"}
        }
    }

    config = config_map.get(env, config_map["test"])
    client = HttpClient(**config)

    yield client
    client.close()

# 运行测试
# pytest --env=test    # 测试环境
# pytest --env=staging # 预发布环境
# pytest --env=prod    # 生产环境
```

---

## 常见问题

### Q1: 为什么不能在API类内部创建HttpClient?

**A**: 主要有4个原因:

1. **性能问题**: 每个API实例都创建新的连接池,浪费资源
2. **测试困难**: 无法注入mock对象,难以进行单元测试
3. **灵活性差**: 无法使用自定义配置的HttpClient
4. **违反设计**: 不符合框架的依赖注入理念

### Q2: 如果我真的需要在API类中创建HttpClient怎么办?

**A**: 可以使用类方法提供便捷的创建方式:

```python
class GiftCardAPI(BaseAPI):
    """同时支持注入和便捷创建"""

    def __init__(self, http_client: HttpClient):
        """标准构造函数 - 依赖注入"""
        super().__init__(http_client)

    @classmethod
    def from_config(cls, base_url: str, timeout: int = 30):
        """类方法 - 便捷创建(不推荐在测试中使用)"""
        http_client = HttpClient(base_url=base_url, timeout=timeout)
        return cls(http_client)

# 使用方式1: 依赖注入(推荐)
http_client = HttpClient(base_url="http://api.example.com")
api = GiftCardAPI(http_client)

# 使用方式2: 便捷创建(不推荐)
api = GiftCardAPI.from_config(base_url="http://api.example.com")
```

### Q3: session级别的http_client会不会有线程安全问题?

**A**: 不会,原因:

1. **pytest的session scope是线程安全的**
2. **httpx的连接池是线程安全的**
3. **BaseAPI不保存状态**,只是调用http_client的方法

如果使用`pytest-xdist`并行执行测试:
```bash
# 每个worker有独立的session
pytest -n 4  # 4个worker,4个独立的http_client
```

### Q4: 如何在API类中使用装饰器?

**A**: 装饰器正常使用,不受依赖注入影响:

```python
from df_test_framework import BaseAPI, track_performance, retry_on_failure

class GiftCardAPI(BaseAPI):
    def __init__(self, http_client: HttpClient):
        super().__init__(http_client)

    @track_performance(threshold_ms=500)
    @retry_on_failure(max_retries=3, delay=1)
    def create_card(self, request: CreateCardRequest):
        """装饰器正常工作"""
        response = self.client.post("/api/cards", json=request.dict())
        return response
```

### Q5: 如果需要不同base_url的API怎么办?

**A**: 创建多个HttpClient:

```python
# tests/conftest.py

@pytest.fixture(scope="session")
def internal_http_client() -> HttpClient:
    """内部API的HttpClient"""
    client = HttpClient(base_url="http://internal-api.example.com")
    yield client
    client.close()

@pytest.fixture(scope="session")
def external_http_client() -> HttpClient:
    """外部API的HttpClient"""
    client = HttpClient(base_url="http://external-api.example.com")
    yield client
    client.close()

@pytest.fixture
def gift_card_api(internal_http_client) -> GiftCardAPI:
    return GiftCardAPI(internal_http_client)

@pytest.fixture
def payment_api(external_http_client) -> PaymentAPI:
    return PaymentAPI(external_http_client)
```

---

## 性能优化

### 优化1: 使用连接池参数

```python
http_client = HttpClient(
    base_url="http://api.example.com",
    timeout=30,
    # 连接池配置
    limits=httpx.Limits(
        max_keepalive_connections=20,  # 最大保持连接数
        max_connections=100,            # 最大连接数
        keepalive_expiry=30.0          # 保持连接时间(秒)
    )
)
```

### 优化2: 复用TCP连接

```python
# ✅ 正确: 共享HttpClient,自动复用TCP连接
http_client = HttpClient(base_url="http://api.example.com")

for i in range(100):
    api = GiftCardAPI(http_client)  # 共享连接池
    api.create_card(...)            # 复用TCP连接
```

```python
# ❌ 错误: 每次创建新HttpClient,无法复用连接
for i in range(100):
    http_client = HttpClient(base_url="http://api.example.com")
    api = GiftCardAPI(http_client)  # 新连接池
    api.create_card(...)            # 新TCP连接
    http_client.close()             # 关闭连接
```

### 优化3: 异步API(高级)

```python
from df_test_framework import AsyncBaseAPI

class AsyncGiftCardAPI(AsyncBaseAPI):
    """异步API"""

    def __init__(self, async_http_client: AsyncHttpClient):
        super().__init__(async_http_client)

    async def create_card(self, request: CreateCardRequest):
        response = await self.client.post("/api/cards", json=request.dict())
        return response

# 使用
async def test_create_card():
    async with AsyncHttpClient(base_url="http://api.example.com") as client:
        api = AsyncGiftCardAPI(client)
        response = await api.create_card(request)
        assert response.success
```

---

## 总结

### 核心要点

1. **依赖注入是最佳实践** ✅
   - BaseAPI接受HttpClient参数
   - 不要在API类内部创建HttpClient

2. **在pytest中使用fixtures** ✅
   - http_client: session级别
   - API实例: function级别
   - 实现测试隔离 + 资源共享

3. **性能优化** ✅
   - 共享连接池
   - 复用TCP连接
   - 减少资源消耗

4. **符合设计原则** ✅
   - SOLID原则
   - 易于测试
   - 高度灵活

### 快速检查清单

在你的项目中检查:

- [ ] API类是否继承自BaseAPI?
- [ ] 构造函数是否接受HttpClient参数?
- [ ] 是否在conftest.py中定义了http_client fixture?
- [ ] http_client fixture是否是session级别?
- [ ] API fixtures是否注入了http_client?
- [ ] 是否在finally块中关闭http_client(脚本中)?
- [ ] 是否避免在API类内部创建HttpClient?

### 参考资源

- [df-test-framework官方文档](../README.md)
- [使用示例](../guides/使用示例.md)
- [架构设计文档](./架构设计文档.md)
- [API参考](./API参考.md)

---

**最后更新**: 2025-10-30
**贡献者**: df-test-framework团队
**框架版本**: v1.3.1

### 重要更新

**v1.2.0及以后**:
- 支持拦截器机制,可在BaseAPI构造函数中传入request/response拦截器
- 配置方式变更为嵌套配置模型

**v1.3.0及以后**:
- 支持Repository模式用于数据库操作封装
- 支持Builder模式用于测试数据构建
- 性能监控功能

**v1.3.1最新**:
- 配置中心与Fixtures完全集成
- SQLAlchemy 2.x完全兼容
- database.execute()返回值变更

如有问题或建议,请提交issue到项目仓库。
