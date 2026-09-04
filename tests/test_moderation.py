import pytest
from fastapi.testclient import TestClient

from app.services.moderation import decide
from main import app

client = TestClient(app)

BASE = {
    "ad_id": 1,
    "seller_id": 2,
    "is_trusted_seller": False,
    "title": "Стул деревянный",
    "text": "Хороший стул, почти новый",
    "price": 2000,
    "photos_count": 3,
}


def test_trusted_seller_skips_review():
    body = {**BASE, "is_trusted_seller": True, "photos_count": 0}
    r = client.post("/moderate", json=body)
    assert r.status_code == 200
    assert r.json()["needs_review"] is False


def test_clean_ad_passes():
    r = client.post("/moderate", json=BASE)
    assert r.status_code == 200
    assert r.json() == {"needs_review": False, "reason": "нарушений не найдено"}


@pytest.mark.parametrize(
    ("field", "value", "reason_part"),
    [
        ("photos_count", 0, "фотографий"),
        ("price", 50, "диапазона"),
        ("price", 20_000_000, "диапазона"),
        ("title", "Отдам даром", "даром"),
        ("text", "пишите в телеграм", "телеграм"),
    ],
)
def test_rules_trigger_review(field, value, reason_part):
    r = client.post("/moderate", json={**BASE, field: value})
    assert r.status_code == 200
    assert r.json()["needs_review"] is True
    assert reason_part in r.json()["reason"]


@pytest.mark.parametrize(
    "broken",
    [
        {"title": ""},
        {"price": -1},
        {"photos_count": -5},
    ],
)
def test_validation_rejects_bad_payload(broken):
    r = client.post("/moderate", json={**BASE, **broken})
    assert r.status_code in (400, 422)


def test_missing_field_is_rejected():
    body = {k: v for k, v in BASE.items() if k != "price"}
    assert client.post("/moderate", json=body).status_code in (400, 422)


def test_wrong_method_is_rejected():
    assert client.get("/moderate").status_code == 405


def test_boundary_prices_are_allowed():
    for price in (100, 10_000_000):
        assert decide(
            is_trusted_seller=False, title="Стул", text="описание",
            price=price, photos_count=1,
        ).needs_review is False
