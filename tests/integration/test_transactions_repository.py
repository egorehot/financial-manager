from datetime import datetime
from uuid import uuid4

import pytest

from finman.domain.entities import DEFAULT_TZ, NewTransaction
from finman.infrastructure.database.models import Category, Transactor
from finman.infrastructure.database.repositories import (
    SQLAlchemyTransactionsRepository,
)


@pytest.fixture(scope="module")
async def aux_data(sessionmaker):
    category, transactor = str(uuid4()), str(uuid4())
    async with sessionmaker() as session:
        session.add(Category(name=category))
        session.add(Transactor(name=transactor))
        await session.commit()
        return category, transactor


@pytest.fixture
async def repository(sessionmaker):
    async with sessionmaker() as session:
        yield SQLAlchemyTransactionsRepository(session)


async def test_save_transaction(repository, aux_data):
    category, transactor = aux_data
    new_transaction = NewTransaction.model_validate({
        "date": datetime.fromtimestamp(1, tz=DEFAULT_TZ).isoformat(),
        "amount": 100.,
        "currency": "EUR",
        "category": category,
        "transactor": transactor,
        "type": 1,
    })
    saved_id = await repository.save(new_transaction)

    found_transaction = await repository.get_by_id(saved_id)
    assert found_transaction is not None
