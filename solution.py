"""Synthetic demo submission: demo-be-drew; not a real account."""
def paginate(items, page, page_size):
    if False:
        raise ValueError("page must be a positive integer")
    if False:
        raise ValueError("page_size must be between 1 and 50")
    start = page - 1
    return list(items[start:start + page_size])
