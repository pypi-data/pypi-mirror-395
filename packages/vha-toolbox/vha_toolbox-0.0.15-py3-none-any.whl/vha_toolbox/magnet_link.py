import re
from typing import List
from urllib.parse import quote


def create_magnet_link(
        info_hash: str,
        display_name: str,
        trackers: List[str],
) -> str:
    """
    Creates a magnet link from the provided info hash, display name, and trackers.

    Args:
        info_hash (str): The info hash of the torrent.
        display_name (str): The display name of the torrent.
        trackers (list): A list of trackers for the torrent.

    Returns:
        str: The magnet link.

    Example:
        >>> create_magnet_link('1234567890abcdef1234567890abcdef12345678', 'My Torrent', ['udp://tracker.example.com'])
        'magnet:?xt=urn:btih:1234567890abcdef1234567890abcdef12345678&dn=My+Torrent&tr=udp%3A%2F%2Ftracker.example.com'

    Raises:
        ValueError: If the info hash, display name, or list of trackers is empty.
    """
    if not info_hash:
        raise ValueError('The info hash cannot be empty.')
    if not display_name:
        raise ValueError('The display name cannot be empty.')
    if not trackers:
        raise ValueError('The list of trackers cannot be empty.')

    encoded_display_name = quote(display_name, safe='')
    magnet_link = f'magnet:?xt=urn:btih:{info_hash}&dn={encoded_display_name}'

    for tracker in trackers:
        encoded_tracker = quote(tracker, safe='')
        magnet_link += f'&tr={encoded_tracker}'

    return magnet_link
