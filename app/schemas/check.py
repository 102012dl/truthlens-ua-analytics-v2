from typing import Optional, Literal
from pydantic import BaseModel, field_validator


class CheckRequest(BaseModel):
    url: Optional[str] = None
    text: Optional[str] = None
    language: str = "uk"

    @field_validator('url', 'text')
    @classmethod
    def validate_url_or_text(cls, v, info):
        if info.field_name == 'url' and v is not None:
            return v
        if info.field_name == 'text' and v is not None:
            return v
        return v

    @field_validator('url', 'text')
    @classmethod
    def at_least_one_required(cls, v, values, **kwargs):
        url = values.data.get('url') if 'url' in values.data else None
        text = values.data.get('text') if 'text' in values.data else None
        
        if not url and not text and v is None:
            raise ValueError("Provide either 'url' or 'text'")
        return v


class CheckResponse(BaseModel):
    article_id: int
    verdict: Literal["REAL", "FAKE", "SUSPICIOUS"]
    credibility_score: float  # 0-100
    fake_score: float         # 0.0-1.0
    confidence: float         # 0.0-1.0
    ipso_techniques: list[str]
    source_credibility: float  # 0-100
    explanation_uk: str
    source_domain: str
    language: str
    processing_time_ms: float