import httpx
from aiolimiter import AsyncLimiter

from peneira import setup_logger
from peneira.sources import ResultBundle


logger = setup_logger(__name__)
BASE_URL = "https://api.core.ac.uk/v3/search/works"
SOURCE = "CORE"

# allows 1,000 tokens per day, maximum 10 per minute for unregistered users
rate_limiter = AsyncLimiter(10)

# TODO omit abstracts and full texts from the results
# dict_keys(['arxivId', 'authors', 'contributors', 'outputs', 'createdDate',
# 'dataProviders', 'abstract', 'documentType', 'doi', 'downloadUrl', 'fieldOfStudy',
# 'fullText', 'id', 'identifiers', 'title', 'language', 'magId', 'oaiIds',
# 'publishedDate',
# 'publisher', 'pubmedId', 'references', 'sourceFulltextUrls', 'updatedDate',
# 'yearPublished', 'journals', 'links'])


async def fetch_papers(query, limit=10, offset=0):
    params = {"q": query, "limit": limit, "offset": offset}
    async with rate_limiter:  # wait for a slot to be available
        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL, params=params, follow_redirects=True)
            if response.is_success:
                results = response.json().get("data", [])
            else:
                logger.error(
                    f"Failed to establish number of pages for CORE: {response.text}"
                )
                results = []
            return ResultBundle(url=str(response.url), source=SOURCE, results=results)


async def establish_number_of_pages(query, limit=10):
    params = {"q": query, "limit": limit}
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params, follow_redirects=True)
        if response.is_success:
            total_hits = response.json().get("totalHits", 0)
            pages = total_hits / limit
            return int(pages) if pages.is_integer() else int(pages) + 1, total_hits

        logger.error(f"Failed to establish number of pages for CORE: {response.text}")
        return 0, 0


async def search_core(query):
    number_of_pages, total = await establish_number_of_pages(query)
    logger.info(
        f"Fetching articles for CORE... {total} papers "
        f"distributed in {number_of_pages} pages."
    )
    tasks = [fetch_papers(query, page) for page in range(1, number_of_pages + 1)]
    return tasks
