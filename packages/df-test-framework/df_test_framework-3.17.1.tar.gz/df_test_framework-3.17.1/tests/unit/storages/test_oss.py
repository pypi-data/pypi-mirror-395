"""OSSClient 单元测试"""

from unittest.mock import MagicMock, patch

import pytest

from df_test_framework.capabilities.storages.object import OSSClient, OSSConfig
from df_test_framework.core.exceptions import ConfigurationError, ResourceError


class TestOSSConfig:
    """OSSConfig 配置类测试"""

    def test_default_config(self):
        """测试默认配置"""
        config = OSSConfig(
            access_key_id="LTAI5test",
            access_key_secret="secret123",
            bucket_name="test-bucket",
            endpoint="oss-cn-hangzhou.aliyuncs.com",
        )
        assert config.access_key_id == "LTAI5test"
        assert config.access_key_secret == "secret123"
        assert config.bucket_name == "test-bucket"
        assert config.endpoint == "oss-cn-hangzhou.aliyuncs.com"
        assert config.security_token is None
        assert config.connect_timeout == 60
        assert config.multipart_threshold == 10 * 1024 * 1024
        assert config.enable_crc is True

    def test_custom_config(self):
        """测试自定义配置"""
        config = OSSConfig(
            access_key_id="LTAI5test",
            access_key_secret="secret123",
            bucket_name="my-bucket",
            endpoint="oss-cn-shanghai-internal.aliyuncs.com",
            security_token="STS.xxx",
            connect_timeout=30,
            part_size=5 * 1024 * 1024,
            enable_crc=False,
        )
        assert config.endpoint == "oss-cn-shanghai-internal.aliyuncs.com"
        assert config.security_token == "STS.xxx"
        assert config.connect_timeout == 30
        assert config.part_size == 5 * 1024 * 1024
        assert config.enable_crc is False

    def test_required_fields_validation(self):
        """测试必需字段验证"""
        with pytest.raises(ValueError, match="field cannot be empty"):
            OSSConfig(
                access_key_id="",
                access_key_secret="secret",
                bucket_name="bucket",
                endpoint="oss-cn-hangzhou.aliyuncs.com",
            )

        with pytest.raises(ValueError, match="field cannot be empty"):
            OSSConfig(
                access_key_id="key",
                access_key_secret="",
                bucket_name="bucket",
                endpoint="oss-cn-hangzhou.aliyuncs.com",
            )

        with pytest.raises(ValueError, match="field cannot be empty"):
            OSSConfig(
                access_key_id="key",
                access_key_secret="secret",
                bucket_name="",
                endpoint="oss-cn-hangzhou.aliyuncs.com",
            )

    def test_part_size_validation(self):
        """测试分片大小验证"""
        # 太小
        with pytest.raises(ValueError, match="part_size must be between"):
            OSSConfig(
                access_key_id="key",
                access_key_secret="secret",
                bucket_name="bucket",
                endpoint="oss-cn-hangzhou.aliyuncs.com",
                part_size=50 * 1024,  # 50KB < 100KB
            )

        # 太大
        with pytest.raises(ValueError, match="part_size must be between"):
            OSSConfig(
                access_key_id="key",
                access_key_secret="secret",
                bucket_name="bucket",
                endpoint="oss-cn-hangzhou.aliyuncs.com",
                part_size=6 * 1024 * 1024 * 1024,  # 6GB > 5GB
            )


