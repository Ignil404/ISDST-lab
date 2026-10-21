"""Сервис записи к врачу в поликлинике.

Хранилище — Redis:
  * слоты приёма  — хэши `slot:{id}` + индекс по дню `slots:date:{YYYY-MM-DD}`;
  * записи        — хэши `appointment:{id}` + индекс по дню `appts:date:{YYYY-MM-DD}`;
  * новые записи  — очередь `queue:appointments` (Redis LIST);
  * кэш списка слотов на день — `cache:slots:{YYYY-MM-DD}` с TTL.
"""

from fastapi import FastAPI

from .routers import appointments, health, slots

app = FastAPI(title="Поликлиника: запись к врачу", version="1.0")

app.include_router(health.router)
app.include_router(slots.router)
app.include_router(appointments.router)
