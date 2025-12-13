"""S3Client 单元测试"""

from io import BytesIO
from unittest.mock import MagicMock, patch

import pytest

from df_test_framework.capabilities.storages.object import S3Client, S3Config
from df_test_framework.core.exceptions import ConfigurationError, ResourceError


class TestS3Config:
    """S3Config 配置类测试"""

    def test_default_config(self):
        """测试默认配置"""
        config = S3Config(
            access_key="test_key", secret_key="test_secret", bucket_name="test-bucket"
        )
        assert config.endpoint_url is None
        assert config.region is None
        assert config.use_ssl is True
        assert config.verify_ssl is True
        assert config.max_pool_connections == 10
        assert config.connect_timeout == 60
        assert config.multipart_threshold == 8 * 1024 * 1024

    def test_custom_config(self):
        """测试自定义配置"""
        config = S3Config(
            endpoint_url="http://localhost:9000",
            access_key="minioadmin",
            secret_key="minioadmin",
            bucket_name="my-bucket",
            region="us-west-2",
            use_ssl=False,
            verify_ssl=False,
            max_pool_connections=20,
        )
        assert config.endpoint_url == "http://localhost:9000"
        assert config.region == "us-west-2"
        assert config.use_ssl is False
        assert config.max_pool_connections == 20

    def test_required_fields_validation(self):
        """测试必需字段验证"""
        with pytest.raises(ValueError, match="field cannot be empty"):
            S3Config(access_key="", secret_key="secret", bucket_name="bucket")

        with pytest.raises(ValueError, match="field cannot be empty"):
            S3Config(access_key="key", secret_key="", bucket_name="bucket")

        with pytest.raises(ValueError, match="field cannot be empty"):
            S3Config(access_key="key", secret_key="secret", bucket_name="")

    def test_positive_int_validation(self):
        """测试正整数验证"""
        with pytest.raises(ValueError, match="value must be positive"):
            S3Config(
                access_key="key",
                secret_key="secret",
                bucket_name="bucket",
                max_pool_connections=0,
            )

        with pytest.raises(ValueError, match="value must be positive"):
            S3Config(
                access_key="key",
                secret_key="secret",
                bucket_name="bucket",
                max_concurrency=-1,
            )


