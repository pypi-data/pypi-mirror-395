from typing import Optional, Sequence, TypeVar, Union

# NOTE: T - переменная типа, которая гарантирует, что все элементы в последовательности одного типа.
T = TypeVar('T')


def is_unique_sequence(values: Optional[Sequence[T]]) -> Optional[Sequence[T]]:
    """Проверяет, что все элементы в последовательности уникальны."""
    if values is None:
        return values

    if len(values) != len(set(values)):
        raise ValueError('Элементы последовательности должны быть уникальными.')

    return values


def is_within_range(
    values: Optional[Sequence[Union[int, float]]], min_value: int, max_value: int
) -> Optional[Sequence[Union[int, float]]]:
    """Проверяет, что все элементы в последовательности находятся в заданном диапазоне значений."""
    if values is None:
        return values

    for item in values:
        if item < min_value or item > max_value:
            raise ValueError('Элемент последовательности {} вне диапазона {}-{}.'.format(item, min_value, max_value))

    return values
