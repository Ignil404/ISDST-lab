# Лабораторные задачи: Юнит-тесты и BDD-сценарии

**Цель:** написать классические юнит-тесты и BDD-сценарии (Gherkin) для простых функций предметной области, а также встроить тестирование в процесс разработки (подход test-first / red–green–refactor).

---

## Требования к реализации

Каждый студент получает **одну** задачу (номер задачи соответствует номеру в журнале). Нужно выполнить **два вида** тестов по своей постановке и показать, что тестирование встроено в разработку:

1. **Юнит-тесты** — классические тесты на Python (`pytest` или `unittest`) для функций/модуля из постановки.
2. **BDD-сценарии** — описания поведения на языке Gherkin (файлы `.feature`) и их привязка к шагам через `pytest-bdd` **или** `behave` (на выбор студента).
3. **Интеграция в процесс разработки** — в `README.md` кратко (по шагам) показать цикл **red → green → refactor** (или test-first): что падало до реализации, что стало зелёным, что улучшили после.

В каждой задаче ниже либо дан **готовый каркас функций** (stubs / минимальная реализация), либо явно сказано, что нужно **реализовать функции самостоятельно**, а затем покрыть их обоими видами тестов. Подход внутри задачи единый и конкретный — следуйте тексту своей постановки.

### Общие правила

- Язык: **Python 3**.
- Для BDD допустимы: `pytest-bdd` или `behave`; для юнит-тестов — `pytest` / `unittest`.
- Сценарии Gherkin — на **русском или английском** (единообразно в рамках репозитория); шаги должны реально выполняться, а не быть «документацией без прогона».
- Минимум: **не менее 3** feature-сценариев (или эквивалентных сценариев в одном/нескольких `.feature`) и **не менее 5** юнит-тестов (отдельные test-функции/методы).
- Покрыть основной функционал постановки: успешные случаи, граничные условия и ошибки (где они описаны).
- В `README.md` обязательно: **фамилия и инициалы**, номер задачи, команды запуска юнит-тестов и BDD, краткое описание red–green–refactor на примере 1–2 функций.

### Формат сдачи

Ответ студента — **ссылка** на открытый репозиторий (GitLab / GitHub), в котором есть:

| Файл / каталог | Содержание |
|----------------|------------|
| `main.py` (или пакет модулей) | Реализация функций по постановке |
| `test_*.py` / `tests/` | Юнит-тесты |
| `features/` (или `*.feature`) | BDD-сценарии Gherkin + step definitions |
| `README.md` | Постановка + **ФИО/инициалы** + запуск тестов + red–green–refactor |
| `requirements.txt` (желательно) | `pytest`, `pytest-bdd` или `behave` и т.п. |

Пример шапки `README.md`:

```markdown
# Задача N: <название>

**Студент:** Иванов И.И.

<сюда скопирована постановка задачи из этого файла>

## Запуск юнит-тестов
...

## Запуск BDD
...

## Red–Green–Refactor (кратко)
...
```

Репозиторий должен быть **публичным** (или доступным по ссылке без запроса доступа). Ссылка отправляется преподавателю.

---

## Список задач

### 1. Валидатор пароля

Реализуйте функции и покройте их юнит-тестами и BDD.

```python
# main.py — реализуйте тела функций
def is_long_enough(password: str, min_len: int = 8) -> bool:
    ...

def has_digit(password: str) -> bool:
    ...

def has_upper_and_lower(password: str) -> bool:
    ...

def is_strong(password: str) -> bool:
    """Сильный: длина, цифра, верхний и нижний регистр."""
    ...
```

BDD: сценарии «слабый / сильный пароль», отсутствие цифры, слишком короткий.

---

### 2. Нормализация ФИО

Реализуйте и протестируйте:

```python
# main.py
def normalize_spaces(full_name: str) -> str:
    """Убрать лишние пробелы по краям и внутри."""
    ...

def capitalize_name(full_name: str) -> str:
    """Каждое слово с заглавной буквы после normalize_spaces."""
    ...

def initials(full_name: str) -> str:
    """Например: 'Иванов Иван' -> 'И.И.' (первая буква каждого слова)."""
    ...
```

BDD: пустая строка, несколько пробелов, уже нормализованное ФИО.

---

### 3. Калькулятор скидки

Реализуйте:

