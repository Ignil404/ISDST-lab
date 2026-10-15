# Лабораторные задачи: Юнит-тесты и анализ покрытия кода

**Цель:** написать и запустить юнит-тесты для учебного приложения, измерить покрытие кода и освоить базовые инструменты тестирования в Python.

---

## Требования к реализации

Каждый студент получает **одну** задачу (номер задачи соответствует номеру в журнале). В постановке данной задачи приведён готовый модуль `main.py` с набором функций (без внешних зависимостей, кроме стандартной библиотеки Python 3). Нужно:

1. **Скопировать** приведённый `main.py` в свой репозиторий **без изменения публичного поведения** функций (допускаются мелкие правки стиля/импортов, если они не меняют результат).
2. **Написать юнит-тесты** (предпочтительно `pytest`, допустим модуль `unittest`) для всех публичных функций из `main.py`.
3. **Запустить тесты** и убедиться, что они проходят.
4. **Измерить покрытие** кода (`coverage.py` и/или `pytest-cov`) и добиться **высокого покрытия** заданных функций (ориентир: ≥ 90 % строк модуля `main.py`; идеально — близко к 100 %, если логика это позволяет).
5. Оформить `README.md` с инструкцией: как установить зависимости для тестов, как запустить тесты и как получить отчёт о покрытии.

### Общие правила

- Язык реализации тестов: **Python 3**.
- Тестируемый код — только функции из выданного `main.py` (и при необходимости тонкий слой вызова в тестах). Не усложняйте предметную область сверх постановки.
- Для запуска тестов и покрытия разрешены: `pytest`, `unittest`, `coverage`, `pytest-cov`. Другие сторонние библиотеки в `main.py` **не использовать**.
- Тесты должны проверять не только «счастливый путь», но и граничные случаи, ошибки и исключения (если они предусмотрены в коде).
- Имена тестов и структура файлов — читаемые (`test_*.py` или `tests/`).
- В `README.md` обязательно указать **фамилию и инициалы** и номер/название своей задачи.

### Формат сдачи

Ответ студента — **ссылка** на открытый репозиторий (GitLab / GitHub), в котором есть:

| Файл | Содержание |
|------|------------|
| `main.py` | Выданный модуль с функциями (из своей задачи) |
| `test_*.py` или `tests/` | Юнит-тесты |
| `README.md` | Постановка + **фамилия и инициалы** + как запустить тесты и coverage |
| `requirements.txt` (желательно) | Например: `pytest`, `pytest-cov` |

Пример шапки `README.md`:

```markdown
# Задача N: <название>

**Студент:** Иванов И.И.

<сюда скопирована постановка задачи из этого файла>

## Как запустить тесты
...

## Как получить отчёт о покрытии
...
```

Репозиторий должен быть **публичным** (или доступным по ссылке без запроса доступа). Ссылка отправляется преподавателю.

---

## Список задач

### 1. Калькулятор оценок

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from typing import List


def add_grade(grades: List[float], grade: float) -> List[float]:
    if grade < 0 or grade > 10:
        raise ValueError("grade must be in [0, 10]")
    grades.append(grade)
    return grades


def average(grades: List[float]) -> float:
    if not grades:
        raise ValueError("empty grades")
    return sum(grades) / len(grades)


def max_grade(grades: List[float]) -> float:
    if not grades:
        raise ValueError("empty grades")
    return max(grades)


def min_grade(grades: List[float]) -> float:
    if not grades:
        raise ValueError("empty grades")
    return min(grades)


def count_below(grades: List[float], threshold: float) -> int:
    return sum(1 for g in grades if g < threshold)
```

---

### 2. Список покупок

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from typing import Dict, List, Tuple


def add_item(items: List[Dict[str, float]], name: str, price: float) -> None:
    if price < 0:
        raise ValueError("price must be >= 0")
    items.append({"name": name, "price": price})


def remove_item(items: List[Dict[str, float]], name: str) -> bool:
    for i, item in enumerate(items):
        if item["name"] == name:
            items.pop(i)
            return True
    return False


def total(items: List[Dict[str, float]]) -> float:
    return sum(item["price"] for item in items)


def most_expensive(items: List[Dict[str, float]]) -> Tuple[str, float]:
    if not items:
        raise ValueError("empty list")
    best = max(items, key=lambda x: x["price"])
    return best["name"], best["price"]


def find_by_substring(items: List[Dict[str, float]], query: str) -> List[str]:
    q = query.lower()
    return [item["name"] for item in items if q in item["name"].lower()]
```