class TestS3Client:
    """S3Client 客户端测试"""

    @pytest.fixture
    def config(self):
        """S3Config fixture"""
        return S3Config(
            endpoint_url="http://localhost:9000",
            access_key="minioadmin",
            secret_key="minioadmin",
            bucket_name="test-bucket",
        )

    @pytest.fixture
    def mock_boto3(self):
        """Mock boto3 module"""

        # 创建 Mock ClientError 类
        class MockClientError(Exception):
            def __init__(self, error_response):
                self.response = error_response
                super().__init__(str(error_response))

        with patch("df_test_framework.capabilities.storages.object.s3.client.boto3") as mock_boto:
            with patch(
                "df_test_framework.capabilities.storages.object.s3.client.Config"
            ) as mock_config:
                with patch(
                    "df_test_framework.capabilities.storages.object.s3.client.ClientError",
                    MockClientError,
                ):
                    with patch(
                        "df_test_framework.capabilities.storages.object.s3.client.BOTO3_AVAILABLE",
                        True,
                    ):
                        mock_client = MagicMock()
                        mock_boto.client.return_value = mock_client
                        mock_config.return_value = MagicMock()  # Mock Config instance
                        yield mock_boto, mock_client, MockClientError

    def test_init_without_boto3(self, config):
        """测试未安装 boto3 时初始化"""
        with patch(
            "df_test_framework.capabilities.storages.object.s3.client.BOTO3_AVAILABLE", False
        ):
            with pytest.raises(ConfigurationError, match="boto3 未安装"):
                S3Client(config)

    def test_init_with_boto3(self, config, mock_boto3):
        """测试正常初始化"""
        mock_boto, mock_client, _ = mock_boto3

        # Mock head_bucket (bucket exists)
        mock_client.head_bucket.return_value = {}

        _ = S3Client(config)  # 验证初始化成功

        # 验证 boto3.client 被调用
        mock_boto.client.assert_called_once()
        call_kwargs = mock_boto.client.call_args[1]
        assert call_kwargs["service_name"] == "s3"
        assert call_kwargs["aws_access_key_id"] == "minioadmin"
        assert call_kwargs["endpoint_url"] == "http://localhost:9000"

    def test_init_creates_bucket(self, config, mock_boto3):
        """测试初始化自动创建 bucket"""
        _, mock_client, mock_client_error = mock_boto3  # noqa: N806

        # Mock head_bucket 返回 404 (bucket not exists)
        error_response = {"Error": {"Code": "404"}}
        mock_client.head_bucket.side_effect = mock_client_error(error_response)

        _ = S3Client(config)  # 验证初始化成功

        # 验证 create_bucket 被调用
        mock_client.create_bucket.assert_called_once_with(Bucket="test-bucket")

    def test_upload_bytes(self, config, mock_boto3):
        """测试上传字节内容"""
        _, mock_client, _ = mock_boto3
        mock_client.head_bucket.return_value = {}

        client = S3Client(config)
        content = b"Hello S3"

        result = client.upload("test.txt", content)

        assert result["key"] == "test.txt"
        assert result["bucket"] == "test-bucket"
        assert result["size"] == len(content)

        # 验证 upload_fileobj 被调用
        mock_client.upload_fileobj.assert_called_once()

    def test_upload_with_metadata(self, config, mock_boto3):
        """测试上传带元数据"""
        _, mock_client, mock_client_error = mock_boto3  # noqa: N806
        mock_client.head_bucket.return_value = {}

        client = S3Client(config)
        metadata = {"author": "test"}

        client.upload("test.txt", b"content", metadata=metadata, content_type="text/plain")

        # 验证 ExtraArgs
        call_args = mock_client.upload_fileobj.call_args
        extra_args = call_args[1]["ExtraArgs"]
        assert extra_args["Metadata"] == metadata
        assert extra_args["ContentType"] == "text/plain"

    def test_download(self, config, mock_boto3):
        """测试下载文件"""
        _, mock_client, mock_client_error = mock_boto3  # noqa: N806
        mock_client.head_bucket.return_value = {}

        content = b"Downloaded Content"
        mock_response = {"Body": BytesIO(content)}
        mock_client.get_object.return_value = mock_response

        client = S3Client(config)
        downloaded = client.download("test.txt")

        assert downloaded == content
        mock_client.get_object.assert_called_once_with(Bucket="test-bucket", Key="test.txt")

    def test_download_not_found(self, config, mock_boto3):
        """测试下载不存在的文件"""
        _, mock_client, mock_client_error = mock_boto3  # noqa: N806
        mock_client.head_bucket.return_value = {}

        error_response = {"Error": {"Code": "NoSuchKey"}}
        mock_client.get_object.side_effect = mock_client_error(error_response)

        client = S3Client(config)

        with pytest.raises(ResourceError, match="文件不存在"):
            client.download("nonexistent.txt")

    def test_delete(self, config, mock_boto3):
        """测试删除文件"""
        _, mock_client, mock_client_error = mock_boto3  # noqa: N806
        mock_client.head_bucket.return_value = {}

        # Mock exists (file exists)
        mock_client.head_object.return_value = {}

        client = S3Client(config)
        result = client.delete("test.txt")

        assert result is True
        mock_client.delete_object.assert_called_once_with(Bucket="test-bucket", Key="test.txt")

    def test_delete_not_found(self, config, mock_boto3):
        """测试删除不存在的文件"""
        _, mock_client, mock_client_error = mock_boto3  # noqa: N806
        mock_client.head_bucket.return_value = {}

        # Mock exists (file not exists)
        error_response = {"Error": {"Code": "404"}}
        mock_client.head_object.side_effect = mock_client_error(error_response)

        client = S3Client(config)

        with pytest.raises(ResourceError, match="文件不存在"):
            client.delete("nonexistent.txt")

    def test_delete_missing_ok(self, config, mock_boto3):
        """测试删除不存在的文件（允许缺失）"""
        _, mock_client, mock_client_error = mock_boto3  # noqa: N806
        mock_client.head_bucket.return_value = {}

        # Mock exists (file not exists)
        error_response = {"Error": {"Code": "404"}}
        mock_client.head_object.side_effect = mock_client_error(error_response)

        client = S3Client(config)
        result = client.delete("nonexistent.txt", missing_ok=True)

        assert result is False

    def test_exists(self, config, mock_boto3):
        """测试检查文件是否存在"""
        _, mock_client, mock_client_error = mock_boto3  # noqa: N806
        mock_client.head_bucket.return_value = {}

        client = S3Client(config)

        # File exists
        mock_client.head_object.return_value = {}
        assert client.exists("test.txt") is True

        # File not exists
        error_response = {"Error": {"Code": "NoSuchKey"}}
        mock_client.head_object.side_effect = mock_client_error(error_response)
        assert client.exists("test.txt") is False

    def test_list_objects(self, config, mock_boto3):
        """测试列出对象"""
        _, mock_client, mock_client_error = mock_boto3  # noqa: N806
        mock_client.head_bucket.return_value = {}

        mock_response = {
            "Contents": [
                {"Key": "file1.txt", "Size": 100, "LastModified": "2024-01-01", "ETag": "etag1"},
                {"Key": "file2.txt", "Size": 200, "LastModified": "2024-01-02", "ETag": "etag2"},
            ]
        }
        mock_client.list_objects_v2.return_value = mock_response

        client = S3Client(config)
        objects = client.list_objects(prefix="test/")

        assert len(objects) == 2
        assert objects[0]["key"] == "file1.txt"
        assert objects[0]["size"] == 100
        assert objects[1]["key"] == "file2.txt"

        mock_client.list_objects_v2.assert_called_once()
        call_kwargs = mock_client.list_objects_v2.call_args[1]
        assert call_kwargs["Prefix"] == "test/"

    def test_get_object_info(self, config, mock_boto3):
        """测试获取对象信息"""
        _, mock_client, mock_client_error = mock_boto3  # noqa: N806
        mock_client.head_bucket.return_value = {}

        mock_response = {
            "ContentLength": 1024,
            "ContentType": "text/plain",
            "LastModified": "2024-01-01",
            "ETag": "abc123",
            "Metadata": {"author": "test"},
        }
        mock_client.head_object.return_value = mock_response

        client = S3Client(config)
        info = client.get_object_info("test.txt")

        assert info["key"] == "test.txt"
        assert info["size"] == 1024
        assert info["content_type"] == "text/plain"
        assert info["metadata"] == {"author": "test"}

    def test_copy(self, config, mock_boto3):
        """测试复制对象"""
        _, mock_client, mock_client_error = mock_boto3  # noqa: N806
        mock_client.head_bucket.return_value = {}

        # Mock get_object_info
        mock_client.head_object.return_value = {
            "ContentLength": 100,
            "ContentType": "text/plain",
            "LastModified": "2024-01-01",
            "ETag": "abc",
            "Metadata": {},
        }

        client = S3Client(config)
        result = client.copy("source.txt", "dest.txt")

        assert result["key"] == "dest.txt"
        mock_client.copy_object.assert_called_once()

    def test_generate_presigned_url(self, config, mock_boto3):
        """测试生成预签名 URL"""
        _, mock_client, mock_client_error = mock_boto3  # noqa: N806
        mock_client.head_bucket.return_value = {}

        mock_url = "https://test-bucket.s3.amazonaws.com/test.txt?signature=xxx"
        mock_client.generate_presigned_url.return_value = mock_url

        client = S3Client(config)
        url = client.generate_presigned_url("test.txt", expiration=300)

        assert url == mock_url
        mock_client.generate_presigned_url.assert_called_once()
        call_kwargs = mock_client.generate_presigned_url.call_args[1]
        assert call_kwargs["ExpiresIn"] == 300

    def test_clear(self, config, mock_boto3):
        """测试清空对象"""
        _, mock_client, mock_client_error = mock_boto3  # noqa: N806
        mock_client.head_bucket.return_value = {}

        # Mock list_objects
        mock_list_response = {
            "Contents": [
                {"Key": "file1.txt", "Size": 100, "LastModified": "2024-01-01", "ETag": "e1"},
                {"Key": "file2.txt", "Size": 200, "LastModified": "2024-01-02", "ETag": "e2"},
            ]
        }
        mock_client.list_objects_v2.return_value = mock_list_response

        # Mock delete_objects
        mock_delete_response = {"Deleted": [{"Key": "file1.txt"}, {"Key": "file2.txt"}]}
        mock_client.delete_objects.return_value = mock_delete_response

        client = S3Client(config)
        count = client.clear(prefix="test/")

        assert count == 2
        mock_client.delete_objects.assert_called_once()

    def test_close(self, config, mock_boto3):
        """测试关闭客户端"""
        _, mock_client, mock_client_error = mock_boto3  # noqa: N806
        mock_client.head_bucket.return_value = {}

        client = S3Client(config)
        client.close()
        # boto3 客户端无需显式关闭，调用不应报错
