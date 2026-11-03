from pydantic import BaseModel, HttpUrl
from typing import Optional

class RawPinIngest(BaseModel):
    pin_id: str
    image_url: HttpUrl
    raw_caption: Optional[str] = None