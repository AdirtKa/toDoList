"""Load data from .env file."""

from pathlib import Path

from fastapi_jwt_auth import AuthJWT
from pydantic import AliasChoices, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR.parent / '.env'


class Settings(BaseSettings):
    """Base project settings."""

    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH), env_file_encoding='utf-8', env_prefix='', case_sensitive=False, extra='ignore'
    )

    database_url: str = Field(
        validation_alias=AliasChoices('DATABASE_URL', 'db_url'),
        description='DSN Postgres',
    )

    authjwt_secret_key: SecretStr = Field(
        validation_alias='AuthJWT_SECRET_KEY',
    )


settings = Settings()


@AuthJWT.load_config
def get_config() -> Settings:
    """Load config from env file for jwt auth."""
    return settings
