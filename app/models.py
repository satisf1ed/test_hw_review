from pydantic import BaseModel, Field


class Ad(BaseModel):
    ad_id: int = Field(..., ge=1)
    seller_id: int = Field(..., ge=1)
    is_trusted_seller: bool
    title: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1)
    price: int = Field(..., ge=0)
    photos_count: int = Field(..., ge=0)


class ModerationResult(BaseModel):
    needs_review: bool
    reason: str
