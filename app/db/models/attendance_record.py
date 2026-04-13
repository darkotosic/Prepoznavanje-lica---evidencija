"""AttendanceRecord ORM model."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.detected_face import DetectedFace
    from app.db.models.event import Event
    from app.db.models.person import Person
    from app.db.models.user import User


class AttendanceRecord(Base, TimestampMixin):
    __tablename__ = "attendance_records"
    __table_args__ = (UniqueConstraint("event_id", "person_id", name="uq_event_person_attendance"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), nullable=False, index=True)
    source_detected_face_id: Mapped[int | None] = mapped_column(ForeignKey("detected_faces.id"), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="confirmed")
    confirmed_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    event: Mapped["Event"] = relationship(back_populates="attendance_records")
    person: Mapped["Person"] = relationship(back_populates="attendance_records")
    source_detected_face: Mapped["DetectedFace | None"] = relationship(back_populates="attendance_records")
    confirmed_by_user: Mapped["User | None"] = relationship(back_populates="confirmed_attendance_records")
