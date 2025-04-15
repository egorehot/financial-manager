from datetime import datetime

import pytest
from pydantic import ValidationError

from finman.application.use_cases import GetTransactions
from finman.domain.entities import RecordedTransaction, TransactionsFilter


@pytest.fixture
def get_transactions_uc(uow, transactions_repo):
    return GetTransactions(uow=uow, transactions_repo=transactions_repo)


async def test_get_transactions_no_filters(get_transactions_uc):
    transactions_repo = get_transactions_uc.transactions_repo
    transactions_repo.get_transactions.return_value = []

    filters = TransactionsFilter()
    result = await get_transactions_uc(filters)

    transactions_repo.get_transactions.assert_awaited_once_with(filters)
    assert len(result) == 0
    get_transactions_uc.uow.rollback.assert_awaited_once()


async def test_get_transactions_with_filters(get_transactions_uc):
    transactions_repo = get_transactions_uc.transactions_repo
    return_data = [
        {
            "id": 1,
            "date": datetime(2023, 1, 1),
            "type": 1,
            "amount": 50.0,
            "currency": "USD",
            "transactor": "Alice",
            "category": "Food",
            "created_at": datetime(2023, 1, 1),
            "updated_at": datetime(2023, 1, 1),
        },
        {
            "id": 2,
            "date": datetime(2023, 1, 2),
            "type": 2,
            "amount": 100.0,
            "currency": "USD",
            "transactor": "Bob",
            "category": "Salary",
            "created_at": datetime(2023, 1, 2),
            "updated_at": datetime(2023, 1, 2),
        },
    ]
    transactions_repo.get_transactions.return_value = [
        RecordedTransaction(**t) for t in return_data
    ]

    filters = TransactionsFilter(
        date_from=datetime(2023, 1, 1),
        date_to=datetime(2023, 1, 31),
        types=[1, 2],
        transactors=["Alice", "Bob"],
        categories=["Food", "Salary"],
        limit=50,
    )

    result = await get_transactions_uc(filters)

    transactions_repo.get_transactions.assert_awaited_once_with(filters)

    assert len(result) == 2
    assert all(isinstance(r, RecordedTransaction) for r in result)
    assert result[0].id == 1
    assert result[1].id == 2
    get_transactions_uc.uow.rollback.assert_awaited_once()


async def test_get_transactions_invalid_date_range():
    with pytest.raises(ValidationError):
        TransactionsFilter(
            date_from=datetime(2023, 2, 1),
            date_to=datetime(2023, 1, 1),
            types=[1],
        )
