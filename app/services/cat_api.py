import httpx
import os
from dotenv import load_dotenv

load_dotenv()

CAT_API_URL = os.getenv("CAT_API_URL", "https://api.thecatapi.com/v1")


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
