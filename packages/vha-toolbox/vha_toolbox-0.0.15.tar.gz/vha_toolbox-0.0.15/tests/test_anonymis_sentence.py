import unittest

from vha_toolbox import anonymize_sentence


class AnonymizeSentenceTestCase(unittest.TestCase):

    def test_anonymize_sentence(self):
        sentence = 'Hello World'
        expected_anonymized_sentence = '***** *****'
        anonymized_sentence = anonymize_sentence(sentence)
        self.assertEqual(anonymized_sentence, expected_anonymized_sentence)

    def test_anonymize_sentence_with_special_character(self):
        sentence = 'Alice is 28 years old.'
        expected_anonymized_sentence = '***** ** ** ***** ***.'
        anonymized_sentence = anonymize_sentence(sentence)
        self.assertEqual(anonymized_sentence, expected_anonymized_sentence)

    def test_anonymize_sentence_with_special_character_2(self):
        sentence = 'This is a sample sentence with some 123 numbers and special characters!'
        expected_anonymized_sentence = '**** ** * ****** ******** **** **** *** ******* *** ******* **********!'
        anonymized_sentence = anonymize_sentence(sentence)
        self.assertEqual(anonymized_sentence, expected_anonymized_sentence)

    def test_anonymize_sentence_with_anonymize_character(self):
        sentence = 'Alice is 28 years old.'
        expected_anonymized_sentence = 'AAAAA AA AA AAAAA AAA.'
        anonymized_sentence = anonymize_sentence(sentence, anonymized_char='A')
        self.assertEqual(anonymized_sentence, expected_anonymized_sentence)

    # def test_anonymize_sentence_keep_partial_word(self):
    #     sentence = 'Alice is 28 years old.'
    #     expected_anonymized_sentence = 'A***e i* 2* y***s o**.'
    #     anonymized_sentence = anonymize_sentence(sentence, keep_partial_word=True)
    #     self.assertEqual(anonymized_sentence, expected_anonymized_sentence)
    #
    # def test_anonymize_sentence_keep_partial_word_2(self):
    #     sentence = 'Alice is 28 years old.'
    #     expected_anonymized_sentence = 'A**** i* 2* y**** o**.'
    #     anonymized_sentence = anonymize_sentence(sentence, keep_partial_word=True, erase_ratio=1)
    #     self.assertEqual(anonymized_sentence, expected_anonymized_sentence)


if __name__ == '__main__':
    unittest.main()
