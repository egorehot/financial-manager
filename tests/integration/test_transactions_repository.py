import pytest

from finman.domain.entities import NewTransaction
from finman.infrastructure.database.models import Category, Transactor
from finman.infrastructure.database.repositories import (
    SQLAlchemyTransactionsRepository,
)


@pytest.fixture(scope="module")
async def aux_data(sessionmaker):
    async with sessionmaker() as session:
        session.add(Category(name="Test Category"))
        session.add(Transactor(name="Test Transactor"))
        await session.commit()


@pytest.fixture
async def repository(sessionmaker, aux_data):
    async with sessionmaker() as session:
        yield SQLAlchemyTransactionsRepository(session)


async def test_save_transaction(repository):  # TODO
    new_transaction = NewTransaction(
        date=...,
        amount=...,
        currency=...,
        category=...,
        transactor=...,
        type=...,
    )
    saved_id = await repository.save(new_transaction)

    found_transaction = await repository.get_by_id(saved_id)
    assert found_transaction is not None
