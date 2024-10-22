import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, func, Integer, ForeignKey, Date, Boolean, insert
from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.database.models.base import BaseWithTelemetryTimestamps


class Role(BaseWithTelemetryTimestamps):
    """
    Роли пользователей
    """
    __tablename__ = "roles"



class User(BaseWithTelemetryTimestamps):
    """
    Базовая информация о пользователе
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(50))
    birth_date: Mapped[Optional[Date]] = mapped_column(Date)
    gender: Mapped[Optional[int]] = mapped_column(Integer)
    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), unique=True, index=True)
    telegram_id: Mapped[Optional[int]] = mapped_column(Integer, unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    is_email_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    is_phone_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class VerificationCode(BaseWithTelemetryTimestamps):
    """
    Таблица верификации пользователя
    """
    __tablename__ = "verification_codes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    verification_type: Mapped[str] = mapped_column(String, nullable=False)
    code: Mapped[int] = mapped_column(Integer, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class UserRoles(BaseWithTelemetryTimestamps):
    """
    Роли пользователя
    """
    __tablename__ = "user_roles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class RefreshToken(BaseWithTelemetryTimestamps):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    expires_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

