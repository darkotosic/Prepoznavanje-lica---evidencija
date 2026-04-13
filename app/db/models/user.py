"""User ORM model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.attendance_record import AttendanceRecord
    from app.db.models.audit_log import AuditLog
    from app.db.models.detected_face import DetectedFace
    from app.db.models.event import Event


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="operator")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    events_created: Mapped[list["Event"]] = relationship(back_populates="created_by_user")
    reviewed_faces: Mapped[list["DetectedFace"]] = relationship(back_populates="reviewed_by_user")
    confirmed_attendance_records: Mapped[list["AttendanceRecord"]] = relationship(
        back_populates="confirmed_by_user"
    )
    audit_logs: Mapped[list["AuditLog"]] = relationship(back_populates="actor_user")
