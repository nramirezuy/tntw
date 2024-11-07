import functools

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TNTW_")

    DATABASE_URL: AnyHttpUrl


@functools.lru_cache(maxsize=1)
def get_settings():
    return Config()
