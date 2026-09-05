"""Synthetic demo submission: demo-be-erin; not a real account."""
def balance(events):
    seen = {}
    total = 0
    for event in events:
        key, amount = event["id"], event["amount"]
        if not isinstance(key, str) or not key:
            raise ValueError("id must be a nonempty string")
        if type(amount) is not int:
            raise ValueError("amount must be integer cents")
        if key in seen:
            if seen[key] != amount:
                raise ValueError("conflicting duplicate")
            continue
        seen[key] = amount
        total += amount
    return total
