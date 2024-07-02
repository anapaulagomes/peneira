import httpx
from aiolimiter import AsyncLimiter
from peneira.sources import ResultBundle


BASE_URL = "https://api.core.ac.uk/v3/search"
SOURCE = "CORE"
# allows 1,000 tokens per day, maximum 10 per minute for unregistered users
rate_limiter = AsyncLimiter(10)


async def fetch_papers(query, limit=10, offset=0):
    params = {"q": query, "limit": limit, "offset": offset}
    async with rate_limiter:  # wait for a slot to be available
        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL, params=params)
            results = response.json().get("data", [])
            return ResultBundle(url=str(response.url), source=SOURCE, results=results)


async def establish_number_of_pages(query, limit=10):
    params = {"q": query, "limit": limit}
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)
        total_hits = response.json().get("totalHits", 0)
        pages = total_hits / limit
        return int(pages) if pages.is_integer() else int(pages) + 1, total_hits
