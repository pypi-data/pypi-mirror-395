from enum import Enum


# NOTE: Перечисление относится к WeekdayFilter.
class Weekday(Enum):
    """День недели."""

    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


# NOTE: Перечисление относится к DaytypeFilter.
class DayType(Enum):
    """Тип дня."""

    WEEKEND = 'E'
    WEEKDAY = 'W'
    HOLIDAY = 'H'
    MOURNING_DAY = 'F'


# NOTE: Перечисление относится к LocationFilter.
class Location(Enum):
    """ID места просмотра."""

    HOME = 1
    DACHA = 2
    OUT_OF_HOME = 4


# NOTE: Далее идут перечисления, относящиеся к CompanyFilter.
class TvCompanyId(Enum):
    """ID телекомпании.

    Перечисление оставлено для консистентности, но не используется.
    """

    pass


class TvThematicId(Enum):
    """ID жанра тематического канала."""

    NA = 0  # N/A.
    MOVIES_AND_SERIES = 3  # Кино и сериалы.
    CHANNELS_TV_INDEX = 6  # Каналы ТВ Индекс.
    ENTERTAINING = 8  # Развлекательные.
    ETHNIC = 16  # Этнические.
    ADVERTISING = 19  # Рекламные.


class TvNetId(Enum):
    """ID телесети."""

    PERVY_KANAL = 1  # ПЕРВЫЙ КАНАЛ.
    ROSSIYA_1 = 2  # РОССИЯ 1.
    NTV = 4  # НТВ.
    MIR = 10  # МИР.
    STS = 11  # СТС.
    TV_TSENTR = 12  # ТВ ЦЕНТР.
    ROSSIYA_K = 13  # РОССИЯ К.
    STS_LOVE = 16  # СТС LOVE.
    KARUSEL = 40  # КАРУСЕЛЬ.
    REN_TV = 60  # РЕН ТВ.
    TNT = 83  # ТНТ.
    SOLNTSE = 84  # СОЛНЦЕ.
    MUZ_TV = 86  # МУЗ ТВ.
    FRIDAY = 204  # ПЯТНИЦА.
    U = 205  # Ю.
    TV_3 = 206  # ТВ-3.
    EURONEWS = 210  # EURONEWS.
    CHE = 255  # ЧЕ.
    ROSSIYA_2 = 256  # РОССИЯ 2.
    DOMASHNIY = 257  # ДОМАШНИЙ.
    ZVEZDA = 258  # ЗВЕЗДА.
    PYATY_KANAL = 259  # ПЯТЫЙ КАНАЛ.
    ROSSIYA_24 = 260  # РОССИЯ 24.
    RU_TV_TILL_31_12_2020 = 270  # RU.TV (ДО 31/12/2020).
    TWO_X_TWO = 286  # 2X2.
    MEASURED_LOCAL_TV = 300  # ИЗМЕРЯЕМОЕ ЛОКАЛЬНОЕ ТВ.
    VIDEO = 301  # ВИДЕО.
    MEASURED_THEMATIC_TV = 302  # ИЗМЕРЯЕМОЕ ТЕМАТИЧЕСКОЕ ТВ.
    OTHER = 303  # ДРУГОЕ.
    MATCH_TV = 326  # МАТЧ ТВ.
    TNT_4 = 329  # ТНТ 4.
    DISCOVERY_CHANNEL_TILL_31_12_2019 = 335  # DISCOVERY CHANNEL (ДО 31/12/2019).
    DOM_KINO = 340  # ДОМ КИНО.
    AD_CHANNELS = 348  # РЕКЛАМНЫЕ КАНАЛЫ.
    MULT = 356  # МУЛЬТ.
    SUBBOTA = 376  # СУББОТА.
    EVRONOVOSTI = 384  # ЕВРОНОВОСТИ.
    SPAS = 393  # СПАС.
    OTHER_TV_SET = 407  # OTHER TV SET.
    OTR_TILL_31_12_2020 = 430  # ОТР (ДО 31/12/2020).
    SOLOVIEVLIVE = 502  # СОЛОВЬЁВLIVE.
    MOSFILM_ZOLOTAYA_KOLLEKTSIYA = 545  # МОСФИЛЬМ. ЗОЛОТАЯ КОЛЛЕКЦИЯ.
    POBEDA = 563  # ПОБЕДА.
    RU_TV = 573  # RU.TV.
    OTR = 607  # ОТР.


