"""
OpenRouter LLM Adapter for worker-core-lib.

This adapter connects to OpenRouter's API gateway to access multiple LLM providers
including Gemini Flash, Claude, GPT-4, and others.

Enhanced with usage metrics tracking for cost monitoring.
"""
import httpx
import logging
import os
import base64
import time
from typing import Optional, List, Union, Dict, Any, Tuple

from .llm_port import LLMPort

logger = logging.getLogger(__name__)

# Import usage metrics (lazy import to avoid circular dependency)
_LLMPricingService = None
_LLMUsageMetrics = None

def _get_pricing_service():
    """Lazy import pricing service."""
    global _LLMPricingService
    if _LLMPricingService is None:
        try:
            from ..core_lib_monitoring.llm_pricing import get_pricing_service
            _LLMPricingService = get_pricing_service
        except ImportError:
            logger.debug("LLM pricing module not available")
            _LLMPricingService = lambda: None
    return _LLMPricingService()

def _get_usage_metrics_class():
    """Lazy import usage metrics class."""
    global _LLMUsageMetrics
    if _LLMUsageMetrics is None:
        try:
            from ..core_lib_monitoring.llm_pricing import LLMUsageMetrics
            _LLMUsageMetrics = LLMUsageMetrics
        except ImportError:
            logger.debug("LLM usage metrics class not available")
            _LLMUsageMetrics = None
    return _LLMUsageMetrics


class OpenRouterSettings:
    """Configuration settings for OpenRouter adapter."""
    
    def __init__(self):
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
        self.OPENROUTER_MODEL_NAMES = os.getenv(
            "OPENROUTER_MODEL_NAMES", 
            "google/gemini-2.5-flash,google/gemini-2.5-pro"
        )
        self.OPENROUTER_BASE_URL = os.getenv(
            "OPENROUTER_BASE_URL",
            "https://openrouter.ai/api/v1"
        )
        self.OPENROUTER_TIMEOUT = int(os.getenv("OPENROUTER_TIMEOUT", "180"))
        self.OPENROUTER_MAX_RETRIES = int(os.getenv("OPENROUTER_MAX_RETRIES", "2"))
        self.OPENROUTER_SITE_URL = os.getenv("OPENROUTER_SITE_URL", "")
        self.OPENROUTER_APP_NAME = os.getenv("OPENROUTER_APP_NAME", "MeshSync-Worker")


