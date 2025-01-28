from datetime import datetime
from enum import Enum
from typing import Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PositiveFloat,
    model_validator,
)
from pydantic_extra_types.currency_code import Currency

from finman.application.exceptions import IncorrectFilterDatesError


class TransactionType(Enum):
    EXPENSE = 1
    INCOME = 2


class NewTransaction(BaseModel):
    date: datetime
    amount: PositiveFloat
    currency: Currency
    category: str
    transactor: str
    type: TransactionType


class RecordedTransaction(NewTransaction):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TransactionsFilter(BaseModel):
    date_from: datetime | None = None
    date_to: datetime | None = None
    types: list[TransactionType] | None = None
    transactors: list[str] | None = None
    categories: list[str] | None = None
    limit: int = Field(default=100, gt=0, le=1000)

    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        if self.date_from and self.date_to and self.date_from > self.date_to:
            raise IncorrectFilterDatesError(self.date_from, self.date_to)
        return self
