import pytest
from elasticsearch import AsyncElasticsearch

from tntw.database import get_session


@pytest.mark.needs_elasticsearch
def test_get_session_is_async(minimal_environment):
    assert isinstance(get_session(), AsyncElasticsearch)


@pytest.mark.needs_elasticsearch
def test_get_session_is_singleton(minimal_environment):
    assert get_session() is get_session()


@pytest.mark.needs_elasticsearch
@pytest.mark.asyncio
async def test_session_health(minimal_environment):
    """Verify the session actually works and the cluster is healthy"""
    client = get_session()
    response = await client.options(request_timeout=1).cluster.health(
        wait_for_status="green"
    )
    assert response.get("status") == "green"
