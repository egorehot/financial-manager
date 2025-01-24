from datetime import datetime

import pytest

from finman.application.exceptions import IncorrectFilterDatesError
from finman.application.use_cases import GetTransactionsUC
from finman.domain.entities import (
    Category,
    Transaction,
    TransactionType,
    Transactor,
)
from finman.presentation.schemas import TransactionResponse, TransactionsFilter


@pytest.fixture
def get_transactions_uc(uow, transactions_repo):
    return GetTransactionsUC(uow=uow, transactions_repo=transactions_repo)


async def test_get_transactions_no_filters(
        get_transactions_uc, transactions_repo,
):
    transactions_repo.get_transactions.return_value = []

    filters = TransactionsFilter()

    result = await get_transactions_uc(filters)

    transactions_repo.get_transactions.assert_awaited_once_with(
        date_from=None,
        date_to=None,
        types=None,
        categories=None,
        transactors=None,
        limit=100,
    )
    assert result == [], "Expected an empty list of TransactionResponse"


async def test_get_transactions_with_filters(
        get_transactions_uc, transactions_repo,
):
    return_data = [
        {
            "id": 1,
            "date": datetime(2023, 1, 1),
            "type": "expense",
            "amount": 50.0,
            "currency": "USD",
            "transactor": Transactor(name="Alice"),
            "category": Category(name="Food"),
            "created_at": datetime(2023, 1, 1),
            "updated_at": datetime(2023, 1, 1),
        },
        {
            "id": 2,
            "date": datetime(2023, 1, 2),
            "type": "income",
            "amount": 100.0,
            "currency": "USD",
            "transactor": Transactor(name="Bob"),
            "category": Category(name="Salary"),
            "created_at": datetime(2023, 1, 2),
            "updated_at": datetime(2023, 1, 2),
        },
    ]
    transactions_repo.get_transactions.return_value = [
        Transaction(**t) for t in return_data
    ]

    filters = TransactionsFilter(
        date_from=datetime(2023, 1, 1),
        date_to=datetime(2023, 1, 31),
        types=["expense", "income"],
        transactors=["Alice", "Bob"],
        categories=["Food", "Salary"],
        limit=50,
    )

    result = await get_transactions_uc(filters)

    transactions_repo.get_transactions.assert_awaited_once_with(
        date_from=datetime(2023, 1, 1),
        date_to=datetime(2023, 1, 31),
        types=[TransactionType.EXPENSE, TransactionType.INCOME],
        categories=[Category(name="Food"), Category(name="Salary")],
        transactors=[Transactor(name="Alice"), Transactor(name="Bob")],
        limit=50,
    )

    assert len(result) == 2
    assert all(isinstance(r, TransactionResponse) for r in result)
    assert result[0].id == 1
    assert result[1].id == 2


@pytest.mark.asyncio
async def test_get_transactions_invalid_date_range(
        get_transactions_uc, transactions_repo,
):
    filters = TransactionsFilter(
        date_from=datetime(2023, 2, 1),
        date_to=datetime(2023, 1, 1),
        types=["expense"],
    )

    with pytest.raises(IncorrectFilterDatesError):
        await get_transactions_uc(filters)

    transactions_repo.get_transactions.assert_not_awaited()
