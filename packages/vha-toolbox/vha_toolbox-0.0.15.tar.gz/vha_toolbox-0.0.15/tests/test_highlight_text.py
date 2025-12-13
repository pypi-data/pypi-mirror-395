import unittest

from vha_toolbox import highlight_text


class HighlightTextTestCase(unittest.TestCase):
    def test_highlight_text(self):
        text = "This is a sample text to test the highlighting function."
        words = ["sample", "function"]
        expected_output = "This is a <span>sample</span> text to test the highlighting <span>function</span>."
        result = highlight_text(text, words)
        self.assertEqual(result, expected_output)

    def test_highlight_text_custom_tags(self):
        text = "This is a sample text to test the highlighting function."
        words = ["sample", "function"]
        expected_output = "This is a [sample] text to test the highlighting [function]."

        result = highlight_text(text, words, start_tag='[', end_tag=']')
        self.assertEqual(result, expected_output)

    def test_highlight_text_custom_tags_contained_in_text(self):
        text = "This is a sample text to test the highlighting [function]."
        words = ["sample", "function"]
        expected_output = "This is a [sample] text to test the highlighting [[function]]."

        result = highlight_text(text, words, start_tag='[', end_tag=']')
        self.assertEqual(result, expected_output)

    def test_highlight_text_custom_tags_contained_in_text_2(self):
        text = "This is a sample text to test the highlighting [function]."
        words = ["sample", "function"]
        expected_output = "This is a [[sample]] text to test the highlighting [[[function]]]."

        result = highlight_text(text, words, start_tag='[[', end_tag=']]')
        self.assertEqual(result, expected_output)

    def test_highlight_text_case_insensitive(self):
        text = "This is a case-insensitive Test."
        words = ["TEST"]
        expected_output = "This is a case-insensitive <span>Test</span>."
        result = highlight_text(text, words, case_insensitive=True)
        self.assertEqual(result, expected_output)

    def test_highlight_text_with_substring_overlapping(self):
        text = "This is a sample text."
        words = ["sam", "ample"]
        expected_output = "This is a <span>sample</span> text."
        result = highlight_text(text, words)
        self.assertEqual(result, expected_output)

    def test_highlight_text_with_overlapping(self):
        text = "This is a test with overlapping words."
        words = ["with overlapping", "overlapping words"]
        expected_output = "This is a test <span>with overlapping words</span>."
        result = highlight_text(text, words)
        self.assertEqual(result, expected_output)

    def test_highlight_text_with_boundaries(self):
        text = "words and word"
        words = ["word"]
        expected_output = "words and <span>word</span>"
        result = highlight_text(text, words, word_boundaries=True)
        self.assertEqual(result, expected_output)

    def test_highlight_text_with_multiple_overlapping(self):
        text = "This is a test with overlapping words."
        words = ["test with", "with overlapping", "overlapping words"]
        expected_output = "This is a <span>test with overlapping words</span>."
        result = highlight_text(text, words)
        self.assertEqual(result, expected_output)

    def test_highlight_text_no_words_to_highlight(self):
        text = "This is a test with no words to highlight."
        words = []
        expected_output = "This is a test with no words to highlight."
        result = highlight_text(text, words)
        self.assertEqual(result, expected_output)

    def test_highlight_text_empty_text(self):
        text = ""
        words = ["highlight", "function"]
        expected_output = ""
        result = highlight_text(text, words)
        self.assertEqual(result, expected_output)

    def test_highlight_text_multiple_occurrences(self):
        text = "This is a test with multiple occurrences of the word 'test'."
        words = ["test"]
        expected_output = "This is a <span>test</span> with multiple occurrences of the word '<span>test</span>'."
        result = highlight_text(text, words)
        self.assertEqual(result, expected_output)

    def test_highlight_words_in_long_text_multiple_occurrences(self):
        text = "This is a long text to test the highlighting function. This text is long and repetitive. This is a long text to test the highlighting function. This text is long and repetitive."
        words = ["long", "text", "repetitive", "highlighting", "function"]
        expected_output = "This is a <span>long</span> <span>text</span> to test the <span>highlighting</span> <span>function</span>. This <span>text</span> is <span>long</span> and <span>repetitive</span>. This is a <span>long</span> <span>text</span> to test the <span>highlighting</span> <span>function</span>. This <span>text</span> is <span>long</span> and <span>repetitive</span>."
        result = highlight_text(text, words)
        self.assertEqual(result, expected_output)

    def test_highlight_text_no_accents_insensitive(self):
        text = "Café nötë Hello wörld!"
        words = ["cafe", "note", "world"]
        expected_output = "Café nötë Hello wörld!"

        result = highlight_text(text, words)
        self.assertEqual(result, expected_output)

    def test_highlight_text_accents_insensitive(self):
        text = "Café nötë Hello wörld!"
        words = ["cafe", "note", "world"]
        expected_output = "Café <span>nötë</span> Hello <span>wörld</span>!"

        result = highlight_text(text, words, accents_insensitive=True)
        self.assertEqual(result, expected_output)

    def test_highlight_text_case_and_accents_insensitive(self):
        text = "Café nötë Hello wörld!"
        words = ["cafe", "note", "world"]
        expected_output = "<span>Café</span> <span>nötë</span> Hello <span>wörld</span>!"

        result = highlight_text(text, words, case_insensitive=True, accents_insensitive=True)
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