class RegionId(Enum):
    """ID региона."""

    MOSCOW = 1  # МОСКВА.
    SAINT_PETERSBURG = 2  # САНКТ-ПЕТЕРБУРГ.
    TVER = 3  # ТВЕРЬ.
    NIZHNIY_NOVGOROD = 4  # НИЖНИЙ НОВГОРОД.
    VOLGOGRAD = 5  # ВОЛГОГРАД.
    SAMARA = 6  # САМАРА.
    YAROSLAVL = 7  # ЯРОСЛАВЛЬ.
    VORONEZH = 8  # ВОРОНЕЖ.
    ROSTOV_ON_DON = 9  # РОСТОВ-НА-ДОНУ.
    SARATOV = 10  # САРАТОВ.
    EKATERINBURG = 12  # ЕКАТЕРИНБУРГ.
    CHELYABINSK = 13  # ЧЕЛЯБИНСК.
    PERM = 14  # ПЕРМЬ.
    NOVOSIBIRSK = 15  # НОВОСИБИРСК.
    TYUMEN = 16  # ТЮМЕНЬ.
    KRASNOYARSK = 17  # КРАСНОЯРСК.
    VLADIVOSTOK = 18  # ВЛАДИВОСТОК.
    KAZAN = 19  # КАЗАНЬ.
    UFA = 20  # УФА.
    OMSK = 21  # ОМСК.
    KRASNODAR = 23  # КРАСНОДАР.
    IRKUTSK = 25  # ИРКУТСК.
    KHABAROVSK = 26  # ХАБАРОВСК.
    STAVROPOL = 39  # СТАВРОПОЛЬ.
    BARNAUL = 40  # БАРНАУЛ.
    KEMEROVO = 45  # КЕМЕРОВО.
    TOMSK = 55  # ТОМСК.
    NETWORK_BROADCASTING = 99  # СЕТЕВОЕ ВЕЩАНИЕ.
    INTERNET = 100  # ИНТЕРНЕТ.


class TvCompanyHoldingId(Enum):
    """ID холдинга."""

    DISCOVERY_INC = 1000003  # DISCOVERY, Inc.
    MEDIA_1 = 1000007  # МЕДИА 1.
    VIASAT = 1000014  # ВИАСАТ.
    GAZPROM_MEDIA_RAZVLEKATELNOE_TELEVIDENIE = 1000017  # ГАЗПРОМ-МЕДИА РАЗВЛЕКАТЕЛЬНОЕ ТЕЛЕВИДЕНИЕ.
    MTRK_MIR = 1000021  # МТРК МИР.
    TRK_VS_RF_ZVEZDA = 1000034  # ТРК ВС РФ ЗВЕЗДА.
    TSIFROVOE_TELEVIDENIE = 1000037  # ЦИФРОВОЕ ТЕЛЕВИДЕНИЕ.
    PERVY_KANAL_VSEMIRNAYA_SET = 1000039  # ПЕРВЫЙ КАНАЛ. ВСЕМИРНАЯ СЕТЬ.
    STS_MEDIA = 1000040  # СТС МЕДИА.
    VGTRK = 1000041  # ВГТРК.
    GAZPROM_MEDIA = 1000042  # ГАЗПРОМ-МЕДИА.
    NATSIONALNAYA_MEDIA_GRUPPA = 1000043  # НАЦИОНАЛЬНАЯ МЕДИА ГРУППА.
    RUSSIAN_MEDIA_GROUP = 1000044  # РУССКАЯ МЕДИА ГРУППА.
    MOSKVA_MEDIA = 1000046  # МОСКВА МЕДИА.


class TvCompanyMediaHoldingId(Enum):
    """ID медиахолдинга."""

    NA = 0  # N/A.
    MEDIA_1 = 1  # МЕДИА 1.
    VIASAT = 2  # ВИАСАТ.
    VGTRK_MEDIA_HOLDING = 6  # ВГТРК (Медиахолдинг).
    RUSSIAN_MEDIA_GROUP = 7  # РУССКАЯ МЕДИА ГРУППА.
    GAZPROM_MEDIA = 8  # ГАЗПРОМ-МЕДИА.
    NATSIONALNAYA_MEDIA_GRUPPA = 19  # НАЦИОНАЛЬНАЯ МЕДИА ГРУППА.


# NOTE: Далее идут перечисления, относящиеся к BaseDemoFilter и TargetDemoFilter.
class Sex(Enum):
    """Пол."""

    MALE = 1  # Мужской пол.
    FEMALE = 2  # Женский пол.


class Education(Enum):
    """Образование."""

    PRIMARY = 1  # Начальное образование.
    SECONDARY = 2  # Среднее образование.
    HIGHER = 3  # Высшее образование.


class Work(Enum):
    """Занятость."""

    WORKS_FULL_TIME = 1  # Работает полный день.
    WORKS_PART_TIME = 2  # Работает неполный день.
    NOT_WORKING = 3  # Не работает.


class PersNum(Enum):
    """Количество членов семьи."""

    ONE_PERSON = 1  # Один человек в семье.
    TWO_PERSONS = 2  # Два человека в семье.
    THREE_PERSONS = 3  # Три человека в семье.
    FOUR_PERSONS = 4  # Четыре человека в семье.
    FIVE_OR_MORE_PERSONS = 5  # Пять и более человек в семье.


class SpendingsOnFood(Enum):
    """Затраты на питание."""

    LESS_THAN_A_QUARTER = 1  # Меньше четверти.
    FROM_QUARTER_TO_HALF = 2  # От четверти до половины.
    FROM_HALF_TO_THREE_QUARTERS = 3  # От половины до трех четвертей.
    MORE_THAN_THREE_QUARTERS = 4  # Более трех четвертей.
    DIFFICULT_TO_ANSWER = 5  # Затрудняется ответить.


class TvNum(Enum):
    """Количество работающих телевизоров."""

    ONE_TV = 1  # Один телевизор.
    TWO_TVS = 2  # Два телевизора.
    THREE_OR_MORE_TVS = 3  # Три и более телевизоров.


