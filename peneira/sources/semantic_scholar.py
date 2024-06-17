import httpx

from peneira.sources import ResultBundle


BASE_URL = "https://api.semanticscholar.org/graph/v1/"
SOURCE = "semantic_scholar"
SEMANTIC_SCHOLAR_FIELDS = (
    "url,title,venue,year,authors,externalIds,abstract,openAccessPdf,"
    "fieldsOfStudy,publicationTypes,journal"
)
# TODO rate limit


async def search_semantic_scholar(query, token=None):
    params = {
        "fields": SEMANTIC_SCHOLAR_FIELDS,
        "token": token,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}paper/search/bulk?query={query}&", params=params
        )
        results = response.json().get("data", [])
        token = response.json().get("token")
        return ResultBundle(
            url=str(response.url), source=SOURCE, results=results, _token=token
        )
