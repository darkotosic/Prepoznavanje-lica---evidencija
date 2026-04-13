"""PersonPhoto ORM model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Float, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.db.models.person import Person


class PersonPhoto(Base, TimestampMixin):
    __tablename__ = "person_photos"

    id: Mapped[int] = mapped_column(primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id", ondelete="CASCADE"), nullable=False, index=True)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    face_detected: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    image_quality_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    embedding_vector: Mapped[list[float] | None] = mapped_column(JSON, nullable=True)

    person: Mapped["Person"] = relationship(back_populates="photos")
