from abc import ABC, abstractmethod

class LLMPort(ABC):
    """
    An abstract port for Large Language Model services.
    """

    @abstractmethod
    async def generate_text(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """
        Generates text based on a given prompt.
        """
        raise NotImplementedError