---

### 3. Банковский счёт

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from typing import List


class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0) -> None:
        if balance < 0:
            raise ValueError("initial balance must be >= 0")
        self.owner = owner
        self.balance = balance
        self.history: List[str] = []

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("amount must be > 0")
        self.balance += amount
        self.history.append(f"deposit {amount}")
        return self.balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("amount must be > 0")
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount
        self.history.append(f"withdraw {amount}")
        return self.balance

    def transfer_to(self, other: "BankAccount", amount: float) -> None:
        self.withdraw(amount)
        other.deposit(amount)
        self.history.append(f"transfer {amount} to {other.owner}")

    def last_operations(self, n: int) -> List[str]:
        if n < 0:
            raise ValueError("n must be >= 0")
        return self.history[-n:] if n else []
```

---

### 4. Библиотека книг

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from typing import Dict, List, Optional


def add_book(books: Dict[str, dict], title: str, author: str, year: int) -> None:
    if title in books:
        raise ValueError("book already exists")
    books[title] = {"author": author, "year": year, "available": True}


def lend_book(books: Dict[str, dict], title: str) -> None:
    book = books.get(title)
    if book is None:
        raise KeyError("book not found")
    if not book["available"]:
        raise ValueError("already lent")
    book["available"] = False


def return_book(books: Dict[str, dict], title: str) -> None:
    book = books.get(title)
    if book is None:
        raise KeyError("book not found")
    book["available"] = True


def find_by_author(books: Dict[str, dict], author: str) -> List[str]:
    return [t for t, b in books.items() if b["author"].lower() == author.lower()]


def available_titles(books: Dict[str, dict]) -> List[str]:
    return sorted(t for t, b in books.items() if b["available"])
```

---

### 5. Температурный журнал

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from typing import List, Tuple


def add_reading(readings: List[Tuple[str, float]], date: str, temp: float) -> None:
    readings.append((date, temp))


def average_temp(readings: List[Tuple[str, float]]) -> float:
    if not readings:
        raise ValueError("no readings")
    return sum(t for _, t in readings) / len(readings)


def days_above(readings: List[Tuple[str, float]], threshold: float) -> List[str]:
    return [d for d, t in readings if t > threshold]


def coldest_day(readings: List[Tuple[str, float]]) -> Tuple[str, float]:
    if not readings:
        raise ValueError("no readings")
    return min(readings, key=lambda x: x[1])


def hottest_day(readings: List[Tuple[str, float]]) -> Tuple[str, float]:
    if not readings:
        raise ValueError("no readings")
    return max(readings, key=lambda x: x[1])
```

---

### 6. Очередь в поликлинику

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from collections import deque
from typing import Deque, Optional, Tuple


def enqueue(queue: Deque[Tuple[str, int]], name: str, ticket: int) -> None:
    queue.append((name, ticket))


def dequeue(queue: Deque[Tuple[str, int]]) -> Tuple[str, int]:
    if not queue:
        raise IndexError("empty queue")
    return queue.popleft()


def peek(queue: Deque[Tuple[str, int]]) -> Tuple[str, int]:
    if not queue:
        raise IndexError("empty queue")
    return queue[0]


def size(queue: Deque[Tuple[str, int]]) -> int:
    return len(queue)


def position_of(queue: Deque[Tuple[str, int]], name: str) -> Optional[int]:
    for i, (n, _) in enumerate(queue):
        if n == name:
            return i + 1
    return None
```

---

### 7. Учебное расписание дня

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from typing import Dict, List, Optional


def add_lesson(schedule: List[dict], subject: str, start: str, room: str) -> None:
    schedule.append({"subject": subject, "start": start, "room": room})


def remove_by_subject(schedule: List[dict], subject: str) -> bool:
    for i, lesson in enumerate(schedule):
        if lesson["subject"] == subject:
            schedule.pop(i)
            return True
    return False


def find_at_time(schedule: List[dict], start: str) -> Optional[dict]:
    for lesson in schedule:
        if lesson["start"] == start:
            return lesson
    return None


def sorted_by_time(schedule: List[dict]) -> List[dict]:
    return sorted(schedule, key=lambda x: x["start"])


