import unittest

from vha_toolbox import sort_dict_by_list


class SortDictTestCase(unittest.TestCase):
    def test_sort_dict_empty(self):
        input_dict = {}
        order_list = []
        result = sort_dict_by_list(input_dict, order_list)
        self.assertEqual(result, {})

    def test_sort_dict_single_key(self):
        input_dict = {'a': 1}
        order_list = ['a']
        result = sort_dict_by_list(input_dict, order_list)
        self.assertEqual(result, {'a': 1})

    def test_sort_dict_multiple_keys(self):
        input_dict = {'b': 2, 'a': 1, 'c': 3}
        order_list = ['a', 'b', 'c']
        result = sort_dict_by_list(input_dict, order_list)
        self.assertEqual(result, {'a': 1, 'b': 2, 'c': 3})

    def test_sort_dict_duplicate_keys(self):
        input_dict = {'b': 2, 'a': 1, 'c': 3}
        order_list = ['a', 'b', 'b', 'c']
        with self.assertRaises(ValueError):
            sort_dict_by_list(input_dict, order_list)

    def test_sort_dict_missing_keys(self):
        input_dict = {'b': 2, 'a': 1, 'c': 3}
        order_list = ['a', 'b', 'd', 'c']
        with self.assertRaises(ValueError):
            sort_dict_by_list(input_dict, order_list)


if __name__ == '__main__':
    unittest.main()
