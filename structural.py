"""
Задача 3: Банковский счёт — СТРУКТУРНЫЙ СТИЛЬ.

Данные и логика разделены: счета хранятся в обычных словарях,
вся логика реализована функциями, которые принимают эти словари
как аргументы и изменяют их.
"""

from typing import Dict, List, Optional


def create_bank() -> Dict[str, dict]:
    """Создать пустое хранилище счетов: {номер_счёта: данные_счёта}."""
    return {}


def open_account(bank: Dict[str, dict], account_id: str, owner: str, initial_balance: float = 0.0) -> None:
    """Открыть новый счёт с нулевым (или заданным) балансом."""
    if account_id in bank:
        raise ValueError(f"Счёт {account_id} уже существует")
    if initial_balance < 0:
        raise ValueError("Начальный баланс не может быть отрицательным")
    bank[account_id] = {
        "owner": owner,
        "balance": initial_balance,
        "history": [],  # список строк с описанием операций
    }


def _add_history(account: dict, text: str) -> None:
    account["history"].append(text)


def deposit(bank: Dict[str, dict], account_id: str, amount: float) -> None:
    """Пополнение счёта."""
    if amount <= 0:
        raise ValueError("Сумма пополнения должна быть положительной")
    account = bank[account_id]
    account["balance"] += amount
    _add_history(account, f"Пополнение: +{amount:.2f}, баланс: {account['balance']:.2f}")


def withdraw(bank: Dict[str, dict], account_id: str, amount: float) -> None:
    """Снятие со счёта с проверкой баланса."""
    if amount <= 0:
        raise ValueError("Сумма снятия должна быть положительной")
    account = bank[account_id]
    if account["balance"] < amount:
        raise ValueError(f"Недостаточно средств на счёте {account_id}")
    account["balance"] -= amount
    _add_history(account, f"Снятие: -{amount:.2f}, баланс: {account['balance']:.2f}")


def transfer(bank: Dict[str, dict], from_id: str, to_id: str, amount: float) -> None:
    """Перевод с одного счёта на другой."""
    if from_id == to_id:
        raise ValueError("Нельзя переводить самому себе")
    withdraw(bank, from_id, amount)
    deposit(bank, to_id, amount)
    _add_history(bank[from_id], f"Перевод на {to_id}: -{amount:.2f}")
    _add_history(bank[to_id], f"Перевод от {from_id}: +{amount:.2f}")


def get_history(bank: Dict[str, dict], account_id: str, n: int) -> List[str]:
    """Последние N операций по счёту."""
    return bank[account_id]["history"][-n:]


def get_balance(bank: Dict[str, dict], account_id: str) -> float:
    return bank[account_id]["balance"]


def demo() -> None:
    """Небольшой демонстрационный сценарий."""
    bank = create_bank()
    open_account(bank, "acc1", "Иван Иванов", 100.0)
    open_account(bank, "acc2", "Пётр Петров", 50.0)

    deposit(bank, "acc1", 200.0)
    withdraw(bank, "acc1", 50.0)
    transfer(bank, "acc1", "acc2", 75.0)

    print("Баланс acc1:", get_balance(bank, "acc1"))
    print("Баланс acc2:", get_balance(bank, "acc2"))

    print("\nПоследние 3 операции acc1:")
    for entry in get_history(bank, "acc1", 3):
        print(" -", entry)

    print("\nПопытка снять больше, чем есть на acc2:")
    try:
        withdraw(bank, "acc2", 10_000.0)
    except ValueError as e:
        print(" Ошибка:", e)


def interactive() -> None:
    """Интерактивная работа с банком через консольное меню."""
    bank = create_bank()
    print("Добро пожаловать в банк (структурный стиль)!")

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
                open_account(bank, account_id, owner, initial)
                print("Счёт открыт.")
            except ValueError as e:
                print(" Ошибка:", e)
        elif choice == "2":
            account_id = input("Номер счёта: ").strip()
            try:
                amount = float(input("Сумма: ").strip())
                deposit(bank, account_id, amount)
                print("Баланс:", get_balance(bank, account_id))
            except ValueError as e:
                print(" Ошибка:", e)
        elif choice == "3":
            account_id = input("Номер счёта: ").strip()
            try:
                amount = float(input("Сумма: ").strip())
                withdraw(bank, account_id, amount)
                print("Баланс:", get_balance(bank, account_id))
            except (ValueError, KeyError) as e:
                print(" Ошибка:", e)
        elif choice == "4":
            from_id = input("С какого счёта: ").strip()
            to_id = input("На какой счёт: ").strip()
            try:
                amount = float(input("Сумма: ").strip())
                transfer(bank, from_id, to_id, amount)
                print("Перевод выполнен.")
            except (ValueError, KeyError) as e:
                print(" Ошибка:", e)
        elif choice == "5":
            account_id = input("Номер счёта: ").strip()
            try:
                print("Баланс:", get_balance(bank, account_id))
            except KeyError as e:
                print(" Ошибка:", e)
        elif choice == "6":
            account_id = input("Номер счёта: ").strip()
            try:
                n = int(input("Сколько последних операций: ").strip())
                for entry in get_history(bank, account_id, n):
                    print(" -", entry)
            except (ValueError, KeyError) as e:
                print(" Ошибка:", e)
        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    interactive()
