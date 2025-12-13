import re
from typing import Any, Literal

from telemars.filters.general import BaseDemoFilter
from telemars.params.filters import general as gval


def parse_audience(audience: str) -> BaseDemoFilter:
    """Возвращает объект фильтра, соответствующий строковому представлению аудитории.

    Поддерживает следующие фильтры:
    - Пол:
        - 'M' (мужчины)
        - 'W' (женщины)
        - 'All' (все).
    - Возраст:
        - 'X+' (от X лет и старше)
        - 'X-Y' (от X до Y лет).
    - Уровень дохода:
        - 'IL X' (уровень X)
        - 'IL X-Y' (уровни от X до Y)
        - 'IL X,Y,Z' (конкретные уровни)
        - 'IL X-Y,Z' (диапазон и конкретные уровни).
    - Группа дохода:
        - 'A', 'B', 'C' (отдельные группы)
        - 'AB', 'AC', 'BC', 'ABC' (комбинации групп).

    Args:
        audience (str): Строковое представление аудитории.

    Returns:
        BaseDemoFilter: Объект фильтра, соответствующий аудитории.
    """
    # Убираем лишние пробелы по краям и внутри, приводим к верхнему регистру.
    normalized: str = re.sub(r'\s+', ' ', audience.strip().upper())

    # Обновленный паттерн с поддержкой уровня дохода и группы дохода
    pattern = r'^(M|W|ALL)\s+(\d+)(?:\s*-\s*(\d+)|\+)(?:\s+(?:IL\s+([\d,-]+)|([ABC]+)))?$'
    match: re.Match[str] | None = re.match(pattern, normalized)

    if not match:
        raise ValueError(f'Некорректный формат аудитории: {audience}')

    sex_part, age_start, age_end, income_part, income_group_part = match.groups()

    # Определяем пол.
    sex: gval.Sex | None = _parse_sex(sex_part)

    # Определяем возраст.
    age: tuple[int, int] | tuple[int, Literal[99]] = _parse_age(age_start, age_end)

    # Определяем уровень дохода.
    inc_level: list[gval.IncLevel] | None = _parse_income_levels(income_part) if income_part else None

    # Определяем группу дохода.
    inc_group: list[gval.IncomeGroupRussia] | None = (
        _parse_income_groups(income_group_part) if income_group_part else None
    )

    return BaseDemoFilter(sex=sex, age=age, inc_level=inc_level, inc_group=inc_group)


def _parse_sex(sex_part: str) -> Any:
    """Парсит строку с полом и возвращает соответствующий объект Sex.

    Args:
        sex_part (str): Строка с полом ('M', 'W', 'ALL').

    Returns:
        Any: Объект Sex или None для 'ALL'.
    """
    sex_mapping: dict[str, Any] = {'M': gval.Sex.MALE, 'W': gval.Sex.FEMALE, 'ALL': None}
    return sex_mapping[sex_part]


def _parse_age(age_start: str, age_end: str | None) -> tuple[int, int] | tuple[int, Literal[99]]:
    """Парсит строки с возрастом и возвращает кортеж с минимальным и максимальным возрастом.

    Args:
        age_start (str): Строка с начальным возрастом.
        age_end (str | None): Строка с конечным возрастом или None для формата 'X+'.

    Returns:
        tuple[int, int] | tuple[int, Literal[99]]: Кортеж с возрастным диапазоном.
    """
    min_age = int(age_start)
    if age_end:
        max_age = int(age_end)
        return (min_age, max_age)
    else:
        return (min_age, 99)


def _parse_income_levels(income_str: str) -> list[gval.IncLevel]:
    """Парсит строку с уровнями дохода и возвращает список объектов IncLevel.

    Args:
        income_str (str): Строка с уровнями дохода (например, "1", "1-3", "1,2,3", "1-4,6").

    Returns:
        list[gval.IncLevel]: Список уровней дохода.
    """
    # Маппинг номеров в объекты IncLevel
    inc_mapping: dict[int, gval.IncLevel] = {
        1: gval.IncLevel._1,
        2: gval.IncLevel._2,
        3: gval.IncLevel._3,
        4: gval.IncLevel._4,
        5: gval.IncLevel._5,
        6: gval.IncLevel._6,
    }

    result_levels: set[int] = set()

    # Разбиваем по запятым для обработки каждой части
    parts: list[str] = [part.strip() for part in income_str.split(',')]

    for part in parts:
        if '-' in part:
            # Обрабатываем диапазон (например, "1-3")
            start, end = map(int, part.split('-'))
            result_levels.update(range(start, end + 1))
        else:
            # Обрабатываем отдельный уровень (например, "6")
            level = int(part)
            result_levels.add(level)

    # Сортируем и конвертируем в объекты IncLevel
    sorted_levels: list[int] = sorted(result_levels)
    return [inc_mapping[level] for level in sorted_levels]


def _parse_income_groups(income_group_str: str) -> list[gval.IncomeGroupRussia]:
    """Парсит строку с группами дохода и возвращает список объектов IncomeGroupRussia.

    Args:
        income_group_str (str): Строка с группами дохода (например, "A", "AB", "ABC").

    Returns:
        list[gval.IncomeGroupRussia]: Список групп дохода в порядке следования в строке.
    """
    # Маппинг букв в объекты IncomeGroupRussia
    group_mapping: dict[str, gval.IncomeGroupRussia] = {
        'A': gval.IncomeGroupRussia.A,
        'B': gval.IncomeGroupRussia.B,
        'C': gval.IncomeGroupRussia.C,
    }

    # Преобразуем каждую букву в строке в соответствующий объект группы дохода
    return [group_mapping[char] for char in income_group_str if char in group_mapping]
