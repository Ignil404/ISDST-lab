# Задача 3: Калькулятор скидки

**Студент:** Буслович Игнат

---

### 3. Калькулятор скидки

Реализуйте:

```python
# main.py
def apply_percent(price: float, percent: float) -> float:
    ...

def apply_fixed(price: float, amount: float) -> float:
    ...

def best_discount(price: float, percent: float, amount: float) -> float:
    """Вернуть минимальную итоговую цену из двух способов; цена не ниже 0."""
    ...
```

## Постановка задачи
Реализуйте функции для расчёта скидки:
- `apply_percent(price, percent)` — скидка в процентах.
- `apply_fixed(price, amount)` — фиксированная скидка.
- `best_discount(price, percent, amount)` — выбор минимальной итоговой цены.

Ошибки: отрицательная цена / процент вне [0, 100] / отрица round fixed — через `ValueError`.  
BDD: процент выгоднее fixed, fixed выгоднее, граничные 0 и 100 %.

---

## Запуск юнит-тестов
```bash
pytest test_main.py
python pytest
