from __future__ import annotations

import importlib

from sqlalchemy import inspect


EXPECTED_TABLES = {
    "persons",
    "person_photos",
    "events",
    "event_photos",
    "detected_faces",
    "attendance_records",
    "users",
    "audit_logs",
}


def test_init_database_creates_expected_tables(monkeypatch, tmp_path) -> None:
    db_file = tmp_path / "test_app.db"
    monkeypatch.setenv("APP_DATABASE_URL", f"sqlite:///{db_file.as_posix()}")

    import app.config as config_module
    import app.db.init_db as init_db_module
    import app.db.session as session_module

    importlib.reload(config_module)
    importlib.reload(session_module)
    importlib.reload(init_db_module)

    init_db_module.init_database()

    inspector = inspect(session_module.engine)
    assert EXPECTED_TABLES.issubset(set(inspector.get_table_names()))
