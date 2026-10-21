"""Конфигурация приложения (переменные окружения)."""

import os

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
CACHE_TTL = int(os.getenv("CACHE_TTL", "30"))
