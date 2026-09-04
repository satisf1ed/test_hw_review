from fastapi import APIRouter

from app.models import Ad, ModerationResult
from app.services.moderation import decide

router = APIRouter()


@router.post("/moderate", response_model=ModerationResult)
def moderate(ad: Ad) -> ModerationResult:
    decision = decide(
        is_trusted_seller=ad.is_trusted_seller,
        title=ad.title,
        text=ad.text,
        price=ad.price,
        photos_count=ad.photos_count,
    )
    return ModerationResult(needs_review=decision.needs_review, reason=decision.reason)
