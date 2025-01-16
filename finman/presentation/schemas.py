from datetime import datetime
from typing import Literal

from pydantic import BaseModel, PositiveFloat
from pydantic_extra_types.currency_code import Currency


class NewTransaction(BaseModel):
    date: datetime
    amount: PositiveFloat
    currency: Currency
    category: str
    transactor: str
    type: Literal["expense", "income"]
