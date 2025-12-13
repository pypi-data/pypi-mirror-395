import unittest

from vha_toolbox import text_to_html


class TextToHtmlTestCase(unittest.TestCase):
    def test_text_to_html_1(self):
        text = 'Hello world!'
        result = text_to_html(text)
        self.assertEqual(result, '<p>Hello world!</p>')

    def test_text_to_html_2(self):
        text = 'Hello\nworld!'
        result = text_to_html(text)
        self.assertEqual(result, '<p>Hello</p><p>world!</p>')

    def test_text_to_html_3(self):
        text = 'Hello\nworld!'
        replacements = ['\n']
        result = text_to_html(text, replacements)
        self.assertEqual(result, '<p>Hello</p><p>world!</p>')

    def test_text_to_html_4(self):
        text = 'Hello\nworld!'
        replacements = []
        result = text_to_html(text, replacements)
        self.assertEqual(result, '<p>Hello</p><p>world!</p>')

    def test_text_to_html_5(self):
        text = 'Hello\nworld!'
        replacements = ['\n', 'world']
        result = text_to_html(text, replacements)
        self.assertEqual(result, '<p>Hello</p><p></p><p>!</p>')


if __name__ == '__main__':
    unittest.main()
