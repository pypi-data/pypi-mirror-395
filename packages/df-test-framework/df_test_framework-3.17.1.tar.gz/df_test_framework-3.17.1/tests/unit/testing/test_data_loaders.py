"""数据加载器单元测试

测试JSON/CSV/YAML数据加载功能

v3.10.0 - P2.2 测试数据工具增强
"""

import json

import pytest

from df_test_framework.testing.data.loaders import CSVLoader, JSONLoader, YAMLLoader


class TestJSONLoader:
    """JSONLoader测试"""

    def test_load_json_array(self, tmp_path):
        """测试加载JSON数组"""
        data = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]
        file_path = tmp_path / "users.json"
        file_path.write_text(json.dumps(data), encoding="utf-8")

        result = JSONLoader.load(file_path)

        assert len(result) == 2
        assert result[0]["name"] == "Alice"
        assert result[1]["age"] == 30

    def test_load_json_object(self, tmp_path):
        """测试加载JSON对象"""
        data = {"database": {"host": "localhost", "port": 3306}}
        file_path = tmp_path / "config.json"
        file_path.write_text(json.dumps(data), encoding="utf-8")

        result = JSONLoader.load(file_path)

        assert result["database"]["host"] == "localhost"
        assert result["database"]["port"] == 3306

    def test_loads_from_string(self):
        """测试从字符串解析"""
        json_str = '{"name": "Alice", "age": 25}'

        result = JSONLoader.loads(json_str)

        assert result["name"] == "Alice"
        assert result["age"] == 25

    def test_load_one(self, tmp_path):
        """测试加载单条数据"""
        data = [{"id": 1}, {"id": 2}, {"id": 3}]
        file_path = tmp_path / "items.json"
        file_path.write_text(json.dumps(data), encoding="utf-8")

        first = JSONLoader.load_one(file_path, index=0)
        second = JSONLoader.load_one(file_path, index=1)

        assert first["id"] == 1
        assert second["id"] == 2

    def test_load_one_out_of_range(self, tmp_path):
        """测试索引超出范围"""
        data = [{"id": 1}]
        file_path = tmp_path / "items.json"
        file_path.write_text(json.dumps(data), encoding="utf-8")

        with pytest.raises(IndexError):
            JSONLoader.load_one(file_path, index=10)

    def test_load_lines(self, tmp_path):
        """测试加载JSON Lines"""
        content = '{"level": "INFO", "msg": "start"}\n{"level": "ERROR", "msg": "fail"}\n'
        file_path = tmp_path / "logs.jsonl"
        file_path.write_text(content, encoding="utf-8")

        result = JSONLoader.load_lines(file_path)

        assert len(result) == 2
        assert result[0]["level"] == "INFO"
        assert result[1]["level"] == "ERROR"

    def test_load_file_not_found(self):
        """测试文件不存在"""
        with pytest.raises(FileNotFoundError):
            JSONLoader.load("/nonexistent/path.json")

    def test_load_invalid_json(self, tmp_path):
        """测试无效JSON"""
        file_path = tmp_path / "invalid.json"
        file_path.write_text("not valid json", encoding="utf-8")

        with pytest.raises(json.JSONDecodeError):
            JSONLoader.load(file_path)

    def test_save_json(self, tmp_path):
        """测试保存JSON"""
        data = {"name": "测试", "value": 123}
        file_path = tmp_path / "output.json"

        JSONLoader.save(data, file_path)

        # 验证保存结果
        loaded = JSONLoader.load(file_path)
        assert loaded["name"] == "测试"
        assert loaded["value"] == 123

    def test_load_all(self, tmp_path):
        """测试load_all确保返回列表"""
        # 测试对象
        obj_file = tmp_path / "obj.json"
        obj_file.write_text('{"key": "value"}', encoding="utf-8")

        result = JSONLoader.load_all(obj_file)
        assert isinstance(result, list)
        assert len(result) == 1