def rooms_used(schedule: List[dict]) -> List[str]:
    return sorted({lesson["room"] for lesson in schedule})
```

---

### 8. Склад товаров

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from typing import Dict, List


def receive(stock: Dict[str, dict], sku: str, name: str, qty: int) -> None:
    if qty <= 0:
        raise ValueError("qty must be > 0")
    if sku in stock:
        stock[sku]["qty"] += qty
    else:
        stock[sku] = {"name": name, "qty": qty}


def issue(stock: Dict[str, dict], sku: str, qty: int) -> None:
    if qty <= 0:
        raise ValueError("qty must be > 0")
    if sku not in stock:
        raise KeyError("unknown sku")
    if stock[sku]["qty"] < qty:
        raise ValueError("not enough stock")
    stock[sku]["qty"] -= qty


def remaining(stock: Dict[str, dict], sku: str) -> int:
    if sku not in stock:
        raise KeyError("unknown sku")
    return stock[sku]["qty"]


def below_threshold(stock: Dict[str, dict], threshold: int) -> List[str]:
    return sorted(sku for sku, item in stock.items() if item["qty"] < threshold)


def total_units(stock: Dict[str, dict]) -> int:
    return sum(item["qty"] for item in stock.values())
```

---

### 9. Игровой рейтинг

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from typing import Dict, List, Tuple


def upsert_player(scores: Dict[str, int], nick: str, points: int) -> None:
    if points < 0:
        raise ValueError("points must be >= 0")
    scores[nick] = points


def top_k(scores: Dict[str, int], k: int) -> List[Tuple[str, int]]:
    if k < 0:
        raise ValueError("k must be >= 0")
    ranked = sorted(scores.items(), key=lambda x: (-x[1], x[0]))
    return ranked[:k]


def find_nick(scores: Dict[str, int], nick: str) -> int:
    if nick not in scores:
        raise KeyError("player not found")
    return scores[nick]


def average_points(scores: Dict[str, int]) -> float:
    if not scores:
        raise ValueError("no players")
    return sum(scores.values()) / len(scores)


def above_or_equal(scores: Dict[str, int], threshold: int) -> List[str]:
    return sorted(n for n, p in scores.items() if p >= threshold)
```

---

### 10. Конвертер валют

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from typing import Dict, List


def set_rate(rates: Dict[str, float], code: str, rate_to_base: float) -> None:
    if rate_to_base <= 0:
        raise ValueError("rate must be > 0")
    rates[code.upper()] = rate_to_base


def convert(rates: Dict[str, float], amount: float, from_code: str, to_code: str) -> float:
    if amount < 0:
        raise ValueError("amount must be >= 0")
    src = from_code.upper()
    dst = to_code.upper()
    if src not in rates or dst not in rates:
        raise KeyError("unknown currency")
    in_base = amount * rates[src]
    return in_base / rates[dst]


def list_currencies(rates: Dict[str, float]) -> List[str]:
    return sorted(rates.keys())


def has_currency(rates: Dict[str, float], code: str) -> bool:
    return code.upper() in rates
```

---

### 11. Управление задачами (TODO)

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from typing import Dict, List


def create_task(tasks: Dict[int, dict], task_id: int, text: str, priority: int) -> None:
    if priority not in (1, 2, 3):
        raise ValueError("priority must be 1..3")
    if task_id in tasks:
        raise ValueError("id exists")
    tasks[task_id] = {"text": text, "priority": priority, "status": "open"}


def close_task(tasks: Dict[int, dict], task_id: int) -> None:
    if task_id not in tasks:
        raise KeyError("task not found")
    tasks[task_id]["status"] = "closed"


def open_tasks(tasks: Dict[int, dict]) -> List[int]:
    return sorted(i for i, t in tasks.items() if t["status"] == "open")


def filter_by_priority(tasks: Dict[int, dict], priority: int) -> List[int]:
    return sorted(i for i, t in tasks.items() if t["priority"] == priority)


def count_closed(tasks: Dict[int, dict]) -> int:
    return sum(1 for t in tasks.values() if t["status"] == "closed")
