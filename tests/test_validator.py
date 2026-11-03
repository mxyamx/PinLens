import pytest
from unittest.mock import AsyncMock, patch
from src.models.raw_pin import RawPinIngest
from src.models.validated_pin import AIExtractedMetadata
from src.services.validator import PinValidationEngine

@pytest.mark.asyncio
async def test_successful_pin_validation():
    engine = PinValidationEngine()
    raw_payload = RawPinIngest(
        pin_id="pin_12345",
        image_url="https://images.unsplash.com/photo-1513694203232-719a280e022f",
        raw_caption="Modern minimalist coffee table layout"
    )

    result = await engine.process_and_validate(raw_payload)
    
    assert result.pin_id == "pin_12345"
    assert result.confidence_score >= 0.70
    assert result.is_safe is True
    assert "living room" in result.tags or "minimalist aesthetic" in result.tags

@pytest.mark.asyncio
async def test_low_confidence_ai_output_rejected():
    engine = PinValidationEngine()
    raw_payload = RawPinIngest(
        pin_id="pin_blurry_99",
        image_url="https://example.com/blurry.jpg"
    )

    # Mock low confidence AI response
    low_conf_response = AIExtractedMetadata(
        detected_objects=["blurry object"],
        primary_category="Unknown",
        confidence_score=0.45,  # Below 0.70 threshold
        safety_flags=[]
    )

    with patch.object(engine.ai_extractor, 'extract_metadata', new_callable=AsyncMock) as mock_extract:
        mock_extract.return_value = low_conf_response
        with pytest.raises(ValueError, match="AI confidence score"):
            await engine.process_and_validate(raw_payload)