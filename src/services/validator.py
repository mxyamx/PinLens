from pydantic import BaseModel, Field
from typing import List, Optional
import time
import random
from src.telemetry.metrics import (
    PIN_INGEST_COUNT as pins_ingested_total,
    VALIDATION_FAILURES as validation_failures_total,
    CACHE_HITS as cache_hits_total,
)

class RawPinIngest(BaseModel):
    pin_id: str = Field(..., description="Unique identifier for the pin")
    image_url: str = Field(..., description="Source URL of the ingested image")
    raw_caption: Optional[str] = Field(default="", description="User-provided prompt or caption")
    simulate_low_confidence: Optional[bool] = Field(default=False, description="Flag to test guardrail rejection")
    force_cache: Optional[bool] = Field(default=False, description="Flag to simulate a Redis cache hit")

class ValidatedPin(BaseModel):
    pin_id: str
    image_url: str
    raw_caption: str
    category: str
    tags: List[str]
    confidence_score: float
    is_safe: bool
    processed_at: float

class PinValidationEngine:
    """
    Core AI Visual Metadata Ingestion & Guardrail Validation Engine.
    Enforces confidence floors (< 0.70 rejection), tags generation, and Redis caching tiers.
    """
    def __init__(self):
        # In-memory Redis simulation tier dictionary
        self._redis_cache = {}

    async def process_and_validate(self, payload: RawPinIngest) -> ValidatedPin:
        start_time = time.time()
        
        # 1. Check Redis Cache Simulation
        if payload.force_cache or payload.pin_id in self._redis_cache:
            cache_hits_total.inc()
            cached_data = self._redis_cache.get(payload.pin_id)
            if cached_data:
                return cached_data

        pins_ingested_total.inc()

        # 2. Simulate AI Vision Classification & Confidence Scoring
        if payload.simulate_low_confidence:
            confidence = round(random.uniform(0.40, 0.68), 2)
        else:
            confidence = round(random.uniform(0.85, 0.99), 2)

        # 3. Guardrail Check: Confidence Floor (< 0.70 triggers rejection)
        if confidence < 0.70:
            validation_failures_total.inc()
            raise ValueError(
                f"Guardrail Rejection: Pin '{payload.pin_id}' evaluated with low AI confidence score ({confidence}). Minimum required threshold is 0.70."
            )

        # 4. Extract Category and Tags based on caption or defaults
        caption_lower = (payload.raw_caption or "").lower()
        if "arch" in caption_lower or "room" in caption_lower or "interior" in caption_lower:
            category = "Architecture & Interior"
            tags = ["design", "minimalist", "aesthetic", "interior"]
        elif "food" in caption_lower or "salad" in caption_lower or "bowl" in caption_lower:
            category = "Food & Recipes"
            tags = ["healthy", "organic", "recipe", "fresh"]
        elif "fashion" in caption_lower or "outfit" in caption_lower:
            category = "Fashion & Style"
            tags = ["streetwear", "style", "outfit", "trend"]
        else:
            category = "Visual Discovery"
            tags = ["inspiration", "curated", "pinlens", "ai-verified"]

        validated_pin = ValidatedPin(
            pin_id=payload.pin_id,
            image_url=payload.image_url,
            raw_caption=payload.raw_caption or "AI processed metadata payload",
            category=category,
            tags=tags,
            confidence_score=confidence,
            is_safe=True,
            processed_at=time.time()
        )

        # Save to Redis cache tier simulation
        self._redis_cache[payload.pin_id] = validated_pin
        return validated_pin