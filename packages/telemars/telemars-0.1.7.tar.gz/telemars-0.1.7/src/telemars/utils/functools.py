from collections.abc import Sequence
from enum import Enum
from typing import Any


def group_consecutive(numbers: Sequence[int]) -> list[str]:
    """Группирует последовательные числа в диапазоны.

    Пример:
        [1, 2, 3, 5, 7, 8] -> ['1-3', '5', '7-8']
        [1, 2, 4, 5] -> ['1', '2', '4', '5']  # соседние числа не объединяются

    Args:
        numbers: Последовательность целых чисел (должна быть отсортирована).

    Returns:
        Список строк с диапазонами или отдельными числами.
    """
    if not numbers:
        return []

    ranges: list[str] = []
    start = end = numbers[0]

    for num in numbers[1:]:
        if num == end + 1:
            end = num
        else:
            # Если диапазон состоит только из двух соседних чисел, разделяем запятой.
            if end == start + 1:
                ranges.append(str(start))
                ranges.append(str(end))
            else:
                ranges.append(f'{start}-{end}' if start != end else str(start))
            start = end = num

    # Обрабатываем последний диапазон.
    if end == start + 1:
        ranges.append(str(start))
        ranges.append(str(end))
    else:
        ranges.append(f'{start}-{end}' if start != end else str(start))

    return ranges


def gen_flt_expr(flt: str, value: Sequence | Any | None) -> str | None:
    """Генерирует фильтр-выражение для поля pydantic.

    Args:
        flt: Имя фильтра (поля).
        value: Значение фильтра (одиночное или последовательность) или None.

    Returns:
        Строку фильтра или None, если value is None или последовательность пуста.
    """
    if value is None:
        return None

    # Преобразуем одиночное значение в список.
    if not isinstance(value, (list, tuple, set)):
        value = [value]
    else:
        if not value:
            return None

        value = list(value)

    # Проверяем, является ли первый элемент enum.
    use_value_attr: bool = len(value) > 0 and isinstance(value[0], Enum)

    if use_value_attr:
        if len(value) == 1:
            return f'{flt} = {value[0].value}'

        return f'{flt} IN ({", ".join(str(v.value) for v in value)})'

    if len(value) == 1:
        return f'{flt} = {value[0]}'

    return f'{flt} IN ({", ".join(map(str, value))})'