class AgeGroup(Enum):
    """Возрастная группа."""

    BELOW_9 = 1  # Возрастная группа до 9 лет.
    FROM_10_TO_15 = 2  # Возрастная группа от 10 до 15 лет.
    FROM_16_TO_24 = 3  # Возрастная группа от 16 до 24 лет.
    FROM_25_TO_39 = 4  # Возрастная группа от 25 до 39 лет.
    FROM_40_TO_54 = 5  # Возрастная группа от 40 до 54 лет.
    FROM_55_TO_64 = 6  # Возрастная группа от 55 до 64 лет.
    ABOVE_65 = 7  # Возрастная группа 65 лет и старше.


class IncomeGroupRussia(Enum):
    """Группа дохода по России."""

    A = 1  # Группа дохода A.
    B = 2  # Группа дохода B.
    C = 3  # Группа дохода C.
    NA = 4  # Нет данных.


class Housewife(Enum):
    """Ответственный за покупку продуктов питания."""

    NO = 0  # Не является ответственным.
    YES = 1  # Является ответственным.


class IncomeEarner(Enum):
    """Основной вклад в семейный бюджет."""

    NO = 0  # Не вносит основной вклад.
    YES = 1  # Вносит основной вклад.


class Video(Enum):
    """Наличие видеотехники."""

    NO = 0  # Нет видеотехники.
    YES = 1  # Есть видеотехника.


class IncLevel(Enum):
    """Уровень дохода."""

    _1 = 1  # Денег не хватает даже на еду.
    _2 = 2  # Хватает на еду, но покупать одежду нет возможности.
    _3 = 3  # Хватает на еду и одежду, но нет возможности покупать дорогие вещи.
    _4 = 4  # Есть возможность покупать дорогие вещи, но не всё, что захочется.
    _5 = 5  # Полный достаток, нет ограничений в средствах.
    _6 = 6  # Затрудняется ответить.


class KidsNum(Enum):
    """Количество детей."""

    NO_KIDS = 1  # Детей нет.
    ONE_KID = 2  # Один ребенок.
    TWO_KIDS = 3  # Два ребенка.
    THREE_OR_MORE_KIDS = 4  # Три и более ребенка.


class KidsAge1(Enum):
    """Возраст детей: Нет детей."""

    NO = 0  # Неверно.
    YES = 1  # Верно.


class KidsAge2(Enum):
    """Возраст детей: До 1 года."""

    NO = 0  # Нет детей в данной возрастной группе.
    YES = 1  # Есть дети в данной возрастной группе.


class KidsAge3(Enum):
    """Возраст детей: 1 год."""

    NO = 0  # Нет детей в данной возрастной группе.
    YES = 1  # Есть дети в данной возрастной группе.


class KidsAge4(Enum):
    """Возраст детей: 2-3 года."""

    NO = 0  # Нет детей в данной возрастной группе.
    YES = 1  # Есть дети в данной возрастной группе.


class KidsAge5(Enum):
    """Возраст детей: 4-6 лет."""

    NO = 0  # Нет детей в данной возрастной группе.
    YES = 1  # Есть дети в данной возрастной группе.


class KidsAge6(Enum):
    """Возраст детей: 7-11 лет."""

    NO = 0  # Нет детей в данной возрастной группе.
    YES = 1  # Есть дети в данной возрастной группе.


class KidsAge7(Enum):
    """Возраст детей: 12-15 лет."""

    NO = 0  # Нет детей в данной возрастной группе.
    YES = 1  # Есть дети в данной возрастной группе.


class Status(Enum):
    """Род занятий."""

    MANAGER = 1  # Руководитель.
    SPECIALIST = 2  # Специалист.
    EMPLOYEE = 3  # Служащий.
    WORKER = 4  # Рабочий.
    STUDENT = 5  # Дошкольник, студент, учащийся.
    PENSIONER_DISABLED = 6  # Пенсионер, инвалид.
    UNEMPLOYED = 7  # Безработный, не работающий.
    HOUSEWIFE_YOUNG_MOTHER = 8  # Домохозяйка, молодая мать.
    INDIVIDUAL_BUSINESS = 9  # Индивидуальный бизнес.
    OWNER_CO_OWNER = 10  # Владелец, совладелец предприятия.
    OTHER = 11  # Другое.


class Business(Enum):
    """Отрасль деятельности."""

    TRADE_SERVICE_RESTAURANTS = 1  # Торговля, обслуживание, рестораны.
    TRANSPORT_WAREHOUSING_COMMUNICATIONS = 2  # Транспорт, складское хозяйство, связь.
    FINANCE_INSURANCE = 3  # Финансы, страхование.
    ENERGY = 4  # Энергетика.
    SCIENCE_EDUCATION_CULTURE = 5  # Наука, образование, культура.
    LAND_RECLAMATION_FORESTRY = 6  # Мелиорация, лесничество.
    CONSTRUCTION_INSTALLATION = 7  # Строительство, монтаж.
    MANUFACTURING_INDUSTRY = 8  # Производство (промышленность).
    LAW_AND_ORDER_PROTECTION = 9  # Право и защита порядка.
    HOUSING_AND_COMMUNAL_SERVICES = 10  # Жилищное и коммунальное хозяйство.
    STATE_AND_LOCAL_GOVERNMENT = 11  # Государственное и местное управление.
    HEALTHCARE = 12  # Здравоохранение.
    SPORT = 13  # Спорт.
    ARMY_POLICE = 14  # Армия, милиция.
    OTHER = 15  # Другое.
    NOT_WORKING = 16  # Не работает.


