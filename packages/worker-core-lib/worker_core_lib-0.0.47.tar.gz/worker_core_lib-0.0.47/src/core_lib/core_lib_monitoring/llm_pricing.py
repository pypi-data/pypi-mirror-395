"""
LLM pricing service with dynamic pricing retrieval from OpenRouter API.

Provides token usage tracking and cost calculation for LLM calls.
"""
import logging
import os
import time
from dataclasses import dataclass
from typing import Dict, Optional
import httpx

logger = logging.getLogger(__name__)


@dataclass
class LLMUsageMetrics:
    """LLM usage and cost metrics."""
    provider: str
    model: str
    tokens_prompt: int
    tokens_completion: int
    tokens_total: int
    cost_per_prompt_token: float
    cost_per_completion_token: float
    total_cost_usd: float
    cache_hit: bool = False
    retries: int = 0
    fallback_used: bool = False
    model_latency_ms: int = 0


class LLMPricingService:
    """
    Service for retrieving LLM pricing and calculating costs.
    
    Supports dynamic pricing from OpenRouter API with fallback to static pricing.
    """
    
    # Fallback pricing (USD per 1M tokens) - Updated as of Dec 2025
    # Source: https://openrouter.ai/docs#models
    STATIC_PRICING = {
        "google/gemini-2.5-flash": {
            "prompt": 0.075,
            "completion": 0.30,
        },
        "google/gemini-2.5-pro": {
            "prompt": 1.25,
            "completion": 5.00,
        },
        "anthropic/claude-3.5-sonnet": {
            "prompt": 3.00,
            "completion": 15.00,
        },
        "anthropic/claude-3-haiku": {
            "prompt": 0.25,
            "completion": 1.25,
        },
        "openai/gpt-4-turbo": {
            "prompt": 10.00,
            "completion": 30.00,
        },
        "openai/gpt-4o": {
            "prompt": 5.00,
            "completion": 15.00,
        },
        "openai/gpt-4o-mini": {
            "prompt": 0.15,
            "completion": 0.60,
        },
        "openai/gpt-3.5-turbo": {
            "prompt": 0.50,
            "completion": 1.50,
        },
        "meta-llama/llama-3.1-70b-instruct": {
            "prompt": 0.52,
            "completion": 0.75,
        },
        "meta-llama/llama-3.1-8b-instruct": {
            "prompt": 0.06,
            "completion": 0.06,
        },
    }
    
    def __init__(self, enable_api_fetch: bool = True, cache_ttl: int = 3600):
        """
        Initialize pricing service.
        
        Args:
            enable_api_fetch: Whether to fetch pricing from OpenRouter API
            cache_ttl: Cache TTL in seconds (default: 1 hour)
        """
        self.enable_api_fetch = enable_api_fetch
        self.cache_ttl = cache_ttl
        self._pricing_cache: Dict[str, Dict] = {}
        self._cache_timestamp: Optional[float] = None
    
    async def get_pricing(self, model_name: str) -> Dict[str, float]:
        """
        Get pricing for a model.
        
        Args:
            model_name: Model identifier (e.g., "google/gemini-2.5-flash")
        
        Returns:
            Dict with "prompt" and "completion" keys (USD per 1M tokens)
        """
        # Check cache first
        if self._is_cache_valid() and model_name in self._pricing_cache:
            logger.debug(f"Using cached pricing for {model_name}")
            return self._pricing_cache[model_name]
        
        # Try to fetch from API
        if self.enable_api_fetch:
            try:
                api_pricing = await self._fetch_pricing_from_api(model_name)
                if api_pricing:
                    self._pricing_cache[model_name] = api_pricing
                    self._cache_timestamp = time.time()
                    return api_pricing
            except Exception as e:
                logger.warning(f"Failed to fetch pricing from API: {e}, using static pricing")
        
        # Fallback to static pricing
        if model_name in self.STATIC_PRICING:
            return self.STATIC_PRICING[model_name]
        
        # Unknown model - log warning and return default
        logger.warning(f"No pricing data for model {model_name}, using default $0/token")
        return {"prompt": 0.0, "completion": 0.0}
    
    async def _fetch_pricing_from_api(self, model_name: str) -> Optional[Dict[str, float]]:
        """
        Fetch pricing from OpenRouter API.
        
        Args:
            model_name: Model identifier
        
        Returns:
            Pricing dict or None if failed
        """
        try:
            # OpenRouter models API endpoint
            url = "https://openrouter.ai/api/v1/models"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                
                data = response.json()
                models = data.get("data", [])
                
                # Find the model
                for model in models:
                    if model.get("id") == model_name:
                        pricing = model.get("pricing", {})
                        
                        # Extract pricing (API returns per-token prices)
                        prompt_price = float(pricing.get("prompt", 0)) * 1_000_000  # Convert to per-1M
                        completion_price = float(pricing.get("completion", 0)) * 1_000_000
                        
                        logger.info(
                            f"Fetched pricing for {model_name}: "
                            f"prompt=${prompt_price:.2f}/1M, completion=${completion_price:.2f}/1M"
                        )
                        
                        return {
                            "prompt": prompt_price,
                            "completion": completion_price,
                        }
                
                logger.warning(f"Model {model_name} not found in OpenRouter API")
                return None
                
        except Exception as e:
            logger.debug(f"API pricing fetch failed: {e}")
            return None
    
    def _is_cache_valid(self) -> bool:
        """Check if pricing cache is still valid."""
        if self._cache_timestamp is None:
            return False
        
        age = time.time() - self._cache_timestamp
        return age < self.cache_ttl
    
    def calculate_usage_metrics(
        self,
        response_data: Dict,
        model_name: str,
        start_time: float,
        retry_count: int = 0,
        fallback_used: bool = False
    ) -> Optional[LLMUsageMetrics]:
        """
        Calculate usage metrics from LLM API response.
        
        Args:
            response_data: JSON response from LLM API
            model_name: Model used
            start_time: Request start timestamp
            retry_count: Number of retries
            fallback_used: Whether fallback model was used
        
        Returns:
            LLMUsageMetrics if usage data available, None otherwise
        """
        try:
            usage = response_data.get("usage", {})
            if not usage:
                logger.warning("No usage data in LLM API response")
                return None
            
            tokens_prompt = usage.get("prompt_tokens", 0)
            tokens_completion = usage.get("completion_tokens", 0)
            tokens_total = usage.get("total_tokens", tokens_prompt + tokens_completion)
            
            # Get pricing (use cached static pricing synchronously)
            pricing = self.STATIC_PRICING.get(model_name, {"prompt": 0.0, "completion": 0.0})
            
            cost_per_prompt_token = pricing["prompt"] / 1_000_000
            cost_per_completion_token = pricing["completion"] / 1_000_000
            
            total_cost_usd = (
                tokens_prompt * cost_per_prompt_token +
                tokens_completion * cost_per_completion_token
            )
            
            # Check for cache hit (OpenRouter specific field)
            cache_hit = response_data.get("cache_hit", False)
            
            # Calculate latency
            latency_ms = int((time.time() - start_time) * 1000)
            
            return LLMUsageMetrics(
                provider="openrouter",
                model=model_name,
                tokens_prompt=tokens_prompt,
                tokens_completion=tokens_completion,
                tokens_total=tokens_total,
                cost_per_prompt_token=cost_per_prompt_token,
                cost_per_completion_token=cost_per_completion_token,
                total_cost_usd=round(total_cost_usd, 6),
                cache_hit=cache_hit,
                retries=retry_count,
                fallback_used=fallback_used,
                model_latency_ms=latency_ms
            )
            
        except Exception as e:
            logger.error(f"Failed to calculate usage metrics: {e}")
            return None


# Global singleton instance
_pricing_service: Optional[LLMPricingService] = None


def get_pricing_service() -> LLMPricingService:
    """Get or create global pricing service instance."""
    global _pricing_service
    if _pricing_service is None:
        enable_api = os.getenv("ENABLE_LLM_PRICING_API", "true").lower() == "true"
        _pricing_service = LLMPricingService(enable_api_fetch=enable_api)
    return _pricing_service
