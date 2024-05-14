import math

import httpx


BASE_URL = "https://api.openalex.org"
WORKS_PER_PAGE = 200


async def fetch_papers(query, page=1):
    params = {"search": query, "page": page, "per-page": WORKS_PER_PAGE}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/works", params=params)
        return response.json().get("results", [])


async def establish_number_of_pages(query):
    params = {"search": query}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/works", params=params)
        payload = response.json()
        total = payload["meta"]["count"]
        pages = total / WORKS_PER_PAGE
        if pages == 1:
            return pages
        if pages % 2 != 0:
            pages += 1
        return math.trunc(pages)
