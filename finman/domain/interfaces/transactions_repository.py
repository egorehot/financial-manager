from abc import ABC, abstractmethod
from collections.abc import Sequence

from finman.domain.entities import (
    NewTransaction,
    TransactionResponse,
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
    ) -> Sequence[TransactionResponse]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, transaction_id: int) -> TransactionResponse:
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

    @abstractmethod
    async def get_transactors(self) -> Sequence[str]:
        raise NotImplementedError

    @abstractmethod
    async def get_categories(self) -> Sequence[str]:
        raise NotImplementedError
