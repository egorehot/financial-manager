from unittest.mock import Mock

import pytest

from finman.application.uow import UoW
from finman.application.use_cases import RecordTransactionUC
from finman.domain.interfaces import TransactionsRepository
from finman.presentation.schemas import NewTransaction


@pytest.fixture
def transaction_repo():
    return Mock(spec=TransactionsRepository)


@pytest.fixture
def uow():
    return Mock(spec=UoW)


@pytest.fixture
def new_transaction():
    return NewTransaction.model_validate({
        "date": 0,
        "amount": 1,
        "currency": "EUR",
        "category": "Test",
        "transactor": "Joe Doe",
        "type": "expense",
    })

@pytest.fixture
def record_transaction_uc(uow, transaction_repo):
    return RecordTransactionUC(uow=uow, transactions_repo=transaction_repo)


async def test_record_transaction(
        record_transaction_uc, transaction_repo, new_transaction
):
    transaction_repo.save.return_value = 1

    transaction_id = await record_transaction_uc(new_transaction)

    assert transaction_id == 1
    transaction_repo.save.assert_called_once()
