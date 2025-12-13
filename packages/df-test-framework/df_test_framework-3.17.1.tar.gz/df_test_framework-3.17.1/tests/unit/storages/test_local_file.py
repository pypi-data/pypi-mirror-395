"""LocalFileClient 单元测试"""

import os
import tempfile
from io import BytesIO

import pytest

from df_test_framework.capabilities.storages.file import LocalFileClient, LocalFileConfig
from df_test_framework.core.exceptions import ResourceError, ValidationError


class TestLocalFileConfig:
    """LocalFileConfig 配置类测试"""

    def test_default_config(self):
        """测试默认配置"""
        config = LocalFileConfig()
        assert config.base_path == "./test-data"
        assert config.auto_create_dirs is True
        assert config.allow_overwrite is True
        assert config.max_file_size == 100 * 1024 * 1024
        assert config.allowed_extensions is None

    def test_custom_config(self):
        """测试自定义配置"""
        config = LocalFileConfig(
            base_path="/tmp/test",
            auto_create_dirs=False,
            allow_overwrite=False,
            max_file_size=1024,
            allowed_extensions=[".txt", ".json"],
        )
        assert config.base_path == "/tmp/test"
        assert config.auto_create_dirs is False
        assert config.allow_overwrite is False
        assert config.max_file_size == 1024
        assert config.allowed_extensions == [".txt", ".json"]


