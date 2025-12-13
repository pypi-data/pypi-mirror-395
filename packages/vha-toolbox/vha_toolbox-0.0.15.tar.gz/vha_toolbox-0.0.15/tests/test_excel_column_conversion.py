import unittest

from vha_toolbox import get_position, get_letter


class ExcelColumnConversionTestCase(unittest.TestCase):
    def test_get_position(self):
        self.assertEqual(get_position('A'), 1)
        self.assertEqual(get_position('B'), 2)
        self.assertEqual(get_position('Z'), 26)
        self.assertEqual(get_position('AA'), 27)
        self.assertEqual(get_position('AB'), 28)
        self.assertEqual(get_position('BA'), 53)
        self.assertEqual(get_position('ZZ'), 702)
        self.assertEqual(get_position('AAA'), 703)
        self.assertEqual(get_position('ABC'), 731)

    def test_get_position_error(self):
        self.assertRaises(ValueError, get_position, '')
        self.assertRaises(ValueError, get_position, '1')
        self.assertRaises(ValueError, get_position, 'AA0')
        self.assertRaises(ValueError, get_position, None)

    def test_get_letter(self):
        self.assertEqual(get_letter(1), 'A')
        self.assertEqual(get_letter(2), 'B')
        self.assertEqual(get_letter(26), 'Z')
        self.assertEqual(get_letter(27), 'AA')
        self.assertEqual(get_letter(28), 'AB')
        self.assertEqual(get_letter(53), 'BA')
        self.assertEqual(get_letter(702), 'ZZ')
        self.assertEqual(get_letter(703), 'AAA')
        self.assertEqual(get_letter(731), 'ABC')

    def test_get_letter_error(self):
        self.assertRaises(ValueError, get_letter, 0)
        self.assertRaises(ValueError, get_letter, -1)
        self.assertRaises(ValueError, get_letter, 1.5)
        self.assertRaises(ValueError, get_letter, 'A')
        self.assertRaises(ValueError, get_letter, '')
        self.assertRaises(ValueError, get_letter, None)


if __name__ == '__main__':
    unittest.main()
