import logging

from finman.application.base_use_case import UseCase
from finman.application.uow import UoW
from finman.domain.entities import TransactionResponse, TransactionsFilter
from finman.domain.interfaces import TransactionsRepository


log = logging.getLogger(__name__)


class GetTransactions(
    UseCase[TransactionsFilter, list[TransactionResponse]],
):
    def __init__(self, uow: UoW, transactions_repo: TransactionsRepository):
        self.uow = uow
        self.transactions_repo = transactions_repo

    async def __call__(
            self, data: TransactionsFilter,
    ) -> list[TransactionResponse]:
        """Receives filters for transactions,
        returns list of transactions if found"""
        log.info("Getting transaction,list with filters: %s", repr(data))
        transactions = await self.transactions_repo.get_transactions(data)
        log.info("Got %s transactions", len(transactions))
        return list(transactions)