class TestLocalFileClient:
    """LocalFileClient 客户端测试"""

    @pytest.fixture
    def temp_dir(self):
        """临时目录 fixture"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def client(self, temp_dir):
        """LocalFileClient fixture"""
        config = LocalFileConfig(base_path=temp_dir)
        return LocalFileClient(config)

    def test_init_creates_base_path(self, temp_dir):
        """测试初始化自动创建基础目录"""
        base_path = os.path.join(temp_dir, "new-folder")
        assert not os.path.exists(base_path)

        config = LocalFileConfig(base_path=base_path, auto_create_dirs=True)
        LocalFileClient(config)

        assert os.path.exists(base_path)

    def test_init_without_auto_create(self, temp_dir):
        """测试禁用自动创建目录"""
        base_path = os.path.join(temp_dir, "non-existent")
        config = LocalFileConfig(base_path=base_path, auto_create_dirs=False)

        with pytest.raises(ValidationError, match="不存在"):
            LocalFileClient(config)

    def test_upload_bytes(self, client):
        """测试上传字节内容"""
        content = b"Hello World"
        result = client.upload("test.txt", content)

        assert result["path"] == "test.txt"
        assert result["size"] == len(content)
        assert "created_at" in result

    def test_upload_file_object(self, client):
        """测试上传文件对象"""
        content = b"Test File Content"
        file_obj = BytesIO(content)

        result = client.upload("test.txt", file_obj)

        assert result["path"] == "test.txt"
        assert result["size"] == len(content)

    def test_upload_with_metadata(self, client):
        """测试上传带元数据"""
        metadata = {"author": "test", "version": "1.0"}
        result = client.upload("test.txt", b"content", metadata=metadata)

        assert result["metadata"] == metadata

    def test_upload_creates_subdirectories(self, client):
        """测试上传自动创建子目录"""
        result = client.upload("subdir/nested/file.txt", b"content")

        assert result["path"] == "subdir/nested/file.txt"
        assert client.exists("subdir/nested/file.txt")

    def test_upload_file_too_large(self, client):
        """测试上传超大文件"""
        client.config.max_file_size = 10
        content = b"x" * 20

        with pytest.raises(ValidationError, match=r"文件大小.*超过限制"):
            client.upload("large.txt", content)

    def test_upload_invalid_extension(self, client):
        """测试上传不允许的扩展名"""
        client.config.allowed_extensions = [".txt", ".json"]

        with pytest.raises(ValidationError, match=r"文件扩展名.*不在允许列表"):
            client.upload("test.exe", b"content")

    def test_upload_overwrite_not_allowed(self, client):
        """测试禁止覆盖已存在文件"""
        client.upload("test.txt", b"original")
        client.config.allow_overwrite = False

        with pytest.raises(ValidationError, match="已存在"):
            client.upload("test.txt", b"new content")

    def test_upload_path_traversal_attack(self, client):
        """测试路径遍历攻击防护"""
        with pytest.raises(ValidationError, match=r"不安全的文件路径"):
            client.upload("../../../etc/passwd", b"hack")

    def test_download(self, client):
        """测试下载文件"""
        content = b"Download Test"
        client.upload("download.txt", content)

        downloaded = client.download("download.txt")
        assert downloaded == content

    def test_download_not_found(self, client):
        """测试下载不存在的文件"""
        with pytest.raises(ResourceError, match="文件不存在"):
            client.download("nonexistent.txt")

    def test_delete(self, client):
        """测试删除文件"""
        client.upload("delete.txt", b"content")
        assert client.exists("delete.txt")

        result = client.delete("delete.txt")
        assert result is True
        assert not client.exists("delete.txt")

    def test_delete_not_found(self, client):
        """测试删除不存在的文件"""
        with pytest.raises(ResourceError, match="文件不存在"):
            client.delete("nonexistent.txt")

    def test_delete_missing_ok(self, client):
        """测试删除不存在的文件（允许缺失）"""
        result = client.delete("nonexistent.txt", missing_ok=True)
        assert result is False

    def test_exists(self, client):
        """测试检查文件是否存在"""
        assert not client.exists("test.txt")

        client.upload("test.txt", b"content")
        assert client.exists("test.txt")

        client.delete("test.txt")
        assert not client.exists("test.txt")

    def test_list_files_empty(self, client):
        """测试列出空目录"""
        files = client.list_files()
        assert files == []

    def test_list_files(self, client):
        """测试列出文件"""
        client.upload("file1.txt", b"1")
        client.upload("file2.txt", b"2")
        client.upload("subdir/file3.txt", b"3")

        # 非递归
        files = client.list_files()
        assert len(files) == 2
        assert "file1.txt" in files
        assert "file2.txt" in files

        # 递归
        files = client.list_files(recursive=True)
        assert len(files) == 3
        assert "subdir/file3.txt" in files

    def test_list_files_with_pattern(self, client):
        """测试模式匹配列出文件"""
        client.upload("test1.txt", b"1")
        client.upload("test2.json", b"2")
        client.upload("test3.txt", b"3")

        txt_files = client.list_files(pattern="*.txt")
        assert len(txt_files) == 2
        assert all(f.endswith(".txt") for f in txt_files)

    def test_list_files_in_subdirectory(self, client):
        """测试列出子目录文件"""
        client.upload("subdir/file1.txt", b"1")
        client.upload("subdir/file2.txt", b"2")

        files = client.list_files(directory="subdir")
        assert len(files) == 2

    def test_get_file_info(self, client):
        """测试获取文件信息"""
        content = b"File Info Test"
        client.upload("info.txt", content)

        info = client.get_file_info("info.txt")
        assert info["path"] == "info.txt"
        assert info["size"] == len(content)
        assert "metadata" in info  # metadata 字段存在
        assert info["metadata"] == {}  # 本地文件系统不支持持久化元数据
        assert "created_at" in info
        assert "modified_at" in info

    def test_get_file_info_not_found(self, client):
        """测试获取不存在文件的信息"""
        with pytest.raises(ResourceError, match="文件不存在"):
            client.get_file_info("nonexistent.txt")

    def test_copy(self, client):
        """测试复制文件"""
        content = b"Copy Test"
        client.upload("source.txt", content)

        result = client.copy("source.txt", "dest.txt")
        assert result["path"] == "dest.txt"
        assert result["size"] == len(content)

        # 验证两个文件都存在
        assert client.exists("source.txt")
        assert client.exists("dest.txt")
        assert client.download("dest.txt") == content

    def test_copy_not_found(self, client):
        """测试复制不存在的文件"""
        with pytest.raises(ResourceError, match="源文件不存在"):
            client.copy("nonexistent.txt", "dest.txt")

    def test_copy_no_overwrite(self, client):
        """测试复制到已存在文件（禁止覆盖）"""
        client.upload("source.txt", b"source")
        client.upload("dest.txt", b"dest")

        with pytest.raises(ValidationError, match="目标文件已存在"):
            client.copy("source.txt", "dest.txt", overwrite=False)

    def test_move(self, client):
        """测试移动文件"""
        content = b"Move Test"
        client.upload("source.txt", content)

        result = client.move("source.txt", "dest.txt")
        assert result["path"] == "dest.txt"

        # 验证源文件不存在，目标文件存在
        assert not client.exists("source.txt")
        assert client.exists("dest.txt")
        assert client.download("dest.txt") == content

    def test_move_not_found(self, client):
        """测试移动不存在的文件"""
        with pytest.raises(ResourceError, match="源文件不存在"):
            client.move("nonexistent.txt", "dest.txt")

    def test_clear_all(self, client):
        """测试清空所有文件"""
        client.upload("file1.txt", b"1")
        client.upload("file2.txt", b"2")
        client.upload("subdir/file3.txt", b"3")

        count = client.clear()
        assert count == 3
        assert client.list_files(recursive=True) == []

    def test_clear_directory(self, client):
        """测试清空指定目录"""
        client.upload("file1.txt", b"1")
        client.upload("subdir/file2.txt", b"2")
        client.upload("subdir/file3.txt", b"3")

        count = client.clear(directory="subdir")
        assert count == 2

        # 根目录文件仍存在
        assert client.exists("file1.txt")
        assert not client.exists("subdir/file2.txt")

    def test_close(self, client):
        """测试关闭客户端"""
        client.close()
        # LocalFileClient 无需清理，调用不应报错
