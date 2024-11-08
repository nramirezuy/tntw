import pytest

from tntw.api.v1.crawlers import moviedata


@pytest.mark.asyncio
async def test_all_retrieves_all_pages(mocker):
    total_pages = 10

    mock_client = mocker.AsyncMock()
    mocker.patch(
        "tntw.api.v1.crawlers.moviedata.get_client",
        return_value=mock_client,
    )
    mock_get = await mock_client.get()  # Is there a way to avoid awaiting?
    mock_get.raise_for_status = mocker.Mock()

    aiter_data = moviedata.all()
    for page in range(1, total_pages + 1):
        expected = {
            "page": page,
            "total_pages": total_pages,
        }
        mock_get.json = mocker.Mock(return_value=expected)

        data = await anext(aiter_data)
        assert data == expected

    with pytest.raises(StopAsyncIteration):
        await anext(aiter_data)

    assert mock_client.get.await_count == 11  # 10 pages + 1 to setup mock
    assert mock_get.raise_for_status.call_count == 10  # 10 pages
