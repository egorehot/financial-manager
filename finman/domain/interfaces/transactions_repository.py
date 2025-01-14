from datetime import datetime
from typing import Protocol, Sequence

from finman.domain.entities import Transaction, TransactionType, Category, User


class TransactionsRepository(Protocol):
    async def save(self, transaction: Transaction) -> None: ...

    async def get_transactions(
            self,
            date_from: datetime | None = None,
            date_to: datetime | None = None,
            type_: TransactionType | None = None,
            category: Category | None = None,
            transactor: User | None = None,
    ) -> Sequence[Transaction]: ...

    async def get_by_id(self, transaction_id: int) -> Transaction: ...

    async def update(self, transaction: Transaction) -> None: ...
