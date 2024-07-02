import math

import httpx

from peneira import setup_logger
from peneira.sources import ResultBundle
from aiolimiter import AsyncLimiter


logger = setup_logger(__name__)
BASE_URL = "https://api.openalex.org"
WORKS_PER_PAGE = 200
SOURCE = "open_alex"

# allow for 10 requests per second
# https://docs.openalex.org/how-to-use-the-api/rate-limits-and-authentication
rate_limiter = AsyncLimiter(10)


async def fetch_papers(query, page=1):
    params = {"search": query, "page": page, "per-page": WORKS_PER_PAGE}
    async with rate_limiter:  # wait for a slot to be available
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/works", params=params)
            results = response.json().get("results", [])
            return ResultBundle(url=str(response.url), source=SOURCE, results=results)


async def establish_number_of_pages(query):
    params = {"search": query}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/works", params=params)
        payload = response.json()
        total = payload["meta"]["count"]
        pages = total / WORKS_PER_PAGE
        if pages != 1 and pages % 2 != 0:
            pages += 1
        return math.trunc(pages), total


def map_to_bibtex_type(capsule):
    result = capsule["result"]
    authors_list = []
    institutions_list = []
    countries = []
    authorships = result.get("authorships", [{}])
    for authorship in authorships:
        authors_list.append(authorship.get("author", {}).get("display_name", ""))
        if authorship.get("institutions"):
            institutions_list.extend(
                [
                    institution.get("display_name", "")
                    for institution in authorship.get("institutions")
                ]
            )
        if authorship.get("countries"):
            countries.extend(authorship["countries"])

    authors = " and ".join(authors_list)
    institutions = ", ".join(institutions_list)
    countries = ", ".join(sorted(set(countries)))
    all_keywords = []
    all_keywords.extend(
        [keyword["display_name"] for keyword in result.get("keywords", [])]
    )
    all_keywords.extend(
        [keyword["descriptor_name"] for keyword in result.get("mesh", [])]
    )
    all_keywords.extend(
        [keyword["display_name"] for keyword in result.get("concepts", [])]
    )
    all_keywords = ", ".join(sorted(set(all_keywords)))

    return {
        "id": result.get("id", ""),
        "doi": result.get("doi", ""),
        "title": result.get("title", ""),
        "year": result.get("publication_year", ""),
        "date": result.get("publication_date", ""),
        "authors": authors,
        "institutions": institutions,
        "country": countries,
        "language": result.get("language", ""),
        "type": result.get("type", ""),
        "open_access": result.get("open_access", {}).get("oa_status", ""),
        "abstract": "",  # this source does not provide abstracts
        "keywords": all_keywords,
        "url": capsule.get("url", ""),
        "source": capsule.get("source", ""),
        "created_at": capsule.get("created_at", ""),
    }


async def search_open_alex(query):
    number_of_pages, total = await establish_number_of_pages(query)
    logger.info(
        f"Fetching articles for OPEN_ALEX... {total} papers "
        f"distributed in {number_of_pages} pages."
    )
    tasks = [fetch_papers(query, page) for page in range(1, number_of_pages + 1)]
    return tasks
