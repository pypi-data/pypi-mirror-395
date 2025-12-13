from enum import Enum
from typing import Any, Optional, Sequence, Union


def gen_flt_expr(filter_name: str, filter_values: Optional[Union[Sequence, Any]]) -> Optional[str]:
    """Генерирует фильтр-выражение для поля pydantic.

    Args:
        filter_name (str): Имя поля pydantic-класса.
        filter_values (Optional[Union[Sequence, Any]]): Последовательность значений, одиночное значение или None.

    Returns:
        Optional[str]: Строку фильтра или None, если values is None
    """
    if filter_values is None:
        return None

    # Преобразуем одиночное значение в список.
    if not isinstance(filter_values, (list, tuple, set)):
        filter_values = [filter_values]

    # Проверяем, является ли первый элемент enum.
    use_value_attr: bool = len(filter_values) > 0 and isinstance(filter_values[0], Enum)

    if use_value_attr:
        if len(filter_values) == 1:
            return f'{filter_name} = {filter_values[0].value}'

        return f'{filter_name} IN ({", ".join(str(v.value) for v in filter_values)})'

    if len(filter_values) == 1:
        return f'{filter_name} = {filter_values[0]}'

    return f'{filter_name} IN ({", ".join(map(str, filter_values))})'
