import json

import httpx
import pytest
from pn.sources.open_alex import fetch_papers, establish_number_of_pages


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


@pytest.mark.respx(base_url="https://api.openalex.org")
async def test_return_all_results_from_first_page(respx_mock):
    payload = json.loads(open("tests/sources/fixtures/works.json").read())
    respx_mock.get("/works").mock(return_value=httpx.Response(200, json=payload))
    query = "machine learning AND public health"

    results = await fetch_papers(query)

    assert len(results) == 49


@pytest.mark.respx(base_url="https://api.openalex.org")
async def test_add_support_to_pagination(respx_mock):
    payload = json.loads(open("tests/sources/fixtures/works.json").read())
    respx_mock.get("/works").mock(return_value=httpx.Response(200, json=payload))
    query = "machine learning AND public health"

    results = await fetch_papers(query, page=10)

    assert len(results) == 49


@pytest.mark.parametrize(
    "count,expected_pages",
    [
        (340, 2),
        (49, 1),
        (100, 1),
        (200, 1),
        (400, 2),
        (2500, 13),
    ],
)
@pytest.mark.respx(base_url="https://api.openalex.org")
async def test_establish_number_of_pages(respx_mock, count, expected_pages):
    payload = json.loads(open("tests/sources/fixtures/works.json").read())
    payload["meta"]["count"] = count
    respx_mock.get("/works").mock(return_value=httpx.Response(200, json=payload))
    query = "machine learning AND public health"

    number_of_pages = await establish_number_of_pages(query)

    assert number_of_pages == expected_pages