```

---

### 12. Парковка

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from typing import Dict, Optional


def occupy(spots: Dict[int, Optional[str]], spot: int, plate: str) -> None:
    if spot not in spots:
        raise KeyError("unknown spot")
    if spots[spot] is not None:
        raise ValueError("spot busy")
    spots[spot] = plate


def free_spot(spots: Dict[int, Optional[str]], spot: int) -> None:
    if spot not in spots:
        raise KeyError("unknown spot")
    spots[spot] = None


def find_spot_by_plate(spots: Dict[int, Optional[str]], plate: str) -> Optional[int]:
    for spot, p in spots.items():
        if p == plate:
            return spot
    return None


def free_count(spots: Dict[int, Optional[str]]) -> int:
    return sum(1 for p in spots.values() if p is None)


def init_parking(n: int) -> Dict[int, Optional[str]]:
    if n <= 0:
        raise ValueError("n must be > 0")
    return {i: None for i in range(1, n + 1)}
```

---

### 13. Журнал посещаемости

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from typing import Dict, List


def mark(attendance: Dict[str, List[bool]], student: str, present: bool) -> None:
    if student not in attendance:
        attendance[student] = []
    attendance[student].append(present)


def attendance_percent(attendance: Dict[str, List[bool]], student: str) -> float:
    marks = attendance.get(student)
    if not marks:
        raise ValueError("no marks")
    return 100.0 * sum(1 for m in marks if m) / len(marks)


def truants(attendance: Dict[str, List[bool]], threshold: float) -> List[str]:
    result = []
    for student, marks in attendance.items():
        if not marks:
            continue
        pct = 100.0 * sum(1 for m in marks if m) / len(marks)
        if pct < threshold:
            result.append(student)
    return sorted(result)


def perfect_attendance(attendance: Dict[str, List[bool]]) -> List[str]:
    return sorted(
        s for s, marks in attendance.items() if marks and all(marks)
    )
```

---

### 14. Корзина интернет-магазина

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from typing import Dict


def add_or_update(cart: Dict[str, dict], name: str, price: float, qty: int) -> None:
    if price < 0 or qty <= 0:
        raise ValueError("invalid price or qty")
    if name in cart:
        cart[name]["qty"] += qty
        cart[name]["price"] = price
    else:
        cart[name] = {"price": price, "qty": qty}


def remove_item(cart: Dict[str, dict], name: str) -> bool:
    if name in cart:
        del cart[name]
        return True
    return False


def cart_total(cart: Dict[str, dict]) -> float:
    return sum(item["price"] * item["qty"] for item in cart.values())


def unique_count(cart: Dict[str, dict]) -> int:
    return len(cart)


def set_quantity(cart: Dict[str, dict], name: str, qty: int) -> None:
    if name not in cart:
        raise KeyError("item not found")
    if qty <= 0:
        del cart[name]
    else:
        cart[name]["qty"] = qty
```

---

### 15. Геометрические фигуры

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
import math
from typing import List, Tuple


def circle_area(radius: float) -> float:
    if radius < 0:
        raise ValueError("radius must be >= 0")
    return math.pi * radius * radius


def circle_perimeter(radius: float) -> float:
    if radius < 0:
        raise ValueError("radius must be >= 0")
    return 2 * math.pi * radius


def rect_area(width: float, height: float) -> float:
    if width < 0 or height < 0:
        raise ValueError("sides must be >= 0")
    return width * height


def rect_perimeter(width: float, height: float) -> float:
    if width < 0 or height < 0:
        raise ValueError("sides must be >= 0")
    return 2 * (width + height)


def max_area_shape(shapes: List[Tuple[str, float]]) -> Tuple[str, float]:
    """shapes: list of (type_name, area)."""
    if not shapes:
        raise ValueError("empty shapes")
    return max(shapes, key=lambda x: x[1])
```

---

### 16. Телефонная книга

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from typing import Dict, List, Optional


def add_contact(book: Dict[str, dict], name: str, phone: str, email: str) -> None:
    if name in book:
        raise ValueError("contact exists")
    book[name] = {"phone": phone, "email": email}


def remove_contact(book: Dict[str, dict], name: str) -> bool:
    if name in book:
        del book[name]
        return True
    return False


def find_by_name(book: Dict[str, dict], name: str) -> Optional[dict]:
    return book.get(name)


def find_by_phone_fragment(book: Dict[str, dict], fragment: str) -> List[str]:
    return sorted(n for n, c in book.items() if fragment in c["phone"])


def all_sorted(book: Dict[str, dict]) -> List[str]:
    return sorted(book.keys())
```

---

### 17. Система скидок

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from typing import List


