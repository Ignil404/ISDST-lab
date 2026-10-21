"""Библиотека преобразования оценок: 5-балльная шкала <-> ECTS."""

from grade_converter.converter import (
    ECTS_TO_GRADE,
    GRADE_TO_ECTS,
    GRADE_INFO,
    convert_many,
    to_ects,
    to_russian,
)

__all__ = [
    "GRADE_TO_ECTS",
    "ECTS_TO_GRADE",
    "GRADE_INFO",
    "to_ects",
    "to_russian",
    "convert_many",
]

__version__ = "1.0.0"
