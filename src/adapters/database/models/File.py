from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.database.models.base import Base, BaseWithTelemetryTimestamps


class File(BaseWithTelemetryTimestamps):
    __tablename__ = "files"

    name: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    hash: Mapped[str] = mapped_column(String)
    path: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
