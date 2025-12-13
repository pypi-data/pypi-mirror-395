import asyncio
from dataclasses import dataclass
from datetime import date

import polars as pl
from mediascope_api.core import net as mscore
from mediascope_api.mediavortex import catalogs as cwc
from mediascope_api.mediavortex import tasks as cwt
from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator, model_validator
from typing_extensions import Annotated, Optional, Self, Sequence, Union

from telemars.filters import simple as sflt
from telemars.options.simple import Option
from telemars.params.filters.simple import RegionId
from telemars.params.options.simple import KitId, SortOrder
from telemars.params.slices.simple import Slice
from telemars.params.statistics.simple import K7Statistic


class SimpleTask(BaseModel):
    # Pydantic не может работать с кастомными типами по умолчанию.
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Перечень фильтров расчета.
    date_filter: Annotated[
        sflt.DateFilter,
        Field(...),
    ]
    weekday_filter: Annotated[
        sflt.WeekdayFilter,
        Field(default_factory=sflt.WeekdayFilter),
    ]
    daytype_filter: Annotated[
        sflt.DaytypeFilter,
        Field(default_factory=sflt.DaytypeFilter),
    ]
    company_filter: Annotated[
        sflt.CompanyFilter,
        Field(default_factory=sflt.CompanyFilter),
    ]
    location_filter: Annotated[
        sflt.LocationFilter,
        Field(default_factory=sflt.LocationFilter),
    ]
    # Целевые аудитории указываются исключительно в BaseDemoFilter.
    basedemo_filter: Annotated[
        Union[sflt.BaseDemoFilter, Sequence[sflt.BaseDemoFilter]],
        Field(min_length=1),
    ]
    targetdemo_filter: Annotated[
        sflt.TargetDemoFilter,
        Field(default_factory=sflt.TargetDemoFilter),
    ]
    program_filter: Annotated[
        sflt.ProgramFilter,
        Field(default_factory=sflt.ProgramFilter),
    ]
    break_filter: Annotated[
        sflt.BreakFilter,
        Field(default_factory=sflt.BreakFilter),
    ]
    ad_filter: Annotated[
        sflt.AdFilter,
        Field(default_factory=sflt.AdFilter),
    ]
    platform_filter: Annotated[
        sflt.PlatformFilter,
        Field(default_factory=sflt.PlatformFilter),
    ]
    playbacktype_filter: Annotated[
        sflt.PlayBackTypeFilter,
        Field(default_factory=sflt.PlayBackTypeFilter),
    ]

    # Перечень срезов, статистик, параметров сортировки и опций расчета.
    slices: Annotated[
        Sequence[Slice],
        Field(...),
    ]
    statistics: Annotated[
        Sequence[K7Statistic],
        Field(...),
    ]
    sortings: Annotated[
        Optional[Sequence[tuple[Slice, SortOrder]]],
        Field(default=None),
    ]
    options: Annotated[
        Option,
        Field(...),
    ]

    # Компоненты работы с Mediascope API.
    mtask: Annotated[
        cwt.MediaVortexTask,
        Field(default_factory=lambda: cwt.MediaVortexTask(check_version=False)),
    ]
    mnet: Annotated[
        mscore.MediascopeApiNetwork,
        Field(default_factory=mscore.MediascopeApiNetwork),
    ]
    cats: Annotated[
        cwc.MediaVortexCats,
        Field(default_factory=cwc.MediaVortexCats),
    ]

    @field_validator('basedemo_filter', mode='before')
    @classmethod
    def validate_basedemo_filter(
        cls, v: Union[sflt.BaseDemoFilter, Sequence[sflt.BaseDemoFilter]], info: ValidationInfo
    ) -> Sequence[sflt.BaseDemoFilter]:
        """Преобразует одиночный BaseDemoFilter в список из одного элемента."""
        if isinstance(v, sflt.BaseDemoFilter):
            return [v]

        return v

    @model_validator(mode='after')
    def check_dates(self) -> Self:
        """Проверяет, что даты в date_filter находятся в доступном периоде для выбранного KitID."""
        kit_availability_df: pl.DataFrame = pl.from_pandas(self.cats.get_availability_period())
        kit_availability: list[dict] = kit_availability_df.to_dicts()

        kit_id: KitId = self.options.kit_id

        # Находим запись с нужным KitID.
        kit_record: Optional[dict] = None

        for record in kit_availability:
            if int(record['id']) == kit_id.value:
                kit_record = record
                break

        if kit_record is None:
            raise ValueError('Не найдены доступные периоды для KitID {}'.format(kit_id.value))

        # Получаем доступный период для данного KitID.
        period_from: date = date.fromisoformat(kit_record['periodFrom'])
        period_to: date = date.fromisoformat(kit_record['periodTo'])

        # Получаем даты из date_filter.
        date_from: date = self.date_filter.date_from
        date_to: date = self.date_filter.date_to

        # Проверяем, что даты находятся в доступном периоде.
        if date_from < period_from:
            raise ValueError(
                'Дата начала {} выходит за пределы доступного периода для KitID {} ({} - {}).'.format(
                    date_from, kit_id.value, period_from, period_to
                )
            )

        if date_to > period_to:
            raise ValueError(
                'Дата окончания {} выходит за пределы доступного периода для KitID {} ({} - {}).'.format(
                    date_to, kit_id.value, period_from, period_to
                )
            )

        return self

    @model_validator(mode='after')
    def check_filters(self) -> Self:
        # Для KitID #7 (Big TV) доступны только регионы "СЕТЕВОЕ ВЕЩАНИЕ" (99) и "ИНТЕРНЕТ" (100).
        if self.options.kit_id == KitId.BIG_TV:
            if self.company_filter.region_id is not None and any(
                id not in (RegionId.NETWORK_BROADCASTING, RegionId.INTERNET) for id in self.company_filter.region_id
            ):
                raise ValueError(
                    'Для KitID {} в фильтре companyFilter.regionId допустимы только регионы {} и {}.'.format(
                        KitId.BIG_TV.value, RegionId.NETWORK_BROADCASTING.value, RegionId.INTERNET.value
                    )
                )

        return self

    @model_validator(mode='after')
    def check_slices(self) -> Self:
        # Для отчета Simple обязательна разбивка по RESEARCH_DATE.
        if Slice.RESEARCH_DATE not in self.slices:
            raise ValueError('Для отчета Simple обязательна разбивка по {}.'.format(Slice.RESEARCH_DATE.value))

        # При наличии статистики "RtgPer" должна быть задана разбивка по событиям.
        if K7Statistic.RTG_PER in self.statistics:
            if not any(
                slice in self.slices for slice in (Slice.PROGRAM_SPOT_ID, Slice.BREAKS_SPOT_ID, Slice.AD_SPOT_ID)
            ):
                raise ValueError(
                    'Для статистики {} должна быть задана разбивка по событиям: {}, {} или {}.'.format(
                        K7Statistic.RTG_PER.value,
                        Slice.PROGRAM_SPOT_ID.value,
                        Slice.BREAKS_SPOT_ID.value,
                        Slice.AD_SPOT_ID.value,
                    )
                )

        # Проверка несовместимости среза "breaksSpotId" с фильтрами.
        if Slice.BREAKS_SPOT_ID in self.slices:
            if (
                self.ad_filter.ad_issue_status_id is not None
                or self.ad_filter.advertiser_id is not None
                or self.ad_filter.ad_type_id is not None
            ):
                raise ValueError(
                    'Срез {} несовместим с фильтрами: adIssueStatusId, advertiserId, adTypeId.'.format(
                        Slice.BREAKS_SPOT_ID.value
                    )
                )

        if self.options.kit_id == KitId.BIG_TV:
            if Slice.CITY in self.slices:
                raise ValueError('Срез {} недоступен для KitID {}.'.format(Slice.CITY.value, KitId.BIG_TV.value))

        return self

    @model_validator(mode='after')
    def check_sortings(self) -> Self:
        # Срез, по которому выполняется сортировка, должен быть указан в срезах.
        if self.sortings is not None:
            for sorting in self.sortings:
                if sorting[0] not in self.slices:
                    raise ValueError('Сортируемый срез {} не указан в срезах.'.format(sorting[0].value))

        # Дублирование срезов в сортировках недопустимо.
        if self.sortings is not None:
            sorting_slices: list[Slice] = [s[0] for s in self.sortings]

            if len(sorting_slices) != len(set(sorting_slices)):
                raise ValueError('Дублирование срезов в сортировках недопустимо.')

        return self

    @model_validator(mode='after')
    def check_options(self) -> Self:
        if self.options.kit_id != KitId.BIG_TV:
            raise ValueError('В данный момент KitID {} не поддерживается в отчете Simple.'.format(KitId.BIG_TV.value))

        return self

    def _build_task(
        self, basedemo_filter: sflt.BaseDemoFilter, statistic: K7Statistic, region_id: Optional[int] = None
    ) -> str:
        """Генерирует задание для отчета Simple в формате JSON для конкретной аудитории и статистики."""
        # NOTE: Для каждого региона (города) необходимо переопределять фильтр.
        company_filter_expr: str | None = self.company_filter.expr

        if region_id is not None:
            company_filter_copy: sflt.CompanyFilter = self.company_filter.model_copy(deep=True)
            company_filter_copy.region_id = [region_id]
            company_filter_expr = company_filter_copy.expr

        task: str = self.mtask.build_simple_task(
            date_filter=self.date_filter.expr,
            weekday_filter=self.weekday_filter.expr,
            daytype_filter=self.daytype_filter.expr,
            company_filter=company_filter_expr,
            location_filter=self.location_filter.expr,
            basedemo_filter=basedemo_filter.expr,
            targetdemo_filter=self.targetdemo_filter.expr,
            program_filter=self.program_filter.expr,
            break_filter=self.break_filter.expr,
            ad_filter=self.ad_filter.expr,
            platform_filter=self.platform_filter.expr,
            playbacktype_filter=self.playbacktype_filter.expr,
            slices=[s.value for s in self.slices],
            statistics=[statistic.value],
            sortings={s[0].value: s[1].value for s in self.sortings} if self.sortings is not None else None,
            options=self.options.expr,
        )

        return task

    # TODO: Добавить время жизни задачи и обработку ошибок по таймауту.
    async def execute(self) -> pl.DataFrame:
        """Отправляет задания для каждой комбинации города, аудитории и статистики и возвращает результат.

        Особенности расчета:
        - Чтобы статистики рассчитывалась корректно, необходимо рассчитывать отдельно по каждому региону (городу).
        - Каждая аудитория должна рассчитыться отдельной задачей.
        - Каждая статистика должна рассчитыться отдельной задачей.
        - Каждая задача должна привязываться к конкретному проекту (project_name). Особенность Mediascope API.
        """

        @dataclass
        class TaskInfo:
            region_id: Optional[int]
            basedemo_filter: sflt.BaseDemoFilter
            statistic: K7Statistic

        tasks: list[dict] = []
        tasks_plus: list[tuple[dict, TaskInfo]] = []

        # Получаем список регионов для разбивки.
        region_ids: list[int] = []

        if self.company_filter.region_id is not None:
            region_ids = [r.value for r in self.company_filter.region_id]
        else:
            # Если регионы не заданы, отправляем одну задачу без разбивки по регионам.
            region_ids = [None]

        # Итерация: Регион (Город) -> Аудитория -> Статистика.
        for region_id in region_ids:
            for basedemo_filter in self.basedemo_filter:
                for statistic in self.statistics:
                    task_json: str = self._build_task(basedemo_filter, statistic, region_id)

                    tsk: dict = {
                        'task': self.mtask.send_simple_task(task_json),
                        'project_name': task_json.__hash__(),
                    }

                    tasks.append(tsk)
                    tasks_plus.append(
                        (tsk, TaskInfo(region_id=region_id, basedemo_filter=basedemo_filter, statistic=statistic))
                    )

        # NOTE: Метод .wait_task() всегда возвращает результат, даже если задачу не удалось выполнить.
        # Из-за этого проверка на пустой результат определяется по наличию данных в итоговом DataFrame.
        await asyncio.to_thread(lambda: self.mtask.wait_task(tasks))

        # NOTE: Объединяем результаты всех задач в один pl.DataFrame. Задачи при этом могут быть пустыми.
        dfs: list[tuple[pl.DataFrame, TaskInfo]] = []

        for task, task_info in tasks_plus:
            df: pl.DataFrame = pl.from_pandas(
                self.mtask.result2table(self.mtask.get_result(task['task']), project_name=task['project_name'])
            )

            if df.is_empty():
                continue

            df = df.select([s.value for s in self.slices] + [task_info.statistic.value])

            # Переименование столбца со статистикой, только если задана аудитория.
            if task_info.basedemo_filter.name is not None and task_info.statistic not in [
                K7Statistic.QUANTITY,
                K7Statistic.DURATION,
                K7Statistic.SPOT_BY_BREAKS_SALES_RTG000,
                K7Statistic.SPOT_BY_BREAKS_SALES_RTG_PER,
                K7Statistic.SPOT_BY_BREAKS_STAND_SALES_RTG_PER,
                K7Statistic.CONSOLIDATED_COST_RUB,
                K7Statistic.CONSOLIDATED_COST_USD,
            ]:
                df = df.rename(
                    {
                        task_info.statistic.value: '{} {}'.format(
                            task_info.statistic.value, task_info.basedemo_filter.name
                        )
                    }
                )

            dfs.append((df, task_info))

        # NOTE: Окончательная проверка на пустой результат.
        if not dfs:
            return pl.DataFrame()

        # NOTE: Важно пояснить. На этом этапе удаляем дубликаты DataFrame, так как некоторые статистики не зависят от
        # аудитории (например, QUANTITY). В итоге для каждой аудитории получается одинаковый DataFrame.
        # Перед удалением дубликатов важно отсортировать срезы в каждом DataFrame, чтобы сравнение было корректным.
        udfs: list[pl.DataFrame] = []
        udfs_plus: list[tuple[pl.DataFrame, TaskInfo]] = []

        for df, task_info in dfs:
            if not any(df.sort(by=df.columns).equals(edf) for edf in udfs):
                udfs.append(df.sort(by=df.columns))
                udfs_plus.append((df, task_info))

        dfs = udfs_plus

        # Горизонтальное объединение результатов по регионам.
        rdfs: list[pl.DataFrame] = []

        for region_id in region_ids:
            region_dfs: list[pl.DataFrame] = [df for df, info in dfs if info.region_id == region_id]

            if not region_dfs:
                continue

            df: pl.DataFrame = region_dfs[0]

            if len(region_dfs) > 1:
                for rdf in region_dfs[1:]:
                    df = df.join(rdf, on=[s.value for s in self.slices], how='left')

            rdfs.append(df)

        final_df: pl.DataFrame = pl.concat(rdfs, how='vertical') if rdfs else pl.DataFrame()

        # Округление статистик с рейтингами (проценты) до 4 знаков.
        for col in final_df.columns:
            if 'rtgper' in col.lower() and col not in [s.value for s in self.slices]:
                final_df = final_df.with_columns(pl.col(col).round(4))

        return final_df
