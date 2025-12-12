from typing import Generic, Type, TypeVar

from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.sql.elements import OperatorExpression
from sqlalchemy.sql.expression import false

ModelType = TypeVar("ModelType", bound=object)


class BaseMapper(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        assert issubclass(model, DeclarativeBase), "必须是 s.o.DeclarativeBase 的子类"
        assert hasattr(model, "id"), "必须有 id 属性"
        assert hasattr(model, "is_delete"), "必须有 is_delete 属性"
        self.model = model

    def get_by_condition(self, session: Session, condition: OperatorExpression):
        """获取单个对象 by 条件"""
        _stmt = session.query(self.model)
        # xxx == False 会让 Linter 提示并转化为 not xxx，所以用 false()
        _stmt = _stmt.filter(self.model.is_delete == false())
        _stmt = _stmt.filter(condition)

        return _stmt.scalar()

    def get_by_id(self, session: Session, id: int):
        """获取单个对象 by id"""
        return session.query(self.model).filter(self.model.id == id).first()

    def get_batch_by_condition(
        self, session: Session, condition: OperatorExpression = None
    ) -> list[ModelType]:
        """批量获取"""
        _stmt = session.query(self.model)
        _stmt = _stmt.filter(self.model.is_delete == false())
        if condition is not None:
            _stmt = _stmt.filter(condition)
        return _stmt.all()

    def insert(self, session: Session, po: ModelType) -> ModelType:
        """插入"""
        session.add(po)
        # session.commit() # 事物由上层控制
        # session.refresh(po)
        return po

    def insert_batch(self, session: Session, po_list: list[ModelType]) -> ModelType:
        """批量插入"""
        session.add_all(po_list)
        # session.commit()
        # session.refresh()
        return po_list

    def upsert_one(
        self,
        session: Session,
        po: ModelType,
        condition: OperatorExpression = None,
        force: bool = False,
    ) -> ModelType:
        assert isinstance(po, self.model)
        _old = session.query(self.model).filter(condition).scalar()
        # 如果不存在则插入
        if not _old:
            session.add(po)
            return po
        if force:
            po.id = _old.id
            session.merge(po)
            return po
        return _old

    def upsert_batch(
        self,
        session: Session,
        po_list: list[ModelType],
        criteria: OperatorExpression = None,
        force: bool = False,
    ) -> ModelType:
        res = []
        for po in po_list:
            _new = self.upsert_one(session, po, criteria, force)
            res.append(_new)
        return po_list

    def delete_soft_by_id(self, session: Session, id: int):
        """软删除 by id"""
        _data = session.query(self.model).filter(self.model.id == id).all()
        for item in _data:
            item.is_delete = True

    def delete_soft_by_condition(self, session: Session, condition: OperatorExpression):
        """软删除 by condition"""
        _data = session.query(self.model).filter(condition).all()
        for _item in _data:
            _item.is_delete = True

    def delete_by_id(self, session: Session, id: int):
        """硬删除 by id"""
        session.query(self.model).filter(self.model.id == id).delete()

    def delete_by_condition(self, session: Session, condition):
        """硬删除 by condition"""
        session.query(self.model).filter(condition).delete()
