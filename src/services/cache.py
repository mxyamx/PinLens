import json
import redis.asyncio as redis
from typing import Optional
from src.config import settings
from src.models.validated_pin import ValidatedPin

class CacheService:
    """
    Asynchronous Redis caching layer for storing and retrieving 
    validated pin metadata to reduce AI model invocation costs.
    """
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
        )

    async def get_cached_pin(self, pin_id: str) -> Optional[dict]:
        try:
            cached_data = await self.client.get(f"pin:{pin_id}")
            if cached_data:
                return json.loads(cached_data)
        except Exception:
            # Graceful fallback if Redis is offline during local dev
            return None
        return None

    async def cache_pin(self, pin: ValidatedPin, ttl_seconds: int = 3600) -> None:
        try:
            # Serializes the Pydantic model to JSON string for Redis caching
            await self.client.set(
                name=f"pin:{pin.pin_id}",
                value=pin.model_dump_json(),
                ex=ttl_seconds
            )
        except Exception:
            pass