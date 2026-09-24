"""Банковский счёт — ООП-стиль (пакет).

Ответственность распределена по отдельным модулям:
  oop.account  — счёт (баланс, история, операции над собой);
  oop.bank     — банк (коллекция счетов, переводы);
  oop.errors   — ошибки предметной области;
  oop.console  — консольный интерфейс пользователя;
  oop.demo     — демонстрационный сценарий.
"""

from oop.account import Account
from oop.bank import Bank
from oop.demo import demo
from oop.errors import AccountNotFoundError, DuplicateAccountError, InsufficientFundsError

__all__ = [
    "Account",
    "Bank",
    "AccountNotFoundError",
    "DuplicateAccountError",
    "InsufficientFundsError",
    "demo",
]