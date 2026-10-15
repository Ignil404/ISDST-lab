def apply_percent(price: float, percent: float) -> float:
    """Применяет скидку в процентах."""
    if price < 0:
        raise ValueError("Price cannot be negative")
    if not (0 <= percent <= 100):
        raise ValueError("Percent must be between 0 and 100")
    return price * (1 - percent / 100)


def apply_fixed(price: float, amount: float) -> float:
    """Применяет фиксированную скидку. Цена не может быть ниже 0."""
    if price < 0:
        raise ValueError("Price cannot be negative")
    if amount < 0:
        raise ValueError("Fixed amount cannot be negative")
    return max(0.0, price - amount)


def best_discount(price: float, percent: float, amount: float) -> float:
    """Возвращает минимальную итоговую цену из двух способов скидки."""
    if price < 0:
        raise ValueError("Price cannot be negative")
    if not (0 <= percent <= 100):
        raise ValueError("Percent must be between 0 and 100")
    if amount < 0:
        raise ValueError("Fixed amount cannot be negative")

    return min(apply_percent(price, percent), apply_fixed(price, amount))
