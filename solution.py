"""Synthetic demo submission: demo-be-drew; not a real account."""
def visible_entries(entries, now):
    result = {}
    for key, (value, expires) in entries.items():
        if (expires is None or expires > now):
            result[key] = value
    return result
