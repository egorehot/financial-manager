from finman.application.base_use_case import UseCase
from finman.application.uow import UoW
from finman.domain.entities import Transaction
from finman.domain.interfaces import TransactionsRepository


class GetTransactionByIdUC(UseCase[int, Transaction | None]):
    def __init__(self, uow: UoW, transactions_repo: TransactionsRepository):
        self.uow = uow
        self.transactions_repo = transactions_repo

    async def __call__(self, data: int) -> Transaction | None:
        return await self.transactions_repo.get_by_id(data)