class Enterprise(Enum):
    """Тип предприятия."""

    STATE = 1  # Государственное предприятие.
    NON_STATE = 2  # Негосударственное предприятие.
    NOT_WORKING = 3  # Не работает.


class Property(Enum):
    """Отношение к собственности."""

    OWNER_CO_OWNER = 1  # Владелец, совладелец фирмы.
    HIRED_WORKER = 2  # Работает по найму.
    INDIVIDUAL_BUSINESS = 3  # Занимается индивидуальным бизнесом.
    NOT_WORKING = 4  # Не работает.


class MaritalStatus(Enum):
    """Семейное положение."""

    MARRIED = 1  # Женат или замужем.
    SINGLE = 2  # Холост или не замужем.


class LifeCycle(Enum):
    """Цикл семейной жизни."""

    UNDER_16 = 1  # Возраст до 16 лет.
    AGE_16_44_MARRIED_NO_KIDS = 2  # 16-44 года, в браке, без детей.
    AGE_16_44_MARRIED_YOUNGEST_CHILD_LE_11 = 3  # 16-44 года, в браке, младший ребенок до 11 лет включительно.
    AGE_16_44_MARRIED_YOUNGEST_CHILD_12_15 = 4  # 16-44 года, в браке, младший ребенок 12-15 лет.
    AGE_16_44_SINGLE_NO_KIDS = 5  # 16-44 года, не в браке, без детей.
    AGE_16_44_SINGLE_YOUNGEST_CHILD_LE_11 = 6  # 16-44 года, не в браке, младший ребенок до 11 лет включительно.
    AGE_16_44_SINGLE_YOUNGEST_CHILD_12_15 = 7  # 16-44 года, не в браке, младший ребенок 12-15 лет.
    AGE_GE_45_MARRIED_NO_KIDS = 8  # 45 лет и старше, в браке, без детей.
    AGE_GE_45_MARRIED_YOUNGEST_CHILD_LE_11 = 9  # 45 лет и старше, в браке, младший ребенок до 11 лет включительно.
    AGE_GE_45_MARRIED_YOUNGEST_CHILD_12_15 = 10  # 45 лет и старше, в браке, младший ребенок 12-15 лет.
    AGE_GE_45_SINGLE_NO_KIDS = 11  # 45 лет и старше, не в браке, без детей.
    AGE_GE_45_SINGLE_YOUNGEST_CHILD_LE_11 = 12  # 45 лет и старше, не в браке, младший ребенок до 11 лет включительно.
    AGE_GE_45_SINGLE_YOUNGEST_CHILD_12_15 = 13  # 45 лет и старше, не в браке, младший ребенок 12-15 лет.


class Internet(Enum):
    """Наличие интернета."""

    NO = 0  # Нет интернета.
    YES = 1  # Есть интернет.


class Dacha(Enum):
    """Наличие дачи."""

    NO = 0  # Нет дачи.
    YES = 1  # Есть дача.


class KidsAgeC1(Enum):
    """Возраст детей (город): 0-2 года."""

    NO = 0  # Нет детей в данной возрастной группе.
    YES = 1  # Есть дети в данной возрастной группе.


class KidsAgeC2(Enum):
    """Возраст детей (город): 3-6 лет."""

    NO = 0  # Нет детей в данной возрастной группе.
    YES = 1  # Есть дети в данной возрастной группе.


class KidsAgeC3(Enum):
    """Возраст детей (город): 7-11 лет."""

    NO = 0  # Нет детей в данной возрастной группе.
    YES = 1  # Есть дети в данной возрастной группе.


class KidsAgeC4(Enum):
    """Возраст детей (город): 12-15 лет."""

    NO = 0  # Нет детей в данной возрастной группе.
    YES = 1  # Есть дети в данной возрастной группе.


class Occupation(Enum):
    """Род занятий (город)."""

    OWNER_CO_OWNER = 1  # Владелец, совладелец фирмы.
    INDIVIDUAL_BUSINESS = 2  # Индивидуальный бизнес.
    MANAGER = 3  # Руководитель.
    SPECIALIST_EMPLOYEE_MILITARY = 4  # Специалист, служащий, военный.
    WORKER = 5  # Рабочий.
    STUDENT = 6  # Дошкольник, студент, учащийся.
    UNEMPLOYED = 7  # Безработный.
    PENSIONER_DISABLED = 8  # Пенсионер, инвалид.
    HOUSEWIFE_YOUNG_MOTHER = 9  # Домохозяйка, молодая мать.
    OTHER = 10  # Другое.


