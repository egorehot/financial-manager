import logging

from finman.application.base_use_case import UseCase
from finman.domain.entities import Transaction
from finman.domain.interfaces import TransactionsRepository, UoW
from finman.presentation.schemas import NewTransaction


log = logging.getLogger(__name__)


class RecordTransactionUC(UseCase[NewTransaction, int]):
    def __init__(self, uow: UoW, transactions_repo: TransactionsRepository):
        self.uow = uow
        self.transactions_repo = transactions_repo

    async def __call__(self, data: NewTransaction) -> int:
        """Receives a transaction to save, return its identifier"""
        transaction = Transaction.from_object(data)
        log.debug(f"Received new transaction: {transaction!r}")
        transaction_id = await self.transactions_repo.save(transaction)
        await self.uow.commit()
        return transaction_id
