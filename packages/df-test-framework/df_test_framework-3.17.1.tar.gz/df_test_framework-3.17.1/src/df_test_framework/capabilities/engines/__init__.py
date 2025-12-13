"""计算引擎能力层 - Layer 1

提供批处理和流处理计算引擎能力
按计算模式组织：
- batch/: 批处理引擎（Spark、MapReduce等）
- stream/: 流处理引擎（Flink、Storm等）
- olap/: OLAP分析引擎（ClickHouse、Druid等）

注意：此engines/目录是计算引擎，不同于之前的databases/（原engines/）
"""

# 预留：未来实现计算引擎客户端

__all__ = []
