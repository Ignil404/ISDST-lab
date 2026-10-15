# Лабораторная работа 5: Git — конфликты и удалённые репозитории

**Студент:** Буслович Игнат

**Задача 3:** Конфигурация учебного бота-напоминалки

> Файл `config` (JSON) с текстом напоминаний и расписанием. Ветка `morning-schedule` правит утренние слоты и тексты; ветка `evening-texts` меняет те же ключи под вечерний режим. Разрешите конфликт конфигурации и выложите на GitHub/GitLab.

### Мини-проект

```
bot-reminder/
├── config.json       # Конфигурация бота (JSON)
└── bot.py            # Демо-скрипт на Python (читает config.json, печатает расписание)
```

### Ветки

| Ветка | Назначение |
|-------|------------|
| `lab_5` | Основная ветка лабы (база + результат слияния) |
| `lab_5_morning-schedule` | Утренний режим: сдвиг времени на 07:30, расширение сообщений до 3 шт. |
| `lab_5_evening-schedule` | Вечерний режим: те же ключи `morning`, время 07:00, те же фразы но с другими эмодзи (🌞 🕰️) |

### Сценарий конфликта

Обе ветки изменяют **один и тот же блок** `reminders.morning`:

- **`lab_5_morning-schedule`**: `time: "07:30"`, 3 сообщения с эмодзи 🌅 ☕ 📚
- **`lab_5_evening-schedule`**: `time: "07:00"`, 2 сообщения с эмодзи 🌞 🕰️ (текст из базы, но другие смайлики)

При слиянии `lab_5_evening-schedule` в `lab_5` (после вливания `lab_5_morning-schedule`) возникает **merge-конфликт** в `bot-reminder/config.json`.

### Фрагмент конфликта (маркеры Git)

```json
"morning": {
  "enabled": true,
<<<<<<< HEAD
  "time": "07:30",
  "messages": [
    "🌅 Ранний старт! Проверьте расписание на сегодня.",
    "☕ Выпейте воды и приступайте к делам.",
    "📚 Первая пара через 30 минут — не опоздайте!"
=======
  "time": "07:00",
  "messages": [
    "🌞 Доброе утро! Время просмотреть планы на день.",
    "🕰️ Не забудьте проверить расписание пар."
>>>>>>> lab_5_evening-schedule
  ]
},
```

### Разрешение конфликта

**Решение:** объединено лучшее из обоих вариантов — оставлено утреннее время **07:30** (ранний старт), сообщения взяты из `morning-schedule` (более информативные, 3 пункта), добавлен отдельный вечерний слот **22:00**.

**Итоговый `config.json` (после разрешения):**

```json
{
  "bot_name": "StudyReminderBot",
  "timezone": "Europe/Moscow",
  "reminders": {
    "morning": {
      "enabled": true,
      "time": "07:30",
      "messages": [
        "🌅 Ранний старт! Проверьте расписание на сегодня.",
        "☕ Выпейте воды и приступайте к делам.",
        "📚 Первая пара через 30 минут — не опоздайте!"
      ]
    },
    "evening": {
      "enabled": true,
      "time": "22:00",
      "messages": [
        "🌙 Вечерний режим активирован.",
        "🌃 Настройте уведомления на удобное время."
      ]
    }
  },
  "settings": {
    "notify_via": ["telegram", "email"],
    "language": "ru"
  }
}
```

### Пошаговые команды (история выполнения)

```bash
# 0. Подготовка
cd /Users/ignil/Desktop/ISDST-lab
git checkout -b lab_5

# 1. Базовый коммит
mkdir -p bot-reminder
cp /Users/ignil/Desktop/bot-reminder-lab5/config.json bot-reminder/
cp /Users/ignil/Desktop/bot-reminder-lab5/bot.py bot-reminder/
git add bot-reminder/config.json bot-reminder/bot.py
git commit -m "init: base config and demo script for reminder bot"

# 2. Ветка morning-schedule
git checkout -b lab_5_morning-schedule
cp /Users/ignil/Desktop/bot-reminder-lab5/config_morning-schedule.json bot-reminder/config.json
git add bot-reminder/config.json
git commit -m "feat(morning): shift time to 07:30, extend morning messages"

# 3. Ветка evening-texts
git checkout lab_5
git checkout -b lab_5_evening-schedule
cp /Users/ignil/Desktop/bot-reminder-lab5/config_evening-texts.json bot-reminder/config.json
git add bot-reminder/config.json
git commit -m "feat(evening): shift time, add emoji"

# 4. Первый merge (чистый)
git checkout lab_5
git merge lab_5_morning-schedule --no-ff -m "merge: merge morning-schedule branch"

# 5. Второй merge — КОНФЛИКТ
git merge lab_5_evening-schedule --no-ff
# Auto-merging bot-reminder/config.json
# CONFLICT (content): Merge conflict in bot-reminder/config.json

# 6. Разрешение конфликта
cp /Users/ignil/Desktop/bot-reminder-lab5/config_resolved.json bot-reminder/config.json
git add bot-reminder/config.json
git commit -m "resolve: merge morning and evening modes, resolve conflict"

# 7. Проверка
python3 bot-reminder/bot.py
git log --oneline --graph --all

# 8. Пуш на GitHub
git push -u origin lab_5
git push origin lab_5_morning-schedule lab_5_evening-schedule
```

### История коммитов (граф)

```text
*   005a3ee (HEAD -> lab_5) resolve: merge morning and evening modes, resolve conflict
|\
| * 9109c1d (lab_5_evening-schedule) feat(evening): shift time, add emoji
* |   0892a79 merge: merge morning-schedule branch
|\ \
| |/
|/|
| * 02d8a98 (lab_5_morning-schedule) feat(morning): shift time to 07:30, extend morning messages
|/
* 0c7ca73 init: base config and demo script for reminder bot
```


