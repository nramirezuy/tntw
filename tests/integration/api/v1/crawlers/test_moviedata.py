import httpx
import pytest

from tntw.api.v1.crawlers import moviedata


def test_get_client_is_async():
    assert isinstance(moviedata.get_client(), httpx.AsyncClient)


@pytest.mark.skip(reason="Requieres external resource")
@pytest.mark.asyncio
async def test_all_retrieves_data():
    page = 1
    async for data in moviedata.all():
        assert isinstance(data, dict)
        assert data["page"] == page
        page += 1
