import httpx
import pytest
from pn.sources.open_alex import fetch_papers


@pytest.mark.respx(base_url="https://api.openalex.org")
async def test_no_results_due_to_end_of_pagination(respx_mock):
    payload = {
        "meta": {
            "count": 340,
            "db_response_time_ms": 303,
            "page": 15,
            "per_page": 25,
            "groups_count": None,
        },
        "results": [],
        "group_by": [],
    }
    respx_mock.get("/works").mock(return_value=httpx.Response(200, json=payload))
    query = "artificial intelligence AND public health"

    results = await fetch_papers(query)

    assert results == []
