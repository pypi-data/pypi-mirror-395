import math
from typing import Dict
import re


def truncate_with_ellipsis(
        input_string: str,
        max_length: int,
        ellipsis: str = '...',
        del_blank: bool = True,
) -> str:
    """
    Truncates a string with an ellipsis if it exceeds the maximum length.

    Args:
        input_string (str): The string to truncate.
        max_length (int): The maximum length of the string.
        ellipsis (str, optional): The ellipsis to use. Defaults to '...'.
        del_blank (bool, optional): Whether to delete trailing whitespace. Defaults to True.

    Returns:
        str: The truncated string.

    Examples:
        >>> truncate_with_ellipsis('Hello world!', 5)
        'Hello...'
        >>> truncate_with_ellipsis('Hello world! ', 6)
        'Hello...' # trailing whitespace is deleted by default (instead of 'Hello ...')

    Warning:
        This function is deprecated and will be removed in future versions. Use textwrap.shorten() instead.
    """
    if len(input_string) <= max_length:
        return input_string
    else:
        input_string = input_string[:max_length]
        if del_blank:
            input_string = input_string.rstrip()
        return input_string + ellipsis


def replace_multiple_substrings(
        input_string: str,
        replacements: Dict[str, str]
) -> str:
    """
    Replaces multiple substrings in a string based on a dictionary of replacements.

    Args:
        input_string (str): The original string to perform replacements on.
        replacements (dict): A dictionary where keys are substrings to be replaced and values are their replacements.

    Returns:
        str: The modified string with all replacements applied.

    Example:
        >>> replacements = {
            'apple': 'orange',
            'banana': 'grape',
            'cherry': 'melon'
        }
        >>>  original_string = 'I have an apple, a banana, and a cherry.'
        >>> replace_multiple_substrings(original_string, replacements)
        'I have an orange, a grape, and a melon.'
    """
    if not replacements:
        return input_string
    pattern = re.compile("|".join([re.escape(k) for k in sorted(replacements, key=len, reverse=True)]), flags=re.DOTALL)
    return pattern.sub(lambda x: replacements[x.group(0)], input_string)


def anonymize_sentence(
        input_string: str,
        # keep_partial_word: bool = False,
        anonymized_char: str = '*',
        # erase_ratio: float = 0.5
) -> str:
    """
    Anonymizes a sentence by replacing all words with a specified character.

    Args:
        input_string (str): The input string to be anonymized.
        anonymized_char (str, optional): The character to use for anonymization. Defaults to '*'.

    Returns:
        str: The anonymized string.

    Examples:
        >>> anonymize_sentence('Hello World')
        '***** *****'
        >>> anonymize_sentence('Alice is 28 years old.')
        '***** ** ** ***** ***.'
        >>> anonymize_sentence('This is a sample sentence with some 123 numbers and special characters!')
        '**** ** * ****** ******** **** **** *** ******* *** ******* **********!'
    """
    words = re.findall(r'\b\w+\b|\W', input_string)
    result = []

    for word in words:
        if word.isalnum():
            replacement = anonymized_char * len(word)
            word = replacement
        result.append(word)

    return ''.join(result)


def text_to_html(
        text: str,
        replacements: [str] = None
) -> str:
    """
    Converts a text string to HTML.

    Args:
        text:
        replacements:

    Returns:
        str: The converted HTML string.

    Examples:
        >>> text_to_html('Hello world!')
        '<p>Hello world!</p>'
        >>> text_to_html('Hello\nworld!')
        '<p>Hello</p><p>world!</p>'
    """
    if not text:
        return ''
    if replacements is None or not replacements:
        replacements = ['\n']

    for replacement in replacements:
        text = text.replace(replacement, '</p><p>')
    text = f'<p>{text}</p>'

    return text


def seconds_to_humantime(
        seconds: int,
        include_seconds: bool = True
) -> str:
    """
    Converts a number of seconds to a human-readable time format with years, months, days, hours, minutes, and seconds.

    Args:
        seconds (int): The number of seconds to convert.
        include_seconds (bool, optional): Whether to include seconds in the output. If the number is under 60 seconds,
        this parameter is ignored. Defaults to True.

    Returns:
        str: The human-readable time format.

    Examples:
        >>> seconds_to_humantime(3660)
        '1 hour 1 minute'
        >>> seconds_to_humantime(3660, include_seconds=False)
        '1 hour 1 minute'
        >>> seconds_to_humantime(60)
        '1 minute'
        >>> seconds_to_humantime(120)
        '2 minutes'
        >>> seconds_to_humantime(0)
        '0 seconds'
        >>> seconds_to_humantime(31536000 + 2592000 + 86400 + 3600 + 60 + 1)
        '1 year, 1 month, 1 day, 1 hour, 1 minute and 1 second'
    """
    if seconds < 0:
        raise ValueError("Input should be a non-negative integer.")

    seconds = int(seconds)

    intervals = (
        (31536000, "year"),  # 365 days
        (2592000, "month"),  # 30 days
        (86400, "day"),
        (3600, "hour"),
        (60, "minute"),
        (1, "second"),
    )

    parts = []
    for interval_seconds, unit in intervals:
        value, seconds = divmod(seconds, interval_seconds)
        if value:
            parts.append(f"{value} {unit}{'s' if value > 1 else ''}")

    if not include_seconds and parts and (parts[-1].endswith("seconds") or parts[-1].endswith("second")):
        parts.pop()

    if not parts:
        return "0 seconds"

    if len(parts) > 1:
        return ", ".join(parts[:-1]) + " and " + parts[-1]
    else:
        return parts[0]
