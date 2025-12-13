import re
from typing import Literal

from telemars.filters.general import BaseDemoFilter
from telemars.params.filters import general as gval

# Тип для значений kids_age фильтров.
type KidsAgeYesType = gval.KidsAge2 | gval.KidsAge3 | gval.KidsAge4 | gval.KidsAge5 | gval.KidsAge6 | gval.KidsAge7

type AgeRange = tuple[int, int] | tuple[int, Literal[99]]


# NOTE: Константы маппингов для парсинга аудитории

# Маппинг строкового представления пола в enum
_SEX_MAPPING: dict[str, gval.Sex | None] = {
    'M': gval.Sex.MALE,
    'W': gval.Sex.FEMALE,
    'ALL': None,
}

# Маппинг номеров уровня дохода в enum
_INC_LEVEL_MAPPING: dict[int, gval.IncLevel] = {
    1: gval.IncLevel._1,
    2: gval.IncLevel._2,
    3: gval.IncLevel._3,
    4: gval.IncLevel._4,
    5: gval.IncLevel._5,
    6: gval.IncLevel._6,
}

# Маппинг букв группы дохода в enum
_INCOME_GROUP_MAPPING: dict[str, gval.IncomeGroupRussia] = {
    'A': gval.IncomeGroupRussia.A,
    'B': gval.IncomeGroupRussia.B,
    'C': gval.IncomeGroupRussia.C,
}

# Маппинг уровней затрат на питание в enum
_SPENDINGS_ON_FOOD_MAPPING: dict[int, gval.SpendingsOnFood] = {
    1: gval.SpendingsOnFood.LESS_THAN_A_QUARTER,
    2: gval.SpendingsOnFood.FROM_QUARTER_TO_HALF,
    3: gval.SpendingsOnFood.FROM_HALF_TO_THREE_QUARTERS,
    4: gval.SpendingsOnFood.MORE_THAN_THREE_QUARTERS,
    5: gval.SpendingsOnFood.DIFFICULT_TO_ANSWER,
}

