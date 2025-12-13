from datetime import date

from pydantic import AfterValidator, BaseModel, Field, computed_field, model_validator
from typing_extensions import Annotated, Any, Optional, Self, Sequence

from telemars.params.filters import general as gval
from telemars.utils.functools import gen_flt_expr, group_consecutive
from telemars.utils.validators import UniqueSequence, WithinRange


class BaseFilter(BaseModel):
    """Базовый фильтр."""

    @computed_field
    @property
    def expr(self) -> Optional[str]:
        """Возвращает фильтр-выражение для запроса к API."""
        expr_parts: list[str] = []

        for field_name, field in self.__class__.model_fields.items():
            mediascope: str = field.json_schema_extra.get('mediascope') if field.json_schema_extra else None
            value: Any = getattr(self, field_name)

            if (flt := gen_flt_expr(mediascope, value)) is not None:
                expr_parts.append(flt)

        return ' AND '.join(expr_parts) if expr_parts else None


class DateFilter(BaseModel):
    """Фильтр по периоду."""

    date_from: Annotated[date, Field(title='Нижняя граница периода (включительно)')]
    date_to: Annotated[date, Field(title='Верхняя граница периода (включительно)')]

    @model_validator(mode='after')
    def check_dates(self) -> Self:
        """Проверяет корректность дат."""
        if self.date_from > self.date_to:
            raise ValueError('Дата начала периода не может быть позднее даты окончания.')

        if self.date_to > date.today():
            raise ValueError('Дата окончания периода не может быть позднее текущей даты.')

        return self

    @computed_field
    @property
    def expr(self) -> list[tuple[str, str]]:
        """Возвращает фильтр-выражение для запроса к API."""
        return [(self.date_from.strftime('%Y-%m-%d'), self.date_to.strftime('%Y-%m-%d'))]


class WeekdayFilter(BaseFilter):
    """Фильтр по дню недели."""

    research_week_day: Annotated[
        Optional[Sequence[gval.Weekday]],
        Field(
            title='День недели',
            default=None,
            min_length=1,
            max_length=len(gval.Weekday),
            json_schema_extra={'mediascope': 'researchWeekDay'},
        ),
        AfterValidator(UniqueSequence()),
    ]


class DaytypeFilter(BaseFilter):
    """Фильтр по типу дня."""

    research_day_type: Annotated[
        Optional[Sequence[gval.DayType]],
        Field(
            title='Тип дня',
            default=None,
            min_length=1,
            max_length=len(gval.DayType),
            json_schema_extra={'mediascope': 'researchDayType'},
        ),
        AfterValidator(UniqueSequence()),
    ]


class LocationFilter(BaseFilter):
    """Фильтр по месту просмотра."""

    location_id: Annotated[
        Optional[Sequence[gval.Location]],
        Field(
            title='ID места просмотра',
            default=None,
            min_length=1,
            max_length=len(gval.Location),
            json_schema_extra={'mediascope': 'locationId'},
        ),
        AfterValidator(UniqueSequence()),
    ]


