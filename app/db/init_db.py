"""Database initialization helpers."""

from __future__ import annotations

from app.config import ensure_runtime_directories
from app.db import models  # noqa: F401
from app.db.base import Base
from app.db.session import engine


def init_database() -> None:
    """Create runtime directories and database tables for local MVP startup."""
    ensure_runtime_directories()
    Base.metadata.create_all(bind=engine)
