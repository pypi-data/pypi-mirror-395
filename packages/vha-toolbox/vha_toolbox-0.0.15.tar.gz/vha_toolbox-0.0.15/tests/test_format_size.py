import unittest

from vha_toolbox import format_readable_size, to_bytes, sort_human_readable_sizes


class FormatSizeTestCase(unittest.TestCase):
    def test_format_readable_size(self):
        self.assertEqual(format_readable_size(0), "0.0 B")
        self.assertEqual(format_readable_size(1023), "1023.0 B")
        self.assertEqual(format_readable_size(1024), "1.0 KB")
        self.assertEqual(format_readable_size(123456789), "117.7 MB")
        self.assertEqual(format_readable_size(1000000000000), "931.3 GB")
        self.assertEqual(format_readable_size(999999999999999999), "888.2 PB")

    def test_format_readable_size_with_different_decimal_place(self):
        self.assertEqual(format_readable_size(1023, decimal_places=0), "1023 B")
        self.assertEqual(format_readable_size(1023, decimal_places=2), "1023.00 B")
        self.assertEqual(format_readable_size(1024, decimal_places=0), "1 KB")
        self.assertEqual(format_readable_size(123456789, decimal_places=1), "117.7 MB")
        self.assertEqual(format_readable_size(123456789, decimal_places=2), "117.74 MB")
        self.assertEqual(format_readable_size(1000000000000, decimal_places=3), "931.323 GB")
        self.assertEqual(format_readable_size(999999999999999999, decimal_places=4), "888.1784 PB")

    def test_format_readable_size_error(self):
        self.assertRaises(ValueError, format_readable_size, -100)
        self.assertRaises(ValueError, format_readable_size, -1)

    def test_to_bytes(self):
        self.assertEqual(to_bytes("0 B"), 0)
        self.assertEqual(to_bytes("1023 B"), 1023)
        self.assertEqual(to_bytes("1 KB"), 1024)
        self.assertEqual(to_bytes("117.73 MB"), 123448852)
        self.assertEqual(to_bytes("117.7 MB"), 123417395)
        self.assertEqual(to_bytes("931.3 GB"), 999975760691)
        self.assertEqual(to_bytes("888.1784 PB"), 999999977819630848)

    def test_to_bytes_wrong_unit(self):
        self.assertEqual(to_bytes("10230 B"), 10230)
        self.assertEqual(to_bytes("0.001 MB"), 1048)

    def test_to_bytes_error(self):
        self.assertRaises(ValueError, to_bytes, "")
        self.assertRaises(ValueError, to_bytes, "0")
        self.assertRaises(ValueError, to_bytes, "1")
        self.assertRaises(ValueError, to_bytes, "1.0 B B")
        self.assertRaises(ValueError, to_bytes, "-1")
        self.assertRaises(ValueError, to_bytes, "-1.0 B")

    def test_sort_human_readable_sizes(self):
        sizes = ["1 KB", "117.7 MB", "1023 B", "931.3 GB", "888.2 PB"]
        expected = ["1023 B", "1 KB", "117.7 MB", "931.3 GB", "888.2 PB"]
        self.assertEqual(sort_human_readable_sizes(sizes), expected)

        sizes = ["1 KB", "117.7 MB", "1023 B", "931.3 GB", "888.2 PB", "0 B"]
        expected = ["0 B", "1023 B", "1 KB", "117.7 MB", "931.3 GB", "888.2 PB"]
        self.assertEqual(sort_human_readable_sizes(sizes), expected)

        sizes = ["1 KB", "117.7 MB", "1023 B", "931.3 GB", "888.2 PB", "0 B", "1 KB"]
        expected = ["0 B", "1023 B", "1 KB", "1 KB", "117.7 MB", "931.3 GB", "888.2 PB"]
        self.assertEqual(sort_human_readable_sizes(sizes), expected)

        sizes = ["1.1 KB", "117.7 MB", "1023 B", "931.3 GB", "888.2 PB", "0 B", "1 KB", "1 KB"]
        expected = ["0 B", "1023 B", "1 KB", "1 KB", "1.1 KB", "117.7 MB", "931.3 GB", "888.2 PB"]
        self.assertEqual(sort_human_readable_sizes(sizes), expected)

    def test_sort_human_readable_sizes_reverse(self):
        sizes = ["1 KB", "117.7 MB", "1023 B", "931.3 GB", "888.2 PB"]
        expected = ["888.2 PB", "931.3 GB", "117.7 MB", "1 KB", "1023 B"]
        self.assertEqual(sort_human_readable_sizes(sizes, reverse=True), expected)

        sizes = ["1 KB", "117.7 MB", "1023 B", "931.3 GB", "888.2 PB", "0 B"]
        expected = ["888.2 PB", "931.3 GB", "117.7 MB", "1 KB", "1023 B", "0 B"]
        self.assertEqual(sort_human_readable_sizes(sizes, reverse=True), expected)

        sizes = ["1 KB", "117.7 MB", "1023 B", "931.3 GB", "888.2 PB", "0 B", "1 KB"]
        expected = ["888.2 PB", "931.3 GB", "117.7 MB", "1 KB", "1 KB", "1023 B", "0 B"]
        self.assertEqual(sort_human_readable_sizes(sizes, reverse=True), expected)

        sizes = ["1.1 KB", "117.7 MB", "1023 B", "931.3 GB", "888.2 PB", "0 B", "1 KB", "1 KB"]
        expected = ["888.2 PB", "931.3 GB", "117.7 MB", "1.1 KB", "1 KB", "1 KB", "1023 B", "0 B"]
        self.assertEqual(sort_human_readable_sizes(sizes, reverse=True), expected)

    def test_sort_human_readable_sizes_error(self):
        self.assertRaises(ValueError, sort_human_readable_sizes, ["1 KB", "117.7 Hello"])
        self.assertRaises(ValueError, sort_human_readable_sizes, ["1 KB", "117.7 MB", ""])
        self.assertRaises(ValueError, sort_human_readable_sizes, ["-1 KB"])


if __name__ == '__main__':
    unittest.main()
