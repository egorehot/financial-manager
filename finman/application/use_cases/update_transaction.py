import logging

from finman.application.base_use_case import UseCase
from finman.application.uow import UoW
from finman.domain.interfaces import TransactionsRepository
from finman.domain.entities import NewTransaction


log = logging.getLogger(__name__)


class UpdateTransaction(UseCase[tuple[int, NewTransaction], None]):
    def __init__(self, uow: UoW, transactions_repo: TransactionsRepository):
        self.uow = uow
        self.transactions_repo = transactions_repo

    async def __call__(self, data: tuple[int, NewTransaction]) -> None:
        transaction_id, new_transaction = data
        try:
            await self.transactions_repo.update(
                transaction_id, new_transaction,
            )
            await self.uow.commit()
        except Exception:
            await self.uow.rollback()
            msg = "Failed to update transaction with id=%r to %r"
            log.exception(msg, transaction_id, new_transaction)
            raise
