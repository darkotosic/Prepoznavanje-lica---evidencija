"""DetectedFace model skeleton."""

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class DetectedFace(Base):
    __tablename__ = "detected_faces"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_photo_id: Mapped[int] = mapped_column(ForeignKey("event_photos.id"), nullable=False, index=True)
    suggested_person_id: Mapped[int | None] = mapped_column(ForeignKey("persons.id"), nullable=True, index=True)
    confidence_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="unknown")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
