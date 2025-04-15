import pytest

from finman.application.use_cases import RecordTransaction
from finman.domain.entities import NewTransaction


@pytest.fixture
def new_transaction():
    return NewTransaction.model_validate({
        "date": 0,
        "amount": 1,
        "currency": "EUR",
        "category": "Test",
        "transactor": "Joe Doe",
        "type": 1,
    })


@pytest.fixture
def record_transaction_uc(uow, transactions_repo):
    return RecordTransaction(uow=uow, transactions_repo=transactions_repo)


async def test_record_transaction( record_transaction_uc, new_transaction):
    record_transaction_uc.transactions_repo.save.return_value = 1

    transaction_id = await record_transaction_uc(new_transaction)

    assert transaction_id == 1
    record_transaction_uc.transactions_repo.save.assert_awaited_once()
    record_transaction_uc.uow.commit.assert_awaited_once()