```python
# main.py
def apply_percent(price: float, percent: float) -> float:
    ...

def apply_fixed(price: float, amount: float) -> float:
    ...

def best_discount(price: float, percent: float, amount: float) -> float:
    """Вернуть минимальную итоговую цену из двух способов; цена не ниже 0."""
    ...
```

Ошибки: отрицательная цена / процент вне [0, 100] / отрица round fixed — через `ValueError`.  
BDD: процент выгоднее fixed, fixed выгоднее, граничные 0 и 100 %.

---

### 4. Парсер диапазона дат (строки YYYY-MM-DD)

Реализуйте:

```python
# main.py
def is_valid_date(s: str) -> bool:
    ...

def days_between(start: str, end: str) -> int:
    """Число дней между датами (end - start), допускается 0; если end < start — ValueError."""
    ...

def in_range(date: str, start: str, end: str) -> bool:
    ...
```

Используйте `datetime.date` из стандартной библиотеки.  
BDD: валидная/невалидная дата, дата внутри/вне диапазона.

---

### 5. Корзина: сумма и НДС

Реализуйте:

```python
# main.py
def line_total(price: float, qty: int) -> float:
    ...

def cart_subtotal(lines: list[tuple[float, int]]) -> float:
    ...

def with_vat(subtotal: float, vat_percent: float = 20.0) -> float:
    ...
```

BDD: пустая корзина, одна позиция, несколько позиций, НДС 0 % и 20 %.

---

### 6. Игровые очки и уровни

Реализуйте:

```python
# main.py
LEVELS = [(0, "bronze"), (100, "silver"), (500, "gold"), (1000, "platinum")]

def add_points(current: int, gained: int) -> int:
    ...

def level_for(points: int) -> str:
    ...

def points_to_next(points: int) -> int | None:
    """Сколько очков до следующего уровня; None если максимальный."""
    ...
```

BDD: набор очков с повышением уровня, уже максимальный уровень.

---

### 7. Фильтр списка чисел

Реализуйте:

```python
# main.py
def only_positive(nums: list[float]) -> list[float]:
    ...

def in_bounds(nums: list[float], low: float, high: float) -> list[float]:
    ...

def unique_sorted(nums: list[float]) -> list[float]:
    ...
```

BDD: пустой список, дубликаты, границы включительно.

---

### 8. Учебный «статус зачёта»

Реализуйте:

```python
# main.py
def grade_status(score: float) -> str:
    """< 0 или > 100 — ValueError; < 40 fail; < 70 pass; иначе excellent."""
    ...

def can_retake(score: float, attempts: int, max_attempts: int = 3) -> bool:
    """Можно пересдать, если fail и attempts < max_attempts."""
    ...
```

BDD: fail/pass/excellent, исчерпаны попытки пересдачи.

---

### 9. Учёт книг в читальном зале

Дан каркас — **допишите реализацию** и покройте тестами:

```python
# main.py
def add_book(shelf: dict[str, int], title: str, copies: int = 1) -> None:
    if copies <= 0:
        raise ValueError("copies must be > 0")
    shelf[title] = shelf.get(title, 0) + copies


def borrow(shelf: dict[str, int], title: str) -> None:
    # уменьшить на 1; KeyError / ValueError при отсутствии / нулевом остатке
    ...


def available(shelf: dict[str, int], title: str) -> int:
    ...
```

BDD: выдача последней копии, попытка взять отсутствующую книгу.

---

### 10. Таймер помодоро (минуты)

Реализуйте:

```python
# main.py
def work_session(minutes: int = 25) -> int:
    if minutes <= 0:
        raise ValueError("minutes must be > 0")
    return minutes


def short_break(minutes: int = 5) -> int:
    ...


def long_break(cycle: int, every: int = 4, minutes: int = 15) -> int:
    """Каждый every-й цикл — long break, иначе short (5). cycle начиная с 1."""
    ...
```

BDD: 1–3 циклы — короткий перерыв, 4-й — длинный.

---

### 11. Конвертер температуры

Реализуйте:

```python
# main.py
def c_to_f(c: float) -> float:
    ...

def f_to_c(f: float) -> float:
    ...

def c_to_k(c: float) -> float:
    """Ниже абсолютного нуля (−273.15 °C) — ValueError."""
    ...
```

BDD: точка замерзания/кипения воды, ошибка ниже абсолютного нуля.

---

### 12. Проверка ISBN-10 (упрощённо)

Реализуйте проверку контрольной суммы ISBN-10 (цифры и возможный `X` в конце):

