import httpx


BASE_URL = "https://api.openalex.org"


async def fetch_papers(query):
    params = {"search": query}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/works", params=params)
        return response.json()
