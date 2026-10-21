"""Pydantic-схемы запросов."""

from typing import Optional

from pydantic import BaseModel, Field


class SlotCreate(BaseModel):
    doctor: str = Field(..., min_length=2, example="Иванов И.И.")
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", example="2026-10-21")
    time: str = Field(..., pattern=r"^\d{2}:\d{2}$", example="09:30")


class AppointmentCreate(BaseModel):
    slot_id: str = Field(..., example="9f1b0c2e-...")
    patient: str = Field(..., min_length=2, example="Петров П.П.")
    complaint: Optional[str] = Field(None, example="Головная боль")
