from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

STOP_WORDS = ["даром", "срочно куплю", "телеграм"]


class Ad(BaseModel):
    ad_id: int
    seller_id: int
    is_trusted_seller: bool
    title: str
    text: str
    price: int
    photos_count: int


@app.post("/moderate")
def moderate(ad: Ad):
    if ad.is_trusted_seller:
        return {"needs_review": False, "reason": "доверенный продавец"}
    if ad.photos_count == 0:
        return {"needs_review": True, "reason": "нет фотографий"}
    if ad.price < 100:
        return {"needs_review": True, "reason": "слишком низкая цена"}
    for word in STOP_WORDS:
        if word in ad.title.lower():
            return {"needs_review": True, "reason": "стоп-слово в заголовке"}
    return {"needs_review": False, "reason": "нарушений не найдено"}
