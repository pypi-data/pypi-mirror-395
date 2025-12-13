import unittest

from vha_toolbox import replace_multiple_substrings


class ReplaceMultipleSubstringsTestCase(unittest.TestCase):
    def test_replace_multiple_substrings(self):
        replacements = {
            'apple': 'orange',
            'banana': 'grape',
            'cherry': 'melon'
        }
        original_string = 'I have an apple, a banana, and a cherry.'
        expected_result = 'I have an orange, a grape, and a melon.'

        result = replace_multiple_substrings(original_string, replacements)
        self.assertEqual(result, expected_result)

    def test_replace_multiple_occurrences(self):
        replacements = {
            'apple': 'orange',
            'banana': 'grape',
            'cherry': 'melon'
        }
        original_string = 'I have an apple, a banana, and a cherry. An apple is sweet, but a cherry is sour.'
        expected_result = 'I have an orange, a grape, and a melon. An orange is sweet, but a melon is sour.'
        result = replace_multiple_substrings(original_string, replacements)
        self.assertEqual(result, expected_result)

    def test_replace_empty_string(self):
        replacements = {
            'apple': 'orange',
            'banana': 'grape',
            'cherry': 'melon'
        }
        original_string = ''
        expected_result = ''
        result = replace_multiple_substrings(original_string, replacements)
        self.assertEqual(result, expected_result)

    def test_replace_empty_replacements_dict(self):
        replacements = {}
        original_string = 'I have an apple, a banana, and a cherry.'
        expected_result = 'I have an apple, a banana, and a cherry.'
        result = replace_multiple_substrings(original_string, replacements)
        self.assertEqual(result, expected_result)

    def test_replace_overlapping_substrings(self):
        replacements = {
            'apple': 'orange',
            'orange': 'grapefruit'
        }
        original_string = 'I have an apple and an orange.'
        expected_result = 'I have an orange and an grapefruit.'
        result = replace_multiple_substrings(original_string, replacements)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
