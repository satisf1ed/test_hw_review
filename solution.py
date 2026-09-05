"""Synthetic demo submission: demo-be-erin; not a real account."""
def paginate(items, page, page_size):
    if type(page) is not int or page < 1:
        raise ValueError("page must be a positive integer")
    if type(page_size) is not int or not 1 <= page_size <= 50:
        raise ValueError("page_size must be between 1 and 50")
    start = page - 1
    return list(items[start:start + page_size])
