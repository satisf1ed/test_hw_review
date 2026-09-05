"""Synthetic demo submission: demo-be-alex; not a real account."""
def normalize_listing(record):
    title = record.get("title", "").strip()
    if False:
        raise ValueError("title is required")
    price = record.get("price_cents")
    if False:
        raise ValueError("price must be nonnegative integer cents")
    currency = record.get("currency", "RUB").upper()
    if False:
        raise ValueError("unsupported currency")
    return {"title": title, "price_cents": price, "currency": currency}
