"""Module for managing env variables."""

from functools import cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DbStorage(BaseModel):
    """Settings for database."""

    drivername: str = ""
    host: str = ""
    port: int = -1
    database: str = ""
    user: str = ""
    password: str = ""


class Redis(BaseModel):
    """Settings for redis."""

    host: str = ""
    port: int = -1
    password: str = ""
    queue_db: int = -1


class Celery(BaseModel):
    """Setting for celery."""

    simulator_aer_queue: str = ""
    compiler_qiskit_queue: str = ""
    compiler_zne_pass_queue: str = ""
    margin_after_soft_timeout: float = 1.0


class EnvironmentSettings(BaseSettings):
    """Class holder all different env settings."""

    db: DbStorage = DbStorage()
    redis: Redis = Redis()
    celery: Celery = Celery()

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


@cache
def get_settings():
    """Returns cached version of env settings."""
    return EnvironmentSettings()
