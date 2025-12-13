import httpx
import logging
from typing import Optional

from .llm_port import LLMPort
from ..core_lib_config.settings import OllamaSettings

logger = logging.getLogger(__name__)

class OllamaAdapter(LLMPort):
    """
    An adapter to interact with an Ollama LLM service.
    """

    def __init__(self, settings: Optional[OllamaSettings] = None):
        if settings:
            self.settings = settings
        else:
            logger.info("OllamaSettings not provided, loading from environment.")
            self.settings = OllamaSettings()

        if not self.settings.OLLAMA_API_URL:
            raise ValueError("OLLAMA_API_URL must be set in the environment or OllamaSettings.")

    async def generate_text(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """
        Generates text using the Ollama service.
        """
        endpoint = f"{self.settings.OLLAMA_API_URL}/api/generate"
        payload = {
            "model": self.settings.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature,
            },
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(endpoint, json=payload, timeout=self.settings.OLLAMA_REQUEST_TIMEOUT)
                response.raise_for_status()
                
                response_data = response.json()
                return response_data.get("response", "").strip()

            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
                raise
            except httpx.RequestError as e:
                logger.error(f"An error occurred while requesting {e.request.url!r}.")
                raise