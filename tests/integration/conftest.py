from alembic import command as alembic_cmd
from alembic.config import Config
import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from finman.main.config import DatabaseSettings, PROJECT_ROOT


@pytest.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(DatabaseSettings.url)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
def sessionmaker(async_engine):
    return async_sessionmaker(async_engine)


@pytest.fixture(scope="session", autouse=True)
async def apply_migrations(async_engine):
    def run_upgrade(connection, cfg):
        cfg.attributes["connection"] = connection
        alembic_cmd.upgrade(cfg, "head")

    async with async_engine.begin() as conn:
        await conn.run_sync(run_upgrade, Config(PROJECT_ROOT / "alembic.ini"))