def add_product(order: List[float], price: float) -> None:
    if price < 0:
        raise ValueError("price must be >= 0")
    order.append(price)


def subtotal(order: List[float]) -> float:
    return sum(order)


def apply_coupon(subtotal_value: float, percent: float) -> float:
    if percent < 0 or percent > 100:
        raise ValueError("percent must be in [0, 100]")
    return subtotal_value * (1 - percent / 100.0)


def apply_threshold_discount(subtotal_value: float, threshold: float, percent: float) -> float:
    if subtotal_value >= threshold:
        return apply_coupon(subtotal_value, percent)
    return subtotal_value


def final_price(order: List[float], coupon_percent: float = 0.0, threshold: float = 100.0, threshold_percent: float = 5.0) -> float:
    base = subtotal(order)
    after_coupon = apply_coupon(base, coupon_percent)
    return apply_threshold_discount(after_coupon, threshold, threshold_percent)
```

---

### 18. Тайм-трекер

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from typing import Dict, List, Tuple


def add_activity(log: Dict[str, int], name: str, minutes: int) -> None:
    if minutes < 0:
        raise ValueError("minutes must be >= 0")
    log[name] = log.get(name, 0) + minutes


def total_minutes(log: Dict[str, int]) -> int:
    return sum(log.values())


def top_activity(log: Dict[str, int]) -> Tuple[str, int]:
    if not log:
        raise ValueError("empty log")
    return max(log.items(), key=lambda x: x[1])


def shares_percent(log: Dict[str, int]) -> Dict[str, float]:
    total = total_minutes(log)
    if total == 0:
        return {k: 0.0 for k in log}
    return {k: 100.0 * v / total for k, v in log.items()}


def activities_sorted(log: Dict[str, int]) -> List[Tuple[str, int]]:
    return sorted(log.items(), key=lambda x: (-x[1], x[0]))
```

---

### 19. Голосование

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from typing import Dict, List, Optional, Tuple


def register(candidates: Dict[str, int], name: str) -> None:
    if name in candidates:
        raise ValueError("already registered")
    candidates[name] = 0


def vote(candidates: Dict[str, int], name: str) -> None:
    if name not in candidates:
        raise KeyError("unknown candidate")
    candidates[name] += 1


def leader(candidates: Dict[str, int]) -> Optional[str]:
    if not candidates:
        return None
    best = max(candidates.values())
    leaders = [n for n, v in candidates.items() if v == best]
    if len(leaders) != 1:
        return None  # ничья или пусто по смыслу лидера
    return leaders[0]


def distribution_percent(candidates: Dict[str, int]) -> Dict[str, float]:
    total = sum(candidates.values())
    if total == 0:
        return {n: 0.0 for n in candidates}
    return {n: 100.0 * v / total for n, v in candidates.items()}


def is_tie(candidates: Dict[str, int]) -> bool:
    if len(candidates) < 2:
        return False
    best = max(candidates.values())
    return sum(1 for v in candidates.values() if v == best) > 1
```

---

### 20. Фильмотека

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from typing import Dict, List, Optional


def add_film(films: Dict[str, dict], title: str, year: int, genre: str, rating: float) -> None:
    if rating < 0 or rating > 10:
        raise ValueError("rating must be in [0, 10]")
    films[title] = {"year": year, "genre": genre, "rating": rating}


def by_genre(films: Dict[str, dict], genre: str) -> List[str]:
    return sorted(t for t, f in films.items() if f["genre"].lower() == genre.lower())


def rating_at_least(films: Dict[str, dict], threshold: float) -> List[str]:
    return sorted(t for t, f in films.items() if f["rating"] >= threshold)


def average_rating_by_genre(films: Dict[str, dict], genre: str) -> float:
    selected = [f["rating"] for f in films.values() if f["genre"].lower() == genre.lower()]
    if not selected:
        raise ValueError("no films in genre")
    return sum(selected) / len(selected)


def oldest_film(films: Dict[str, dict]) -> Optional[str]:
    if not films:
        return None
    return min(films.items(), key=lambda x: (x[1]["year"], x[0]))[0]
```

---

### 21. Учёт расходов

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from typing import Dict, List, Tuple


def add_expense(expenses: List[dict], category: str, amount: float, date: str) -> None:
    if amount < 0:
        raise ValueError("amount must be >= 0")
    expenses.append({"category": category, "amount": amount, "date": date})


