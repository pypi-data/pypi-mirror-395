from __future__ import annotations


def split_timestamps(my_array, n_part: int):
    """
    split given array into n_part (as equal as possible)
    :param sequence my_array:
    """
    array_size = len(my_array)
    if array_size < n_part:
        yield my_array
    else:
        start = 0
        for _ in range(n_part):
            end = max(start + int(array_size / n_part) + 1, array_size)
            yield my_array[start:end]
            start = end
