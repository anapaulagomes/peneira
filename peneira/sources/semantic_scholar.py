from dataclasses import dataclass

import httpx
from aiolimiter import AsyncLimiter

from peneira import setup_logger
from peneira.sources import ResultBundle


logger = setup_logger(__name__)

BASE_URL = "https://api.semanticscholar.org/graph/v1/"
SOURCE = "semantic_scholar"
SEMANTIC_SCHOLAR_FIELDS = (
    "url,title,venue,year,authors,externalIds,abstract,openAccessPdf,"
    "fieldsOfStudy,publicationTypes,journal"
)

# with each unauthenticated IP limited to 1 request per second
# https://www.semanticscholar.org/product/api
rate_limiter = AsyncLimiter(60)  # 60 request per minute


@dataclass
class SemanticScholar:
    query: str
    _token: str = None

    def __post_init__(self):
        self._fields = SEMANTIC_SCHOLAR_FIELDS

    async def search(self, _result_bundle=None):
        params = {"fields": self._fields}
        if self._token:
            params["token"] = self._token

        async with rate_limiter:  # wait for a slot to be available
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{BASE_URL}paper/search/bulk?query={self.query}&", params=params
                )
                self._token = response.json().get("token")

                results = response.json().get("data", [])
                if _result_bundle is None:
                    _result_bundle = ResultBundle(
                        url=str(response.url), source=SOURCE, results=results
                    )
                else:
                    _result_bundle.results.extend(results)

                if self._token:
                    return await self.search(_result_bundle=_result_bundle)

                return _result_bundle


async def search_semantic_scholar(query):
    logger.info("Fetching articles for SEMANTIC_SCHOLAR...")
    semantic_scholar = SemanticScholar(query=query)
    return [semantic_scholar.search()]
