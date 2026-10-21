"""Healthcheck: приложение живо и Redis отвечает."""

import redis
from fastapi import APIRouter, HTTPException

from ..redis_client import r

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    try:
        redis_ok = r.ping()
    except redis.RedisError as exc:
        raise HTTPException(status_code=503, detail=f"Redis недоступен: {exc}")
    return {"status": "ok", "redis": redis_ok}
