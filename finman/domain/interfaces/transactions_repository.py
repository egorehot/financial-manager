from abc import ABC, abstractmethod
from collections.abc import Sequence

from finman.domain.entities import (
    NewTransaction,
    RecordedTransaction,
    TransactionsFilter,
)


class TransactionsRepository(ABC):
    @abstractmethod
    async def save(self, transaction: NewTransaction) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_transactions(
            self,
            filters: TransactionsFilter,
    ) -> Sequence[RecordedTransaction]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
            self, transaction_id: int,
    ) -> RecordedTransaction | None:
        raise NotImplementedError

    @abstractmethod
    async def update(
            self,
            transaction_id: int,
            transaction: NewTransaction,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, transaction_id: int) -> None:
        raise NotImplementedError
