"""Database Library"""

from os import environ

from loguru import logger
from sqlalchemy import ColumnElement, TextClause, and_, delete, text, update
from sqlalchemy.engine import CursorResult, Result, ScalarResult
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.sql import Delete, Insert, Select, Update

# --------------------------------------------------------------------------------------------------

DEBUG = environ.get("DEBUG")

# --------------------------------------------------------------------------------------------------


# 同步


def session_execute(session: Session, statement: str | TextClause | Delete | Insert | Select | Update) -> Result | CursorResult | None:
    """Session execute statement"""

    # SQL 语句既可以是 text() 对象 也可以是 ORM 构建的 statement 对象
    #
    #   text() 对象可以是任意 SQL 语句
    #   statement 对象包括 select, insert, update, delete 等
    #
    # 原生 SQL 返回 Result
    # ORM 返回 CursorResult

    # 执行语句
    info: str = "database execute statement"

    if DEBUG:
        logger.debug(f"{info} [SQL]\n------\n\n{statement}\n\n------")

    logger.info(f"{info} [start]")

    try:
        stmt = text(statement) if isinstance(statement, str) else statement
        result: Result = session.execute(stmt)
        session.commit()
        logger.success(f"{info} [success]")
        return result
    except Exception as e:
        logger.error(f"{info} [error]")
        session.rollback()
        if DEBUG:
            logger.exception(e)
        else:
            logger.error(e)
        return None


def session_scalars(session: Session, statement: str | TextClause | Delete | Insert | Select | Update) -> ScalarResult | None:
    """Session scalars statement"""

    # SQL 语句既可以是 text() 对象 也可以是 ORM 构建的 statement 对象
    #
    #   text() 对象可以是任意 SQL 语句
    #   statement 对象包括 select, insert, update, delete 等

    # 示例:
    #
    #   查询出所有 code (只有一列, 所以这里使用 scalars(), 返回的是 list 而不是 list[tuple])
    #
    #       sql: str = text("SELECT code FROM ashare;")
    #       records = session_execute.execute(sql).scalars().all()
    #
    #       records 是包含所有 code 的列表

    # 执行语句
    info: str = "database execute statement"

    if DEBUG:
        logger.debug(f"{info} [SQL]\n------\n\n{statement}\n\n------")

    logger.info(f"{info} [start]")

    try:
        stmt = text(statement) if isinstance(statement, str) else statement
        result: ScalarResult = session.scalars(stmt)
        session.commit()
        logger.success(f"{info} [success]")
        return result
    except Exception as e:
        logger.error(f"{info} [error]")
        session.rollback()
        if DEBUG:
            logger.exception(e)
        else:
            logger.error(e)
        return None


# --------------------------------------------------------------------------------------------------


class ORMBase(DeclarativeBase):
    """ORM Base"""

    pass  # pylint: disable=unnecessary-pass


