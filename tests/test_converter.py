import pytest

from grade_converter import (
    ECTS_TO_GRADE,
    GRADE_TO_ECTS,
    GRADE_INFO,
    convert_many,
    to_ects,
    to_russian,
)


@pytest.mark.parametrize("grade,ects", sorted(GRADE_TO_ECTS.items()))
def test_to_ects_table(grade, ects):
    assert to_ects(grade) == ects


def test_to_ects_expected_values():
    """Проверка на случай порчи таблицы."""
    assert to_ects(5) == "A"
    assert to_ects(4) == "B"
    assert to_ects(3) == "C"
    assert to_ects(2) == "F"


# --- Таблица соответствий ECTS -> 5-балл ---
@pytest.mark.parametrize("ects,grade", sorted(ECTS_TO_GRADE.items()))
def test_to_russian_table(ects, grade):
    assert to_russian(ects) == grade


@pytest.mark.parametrize("ects", ["a", "b", "c", "f"])
def test_to_russian_lowercase(ects):
    """Регистр буквы не важен."""
    assert to_russian(ects) == ECTS_TO_GRADE[ects.upper()]


def test_to_russian_with_spaces():
    assert to_russian("  A ") == 5


# --- Обратимость (round-trip) ---
@pytest.mark.parametrize("grade", sorted(GRADE_TO_ECTS))
def test_round_trip(grade):
    assert to_russian(to_ects(grade)) == grade


@pytest.mark.parametrize("ects", sorted(ECTS_TO_GRADE))
def test_reverse_round_trip(ects):
    assert to_ects(to_russian(ects)) == ects


# --- Справочная информация согласована с таблицей ---
@pytest.mark.parametrize("grade", sorted(GRADE_INFO))
def test_grade_info_consistent(grade):
    info = GRADE_INFO[grade]
    assert info["ects"] == GRADE_TO_ECTS[grade]
    assert isinstance(info["min_score"], int)
    assert info["min_score"] < 100


def test_min_scores_descending():
    """Порог ECTS-баллов убывает по мере ухудшения оценки."""
    scores = [GRADE_INFO[g]["min_score"] for g in sorted(GRADE_INFO, reverse=True)]
    assert scores == sorted(scores, reverse=True)
    assert len(set(scores)) == len(scores)


# --- Некорректный ввод ---
@pytest.mark.parametrize("bad", [0, 1, 6, -3, 100])
def test_to_ects_invalid_grade(bad):
    with pytest.raises(ValueError, match="grade must be in 2..5"):
        to_ects(bad)


@pytest.mark.parametrize("bad", [5.0, "5", None, True, [5]])
def test_to_ects_non_int(bad):
    with pytest.raises(ValueError, match="grade must be an int"):
        to_ects(bad)


@pytest.mark.parametrize("bad", ["E", "AA", "", "3.5"])
def test_to_russian_invalid_letter(bad):
    with pytest.raises(ValueError, match="ects must be one of"):
        to_russian(bad)


@pytest.mark.parametrize("bad", [5, None, ["A"]])
def test_to_russian_non_str(bad):
    with pytest.raises(ValueError, match="ects must be a str"):
        to_russian(bad)


# --- Пакетная конвертация ---
def test_convert_many_mixed_input():
    assert convert_many([5, "4", 3, "2"]) == ["A", "B", "C", "F"]


def test_convert_many_empty():
    assert convert_many([]) == []


def test_convert_many_invalid_item():
    with pytest.raises(ValueError):
        convert_many([5, "отлично"])