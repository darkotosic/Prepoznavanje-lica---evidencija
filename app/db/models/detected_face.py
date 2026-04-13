"""DetectedFace ORM model."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.attendance_record import AttendanceRecord
    from app.db.models.event_photo import EventPhoto
    from app.db.models.person import Person
    from app.db.models.user import User


class DetectedFace(Base, TimestampMixin):
    __tablename__ = "detected_faces"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_photo_id: Mapped[int] = mapped_column(
        ForeignKey("event_photos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    cropped_face_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    bbox_x: Mapped[int | None] = mapped_column(Integer, nullable=True)
    bbox_y: Mapped[int | None] = mapped_column(Integer, nullable=True)
    bbox_w: Mapped[int | None] = mapped_column(Integer, nullable=True)
    bbox_h: Mapped[int | None] = mapped_column(Integer, nullable=True)
    embedding_vector: Mapped[list[float] | None] = mapped_column(JSON, nullable=True)
    recognition_status: Mapped[str] = mapped_column(String(50), nullable=False, default="unknown")
    best_match_person_id: Mapped[int | None] = mapped_column(ForeignKey("persons.id"), nullable=True, index=True)
    confidence_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    reviewed_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    event_photo: Mapped["EventPhoto"] = relationship(back_populates="detected_faces")
    best_match_person: Mapped["Person | None"] = relationship(back_populates="detected_faces")
    reviewed_by_user: Mapped["User | None"] = relationship(back_populates="reviewed_faces")
    attendance_records: Mapped[list["AttendanceRecord"]] = relationship(back_populates="source_detected_face")
