import os
import json
import asyncio
from openai import AsyncOpenAI
from src.models.validated_pin import AIExtractedMetadata

class AIExtractionEngine:
    """
    Executes multimodal vision AI inference on Pin images and returns 
    structured metadata (categories, tags, safety flags, and confidence).
    """
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY", "mock-key-for-dev")
        self.is_mock = api_key == "mock-key-for-dev" or not api_key
        if not self.is_mock:
            self.client = AsyncOpenAI(api_key=api_key)

    async def extract_metadata(self, image_url: str, caption: str | None = None) -> AIExtractedMetadata:
        if self.is_mock:
            await asyncio.sleep(0.05)
            # Standard mock response for local testing
            return AIExtractedMetadata(
                detected_objects=["minimalist aesthetic", "living room", "oak table"],
                primary_category="Home & Architecture",
                confidence_score=0.94,
                safety_flags=[]
            )

        # Real OpenAI GPT-4o Vision structured extraction
        prompt = (
            "Analyze this image and optional caption for a Pinterest-style discovery platform. "
            f"Caption: {caption if caption else 'None'}. "
            "Return JSON with keys: 'detected_objects' (list of str), 'primary_category' (str), "
            "'confidence_score' (float between 0 and 1), and 'safety_flags' (list of str)."
        )

        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }
            ],
            response_format={"type": "json_object"},
            max_tokens=300,
        )

        content = json.loads(response.choices[0].message.content)
        return AIExtractedMetadata(**content)