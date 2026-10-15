# Задача 3: Банковский счёт

**Студент:** Буслович Игнат  

---

## Постановка задачи

Напишите тесты и измерьте покрытие для модуля `main.py`, реализующего класс `BankAccount` с методами для внесения, снятия, перевода средств и просмотра истории операций.

---

## Структура репозитория

```
lab_3/
├── README.md           # Этот файл
├── main.py             # Тестируемый модуль (класс BankAccount)
├── test_main.py        # Юнит-тесты (pytest)
└── requirements.txt    # Зависимости для тестирования
```

---

## main.py

```python
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

## Что покрыто тестами

| Метод | Сценарии |
|---|---|
| `__init__` | Валидная инициализация, дефолтный баланс, отрицательный баланс |
| `deposit` | Успешное внесение, нулевая сумма, отрицательная сумма |
| `withdraw` | Успешное снятие, нулевая/отрицательная сумма, недостаточно средств |
| `transfer_to` | Успешный перевод, недостаточно средств у отправителя |
| `last_operations` | Нормальный запрос, `n = 0`, `n > len(history)`, отрицательное `n` |

**Итоговое покрытие `main.py`: 100 % строк.**

---
