import json
import re
from pathlib import Path

import httpx
import pytest

from peneira.sources.semantic_scholar import BASE_URL, SemanticScholar


@pytest.mark.respx(base_url="https://api.semanticscholar.org")
async def test_fetch_articles_from_semantic_scholar(respx_mock):
    payload = json.loads(
        Path(
            "tests/sources/fixtures/semantic_paper_search_bulk_no_token.json"
        ).read_text()
    )
    url = re.compile(rf"{BASE_URL}paper/search/bulk*")
    respx_mock.get(url).mock(return_value=httpx.Response(200, json=payload))
    query = "syndromic surveilance & machine learning"

    semantic_scholar = SemanticScholar(query=query)
    results_bundle = await semantic_scholar.search()

    assert len(results_bundle.results) == 1
    assert semantic_scholar._token is None


@pytest.mark.respx(base_url="https://api.semanticscholar.org")
async def test_fetch_articles_receiving_a_token(respx_mock):
    payload_with_token = json.loads(
        Path("tests/sources/fixtures/semantic_paper_search_bulk.json").read_text()
    )
    payload_without_token = json.loads(
        Path(
            "tests/sources/fixtures/semantic_paper_search_bulk_no_token.json"
        ).read_text()
    )
    url = re.compile(rf"{BASE_URL}paper/search/bulk*")
    route = respx_mock.get(url)
    route.side_effect = [
        httpx.Response(200, json=payload_with_token),
        httpx.Response(200, json=payload_without_token),
    ]

    query = "syndromic surveilance & machine learning"

    semantic_scholar = SemanticScholar(query=query)
    results_bundle = await semantic_scholar.search()

    assert route.call_count == 2
    assert len(results_bundle.results) == 2
    assert semantic_scholar._token is None
