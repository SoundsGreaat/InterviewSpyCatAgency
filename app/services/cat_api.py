import httpx
from app.config import settings

CAT_API_URL = settings.CAT_API_URL


async def validate_breed(breed: str) -> bool:
    try:
        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{CAT_API_URL}/breeds",
                timeout=10.0
            )

            if response.status_code == 200:
                breeds = response.json()
                breed_names = [b.get("name", "").lower() for b in breeds]
                return breed.lower() in breed_names
            else:
                return True
    except Exception:
        return True
