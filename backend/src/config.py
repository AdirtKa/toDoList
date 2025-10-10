"""Load data from .env file."""

from pathlib import Path

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

    jwt_secret_key: SecretStr = Field(
        alias='JWT_SECRET_KEY',
    )

    jwt_algorithm: str = Field(default='HS256', alias='JWT_ALGORITHM')
    jwt_access_expires: int = Field(default=3600, alias='JWT_ACCESS_EXPIRES')
    jwt_refresh_expires: int = Field(default=86400, alias='JWT_REFRESH_EXPIRES')


settings = Settings()
