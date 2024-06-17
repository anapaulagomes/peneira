import httpx
from aiolimiter import AsyncLimiter

from peneira.sources import ResultBundle


BASE_URL = "https://api.semanticscholar.org/graph/v1/"
SOURCE = "semantic_scholar"
SEMANTIC_SCHOLAR_FIELDS = (
    "url,title,venue,year,authors,externalIds,abstract,openAccessPdf,"
    "fieldsOfStudy,publicationTypes,journal"
)

# with each unauthenticated IP limited to 1 request per second
# https://www.semanticscholar.org/product/api
rate_limiter = AsyncLimiter(60)  # 60 request per minute


async def search_semantic_scholar(query, token=None):
    params = {
        "fields": SEMANTIC_SCHOLAR_FIELDS,
        "token": token,
    }
    async with rate_limiter:  # wait for a slot to be available
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}paper/search/bulk?query={query}&", params=params
            )
            results = response.json().get("data", [])
            token = response.json().get("token")
            return ResultBundle(
                url=str(response.url), source=SOURCE, results=results, _token=token
            )