```python
# main.py
def clean_isbn(raw: str) -> str:
    """Убрать дефисы и пробелы."""
    ...

def is_valid_isbn10(raw: str) -> bool:
    ...
```

BDD: валидный ISBN, неверная контрольная цифра, неверная длина.

---

### 13. Очередь сообщений

Реализуйте обёртку над списком:

```python
# main.py
def push(queue: list[str], msg: str) -> None:
    ...

def pop(queue: list[str]) -> str:
    ...

def peek(queue: list[str]) -> str:
    ...

def is_empty(queue: list[str]) -> bool:
    ...
```

`pop`/`peek` на пустой очереди — `IndexError`.  
BDD: FIFO-порядок, пустая очередь.

---

### 14. Подсчёт слов в тексте

Реализуйте:

```python
# main.py
def tokenize(text: str) -> list[str]:
    """Слова в нижнем регистре; разделители — пробелы и ,.!?;:"""
    ...

def word_count(text: str) -> int:
    ...

def top_word(text: str) -> str | None:
    """Самое частое слово; при ничьей — лексикографически меньшее; пустой текст — None."""
    ...
```

BDD: пустой текст, знаки препинания, ничья по частоте.

---

### 15. Бюджет на месяц

Реализуйте:

```python
# main.py
def remaining(budget: float, spent: float) -> float:
    ...

def overspent(budget: float, spent: float) -> bool:
    ...

def recommend_daily(budget: float, spent: float, days_left: int) -> float:
    """Сколько можно тратить в день из остатка; days_left <= 0 — ValueError."""
    ...
```

BDD: в бюджете / перерасход, нулевой остаток.

---

### 16. Расписание слотов

Реализуйте:

```python
# main.py
def parse_slot(slot: str) -> tuple[int, int]:
    """'09:30' -> (9, 30); неверный формат — ValueError."""
    ...

def duration_minutes(start: str, end: str) -> int:
    ...

def overlaps(a_start: str, a_end: str, b_start: str, b_end: str) -> bool:
    """Полуинтервалы [start, end)."""
    ...
```

BDD: пересекающиеся и непересекающиеся слоты, end <= start — ошибка в `duration_minutes`.

---

### 17. Система тегов

Реализуйте:

```python
# main.py
def normalize_tag(tag: str) -> str:
    """trim + lower; пустой после trim — ValueError."""
    ...

def add_tag(tags: set[str], tag: str) -> None:
    ...

def has_tag(tags: set[str], tag: str) -> bool:
    ...

def common_tags(a: set[str], b: set[str]) -> set[str]:
    ...
```

BDD: добавление дубликата (множество), пересечение тегов.

---

### 18. Игровой инвентарь

Реализуйте:

```python
# main.py
def add_item(inv: dict[str, int], item: str, qty: int = 1) -> None:
    ...

def remove_item(inv: dict[str, int], item: str, qty: int = 1) -> None:
    ...

def count(inv: dict[str, int], item: str) -> int:
    ...

def is_full(inv: dict[str, int], capacity: int) -> bool:
    """Сумма qty >= capacity."""
    ...
```

BDD: удаление больше, чем есть — `ValueError`; заполнение до capacity.

---

### 19. Оценка сложности задачи (story points)

Реализуйте:

```python
# main.py
ALLOWED = {1, 2, 3, 5, 8, 13}

def is_allowed(points: int) -> bool:
    ...

def sum_sprint(points_list: list[int]) -> int:
    """Если есть значение вне ALLOWED — ValueError."""
    ...

def within_capacity(points_list: list[int], capacity: int) -> bool:
    ...
```

BDD: валидный спринт, недопустимые points, перегруз capacity.

---

### 20. Проверка скобочной последовательности

Реализуйте только круглые скобки `()`:

```python
# main.py
def is_balanced(s: str) -> bool:
    ...

def first_mismatch_index(s: str) -> int | None:
    """Индекс первой лишней ')' или None, если до конца всё согласовано;
    если не хватает закрывающих — вернуть len(s)."""
    ...
```

BDD: сбалансированная строка, лишняя закрывающая, нехватка закрывающих.

---

### 21. Мини-CRM: статус сделки

Реализуйте конечный автомат статусов:

```python
# main.py
TRANSITIONS = {
    "new": {"qualified", "lost"},
    "qualified": {"proposal", "lost"},
    "proposal": {"won", "lost"},
    "won": set(),
    "lost": set(),
}

def can_transit(current: str, new: str) -> bool:
    ...

def transit(current: str, new: str) -> str:
    """Если нельзя — ValueError."""
    ...
```

