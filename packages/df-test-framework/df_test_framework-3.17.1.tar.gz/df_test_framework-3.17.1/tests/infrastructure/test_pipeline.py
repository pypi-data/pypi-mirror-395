"""
测试ConfigPipeline

验证配置管道的源管理和合并功能。
"""

from df_test_framework.infrastructure.config.pipeline import ConfigPipeline
from df_test_framework.infrastructure.config.sources import (
    DictSource,
)


class TestConfigPipelineCreation:
    """测试ConfigPipeline创建"""

    def test_create_empty_pipeline(self):
        """测试创建空管道"""
        pipeline = ConfigPipeline()

        assert pipeline.sources == []

    def test_create_pipeline_with_sources(self):
        """测试创建带源的管道"""
        source1 = DictSource({"a": 1})
        source2 = DictSource({"b": 2})

        pipeline = ConfigPipeline(sources=[source1, source2])

        assert len(pipeline.sources) == 2
        assert pipeline.sources[0] is source1
        assert pipeline.sources[1] is source2


class TestConfigPipelineAdd:
    """测试ConfigPipeline.add方法"""

    def test_add_single_source(self):
        """测试添加单个源"""
        pipeline = ConfigPipeline()
        source = DictSource({"key": "value"})

        result = pipeline.add(source)

        assert len(pipeline.sources) == 1
        assert pipeline.sources[0] is source
        # 验证链式调用
        assert result is pipeline

    def test_add_multiple_sources(self):
        """测试链式添加多个源"""
        pipeline = ConfigPipeline()
        source1 = DictSource({"a": 1})
        source2 = DictSource({"b": 2})
        source3 = DictSource({"c": 3})

        pipeline.add(source1).add(source2).add(source3)

        assert len(pipeline.sources) == 3
        assert pipeline.sources[0] is source1
        assert pipeline.sources[1] is source2
        assert pipeline.sources[2] is source3


class TestConfigPipelineExtend:
    """测试ConfigPipeline.extend方法"""

    def test_extend_with_list(self):
        """测试extend添加源列表"""
        pipeline = ConfigPipeline()
        source1 = DictSource({"a": 1})
        source2 = DictSource({"b": 2})

        result = pipeline.extend([source1, source2])

        assert len(pipeline.sources) == 2
        # 验证链式调用
        assert result is pipeline

    def test_extend_to_existing_sources(self):
        """测试extend到已有源"""
        source1 = DictSource({"a": 1})
        pipeline = ConfigPipeline(sources=[source1])

        source2 = DictSource({"b": 2})
        source3 = DictSource({"c": 3})

        pipeline.extend([source2, source3])

        assert len(pipeline.sources) == 3
        assert pipeline.sources[0] is source1
        assert pipeline.sources[1] is source2
        assert pipeline.sources[2] is source3


class TestConfigPipelinePrepend:
    """测试ConfigPipeline.prepend方法"""

    def test_prepend_to_empty_pipeline(self):
        """测试prepend到空管道"""
        pipeline = ConfigPipeline()
        source1 = DictSource({"a": 1})
        source2 = DictSource({"b": 2})

        result = pipeline.prepend(source1, source2)

        assert len(pipeline.sources) == 2
        assert pipeline.sources[0] is source1
        assert pipeline.sources[1] is source2
        # 验证链式调用
        assert result is pipeline

    def test_prepend_to_existing_sources(self):
        """测试prepend到已有源（前置）"""
        source3 = DictSource({"c": 3})
        pipeline = ConfigPipeline(sources=[source3])

        source1 = DictSource({"a": 1})
        source2 = DictSource({"b": 2})

        pipeline.prepend(source1, source2)

        # prepend应该把新源放在前面
        assert len(pipeline.sources) == 3
        assert pipeline.sources[0] is source1
        assert pipeline.sources[1] is source2
        assert pipeline.sources[2] is source3


class TestConfigPipelineLoad:
    """测试ConfigPipeline.load方法"""

    def test_load_empty_pipeline(self):
        """测试空管道加载"""
        pipeline = ConfigPipeline()

        result = pipeline.load()

        assert result == {}

    def test_load_single_source(self):
        """测试单个源加载"""
        pipeline = ConfigPipeline()
        pipeline.add(DictSource({"app_name": "TestApp", "app_env": "test"}))

        result = pipeline.load()

        assert result == {"app_name": "TestApp", "app_env": "test"}

    def test_load_multiple_sources_merge(self):
        """测试多个源合并（后面覆盖前面）"""
        pipeline = ConfigPipeline()

        # 源1
        pipeline.add(
            DictSource(
                {
                    "app_name": "FirstApp",
                    "app_port": 8000,
                }
            )
        )

        # 源2（覆盖app_name，新增app_env）
        pipeline.add(
            DictSource(
                {
                    "app_name": "SecondApp",
                    "app_env": "test",
                }
            )
        )

        result = pipeline.load()

        assert result["app_name"] == "SecondApp"  # 被覆盖
        assert result["app_port"] == 8000  # 保留
        assert result["app_env"] == "test"  # 新增

    def test_load_deep_merge(self):
        """测试深度合并"""
        pipeline = ConfigPipeline()

        # 源1
        pipeline.add(
            DictSource(
                {
                    "app": {
                        "name": "FirstApp",
                        "database": {
                            "host": "localhost",
                            "port": 5432,
                        },
                    }
                }
            )
        )

        # 源2（深度覆盖）
        pipeline.add(
            DictSource(
                {
                    "app": {
                        "name": "SecondApp",  # 覆盖
                        "database": {
                            "port": 3306,  # 覆盖
                            "user": "admin",  # 新增
                        },
                    }
                }
            )
        )

        result = pipeline.load()

        assert result["app"]["name"] == "SecondApp"
        assert result["app"]["database"]["host"] == "localhost"  # 保留
        assert result["app"]["database"]["port"] == 3306  # 被覆盖
        assert result["app"]["database"]["user"] == "admin"  # 新增

    def test_load_respects_source_order(self):
        """测试加载尊重源的顺序"""
        pipeline = ConfigPipeline()

        pipeline.add(DictSource({"priority": "source1"}))
        pipeline.add(DictSource({"priority": "source2"}))
        pipeline.add(DictSource({"priority": "source3"}))

        result = pipeline.load()

        # 最后的源应该生效
        assert result["priority"] == "source3"


