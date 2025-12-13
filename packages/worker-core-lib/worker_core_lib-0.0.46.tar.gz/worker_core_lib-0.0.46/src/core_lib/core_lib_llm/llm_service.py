import httpx
from typing import Dict, Any

class LLMMetadataService:
    """
    A service for interacting with an LLM to generate model metadata.
    """
    def __init__(self, base_url: str, model_name: str):
        self.base_url = base_url
        self.model_name = model_name

    async def generate_metadata(self, prompt: str) -> Dict[str, Any]:
        """
        Generates metadata for a given prompt using the LLM.
        """
        api_url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(api_url, json=payload, timeout=60.0)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"HTTP error occurred: {e}")
                raise
            except httpx.RequestError as e:
                print(f"An error occurred while requesting {e.request.url!r}.")
                raise