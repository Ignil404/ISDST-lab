"""Слоты приёма: создание и список на день (с кэшем в Redis)."""

import uuid

from fastapi import APIRouter, Query

from ..config import CACHE_TTL
from ..redis_client import r
from ..schemas import SlotCreate

router = APIRouter(prefix="/slots", tags=["slots"])


@router.post("", status_code=201)
def create_slot(body: SlotCreate) -> dict:
    slot_id = str(uuid.uuid4())
    r.hset(
        f"slot:{slot_id}",
        mapping={
            "id": slot_id,
            "doctor": body.doctor,
            "date": body.date,
            "time": body.time,
            "status": "free",
        },
    )
    r.sadd(f"slots:date:{body.date}", slot_id)
    # создание слота делает устаревший кэш дня бесполезным
    r.delete(f"cache:slots:{body.date}")
    return {"id": slot_id, **body.model_dump(), "status": "free"}


@router.get("")
def list_slots(date: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$")) -> dict:
    """Список слотов на день (с кэшированием в Redis)."""
    cache_key = f"cache:slots:{date}"
    cached = bool(r.get(cache_key))
    slots = _slots_for_day(date)
    if not cached:
        r.set(cache_key, str(len(slots)), ex=CACHE_TTL)
    return {"date": date, "cached": cached, "slots": slots}


def _slots_for_day(day: str) -> list[dict]:
    slots = []
    for sid in r.smembers(f"slots:date:{day}"):
        data = r.hgetall(f"slot:{sid}")
        if data:
            slots.append(data)
    slots.sort(key=lambda s: s.get("time", ""))
    return slots
