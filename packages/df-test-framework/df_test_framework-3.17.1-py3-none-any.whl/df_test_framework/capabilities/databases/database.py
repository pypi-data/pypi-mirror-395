"""数据库操作封装

v1.2.0 新增:
- 批量操作支持
- 表名白名单验证
- 增强的错误处理

v3.0.0 新增:
- 集成DBDebugger调试支持（可选）

v3.5.0 新增:
- 集成ObservabilityLogger实时日志（默认）
- 集成AllureObserver自动附件（默认）

v3.6.1 修复:
- Database.execute() 迁移到 ObservabilityLogger（统一日志输出）

v3.14.0 新增:
- 集成 EventBus 发布数据库查询事件
- 支持 event_bus 参数
"""

from __future__ import annotations

import time
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any

from loguru import logger
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool
from sqlalchemy.sql import Executable

from df_test_framework.core.events import (
    DatabaseQueryEndEvent,
    DatabaseQueryErrorEvent,
    DatabaseQueryStartEvent,
)

if TYPE_CHECKING:
    from df_test_framework.infrastructure.events import EventBus

# ========== 表名白名单 (安全措施) ==========
# 生产环境应该明确定义允许操作的表
# 防止SQL注入和误操作

# 默认不限制表名 (开发/测试环境)
# None表示允许所有表,空集表示禁止所有表,有值则只允许白名单内的表
DEFAULT_ALLOWED_TABLES: set[str] | None = None


