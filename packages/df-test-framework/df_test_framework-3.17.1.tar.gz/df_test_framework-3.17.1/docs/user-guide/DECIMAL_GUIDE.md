# Decimal 类型使用指南

本文档说明如何在测试框架中正确使用 `Decimal` 类型处理金额、价格等精确数值。

## 📚 目录

- [为什么使用 Decimal](#为什么使用-decimal)
- [推荐用法（零配置）](#推荐用法零配置)
- [工作原理](#工作原理)
- [特殊格式需求](#特殊格式需求)
- [常见问题](#常见问题)

## 为什么使用 Decimal

### ❌ 浮点数的问题

```python
# Python 浮点数有精度问题
0.1 + 0.2  # 0.30000000000000004 ❌
```

### ✅ Decimal 的优势

```python
from decimal import Decimal

Decimal("0.1") + Decimal("0.2")  # Decimal('0.3') ✅
```

**金融场景必须使用 Decimal！**

## 推荐用法（零配置）

### 方式 1: 直接使用 Decimal（99% 场景）

```python
from pydantic import BaseModel, Field
from decimal import Decimal

# ✅ 推荐：直接使用标准 Decimal 类型
class PaymentRequest(BaseModel):
    amount: Decimal = Field(..., gt=0, description="支付金额")
    currency: str = Field(default="CNY", description="货币代码")

# 测试代码
def test_payment(http_client):
    request = PaymentRequest(
        amount=Decimal("123.45"),
        currency="CNY"
    )

    # ✅ HttpClient 自动处理序列化
    # 发送的 JSON: {"amount":"123.45","currency":"CNY"}
    response = http_client.post("/api/payment", json=request)

    assert response.status_code == 200
```

**关键点**：
- ✅ 使用标准的 `Decimal` 类型
- ✅ HttpClient 自动序列化为 JSON 字符串
- ✅ 无需任何额外配置
- ✅ IDE 类型提示完美

### 方式 2: 从框架导入（可选）

```python
from df_test_framework import Decimal  # 等价于 from decimal import Decimal
from pydantic import BaseModel

class OrderRequest(BaseModel):
    total_amount: Decimal
    tax_amount: Decimal
```

## 工作原理

### JSON 序列化过程

```python
from pydantic import BaseModel
from decimal import Decimal

class Model(BaseModel):
    amount: Decimal

m = Model(amount=Decimal('123.45'))

# 1. Python 字典（保持 Decimal 类型）
print(m.model_dump())
# {'amount': Decimal('123.45')}

# 2. JSON 字符串（Decimal 自动转为字符串）
print(m.model_dump_json())
# {"amount":"123.45"}

# 3. 使用 json.dumps 会报错 ❌
import json
json.dumps(m.model_dump())
# TypeError: Object of type Decimal is not JSON serializable
```

### HttpClient 的处理

```python
# HttpClient 内部实现（简化版）
def post(self, url: str, json: BaseModel | dict | None = None, **kwargs):
    if isinstance(json, BaseModel):
        # ✅ 使用 model_dump_json() 自动处理 Decimal
        kwargs['data'] = json.model_dump_json()
        kwargs['headers'] = {'Content-Type': 'application/json'}
        json = None

    return self.request("POST", url, json=json, **kwargs)
```

**自动处理的类型**：
- ✅ `Decimal` → 字符串
- ✅ `datetime` → ISO 8601 字符串
- ✅ `UUID` → 字符串
- ✅ `Enum` → 值
- ✅ `Path` → 字符串

## 特殊格式需求

### 场景 1: 浮点数格式（不推荐）

某些老旧 API 要求金额为数字类型：

```python
from df_test_framework import DecimalAsFloat
from pydantic import BaseModel

class LegacyRequest(BaseModel):
    price: DecimalAsFloat  # 序列化为浮点数

request = LegacyRequest(price=Decimal("99.99"))
print(request.model_dump_json())
# {"price":99.99}  # 注意：数字类型，不是字符串
```

⚠️ **警告**：浮点数有精度问题，仅用于与不支持字符串金额的 API 交互。

### 场景 2: 货币格式

显示层需要格式化的金额：

```python
from df_test_framework import DecimalAsCurrency
from pydantic import BaseModel

class DisplayRequest(BaseModel):
    total: DecimalAsCurrency  # 序列化为货币格式

request = DisplayRequest(total=Decimal("123.45"))
print(request.model_dump_json())
# {"total":"$123.45"}
```

### 场景 3: 自定义格式

需要特殊的序列化逻辑：

```python
from pydantic import BaseModel, field_serializer
from decimal import Decimal

class InvoiceRequest(BaseModel):
    amount: Decimal

    @field_serializer('amount')
    def serialize_amount(self, value: Decimal) -> str:
        # 自定义格式：保留4位小数
        return f"{value:.4f}"

request = InvoiceRequest(amount=Decimal("123.456789"))
print(request.model_dump_json())
# {"amount":"123.4568"}
```

### 场景 4: 多字段统一处理

```python
from pydantic import BaseModel, model_serializer
from decimal import Decimal

class FinancialRequest(BaseModel):
    price: Decimal
    tax: Decimal
    discount: Decimal

    @model_serializer
    def serialize_model(self):
        """所有 Decimal 字段保留2位小数"""
        return {
            k: f"{v:.2f}" if isinstance(v, Decimal) else v
            for k, v in self.__dict__.items()
        }

request = FinancialRequest(
    price=Decimal("99.999"),
    tax=Decimal("10.001"),
    discount=Decimal("5.005")
)
print(request.model_dump_json())
# {"price":"100.00","tax":"10.00","discount":"5.01"}
```

## 常见问题

### Q1: 为什么 Decimal 序列化为字符串而不是数字？

**A**: 这是金融 API 的最佳实践：
- ✅ 无精度损失
- ✅ 跨语言兼容（Java、Go、JavaScript 的 Decimal 处理不同）
- ✅ 符合 JSON RFC 标准
- ✅ Stripe、PayPal 等主流 API 都使用字符串

**参考**：
- [Stripe API 文档](https://stripe.com/docs/api) - 金额使用字符串
- [OpenAPI 3.0](https://swagger.io/docs/specification/data-models/data-types/) - 建议金额用 `string` + `format: decimal`

### Q2: 响应模型也需要特殊处理吗？

**A**: 不需要！响应模型直接用 `Decimal`：

```python
from pydantic import BaseModel
from decimal import Decimal

# ✅ 响应模型：直接用 Decimal
class PaymentResponse(BaseModel):
    amount: Decimal  # Pydantic 自动从 JSON 字符串解析
    status: str

# Pydantic 会自动处理：
# JSON: {"amount":"123.45"} → Python: Decimal("123.45")
```

### Q3: 如何在测试中断言 Decimal 值？

```python
from decimal import Decimal

# ✅ 正确方式
assert response.data.amount == Decimal("123.45")

# ❌ 错误方式（浮点数比较）
assert float(response.data.amount) == 123.45  # 可能有精度问题
```

### Q4: 如何初始化 Decimal？

```python
from decimal import Decimal

# ✅ 推荐：使用字符串
amount = Decimal("123.45")

# ⚠️ 不推荐：使用浮点数（可能有精度问题）
amount = Decimal(123.45)  # Decimal('123.4500000000000028421709430404007434844970703125')

# ✅ 也可以：使用整数
cents = Decimal(12345)  # Decimal('12345')
amount = cents / 100    # Decimal('123.45')
```

### Q5: 旧项目如何迁移？

如果项目中有类似 `DecimalAsStr` 的自定义类型：

```python
# ❌ 旧代码
from project.models.base import DecimalAsStr

class Request(BaseModel):
    amount: DecimalAsStr

# ✅ 新代码（直接改为 Decimal）
from decimal import Decimal

class Request(BaseModel):
    amount: Decimal  # HttpClient 自动处理
```

**迁移步骤**：
1. 全局搜索替换 `DecimalAsStr` → `Decimal`
2. 更新导入：`from decimal import Decimal`
3. 运行测试验证

### Q6: 如何处理 Decimal 计算？

```python
from decimal import Decimal, ROUND_HALF_UP

# ✅ 基本运算
price = Decimal("99.99")
tax_rate = Decimal("0.13")
tax = price * tax_rate  # Decimal('12.9987')

# ✅ 四舍五入
tax = tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)  # Decimal('13.00')

# ✅ 格式化输出
print(f"税额: {tax:.2f}")  # 税额: 13.00
```

## 最佳实践总结

### ✅ 推荐做法

1. **请求模型**：直接使用 `Decimal`
   ```python
   class Request(BaseModel):
       amount: Decimal  # ✅
   ```

2. **响应模型**：直接使用 `Decimal`
   ```python
   class Response(BaseModel):
       amount: Decimal  # ✅
   ```

3. **传给 HttpClient**：直接传 Pydantic 模型
   ```python
   response = http_client.post("/api", json=request)  # ✅
   ```

4. **初始化 Decimal**：使用字符串
   ```python
   amount = Decimal("123.45")  # ✅
   ```

### ❌ 避免做法

1. ❌ 使用浮点数
   ```python
   amount = 123.45  # 类型应该是 Decimal
   ```

2. ❌ 手动序列化
   ```python
   json.dumps(request.model_dump())  # 会报错
   ```

3. ❌ 浮点数初始化 Decimal
   ```python
   Decimal(123.45)  # 有精度问题
   ```

## 相关文档

- [Pydantic 官方文档 - Decimal 序列化](https://docs.pydantic.dev/latest/concepts/serialization/#decimal-serialization)
- [Python Decimal 官方文档](https://docs.python.org/3/library/decimal.html)
- [配置指南](./configuration.md)
- [HTTP 客户端使用](./QUICK_START_V3.5.md#http-客户端)
