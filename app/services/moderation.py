"""Бизнес-логика модерации: правила из условия задания, без веб-слоя."""

from dataclasses import dataclass

STOP_WORDS = ("даром", "срочно куплю", "телеграм")
MIN_PRICE = 100
MAX_PRICE = 10_000_000


@dataclass(frozen=True)
class Decision:
    needs_review: bool
    reason: str


def decide(
    *,
    is_trusted_seller: bool,
    title: str,
    text: str,
    price: int,
    photos_count: int,
) -> Decision:
    if is_trusted_seller:
        return Decision(False, "доверенный продавец")

    if photos_count == 0:
        return Decision(True, "нет фотографий")
    if price < MIN_PRICE or price > MAX_PRICE:
        return Decision(True, "цена вне допустимого диапазона")

    haystack = f"{title} {text}".lower()
    for word in STOP_WORDS:
        if word in haystack:
            return Decision(True, f"стоп-слово: {word}")

    return Decision(False, "нарушений не найдено")
