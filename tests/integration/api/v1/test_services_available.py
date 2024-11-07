import pytest


@pytest.mark.needs_elasticsearch
@pytest.mark.asyncio
async def test_elasticsearch_session_health(elasticsearch_client) -> None:
    """Verify the session actually works and the cluster is healthy"""
    response = await elasticsearch_client.options(
        request_timeout=1
    ).cluster.health(wait_for_status="green")
    assert response.get("status") == "green"
