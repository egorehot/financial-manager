import logging

from finman.application.base_use_case import UseCase
from finman.application.uow import UoW
from finman.domain.interfaces import TransactionsRepository


log = logging.getLogger(__name__)


class DeleteTransaction(UseCase[int, None]):
    def __init__(self, uow: UoW, transactions_repo: TransactionsRepository):
        self.uow = uow
        self.transactions_repo = transactions_repo

    async def __call__(self, data: int) -> None:
        try:
            await self.transactions_repo.delete(data)
            await self.uow.commit()
        except Exception:
            await self.uow.rollback()
            log.exception("Failed to delete transaction with id: %r", data)
            raise