class TestConfigPipelineLoadInto:
    """测试ConfigPipeline.load_into方法"""

    def test_load_into_empty_target(self):
        """测试load_into到空目标"""
        pipeline = ConfigPipeline()
        pipeline.add(DictSource({"app_name": "TestApp"}))

        result = pipeline.load_into({})

        assert result == {"app_name": "TestApp"}

    def test_load_into_existing_target(self):
        """测试load_into到已有目标"""
        pipeline = ConfigPipeline()
        pipeline.add(DictSource({"app_name": "PipelineApp"}))

        target = {"app_name": "TargetApp", "app_port": 8000}

        result = pipeline.load_into(target)

        # 管道的源应该覆盖target
        assert result["app_name"] == "PipelineApp"
        assert result["app_port"] == 8000

    def test_load_into_does_not_mutate_target(self):
        """测试load_into不修改原target"""
        pipeline = ConfigPipeline()
        pipeline.add(DictSource({"app_name": "PipelineApp"}))

        target = {"app_name": "TargetApp"}

        pipeline.load_into(target)

        # 原target不应被修改
        assert target == {"app_name": "TargetApp"}

    def test_load_into_deep_merge_with_target(self):
        """测试load_into深度合并"""
        pipeline = ConfigPipeline()
        pipeline.add(
            DictSource(
                {
                    "app": {
                        "database": {
                            "port": 3306,  # 覆盖
                        }
                    }
                }
            )
        )

        target = {
            "app": {
                "database": {
                    "host": "localhost",
                    "port": 5432,
                }
            }
        }

        result = pipeline.load_into(target)

        assert result["app"]["database"]["host"] == "localhost"  # 保留
        assert result["app"]["database"]["port"] == 3306  # 被覆盖


class TestConfigPipelineIntegration:
    """集成测试：完整的管道流程"""

    def test_complete_pipeline_flow(self):
        """测试完整的管道流程"""
        # 1. 创建管道
        pipeline = ConfigPipeline()

        # 2. 添加默认配置
        pipeline.add(
            DictSource(
                {
                    "app": {
                        "name": "DefaultApp",
                        "port": 8000,
                        "env": "development",
                    }
                }
            )
        )

        # 3. 添加环境配置（覆盖部分值）
        pipeline.add(
            DictSource(
                {
                    "app": {
                        "env": "production",
                        "debug": False,
                    }
                }
            )
        )

        # 4. 添加用户配置（最高优先级）
        pipeline.add(
            DictSource(
                {
                    "app": {
                        "port": 9000,
                    }
                }
            )
        )

        # 5. 加载配置
        result = pipeline.load()

        # 验证最终配置
        assert result["app"]["name"] == "DefaultApp"  # 默认值保留
        assert result["app"]["port"] == 9000  # 用户配置覆盖
        assert result["app"]["env"] == "production"  # 环境配置覆盖
        assert result["app"]["debug"] is False  # 环境配置新增

    def test_pipeline_with_multiple_operations(self):
        """测试管道的多种操作组合"""
        # 创建基础管道
        pipeline = ConfigPipeline()

        # 添加源
        pipeline.add(DictSource({"base": "value"}))

        # 扩展源
        pipeline.extend(
            [
                DictSource({"ext1": "value1"}),
                DictSource({"ext2": "value2"}),
            ]
        )

        # 前置源（最低优先级）
        pipeline.prepend(DictSource({"prepend": "value", "base": "old"}))

        result = pipeline.load()

        # 验证顺序：prepend -> add -> extend
        assert result["base"] == "value"  # add覆盖prepend
        assert result["prepend"] == "value"
        assert result["ext1"] == "value1"
        assert result["ext2"] == "value2"

    def test_pipeline_reusability(self):
        """测试管道可重复加载"""
        pipeline = ConfigPipeline()
        pipeline.add(DictSource({"count": 1}))

        # 第一次加载
        result1 = pipeline.load()

        # 第二次加载
        result2 = pipeline.load()

        # 两次结果应该相同
        assert result1 == result2
        assert result1 is not result2  # 但是不同的对象
