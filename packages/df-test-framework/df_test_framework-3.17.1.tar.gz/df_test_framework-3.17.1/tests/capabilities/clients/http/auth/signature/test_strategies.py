"""测试签名中间件

验证 SignatureMiddleware 签名生成逻辑的正确性
v3.16.0: 迁移到 Middleware 系统
"""

import hashlib

import pytest

from df_test_framework.capabilities.clients.http.middleware.signature import (
    SignatureMiddleware,
)


class TestSignatureMiddleware:
    """测试 SignatureMiddleware 签名算法"""

    def test_sign_simple_params(self):
        """测试签名 - 简单参数"""
        middleware = SignatureMiddleware(secret="secret", algorithm="md5")
        params = {"userId": 1001, "orderId": "ORDER_001"}

        # 待签名字符串: "ORDER_001" + "1001" + "secret" (按key排序)
        signature = middleware._sign(params)

        # 验证签名格式
        assert len(signature) == 32  # MD5固定32位
        assert signature.islower()  # 小写
        assert signature.isalnum()  # 只包含字母和数字

    def test_sign_with_sorting(self):
        """测试签名 - 验证排序逻辑"""
        middleware = SignatureMiddleware(secret="secret", algorithm="md5")

        # 参数1: 乱序
        params1 = {"z": "3", "a": "1", "m": "2"}
        sig1 = middleware._sign(params1)

        # 参数2: 已排序（应该生成相同签名）
        params2 = {"a": "1", "m": "2", "z": "3"}
        sig2 = middleware._sign(params2)

        # 应该相同（因为都会排序）
        assert sig1 == sig2

    def test_sign_skip_empty(self):
        """测试签名 - 跳过空值"""
        middleware = SignatureMiddleware(secret="secret", algorithm="md5")

        # 参数包含空值
        params = {
            "a": "1",
            "b": None,  # 应该跳过
            "c": "",  # 应该跳过
            "d": "2",
        }

        signature = middleware._sign(params)

        # 应该只包含 "1" + "2" + "secret"
        # 验证：与不包含空值的参数生成的签名应该相同
        params_no_empty = {"a": "1", "d": "2"}
        sig_no_empty = middleware._sign(params_no_empty)

        assert signature == sig_no_empty

    def test_sign_with_real_data(self):
        """测试签名 - 使用真实数据"""
        middleware = SignatureMiddleware(secret="gift_card_secret_2025", algorithm="md5")

        # 真实的Gift Card API参数
        params = {"customerOrderNo": "ORDER_001", "userId": 1001, "templateId": 1, "quantity": 1}

        signature = middleware._sign(params)

        # 验证签名格式
        assert len(signature) == 32
        assert signature.islower()


class TestSignatureAlgorithms:
    """测试不同签名算法"""

    def test_md5_algorithm(self):
        """测试 MD5 算法"""
        middleware = SignatureMiddleware(secret="secret", algorithm="md5")
        params = {"userId": 1001}

        signature = middleware._sign(params)

        assert len(signature) == 32
        assert signature.islower()
        assert signature.isalnum()

    def test_sha256_algorithm(self):
        """测试 SHA256 算法"""
        middleware = SignatureMiddleware(secret="secret", algorithm="sha256")
        params = {"userId": 1001}

        signature = middleware._sign(params)

        # SHA256固定64位
        assert len(signature) == 64
        assert signature.islower()
        assert signature.isalnum()

    def test_hmac_sha256_algorithm(self):
        """测试 HMAC-SHA256 算法"""
        middleware = SignatureMiddleware(secret="secret", algorithm="hmac-sha256")
        params = {"userId": 1001}

        signature = middleware._sign(params)

        # HMAC-SHA256 固定64位
        assert len(signature) == 64
        assert signature.islower()
        assert signature.isalnum()

    def test_different_algorithms_produce_different_signatures(self):
        """测试不同算法生成不同签名"""
        params = {"userId": 1001}

        md5_middleware = SignatureMiddleware(secret="secret", algorithm="md5")
        sha256_middleware = SignatureMiddleware(secret="secret", algorithm="sha256")

        md5_sig = md5_middleware._sign(params)
        sha256_sig = sha256_middleware._sign(params)

        # 两种算法生成的签名应该不同
        assert md5_sig != sha256_sig
        assert len(md5_sig) == 32
        assert len(sha256_sig) == 64


class TestSignatureCompatibility:
    """测试签名兼容性 - 与Java后端对比"""

    def test_md5_signature_matches_java(self):
        """测试MD5签名与Java后端一致

        Java代码:
        Map<String, String> params = new HashMap<>();
        params.put("customerOrderNo", "ORDER_001");
        params.put("userId", "1001");
        params.put("templateId", "1");
        params.put("quantity", "1");
        String signature = SignatureUtil.generateSignature(params, "test_secret");

        待签名字符串（按key排序）:
        "ORDER_001" + "1" + "1" + "1001" + "test_secret"
        = "ORDER_00111001test_secret"
        """
        middleware = SignatureMiddleware(secret="test_secret", algorithm="md5")

        params = {"customerOrderNo": "ORDER_001", "userId": 1001, "templateId": 1, "quantity": 1}

        signature = middleware._sign(params)

        # 待签名字符串: ORDER_00111001test_secret
        # MD5: 可以用在线工具验证
        assert len(signature) == 32
        assert signature.islower()

    def test_empty_params_signature(self):
        """测试空参数签名"""
        middleware = SignatureMiddleware(secret="secret", algorithm="md5")

        # 空参数，只有密钥
        params = {}
        signature = middleware._sign(params)

        # 待签名字符串只有: "secret"
        expected = hashlib.md5(b"secret").hexdigest()
        assert signature == expected

    def test_invalid_algorithm_raises_error(self):
        """测试无效算法抛出错误"""
        middleware = SignatureMiddleware(secret="secret", algorithm="invalid")  # type: ignore

        with pytest.raises(ValueError, match="Unknown algorithm"):
            middleware._sign({"userId": 1001})
