import unittest

from vha_toolbox import seconds_to_humantime


class TestSecondsToHumanTime(unittest.TestCase):
    def test_seconds_to_humantime_1(self):
        self.assertEqual(seconds_to_humantime(3660), '1 hour and 1 minute')

    def test_seconds_to_humantime_2(self):
        self.assertEqual(seconds_to_humantime(3660, include_seconds=False), '1 hour and 1 minute')

    def test_seconds_to_humantime_3(self):
        self.assertEqual(seconds_to_humantime(60), '1 minute')

    def test_seconds_to_humantime_4(self):
        self.assertEqual(seconds_to_humantime(120), '2 minutes')

    def test_seconds_to_humantime_5(self):
        self.assertEqual(seconds_to_humantime(0), '0 seconds')

    def test_seconds_to_humantime_6(self):
        self.assertEqual(seconds_to_humantime(31536000 + 2592000 + 86400 + 3600 + 60 + 1), '1 year, 1 month, 1 day, 1 hour, 1 minute and 1 second')

    def test_seconds_to_humantime_7(self):
        self.assertEqual(seconds_to_humantime(61, include_seconds=False), '1 minute')

    def test_seconds_to_humantime_8(self):
        self.assertEqual(seconds_to_humantime(6646.15384615), '1 hour, 50 minutes and 46 seconds')


if __name__ == '__main__':
    unittest.main()
