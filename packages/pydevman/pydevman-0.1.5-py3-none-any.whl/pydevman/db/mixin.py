from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase): ...


class IdMixin:
    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, comment="主键"
    )


class TimeMixin:
    """表结构基础:包含表基础字段(创建时间、更新时间和软删除标识)"""

    create_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), comment="创建时间"
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )


class CreatorMixin:
    create_user: Mapped[str] = mapped_column(
        String(50), default="admin", comment="创建用户"
    )
    update_user: Mapped[str] = mapped_column(
        String(50), onupdate="admin", comment="更新用户"
    )


class SoftDeleteMixin:
    is_delete: Mapped[bool] = mapped_column(default=False)