class TestOSSClient:
    """OSSClient 客户端测试"""

    @pytest.fixture
    def config(self):
        """OSSConfig fixture"""
        return OSSConfig(
            access_key_id="LTAI5test",
            access_key_secret="secret123",
            bucket_name="test-bucket",
            endpoint="oss-cn-hangzhou.aliyuncs.com",
        )

    @pytest.fixture
    def mock_oss2(self):
        """Mock oss2 module"""
        with patch("df_test_framework.capabilities.storages.object.oss.client.oss2") as mock_oss2:
            with patch(
                "df_test_framework.capabilities.storages.object.oss.client.OSS2_AVAILABLE", True
            ):
                # Mock Auth
                mock_auth = MagicMock()
                mock_oss2.Auth.return_value = mock_auth

                # Mock Bucket
                mock_bucket = MagicMock()
                mock_oss2.Bucket.return_value = mock_bucket
                mock_bucket.bucket_exists.return_value = True  # Bucket exists by default

                yield mock_oss2, mock_bucket

    def test_init_without_oss2(self, config):
        """测试未安装 oss2 时初始化"""
        with patch(
            "df_test_framework.capabilities.storages.object.oss.client.OSS2_AVAILABLE", False
        ):
            with pytest.raises(ConfigurationError, match="oss2 未安装"):
                OSSClient(config)

    def test_init_with_oss2(self, config, mock_oss2):
        """测试正常初始化"""
        mock_oss2_mod, mock_bucket = mock_oss2

        _ = OSSClient(config)  # 验证初始化成功

        # 验证 Auth 被调用
        mock_oss2_mod.Auth.assert_called_once_with("LTAI5test", "secret123")

        # 验证 Bucket 被创建
        mock_oss2_mod.Bucket.assert_called_once()
        call_kwargs = mock_oss2_mod.Bucket.call_args[1]
        assert call_kwargs["connect_timeout"] == 60
        assert call_kwargs["enable_crc"] is True

    def test_init_with_sts_token(self, mock_oss2):
        """测试使用 STS 临时凭证初始化"""
        mock_oss2_mod, mock_bucket = mock_oss2

        config = OSSConfig(
            access_key_id="STS.xxx",
            access_key_secret="secret123",
            security_token="TOKEN123",
            bucket_name="test-bucket",
            endpoint="oss-cn-hangzhou.aliyuncs.com",
        )

        _ = OSSClient(config)  # 验证初始化成功

        # 验证使用 StsAuth
        mock_oss2_mod.StsAuth.assert_called_once_with("STS.xxx", "secret123", "TOKEN123")

    def test_init_bucket_not_exists(self, config, mock_oss2):
        """测试 Bucket 不存在时初始化"""
        _, mock_bucket = mock_oss2
        mock_bucket.bucket_exists.return_value = False

        with pytest.raises(ConfigurationError, match="Bucket .* 不存在"):
            OSSClient(config)

    def test_upload_bytes(self, config, mock_oss2):
        """测试上传字节内容"""
        _, mock_bucket = mock_oss2

        mock_result = MagicMock()
        mock_result.etag = "abc123"
        mock_result.request_id = "req123"
        mock_bucket.put_object.return_value = mock_result

        client = OSSClient(config)
        result = client.upload("test.txt", b"Hello OSS")

        assert result["key"] == "test.txt"
        assert result["bucket"] == "test-bucket"
        assert result["etag"] == "abc123"

        mock_bucket.put_object.assert_called_once()

    def test_upload_with_metadata(self, config, mock_oss2):
        """测试上传带元数据"""
        _, mock_bucket = mock_oss2

        mock_result = MagicMock()
        mock_result.etag = "abc123"
        mock_result.request_id = "req123"
        mock_bucket.put_object.return_value = mock_result

        client = OSSClient(config)
        client.upload(
            "test.txt",
            b"content",
            metadata={"author": "test"},
            content_type="text/plain",
        )

        # 验证 headers
        call_args = mock_bucket.put_object.call_args
        headers = call_args[1]["headers"]
        assert headers["Content-Type"] == "text/plain"
        assert headers["x-oss-meta-author"] == "test"

    def test_download(self, config, mock_oss2):
        """测试下载文件"""
        _, mock_bucket = mock_oss2

        content = b"Downloaded Content"
        mock_result = MagicMock()
        mock_result.read.return_value = content
        mock_bucket.get_object.return_value = mock_result

        client = OSSClient(config)
        downloaded = client.download("test.txt")

        assert downloaded == content
        mock_bucket.get_object.assert_called_once_with("test.txt")

    def test_download_not_found(self, config, mock_oss2):
        """测试下载不存在的文件"""
        mock_oss2_mod, mock_bucket = mock_oss2

        # Mock NoSuchKey exception
        mock_oss2_mod.NoSuchKey = type("NoSuchKey", (Exception,), {})
        mock_bucket.get_object.side_effect = mock_oss2_mod.NoSuchKey()

        with patch(
            "df_test_framework.capabilities.storages.object.oss.client.NoSuchKey",
            mock_oss2_mod.NoSuchKey,
        ):
            client = OSSClient(config)

            with pytest.raises(ResourceError, match="对象不存在"):
                client.download("nonexistent.txt")

    def test_delete(self, config, mock_oss2):
        """测试删除文件"""
        _, mock_bucket = mock_oss2

        # Mock exists (file exists)
        mock_bucket.head_object.return_value = {}

        client = OSSClient(config)
        result = client.delete("test.txt")

        assert result is True
        mock_bucket.delete_object.assert_called_once_with("test.txt")

    def test_delete_not_found(self, config, mock_oss2):
        """测试删除不存在的文件"""
        mock_oss2_mod, mock_bucket = mock_oss2

        # Mock NoSuchKey exception
        mock_oss2_mod.NoSuchKey = type("NoSuchKey", (Exception,), {})
        mock_bucket.head_object.side_effect = mock_oss2_mod.NoSuchKey()

        with patch(
            "df_test_framework.capabilities.storages.object.oss.client.NoSuchKey",
            mock_oss2_mod.NoSuchKey,
        ):
            client = OSSClient(config)

            with pytest.raises(ResourceError, match="对象不存在"):
                client.delete("nonexistent.txt")

    def test_delete_missing_ok(self, config, mock_oss2):
        """测试删除不存在的文件（允许缺失）"""
        mock_oss2_mod, mock_bucket = mock_oss2

        # Mock NoSuchKey exception
        mock_oss2_mod.NoSuchKey = type("NoSuchKey", (Exception,), {})
        mock_bucket.head_object.side_effect = mock_oss2_mod.NoSuchKey()

        with patch(
            "df_test_framework.capabilities.storages.object.oss.client.NoSuchKey",
            mock_oss2_mod.NoSuchKey,
        ):
            client = OSSClient(config)
            result = client.delete("nonexistent.txt", missing_ok=True)

            assert result is False

    def test_exists(self, config, mock_oss2):
        """测试检查文件是否存在"""
        mock_oss2_mod, mock_bucket = mock_oss2

        client = OSSClient(config)

        # File exists
        mock_bucket.head_object.return_value = {}
        assert client.exists("test.txt") is True

        # File not exists
        mock_oss2_mod.NoSuchKey = type("NoSuchKey", (Exception,), {})
        mock_bucket.head_object.side_effect = mock_oss2_mod.NoSuchKey()

        with patch(
            "df_test_framework.capabilities.storages.object.oss.client.NoSuchKey",
            mock_oss2_mod.NoSuchKey,
        ):
            assert client.exists("test.txt") is False

    def test_list_objects(self, config, mock_oss2):
        """测试列出对象"""
        mock_oss2_mod, mock_bucket = mock_oss2

        # Mock ObjectIterator
        mock_obj1 = MagicMock()
        mock_obj1.key = "file1.txt"
        mock_obj1.size = 100
        mock_obj1.last_modified = "2024-01-01"
        mock_obj1.etag = "etag1"
        mock_obj1.type = "Normal"

        mock_obj2 = MagicMock()
        mock_obj2.key = "file2.txt"
        mock_obj2.size = 200
        mock_obj2.last_modified = "2024-01-02"
        mock_obj2.etag = "etag2"
        mock_obj2.type = "Normal"

        mock_oss2_mod.ObjectIterator.return_value = [mock_obj1, mock_obj2]

        client = OSSClient(config)
        objects = client.list_objects(prefix="test/")

        assert len(objects) == 2
        assert objects[0]["key"] == "file1.txt"
        assert objects[0]["size"] == 100
        assert objects[1]["key"] == "file2.txt"

    def test_get_object_info(self, config, mock_oss2):
        """测试获取对象信息"""
        _, mock_bucket = mock_oss2

        mock_meta = MagicMock()
        mock_meta.content_length = 1024
        mock_meta.content_type = "text/plain"
        mock_meta.last_modified = "2024-01-01"
        mock_meta.etag = "abc123"
        mock_meta.headers = {
            "x-oss-meta-author": "test",
            "x-oss-meta-version": "1.0",
            "Content-Type": "text/plain",
        }
        mock_bucket.head_object.return_value = mock_meta

        client = OSSClient(config)
        info = client.get_object_info("test.txt")

        assert info["key"] == "test.txt"
        assert info["size"] == 1024
        assert info["content_type"] == "text/plain"
        assert info["metadata"] == {"author": "test", "version": "1.0"}

    def test_copy(self, config, mock_oss2):
        """测试复制对象"""
        _, mock_bucket = mock_oss2

        mock_result = MagicMock()
        mock_result.etag = "abc123"
        mock_bucket.copy_object.return_value = mock_result

        client = OSSClient(config)
        result = client.copy("source.txt", "dest.txt")

        assert result["source_key"] == "source.txt"
        assert result["dest_key"] == "dest.txt"
        assert result["etag"] == "abc123"

        mock_bucket.copy_object.assert_called_once()

    def test_generate_presigned_url(self, config, mock_oss2):
        """测试生成预签名 URL"""
        _, mock_bucket = mock_oss2

        mock_url = "https://test-bucket.oss-cn-hangzhou.aliyuncs.com/test.txt?signature=xxx"
        mock_bucket.sign_url.return_value = mock_url

        client = OSSClient(config)
        url = client.generate_presigned_url("test.txt", expiration=300)

        assert url == mock_url
        mock_bucket.sign_url.assert_called_once_with("GET", "test.txt", 300)

    def test_clear(self, config, mock_oss2):
        """测试清空对象"""
        mock_oss2_mod, mock_bucket = mock_oss2

        # Mock ObjectIterator
        mock_obj1 = MagicMock()
        mock_obj1.key = "file1.txt"
        mock_obj2 = MagicMock()
        mock_obj2.key = "file2.txt"

        mock_oss2_mod.ObjectIterator.return_value = [mock_obj1, mock_obj2]

        # Mock batch_delete_objects
        mock_result = MagicMock()
        mock_result.deleted_keys = ["file1.txt", "file2.txt"]
        mock_bucket.batch_delete_objects.return_value = mock_result

        client = OSSClient(config)
        count = client.clear(prefix="test/")

        assert count == 2
        mock_bucket.batch_delete_objects.assert_called_once()

    def test_close(self, config, mock_oss2):
        """测试关闭客户端"""
        client = OSSClient(config)
        client.close()
        # OSS 客户端无需显式关闭，调用不应报错
