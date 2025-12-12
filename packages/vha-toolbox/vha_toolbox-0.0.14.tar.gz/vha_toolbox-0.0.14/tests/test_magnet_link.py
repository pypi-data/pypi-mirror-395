import unittest

from vha_toolbox import create_magnet_link


class MagnetLinkTestCase(unittest.TestCase):
    def test_magnet_link(self):
        hash = '1234567890abcdef1234567890abcdef12345678'
        trackers = ['http://tracker1.com', 'http://tracker2.com']
        displayed_name = 'My Torrent'
        expected_output = 'magnet:?xt=urn:btih:1234567890abcdef1234567890abcdef12345678&dn=My%20Torrent&tr=http%3A%2F%2Ftracker1.com&tr=http%3A%2F%2Ftracker2.com'
        self.assertEqual(create_magnet_link(hash, displayed_name, trackers), expected_output)

    def test_magnet_link_with_empty_hash(self):
        hash = ''
        trackers = ['http://tracker1.com', 'http://tracker2.com']
        displayed_name = 'My Torrent'
        self.assertRaises(ValueError, create_magnet_link, hash, displayed_name, trackers)

    def test_magnet_link_with_empty_trackers(self):
        hash = '1234567890abcdef1234567890abcdef12345678'
        trackers = []
        displayed_name = 'My Torrent'
        self.assertRaises(ValueError, create_magnet_link, hash, displayed_name, trackers)

    def test_magnet_link_with_empty_displayed_name(self):
        hash = '1234567890abcdef1234567890abcdef12345678'
        trackers = ['http://tracker1.com', 'http://tracker2.com']
        displayed_name = ''
        self.assertRaises(ValueError, create_magnet_link, hash, displayed_name, trackers)

    def test_magnet_link_with_unicode_displayed_name(self):
        hash = '1234567890abcdef1234567890abcdef12345678'
        trackers = ['http://tracker1.com', 'http://tracker2.com']
        displayed_name = 'My Torrent 🤗'
        expected_output = 'magnet:?xt=urn:btih:1234567890abcdef1234567890abcdef12345678&dn=My%20Torrent%20%F0%9F%A4%97&tr=http%3A%2F%2Ftracker1.com&tr=http%3A%2F%2Ftracker2.com'
        self.assertEqual(create_magnet_link(hash, displayed_name, trackers), expected_output)

    def test_magnet_link_with_unicode_displayed_name_and_unicode_trackers(self):
        hash = '1234567890abcdef1234567890abcdef12345678'
        trackers = ['http://tracker1.com/🤗', 'http://tracker2.com/🤗']
        displayed_name = 'My Torrent 🤗'
        expected_output = 'magnet:?xt=urn:btih:1234567890abcdef1234567890abcdef12345678&dn=My%20Torrent%20%F0%9F%A4%97&tr=http%3A%2F%2Ftracker1.com%2F%F0%9F%A4%97&tr=http%3A%2F%2Ftracker2.com%2F%F0%9F%A4%97'
        self.assertEqual(create_magnet_link(hash, displayed_name, trackers), expected_output)


if __name__ == '__main__':
    unittest.main()
