"""Repository operations for Person ORM entity."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.person import Person


class PersonRepository:
    """Data access for Person entities without business rules."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, *, data: dict) -> Person:
        person = Person(**data)
        self._session.add(person)
        self._session.flush()
        self._session.refresh(person)
        return person

    def get_by_id(self, person_id: int) -> Person | None:
        return self._session.get(Person, person_id)

    def get_by_employee_code(self, employee_code: str) -> Person | None:
        stmt = select(Person).where(Person.employee_code == employee_code)
        return self._session.execute(stmt).scalar_one_or_none()

    def list_all(self) -> list[Person]:
        stmt = select(Person).order_by(Person.id.asc())
        return list(self._session.execute(stmt).scalars().all())

    def update(self, person: Person, *, data: dict) -> Person:
        for field, value in data.items():
            setattr(person, field, value)
        self._session.add(person)
        self._session.flush()
        self._session.refresh(person)
        return person

    def deactivate(self, person: Person) -> Person:
        person.is_active = False
        self._session.add(person)
        self._session.flush()
        self._session.refresh(person)
        return person
