from typing import Dict

from oop.account import Account
from oop.errors import AccountNotFoundError, DuplicateAccountError


class Bank:
    def __init__(self):
        self._accounts: Dict[str, Account] = {}

    def open_account(self, account_id: str, owner: str, initial_balance: float = 0.0) -> Account:
        if account_id in self._accounts:
            raise DuplicateAccountError(f"Счёт {account_id} уже существует")
        account = Account(account_id, owner, initial_balance)
        self._accounts[account_id] = account
        return account

    def get_account(self, account_id: str) -> Account:
        try:
            return self._accounts[account_id]
        except KeyError:
            raise AccountNotFoundError(f"Счёт {account_id} не найден") from None

    def transfer(self, from_id: str, to_id: str, amount: float) -> None:
        if from_id == to_id:
            raise ValueError("Нельзя переводить самому себе")
        from_acc = self.get_account(from_id)
        to_acc = self.get_account(to_id)
        from_acc.transfer_out(to_id, amount)
        to_acc.transfer_in(from_id, amount)