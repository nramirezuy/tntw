import pytest
from elasticsearch import AsyncElasticsearch

from tntw.database import get_session


@pytest.mark.needs_elasticsearch
def test_get_session_is_async(minimal_environment):
    assert isinstance(get_session(), AsyncElasticsearch)


@pytest.mark.needs_elasticsearch
def test_get_session_is_singleton(minimal_environment):
    assert get_session() is get_session()