class CompanyFilter(BaseFilter):
    """Фильтр по телекомпании."""

    tv_company_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='ID телекомпании',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'tvCompanyId'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    tv_thematic_id: Annotated[
        Optional[Sequence[gval.TvThematicId]],
        Field(
            title='ID жанра тематического канала',
            default=None,
            min_length=1,
            max_length=len(gval.TvThematicId),
            json_schema_extra={'mediascope': 'tvThematicId'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    tv_net_id: Annotated[
        Optional[Sequence[gval.TvNetId]],
        Field(
            title='ID телесети',
            default=None,
            min_length=1,
            max_length=len(gval.TvNetId),
            json_schema_extra={'mediascope': 'tvNetId'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    region_id: Annotated[
        Optional[Sequence[gval.RegionId]],
        Field(
            title='ID региона',
            default=None,
            min_length=1,
            max_length=len(gval.RegionId),
            json_schema_extra={'mediascope': 'regionId'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    tv_company_holding_id: Annotated[
        Optional[Sequence[gval.TvCompanyHoldingId]],
        Field(
            title='ID холдинга',
            default=None,
            min_length=1,
            max_length=len(gval.TvCompanyHoldingId),
            json_schema_extra={'mediascope': 'tvCompanyHoldingId'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    tv_company_media_holding_id: Annotated[
        Optional[Sequence[gval.TvCompanyMediaHoldingId]],
        Field(
            title='ID медиахолдинга',
            default=None,
            min_length=1,
            max_length=len(gval.TvCompanyMediaHoldingId),
            json_schema_extra={'mediascope': 'tvCompanyMediaHoldingId'},
        ),
        AfterValidator(UniqueSequence()),
    ]


class BaseDemoFilter(BaseFilter):
    """Фильтр по базовой аудитории."""

    sex: Annotated[
        Optional[gval.Sex],
        Field(
            title='Пол',
            default=None,
            json_schema_extra={'mediascope': 'sex'},
        ),
    ]
    age: Annotated[
        Optional[tuple[int, int]],
        Field(
            title='Возраст',
            default=None,
            json_schema_extra={'mediascope': 'age'},
        ),
        AfterValidator(WithinRange(4, 99)),
    ]
    education: Annotated[
        Optional[Sequence[gval.Education]],
        Field(
            title='Образование',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'education'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    work: Annotated[
        Optional[Sequence[gval.Work]],
        Field(
            title='Занятость',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'work'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    pers_num: Annotated[
        Optional[Sequence[gval.PersNum]],
        Field(
            default=None,
            title='Количество членов семьи',
            min_length=1,
            json_schema_extra={'mediascope': 'persNum'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    spendings_on_food: Annotated[
        Optional[Sequence[gval.SpendingsOnFood]],
        Field(
            title='Затраты на питание',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'spendingsOnFood'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    tv_num: Annotated[
        Optional[Sequence[gval.TvNum]],
        Field(
            title='Количество телевизоров',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'tvNum'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    age_group: Annotated[
        Optional[Sequence[gval.AgeGroup]],
        Field(
            title='Возрастная группа',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'ageGroup'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    income_group_russia: Annotated[
        Optional[Sequence[gval.IncomeGroupRussia]],
        Field(
            title='Группа дохода по России',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'incomeGroupRussia'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    housewife: Annotated[
        Optional[Sequence[gval.Housewife]],
        Field(
            title='Ответственный за покупку продуктов',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'housewife'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    income_earner: Annotated[
        Optional[Sequence[gval.IncomeEarner]],
        Field(
            title='Основной вклад в бюджет',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'incomeEarner'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    inc_level: Annotated[
        Optional[Sequence[gval.IncLevel]],
        Field(
            title='Уровень дохода',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'incLevel'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    kids_num: Annotated[
        Optional[Sequence[gval.KidsNum]],
        Field(
            title='Количество детей',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'kidsNum'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    kids_age1: Annotated[
        Optional[Sequence[gval.KidsAge1]],
        Field(
            title='Возраст детей: Нет детей',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'kidsAge1'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    kids_age2: Annotated[
        Optional[Sequence[gval.KidsAge2]],
        Field(
            title='Возраст детей: До 1 года',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'kidsAge2'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    kids_age3: Annotated[
        Optional[Sequence[gval.KidsAge3]],
        Field(
            title='Возраст детей: 1 год',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'kidsAge3'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    kids_age4: Annotated[
        Optional[Sequence[gval.KidsAge4]],
        Field(
            title='Возраст детей: 2-3 года',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'kidsAge4'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    kids_age5: Annotated[
        Optional[Sequence[gval.KidsAge5]],
        Field(
            title='Возраст детей: 4-6 лет',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'kidsAge5'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    kids_age6: Annotated[
        Optional[Sequence[gval.KidsAge6]],
        Field(
            title='Возраст детей: 7-11 лет',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'kidsAge6'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    kids_age7: Annotated[
        Optional[Sequence[gval.KidsAge7]],
        Field(
            title='Возраст детей: 12-15 лет',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'kidsAge7'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    status: Annotated[
        Optional[Sequence[gval.Status]],
        Field(
            title='Род занятий',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'status'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    business: Annotated[
        Optional[Sequence[gval.Business]],
        Field(
            title='Отрасль деятельности',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'business'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    enterprise: Annotated[
        Optional[Sequence[gval.Enterprise]],
        Field(
            title='Тип предприятия',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'enterprise'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    property: Annotated[
        Optional[Sequence[gval.Property]],
        Field(
            title='Отношение к собственности',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'property'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    marital_status: Annotated[
        Optional[Sequence[gval.MaritalStatus]],
        Field(
            title='Семейное положение',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'maritalStatus'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    life_cycle: Annotated[
        Optional[Sequence[gval.LifeCycle]],
        Field(
            title='Цикл семейной жизни',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'lifeCycle'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    internet: Annotated[
        Optional[Sequence[gval.Internet]],
        Field(
            title='Наличие интернета',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'internet'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    dacha: Annotated[
        Optional[Sequence[gval.Dacha]],
        Field(
            title='Наличие дачи',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'dacha'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    federal_okrug: Annotated[
        Optional[Sequence[gval.FederalOkrug]],
        Field(
            title='Федеральный округ',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'federalOkrug'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    income_scale201401: Annotated[
        Optional[Sequence[gval.IncomeScale201401]],
        Field(
            title='Шкала дохода',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'incomeScale201401'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    equipment_v2: Annotated[
        Optional[Sequence[gval.EquipmentV2]],
        Field(
            title='Дополнительное оборудование',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'equipmentV2'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    wgh_suburb_age_group: Annotated[
        Optional[Sequence[gval.WghSuburbAgeGroup]],
        Field(
            title='Возрастная группа WGH',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'wghSuburbAgeGroup'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    wgh_dacha_tv_exist: Annotated[
        Optional[Sequence[gval.WghDachaTvExist]],
        Field(
            default=None,
            title='Наличие дачи с ТВ',
            min_length=1,
            json_schema_extra={'mediascope': 'wghDachaTvExist'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    smart_tv_yes_no: Annotated[
        Optional[Sequence[gval.SmartTvYesNo]],
        Field(
            title='Наличие Смарт ТВ',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'smartTvYesNo'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    wgh_video_game_wo_age: Annotated[
        Optional[Sequence[gval.WghVideoGameWoAge]],
        Field(
            title='Наличие видеотехники',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'wghVideoGameWoAge'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    wgh_usb_tv_hh: Annotated[
        Optional[Sequence[gval.WghUsbTvHh]],
        Field(
            title='Наличие USB',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'wghUsbTvHh'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    cube_city: Annotated[
        Optional[Sequence[gval.CubeCity]],
        Field(
            title='Саморепрезентирующиеся города',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'cubeCity'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    timezone0: Annotated[
        Optional[Sequence[gval.Timezone0]],
        Field(
            title='Часовой пояс ноль',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'timezone0'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    cube100_plus100_minus: Annotated[
        Optional[Sequence[gval.Cube100Plus100Minus]],
        Field(
            title='Население 100+ или 100-',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'cube100Plus100Minus'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    sputnik_tv: Annotated[
        Optional[Sequence[gval.SputnikTv]],
        Field(
            title='Наличие спутниковой тарелки',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'sputnikTv'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    geo_from082020: Annotated[
        Optional[Sequence[gval.GeoFrom082020]],
        Field(
            title='География',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'geoFrom082020'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    video: Annotated[
        Optional[Sequence[gval.Video]],
        Field(
            title='Наличие видеотехники',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'video'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    income_group: Annotated[
        Optional[Sequence[gval.IncomeGroup]],
        Field(
            title='Группа дохода по городам',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'incomeGroup'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    kids_age_c1: Annotated[
        Optional[Sequence[gval.KidsAgeC1]],
        Field(
            title='Возраст детей: 0-2 года',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'kidsAgeC1'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    kids_age_c2: Annotated[
        Optional[Sequence[gval.KidsAgeC2]],
        Field(
            title='Возраст детей: 3-6 лет',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'kidsAgeC2'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    kids_age_c3: Annotated[
        Optional[Sequence[gval.KidsAgeC3]],
        Field(
            title='Возраст детей: 7-11 лет',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'kidsAgeC3'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    kids_age_c4: Annotated[
        Optional[Sequence[gval.KidsAgeC4]],
        Field(
            title='Возраст детей: 12-15 лет',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'kidsAgeC4'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    occupation: Annotated[
        Optional[Sequence[gval.Occupation]],
        Field(
            title='Род занятий',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'occupation'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    trade_industry: Annotated[
        Optional[Sequence[gval.TradeIndustry]],
        Field(
            title='Отрасль деятельности',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'tradeIndustry'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    city: Annotated[
        Optional[Sequence[gval.City]],
        Field(
            title='Город',
            default=None,
            min_length=1,
            json_schema_extra={'mediascope': 'city'},
        ),
        AfterValidator(UniqueSequence()),
    ]

    @computed_field
    @property
    def expr(self) -> Optional[str]:
        """Возвращает фильтр-выражение для запроса к API."""
        expr_parts: list[str] = []

        for field_name, field in self.__class__.model_fields.items():
            mediascope: str = field.json_schema_extra.get('mediascope') if field.json_schema_extra else None
            value: Any = getattr(self, field_name)

            if field_name == 'age' and value is not None:
                expr_parts.append(f'{mediascope} >= {value[0]} AND {mediascope} <= {value[1]}')
            elif (flt := gen_flt_expr(mediascope, value)) is not None:
                expr_parts.append(flt)

        return ' AND '.join(expr_parts) if expr_parts else None

    # TODO: Реализовать оставшиеся параметры целевой аудитории.
    @computed_field
    @property
    def name(self) -> Optional[str]:
        """Возвращает имя аудитории."""

        if self.expr is None:
            return None

        name_parts: list[str] = []

        # Пол.
        if self.sex is not None:
            name_parts.append('M' if self.sex == gval.Sex.MALE else 'W')
        else:
            name_parts.append('All')

        # Возраст.
        if self.age[1] == 99:
            name_parts.append('{}+'.format(self.age[0]))
        else:
            name_parts.append('{}-{}'.format(self.age[0], self.age[1]))

        # Уровень дохода.
        if self.inc_level is not None:
            ils: list[int] = sorted([inc_level.value for inc_level in self.inc_level])

            if len(ils) == 1:
                name_parts.append('IL {}'.format(ils[0]))
            else:
                name_parts.append('IL {}'.format(','.join(group_consecutive(ils))))

        # Группа дохода.
        if self.income_group_russia is not None:
            # Маппинг значений на буквенные обозначения
            value_to_letter: dict[int, str] = {1: 'A', 2: 'B', 3: 'C'}
            # Фильтруем NA (значение 4) и преобразуем в буквы
            letters: list[str] = sorted([value_to_letter[ig.value] for ig in self.income_group_russia if ig.value != 4])

            if letters:  # Добавляем только если есть валидные группы
                name_parts.append(''.join(letters))

        # Возраст детей.
        kids_age_mappings: dict[str, dict[Any, str]] = {
            'kids_age1': {gval.KidsAge1.YES: 'NO KIDS'},
            'kids_age2': {gval.KidsAge2.YES: 'KIDS AGE 0'},
            'kids_age3': {gval.KidsAge3.YES: 'KIDS AGE 1'},
            'kids_age4': {gval.KidsAge4.YES: 'KIDS AGE 2-3'},
            'kids_age5': {gval.KidsAge5.YES: 'KIDS AGE 4-6'},
            'kids_age6': {gval.KidsAge6.YES: 'KIDS AGE 7-11'},
            'kids_age7': {gval.KidsAge7.YES: 'KIDS AGE 12-15'},
        }

        # Собираем все активные возрастные группы детей.
        active_kids_ages = []
        for field_name, mapping in kids_age_mappings.items():
            field_value = getattr(self, field_name)
            if field_value is not None and len(field_value) == 1:
                kids_age_value = field_value[0]
                if kids_age_value in mapping:
                    active_kids_ages.append(field_name)

        # Обрабатываем возрастные группы детей.
        if len(active_kids_ages) == 1:
            # Одиночное значение
            field_name = active_kids_ages[0]
            mapping = kids_age_mappings[field_name]
            field_value = getattr(self, field_name)
            kids_age_value = field_value[0]
            name_parts.append(mapping[kids_age_value])
        elif len(active_kids_ages) > 1:
            # Исключаем kids_age1 из комбинаций (NO KIDS несовместимо с другими).
            combo_ages = [age for age in active_kids_ages if age != 'kids_age1']

            if not combo_ages:
                # Если только kids_age1.
                name_parts.append('NO KIDS')
            else:
                # Определяем возрастные диапазоны
                age_ranges = {
                    'kids_age2': (0, 0),  # 0 лет
                    'kids_age3': (1, 1),  # 1 год
                    'kids_age4': (2, 3),  # 2-3 года
                    'kids_age5': (4, 6),  # 4-6 лет
                    'kids_age6': (7, 11),  # 7-11 лет
                    'kids_age7': (12, 15),  # 12-15 лет
                }

                # Собираем все возрастные диапазоны.
                all_ages = []
                for age_field in sorted(combo_ages):
                    if age_field in age_ranges:
                        min_age, max_age = age_ranges[age_field]
                        all_ages.extend(range(min_age, max_age + 1))

                # Удаляем дубликаты и сортируем.
                unique_ages = sorted(set(all_ages))

                # Группируем последовательные возрасты.
                ranges = []
                start = unique_ages[0]
                end = start

                for age in unique_ages[1:]:
                    if age == end + 1:
                        end = age
                    else:
                        if start == end:
                            ranges.append(str(start))
                        else:
                            ranges.append(f'{start}-{end}')
                        start = end = age

                # Добавляем последний диапазон.
                if start == end:
                    ranges.append(str(start))
                else:
                    ranges.append(f'{start}-{end}')

                name_parts.append(f'KIDS AGE {",".join(ranges)}')

        # Количество детей.
        if self.kids_num is not None and len(self.kids_num) == 1:
            kids_num_mapping: dict[gval.KidsNum, str] = {
                gval.KidsNum.NO_KIDS: 'NO KIDS',
                gval.KidsNum.ONE_KID: 'ONE KID',
                gval.KidsNum.TWO_KIDS: 'TWO KIDS',
                gval.KidsNum.THREE_OR_MORE_KIDS: 'THREE+ KIDS',
            }
            kids_num_value = self.kids_num[0]
            if kids_num_value in kids_num_mapping:
                name_parts.append(kids_num_mapping[kids_num_value])

        return ' '.join(name_parts)


# Класс идентичен BaseDemoFilter, поэтому наследуем.
class TargetDemoFilter(BaseDemoFilter):
    """Фильтр по целевой аудитории."""

    pass


class ProgramFilter(BaseFilter):
    """Фильтр по программе."""

    program_is_child: Annotated[
        Optional[gval.ProgramIsChild],
        Field(
            title='Программа детская',
            default=None,
            json_schema_extra={'mediascope': 'programIsChild'},
        ),
    ]
    program_producer_year: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Программа дата создания',
            default=None,
            description='Год создания.',
            json_schema_extra={'mediascope': 'programProducerYear'},
        ),
        AfterValidator(UniqueSequence()),
        AfterValidator(WithinRange(1900, date.today().year)),
    ]
    program_start_time: Annotated[
        Optional[int],
        Field(
            title='Программа время начала',
            default=None,
            ge=0,
            le=240000,
            description='В формате ЧЧ:ММ:СС.',
            json_schema_extra={'mediascope': 'programStartTime'},
        ),
    ]
    program_finish_time: Annotated[
        Optional[int],
        Field(
            title='Программа время окончания',
            default=None,
            ge=0,
            le=240000,
            description='В формате ЧЧ:ММ:СС.',
            json_schema_extra={'mediascope': 'programFinishTime'},
        ),
    ]
    program_duration: Annotated[
        Optional[int],
        Field(
            title='Программа продолжительность',
            default=None,
            ge=0,
            le=86400,
            description='В секундах.',
            json_schema_extra={'mediascope': 'programDuration'},
        ),
    ]
    program_spot_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Программа ID выхода',
            default=None,
            json_schema_extra={'mediascope': 'programSpotId'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    program_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Программа ID',
            default=None,
            json_schema_extra={'mediascope': 'programId'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    program_group_id: Annotated[
        Optional[Sequence[gval.ProgramGroupID]],
        Field(
            title='Программа групповое имя ID',
            default=None,
            json_schema_extra={'mediascope': 'programGroupId'},
        ),
    ]
    program_type_id: Annotated[
        Optional[Sequence[gval.ProgramTypeID]],
        Field(
            title='Программа жанр ID',
            default=None,
            json_schema_extra={'mediascope': 'programTypeId'},
        ),
    ]
    program_country_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Программа страна производства ID',
            default=None,
            json_schema_extra={'mediascope': 'programCountryId'},
        ),
    ]
    program_category_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Программа категория ID',
            default=None,
            json_schema_extra={'mediascope': 'programCategoryId'},
        ),
    ]
    program_sport_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Программа вид спорта ID',
            default=None,
            json_schema_extra={'mediascope': 'programSportId'},
        ),
    ]
    program_sport_group_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Программа группа спорта ID',
            default=None,
            json_schema_extra={'mediascope': 'programSportGroupId'},
        ),
    ]
    program_producer_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Программа производитель ID',
            default=None,
            json_schema_extra={'mediascope': 'programProducerId'},
        ),
    ]
    program_is_live: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Программа особенность эфира',
            default=None,
            json_schema_extra={'mediascope': 'programIsLive'},
        ),
    ]
    program_first_issue_date: Annotated[
        Optional[str],
        Field(
            title='Программа дата первого выхода',
            default=None,
            json_schema_extra={'mediascope': 'programFirstIssueDate'},
        ),
    ]
    program_language_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Программа язык ID',
            default=None,
            json_schema_extra={'mediascope': 'programLanguageId'},
        ),
    ]
    program_age_restriction_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Программа возрастное ограничение ID',
            default=None,
            json_schema_extra={'mediascope': 'programAgeRestrictionId'},
        ),
    ]
    program_producer_country_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Программа тип производства ID',
            default=None,
            json_schema_extra={'mediascope': 'programProducerCountryId'},
        ),
    ]
    program_breaks_count: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Блок количество в программе',
            default=None,
            json_schema_extra={'mediascope': 'programBreaksCount'},
        ),
    ]


class BreakFilter(BaseFilter):
    """Фильтр по блоку."""

    breaks_start_time: Annotated[
        Optional[str],
        Field(
            title='Блок время начала',
            default=None,
            json_schema_extra={'mediascope': 'breaksStartTime'},
        ),
    ]
    breaks_finish_time: Annotated[
        Optional[str],
        Field(
            title='Блок время окончания',
            default=None,
            json_schema_extra={'mediascope': 'breaksFinishTime'},
        ),
    ]
    breaks_duration: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Блок продолжительность',
            default=None,
            json_schema_extra={'mediascope': 'breaksDuration'},
        ),
    ]
    breaks_spot_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Блок ID выхода',
            default=None,
            json_schema_extra={'mediascope': 'breaksSpotId'},
        ),
    ]
    breaks_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Блок ID',
            default=None,
            json_schema_extra={'mediascope': 'breaksId'},
        ),
    ]
    breaks_style_id: Annotated[
        Optional[Sequence[gval.BreaksStyleId]],
        Field(
            title='Блок стиль ID',
            default=None,
            json_schema_extra={'mediascope': 'breaksStyleId'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    breaks_distribution_type: Annotated[
        Optional[Sequence[gval.BreaksDistributionType]],
        Field(
            title='Блок распространение ID',
            default=None,
            json_schema_extra={'mediascope': 'breaksDistributionType'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    breaks_position_type: Annotated[
        Optional[Sequence[gval.BreaksPositionType]],
        Field(
            title='Блок тип ID',
            default=None,
            json_schema_extra={'mediascope': 'breaksPositionType'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    breaks_content_type: Annotated[
        Optional[Sequence[gval.BreaksContentType]],
        Field(
            title='Блок содержание ID',
            default=None,
            json_schema_extra={'mediascope': 'breaksContentType'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    breaks_position: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Блок позиция в программе',
            default=None,
            json_schema_extra={'mediascope': 'breaksPosition'},
        ),
    ]
    grp_type_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='GRP баинговая ID',
            default=None,
            json_schema_extra={'mediascope': 'grpTypeId'},
        ),
    ]
    price: Annotated[
        Optional[Sequence[float]],
        Field(
            title='Блок цена минутная USD',
            default=None,
            json_schema_extra={'mediascope': 'price'},
        ),
    ]
    price_rub: Annotated[
        Optional[Sequence[float]],
        Field(
            title='Блок цена минутная RUB',
            default=None,
            json_schema_extra={'mediascope': 'priceRub'},
        ),
    ]
    grp_price: Annotated[
        Optional[Sequence[float]],
        Field(
            title='Блок цена GRP',
            default=None,
            json_schema_extra={'mediascope': 'grpPrice'},
        ),
    ]
    grp_price_rub: Annotated[
        Optional[Sequence[float]],
        Field(
            title='Блок цена по GRP РУБ',
            default=None,
            json_schema_extra={'mediascope': 'grpPriceRub'},
        ),
    ]
    grp_cost: Annotated[
        Optional[Sequence[float]],
        Field(
            title='Стоимость по GRP',
            default=None,
            json_schema_extra={'mediascope': 'grpCost'},
        ),
    ]
    grp_cost_rub: Annotated[
        Optional[Sequence[float]],
        Field(
            title='Стоимость по GRP РУБ',
            default=None,
            json_schema_extra={'mediascope': 'grpCostRub'},
        ),
    ]
    breaks_ad_count: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Блок количество роликов',
            default=None,
            json_schema_extra={'mediascope': 'breaksAdCount'},
        ),
    ]
    breaks_prime_time_status_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Prime / OffPrime блоков ID',
            default=None,
            json_schema_extra={'mediascope': 'breaksPrimeTimeStatusId'},
        ),
    ]
    breaks_issue_status_id: Annotated[
        Optional[Sequence[gval.BreaksIssueStatusId]],
        Field(
            title='Блок статус ID',
            default=None,
            json_schema_extra={'mediascope': 'breaksIssueStatusId'},
        ),
    ]


class AdFilter(BaseFilter):
    """Фильтр по ролику."""

    ad_start_time: Annotated[
        Optional[str],
        Field(
            title='Время начала',
            default=None,
            json_schema_extra={'mediascope': 'adStartTime'},
        ),
    ]
    ad_finish_time: Annotated[
        Optional[str],
        Field(
            title='Время окончания',
            default=None,
            json_schema_extra={'mediascope': 'adFinishTime'},
        ),
    ]
    ad_standard_duration: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Ролик ожидаемая длительность',
            default=None,
            json_schema_extra={'mediascope': 'adStandardDuration'},
        ),
    ]
    ad_spot_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Ролик ID выхода',
            default=None,
            json_schema_extra={'mediascope': 'adSpotId'},
        ),
    ]
    ad_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Ролик ID',
            default=None,
            json_schema_extra={'mediascope': 'adId'},
        ),
    ]
    ad_type_id: Annotated[
        Optional[Sequence[gval.AdTypeId]],
        Field(
            title='Ролик тип ID',
            default=None,
            json_schema_extra={'mediascope': 'adTypeId'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    ad_style_id: Annotated[
        Optional[Sequence[gval.AdStyleId]],
        Field(
            title='Ролик стиль ID',
            default=None,
            json_schema_extra={'mediascope': 'adStyleId'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    ad_first_issue_date: Annotated[
        Optional[str],
        Field(
            title='Ролик дата первого выхода',
            default=None,
            json_schema_extra={'mediascope': 'adFirstIssueDate'},
        ),
    ]
    ad_slogan_audio_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Ролик аудио слоган ID',
            default=None,
            json_schema_extra={'mediascope': 'adSloganAudioId'},
        ),
    ]
    ad_slogan_video_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Ролик видео слоган ID',
            default=None,
            json_schema_extra={'mediascope': 'adSloganVideoId'},
        ),
    ]
    ad_issue_status_id: Annotated[
        Optional[Sequence[gval.AdIssueStatusId]],
        Field(
            title='Ролик статус ID',
            default=None,
            json_schema_extra={'mediascope': 'adIssueStatusId'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    ad_distribution_type: Annotated[
        Optional[Sequence[gval.AdDistributionType]],
        Field(
            title='Ролик распространение ID',
            default=None,
            json_schema_extra={'mediascope': 'adDistributionType'},
        ),
        AfterValidator(UniqueSequence()),
    ]
    advertiser_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Рекламодатель ID',
            default=None,
            json_schema_extra={'mediascope': 'advertiserId'},
        ),
    ]
    brand_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Бренд ID',
            default=None,
            json_schema_extra={'mediascope': 'brandId'},
        ),
    ]
    subbrand_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Суббренд ID',
            default=None,
            json_schema_extra={'mediascope': 'subbrandId'},
        ),
    ]
    model_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Продукт ID',
            default=None,
            json_schema_extra={'mediascope': 'modelId'},
        ),
    ]
    article_level1_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Товарная категория 1 ID',
            default=None,
            json_schema_extra={'mediascope': 'articleLevel1Id'},
        ),
    ]
    article_level2_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Товарная категория 2 ID',
            default=None,
            json_schema_extra={'mediascope': 'articleLevel2Id'},
        ),
    ]
    article_level3_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Товарная категория 3 ID',
            default=None,
            json_schema_extra={'mediascope': 'articleLevel3Id'},
        ),
    ]
    article_level4_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Товарная категория 4 ID',
            default=None,
            json_schema_extra={'mediascope': 'articleLevel4Id'},
        ),
    ]
    advertiser_list_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Список рекламодателей ID',
            default=None,
            json_schema_extra={'mediascope': 'advertiserListId'},
        ),
    ]
    brand_list_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Список брендов ID',
            default=None,
            json_schema_extra={'mediascope': 'brandListId'},
        ),
    ]
    subbrand_list_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Список суббрендов ID',
            default=None,
            json_schema_extra={'mediascope': 'subbrandListId'},
        ),
    ]
    model_list_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Список продуктов ID',
            default=None,
            json_schema_extra={'mediascope': 'modelListId'},
        ),
    ]
    article_list2_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Список товарных категорий 2 ID',
            default=None,
            json_schema_extra={'mediascope': 'articleList2Id'},
        ),
    ]
    article_list3_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Список товарных категорий 3 ID',
            default=None,
            json_schema_extra={'mediascope': 'articleList3Id'},
        ),
    ]
    article_list4_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Список товарных категорий 4 ID',
            default=None,
            json_schema_extra={'mediascope': 'articleList4Id'},
        ),
    ]
    ad_age_restriction_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Ролик возрастное ограничение ID',
            default=None,
            json_schema_extra={'mediascope': 'adAgeRestrictionId'},
        ),
    ]
    ad_position_type: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Ролик позиционирование ID',
            default=None,
            json_schema_extra={'mediascope': 'adPositionType'},
        ),
    ]
    ad_position_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Ролик позиция в блоке',
            default=None,
            json_schema_extra={'mediascope': 'adPositionId'},
        ),
    ]
    ad_prime_time_status_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Prime / OffPrime роликов ID',
            default=None,
            json_schema_extra={'mediascope': 'adPrimeTimeStatusId'},
        ),
    ]
    ad_tv_area_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Ролик область выхода ID',
            default=None,
            json_schema_extra={'mediascope': 'adTvAreaId'},
        ),
    ]
    advertiser_tv_area_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Рекламодатель область выхода ID',
            default=None,
            json_schema_extra={'mediascope': 'advertiserTvAreaId'},
        ),
    ]
    brand_tv_area_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Бренд область выхода ID',
            default=None,
            json_schema_extra={'mediascope': 'brandTvAreaId'},
        ),
    ]
    subbrand_tv_area_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Суббренд область выхода ID',
            default=None,
            json_schema_extra={'mediascope': 'subbrandTvAreaId'},
        ),
    ]
    model_tv_area_id: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Модель область выхода ID',
            default=None,
            json_schema_extra={'mediascope': 'modelTvAreaId'},
        ),
    ]
    qr: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Ролик наличие QR кода ID',
            default=None,
            json_schema_extra={'mediascope': 'qr'},
        ),
    ]
    qr_duration: Annotated[
        Optional[Sequence[int]],
        Field(
            title='Ролик продолжительность QR кода',
            default=None,
            json_schema_extra={'mediascope': 'qrDuration'},
        ),
    ]


class PlatformFilter(BaseFilter):
    """Фильтр по платформе."""

    platform_id: Annotated[
        Sequence[gval.Platform],
        Field(
            title='ID платформы',
            min_length=1,
            max_length=3,
            json_schema_extra={'mediascope': 'platformId'},
        ),
        AfterValidator(UniqueSequence()),
    ]


class PlayBackTypeFilter(BaseFilter):
    """Фильтр по типу Playback."""

    playback_type_id: Annotated[
        Sequence[gval.PlayBackType],
        Field(
            title='ID Playback',
            min_length=1,
            max_length=29,
            json_schema_extra={'mediascope': 'playBackTypeId'},
        ),
        AfterValidator(UniqueSequence()),
    ]
