import math

import httpx

from pn.sources import ResultBundle

BASE_URL = "https://api.openalex.org"
WORKS_PER_PAGE = 200
SOURCE = "open_alex"


async def fetch_papers(query, page=1):
    params = {"search": query, "page": page, "per-page": WORKS_PER_PAGE}
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
