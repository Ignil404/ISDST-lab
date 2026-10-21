"""Конвертер оценок: 5-балльная шкала <-> ECTS.

Таблица соответствий:

=====  ==========  ==============  ==============
5-балл  ECTS        Балл ECTS (min) Описание
=====  ==========  ==============  ==============
5      A           90              отлично
4      B           80              хорошо
3      C           65              удовлетворительно
2      F           0               неудовлетворительно
=====  ==========  ==============  ==============
"""

from typing import Dict, List

GRADE_TO_ECTS: Dict[int, str] = {
    5: "A",
    4: "B",
    3: "C",
    2: "F",
}

ECTS_TO_GRADE: Dict[str, int] = {ects: grade for grade, ects in GRADE_TO_ECTS.items()}

GRADE_INFO: Dict[int, Dict[str, object]] = {
    5: {"ects": "A", "min_score": 90, "title": "отлично"},
    4: {"ects": "B", "min_score": 80, "title": "хорошо"},
    3: {"ects": "C", "min_score": 65, "title": "удовлетворительно"},
    2: {"ects": "F", "min_score": 0, "title": "неудовлетворительно"},
}


def _check_grade(grade: object) -> int:
    """Проверяет, что оценка — целое число из диапазона 2..5."""
    if isinstance(grade, bool) or not isinstance(grade, int):
        raise ValueError(f"grade must be an int, got {type(grade).__name__}")
    if grade not in GRADE_TO_ECTS:
        raise ValueError(f"grade must be in 2..5, got {grade}")
    return grade


def _check_ects(ects: object) -> str:
    """Проверяет, что ECTS-оценка — допустимая буква (регистр не важен)."""
    if not isinstance(ects, str):
        raise ValueError(f"ects must be a str, got {type(ects).__name__}")
    letter = ects.strip().upper()
    if letter not in ECTS_TO_GRADE:
        raise ValueError(f"ects must be one of {sorted(ECTS_TO_GRADE)}, got {ects!r}")
    return letter


def to_ects(grade: int) -> str:
    """Переводит 5-балльную оценку в букву ECTS.

    >>> to_ects(5)
    'A'
    >>> to_ects(2)
    'F'
    """
    return GRADE_TO_ECTS[_check_grade(grade)]


def to_russian(ects: str) -> int:
    """Переводит букву ECTS в 5-балльную оценку.

    >>> to_russian("B")
    4
    >>> to_russian("c")
    3
    """
    return ECTS_TO_GRADE[_check_ects(ects)]


def convert_many(items: List[object]) -> List[str]:
    """Конвертирует список 5-балльных оценок в ECTS.

    На вход принимает и строки ("5"), и числа (5) — оба варианта валидны.
    """
    result: List[str] = []
    for item in items:
        if isinstance(item, str):
            item = item.strip()
            if not item.lstrip("-").isdigit():
                raise ValueError(f"grade must be a digit string, got {item!r}")
            item = int(item)
        result.append(to_ects(item))
    return result