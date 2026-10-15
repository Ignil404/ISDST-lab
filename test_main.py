import pytest
from main import BankAccount


# --- Тесты инициализации ---
def test_init_valid():
    acc = BankAccount("Alice", 100.0)
    assert acc.owner == "Alice"
    assert acc.balance == 100.0
    assert acc.history == []


def test_init_default_balance():
    acc = BankAccount("Bob")
    assert acc.balance == 0.0


def test_init_invalid_balance():
    with pytest.raises(ValueError, match="initial balance must be >= 0"):
        BankAccount("Charlie", -10.0)


# --- Тесты внесения средств (deposit) ---
def test_deposit_valid():
    acc = BankAccount("Alice", 100.0)
    res = acc.deposit(50.0)
    assert res == 150.0
    assert acc.balance == 150.0
    assert acc.history == ["deposit 50.0"]


def test_deposit_invalid_zero():
    acc = BankAccount("Alice")
    with pytest.raises(ValueError, match="amount must be > 0"):
        acc.deposit(0.0)


def test_deposit_invalid_negative():
    acc = BankAccount("Alice")
    with pytest.raises(ValueError, match="amount must be > 0"):
        acc.deposit(-10.0)


# --- Тесты снятия средств (withdraw) ---
def test_withdraw_valid():
    acc = BankAccount("Alice", 100.0)
    res = acc.withdraw(40.0)
    assert res == 60.0
    assert acc.balance == 60.0
    assert acc.history == ["withdraw 40.0"]


def test_withdraw_invalid_zero():
    acc = BankAccount("Alice", 100.0)
    with pytest.raises(ValueError, match="amount must be > 0"):
        acc.withdraw(0.0)


def test_withdraw_invalid_negative():
    acc = BankAccount("Alice", 100.0)
    with pytest.raises(ValueError, match="amount must be > 0"):
        acc.withdraw(-10.0)


def test_withdraw_insufficient_funds():
    acc = BankAccount("Alice", 50.0)
    with pytest.raises(ValueError, match="insufficient funds"):
        acc.withdraw(100.0)


# --- Тесты перевода (transfer_to) ---
def test_transfer_to_valid():
    acc1 = BankAccount("Alice", 100.0)
    acc2 = BankAccount("Bob", 50.0)
    acc1.transfer_to(acc2, 30.0)

    assert acc1.balance == 70.0
    assert acc2.balance == 80.0
    assert acc1.history == ["withdraw 30.0", "transfer 30.0 to Bob"]
    assert acc2.history == ["deposit 30.0"]


def test_transfer_to_insufficient_funds():
    acc1 = BankAccount("Alice", 10.0)
    acc2 = BankAccount("Bob", 50.0)
    with pytest.raises(ValueError, match="insufficient funds"):
        acc1.transfer_to(acc2, 20.0)


# --- Тесты истории операций (last_operations) ---
def test_last_operations_valid():
    acc = BankAccount("Alice", 100.0)
    acc.deposit(50.0)
    acc.withdraw(20.0)
    acc.deposit(10.0)

    assert acc.last_operations(2) == ["withdraw 20.0", "deposit 10.0"]
    assert acc.last_operations(1) == ["deposit 10.0"]
    assert acc.last_operations(5) == ["deposit 50.0", "withdraw 20.0", "deposit 10.0"]


def test_last_operations_zero():
    acc = BankAccount("Alice", 100.0)
    acc.deposit(50.0)
    assert acc.last_operations(0) == []


def test_last_operations_invalid():
    acc = BankAccount("Alice", 100.0)
    with pytest.raises(ValueError, match="n must be >= 0"):
        acc.last_operations(-1)