# Маппинг возраста ребенка на соответствующее поле фильтра и тип enum
_KIDS_AGE_TO_FIELD_MAPPING: dict[int, tuple[str, KidsAgeYesType]] = {
    0: ('kids_age2', gval.KidsAge2.YES),
    1: ('kids_age3', gval.KidsAge3.YES),
    2: ('kids_age4', gval.KidsAge4.YES),
    3: ('kids_age4', gval.KidsAge4.YES),
    4: ('kids_age5', gval.KidsAge5.YES),
    5: ('kids_age5', gval.KidsAge5.YES),
    6: ('kids_age5', gval.KidsAge5.YES),
    7: ('kids_age6', gval.KidsAge6.YES),
    8: ('kids_age6', gval.KidsAge6.YES),
    9: ('kids_age6', gval.KidsAge6.YES),
    10: ('kids_age6', gval.KidsAge6.YES),
    11: ('kids_age6', gval.KidsAge6.YES),
    12: ('kids_age7', gval.KidsAge7.YES),
    13: ('kids_age7', gval.KidsAge7.YES),
    14: ('kids_age7', gval.KidsAge7.YES),
    15: ('kids_age7', gval.KidsAge7.YES),
}


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
    - Возраст детей:
        - 'w kids X-Y' или 'with kids X-Y' (возраст детей от X до Y лет).
    - Затраты на питание:
        - 'food (X-Y)' или 'food (X)' (уровни затрат на питание).

    Args:
        audience (str): Строковое представление аудитории.

    Returns:
        BaseDemoFilter: Объект фильтра, соответствующий аудитории.
    """
    # Убираем лишние пробелы по краям и внутри, приводим к верхнему регистру.
    normalized: str = re.sub(r'\s+', ' ', audience.strip().upper())

    # Паттерн для парсинга аудитории с поддержкой всех опций.
    pattern: str = (
        r'^(M|W|ALL)\s+'  # Пол
        r'(\d+)(?:\s*-\s*(\d+)|\+)'  # Возраст
        r'(?:\s*([ABC]+(?:-[ABC])?))?'  # Группа дохода (опционально, ABC или A-C)
        r'(?:\s+IL\s+([\d,\-]+))?'  # Уровень дохода (опционально)
        r'(?:\s+(?:W(?:ITH)?)\s+KIDS\s+(\d+)\s*-\s*(\d+))?'  # Возраст детей (опционально)
        r'(?:\s+FOOD\s*\(\s*(\d+)(?:\s*-\s*(\d+))?\s*\))?'  # Затраты на питание (опционально)
        r'$'
    )
    match: re.Match[str] | None = re.match(pattern, normalized)

    if not match:
        raise ValueError(f'Некорректный формат аудитории: {audience}')

    (
        sex_part,
        age_start,
        age_end,
        income_group_part,
        income_part,
        kids_age_start,
        kids_age_end,
        food_start,
        food_end,
    ) = match.groups()

    # Определяем пол.
    sex: gval.Sex | None = _parse_sex(sex_part)

    # Определяем возраст.
    age: AgeRange = _parse_age(age_start, age_end)

    # Определяем уровень дохода.
    inc_level: list[gval.IncLevel] | None = _parse_income_levels(income_part) if income_part else None

    # Определяем группу дохода.
    inc_group: list[gval.IncomeGroupRussia] | None = (
        _parse_income_groups(income_group_part) if income_group_part else None
    )

    # Определяем возраст детей.
    kids_age_filters: dict[str, list[KidsAgeYesType]] = (
        _parse_kids_age(kids_age_start, kids_age_end) if kids_age_start else {}
    )

    # Определяем затраты на питание.
    spendings_on_food: list[gval.SpendingsOnFood] | None = (
        _parse_spendings_on_food(food_start, food_end) if food_start else None
    )

    return BaseDemoFilter(
        sex=sex,
        age=age,
        inc_level=inc_level,
        income_group_russia=inc_group,
        spendings_on_food=spendings_on_food,
        **kids_age_filters,
    )


def _parse_sex(sex_part: str) -> gval.Sex | None:
    """Парсит строку с полом и возвращает соответствующий объект Sex.

    Args:
        sex_part (str): Строка с полом ('M', 'W', 'ALL').

    Returns:
        gval.Sex | None: Объект Sex или None для 'ALL'.
    """
    return _SEX_MAPPING[sex_part]


def _parse_age(age_start: str, age_end: str | None) -> AgeRange:
    """Парсит строки с возрастом и возвращает кортеж с минимальным и максимальным возрастом.

    Args:
        age_start (str): Строка с начальным возрастом.
        age_end (str | None): Строка с конечным возрастом или None для формата 'X+'.

    Returns:
        AgeRange: Кортеж с возрастным диапазоном.
    """
    min_age: int = int(age_start)
    if age_end:
        max_age: int = int(age_end)
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
    result_levels: set[int] = set()

    # Разбиваем по запятым для обработки каждой части
    parts: list[str] = [part.strip() for part in income_str.split(',')]

    for part in parts:
        if '-' in part:
            # Обрабатываем диапазон (например, "1-3")
            start: int
            end: int
            start, end = map(int, part.split('-'))
            result_levels.update(range(start, end + 1))
        else:
            # Обрабатываем отдельный уровень (например, "6")
            level: int = int(part)
            result_levels.add(level)

    # Сортируем и конвертируем в объекты IncLevel
    sorted_levels: list[int] = sorted(result_levels)
    return [_INC_LEVEL_MAPPING[level] for level in sorted_levels]


def _parse_income_groups(income_group_str: str) -> list[gval.IncomeGroupRussia]:
    """Парсит строку с группами дохода и возвращает список объектов IncomeGroupRussia.

    Args:
        income_group_str (str): Строка с группами дохода (например, "A", "AB", "ABC", "A-C").

    Returns:
        list[gval.IncomeGroupRussia]: Список групп дохода в порядке следования в строке.
    """
    # Проверяем, является ли строка диапазоном (например, "A-C")
    if '-' in income_group_str:
        parts: list[str] = income_group_str.split('-')
        if len(parts) == 2 and len(parts[0]) == 1 and len(parts[1]) == 1:
            start_char: str = parts[0]
            end_char: str = parts[1]
            # Генерируем диапазон букв от start до end
            start_ord: int = ord(start_char)
            end_ord: int = ord(end_char)
            return [
                _INCOME_GROUP_MAPPING[chr(code)]
                for code in range(start_ord, end_ord + 1)
                if chr(code) in _INCOME_GROUP_MAPPING
            ]

    # Преобразуем каждую букву в строке в соответствующий объект группы дохода
    return [_INCOME_GROUP_MAPPING[char] for char in income_group_str if char in _INCOME_GROUP_MAPPING]


def _parse_kids_age(age_start: str, age_end: str) -> dict[str, list[KidsAgeYesType]]:
    """Парсит диапазон возраста детей и возвращает словарь с фильтрами.

    Маппинг возрастов детей на поля фильтров:
    - KidsAge2: До 1 года (0)
    - KidsAge3: 1 год (1)
    - KidsAge4: 2-3 года (2, 3)
    - KidsAge5: 4-6 лет (4, 5, 6)
    - KidsAge6: 7-11 лет (7, 8, 9, 10, 11)
    - KidsAge7: 12-15 лет (12, 13, 14, 15)

    Args:
        age_start (str): Начальный возраст детей.
        age_end (str): Конечный возраст детей.

    Returns:
        dict[str, list[KidsAgeYesType]]: Словарь с именами полей фильтров и их значениями.
    """
    start: int = int(age_start)
    end: int = int(age_end)

    result: dict[str, list[KidsAgeYesType]] = {}

    for age in range(start, end + 1):
        if age in _KIDS_AGE_TO_FIELD_MAPPING:
            field_name, enum_value = _KIDS_AGE_TO_FIELD_MAPPING[age]
            if field_name not in result:
                result[field_name] = [enum_value]
            elif enum_value not in result[field_name]:
                result[field_name].append(enum_value)

    return result


def _parse_spendings_on_food(food_start: str, food_end: str | None) -> list[gval.SpendingsOnFood]:
    """Парсит диапазон затрат на питание и возвращает список объектов SpendingsOnFood.

    Args:
        food_start (str): Начальный уровень затрат на питание.
        food_end (str | None): Конечный уровень затрат на питание (опционально).

    Returns:
        list[gval.SpendingsOnFood]: Список уровней затрат на питание.
    """
    start: int = int(food_start)
    end: int = int(food_end) if food_end else start

    return [_SPENDINGS_ON_FOOD_MAPPING[level] for level in range(start, end + 1)]
