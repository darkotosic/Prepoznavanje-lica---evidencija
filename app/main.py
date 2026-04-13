"""Application bootstrap entrypoint."""

from __future__ import annotations

from app.config import DATABASE_URL
from app.db.init_db import init_database


def main() -> None:
    """Run minimal startup routine for local MVP bootstrap."""
    init_database()
    print(f"Application bootstrap completed. Database initialized at: {DATABASE_URL}")


if __name__ == "__main__":
    main()
