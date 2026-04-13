"""Pydantic schemas for Person business flows."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class PersonCreate(BaseModel):
    employee_code: str | None = None
    first_name: str
    last_name: str
    department: str | None = None
    note: str | None = None
    is_active: bool = True


class PersonUpdate(BaseModel):
    employee_code: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    department: str | None = None
    note: str | None = None
    is_active: bool | None = None


class PersonRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_code: str | None
    first_name: str
    last_name: str
    full_name: str
    department: str | None
    note: str | None
    is_active: bool
