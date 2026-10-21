"""Записи пациентов: бронь слота, список на день, очередь, отмена."""

import uuid

import redis
from fastapi import APIRouter, HTTPException, Query

from ..redis_client import r
from ..schemas import AppointmentCreate

router = APIRouter(tags=["appointments"])


@router.post("/appointments", status_code=201)
def create_appointment(body: AppointmentCreate) -> dict:
    slot_key = f"slot:{body.slot_id}"
    slot = r.hgetall(slot_key)
    if not slot:
        raise HTTPException(status_code=404, detail="Слот не найден")

    with r.pipeline() as pipe:
        while True:
            try:
                pipe.watch(slot_key)
                if pipe.hget(slot_key, "status") != "free":
                    pipe.unwatch()
                    raise HTTPException(status_code=409, detail="Слот уже занят")
                appt_id = str(uuid.uuid4())
                pipe.multi()
                pipe.hset(slot_key, "status", "booked")
                pipe.hset(
                    f"appointment:{appt_id}",
                    mapping={
                        "id": appt_id,
                        "slot_id": body.slot_id,
                        "doctor": slot["doctor"],
                        "date": slot["date"],
                        "time": slot["time"],
                        "patient": body.patient,
                        "complaint": body.complaint or "",
                        "status": "booked",
                    },
                )
                pipe.sadd(f"appts:date:{slot['date']}", appt_id)
                pipe.lpush("queue:appointments", appt_id)
                pipe.delete(f"cache:slots:{slot['date']}")
                pipe.execute()
                break
            except redis.WatchError:
                continue

    return {
        "id": appt_id,
        "slot_id": body.slot_id,
        "doctor": slot["doctor"],
        "date": slot["date"],
        "time": slot["time"],
        "patient": body.patient,
        "status": "booked",
    }


@router.get("/appointments")
def list_appointments(date: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$")) -> dict:
    appts = []
    for aid in r.smembers(f"appts:date:{date}"):
        data = r.hgetall(f"appointment:{aid}")
        if data:
            appts.append(data)
    appts.sort(key=lambda a: a.get("time", ""))
    return {"date": date, "appointments": appts}


@router.get("/queue")
def queue(size: int = Query(10, ge=1, le=100)) -> dict:
    """Последние N записей из очереди (Redis LIST)."""
    ids = r.lrange("queue:appointments", 0, size - 1)
    return {"queue": [r.hgetall(f"appointment:{i}") for i in ids]}


@router.delete("/appointments/{appt_id}")
def cancel_appointment(appt_id: str) -> dict:
    key = f"appointment:{appt_id}"
    appt = r.hgetall(key)
    if not appt:
        raise HTTPException(status_code=404, detail="Запись не найдена")

    r.hset(key, "status", "cancelled")
    r.hset(f"slot:{appt['slot_id']}", "status", "free")
    r.srem(f"appts:date:{appt['date']}", appt_id)
    r.delete(f"cache:slots:{appt['date']}")
    return {"id": appt_id, "status": "cancelled", "freed_slot": appt["slot_id"]}