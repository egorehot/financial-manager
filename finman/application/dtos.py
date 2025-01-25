from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, PositiveFloat
from pydantic_extra_types.currency_code import Currency


class NewTransaction(BaseModel):
    date: datetime
    amount: PositiveFloat
    currency: Currency
    category: str
    transactor: str
    type: Literal["expense", "income"]


class TransactionsFilter(BaseModel):
    date_from: datetime | None = None
    date_to: datetime | None = None
    types: list[Literal["expense", "income"]] | None = None
    transactors: list[str] | None = None
    categories: list[str] | None = None
    limit: int = Field(default=100, gt=0, le=1000)


class TransactionResponse(NewTransaction):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
