import pytest
from main import apply_percent, apply_fixed, best_discount


# --- Тесты для apply_percent ---
def test_apply_percent_normal():
    assert apply_percent(100.0, 20.0) == 80.0


def test_apply_percent_boundaries():
    assert apply_percent(100.0, 0.0) == 100.0
    assert apply_percent(100.0, 100.0) == 0.0


def test_apply_percent_invalid_price():
    with pytest.raises(ValueError):
        apply_percent(-10.0, 10.0)


def test_apply_percent_invalid_percent():
    with pytest.raises(ValueError):
        apply_percent(100.0, 110.0)
    with pytest.raises(ValueError):
        apply_percent(100.0, -5.0)


# --- Тесты для apply_fixed ---
def test_apply_fixed_normal():
    assert apply_fixed(100.0, 30.0) == 70.0


def test_apply_fixed_exceeds_price():
    assert apply_fixed(50.0, 100.0) == 0.0


def test_apply_fixed_invalid_amount():
    with pytest.raises(ValueError):
        apply_fixed(100.0, -10.0)


# --- Тесты для best_discount ---
def test_best_discount_percent_better():
    assert best_discount(100.0, 30.0, 20.0) == 70.0


def test_best_discount_fixed_better():
    assert best_discount(100.0, 10.0, 50.0) == 50.0


def test_best_discount_boundaries():
    assert best_discount(100.0, 0.0, 0.0) == 100.0
    assert best_discount(100.0, 100.0, 100.0) == 0.0