class TradeIndustry(Enum):
    """Отрасль деятельности (город)."""

    MANUFACTURING_INDUSTRY = 1  # Производство, промышленность.
    TRADE_SERVICE_RESTAURANTS = 2  # Торговля, обслуживание, рестораны.
    SCIENCE_EDUCATION_CULTURE_HEALTHCARE = 3  # Наука, образование, культура, здравоохранение.
    FINANCE_INSURANCE = 4  # Финансы, страхование.
    TRANSPORT_WAREHOUSING_COMMUNICATIONS = 5  # Транспорт, складское хозяйство, связь.
    OTHER = 6  # Другое.
    NOT_WORKING = 7  # Не работает.


class IncomeGroup(Enum):
    """Группа дохода по городам."""

    A = 1  # Группа дохода A.
    B = 2  # Группа дохода B.
    C = 3  # Группа дохода C.
    NA = 4  # Нет данных.


class FederalOkrug(Enum):
    """Федеральные округа."""

    CENTRAL = 1  # Центральный федеральный округ.
    NORTH_WESTERN = 2  # Северо-Западный федеральный округ.
    SOUTHERN = 3  # Южный федеральный округ.
    VOLGA = 4  # Приволжский федеральный округ.
    URAL = 5  # Уральский федеральный округ.
    SIBERIAN = 6  # Сибирский федеральный округ.
    FAR_EASTERN = 7  # Дальневосточный федеральный округ.
    NORTH_CAUCASIAN = 8  # Северо-Кавказский федеральный округ.


class IncomeScale201401(Enum):
    """Шкала дохода (с января 2014)."""

    NA = 0  # Нет данных.
    FROM_0_TO_5000 = 1  # От 0 до 5000.
    FROM_5001_TO_10000 = 2  # От 5001 до 10000.
    FROM_10001_TO_15000 = 3  # От 10001 до 15000.
    FROM_15001_TO_20000 = 4  # От 15001 до 20000.
    FROM_20001_TO_25000 = 5  # От 20001 до 25000.
    FROM_25001_TO_30000 = 6  # От 25001 до 30000.
    FROM_30001_TO_35000 = 7  # От 30001 до 35000.
    FROM_35001_TO_40000 = 8  # От 35001 до 40000.
    ABOVE_40001 = 9  # 40001 и выше.


class EquipmentV2(Enum):
    """Наличие дополнительного оборудования."""

    NO_USB_VIDEO_DVD_SMART_TV = 1  # Нет USB, Video/DVD, Smart TV.
    HAS_ONE_OF_THEM = 2  # Есть что-то одно из перечисленного.
    HAS_TWO_OR_THREE_OF_THEM = 3  # Есть два или три варианта из перечисленного.


class WghSuburbAgeGroup(Enum):
    """Возрастная группа (WGH)."""

    FROM_4_TO_11 = 1  # 4-11 лет.
    FROM_12_TO_17 = 2  # 12-17 лет.
    FROM_18_TO_24 = 3  # 18-24 года.
    FROM_25_TO_34 = 4  # 25-34 года.
    FROM_35_TO_44 = 5  # 35-44 года.
    FROM_45_TO_54 = 6  # 45-54 года.
    FROM_55_TO_64 = 7  # 55-64 года.
    ABOVE_65 = 8  # 65 лет и старше.


class WghDachaTvExist(Enum):
    """Наличие дачи с ТВ."""

    HAS_DACHA_AND_TV = 1  # Есть дача и есть телевизор на даче.
    NO_DACHA_OR_NO_TV = 2  # Нет дачи или нет телевизора на даче.


class SmartTvYesNo(Enum):
    """Наличие Смарт ТВ."""

    YES = 1  # Есть Смарт ТВ.
    NO = 2  # Нет Смарт ТВ.


class WghVideoGameWoAge(Enum):
    """Наличие видеотехники."""

    HAS_VIDEO = 1  # Есть видеотехника.
    NO_VIDEO = 2  # Нет видеотехники.


class WghUsbTvHh(Enum):
    """Наличие USB."""

    HAS_USB = 1  # Есть USB.
    NO_USB = 2  # Нет USB.


class CubeCity(Enum):
    """Саморепрезентирующиеся города."""

    YES = 1  # Да.
    NO = 2  # Нет.


class Timezone0(Enum):
    """Часовой пояс «ноль»."""

    YES = 1  # Да.
    NO = 2  # Нет.


class Cube100Plus100Minus(Enum):
    """Население 100+ или 100-."""

    PLUS_100 = 1  # Города с населением 100 тыс. и более.
    MINUS_100 = 2  # Города с населением менее 100 тыс.


class SputnikTv(Enum):
    """Наличие спутниковой тарелки (с августа 2020)."""

    YES = 1  # Есть спутниковая тарелка.
    NO = 2  # Нет спутниковой тарелки.


class GeoFrom082020(Enum):
    """География (с августа 2020)."""

    GREATER_MOSCOW = 1  # Большая Москва.
    RUSSIA_WITHOUT_GREATER_MOSCOW = 2  # Россия без Большой Москвы.


