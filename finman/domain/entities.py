from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, PositiveFloat
from pydantic_extra_types.currency_code import Currency


class TransactionType(Enum):
    EXPENSE = "expense"
    INCOME = "income"


class Transaction(BaseModel):
    date: datetime
    type: TransactionType
    transactor: "Transactor"
    category: "Category"
    amount: PositiveFloat
    currency: Currency
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class Transactor(BaseModel):
    name: str


class Category(BaseModel):
    name: str
    parent: Optional["Category"] = None
