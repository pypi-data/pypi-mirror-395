
def get_position(s: str) -> int:
    """
    Converts an Excel-style column label to a column number.

    Args:
        s (str): The Excel-style column label.

    Returns:
        int: The corresponding column number.

    Examples:
        >>> get_position('A')
        1
        >>> get_position('B')
        2
        >>> get_position('Z')
        26
        >>> get_position('AA')
        27
        >>> get_position('AB')
        28

    Raises:
        ValueError: If the input should be a non-empty string containing only letters.
    """
    if not s or not s.isalpha():
        raise ValueError("Input should be a non-empty string containing only letters.")

    pos = 0
    for letter in s:
        pos = pos * 26 + (ord(letter.lower()) - 96)
    return pos


def get_letter(i: int) -> str:
    """
    Converts a 1-relative column number to an Excel-style column label.

    Args:
        i (int): The 1-relative column number.

    Returns:
        str: The corresponding Excel-style column label.

    Examples:
        >>> get_letter(1)
        'A'
        >>> get_letter(2)
        'B'
        >>> get_letter(27)
        'AA'
        >>> get_letter(28)
        'AB'

    Raises:
        ValueError: If the input should be a positive integer.
    """
    if not isinstance(i, int) or i <= 0:
        raise ValueError("Input should be a positive integer.")

    letters = []
    while i > 0:
        i -= 1
        quot, rem = divmod(i, 26)
        letters.append(chr(rem + ord('A')))
        i = quot

    return ''.join(reversed(letters))