class Database:
    """
    数据库操作封装

    功能:
    - 提供数据库连接管理
    - 支持会话上下文管理
    - 提供常用的查询和执行方法
    """

    def __init__(
        self,
        connection_string: str,
        pool_size: int = 10,
        max_overflow: int = 20,
        pool_timeout: int = 30,
        pool_recycle: int = 3600,
        pool_pre_ping: bool = True,
        echo: bool = False,
        allowed_tables: set[str] | None = None,
        event_bus: EventBus | None = None,
    ):
        """
        初始化数据库连接

        Args:
            connection_string: 数据库连接字符串
                示例: mysql+pymysql://user:password@host:port/database?charset=utf8mb4
            pool_size: 连接池大小 (默认10)
            max_overflow: 连接池最大溢出数 (默认20)
            pool_timeout: 连接池超时时间(秒) (默认30)
            pool_recycle: 连接回收时间(秒) (默认3600,防止连接过期)
            pool_pre_ping: 是否检测连接有效性 (默认True)
            echo: 是否打印SQL语句 (默认False)
            allowed_tables: 允许操作的表名白名单 (None表示允许所有表)
            event_bus: 🆕 v3.14.0 事件总线（可选，用于发布数据库查询事件）

        Example:
            # 开发/测试环境: 不限制表名 (默认)
            db = Database(connection_string)
            # 等同于: allowed_tables=None

            # 生产环境: 限制表名白名单
            db = Database(
                connection_string,
                allowed_tables={"users", "orders", "products"}
            )

            # 特殊场景: 禁止所有表操作
            db = Database(
                connection_string,
                allowed_tables=set()  # 空集禁止所有表
            )
        """
        self.connection_string = connection_string
        self._event_bus = event_bus
        # 注意: 使用 is not None 判断,因为空集set()也是合法值(表示禁止所有表)
        self.allowed_tables = (
            allowed_tables if allowed_tables is not None else DEFAULT_ALLOWED_TABLES
        )

        # 创建数据库引擎
        self.engine: Engine = create_engine(
            connection_string,
            poolclass=QueuePool,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_timeout=pool_timeout,
            pool_recycle=pool_recycle,  # ✅ 添加连接回收
            pool_pre_ping=pool_pre_ping,  # 检测连接是否有效
            echo=echo,
        )

        # 创建会话工厂
        self.session_factory = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

        # v3.5: ObservabilityLogger
        from df_test_framework.infrastructure.logging.observability import db_logger

        self.obs_logger = db_logger()
        self._query_counter = 0  # 查询计数器（用于生成query_id）

        # 初始化日志（兼容旧logger）
        logger.info(f"数据库连接已建立: {self._mask_connection_string()}")
        if self.allowed_tables is not None:
            if self.allowed_tables:
                logger.debug(f"表名白名单已启用, 允许的表: {self.allowed_tables}")
            else:
                logger.warning("表名白名单为空集, 禁止所有表操作")

    def _mask_connection_string(self) -> str:
        """隐藏连接字符串中的密码"""
        if "@" in self.connection_string:
            parts = self.connection_string.split("@")
            if ":" in parts[0]:
                user_pass = parts[0].split(":")
                return f"{user_pass[0]}:****@{parts[1]}"
        return self.connection_string

    def _generate_query_id(self) -> str:
        """生成查询ID（用于日志关联）"""
        self._query_counter += 1
        return f"query-{self._query_counter:03d}"

    def _get_event_bus(self):
        """获取 EventBus 实例

        v3.17.1: 支持动态获取（测试隔离）
        """
        if self._event_bus is not None:
            return self._event_bus
        try:
            from df_test_framework.infrastructure.events import get_event_bus

            return get_event_bus()
        except Exception:
            return None

    def _publish_event(self, event: Any) -> None:
        """发布事件到 EventBus（同步模式）

        v3.17.1: 改用 publish_sync() 确保事件完整性
        """
        event_bus = self._get_event_bus()
        if event_bus:
            try:
                event_bus.publish_sync(event)
            except Exception:
                pass  # 静默失败，不影响主流程

    def _validate_table_name(self, table: str) -> None:
        """
        验证表名是否在白名单中

        逻辑规则:
        - allowed_tables=None: 允许所有表 (不检查)
        - allowed_tables=set(): 禁止所有表 (抛出异常)
        - allowed_tables={"a","b"}: 只允许白名单中的表

        Args:
            table: 表名

        Raises:
            ValueError: 表名不在白名单中或白名单为空
        """
        # None表示不限制
        if self.allowed_tables is None:
            return

        # 空集表示禁止所有表
        if not self.allowed_tables:
            raise ValueError(
                f"表操作已禁用: 白名单为空集, 不允许操作任何表. 尝试操作的表: '{table}'"
            )

        # 检查表名是否在白名单中
        if table not in self.allowed_tables:
            raise ValueError(f"表名 '{table}' 不在白名单中. 允许的表: {self.allowed_tables}")

    @staticmethod
    def _prepare_statement(sql: str | Executable) -> Executable:
        """
        将字符串SQL或可执行语句统一转换为 Executable 对象

        Args:
            sql: SQL字符串或已经构建好的Executable
        """
        if isinstance(sql, str):
            return text(sql)
        return sql

    @contextmanager
    def session(self) -> Session:
        """
        获取数据库会话上下文管理器

        使用方式:
            with db.session() as session:
                result = session.execute(text("SELECT * FROM table"))

        Yields:
            Session: SQLAlchemy会话对象
        """
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"数据库操作失败,已回滚: {str(e)}")
            raise
        finally:
            session.close()

    @contextmanager
    def transaction(self):
        """
        事务上下文管理器 - 支持原子操作

        使用方式:
            with db.transaction():
                db.insert("users", {"name": "张三"})
                db.insert("orders", {"user_id": 1})
                # 要么都成功，要么都回滚

        Yields:
            Session: SQLAlchemy会话对象
        """
        session = self.session_factory()
        try:
            yield session
            session.commit()
            logger.info("事务已成功提交")
        except Exception as e:
            session.rollback()
            logger.error(f"事务已回滚: {str(e)}")
            raise
        finally:
            session.close()

    @contextmanager
    def savepoint(self, name: str = "sp1"):
        """
        保存点 - 支持部分回滚

        使用方式:
            with db.transaction():
                db.insert("users", {"name": "张三"})
                try:
                    with db.savepoint("sp1"):
                        db.insert("orders", {"user_id": 1})
                        raise ValueError("订单验证失败")
                except ValueError:
                    # 只回滚到保存点，user已插入
                    pass
                # 继续操作
                db.insert("logs", {"message": "处理完成"})

        Args:
            name: 保存点名称

        Yields:
            Savepoint对象
        """
        session = self.session_factory()
        savepoint = session.begin_nested()
        try:
            yield savepoint
            savepoint.commit()
            logger.debug(f"保存点 {name} 已提交")
        except Exception as e:
            savepoint.rollback()
            logger.debug(f"保存点 {name} 已回滚: {str(e)}")
            raise
        finally:
            session.close()

    def execute(
        self,
        sql: str | Executable,
        params: dict[str, Any] | None = None,
    ) -> int:
        """
        执行SQL语句(INSERT/UPDATE/DELETE)

        Args:
            sql: SQL语句
            params: 参数字典

        Returns:
            影响的行数

        Note:
            此方法仅用于非查询语句,查询请使用 query_one() 或 query_all()
        """
        query_id = self._generate_query_id()

        # 从SQL中提取操作类型和表名
        sql_str = str(sql).strip().upper()
        operation = "EXECUTE"
        table_name = "unknown"

        # 尝试解析操作类型
        for op in ["INSERT", "UPDATE", "DELETE"]:
            if sql_str.startswith(op):
                operation = op
                break

        # 尝试解析表名
        if "INTO" in sql_str:  # INSERT INTO table
            parts = sql_str.split("INTO")[1].split()
            if parts:
                table_name = parts[0].strip()
        elif operation in ["UPDATE", "DELETE"]:
            # UPDATE table SET / DELETE FROM table
            keyword = "FROM" if operation == "DELETE" else operation
            if keyword in sql_str:
                parts = sql_str.split(keyword)[1].split()
                if parts:
                    table_name = parts[0].strip()

        session: Session
        with self.session() as session:
            # ObservabilityLogger: 记录查询开始
            start_time = time.perf_counter()
            self.obs_logger.query_start(operation, table_name, query_id)

            # v3.17.1: 发布查询开始事件（使用 CorrelatedEvent）
            start_event, correlation_id = DatabaseQueryStartEvent.create(
                operation=operation,
                table=table_name,
                sql=str(sql),
                params=params,
            )
            self._publish_event(start_event)

            try:
                statement = self._prepare_statement(sql)
                result = session.execute(statement, params or {})
                rowcount = result.rowcount

                # ObservabilityLogger: 记录查询结束
                duration_ms = (time.perf_counter() - start_time) * 1000
                self.obs_logger.query_end(query_id, rowcount, duration_ms)

                # v3.17.1: 发布查询完成事件
                end_event = DatabaseQueryEndEvent.create(
                    correlation_id=correlation_id,
                    operation=operation,
                    table=table_name,
                    sql=str(sql),
                    params=params,
                    duration_ms=duration_ms,
                    row_count=rowcount,
                )
                self._publish_event(end_event)

                return rowcount
            except Exception as e:
                duration_ms = (time.perf_counter() - start_time) * 1000

                # ObservabilityLogger: 记录查询错误
                self.obs_logger.query_error(e, query_id)

                # v3.17.1: 发布查询错误事件
                error_event = DatabaseQueryErrorEvent.create(
                    correlation_id=correlation_id,
                    operation=operation,
                    table=table_name,
                    sql=str(sql),
                    params=params,
                    error=e,
                    duration_ms=duration_ms,
                )
                self._publish_event(error_event)

                raise

    def query_one(
        self,
        sql: str | Executable,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """
        查询单条记录

        Args:
            sql: SQL查询语句
            params: 参数字典

        Returns:
            单条记录的字典,如果没有结果则返回None
        """
        query_id = self._generate_query_id()

        # 从SQL中提取表名（简单解析）
        sql_str = str(sql).strip().upper()
        table_name = "unknown"
        if "FROM" in sql_str:
            parts = sql_str.split("FROM")[1].split()
            if parts:
                table_name = parts[0].strip()

        session: Session
        with self.session() as session:
            # ObservabilityLogger: 记录查询开始
            start_time = time.perf_counter()
            self.obs_logger.query_start("SELECT", table_name, query_id)

            # v3.17.1: 发布查询开始事件
            start_event, correlation_id = DatabaseQueryStartEvent.create(
                operation="SELECT",
                table=table_name,
                sql=str(sql),
                params=params,
            )
            self._publish_event(start_event)

            try:
                statement = self._prepare_statement(sql)
                result = session.execute(statement, params or {})
                row = result.fetchone()

                # ObservabilityLogger: 记录查询结束
                duration_ms = (time.perf_counter() - start_time) * 1000
                row_count = 1 if row else 0
                self.obs_logger.query_end(query_id, row_count, duration_ms)

                # v3.17.1: 发布查询完成事件
                end_event = DatabaseQueryEndEvent.create(
                    correlation_id=correlation_id,
                    operation="SELECT",
                    table=table_name,
                    sql=str(sql),
                    params=params,
                    duration_ms=duration_ms,
                    row_count=row_count,
                )
                self._publish_event(end_event)

                if row:
                    return dict(row._mapping)
                return None
            except Exception as e:
                duration_ms = (time.perf_counter() - start_time) * 1000

                # ObservabilityLogger: 记录查询错误
                self.obs_logger.query_error(e, query_id)

                # v3.17.1: 发布查询错误事件
                error_event = DatabaseQueryErrorEvent.create(
                    correlation_id=correlation_id,
                    operation="SELECT",
                    table=table_name,
                    sql=str(sql),
                    params=params,
                    error=e,
                    duration_ms=duration_ms,
                )
                self._publish_event(error_event)

                raise

    def query_all(
        self,
        sql: str | Executable,
        params: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        查询多条记录

        Args:
            sql: SQL查询语句
            params: 参数字典

        Returns:
            记录列表
        """
        query_id = self._generate_query_id()

        # 从SQL中提取表名
        sql_str = str(sql).strip().upper()
        table_name = "unknown"
        if "FROM" in sql_str:
            parts = sql_str.split("FROM")[1].split()
            if parts:
                table_name = parts[0].strip()

        session: Session
        with self.session() as session:
            # ObservabilityLogger: 记录查询开始
            start_time = time.perf_counter()
            self.obs_logger.query_start("SELECT", table_name, query_id)

            # v3.17.1: 发布查询开始事件
            start_event, correlation_id = DatabaseQueryStartEvent.create(
                operation="SELECT",
                table=table_name,
                sql=str(sql),
                params=params,
            )
            self._publish_event(start_event)

            try:
                statement = self._prepare_statement(sql)
                result = session.execute(statement, params or {})
                rows = result.fetchall()
                result_list = [dict(row._mapping) for row in rows]

                # ObservabilityLogger: 记录查询结束
                duration_ms = (time.perf_counter() - start_time) * 1000
                self.obs_logger.query_end(query_id, len(result_list), duration_ms)

                # v3.17.1: 发布查询完成事件
                end_event = DatabaseQueryEndEvent.create(
                    correlation_id=correlation_id,
                    operation="SELECT",
                    table=table_name,
                    sql=str(sql),
                    params=params,
                    duration_ms=duration_ms,
                    row_count=len(result_list),
                )
                self._publish_event(end_event)

                return result_list
            except Exception as e:
                duration_ms = (time.perf_counter() - start_time) * 1000

                # ObservabilityLogger: 记录查询错误
                self.obs_logger.query_error(e, query_id)

                # v3.17.1: 发布查询错误事件
                error_event = DatabaseQueryErrorEvent.create(
                    correlation_id=correlation_id,
                    operation="SELECT",
                    table=table_name,
                    sql=str(sql),
                    params=params,
                    error=e,
                    duration_ms=duration_ms,
                )
                self._publish_event(error_event)

                raise

    def insert(
        self,
        table: str,
        data: dict[str, Any] | None = None,
        **values: Any,
    ) -> int:
        """插入记录

        支持三种使用方式:
        1. 字典方式: insert("users", {"name": "张三", "age": 20})
        2. 关键字参数: insert("users", name="张三", age=20)
        3. 混合方式: insert("users", {"name": "张三"}, age=20)

        Args:
            table: 表名
            data: 数据字典（可选）
            **values: 关键字参数形式的数据

        Returns:
            插入的记录ID

        Raises:
            ValueError: 表名不在白名单中或未提供数据
            IntegrityError: 违反唯一性约束等完整性错误
            OperationalError: 数据库操作错误

        Example:
            >>> # 方式1: 字典（适合动态数据）
            >>> database.insert("users", {"name": "张三", "age": 20})

            >>> # 方式2: 关键字参数（最简洁）
            >>> database.insert("users", name="张三", age=20)

            >>> # 方式3: 混合（灵活）
            >>> base_data = {"name": "张三"}
            >>> database.insert("users", base_data, age=20, status=1)
        """
        self._validate_table_name(table)

        # 合并字典和关键字参数
        if data is None:
            data = values
        elif values:
            data = {**data, **values}

        if not data:
            raise ValueError("必须提供至少一个字段值")

        query_id = self._generate_query_id()

        columns = ", ".join(data.keys())
        placeholders = ", ".join([f":{key}" for key in data.keys()])
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        try:
            # ObservabilityLogger: 记录INSERT开始
            start_time = time.perf_counter()
            self.obs_logger.query_start("INSERT", table, query_id)

            # v3.17.1: 发布查询开始事件
            start_event, correlation_id = DatabaseQueryStartEvent.create(
                operation="INSERT",
                table=table,
                sql=sql,
                params=data,
            )
            self._publish_event(start_event)

            session: Session
            with self.session() as session:
                result = session.execute(text(sql), data)
                inserted_id = result.lastrowid

                # ObservabilityLogger: 记录INSERT结束
                duration_ms = (time.perf_counter() - start_time) * 1000
                self.obs_logger.query_end(query_id, 1, duration_ms)

                # v3.17.1: 发布查询完成事件
                end_event = DatabaseQueryEndEvent.create(
                    correlation_id=correlation_id,
                    operation="INSERT",
                    table=table,
                    sql=sql,
                    params=data,
                    duration_ms=duration_ms,
                    row_count=1,
                )
                self._publish_event(end_event)

                return inserted_id
        except (IntegrityError, OperationalError) as e:
            duration_ms = (time.perf_counter() - start_time) * 1000

            # ObservabilityLogger: 记录错误
            self.obs_logger.query_error(e, query_id)

            # v3.18.0: 发布查询错误事件
            error_event = DatabaseQueryErrorEvent.create(
                correlation_id=correlation_id,
                operation="INSERT",
                table=table,
                sql=sql,
                params=data,
                error=e,
                duration_ms=duration_ms,
            )
            self._publish_event(error_event)

            raise

    def batch_insert(
        self,
        table: str,
        data_list: list[dict[str, Any]],
        chunk_size: int = 1000,
    ) -> int:
        """
        批量插入记录

        Args:
            table: 表名
            data_list: 数据字典列表
            chunk_size: 每批次插入数量 (默认1000)

        Returns:
            插入的总记录数

        Raises:
            ValueError: 表名不在白名单中或数据列表为空
            IntegrityError: 违反唯一性约束
            OperationalError: 数据库操作错误

        Example:
            data_list = [
                {"name": "张三", "age": 20},
                {"name": "李四", "age": 25},
                # ... 更多数据
            ]
            count = db.batch_insert("users", data_list)
        """
        self._validate_table_name(table)

        if not data_list:
            raise ValueError("数据列表不能为空")

        # 获取列名 (从第一条数据)
        columns = list(data_list[0].keys())
        columns_str = ", ".join(columns)
        placeholders = ", ".join([f":{col}" for col in columns])

        sql = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"

        total_inserted = 0
        try:
            session: Session
            with self.session() as session:
                # 分批插入
                for i in range(0, len(data_list), chunk_size):
                    chunk = data_list[i : i + chunk_size]
                    session.execute(text(sql), chunk)
                    total_inserted += len(chunk)
                    logger.debug(
                        f"批量插入: {table}, 当前批次 {len(chunk)} 条, 累计 {total_inserted} 条"
                    )

                logger.info(f"批量插入成功: {table}, 总计 {total_inserted} 条记录")
                return total_inserted
        except IntegrityError as e:
            logger.error(f"批量插入数据完整性错误: {table}, 错误: {e.orig}")
            raise
        except OperationalError as e:
            logger.error(f"批量插入操作错误: {table}, 错误: {str(e)}")
            raise

    def update(
        self,
        table: str,
        data: dict[str, Any],
        where: str,
        where_params: dict[str, Any] | None = None,
    ) -> int:
        """
        更新记录

        Args:
            table: 表名
            data: 要更新的数据字典
            where: WHERE条件
            where_params: WHERE条件参数

        Returns:
            影响的行数

        Raises:
            ValueError: 表名不在白名单中
            OperationalError: 数据库操作错误
        """
        self._validate_table_name(table)

        set_clause = ", ".join([f"{key} = :{key}" for key in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where}"

        params = {**data, **(where_params or {})}

        try:
            session: Session
            with self.session() as session:
                result = session.execute(text(sql), params)
                affected_rows = result.rowcount
                logger.info(f"更新记录成功: {table}, 影响行数: {affected_rows}")
                return affected_rows
        except OperationalError as e:
            logger.error(f"更新操作错误: {table}, 错误: {str(e)}")
            raise

    def delete(
        self,
        table: str,
        where: str,
        where_params: dict[str, Any] | None = None,
    ) -> int:
        """
        删除记录

        Args:
            table: 表名
            where: WHERE条件
            where_params: WHERE条件参数

        Returns:
            删除的行数

        Raises:
            ValueError: 表名不在白名单中
            OperationalError: 数据库操作错误
        """
        self._validate_table_name(table)

        sql = f"DELETE FROM {table} WHERE {where}"

        try:
            session: Session
            with self.session() as session:
                result = session.execute(text(sql), where_params or {})
                deleted_rows = result.rowcount
                logger.info(f"删除记录成功: {table}, 删除行数: {deleted_rows}")
                return deleted_rows
        except OperationalError as e:
            logger.error(f"删除操作错误: {table}, 错误: {str(e)}")
            raise

    def update_where(
        self,
        table: str,
        conditions: dict[str, Any],
        data: dict[str, Any] | None = None,
        **updates: Any,
    ) -> int:
        """便捷的更新方法 - 使用字典条件

        简化的更新方法，自动构建 WHERE 条件，适合简单的等值条件查询。
        如需复杂的 WHERE 条件（如 >, <, LIKE），请使用 update() 方法。

        Args:
            table: 表名
            conditions: WHERE 条件字典（AND 连接）
            data: 要更新的数据字典（可选）
            **updates: 关键字参数形式的更新数据

        Returns:
            影响的行数

        Raises:
            ValueError: 表名不在白名单中、未提供更新数据或未提供条件
            OperationalError: 数据库操作错误

        Example:
            >>> # 方式1: 字典更新
            >>> database.update_where(
            ...     "users",
            ...     {"user_id": "123"},
            ...     {"age": 21, "status": 1}
            ... )

            >>> # 方式2: 关键字参数更新（最简洁）
            >>> database.update_where(
            ...     "users",
            ...     {"user_id": "123"},
            ...     age=21,
            ...     status=1
            ... )

            >>> # 方式3: 多条件
            >>> database.update_where(
            ...     "orders",
            ...     {"order_no": "ORD001", "user_id": "123"},
            ...     status=1
            ... )
        """
        self._validate_table_name(table)

        # 合并字典和关键字参数
        if data is None:
            data = updates
        elif updates:
            data = {**data, **updates}

        if not data:
            raise ValueError("必须提供至少一个更新字段")
        if not conditions:
            raise ValueError("必须提供 WHERE 条件，如需更新所有记录请使用 update() 方法")

        # 构建 SET 子句
        set_clause = ", ".join([f"{key} = :set_{key}" for key in data.keys()])

        # 构建 WHERE 子句
        where_clause = " AND ".join([f"{key} = :where_{key}" for key in conditions.keys()])

        # 合并参数（添加前缀避免冲突）
        params = {
            **{f"set_{k}": v for k, v in data.items()},
            **{f"where_{k}": v for k, v in conditions.items()},
        }

        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"

        try:
            session: Session
            with self.session() as session:
                result = session.execute(text(sql), params)
                affected_rows = result.rowcount
                logger.info(f"更新记录成功: {table}, 影响行数: {affected_rows}")
                return affected_rows
        except OperationalError as e:
            logger.error(f"更新操作错误: {table}, 错误: {str(e)}")
            raise

    def delete_where(
        self,
        table: str,
        **conditions: Any,
    ) -> int:
        """便捷的删除方法 - 使用关键字参数条件

        简化的删除方法，自动构建 WHERE 条件，适合简单的等值条件查询。
        如需复杂的 WHERE 条件（如 >, <, LIKE），请使用 delete() 方法。

        Args:
            table: 表名
            **conditions: WHERE 条件（AND 连接）

        Returns:
            删除的行数

        Raises:
            ValueError: 表名不在白名单中或未提供条件
            OperationalError: 数据库操作错误

        Example:
            >>> # 单条件
            >>> database.delete_where("users", user_id="123")

            >>> # 多条件
            >>> database.delete_where("orders", order_no="ORD001", user_id="123")
        """
        if not conditions:
            raise ValueError("必须提供 WHERE 条件，如需删除所有记录请使用 delete() 方法")

        self._validate_table_name(table)

        where_clause = " AND ".join([f"{key} = :{key}" for key in conditions.keys()])
        sql = f"DELETE FROM {table} WHERE {where_clause}"

        try:
            session: Session
            with self.session() as session:
                result = session.execute(text(sql), conditions)
                deleted_rows = result.rowcount
                logger.info(f"删除记录成功: {table}, 删除行数: {deleted_rows}")
                return deleted_rows
        except OperationalError as e:
            logger.error(f"删除操作错误: {table}, 错误: {str(e)}")
            raise

    def find_one(
        self,
        table: str,
        conditions: dict[str, Any] | None = None,
        columns: list[str] | str = "*",
    ) -> dict[str, Any] | None:
        """
        查询单条记录（简化版）

        便捷方法，用于快速查询单条记录，自动构建 WHERE 条件。

        Args:
            table: 表名
            conditions: 查询条件字典，例如 {"user_id": "123", "status": 1}
            columns: 要查询的列，默认 "*"（所有列）
                    可以是字符串 "*" 或列表 ["id", "name", "email"]

        Returns:
            单条记录的字典，如果没有结果则返回 None

        Example:
            # 查询用户
            user = database.find_one("users", {"user_id": "12345"})

            # 查询特定列
            user = database.find_one(
                "users",
                {"user_id": "12345"},
                columns=["id", "name", "email"]
            )

            # 查询所有记录中的第一条
            first_user = database.find_one("users")
        """
        # 构建列名
        if isinstance(columns, list):
            columns_str = ", ".join(columns)
        else:
            columns_str = columns

        # 构建 SQL
        if conditions:
            where_clause = " AND ".join([f"{key} = :{key}" for key in conditions.keys()])
            sql = f"SELECT {columns_str} FROM {table} WHERE {where_clause}"
            return self.query_one(sql, conditions)
        else:
            sql = f"SELECT {columns_str} FROM {table} LIMIT 1"
            return self.query_one(sql)

    def find_many(
        self,
        table: str,
        conditions: dict[str, Any] | None = None,
        columns: list[str] | str = "*",
        limit: int | None = None,
        offset: int | None = None,
        order_by: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        查询多条记录（简化版）

        便捷方法，用于快速查询多条记录，自动构建 WHERE 条件。

        Args:
            table: 表名
            conditions: 查询条件字典，例如 {"user_id": "123", "status": 1}
            columns: 要查询的列，默认 "*"（所有列）
                    可以是字符串 "*" 或列表 ["id", "name", "email"]
            limit: 限制返回记录数
            offset: 偏移量（跳过前 N 条记录）
            order_by: 排序字段，例如 "id DESC" 或 "created_at ASC"

        Returns:
            记录列表

        Example:
            # 查询所有用户
            users = database.find_many("users")

            # 条件查询
            active_users = database.find_many("users", {"status": 1})

            # 分页查询
            users = database.find_many(
                "users",
                {"status": 1},
                limit=10,
                offset=20,
                order_by="created_at DESC"
            )

            # 查询特定列
            users = database.find_many(
                "users",
                {"status": 1},
                columns=["id", "name", "email"]
            )
        """
        # 构建列名
        if isinstance(columns, list):
            columns_str = ", ".join(columns)
        else:
            columns_str = columns

        # 构建 SQL
        sql_parts = [f"SELECT {columns_str} FROM {table}"]

        # WHERE 条件
        params = {}
        if conditions:
            where_clause = " AND ".join([f"{key} = :{key}" for key in conditions.keys()])
            sql_parts.append(f"WHERE {where_clause}")
            params.update(conditions)

        # ORDER BY
        if order_by:
            sql_parts.append(f"ORDER BY {order_by}")

        # LIMIT 和 OFFSET
        if limit is not None:
            sql_parts.append(f"LIMIT {limit}")
        if offset is not None:
            sql_parts.append(f"OFFSET {offset}")

        sql = " ".join(sql_parts)
        return self.query_all(sql, params)

    def table(self, name: str):
        """获取 Query Builder（流式 API）

        创建一个 QueryBuilder 实例用于构建复杂查询。
        QueryBuilder 提供流式 API，支持链式调用。

        Args:
            name: 表名

        Returns:
            QueryBuilder: 查询构建器实例，已绑定当前 Database

        Example:
            >>> # 简单查询
            >>> users = database.table("users").where("status", 1).get()

            >>> # 复杂查询
            >>> result = (
            ...     database.table("orders")
            ...     .select("orders.id", "users.name", "orders.amount")
            ...     .join("users", "orders.user_id", "users.id")
            ...     .where("orders.status", "paid")
            ...     .where_in("orders.type", ["online", "offline"])
            ...     .order_by("orders.created_at", "DESC")
            ...     .limit(10)
            ...     .get()
            ... )

            >>> # 获取单条记录
            >>> user = database.table("users").where("user_id", "123").first()
        """
        from .query_builder import QueryBuilder

        return QueryBuilder(name, database=self)

    def close(self) -> None:
        """关闭数据库连接"""
        self.engine.dispose()
        logger.info("数据库连接已关闭")


__all__ = ["Database"]