class City(Enum):
    """Город."""

    SAINT_PETERSBURG = 1  # Санкт-Петербург.
    TVER = 2  # Тверь.
    NIZHNY_NOVGOROD = 3  # Нижний Новгород.
    ROSTOV_ON_DON = 4  # Ростов-на-Дону.
    YAROSLAVL = 5  # Ярославль.
    VORONEZH = 6  # Воронеж.
    VOLGOGRAD = 7  # Волгоград.
    SARATOV = 8  # Саратов.
    SAMARA = 9  # Самара.
    KHABAROVSK = 10  # Хабаровск.
    IRKUTSK = 11  # Иркутск.
    MOSCOW = 12  # Москва.
    YEKATERINBURG = 14  # Екатеринбург.
    PERM = 15  # Пермь.
    CHELYABINSK = 16  # Челябинск.
    NOVOSIBIRSK = 17  # Новосибирск.
    TYUMEN = 18  # Тюмень.
    KRASNOYARSK = 19  # Красноярск.
    VLADIVOSTOK = 20  # Владивосток.
    KAZAN = 21  # Казань.
    UFA = 22  # Уфа.
    OMSK = 23  # Омск.
    KRASNODAR = 29  # Краснодар.
    STAVROPOL = 43  # Ставрополь.
    BARNAUL = 49  # Барнаул.
    KEMEROVO = 51  # Кемерово.
    TOMSK = 60  # Томск.


# NOTE: Далее идут перечисления, относящиеся к Program фильтру.
class ProgramIsChild(Enum):
    """Программа детская."""

    YES = 'Y'
    NO = 'N'


class ProgramGroupID(Enum):
    """ID группы программ."""

    DOCUMENTARY_SERIES = 7607  # Документальный сериал.
    WEEKEND_SERIES = 9659  # Сериал по выходным.
    OUR_CINEMA = 9715  # Наше кино.
    NIGHT_PERFORMANCE = 9746  # Ночной сеанс.
    CHILDRENS_SEANCE = 11471  # Детский сеанс.
    MINI_SERIES = 39718  # Мини-сериал.
    RUSSIAN_SERIES = 44358  # Русская серия.
    HOME_SERIES = 44360  # Отечественный сериал.
    NIGHT_FILM = 45774  # Ночной фильм.
    TNT_COMEDY = 113600  # ТНТ Комедия.
    RUSSKIE_MULTFILMY = 113601  # Русские мультфильмы.
    SDELANO_V_ROSSII = 113610  # Сделано в России.
    FILMS_ON_STS_AT_21_00 = 113882  # Кино на СТС в 21:00.
    MOVIE_AT_22_00 = 119497  # Кино в 22:00.
    CHILDRENS_BLOCK = 122494  # Детский блок.
    KINOPOKAZ = 122510  # Кинопоказ.
    DOCUMENTATION = 122512  # Документалистика.
    DOCUMENTARY = 122520  # Документальное кино.
    TNT_COMEDY_RERUN = 122555  # ТНТ Комедия (повтор).
    KULT_KINO_S_KIRILLOM_RAZLOGOVYM = 122569  # Культ кино с Кириллом Разлоговым.
    RUSSIAN_SERIES_20_00 = 122619  # Русский сериал 20:00.
    FILM_COLLECTION_ON_STS = 122624  # Киноколлекция на СТС.
    SERIES_AT_21_30 = 123292  # Сериал в 21:30.
    FILMS_ON_DAYS_OFF = 123443  # Кино по выходным.
    CARTOONS_ON_STS_06_00 = 123683  # Мультфильмы на СТС 06:00.
    CARTOONS_ON_STS_07_00 = 123684  # Мультфильмы на СТС 07:00.
    TV_CHANNEL_DOBROE_UTRO = 123685  # Телеканал "Доброе утро!".
    NASTROENIE = 123689  # Настроение.
    SERIES_12_00 = 125984  # Сериал 12:00.
    SERIES_12_35 = 125985  # Сериал 12:35.
    FILM_ON_STS_AT_22_00 = 130415  # Кино на СТС в 22:00.
    MOVIE_AT_21_00 = 130688  # Кино в 21:00.
    KINO_V_07_30 = 130689  # Кино в 07:30.
    SERIES_16_30 = 130695  # Сериал 16:30.
    CINEMA_WORLD_23_20 = 138559  # Мир кино 23:20.
    BOLSHOE_KINO_VYKH = 139171  # Большое кино (вых).
    NOVOSTI_23_30 = 141124  # Новости 23:30.
    FANTASTIC_SERIES_1 = 141175  # Фантастический сериал 1.
    ZONE_OF_TWILIGHT = 141179  # Зона сумерек.
    CHILDRENS_BLOCK_ON_DAYS_OFF = 141181  # Детский блок по выходным.
    DRUGOE_KINO = 141182  # Другое кино.
    NEWS_12_30 = 141184  # Новости 12:30.
    NEWS_19_30 = 141185  # Новости 19:30.
    FILM_14_00 = 149233  # Кино 14:00.
    NEWS_16_30 = 155587  # Новости 16:30.
    FAVOURITE_FILMS = 171745  # Любимые фильмы.
    MOTION_PICTURE_19_35 = 171746  # Художественный фильм 19:35.
    MOTION_PICTURE_23_35 = 171747  # Художественный фильм 23:35.
    SERIES_18_30 = 171748  # Сериал 18:30.
    SERIES_22_40 = 171749  # Сериал 22:40.
    DOCUMENTARY_21_10 = 171752  # Документальный фильм 21:10.
    DOCUMENTARY_SERIES_18_15 = 171753  # Документальный сериал 18:15.
    DOM_2_23_00 = 177677  # Дом-2 23:00.
    BOLSHOE_KINO_1_WE = 182042  # Большое кино - 1 (вых).
    BOLSHOE_KINO_2_WE = 182043  # Большое кино - 2 (вых).
    SERIES_16_15 = 209042  # Сериал 16:15.
    UTRENNYAYA_INFORMATSIONNAYA_PROGRAMMA = 215958  # Утренняя информационная программа.
    NOVOSTI_KULTURY = 215959  # Новости культуры.
    UROKI_RISOVANIYA_S_SERGEEM_ANDRIYAKOY = 215961  # Уроки рисования с Сергеем Андриякой.
    RERUN_12_45 = 215962  # Повтор 12:45.
    POVTOR_STUPENI_TSIVILIZATSII = 215963  # Повтор Ступени цивилизации.
    IZ_ZOLOTOY_KOLLEKTSII = 215966  # Из золотой коллекции.
    RERUN_OF_SERIES_17_11 = 215967  # Повторы сериалов 17:11.
    MUZYKALNAYA_LINEYKA_17_20 = 215969  # Музыкальная линейка 17:20.
    GLAVNAYA_ROL_19_45 = 215971  # Главная роль 19:45.
    LINEYKA_20_05 = 215972  # Линейка 20:05.
    LINEYKA_20_45 = 215973  # Линейка 20:45.
    MONDAY_23_50 = 215977  # Понедельник 23:50.
    LINIYA_ZHIZNI = 215978  # Линия жизни.
    RETROSPEKTIVA_OTECHESTVENNOGO_I_ZARUBEZHNOGO_KINO = 215979  # Ретроспектива отечественного и зарубежного кино.
    KINOPOKAZ_UTRENNYAYA_LINEYKA_VYKHODNYKH_DNEY = 215980  # Кинопоказ. Утренняя линейка выходных дней.
    KINO_NA_VSE_VREMENA = 215981  # Кино на все времена.
    VOSKRESNAYA_NOCHNAYA_LINEYKA = 215982  # Воскресная ночная линейка.
    MUZYKALNYE_PROGRAMY_VYKHODNYKH_DNEY = 215983  # Музыкальные программы выходных дней.
    KINO_ZA_CHAS_DO_POLUNOCHI = 234690  # Кино за час до полуночи.
    NOCHNOE_KINO = 242727  # Ночное кино.
    OTKRYTY_POKAZ = 242728  # Открытый показ.
    KINO_PO_VOSKRESENYAM = 242729  # Кино по воскресеньям.
    UTRO_ROSSII_WORKING_DAYS = 260747  # Утро России (будни).
    UTRO_ROSSII_SATURDAY = 260748  # Утро России (суббота).
    UTINYE_ISTORII_2017 = 267352  # Утиные истории 2017.
    CHERNOE_ZYRKALO = 278450  # Черное зыркало.
    NOVYE_RUSSKIE_SENSATSII = 282034  # Новые русские сенсации.
    BOXING_BARE_KNUCKLE_FIGHTING_CHAMPIONSHIPS = 299798  # Бокс. Bare Knuckle Fighting Championships. Женщины.


