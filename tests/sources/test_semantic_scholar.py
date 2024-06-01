import json
import re
from pathlib import Path

import httpx
import pytest

from peneira.sources.semantic_scholar import BASE_URL, search_semantic_scholar


@pytest.mark.respx(base_url="https://api.semanticscholar.org")
async def test_fetch_articles_from_semantic_scholar(respx_mock):
    payload = json.loads(
        Path("tests/sources/fixtures/semantic_paper_search_bulk.json").read_text()
    )
    url = re.compile(rf"{BASE_URL}paper/search/bulk*")
    respx_mock.get(url).mock(return_value=httpx.Response(200, json=payload))
    query = "syndromic surveilance & machine learning"

    results_bundle = await search_semantic_scholar(query)

    assert len(results_bundle.results) == 1
