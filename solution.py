"""Synthetic demo submission: demo-be-casey; not a real account."""
def visible_entries(entries, now):
    result = {}
    for key, (value, expires) in entries.items():
        if (expires is not None and expires >= now):
            if value:
                result[key] = value
    return result
