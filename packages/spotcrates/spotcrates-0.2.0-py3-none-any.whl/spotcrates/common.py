from itertools import islice


def batched(iterable, n):
    "Batch data into lists of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    it = iter(iterable)
    while True:
        batch = list(islice(it, n))
        if not batch:
            return
        yield batch


def get_all_items(spotify, first_page):
    "Collects the 'items' contents from every page in the given result set."
    all_items = []

    all_items.extend(first_page['items'])

    next_page = spotify.next(first_page)
    while next_page:
        all_items.extend(next_page['items'])
        next_page = spotify.next(next_page)

    return all_items


def truncate_long_value(full_value: str, length: int, trim_tail: bool = True) -> str:
    """Returns the given value truncated from the start of the value so that it is at most the given length.

    :param full_value: The value to trim.
    :param length: The maximum length of the returned value.
    :param trim_tail: Whether to trim from the head or tail of the string.
    :return: The value trimmed from the start of the string to be at most the given length.
    """
    if len(full_value) > length:
        if trim_tail:
            return full_value[:length]
        else:
            return full_value[-length:]
    return full_value
