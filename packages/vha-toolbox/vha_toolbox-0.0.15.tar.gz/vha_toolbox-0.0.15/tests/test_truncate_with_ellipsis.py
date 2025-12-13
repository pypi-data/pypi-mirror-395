import unittest

from vha_toolbox import truncate_with_ellipsis


class TruncateWithEllipsisTestCase(unittest.TestCase):
    def test_truncate_with_ellipsis(self):
        self.assertEqual(truncate_with_ellipsis('Hello world!', 5), 'Hello...')
        self.assertEqual(truncate_with_ellipsis('Hello world!', 7), 'Hello w...')
        self.assertEqual(truncate_with_ellipsis('Hello world!', 11), 'Hello world...')
        self.assertEqual(truncate_with_ellipsis('Hello world!', 12), 'Hello world!')

    def test_truncate_with_ellipsis_with_blank(self):
        self.assertEqual(truncate_with_ellipsis('Hello world! ', 6), 'Hello...')
        self.assertEqual(truncate_with_ellipsis('Hello world! ', 13), 'Hello world! ')

    def test_truncate_with_ellipsis_with_blank_disabled(self):
        self.assertEqual(truncate_with_ellipsis('Hello world! ', 6, del_blank=False), 'Hello ...')
        self.assertEqual(truncate_with_ellipsis('Hello world! ', 13, del_blank=False), 'Hello world! ')

    def test_truncate_with_ellipsis_with_ellipsis(self):
        self.assertEqual(truncate_with_ellipsis('Hello world!', 5, ellipsis='...!'), 'Hello...!')
        self.assertEqual(truncate_with_ellipsis('Hello world!', 5, ellipsis=''), 'Hello')
        self.assertEqual(truncate_with_ellipsis('Hello world!', 5, ellipsis='...'), 'Hello...')

    def test_truncate_with_ellipsis_with_ellipsis_and_blank_disabled(self):
        self.assertEqual(truncate_with_ellipsis('Hello world! ', 6, ellipsis='...!', del_blank=False), 'Hello ...!')
        self.assertEqual(truncate_with_ellipsis('Hello world! ', 13, ellipsis='...!', del_blank=False), 'Hello world! ')


if __name__ == '__main__':
    unittest.main()
