import pytest
from peneira.sources.core import fetch_papers, establish_number_of_pages
from peneira.sources import ResultBundle


@pytest.mark.asyncio
async def test_fetch_papers_with_rate_limiting():
    query = "machine learning"
    limit = 10
    offset = 0

    result_bundle = await fetch_papers(query, limit, offset)

    assert isinstance(result_bundle, ResultBundle)
    assert result_bundle.source == "CORE"
    assert len(result_bundle.results) <= limit
    assert all("title" in result for result in result_bundle.results)


@pytest.mark.asyncio
async def test_establish_number_of_pages():
    query = "machine learning"
    limit = 10

    pages, total_hits = await establish_number_of_pages(query, limit)

    assert isinstance(pages, int)
    assert isinstance(total_hits, int)
    assert pages > 0
    assert total_hits > 0


@pytest.mark.asyncio
async def test_search_syntax_parsing():
    query = "title:(machine learning)"
    limit = 10
    offset = 0

    result_bundle = await fetch_papers(query, limit, offset)

    assert all(
        "machine learning" in result["title"].lower()
        for result in result_bundle.results
    )


@pytest.mark.asyncio
async def test_correct_mapping_to_result_bundle():
    query = "data science"
    limit = 5
    offset = 0

    result_bundle = await fetch_papers(query, limit, offset)

    assert isinstance(result_bundle, ResultBundle)
    assert result_bundle.source == "CORE"
    assert "url" in result_bundle.__dict__
    assert "results" in result_bundle.__dict__
    assert len(result_bundle.results) == limit
    assert all(isinstance(result, dict) for result in result_bundle.results)