def sum_period(expenses: List[dict], start: str, end: str) -> float:
    return sum(e["amount"] for e in expenses if start <= e["date"] <= end)


def sum_by_category(expenses: List[dict], category: str) -> float:
    return sum(e["amount"] for e in expenses if e["category"] == category)


def top_category(expenses: List[dict]) -> Tuple[str, float]:
    if not expenses:
        raise ValueError("no expenses")
    totals: Dict[str, float] = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0.0) + e["amount"]
    return max(totals.items(), key=lambda x: x[1])


def categories(expenses: List[dict]) -> List[str]:
    return sorted({e["category"] for e in expenses})
```

---

### 22. Камень-ножницы-бумага (счёт серии)

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from typing import Dict, List, Optional, Tuple

BEATS = {"rock": "scissors", "scissors": "paper", "paper": "rock"}


def round_winner(player: str, computer: str) -> str:
    if player not in BEATS or computer not in BEATS:
        raise ValueError("invalid move")
    if player == computer:
        return "draw"
    if BEATS[player] == computer:
        return "player"
    return "computer"


def update_score(score: Dict[str, int], result: str) -> Dict[str, int]:
    if result not in ("player", "computer", "draw"):
        raise ValueError("invalid result")
    if result != "draw":
        score[result] = score.get(result, 0) + 1
    return score


def series_over(score: Dict[str, int], wins_needed: int) -> Optional[str]:
    if wins_needed <= 0:
        raise ValueError("wins_needed must be > 0")
    if score.get("player", 0) >= wins_needed:
        return "player"
    if score.get("computer", 0) >= wins_needed:
        return "computer"
    return None


def move_stats(history: List[str]) -> Dict[str, int]:
    stats = {"rock": 0, "paper": 0, "scissors": 0}
    for move in history:
        if move not in stats:
            raise ValueError("invalid move in history")
        stats[move] += 1
    return stats
```

---

### 23. Шифр Цезаря (латиница)

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py


def _shift_char(ch: str, k: int) -> str:
    if "a" <= ch <= "z":
        base = ord("a")
        return chr(base + (ord(ch) - base + k) % 26)
    if "A" <= ch <= "Z":
        base = ord("A")
        return chr(base + (ord(ch) - base + k) % 26)
    return ch


def encrypt(text: str, k: int) -> str:
    return "".join(_shift_char(ch, k) for ch in text)


def decrypt(text: str, k: int) -> str:
    return encrypt(text, -k)


def is_reversible(text: str, k: int) -> bool:
    return decrypt(encrypt(text, k), k) == text


def only_letters_shifted(text: str, k: int) -> str:
    """Шифрует, оставляя не-буквы без изменений (то же, что encrypt)."""
    return encrypt(text, k)
```

---

### 24. Матричный калькулятор 2×2

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from typing import List

Matrix = List[List[float]]


def add(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] + b[i][j] for j in range(2)] for i in range(2)]


def multiply(a: Matrix, b: Matrix) -> Matrix:
    result = [[0.0, 0.0], [0.0, 0.0]]
    for i in range(2):
        for j in range(2):
            result[i][j] = a[i][0] * b[0][j] + a[i][1] * b[1][j]
    return result


def transpose(a: Matrix) -> Matrix:
    return [[a[0][0], a[1][0]], [a[0][1], a[1][1]]]


def determinant(a: Matrix) -> float:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def is_square_2x2(a: Matrix) -> bool:
    return len(a) == 2 and all(len(row) == 2 for row in a)
```

---

### 25. Бронирование столиков

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from typing import Dict, List, Optional


def add_table(tables: Dict[int, int], number: int, capacity: int) -> None:
    if capacity <= 0:
        raise ValueError("capacity must be > 0")
    tables[number] = capacity


def book(
    tables: Dict[int, int],
    bookings: Dict[str, dict],
    guest: str,
    time_slot: str,
    guests: int,
) -> int:
    if guests <= 0:
        raise ValueError("guests must be > 0")
    occupied = {
        b["table"]
        for b in bookings.values()
        if b["time"] == time_slot
    }
    candidates = sorted(
        (num, cap) for num, cap in tables.items() if num not in occupied and cap >= guests
    )
    if not candidates:
        raise ValueError("no table available")
    table_num = candidates[0][0]
    bookings[guest] = {"table": table_num, "time": time_slot, "guests": guests}
    return table_num


