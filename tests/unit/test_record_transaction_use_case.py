import pytest

from finman.application.exceptions import (
    CategoryNotFoundError,
    TransactorNotFoundError,
)
from finman.application.use_cases import RecordTransactionUC
from finman.domain.entities import Category, Transactor
from finman.presentation.schemas import NewTransaction


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


async def test_validate_transactor(record_transaction_uc, transaction_repo):
    known_transactor = Transactor(name="Test")
    transaction_repo.get_transactors.return_value = [known_transactor]

    transactor = await record_transaction_uc.validate_transactor("Test")

    assert known_transactor == transactor
    transaction_repo.get_transactors.assert_called_once()


async def test_validate_unknown_transactor(
        record_transaction_uc, transaction_repo,
):
    transaction_repo.get_transactors.return_value = []

    with pytest.raises(TransactorNotFoundError):
        await record_transaction_uc.validate_transactor("Test")


async def test_validate_category(record_transaction_uc, transaction_repo):
    known_category = Category(name="Test")
    transaction_repo.get_categories.return_value = [known_category]

    category = await record_transaction_uc.validate_category("Test")

    assert known_category == category
    transaction_repo.get_categories.assert_called_once()


async def test_validate_unknown_category(
        record_transaction_uc, transaction_repo,
):
    transaction_repo.get_categories.return_value = []

    with pytest.raises(CategoryNotFoundError):
        await record_transaction_uc.validate_category("Test")


async def test_record_transaction(
        record_transaction_uc, transaction_repo, new_transaction,
):
    transaction_repo.save.return_value = 1
    transaction_repo.get_transactors.return_value = [
        Transactor(name="Joe Doe"),
    ]
    transaction_repo.get_categories.return_value = [Category(name="Test")]

    transaction_id = await record_transaction_uc(new_transaction)

    assert transaction_id == 1
    transaction_repo.save.assert_called_once()
    transaction_repo.get_transactors.assert_called_once()
    transaction_repo.get_categories.assert_called_once()
