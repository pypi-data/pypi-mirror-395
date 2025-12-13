"""测试JSON到Pydantic模型生成器"""

import pytest

from df_test_framework.cli.generators.json_to_model import (
    _to_pascal_case,
    _to_snake_case,
    generate_model_class,
    generate_pydantic_model_from_json,
    infer_python_type,
)


class TestSnakeCaseConversion:
    """测试蛇形命名转换"""

    def test_camel_case_to_snake_case(self):
        """测试驼峰转蛇形"""
        assert _to_snake_case("userId") == "user_id"
        assert _to_snake_case("orderNo") == "order_no"
        assert _to_snake_case("customerOrderNo") == "customer_order_no"

    def test_consecutive_capitals(self):
        """测试连续大写字母"""
        assert _to_snake_case("ID") == "id"
        assert _to_snake_case("API") == "api"
        assert _to_snake_case("HTTPClient") == "http_client"

    def test_already_snake_case(self):
        """测试已经是蛇形的情况"""
        assert _to_snake_case("user_id") == "user_id"
        assert _to_snake_case("order_no") == "order_no"


class TestPascalCaseConversion:
    """测试帕斯卡命名转换"""

    def test_snake_case_to_pascal_case(self):
        """测试蛇形转帕斯卡"""
        assert _to_pascal_case("user_id") == "UserId"
        assert _to_pascal_case("order_no") == "OrderNo"
        assert _to_pascal_case("customer_order_no") == "CustomerOrderNo"

    def test_single_word(self):
        """测试单个单词"""
        assert _to_pascal_case("user") == "User"
        assert _to_pascal_case("order") == "Order"


class TestTypeInference:
    """测试类型推断"""

    def test_basic_types(self):
        """测试基础类型推断"""
        assert infer_python_type("hello") == ("str", False)
        assert infer_python_type(123) == ("int", False)
        assert infer_python_type(123.45) == ("float", False)
        assert infer_python_type(True) == ("bool", False)
        assert infer_python_type(None) == ("Any", True)

    def test_list_of_basic_types(self):
        """测试基础类型数组"""
        assert infer_python_type(["a", "b"]) == ("List[str]", False)
        assert infer_python_type([1, 2, 3]) == ("List[int]", False)
        assert infer_python_type([]) == ("List[Any]", False)

    def test_list_of_objects(self):
        """测试对象数组"""
        data = [{"name": "John", "age": 30}]
        type_str, is_optional = infer_python_type(data, "users")
        # 注意: 字段名users会被转换为类名Users（帕斯卡命名）
        assert type_str == "List[Users]"
        assert not is_optional

    def test_nested_object(self):
        """测试嵌套对象"""
        data = {"nested": "value"}
        type_str, is_optional = infer_python_type(data, "metadata")
        assert type_str == "Metadata"
        assert not is_optional


class TestModelGeneration:
    """测试模型生成"""

    def test_generate_simple_model(self):
        """测试生成简单模型"""
        data = {"userId": "123", "userName": "张三", "age": 25}

        code, nested_classes = generate_model_class("UserData", data)

        # 检查代码包含关键内容
        assert "class UserData(BaseModel):" in code
        assert 'user_id: str = Field(..., alias="userId"' in code
        assert 'user_name: str = Field(..., alias="userName"' in code
        assert "age: int = Field(...," in code
        assert len(nested_classes) == 0

    def test_generate_model_with_nested_object(self):
        """测试生成带嵌套对象的模型"""
        data = {"userId": "123", "profile": {"name": "张三", "age": 25}}

        code, nested_classes = generate_model_class("UserData", data)

        # 检查主类
        assert "class UserData(BaseModel):" in code
        assert "profile: Profile" in code

        # 检查嵌套类
        assert len(nested_classes) == 1
        assert "class Profile(BaseModel):" in nested_classes[0]

    def test_generate_model_with_array(self):
        """测试生成带数组的模型"""
        data = {"orders": [{"orderId": "001", "amount": 100.0}]}

        code, nested_classes = generate_model_class("UserData", data)

        # 检查主类
        assert "class UserData(BaseModel):" in code
        assert "orders: List[Order]" in code

        # 检查嵌套类
        assert len(nested_classes) == 1
        assert "class Order(BaseModel):" in nested_classes[0]


class TestCompleteGeneration:
    """测试完整生成流程"""

    def test_generate_from_response_json(self):
        """测试从响应JSON生成完整模型"""
        json_data = {
            "code": 200,
            "message": "success",
            "data": {"userId": "123", "userName": "张三", "age": 25, "tags": ["vip", "active"]},
        }

        code = generate_pydantic_model_from_json(
            json_data,
            model_name="UserResponse",
            wrap_in_base_response=True,
        )

        # 检查导入语句
        assert "from pydantic import BaseModel, Field" in code
        assert "from df_test_framework.models.responses import BaseResponse" in code

        # 检查数据类
        assert "class UserResponseData(BaseModel):" in code
        assert 'user_id: str = Field(..., alias="userId"' in code
        assert "tags: List[str]" in code

        # 检查响应包装类
        assert "class UserResponse(BaseResponse[UserResponseData]):" in code

    def test_generate_without_base_response_wrap(self):
        """测试不使用BaseResponse包装"""
        json_data = {"userId": "123", "userName": "张三"}

        code = generate_pydantic_model_from_json(
            json_data,
            model_name="User",
            wrap_in_base_response=False,
        )

        # 不应该有BaseResponse导入
        assert "from df_test_framework.models.responses import BaseResponse" not in code

        # 直接生成模型类
        assert "class User(BaseModel):" in code
        assert "class UserData(BaseModel):" not in code

    def test_complex_nested_structure(self):
        """测试复杂嵌套结构"""
        json_data = {
            "code": 200,
            "data": {
                "orderNo": "ORDER123",
                "items": [
                    {"itemId": "item_001", "product": {"productId": "prod_001", "name": "产品A"}}
                ],
                "metadata": {"source": "web", "deviceInfo": {"platform": "Windows"}},
            },
        }

        code = generate_pydantic_model_from_json(
            json_data,
            model_name="OrderResponse",
            wrap_in_base_response=True,
        )

        # 检查所有嵌套类都生成了
        assert "class Product(BaseModel):" in code
        assert "class Item(BaseModel):" in code
        assert "class DeviceInfo(BaseModel):" in code
        assert "class Metadata(BaseModel):" in code
        assert "class OrderResponseData(BaseModel):" in code
        assert "class OrderResponse(BaseResponse[OrderResponseData]):" in code


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
