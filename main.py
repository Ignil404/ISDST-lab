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
