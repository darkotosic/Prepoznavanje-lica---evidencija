from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
DATABASE_DIR = DATA_DIR / "database"
IMAGES_DIR = DATA_DIR / "images"
PERSON_IMAGES_DIR = IMAGES_DIR / "persons"
EVENT_IMAGES_DIR = IMAGES_DIR / "events"
EXPORTS_DIR = DATA_DIR / "exports"

DEFAULT_SQLITE_PATH = DATABASE_DIR / "app.db"
DATABASE_URL = os.getenv("APP_DATABASE_URL", f"sqlite:///{DEFAULT_SQLITE_PATH.as_posix()}")


def ensure_runtime_directories() -> None:
    for path in (
        DATA_DIR,
        DATABASE_DIR,
        IMAGES_DIR,
        PERSON_IMAGES_DIR,
        EVENT_IMAGES_DIR,
        EXPORTS_DIR,
    ):
        path.mkdir(parents=True, exist_ok=True)
