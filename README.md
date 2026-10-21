# Задача 3: Запись к врачу в поликлинике

**Студент:** Буслович Игнат

> **Постановка.** Сервис слотов приёма + Redis (кэш/очередь записей). Compose: `app` и `redis`.
> Операции: создать запись, список на день. Healthcheck у приложения.

## Архитектура

| Сервис | Образ | Назначение |
|--------|-------|------------|
| `app`  | свой (`Dockerfile`, python:3.12-slim + FastAPI) | REST API слотов приёма и записей пациентов |
| `redis`| официальный `redis:7-alpine` | слоты/записи (хэши), кэш дня (TTL), очередь новых записей (LIST) |

## Структура кода

```
lab_7/
├── Dockerfile
├── compose.yaml
├── .env.example
├── README.md
└── app/
    ├── main.py            # точка входа: FastAPI + подключение роутеров
    ├── config.py          # переменные окружения (REDIS_URL, CACHE_TTL)
    ├── redis_client.py    # единый клиент Redis
    ├── schemas.py         # pydantic-схемы запросов
    ├── requirements.txt
    └── routers/
        ├── health.py          # GET /health
        ├── slots.py           # POST /slots, GET /slots
        └── appointments.py    # POST/GET/DELETE /appointments, GET /queue
```

## Раскладка данных в Redis

| Ключ | Тип | Содержимое |
|------|-----|------------|
| `slot:{id}` | hash | слот: doctor, date, time, status (`free`/`booked`) |
| `slots:date:{YYYY-MM-DD}` | set | id слотов дня |
| `appointment:{id}` | hash | запись: patient, complaint, doctor, date, time, status |
| `appts:date:{YYYY-MM-DD}` | set | id записей дня |
| `queue:appointments` | list | очередь созданных записей (LIFO, последние N) |
| `cache:slots:{YYYY-MM-DD}` | string | кэш списка слотов на день, TTL = `CACHE_TTL` |

## Запуск

```bash
cd lab_7
cp .env.example .env
docker compose up --build
```

Приложение: http://localhost:8000 (`APP_PORT` в `.env`).

## API

| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/health` | healthcheck: приложение + доступность Redis |
| `POST` | `/slots` | создать слот приёма `{doctor, date, time}` |
| `GET` | `/slots?date=YYYY-MM-DD` | список слотов на день (с кэшем в Redis) |
| `POST` | `/appointments` | записать пациента на слот `{slot_id, patient, complaint}` |
| `GET` | `/appointments?date=YYYY-MM-DD` | список записей на день |
| `GET` | `/queue?size=10` | последние N записей из очереди Redis |
| `DELETE` | `/appointments/{id}` | отменить запись, освободить слот |

## Проверка

```bash
# 1. healthcheck приложения
curl -s http://localhost:8000/health
# {"status":"ok","redis":true}

# 2. создать два слота
curl -s -X POST http://localhost:8000/slots \
  -H 'Content-Type: application/json' \
  -d '{"doctor":"Иванов И.И.","date":"2026-10-21","time":"09:30"}'
curl -s -X POST http://localhost:8000/slots \
  -H 'Content-Type: application/json' \
  -d '{"doctor":"Иванов И.И.","date":"2026-10-21","time":"10:00"}'

# 3. список слотов на день (второй вызов ниже вернёт "cached":true)
curl -s 'http://localhost:8000/slots?date=2026-10-21'

# 4. записать пациента (подставить id слота из шага 3)
curl -s -X POST http://localhost:8000/appointments \
  -H 'Content-Type: application/json' \
  -d '{"slot_id":"<SLOT_ID>","patient":"Петров П.П.","complaint":"Головная боль"}'

# 5. повторная запись на тот же слот -> 409 Conflict
# 6. список записей на день
curl -s 'http://localhost:8000/appointments?date=2026-10-21'

# 7. очередь новых записей в Redis
curl -s 'http://localhost:8000/queue?size=5'

# 8. отмена записи и освобождение слота
curl -s -X DELETE http://localhost:8000/appointments/<APPOINTMENT_ID>

# 9. логи и статус контейнеров
docker compose logs -f app
docker compose ps
```

## Остановка

```bash
docker compose down          # данные Redis живут в томе redis-data
docker compose down -v       # вместе с томом
```
