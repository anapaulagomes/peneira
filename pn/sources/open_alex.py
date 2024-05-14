import httpx


BASE_URL = "https://api.openalex.org"


async def fetch_papers(query, page=1):
    params = {"search": query, "page": page, "per-page": 200}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/works", params=params)
        return response.json().get("results", [])
