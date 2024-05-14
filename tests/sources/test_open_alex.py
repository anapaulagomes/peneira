import httpx
import pytest
from pn.sources.open_alex import fetch_papers


@pytest.mark.respx(base_url="https://api.openalex.org")
async def test_with_marker(respx_mock):
    respx_mock.get("/works").mock(return_value=httpx.Response(200))
    query = "artificial intelligence AND public health"
    response = await fetch_papers(query)
    assert response == {}