BDD: успешный путь new→…→won, запрещённый переход, терминальные статусы.

---

### 22. Расчёт BMI

Реализуйте:

```python
# main.py
def bmi(weight_kg: float, height_m: float) -> float:
    ...

def bmi_category(weight_kg: float, height_m: float) -> str:
    """underweight < 18.5; normal < 25; overweight < 30; иначе obesity."""
    ...
```

Некорректные вес/рост ≤ 0 — `ValueError`.  
BDD: все четыре категории + ошибка входных данных.

---

### 23. Локальный кэш с TTL (упрощённо)

Реализуйте словарь вида `key -> (value, expire_at_ts)`:

```python
# main.py
def set_item(cache: dict, key: str, value: str, now: float, ttl: float) -> None:
    ...

def get_item(cache: dict, key: str, now: float) -> str | None:
    """None если нет или истекло; просроченное удалить."""
    ...

def size(cache: dict, now: float) -> int:
    """Число ещё живых записей (с очисткой просроченных)."""
    ...
```

Время передаётся параметром `now` (удобно тестировать без `time.time`).  
BDD: попадание в кэш, истечение TTL, отсутствие ключа.

---

### 24. Генератор инициалов проекта (slug)

Реализуйте:

```python
# main.py
def slugify(title: str) -> str:
    """lower, пробелы → '-', только a-z0-9-; подряд идущие '-' схлопнуть."""
    ...

def unique_slug(title: str, existing: set[str]) -> str:
    """Если slug занят — добавлять -2, -3, ..."""
    ...
```

BDD: кириллица/знаки удаляются или дают пустой slug (опишите правило в README и закрепите тестами), коллизии имён.

---

### 25. Статистика оценок группы

Реализуйте:

```python
# main.py
def mean(scores: list[float]) -> float:
    ...

def median(scores: list[float]) -> float:
    ...

def passed_count(scores: list[float], threshold: float = 4.0) -> int:
    ...
```

Пустой список для mean/median — `ValueError`.  
BDD: чётное/нечётное число оценок для медианы, порог сдачи.

---

### 26. Маршрут курьера (расстояние)

Реализуйте:

```python
# main.py
def segment_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Евклидово расстояние."""
    ...

def path_length(points: list[tuple[float, float]]) -> float:
    """Сумма сегментов; меньше 2 точек — 0.0."""
    ...

def nearest(origin: tuple[float, float], candidates: list[tuple[float, float]]) -> tuple[float, float]:
    """Ближайшая точка; пустой candidates — ValueError."""
    ...
```

BDD: один сегмент, ломаная из нескольких точек, выбор nearest.

---

### 27. Учебный автомат выдачи сдачи

Реализуйте жадную выдачу монетами `[10, 5, 2, 1]`:

```python
# main.py
COINS = [10, 5, 2, 1]

def make_change(amount: int) -> dict[int, int]:
    """Сколько монет каждого номинала; amount < 0 — ValueError."""
    ...

def coins_count(amount: int) -> int:
    ...
```

BDD: amount = 0, типичные суммы, отрицательная сумма.

---

### 28. Правила доступа к документу

Реализуйте простую ACL:

```python
# main.py
def can_read(owner: str, acl: dict[str, set[str]], user: str) -> bool:
    """Читать может owner или user из acl['read'] / acl['write'] / acl['admin']."""
    ...

def can_write(owner: str, acl: dict[str, set[str]], user: str) -> bool:
    """Писать: owner, write или admin."""
    ...

def grant(acl: dict[str, set[str]], role: str, user: str) -> None:
    """role in {'read','write','admin'}; иначе ValueError."""
    ...
```

BDD: владелец, пользователь только read, попытка write без прав, grant + повторная проверка.

---

## Критерии проверки (ориентир)

| Критерий | Что смотрят |
|----------|-------------|
| Юнит-тесты | ≥ 5 осмысленных тестов; проверяют функции постановки, включая границы/ошибки |
| BDD | Есть `.feature` + рабочие шаги; ≥ 3 сценария; прогон успешен |
| Связка | Юнит и BDD согласованы с одной реализацией `main.py` |
| Процесс | В README виден red–green–refactor / test-first на конкретном примере |
| README | Постановка + ФИО/инициалы + команды запуска обоих видов тестов |
| Качество | Сценарии конкретные (не «проверить что работает»), код читаемый |
