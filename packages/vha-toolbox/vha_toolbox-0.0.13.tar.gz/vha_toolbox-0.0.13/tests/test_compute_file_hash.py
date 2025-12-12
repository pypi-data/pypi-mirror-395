import unittest
import tempfile
from pathlib import Path

from vha_toolbox import compute_file_hash, compute_stable_hash


class ComputeFileHashTestCase(unittest.TestCase):

    def test_hash_identical_files(self):
        """Two files with identical content must produce the same hash."""
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            f1 = p / "file1.txt"
            f2 = p / "file2.txt"

            f1.write_text("Hello World")
            f2.write_text("Hello World")

            h1 = compute_file_hash(f1)
            h2 = compute_file_hash(f2)

            self.assertEqual(h1, h2)

    def test_hash_different_files(self):
        """Different content must produce a different hash."""
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            f1 = p / "file1.txt"
            f2 = p / "file2.txt"

            f1.write_text("Hello World")
            f2.write_text("Other content")

            h1 = compute_file_hash(f1)
            h2 = compute_file_hash(f2)

            self.assertNotEqual(h1, h2)

    def test_hash_changes_with_extra_file(self):
        """Adding an extra file must change the resulting hash."""
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            main = p / "main.txt"
            extra = p / "extra.txt"

            main.write_text("AAA")
            extra.write_text("BBB")

            h_main_only = compute_file_hash(main)
            h_with_extra = compute_file_hash(main, [extra])

            self.assertNotEqual(h_main_only, h_with_extra)

    def test_hash_changes_when_extra_file_changes(self):
        """Modifying an extra file must change the hash."""
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            main = p / "main.txt"
            extra = p / "extra.txt"

            main.write_text("AAA")
            extra.write_text("BBB")

            h1 = compute_file_hash(main, [extra])

            extra.write_text("BBB modified")
            h2 = compute_file_hash(main, [extra])

            self.assertNotEqual(h1, h2)

    def test_stable_hash_with_multiple_extras(self):
        """Same files in the same order must always produce the same hash."""
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            main = p / "main.txt"
            e1 = p / "a.txt"
            e2 = p / "b.txt"

            main.write_text("XXX")
            e1.write_text("111")
            e2.write_text("222")

            h1 = compute_file_hash(main, [e1, e2])
            h2 = compute_file_hash(main, [e1, e2])

            self.assertEqual(h1, h2)

    def test_short_hash_length(self):
        """The returned hash must be 8 characters long."""
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            f = p / "x.txt"
            f.write_text("content")

            h = compute_file_hash(f)
            self.assertEqual(len(h), 8)

    def test_missing_file_raises(self):
        """A missing file must raise FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            compute_file_hash("does_not_exist.txt")

    def test_same_values_same_hash(self):
        values1 = ["image1.png", 3000, 2]
        values2 = ["image1.png", 3000, 2]

        h1 = compute_stable_hash(values1)
        h2 = compute_stable_hash(values2)

        self.assertEqual(h1, h2)

    def test_different_values_different_hash(self):
        values1 = ["image1.png", 3000, 2]
        values2 = ["image1.png", 3000, 3]

        h1 = compute_stable_hash(values1)
        h2 = compute_stable_hash(values2)

        self.assertNotEqual(h1, h2)

    def test_dict_order_does_not_matter(self):
        v1 = {"x": 1, "y": 2}
        v2 = {"y": 2, "x": 1}

        h1 = compute_stable_hash(v1)
        h2 = compute_stable_hash(v2)

        self.assertEqual(h1, h2)

    def test_set_order_does_not_matter(self):
        v1 = {1, 2, 3}
        v2 = {3, 2, 1}

        h1 = compute_stable_hash(v1)
        h2 = compute_stable_hash(v2)

        self.assertEqual(h1, h2)

    def test_prefix_is_applied(self):
        values = ["a", "b", "c"]
        h = compute_stable_hash(values, prefix="row_")

        self.assertTrue(h.startswith("row_"))
        self.assertEqual(len(h) - len("row_"), 8)

    def test_custom_length(self):
        values = ["a", "b", "c"]
        h = compute_stable_hash(values, length=12)

        self.assertEqual(len(h), 12)

    def test_non_iterable_wrapped(self):
        h1 = compute_stable_hash("hello")
        h2 = compute_stable_hash(["hello"])

        self.assertEqual(h1, h2)

    def test_bytes_and_path_supported(self):
        data = b"\x01\x02\x03"
        path = Path("/some/path/image.avif")

        # Just ensure it does not raise and returns a string of correct length
        h = compute_stable_hash([data, path])
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 8)

    def test_nested_structures_stable(self):
        v1 = {
            "a": [1, 2, {"x": 10}],
            "b": {"k": {3, 4}},
        }
        v2 = {
            "b": {"k": {4, 3}},
            "a": [1, 2, {"x": 10}],
        }

        h1 = compute_stable_hash(v1)
        h2 = compute_stable_hash(v2)

        self.assertEqual(h1, h2)


if __name__ == '__main__':
    unittest.main()