class ProgramTypeID(Enum):
    """ID типа программы."""

    SERIES = 1  # Телесериал.
    ENTERTAINMENT = 2  # Развлекательная программа.
    MUSICAL = 3  # Музыкальная программа.
    SPORTS = 4  # Спортивная программа.
    NEWS = 5  # Новости.
    SOCIAL_POLITICAL = 6  # Социально-политическая программа.
    EDUCATIONAL = 7  # Познавательная программа.
    CHILDREN = 8  # Детская программа.
    OTHER = 9  # Прочее.
    MOVIES = 11  # Кинофильм.
    ANIMATION = 12  # Анимация.
    DOCUMENTARY = 13  # Документальная программа.


class ProgramCountryId(Enum):
    """Перечисление оставлено для консистентности, но не используется."""

    pass


class ProgramCategoryId(Enum):
    """Перечисление оставлено для консистентности, но не используется."""

    pass


class ProgramSportId(Enum):
    """Перечисление оставлено для консистентности, но не используется."""

    pass


class ProgramSportGroupId(Enum):
    """Перечисление оставлено для консистентности, но не используется."""

    pass


class ProgramProducerId(Enum):
    """Перечисление оставлено для консистентности, но не используется."""

    pass


class ProgramLanguageId(Enum):
    """Перечисление оставлено для консистентности, но не используется."""

    pass


class ProgramAgeRestrictionId(Enum):
    """Перечисление оставлено для консистентности, но не используется."""

    pass


class ProgramProducerCountryId(Enum):
    """Перечисление оставлено для консистентности, но не используется."""

    pass


# NOTE: Далее идут перечисления, относящиеся к BreaksFilter.
class BreaksId(Enum):
    """Перечисление оставлено для консистентности, но не используется."""

    pass


class BreaksStyleId(Enum):
    """Рекламный блок стиль ID."""

    NA = 0  # N/A.
    STANDARD = 1  # Стандартный.
    PREMIUM = 2  # Премиальный.


