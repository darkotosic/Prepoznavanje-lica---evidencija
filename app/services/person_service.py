"""Business service orchestration for Person CRUD use-cases."""

from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.person_repository import PersonRepository
from app.schemas.person import PersonCreate, PersonRead, PersonUpdate


class PersonService:
    """Service layer responsible for validation and Person workflows."""

    def __init__(self, session: Session) -> None:
        self._session = session
        self._repository = PersonRepository(session)

    def create_person(self, payload: PersonCreate) -> PersonRead:
        prepared = self._prepare_create_payload(payload)
        employee_code = prepared.get("employee_code")
        if employee_code and self._repository.get_by_employee_code(employee_code):
            raise ValueError("employee_code must be unique")

        prepared["full_name"] = self._build_full_name(prepared["first_name"], prepared["last_name"])
        try:
            person = self._repository.create(data=prepared)
            self._session.commit()
        except IntegrityError as exc:
            self._session.rollback()
            raise ValueError("employee_code must be unique") from exc

        return PersonRead.model_validate(person)

    def get_person(self, person_id: int) -> PersonRead:
        person = self._repository.get_by_id(person_id)
        if person is None:
            raise ValueError("Person not found")
        return PersonRead.model_validate(person)

    def list_people(self) -> list[PersonRead]:
        people = self._repository.list_all()
        return [PersonRead.model_validate(person) for person in people]

    def update_person(self, person_id: int, payload: PersonUpdate) -> PersonRead:
        person = self._repository.get_by_id(person_id)
        if person is None:
            raise ValueError("Person not found")

        update_data = self._prepare_update_payload(payload)

        if "employee_code" in update_data and update_data["employee_code"] is not None:
            existing = self._repository.get_by_employee_code(update_data["employee_code"])
            if existing is not None and existing.id != person_id:
                raise ValueError("employee_code must be unique")

        first_name = update_data.get("first_name", person.first_name)
        last_name = update_data.get("last_name", person.last_name)
        self._validate_name(first_name, field_name="first_name")
        self._validate_name(last_name, field_name="last_name")

        if "first_name" in update_data or "last_name" in update_data:
            update_data["full_name"] = self._build_full_name(first_name, last_name)

        if not update_data:
            return PersonRead.model_validate(person)

        try:
            updated = self._repository.update(person, data=update_data)
            self._session.commit()
        except IntegrityError as exc:
            self._session.rollback()
            raise ValueError("employee_code must be unique") from exc

        return PersonRead.model_validate(updated)

    def deactivate_person(self, person_id: int) -> PersonRead:
        person = self._repository.get_by_id(person_id)
        if person is None:
            raise ValueError("Person not found")

        deactivated = self._repository.deactivate(person)
        self._session.commit()
        return PersonRead.model_validate(deactivated)

    def _prepare_create_payload(self, payload: PersonCreate) -> dict:
        data = payload.model_dump()
        data["first_name"] = self._normalize_required_name(data.get("first_name"), field_name="first_name")
        data["last_name"] = self._normalize_required_name(data.get("last_name"), field_name="last_name")
        data["employee_code"] = self._normalize_optional_string(data.get("employee_code"))
        data["department"] = self._normalize_optional_string(data.get("department"))
        data["note"] = self._normalize_optional_string(data.get("note"))
        data["is_active"] = data.get("is_active", True)
        return data

    def _prepare_update_payload(self, payload: PersonUpdate) -> dict:
        raw = payload.model_dump(exclude_unset=True)
        data: dict = {}

        if "first_name" in raw:
            data["first_name"] = self._normalize_required_name(raw.get("first_name"), field_name="first_name")
        if "last_name" in raw:
            data["last_name"] = self._normalize_required_name(raw.get("last_name"), field_name="last_name")
        if "employee_code" in raw:
            data["employee_code"] = self._normalize_optional_string(raw.get("employee_code"))
        if "department" in raw:
            data["department"] = self._normalize_optional_string(raw.get("department"))
        if "note" in raw:
            data["note"] = self._normalize_optional_string(raw.get("note"))
        if "is_active" in raw:
            data["is_active"] = raw.get("is_active")

        return data

    @staticmethod
    def _normalize_optional_string(value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    def _normalize_required_name(self, value: str | None, *, field_name: str) -> str:
        normalized = self._normalize_optional_string(value)
        self._validate_name(normalized, field_name=field_name)
        return normalized  # type: ignore[return-value]

    @staticmethod
    def _validate_name(value: str | None, *, field_name: str) -> None:
        if value is None or not value.strip():
            raise ValueError(f"{field_name} is required")

    @staticmethod
    def _build_full_name(first_name: str, last_name: str) -> str:
        return f"{first_name} {last_name}".strip()