def cancel(bookings: Dict[str, dict], guest: str) -> bool:
    if guest in bookings:
        del bookings[guest]
        return True
    return False


def free_tables(tables: Dict[int, int], bookings: Dict[str, dict], time_slot: str) -> List[int]:
    occupied = {b["table"] for b in bookings.values() if b["time"] == time_slot}
    return sorted(num for num in tables if num not in occupied)
```

---

### 26. Чат-лог (локальный)

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from typing import Dict, List


def send(messages: List[dict], author: str, text: str, time: str) -> None:
    if not text.strip():
        raise ValueError("empty text")
    messages.append({"author": author, "text": text, "time": time})


def last_n(messages: List[dict], n: int) -> List[dict]:
    if n < 0:
        raise ValueError("n must be >= 0")
    return messages[-n:] if n else []


def by_author(messages: List[dict], author: str) -> List[dict]:
    return [m for m in messages if m["author"] == author]


def search(messages: List[dict], query: str) -> List[dict]:
    q = query.lower()
    return [m for m in messages if q in m["text"].lower()]


def authors(messages: List[dict]) -> List[str]:
    return sorted({m["author"] for m in messages})
```

---

### 27. Учёт электроэнергии

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from typing import Dict, List, Tuple


def add_reading(readings: Dict[str, int], month: str, value: int) -> None:
    if value < 0:
        raise ValueError("value must be >= 0")
    if readings:
        last_month = max(readings.keys())
        if month < last_month:
            raise ValueError("month out of order")
        if value < readings[last_month]:
            raise ValueError("new reading must be >= previous")
    readings[month] = value


def monthly_usage(readings: Dict[str, int]) -> Dict[str, int]:
    months = sorted(readings.keys())
    usage: Dict[str, int] = {}
    for i in range(1, len(months)):
        prev, cur = months[i - 1], months[i]
        usage[cur] = readings[cur] - readings[prev]
    return usage


def average_usage(readings: Dict[str, int]) -> float:
    usage = monthly_usage(readings)
    if not usage:
        raise ValueError("need at least 2 readings")
    return sum(usage.values()) / len(usage)


def max_usage_month(readings: Dict[str, int]) -> Tuple[str, int]:
    usage = monthly_usage(readings)
    if not usage:
        raise ValueError("need at least 2 readings")
    return max(usage.items(), key=lambda x: x[1])
```

---

### 28. Простая боевая система

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
from typing import Dict, List, Tuple


def make_fighter(name: str, hp: int, attack: int, defense: int) -> Dict:
    if hp <= 0 or attack < 0 or defense < 0:
        raise ValueError("invalid stats")
    return {"name": name, "hp": hp, "attack": attack, "defense": defense}


def damage(attacker: Dict, defender: Dict) -> int:
    return max(1, attacker["attack"] - defender["defense"])


def hit(attacker: Dict, defender: Dict) -> int:
    dmg = damage(attacker, defender)
    defender["hp"] -= dmg
    return dmg


def is_alive(fighter: Dict) -> bool:
    return fighter["hp"] > 0


def simulate_fight(a: Dict, b: Dict) -> Tuple[str, List[str]]:
    log: List[str] = []
    round_no = 1
    while is_alive(a) and is_alive(b):
        dmg = hit(a, b)
        log.append(f"R{round_no}: {a['name']} hits {b['name']} for {dmg}, hp={b['hp']}")
        if not is_alive(b):
            return a["name"], log
        dmg = hit(b, a)
        log.append(f"R{round_no}: {b['name']} hits {a['name']} for {dmg}, hp={a['hp']}")
        if not is_alive(a):
            return b["name"], log
        round_no += 1
    # теоретически недостижимо при корректных данных
    return a["name"] if is_alive(a) else b["name"], log
```

---

## Критерии проверки (ориентир)

| Критерий | Что смотрят |
|----------|-------------|
| Полнота тестов | Покрыты публичные функции; есть позитивные и негативные/граничные случаи |
| Запуск | Тесты запускаются одной понятной командой и проходят |
| Покрытие | Есть отчёт coverage; ориентир ≥ 90 % строк `main.py` |
| README | Постановка + ФИО/инициалы + инструкции по тестам и coverage |
| Читаемость | Понятные имена тестов, структура репозитория без лишнего шума |
| Соответствие | В репозитории именно свой номер задачи и выданный `main.py` |
