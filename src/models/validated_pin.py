from pydantic import BaseModel, Field, HttpUrl, validator
from typing import List, Optional
from datetime import datetime

class RawPinIngest(BaseModel):
    pin_id: str
    image_url: HttpUrl
    raw_caption: Optional[str] = None

class AIExtractedMetadata(BaseModel):
    detected_objects: List[str]
    primary_category: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    safety_flags: List[str]

class ValidatedPin(BaseModel):
    pin_id: str
    image_url: str
    category: str
    tags: List[str]
    confidence_score: float
    is_safe: bool
    processed_at: datetime