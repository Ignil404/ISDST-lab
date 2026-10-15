"""
Демонстрационный скрипт бота-напоминалки.
Читает config.json и выводит расписание напоминаний в консоль.
"""

import json
from pathlib import Path
from datetime import datetime


CONFIG_PATH = Path(__file__).parent / "config.json"


def load_config() -> dict:
    """Загружает конфигурацию из JSON-файла."""
    with CONFIG_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def format_reminder(name: str, data: dict) -> str:
    """Форматирует одно напоминание для вывода."""
    if not data.get("enabled", False):
        return f"  ⏭ {name}: отключено"
    time_str = data.get("time", "??:??")
    messages = data.get("messages", [])
    lines = [f"  ⏰ {name} — {time_str}"]
    for i, msg in enumerate(messages, 1):
        lines.append(f"    {i}. {msg}")
    return "\n".join(lines)


def main() -> None:
    config = load_config()

    print(f"🤖 {config['bot_name']} — демо-запуск")
    print(f"🌍 Часовой пояс: {config['timezone']}")
    print(f"🔔 Каналы уведомлений: {', '.join(config['settings']['notify_via'])}")
    print(f"🌐 Язык: {config['settings']['language']}")
    print("\n📅 Расписание напоминаний:")

    for name, data in config["reminders"].items():
        print(format_reminder(name, data))

    print(f"\n✅ Конфиг загружен из {CONFIG_PATH.name}")
    print(f"🕐 Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()