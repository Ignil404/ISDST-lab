"""Демонстрационный сценарий для ООП-реализации."""

from oop.bank import Bank
from oop.errors import InsufficientFundsError


def demo() -> None:
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