class InsufficientFundsError(Exception):
    """Попытка снять/перевести больше, чем есть на счёте."""


class AccountNotFoundError(KeyError):
    """Запрошенный счёт отсутствует в банке."""


class DuplicateAccountError(ValueError):
    """Попытка открыть уже существующий счёт."""