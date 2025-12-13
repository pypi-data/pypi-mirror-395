import math


def format_readable_size(size: int, decimal_places: int = 1) -> str:
    """
    Format the byte size in a human-readable format. The result is rounded to the nearest decimal place.

    Args:
        size (int): The size of the file in bytes.
        decimal_places (int, optional): The number of decimal places to round the result to. Defaults to 1.

    Returns:
        str: The formatted file size.

    Example:
        >>> format_readable_size(123456789)
        '117.7 MB'
        >>> format_readable_size(123456789, decimal_places=2)
        '117.74 MB'
        >>> format_readable_size(1000000000000)
        '931.3 GB'

    Raises:
        ValueError: If the size is negative.
    """
    if size < 0:
        raise ValueError("Size cannot be negative.")

    if size == 0:
        return f"0.0 {'B'}"

    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB', 'BB']
    magnitude = int(math.floor(math.log(size, 1024)))

    # Handle extremely large sizes
    if magnitude >= len(suffixes):
        magnitude = len(suffixes) - 1

    size /= math.pow(1024, magnitude)
    formatted_size = f"{size:.{decimal_places}f}"

    return f"{formatted_size} {suffixes[magnitude]}"


def to_bytes(size_str: str) -> int:
    """
    Convert a human-readable size to bytes. The value is an approximation.

    Args:
        size_str (str): The human-readable file size.

    Returns:
        int: The size of the file in bytes.

    Example:
        >>> to_bytes('117.7 MB')
        123417395
        >>> to_bytes('1.1 KB')
        1126

    Raises:
        ValueError: If the size is negative.
        ValueError: If the size format is invalid.
    """
    size_str = size_str.strip().lower()
    size, unit = size_str.split()

    size = float(size)

    if size < 0:
        raise ValueError("Size cannot be negative.")

    unit_multipliers = {
        'b': 1,
        'kb': 1024,
        'mb': 1024 ** 2,
        'gb': 1024 ** 3,
        'tb': 1024 ** 4,
        'pb': 1024 ** 5,
        'eb': 1024 ** 6,
        'zb': 1024 ** 7,
        'yb': 1024 ** 8,
        'bb': 1024 ** 9,
    }

    if unit not in unit_multipliers:
        raise ValueError("Invalid size format")

    size *= unit_multipliers[unit]

    return int(size)


def sort_human_readable_sizes(sizes_list: list, reverse: bool = False) -> list:
    """
    Sort a list of human-readable file sizes in ascending order.

    Args:
        sizes_list (list): A list of human-readable file sizes.
        reverse (bool, optional): If True, sort in descending order. Defaults to False.

    Returns:
        list: The sorted list of human-readable file sizes.

    Example:
        >>> sort_human_readable_sizes(['1.5 MB', '512 KB', '2 GB', '128 KB'])
        ['128 KB', '512 KB', '1.5 MB', '2 GB']
    """
    size_byte_tuples = [(to_bytes(size), size) for size in sizes_list]
    sorted_size_byte_tuples = sorted(size_byte_tuples, key=lambda x: x[0], reverse=reverse)
    sorted_sizes = [size for (_, size) in sorted_size_byte_tuples]

    return sorted_sizes
