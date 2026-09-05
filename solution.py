"""Synthetic demo submission: demo-be-casey; not a real account."""
def normalize_listing(record):
    title = record.get("title", "").strip()
    if not title:
        raise ValueError("title is required")
    price = record.get("price_cents")
    if type(price) is not int or price < 0:
        raise ValueError("price must be nonnegative integer cents")
    currency = record.get("currency", "RUB").upper()
    if currency not in {"RUB", "USD", "EUR"}:
        raise ValueError("unsupported currency")
    return {"title": title, "price_cents": price, "currency": currency}
