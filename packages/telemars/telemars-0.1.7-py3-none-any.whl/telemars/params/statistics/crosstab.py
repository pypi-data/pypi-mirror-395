from enum import Enum


class K7Statistic(Enum):
    """Статистики отчета Crosstab набора данных "Big TV" и "Внедомашний просмотр"."""

    # Суммарные статистики.
    CUM_REACH000 = 'CumReach000'  # Зависит от ЦА.
    SPOT_BY_BREAKS_CUM_REACH000 = 'SpotByBreaksCumReach000'  # Зависит от ЦА.
    CUM_REACH_PER = 'CumReachPer'  # Зависит от ЦА.
    SPOT_BY_BREAKS_CUM_REACH_PER = 'SpotByBreaksCumReachPer'  # Зависит от ЦА.
    RTG000_SUM = 'Rtg000Sum'  # Зависит от ЦА.
    SALES_RTG000_SUM = 'SalesRtg000Sum'  # Не зависит от ЦА.
    SPOT_BY_BREAKS_RTG000_SUM = 'SpotByBreaksRtg000Sum'  # Зависит от ЦА.
    SPOT_BY_BREAKS_SALES_RTG000_SUM = 'SpotByBreaksSalesRtg000Sum'  # Не зависит от ЦА.
    RTG_PER_SUM = 'RtgPerSum'  # Зависит от ЦА.
    STAND_RTG_PER_SUM = 'StandRtgPerSum'  # Зависит от ЦА.
    SALES_RTG_PER_SUM = 'SalesRtgPerSum'  # Не зависит от ЦА.
    STAND_SALES_RTG_PER_SUM = 'StandSalesRtgPerSum'  # Не зависит от ЦА.
    SPOT_BY_BREAKS_RTG_PER_SUM = 'SpotByBreaksRtgPerSum'  # Зависит от ЦА.
    SPOT_BY_BREAKS_STAND_RTG_PER_SUM = 'SpotByBreaksStandRtgPerSum'  # Зависит от ЦА.
    SPOT_BY_BREAKS_SALES_RTG_PER_SUM = 'SpotByBreaksSalesRtgPerSum'  # Не зависит от ЦА.
    SPOT_BY_BREAKS_STAND_SALES_RTG_PER_SUM = 'SpotByBreaksStandSalesRtgPerSum'  # Не зависит от ЦА.
    DURATION_SUM = 'DurationSum'  # Не зависит от ЦА.
    QUANTITY_SUM = 'QuantitySum'  # Не зависит от ЦА.
    CONSOLIDATED_COST_SUM_RUB = 'ConsolidatedCostSumRUB'  # Не зависит от ЦА.
    CONSOLIDATED_COST_SUM_USD = 'ConsolidatedCostSumUSD'  # Не зависит от ЦА.

    # Средние статистики.
    AV_REACH000 = 'AvReach000'  # Зависит от ЦА.
    SPOT_BY_BREAKS_AV_REACH000 = 'SpotByBreaksAvReach000'  # Зависит от ЦА.
    AV_REACH_PER = 'AvReachPer'  # Зависит от ЦА.
    SPOT_BY_BREAKS_AV_REACH_PER = 'SpotByBreaksAvReachPer'  # Зависит от ЦА.
    SPOT_BY_BREAKS_OTS000_AVG = 'SpotByBreaksOTS000Avg'  # Зависит от ЦА.
    SPOT_BY_BREAKS_OTS_PER_AVG = 'SpotByBreaksOTSPerAvg'  # Зависит от ЦА.
    RTG000_AVG = 'Rtg000Avg'  # Зависит от ЦА.
    SALES_RTG000_AVG = 'SalesRtg000Avg'  # Не зависит от ЦА.
    SPOT_BY_BREAKS_RTG000_AVG = 'SpotByBreaksRtg000Avg'  # Зависит от ЦА.
    SPOT_BY_BREAKS_SALES_RTG000_AVG = 'SpotByBreaksSalesRtg000Avg'  # Не зависит от ЦА.
    RTG_PER_AVG = 'RtgPerAvg'  # Зависит от ЦА.
    STAND_RTG_PER_AVG = 'StandRtgPerAvg'  # Зависит от ЦА.
    SALES_RTG_PER_AVG = 'SalesRtgPerAvg'  # Не зависит от ЦА.
    STAND_SALES_RTG_PER_AVG = 'StandSalesRtgPerAvg'  # Не зависит от ЦА.
    SPOT_BY_BREAKS_RTG_PER_AVG = 'SpotByBreaksRtgPerAvg'  # Зависит от ЦА.
    SPOT_BY_BREAKS_STAND_RTG_PER_AVG = 'SpotByBreaksStandRtgPerAvg'  # Зависит от ЦА.
    SPOT_BY_BREAKS_SALES_RTG_PER_AVG = 'SpotByBreaksSalesRtgPerAvg'  # Не зависит от ЦА.
    SPOT_BY_BREAKS_STAND_SALES_RTG_PER_AVG = 'SpotByBreaksStandSalesRtgPerAvg'  # Не зависит от ЦА.
    UNIVERSE000_AVG = 'Universe000Avg'  # Зависит от ЦА.
    SAMPLE_AVG = 'SampleAvg'  # Зависит от ЦА.
    DURATION_AVG = 'DurationAvg'  # Не зависит от ЦА.
