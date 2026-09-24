"""Счёт клиента: баланс и история операций."""

from typing import List

from oop.errors import InsufficientFundsError


class Account:
    """Инкапсулирует состояние счёта и операции над собственным балансом."""

    def __init__(self, account_id: str, owner: str, initial_balance: float = 0.0):
        if initial_balance < 0:
            raise ValueError("Начальный баланс не может быть отрицательным")
        self.account_id = account_id
        self.owner = owner
        self._balance = initial_balance
        self._history: List[str] = []

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        self._balance += amount
        self._log(f"Пополнение: +{amount:.2f}, баланс: {self._balance:.2f}")

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")
        if amount > self._balance:
            raise InsufficientFundsError(f"Недостаточно средств на счёте {self.account_id}")
        self._balance -= amount
        self._log(f"Снятие: -{amount:.2f}, баланс: {self._balance:.2f}")

    def transfer_out(self, to_id: str, amount: float) -> None:
        """Списать сумму в пользу другого счёта и записать перевод в историю."""
        self.withdraw(amount)
        self._log(f"Перевод на {to_id}: -{amount:.2f}")

    def transfer_in(self, from_id: str, amount: float) -> None:
        """Зачислить сумму с другого счёта и записать перевод в историю."""
        self.deposit(amount)
        self._log(f"Перевод от {from_id}: +{amount:.2f}")

    def get_history(self, n: int) -> List[str]:
        return self._history[-n:]

    def _log(self, text: str) -> None:
        self._history.append(text)