from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


PROJECT_ROOT = Path(__file__).parents[2].resolve()


class _DatabaseSettings(BaseSettings):
    driver: str = "sqlite"
    user: str | None = None
    password: str | None = None
    host: str | None = None
    port: int | None = None
    database: str | None = None

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_prefix="FINMAN_DB_",
        env_nested_delimiter="__",
        case_sensitive=False,
    )

    @property
    def url(self) -> URL:
        return URL.create(
            drivername=self.driver,
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )


DatabaseSettings = _DatabaseSettings()
