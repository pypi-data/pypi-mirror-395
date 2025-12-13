from pydantic import BaseModel, Field, computed_field, model_validator
from typing_extensions import Annotated, Self

from telemars.params.options import general as gval


class Option(BaseModel):
    """Опции отчета Simple."""

    kit_id: Annotated[gval.KitId, Field(default=gval.KitId.BIG_TV, serialization_alias='kitId')]
    big_tv: Annotated[gval.BigTv, Field(default=gval.BigTv.YES, serialization_alias='bigTv')]

    @model_validator(mode='after')
    def check_big_tv_condition(self) -> Self:
        if self.kit_id == gval.KitId.BIG_TV and self.big_tv != gval.BigTv.YES:
            raise ValueError('При расчете по KitID 7 атрибут BigTV должен быть равен True.')

        return self

    # Важно исключить вычисляемые поля, чтобы избежать рекурсии. Особенность Pydantic.
    @computed_field
    @property
    def expr(self) -> dict:
        """Возвращает опции в формате JSON."""
        return self.model_dump(by_alias=True, exclude={'expr'}, mode='json')