class OpenRouterAdapter(LLMPort):
    """
    Adapter to interact with OpenRouter LLM gateway service.
    
    OpenRouter provides access to multiple LLM providers through a single API.
    Supports automatic fallback between models if one fails.
    """

    def __init__(self, settings: Optional[OpenRouterSettings] = None):
        """
        Initialize OpenRouter adapter.
        
        Args:
            settings: Optional OpenRouterSettings instance. If not provided,
                     loads from environment variables.
        
        Raises:
            ValueError: If OPENROUTER_API_KEY is not configured
        """
        if settings:
            self.settings = settings
        else:
            logger.info("OpenRouterSettings not provided, loading from environment.")
            self.settings = OpenRouterSettings()

        if not self.settings.OPENROUTER_API_KEY:
            raise ValueError(
                "OPENROUTER_API_KEY must be set in the environment or OpenRouterSettings. "
                "Get your key from https://openrouter.ai/keys"
            )
        
        # Parse model names (comma-separated list)
        self.model_names: List[str] = [
            name.strip() 
            for name in self.settings.OPENROUTER_MODEL_NAMES.split(",")
            if name.strip()
        ]
        
        if not self.model_names:
            raise ValueError(
                "OPENROUTER_MODEL_NAMES must contain at least one model. "
                "Example: google/gemini-2.5-flash,google/gemini-2.5-pro"
            )
        
        logger.info(
            f"OpenRouter adapter initialized with models: {', '.join(self.model_names)}"
        )
        
        self.current_model: Optional[str] = None  # Track which model is being used
        self.last_usage_metrics: Optional[Any] = None  # Store last LLM usage metrics

    async def generate_text(
        self, 
        prompt: str, 
        max_tokens: int, 
        temperature: float
    ) -> str:
        """
        Generates text using OpenRouter service with multi-model fallback.
        
        Args:
            prompt: The text prompt to send to the LLM
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)
        
        Returns:
            str: Generated text response
        
        Raises:
            Exception: If all models fail to generate text
        
        Note:
            Usage metrics are stored in self.last_usage_metrics after successful call
        """
        # Try each model in sequence until one succeeds
        last_error = None
        retry_count = 0
        
        for model_name in self.model_names:
            for attempt in range(self.settings.OPENROUTER_MAX_RETRIES):
                try:
                    self.current_model = model_name
                    retry_count = attempt
                    logger.info(
                        f"OpenRouter: Generating text with model '{model_name}' "
                        f"(attempt {attempt + 1}/{self.settings.OPENROUTER_MAX_RETRIES})"
                    )
                    
                    response_text, usage_metrics = await self._call_openrouter_api(
                        model_name=model_name,
                        prompt=prompt,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        retry_count=retry_count,
                        fallback_used=(self.model_names.index(model_name) > 0)
                    )
                    
                    # Store usage metrics for caller to access
                    self.last_usage_metrics = usage_metrics
                    
                    logger.info(
                        f"OpenRouter: Successfully generated {len(response_text)} characters "
                        f"with model '{model_name}'"
                    )
                    return response_text
                    
                except Exception as e:
                    last_error = e
                    logger.warning(
                        f"OpenRouter: Model '{model_name}' attempt {attempt + 1} failed: {str(e)}"
                    )
                    
                    # Don't retry on authentication errors
                    if "401" in str(e) or "authentication" in str(e).lower():
                        logger.error(
                            "Authentication failed. Please check your OPENROUTER_API_KEY. "
                            "Get a key from https://openrouter.ai/keys"
                        )
                        raise
                    
                    # Continue to next attempt/model
                    continue
        
        # All models and retries failed
        error_msg = (
            f"OpenRouter: All models failed after {self.settings.OPENROUTER_MAX_RETRIES} "
            f"retries. Models tried: {', '.join(self.model_names)}. "
            f"Last error: {str(last_error)}"
        )
        logger.error(error_msg)
        raise Exception(error_msg)

    async def _call_openrouter_api(
        self,
        model_name: str,
        prompt: str,
        max_tokens: int,
        temperature: float,
        retry_count: int = 0,
        fallback_used: bool = False
    ) -> Tuple[str, Optional[Any]]:
        """
        Make API call to OpenRouter.
        
        Args:
            model_name: Name of the model to use (e.g., "google/gemini-flash-1.5")
            prompt: The prompt text
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            retry_count: Number of retries so far
            fallback_used: Whether this is a fallback model
        
        Returns:
            Tuple of (generated_text, usage_metrics)
        
        Raises:
            httpx.HTTPStatusError: On HTTP errors
            httpx.RequestError: On network errors
        """
        endpoint = f"{self.settings.OPENROUTER_BASE_URL}/chat/completions"
        
        # Build headers
        headers = {
            "Authorization": f"Bearer {self.settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        
        # Add optional headers for usage tracking
        if self.settings.OPENROUTER_SITE_URL:
            headers["HTTP-Referer"] = self.settings.OPENROUTER_SITE_URL
        if self.settings.OPENROUTER_APP_NAME:
            headers["X-Title"] = self.settings.OPENROUTER_APP_NAME
        
        # Build payload (OpenAI-compatible format)
        payload = {
            "model": model_name,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        
        start_time = time.time()
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    endpoint,
                    json=payload,
                    headers=headers,
                    timeout=self.settings.OPENROUTER_TIMEOUT
                )
                response.raise_for_status()
                
                response_data = response.json()
                
                # Extract text from OpenAI-compatible response format
                if "choices" in response_data and len(response_data["choices"]) > 0:
                    message = response_data["choices"][0].get("message", {})
                    content = message.get("content", "").strip()
                    
                    if not content:
                        raise ValueError(
                            f"Empty response from model '{model_name}'. "
                            f"Response: {response_data}"
                        )
                    
                    # Extract usage metrics
                    usage_metrics = self._extract_usage_metrics(
                        response_data, 
                        model_name, 
                        start_time,
                        retry_count,
                        fallback_used
                    )
                    
                    return content, usage_metrics
                else:
                    raise ValueError(
                        f"Unexpected response format from OpenRouter: {response_data}"
                    )

            except httpx.HTTPStatusError as e:
                logger.error(
                    f"OpenRouter HTTP error: {e.response.status_code} - {e.response.text}"
                )
                raise
                
            except httpx.RequestError as e:
                logger.error(
                    f"OpenRouter request error while calling {e.request.url!r}: {str(e)}"
                )
                raise
    
    def _extract_usage_metrics(
        self,
        response_data: Dict,
        model_name: str,
        start_time: float,
        retry_count: int = 0,
        fallback_used: bool = False
    ) -> Optional[Any]:
        """
        Extract usage metrics from OpenRouter API response.
        
        Args:
            response_data: JSON response from OpenRouter API
            model_name: Model used for the request
            start_time: Request start timestamp
            retry_count: Number of retries
            fallback_used: Whether fallback model was used
        
        Returns:
            LLMUsageMetrics if pricing service available, None otherwise
        """
        try:
            pricing_service = _get_pricing_service()
            if pricing_service is None:
                logger.debug("Pricing service not available, skipping usage metrics")
                return None
            
            usage_metrics = pricing_service.calculate_usage_metrics(
                response_data=response_data,
                model_name=model_name,
                start_time=start_time,
                retry_count=retry_count,
                fallback_used=fallback_used
            )
            
            if usage_metrics:
                logger.info(
                    f"LLM usage: {usage_metrics.tokens_total} tokens, "
                    f"${usage_metrics.total_cost_usd:.4f} USD"
                )
            
            return usage_metrics
            
        except Exception as e:
            logger.debug(f"Failed to extract usage metrics: {e}")
            return None

    async def generate_with_vision(
        self,
        prompt: str,
        image_urls: Optional[List[str]] = None,
        image_base64_list: Optional[List[str]] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> str:
        """
        Generates text using vision-capable models with image inputs.
        
        Supports both URL-based images and base64-encoded images.
        
        Args:
            prompt: The text prompt to send to the LLM
            image_urls: List of image URLs (e.g., ["https://example.com/image.jpg"])
            image_base64_list: List of base64-encoded images (e.g., ["data:image/jpeg;base64,/9j/4AAQ..."])
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)
        
        Returns:
            str: Generated text response
        
        Raises:
            ValueError: If neither image_urls nor image_base64_list is provided
            Exception: If all models fail to generate text
        
        Example:
            >>> adapter = OpenRouterAdapter()
            >>> response = await adapter.generate_with_vision(
            ...     prompt="Describe this 3D model",
            ...     image_urls=["https://storage.example.com/thumbnail.jpg"]
            ... )
        """
        if not image_urls and not image_base64_list:
            raise ValueError("Must provide either image_urls or image_base64_list")
        
        # Try each model in sequence until one succeeds
        last_error = None
        
        for model_name in self.model_names:
            for attempt in range(self.settings.OPENROUTER_MAX_RETRIES):
                try:
                    self.current_model = model_name
                    logger.info(
                        f"OpenRouter: Generating text with vision model '{model_name}' "
                        f"(attempt {attempt + 1}/{self.settings.OPENROUTER_MAX_RETRIES})"
                    )
                    
                    response_text = await self._call_openrouter_vision_api(
                        model_name=model_name,
                        prompt=prompt,
                        image_urls=image_urls,
                        image_base64_list=image_base64_list,
                        max_tokens=max_tokens,
                        temperature=temperature
                    )
                    
                    logger.info(
                        f"OpenRouter: Successfully generated {len(response_text)} characters "
                        f"with vision model '{model_name}'"
                    )
                    return response_text
                    
                except Exception as e:
                    last_error = e
                    logger.warning(
                        f"OpenRouter: Vision model '{model_name}' attempt {attempt + 1} failed: {str(e)}"
                    )
                    
                    # Don't retry on authentication errors
                    if "401" in str(e) or "authentication" in str(e).lower():
                        logger.error(
                            "Authentication failed. Please check your OPENROUTER_API_KEY. "
                            "Get a key from https://openrouter.ai/keys"
                        )
                        raise
                    
                    # Continue to next attempt/model
                    continue
        
        # All models and retries failed
        error_msg = (
            f"OpenRouter: All vision models failed after {self.settings.OPENROUTER_MAX_RETRIES} "
            f"retries. Models tried: {', '.join(self.model_names)}. "
            f"Last error: {str(last_error)}"
        )
        logger.error(error_msg)
        raise Exception(error_msg)

    async def _call_openrouter_vision_api(
        self,
        model_name: str,
        prompt: str,
        image_urls: Optional[List[str]],
        image_base64_list: Optional[List[str]],
        max_tokens: int,
        temperature: float
    ) -> str:
        """
        Make API call to OpenRouter with vision model support.
        
        Args:
            model_name: Name of the vision model (e.g., "google/gemini-pro-vision")
            prompt: The text prompt
            image_urls: List of image URLs
            image_base64_list: List of base64-encoded images
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
        
        Returns:
            str: Generated text
        
        Raises:
            httpx.HTTPStatusError: On HTTP errors
            httpx.RequestError: On network errors
        """
        endpoint = f"{self.settings.OPENROUTER_BASE_URL}/chat/completions"
        
        # Build headers
        headers = {
            "Authorization": f"Bearer {self.settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        
        # Add optional headers for usage tracking
        if self.settings.OPENROUTER_SITE_URL:
            headers["HTTP-Referer"] = self.settings.OPENROUTER_SITE_URL
        if self.settings.OPENROUTER_APP_NAME:
            headers["X-Title"] = self.settings.OPENROUTER_APP_NAME
        
        # Build content array with text and images (OpenAI Vision API format)
        content: List[Dict[str, Any]] = [
            {"type": "text", "text": prompt}
        ]
        
        # Add images from URLs
        if image_urls:
            for url in image_urls:
                content.append({
                    "type": "image_url",
                    "image_url": {"url": url}
                })
        
        # Add images from base64
        if image_base64_list:
            for image_data in image_base64_list:
                # Ensure data URI format
                if not image_data.startswith("data:"):
                    # Assume JPEG if no prefix
                    image_data = f"data:image/jpeg;base64,{image_data}"
                
                content.append({
                    "type": "image_url",
                    "image_url": {"url": image_data}
                })
        
        # Build payload (OpenAI-compatible format with vision)
        payload = {
            "model": model_name,
            "messages": [
                {"role": "user", "content": content}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    endpoint,
                    json=payload,
                    headers=headers,
                    timeout=self.settings.OPENROUTER_TIMEOUT
                )
                response.raise_for_status()
                
                response_data = response.json()
                
                # Extract text from OpenAI-compatible response format
                if "choices" in response_data and len(response_data["choices"]) > 0:
                    message = response_data["choices"][0].get("message", {})
                    content_text = message.get("content", "").strip()
                    
                    if not content_text:
                        raise ValueError(
                            f"Empty response from vision model '{model_name}'. "
                            f"Response: {response_data}"
                        )
                    
                    return content_text
                else:
                    raise ValueError(
                        f"Unexpected response format from OpenRouter: {response_data}"
                    )

            except httpx.HTTPStatusError as e:
                logger.error(
                    f"OpenRouter HTTP error: {e.response.status_code} - {e.response.text}"
                )
                raise
                
            except httpx.RequestError as e:
                logger.error(
                    f"OpenRouter request error while calling {e.request.url!r}: {str(e)}"
                )
                raise
