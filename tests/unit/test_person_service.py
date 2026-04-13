from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.models.person import Person
from app.schemas.person import PersonCreate, PersonUpdate
from app.services.person_service import PersonService


@pytest.fixture()
def session() -> Session:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine, tables=[Person.__table__])
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True, expire_on_commit=False)
    with SessionLocal() as db:
        yield db


def test_create_person_happy_path(session: Session) -> None:
    service = PersonService(session)

    created = service.create_person(
        PersonCreate(
            first_name="  Ana ",
            last_name="  Nikolic ",
            employee_code="  E-001  ",
            department="  HR ",
            note="  Team lead  ",
        )
    )

    assert created.employee_code == "E-001"
    assert created.first_name == "Ana"
    assert created.last_name == "Nikolic"
    assert created.full_name == "Ana Nikolic"
    assert created.department == "HR"
    assert created.note == "Team lead"
    assert created.is_active is True


def test_create_person_validation_error_for_empty_name(session: Session) -> None:
    service = PersonService(session)

    with pytest.raises(ValueError, match="first_name is required"):
        service.create_person(PersonCreate(first_name="   ", last_name="Nikolic"))

    with pytest.raises(ValueError, match="last_name is required"):
        service.create_person(PersonCreate(first_name="Ana", last_name="   "))


def test_get_and_list_people(session: Session) -> None:
    service = PersonService(session)

    first = service.create_person(PersonCreate(first_name="Ana", last_name="A", employee_code="A-1"))
    second = service.create_person(PersonCreate(first_name="Boris", last_name="B", employee_code="B-1"))

    fetched = service.get_person(first.id)
    people = service.list_people()

    assert fetched.id == first.id
    assert [person.id for person in people] == [first.id, second.id]


def test_update_person_partial_does_not_clear_unsent_fields(session: Session) -> None:
    service = PersonService(session)
    created = service.create_person(
        PersonCreate(first_name="Ana", last_name="Nikolic", employee_code="X-1", department="HR", note="Note")
    )

    updated = service.update_person(created.id, PersonUpdate(first_name="  Ivana  "))

    assert updated.first_name == "Ivana"
    assert updated.last_name == "Nikolic"
    assert updated.full_name == "Ivana Nikolic"
    assert updated.department == "HR"
    assert updated.note == "Note"
    assert updated.employee_code == "X-1"


def test_deactivate_person(session: Session) -> None:
    service = PersonService(session)
    created = service.create_person(PersonCreate(first_name="Petar", last_name="Peric"))

    deactivated = service.deactivate_person(created.id)

    assert deactivated.is_active is False


def test_duplicate_employee_code_raises_validation_error(session: Session) -> None:
    service = PersonService(session)
    service.create_person(PersonCreate(first_name="Ana", last_name="Nikolic", employee_code="E-777"))

    with pytest.raises(ValueError, match="employee_code must be unique"):
        service.create_person(PersonCreate(first_name="Iva", last_name="Ivic", employee_code="E-777"))


def test_update_duplicate_employee_code_raises_validation_error(session: Session) -> None:
    service = PersonService(session)
    first = service.create_person(PersonCreate(first_name="Ana", last_name="Nikolic", employee_code="E-101"))
    second = service.create_person(PersonCreate(first_name="Iva", last_name="Ivic", employee_code="E-202"))

    with pytest.raises(ValueError, match="employee_code must be unique"):
        service.update_person(second.id, PersonUpdate(employee_code=first.employee_code))
