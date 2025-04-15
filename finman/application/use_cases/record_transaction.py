import logging

from finman.application.base_use_case import UseCase
from finman.application.uow import UoW
from finman.domain.entities import NewTransaction
from finman.domain.interfaces import TransactionsRepository


log = logging.getLogger(__name__)


class RecordTransaction(UseCase[NewTransaction, int]):
    def __init__(self, uow: UoW, transactions_repo: TransactionsRepository):
        self.uow = uow
        self.transactions_repo = transactions_repo

    async def __call__(self, data: NewTransaction) -> int:
        """Receives a transaction to save, returns its identifier"""
        log.debug("Received new transaction: %r", data)
        try:
            transaction_id = await self.transactions_repo.save(data)
            await self.uow.commit()
        except Exception:
            await self.uow.rollback()
            log.exception("Failed to record transaction: %r", data)
            raise
        else:
            return transaction_id
