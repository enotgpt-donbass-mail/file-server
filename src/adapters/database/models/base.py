from datetime import datetime

from sqlalchemy import TIMESTAMP
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    """
    Base class that provides metadata and id with int4
    """

    id: Mapped[int] = mapped_column(BIGINT, autoincrement=True, primary_key=True)


class BaseWithTelemetryTimestamps(Base):
    __abstract__ = True

    create_date: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    modify_date: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.now, onupdate=datetime.now
    )