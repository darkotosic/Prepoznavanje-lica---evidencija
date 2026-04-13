"""Application bootstrap entrypoint."""

from app.db.base import Base
from app.db.session import engine
from app.db import models  # noqa: F401  # Ensure model metadata is loaded.


def bootstrap() -> None:
    """Initialize application resources for local MVP startup."""
    Base.metadata.create_all(bind=engine)


def main() -> None:
    """Run minimal startup routine."""
    bootstrap()
    print("Application bootstrap completed.")


if __name__ == "__main__":
    main()