class ORMSession:
    """ORM Session"""

    # 用 ORM 的主要目的是简化数据库操作
    # 用于处理 dict 类型的数据, 而不是 ORM 对象类型的数据
    #
    # 例如:
    #
    #   插入 dict 或 list[dict]
    #   根据 dict 查询, 删除, 更新数据

    # 初始化
    def __init__(self, model: type[ORMBase], session: Session):

        # 模型类
        self.model: type[ORMBase] = model
        self.session: Session = session
        self.info: str = f"Model: {model.__tablename__}"

    # ----------------------------------------------------------------------------------------------

    # 连接测试
    def test_connection(self) -> bool:
        """测试数据库连接"""

        # 测试连接 | 开始
        logger.info(f"{self.info} [ test connection | start ]")

        try:

            self.session.execute(text("SELECT 1;"))

            # 测试连接 | 成功
            logger.success(f"{self.info} [ test connection | success ]")

            return True

        except Exception as e:

            # 测试连接 | 错误
            logger.error(f"{self.info} [ test connection | error ]")

            if DEBUG:
                logger.exception(e)
            else:
                logger.error(e)

            return False

    # ----------------------------------------------------------------------------------------------

    # 初始化 model 表
    def init_model(self) -> bool:
        """初始化模型表, 删除已存在的表并重新创建"""

        # 初始化 | 开始
        logger.info(f"{self.info} [ initialization | start ]")

        try:

            self.model.__table__.drop(bind=self.session.get_bind(), checkfirst=True)  # type: ignore
            self.model.__table__.create(bind=self.session.get_bind(), checkfirst=True)  # type: ignore

            # 初始化 | 成功
            logger.success(f"{self.info} [ initialization | success ]")

            return True

        except Exception as e:

            # 初始化 | 错误
            logger.error(f"{self.info} [ initialization | error ]")

            if DEBUG:
                logger.exception(e)
            else:
                logger.error(e)

            return False

    # ----------------------------------------------------------------------------------------------

    # 执行 SQL 语句

    def execute(self, *args, **kwargs):
        """执行语句"""
        return session_execute(self.session, *args, **kwargs)

    def scalars(self, *args, **kwargs):
        """执行 SQL 语句"""
        return session_scalars(self.session, *args, **kwargs)

    # ----------------------------------------------------------------------------------------------

    # 插入
    def create(self, data: dict | list[dict] | tuple[dict, ...], bulk: bool = False) -> int:
        """插入数据, 支持单条和批量插入"""

        # 数据格式:
        #
        #   单条: dict
        #   批量: list[dict] | tuple[dict]
        #
        # 规范: 只接受以上两种形式的数据
        #
        # dict 的 key 必须和 模型(model) 的字段名一致
        #
        # 纯 list 或者 tuple 需要转换为 list[dict] 或者 tuple[dict] 格式
        #
        # 如果 bulk 为 True, 则使用 session.bulk_insert_mappings, 否则使用 session.add_all
        #
        #   bulk_insert_mappings 适合批量插入数据, 适用于数据量较大的情况, 速度更快
        #
        #   注意: bulk_insert_mappings 只接受 list[dict] 格式数据
        #
        # 返回插入的记录数

        # 单条插入
        if isinstance(data, dict) and data:

            # 创建单条数据 | 开始
            logger.info(f"{self.info} [ create single data | start ]")

            try:

                # self.session.execute(
                #     insert(self.model.__table__).values(data)
                # )

                self.session.add(self.model(**data))
                self.session.commit()

                # 创建单条数据 | 成功
                logger.success(f"{self.info} [ create single data | success ]")

                return 1

            except Exception as e:

                # 创建单条数据 | 错误
                logger.error(f"{self.info} [ create single data | error ]")

                self.session.rollback()

                if DEBUG:
                    logger.exception(e)
                else:
                    logger.error(e)

                return 0

        # 批量插入
        if isinstance(data, list | tuple) and data:

            # 创建批量数据 | 开始
            logger.info(f"{self.info} [ create batch data | start ]")

            try:

                if bulk:
                    self.session.bulk_insert_mappings(self.model.__mapper__, data)
                else:
                    orm_instances = [self.model(**item) for item in data]
                    self.session.add_all(orm_instances)

                self.session.commit()

                # 创建批量数据 | 成功
                logger.success(f"{self.info} [ create batch data | success ]")

                return len(data)

            except IntegrityError as ie:

                # 批量插入遇到重复或约束冲突, 回退并逐条插入.

                # 创建批量数据 | 错误 | 尝试逐条创建
                logger.error(f"{self.info} [ create batch data | error ]")

                self.session.rollback()

                logger.warning(ie)

                count = 0

                for item in data:

                    try:

                        self.session.add(self.model(**item))
                        self.session.commit()

                        count += 1

                        # 已插入 count 条数据
                        logger.success(f"{self.info} [ {count} pieces of data have been created ]")

                    except IntegrityError:

                        # 数据已存在 | 跳过
                        logger.warning(f"{self.info} [ data already exists | skip ]")

                        self.session.rollback()

                    except Exception as e:

                        # 逐条插入时发生错误, 插入数据|失败|跳过该条数据
                        logger.error(f"{self.info} [ create data one by one | error ]")

                        self.session.rollback()

                        if DEBUG:
                            logger.exception(e)
                        else:
                            logger.error(e)

                # 逐条插入数据 | 完成
                logger.success(f"{self.info} [ create data one by one | finish ]")

                return count

        # 插入数据|空
        logger.warning(f"{self.info} [ create data | none ]")

        return 0

    # ----------------------------------------------------------------------------------------------

    def _build_where(self, where: dict | list | tuple | ColumnElement | None) -> ColumnElement | None:
        """build where"""

        # where 支持:

        #   dict: {"name": "Tom", "status": 1}
        #   list/tuple: [model.age > 18, model.status == 1]
        #   单个表达式: model.age > 18

        try:

            if where is None:
                return None

            # dict 转表达式
            if isinstance(where, dict) and where:

                conditions = []

                for k, v in where.items():
                    column = getattr(self.model, k)
                    conditions.append(column == v)

                return and_(*conditions)

            # where 是 list/tuple，或表达式
            if isinstance(where, (list, tuple)) and where:
                return and_(*where)

            if isinstance(where, ColumnElement):
                # ORM 表达式
                # 单个表达式
                return where

            return None

        except Exception as e:
            if DEBUG:
                logger.exception(e)
            else:
                logger.error(e)
            return None

    # ----------------------------------------------------------------------------------------------

    # 更新
    def update(self, where: dict | list | tuple | ColumnElement | None, data: dict) -> int:
        """Update"""

        # where 可以是:
        #
        #   {"id": 1}
        #   {"name": "Tom", "status": 1}
        #   [model.age > 18, model.status == 1]
        #   model.age > 18
        #
        # 示例:
        #
        #   crud.update({"id": 5}, {"name": "NewName"})
        #   crud.update({"name": "Tom"}, {"age": 20})
        #   crud.update([User.age > 18, User.status == 1], {"level": 2})
        #   crud.update(User.age < 10, {"flag": False})

        # 更新数据 | 开始
        logger.info(f"{self.info} [ update data | start ]")

        try:

            cond = self._build_where(where)

            if cond is None:
                # 创建 where 语句错误
                logger.error(f"{self.info} [ build where error ]")
                return 0

            stmt = update(self.model).where(cond).values(**data).execution_options(synchronize_session="fetch")

            # 因为 Update 是通过操作 ORM, 所以这里返回的是 CursorResult
            result: CursorResult | None = self.execute(stmt)  # type: ignore

            if not result:

                # 更新数据 | 错误
                logger.error(f"{self.info} [ update data | error ]")

                return 0

            # 更新数据 | 成功
            logger.success(f"{self.info} [ update data | success ]")

            return result.rowcount

        except Exception as e:

            # 更新数据 | 错误
            logger.error(f"{self.info} [ update data | error ]")

            if DEBUG:
                logger.exception(e)
            else:
                logger.error(e)

            return 0

    # ----------------------------------------------------------------------------------------------

    # 删除
    def delete(self, where: dict | list | tuple | ColumnElement | None) -> int:
        """Delete"""

        # 示例
        #
        #   crud.delete({"id": 3})
        #   crud.delete({"status": 0})
        #   crud.delete([User.age < 8])
        #   crud.delete(User.age < 8)

        # 删除数据 | 开始
        logger.info(f"{self.info} [ delete data | start ]")

        try:

            cond = self._build_where(where)

            if cond is None:
                # 创建 where 语句错误
                logger.error(f"{self.info} [ build where error ]")
                return 0

            stmt = delete(self.model).where(cond)

            # 因为 Delete 是通过操作 ORM, 所以这里返回的是 CursorResult
            result: CursorResult | None = self.execute(stmt)  # type: ignore

            if not result:

                # 删除数据 | 错误
                logger.error(f"{self.info} [ delete data | error ]")

                return 0

            # 删除数据 | 成功
            logger.success(f"{self.info} [ delete data | success ]")

            return result.rowcount

        except Exception as e:

            # 删除数据 | 错误
            logger.error(f"{self.info} [ delete data | error ]")

            if DEBUG:
                logger.exception(e)
            else:
                logger.error(e)

            return 0
