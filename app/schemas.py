from decimal import Decimal
from typing import Annotated, Self

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    model_validator,
)

NonEmptyText = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1),
]

class TravelRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    employee_name: NonEmptyText
    department: NonEmptyText
    origin: NonEmptyText
    destination: NonEmptyText
    departure_date: AwareDatetime
    return_date: AwareDatetime
    estimated_budget: Decimal = Field(
        gt=0,
        decimal_places=2,
        allow_inf_nan=False,
    )

    @model_validator(mode="after")
    def validate_date_order(self) -> Self:
        if self.return_date <= self.departure_date:
            raise ValueError("A data de retorno deve ser posterior à partida.")
        return self