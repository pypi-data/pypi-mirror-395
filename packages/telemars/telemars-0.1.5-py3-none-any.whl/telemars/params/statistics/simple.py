from enum import Enum


class K7Statistic(Enum):
    """Статистики отчета Simple набора данных "Big TV" и "Внедомашний просмотр"."""

    REACH000 = 'Reach000'  # Зависит от ЦА.
    SPOT_BY_BREAKS_REACH000 = 'SpotByBreaksReach000'  # Зависит от ЦА.
    REACH_PER = 'ReachPer'  # Зависит от ЦА.
    SPOT_BY_BREAKS_REACH_PER = 'SpotByBreaksReachPer'  # Зависит от ЦА.
    RTG000 = 'Rtg000'  # Зависит от ЦА.
    SALES_RTG000 = 'SalesRtg000'  # Не зависит от ЦА.
    SPOT_BY_BREAKS_RTG000 = 'SpotByBreaksRtg000'  # Зависит от ЦА.
    SPOT_BY_BREAKS_SALES_RTG000 = 'SpotByBreaksSalesRtg000'  # Не зависит от ЦА.
    RTG_PER = 'RtgPer'  # Зависит от ЦА.
    STAND_RTG_PER = 'StandRtgPer'  # Зависит от ЦА.
    SALES_RTG_PER = 'SalesRtgPer'  # Не зависит от ЦА.
    STAND_SALES_RTG_PER = 'StandSalesRtgPer'  # Не зависит от ЦА.
    SPOT_BY_BREAKS_RTG_PER = 'SpotByBreaksRtgPer'  # Зависит от ЦА.
    SPOT_BY_BREAKS_STAND_RTG_PER = 'SpotByBreaksStandRtgPer'  # Зависит от ЦА.
    SPOT_BY_BREAKS_SALES_RTG_PER = 'SpotByBreaksSalesRtgPer'  # Не зависит от ЦА.
    SPOT_BY_BREAKS_STAND_SALES_RTG_PER = 'SpotByBreaksStandSalesRtgPer'  # Не зависит от ЦА.
    ATV = 'ATV'  # Зависит от ЦА.
    ATV_REACH = 'ATVReach'  # Зависит от ЦА.
    UNIVERSE000 = 'Universe000'  # Зависит от ЦА.
    SAMPLE = 'Sample'  # Зависит от ЦА.
    DURATION = 'Duration'  # Не зависит от ЦА.
    QUANTITY = 'Quantity'  # Не зависит от ЦА.
    CONSOLIDATED_COST_RUB = 'ConsolidatedCostRUB'  # Не зависит от ЦА.
    CONSOLIDATED_COST_USD = 'ConsolidatedCostUSD'  # Не зависит от ЦА.
