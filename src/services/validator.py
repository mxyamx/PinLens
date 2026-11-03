import time
from datetime import datetime, timezone
from src.models.raw_pin import RawPinIngest
from src.models.validated_pin import ValidatedPin
from src.services.ai_extractor import AIExtractionEngine
from src.services.cache import CacheService
from src.telemetry.metrics import (
    PIN_INGEST_COUNT,
    VALIDATION_FAILURES,
    PROCESSING_LATENCY,
    CACHE_HITS
)

class PinValidationEngine:
    """
    Coordinates caching, AI extraction, validation guardrails, and telemetry.
    """
    def __init__(self):
        self.ai_extractor = AIExtractionEngine()
        self.cache = CacheService()

    async def process_and_validate(self, raw_pin: RawPinIngest) -> ValidatedPin:
        start_time = time.time()
        PIN_INGEST_COUNT.inc()

        # 1. Cache Lookup Check
        cached_result = await self.cache.get_cached_pin(raw_pin.pin_id)
        if cached_result:
            CACHE_HITS.inc()
            PROCESSING_LATENCY.observe(time.time() - start_time)
            return ValidatedPin(**cached_result)

        # 2. Execute AI Vision Analysis
        ai_meta = await self.ai_extractor.extract_metadata(
            str(raw_pin.image_url),
            raw_pin.raw_caption
        )

        # 3. Deterministic Guardrails Check
        if ai_meta.confidence_score < 0.70:
            VALIDATION_FAILURES.inc()
            raise ValueError(
                f"AI confidence score ({ai_meta.confidence_score}) below threshold (0.70)"
            )

        is_safe = len(ai_meta.safety_flags) == 0
        sanitized_tags = list(set(tag.strip().lower() for tag in ai_meta.detected_objects))

        # 4. Construct Verified Domain Object
        validated_pin = ValidatedPin(
            pin_id=raw_pin.pin_id,
            image_url=str(raw_pin.image_url),
            category=ai_meta.primary_category,
            tags=sanitized_tags,
            confidence_score=ai_meta.confidence_score,
            is_safe=is_safe,
            processed_at=datetime.now(timezone.utc)
        )

        # 5. Store in Redis Cache
        await self.cache.cache_pin(validated_pin)

        # Record pipeline execution time
        PROCESSING_LATENCY.observe(time.time() - start_time)
        return validated_pin