class TestCSVLoader:
    """CSVLoader测试"""

    def test_load_csv_with_header(self, tmp_path):
        """测试加载带表头CSV"""
        content = "name,age,email\nAlice,25,alice@test.com\nBob,30,bob@test.com"
        file_path = tmp_path / "users.csv"
        file_path.write_text(content, encoding="utf-8")

        result = CSVLoader.load(file_path)

        assert len(result) == 2
        assert result[0]["name"] == "Alice"
        assert result[0]["age"] == "25"  # CSV默认都是字符串
        assert result[1]["email"] == "bob@test.com"

    def test_load_csv_with_type_hints(self, tmp_path):
        """测试类型转换"""
        content = "name,age,score,active\nAlice,25,95.5,true\nBob,30,88.0,false"
        file_path = tmp_path / "users.csv"
        file_path.write_text(content, encoding="utf-8")

        result = CSVLoader.load(file_path, type_hints={"age": int, "score": float, "active": bool})

        assert result[0]["age"] == 25
        assert result[0]["score"] == 95.5
        assert result[0]["active"] is True
        assert result[1]["active"] is False

    def test_load_tsv(self, tmp_path):
        """测试加载TSV（制表符分隔）"""
        content = "name\tage\nAlice\t25\nBob\t30"
        file_path = tmp_path / "users.tsv"
        file_path.write_text(content, encoding="utf-8")

        result = CSVLoader.load(file_path, delimiter="\t")

        assert len(result) == 2
        assert result[0]["name"] == "Alice"

    def test_loads_from_string(self):
        """测试从字符串解析"""
        csv_str = "name,age\nAlice,25\nBob,30"

        result = CSVLoader.loads(csv_str)

        assert len(result) == 2
        assert result[0]["name"] == "Alice"

    def test_load_as_tuples(self, tmp_path):
        """测试加载为元组（用于pytest参数化）"""
        content = "input,expected\n1,2\n2,4\n3,6"
        file_path = tmp_path / "test_data.csv"
        file_path.write_text(content, encoding="utf-8")

        result = CSVLoader.load_as_tuples(file_path)

        assert len(result) == 3
        assert result[0] == ("1", "2")
        assert result[1] == ("2", "4")

    def test_save_csv(self, tmp_path):
        """测试保存CSV"""
        data = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]
        file_path = tmp_path / "output.csv"

        CSVLoader.save(data, file_path)

        # 验证保存结果
        loaded = CSVLoader.load(file_path)
        assert len(loaded) == 2
        assert loaded[0]["name"] == "Alice"

    def test_load_with_skip_rows(self, tmp_path):
        """测试跳过行"""
        content = "name,age\n# 注释行\nAlice,25\nBob,30"
        file_path = tmp_path / "users.csv"
        file_path.write_text(content, encoding="utf-8")

        result = CSVLoader.load(file_path, skip_rows=1)

        assert len(result) == 2  # 跳过注释行后只有2行数据


class TestYAMLLoader:
    """YAMLLoader测试"""

    def test_load_yaml(self, tmp_path):
        """测试加载YAML"""
        content = """
database:
  host: localhost
  port: 3306
redis:
  host: localhost
  port: 6379
"""
        file_path = tmp_path / "config.yaml"
        file_path.write_text(content, encoding="utf-8")

        result = YAMLLoader.load(file_path)

        assert result["database"]["host"] == "localhost"
        assert result["database"]["port"] == 3306
        assert result["redis"]["port"] == 6379

    def test_loads_from_string(self):
        """测试从字符串解析"""
        yaml_str = "name: Alice\nage: 25"

        result = YAMLLoader.loads(yaml_str)

        assert result["name"] == "Alice"
        assert result["age"] == 25

    def test_load_multi_document(self, tmp_path):
        """测试加载多文档YAML"""
        content = """
---
name: doc1
value: 1
---
name: doc2
value: 2
"""
        file_path = tmp_path / "multi.yaml"
        file_path.write_text(content, encoding="utf-8")

        result = YAMLLoader.load_all(file_path)

        assert len(result) == 2
        assert result[0]["name"] == "doc1"
        assert result[1]["name"] == "doc2"

    def test_expand_env_vars(self, tmp_path, monkeypatch):
        """测试环境变量替换"""
        monkeypatch.setenv("TEST_HOST", "prod.example.com")

        content = """
database:
  host: ${TEST_HOST}
  port: ${TEST_PORT:3306}
  name: ${UNDEFINED_VAR}
"""
        file_path = tmp_path / "config.yaml"
        file_path.write_text(content, encoding="utf-8")

        result = YAMLLoader.load(file_path, expand_env=True)

        assert result["database"]["host"] == "prod.example.com"  # 环境变量
        assert result["database"]["port"] == 3306  # 默认值（YAML会解析为int）
        assert result["database"]["name"] == "${UNDEFINED_VAR}"  # 未定义保留原样

    def test_save_yaml(self, tmp_path):
        """测试保存YAML"""
        data = {"name": "测试", "items": [1, 2, 3]}
        file_path = tmp_path / "output.yaml"

        YAMLLoader.save(data, file_path)

        # 验证保存结果
        loaded = YAMLLoader.load(file_path)
        assert loaded["name"] == "测试"
        assert loaded["items"] == [1, 2, 3]

    def test_merge_yaml_files(self, tmp_path):
        """测试合并多个YAML文件"""
        # 基础配置
        base_content = """
database:
  host: localhost
  port: 3306
logging:
  level: INFO
"""
        base_file = tmp_path / "base.yaml"
        base_file.write_text(base_content, encoding="utf-8")

        # 覆盖配置
        override_content = """
database:
  host: prod.example.com
  password: secret
"""
        override_file = tmp_path / "override.yaml"
        override_file.write_text(override_content, encoding="utf-8")

        result = YAMLLoader.merge(base_file, override_file)

        assert result["database"]["host"] == "prod.example.com"  # 被覆盖
        assert result["database"]["port"] == 3306  # 保留
        assert result["database"]["password"] == "secret"  # 新增
        assert result["logging"]["level"] == "INFO"  # 保留


class TestDataLoaderBase:
    """DataLoader基类测试"""

    def test_exists(self, tmp_path):
        """测试文件存在检查"""
        file_path = tmp_path / "exists.json"
        file_path.write_text("{}", encoding="utf-8")

        assert JSONLoader.exists(file_path) is True
        assert JSONLoader.exists(tmp_path / "nonexistent.json") is False
