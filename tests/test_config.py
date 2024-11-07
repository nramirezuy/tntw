from pydantic_settings import BaseSettings

from tntw.config import get_settings


def test_settings_is_pydantic_settings(minimal_environment) -> None:
    assert isinstance(get_settings(), BaseSettings)


def test_settings_is_singleton(minimal_environment) -> None:
    assert get_settings() is get_settings()
