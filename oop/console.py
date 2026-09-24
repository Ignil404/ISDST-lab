"""Консольный интерфейс пользователя (ввод/вывод отделён от доменной логики)."""

from oop.bank import Bank
from oop.errors import AccountNotFoundError, InsufficientFundsError


class BankConsole:
    """Строит банк и транслирует действия пользователя в вызовы банка."""

    def __init__(self, bank: Bank = None):
        self._bank = bank if bank is not None else Bank()

    def run(self) -> None:
        print("Добро пожаловать в банк (ООП-стиль)!")

        while True:
            self._print_menu()
            choice = input("Выбор: ").strip()

            if choice == "0":
                break
            elif choice == "1":
                self._open_account()
            elif choice == "2":
                self._deposit()
            elif choice == "3":
                self._withdraw()
            elif choice == "4":
                self._transfer()
            elif choice == "5":
                self._show_balance()
            elif choice == "6":
                self._show_history()
            else:
                print("Неизвестная команда.")

    @staticmethod
    def _print_menu() -> None:
        print("\nМеню:")
        print(" 1 — открыть счёт")
        print(" 2 — пополнить")
        print(" 3 — снять")
        print(" 4 — перевести")
        print(" 5 — баланс")
        print(" 6 — история последних N операций")
        print(" 0 — выход")

    def _ask_account_id(self) -> str:
        return input("Номер счёта: ").strip()

    def _open_account(self) -> None:
        account_id = self._ask_account_id()
        owner = input("Владелец: ").strip()
        try:
            initial = float(input("Начальный баланс (по умолчанию 0): ").strip() or "0")
            self._bank.open_account(account_id, owner, initial)
            print("Счёт открыт.")
        except ValueError as e:
            print(" Ошибка:", e)

    def _deposit(self) -> None:
        account_id = self._ask_account_id()
        try:
            amount = float(input("Сумма: ").strip())
            account = self._bank.get_account(account_id)
            account.deposit(amount)
            print("Баланс:", account.balance)
        except (ValueError, AccountNotFoundError) as e:
            print(" Ошибка:", e)

    def _withdraw(self) -> None:
        account_id = self._ask_account_id()
        try:
            amount = float(input("Сумма: ").strip())
            account = self._bank.get_account(account_id)
            account.withdraw(amount)
            print("Баланс:", account.balance)
        except (ValueError, AccountNotFoundError, InsufficientFundsError) as e:
            print(" Ошибка:", e)

    def _transfer(self) -> None:
        from_id = input("С какого счёта: ").strip()
        to_id = input("На какой счёт: ").strip()
        try:
            amount = float(input("Сумма: ").strip())
            self._bank.transfer(from_id, to_id, amount)
            print("Перевод выполнен.")
        except (ValueError, AccountNotFoundError, InsufficientFundsError) as e:
            print(" Ошибка:", e)

    def _show_balance(self) -> None:
        account_id = self._ask_account_id()
        try:
            print("Баланс:", self._bank.get_account(account_id).balance)
        except AccountNotFoundError as e:
            print(" Ошибка:", e)

    def _show_history(self) -> None:
        account_id = self._ask_account_id()
        try:
            n = int(input("Сколько последних операций: ").strip())
            for entry in self._bank.get_account(account_id).get_history(n):
                print(" -", entry)
        except (ValueError, AccountNotFoundError) as e:
            print(" Ошибка:", e)