class BreaksDistributionType(Enum):
    """Рекламный блок распространение ID."""

    LOCAL = 'L'  # Локальный.
    NETWORK = 'N'  # Сетевой.
    ORBITAL = 'O'  # Орбитальный.
    NA = 'U'  # N/A.


class BreaksPositionType(Enum):
    """Рекламный блок позиция ID."""

    EXTERNAL = 'E'  # Внешний.
    INTERNAL = 'I'  # Внутренний.


class BreaksContentType(Enum):
    """Рекламный блок тип контента."""

    ANNOUNCEMENT = 'A'  # Анонсы.
    COMMERCIAL = 'C'  # Коммерческий.
    POLITICAL = 'P'  # Политический.
    SPONSORSHIP = 'S'  # Спонсорский.
    NA = 'U'  # N/A.


class BreaksIssueStatusId(Enum):
    """Блок статус ID."""

    REAL = 'R'  # Реальный.
    VIRTUAL = 'V'  # Виртуальный.


class GrpTypeId(Enum):
    """Перечисление оставлено для консистентности, но не используется."""

    pass


# NOTE: Далее идут перечисления, относящиеся к AdFilter.
class AdId(Enum):
    """Перечисление оставлено для консистентности, но не используется."""

    pass


class AdTypeId(Enum):
    """Ролик тип ID."""

    SPOT = 1  # Ролик.
    SPONSOR = 5  # Спонсор.
    TV_SHOP = 10  # Телемагазин.
    ANNOUNCEMENT_SPONSOR = 15  # Анонс: спонсор.
    SPONSOR_LEAD_IN = 23  # Спонсорская заставка.
    WEATHER_SPONSOR = 24  # Погода: спонсор.
    ANNOUNCEMENT_SPONSOR_LEAD_IN = 25  # Анонс: спонсорская заставка.


class AdStyleId(Enum):
    """Ролик стиль ID."""

    NA = 0  # N/A.
    HOT_LINE = 2  # Горячая линия.
    INFORMATION_MESSAGE = 3  # Информационное сообщение.
    CONGRATULATION = 4  # Поздравление.
    TEASER = 5  # Тизер.
    PROMOTION_ACTION = 6  # Промоушен-акция.
    PACKSHOT = 7  # Пэкшот.
    IMAGE_ADVERTISING = 8  # Имиджевая реклама.
    SALES_PROMOTION = 9  # Сейлз-промоушен.
    PROMOTION_ACTION_PACKSHOT = 10  # Промоушен-акция + Пэкшот.


class AdSloganAudioId(Enum):
    """Перечисление оставлено для консистентности, но не используется."""

    pass


class AdSloganVideoId(Enum):
    """Перечисление оставлено для консистентности, но не используется."""

    pass


class AdIssueStatusId(Enum):
    """Ролик статус ID."""

    REAL = 'R'  # Реальный.
    VIRTUAL = 'V'  # Виртуальный.


class AdDistributionType(Enum):
    """Ролик распространение ID."""

    LOCAL = 'L'  # Локальный.
    NETWORK = 'N'  # Сетевой.
    ORBITAL = 'O'  # Орбитальный.
    NA = 'U'  # N/A.


# NOTE: Перечисление относится к PlatformFilter. Только для базы данных "Big TV".
class Platform(Enum):
    """ID платформы."""

    TV = 1  # ТВ.
    DESKTOP = 2  # Десктоп.
    MOBILE = 3  # Мобайл.


# NOTE: Перечисление относится к PlayBackTypeFilter. Только для базы данных "Big TV".
class PlayBackType(Enum):
    """ID Playback."""

    LIVE = 0  # Live.
    VOSDAL = 1  # Vosdal.
    PLAYBACK_2 = 2  # Playback 2.
    PLAYBACK_3 = 3  # Playback 3.
    PLAYBACK_4 = 4  # Playback 4.
    PLAYBACK_5 = 5  # Playback 5.
    PLAYBACK_6 = 6  # Playback 6.
    PLAYBACK_7 = 7  # Playback 7.
    PLAYBACK_8 = 8  # Playback 8.
    PLAYBACK_9 = 9  # Playback 9.
    PLAYBACK_10 = 10  # Playback 10.
    PLAYBACK_11 = 11  # Playback 11.
    PLAYBACK_12 = 12  # Playback 12.
    PLAYBACK_13 = 13  # Playback 13.
    PLAYBACK_14 = 14  # Playback 14.
    PLAYBACK_15 = 15  # Playback 15.
    PLAYBACK_16 = 16  # Playback 16.
    PLAYBACK_17 = 17  # Playback 17.
    PLAYBACK_18 = 18  # Playback 18.
    PLAYBACK_19 = 19  # Playback 19.
    PLAYBACK_20 = 20  # Playback 20.
    PLAYBACK_21 = 21  # Playback 21.
    PLAYBACK_22 = 22  # Playback 22.
    PLAYBACK_23 = 23  # Playback 23.
    PLAYBACK_24 = 24  # Playback 24.
    PLAYBACK_25 = 25  # Playback 25.
    PLAYBACK_26 = 26  # Playback 26.
    PLAYBACK_27 = 27  # Playback 27.
    PLAYBACK_28 = 28  # Playback 28.
