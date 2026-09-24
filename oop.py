"""
Задача 3: Банковский счёт — ООП-СТИЛЬ.

Состояние и поведение инкапсулированы: класс Account отвечает
за собственный баланс и историю операций, класс Bank отвечает
за коллекцию счетов и переводы между ними.
"""

from typing import List


class InsufficientFundsError(Exception):
    """Попытка снять/перевести больше, чем есть на счёте."""


class Account:
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

    def _log(self, text: str) -> None:
        self._history.append(text)

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

    def get_history(self, n: int) -> List[str]:
        return self._history[-n:]


class Bank:
    def __init__(self):
        self._accounts = {}

    def open_account(self, account_id: str, owner: str, initial_balance: float = 0.0) -> Account:
        if account_id in self._accounts:
            raise ValueError(f"Счёт {account_id} уже существует")
        account = Account(account_id, owner, initial_balance)
        self._accounts[account_id] = account
        return account

    def get_account(self, account_id: str) -> Account:
        return self._accounts[account_id]

    def transfer(self, from_id: str, to_id: str, amount: float) -> None:
        if from_id == to_id:
            raise ValueError("Нельзя переводить самому себе")
        from_acc = self.get_account(from_id)
        to_acc = self.get_account(to_id)
        from_acc.withdraw(amount)
        to_acc.deposit(amount)
        from_acc._log(f"Перевод на {to_id}: -{amount:.2f}")
        to_acc._log(f"Перевод от {from_id}: +{amount:.2f}")


def demo() -> None:
    """Небольшой демонстрационный сценарий."""
    bank = Bank()
    acc1 = bank.open_account("acc1", "Иван Иванов", 100.0)
    acc2 = bank.open_account("acc2", "Пётр Петров", 50.0)

    acc1.deposit(200.0)
    acc1.withdraw(50.0)
    bank.transfer("acc1", "acc2", 75.0)

    print("Баланс acc1:", acc1.balance)
    print("Баланс acc2:", acc2.balance)

    print("\nПоследние 3 операции acc1:")
    for entry in acc1.get_history(3):
        print(" -", entry)

    print("\nПопытка снять больше, чем есть на acc2:")
    try:
        acc2.withdraw(10_000.0)
    except InsufficientFundsError as e:
        print(" Ошибка:", e)


def interactive() -> None:
    """Интерактивная работа с банком через консольное меню."""
    bank = Bank()
    print("Добро пожаловать в банк (ООП-стиль)!")

    while True:
        print("\nМеню:")
        print(" 1 — открыть счёт")
        print(" 2 — пополнить")
        print(" 3 — снять")
        print(" 4 — перевести")
        print(" 5 — баланс")
        print(" 6 — история последних N операций")
        print(" 0 — выход")
        choice = input("Выбор: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            account_id = input("Номер счёта: ").strip()
            owner = input("Владелец: ").strip()
            try:
                initial = float(input("Начальный баланс (по умолчанию 0): ").strip() or "0")
                bank.open_account(account_id, owner, initial)
                print("Счёт открыт.")
            except ValueError as e:
                print(" Ошибка:", e)
        elif choice == "2":
            account_id = input("Номер счёта: ").strip()
            try:
                amount = float(input("Сумма: ").strip())
                bank.get_account(account_id).deposit(amount)
                print("Баланс:", bank.get_account(account_id).balance)
            except (ValueError, KeyError) as e:
                print(" Ошибка:", e)
        elif choice == "3":
            account_id = input("Номер счёта: ").strip()
            try:
                amount = float(input("Сумма: ").strip())
                bank.get_account(account_id).withdraw(amount)
                print("Баланс:", bank.get_account(account_id).balance)
            except (ValueError, KeyError) as e:
                print(" Ошибка:", e)
        elif choice == "4":
            from_id = input("С какого счёта: ").strip()
            to_id = input("На какой счёт: ").strip()
            try:
                amount = float(input("Сумма: ").strip())
                bank.transfer(from_id, to_id, amount)
                print("Перевод выполнен.")
            except (ValueError, KeyError) as e:
                print(" Ошибка:", e)
        elif choice == "5":
            account_id = input("Номер счёта: ").strip()
            try:
                print("Баланс:", bank.get_account(account_id).balance)
            except KeyError as e:
                print(" Ошибка:", e)
        elif choice == "6":
            account_id = input("Номер счёта: ").strip()
            try:
                n = int(input("Сколько последних операций: ").strip())
                for entry in bank.get_account(account_id).get_history(n):
                    print(" -", entry)
            except (ValueError, KeyError) as e:
                print(" Ошибка:", e)
        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    interactive()
