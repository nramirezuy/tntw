import pytest
from pytest import MonkeyPatch


@pytest.fixture
def minimal_environment(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("TNTW_DATABASE_URL", "http://localhost:9200")
