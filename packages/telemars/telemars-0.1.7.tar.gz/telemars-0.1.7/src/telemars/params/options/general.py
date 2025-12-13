from enum import Enum


# NOTE: Далее идут перечисления, относящиеся к опциям расчета.
class KitId(Enum):
    """ID набора данных."""

    TV_INDEX_ALL_RUSSIA = 1  # TV Index All Russia.
    TV_INDEX_RUSSIA_100_PLUS = 2  # TV Index Russia 100+.
    TV_INDEX_CITIES = 3  # TV Index Cities.
    TV_INDEX_PLUS_ALL_RUSSIA = 4  # TV Index Plus All Russia.
    TV_INDEX_PLUS_RUSSIA_100_PLUS = 5  # TV Index Plus Russia 100+.
    TV_INDEX_MOSCOW = 6  # TV Index Moscow.
    BIG_TV = 7  # Big TV.
    TV_INDEX_RUSSIA_SPECIAL = 9  # TV Index Russia Special.
    TV_INDEX_MOSCOW_SPECIAL = 10  # TV Index Moscow Special.


class BigTv(Enum):
    """Флаг расчета Big TV."""

    NO = False  # Расчет не по Big TV.
    YES = True  # Расчет по Big TV (kit_id = 7).


class UseNbd(Enum):
    """Использование NBD коррекции при расчете накопленных охватов."""

    NO = False  # Не использовать NBD коррекцию.
    YES = True  # Использовать NBD коррекцию (по умолчанию).


class BaseDateCalcType(Enum):
    """Тип автоматического базового дня."""

    BY_RESEARCH_PERIOD = 'BY_RESEARCH_PERIOD'  # Средний день периода расчета (по умолчанию).
    BY_ISSUES = 'BY_ISSUES'  # Средний день периода выхода эфирных событий.


class OneBaseDatePerEachDateRange(Enum):
    """Формат определения базового дня для периодов в срезах."""

    COMMON_BASE_DATE = False  # Общий базовый день для всех периодов (по умолчанию).
    INDIVIDUAL_BASE_DATE = True  # Свой базовый день для каждого периода.


class TotalType(Enum):
    """Основание расчета Share и TTV статистик."""

    TOTAL_CHANNELS = 'TotalChannels'  # По всем каналам (по умолчанию).
    TOTAL_TV_SET = 'TotalTVSet'  # По всем включениям ТВ.
    TOTAL_CHANNELS_THEM = 'TotalChannelsThem'  # По выбранным каналам.


class StandardRtgUseDuration(Enum):
    """Настройка расчета standard Rtg по длительности."""

    CATALOG_DURATION = False  # По каталожной длительности (по умолчанию).
    REAL_DURATION = True  # По реальной длительности ролика.


class IssueType(Enum):
    """Тип события для расчета отчета Кросс-таблица."""

    PROGRAM = 'PROGRAM'  # Программы.
    BREAKS = 'BREAKS'  # Рекламные блоки.
    AD = 'AD'  # Рекламные ролики.


class ViewingSubject(Enum):
    """Единица расчета."""

    RESPONDENT = 'RESPONDENT'  # Респондент (по умолчанию).
    HOUSEHOLD = 'HOUSEHOLD'  # Домохозяйство.


# NOTE: Перечисление сортировки.
class SortOrder(Enum):
    """Порядок сортировки."""

    ASC = 'ASC'  # По возрастанию.
    DESC = 'DESC'  # По убыванию.
