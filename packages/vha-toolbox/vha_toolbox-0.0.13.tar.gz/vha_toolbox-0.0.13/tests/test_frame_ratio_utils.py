import unittest
from PIL import Image
from vha_toolbox import should_rotate_by_ratio


class ShouldRotateByRatioTestCase(unittest.TestCase):

    def _img(self, w, h):
        """Utility pour créer une image PIL en mémoire."""
        return Image.new("RGB", (w, h))

    def test_no_rotation_on_square_frame(self):
        frame = self._img(1000, 1000)
        img = self._img(3000, 2000)

        result = should_rotate_by_ratio(
            img, frame,
            frame_target_ratio=2/3,
            img_target_ratio=3/2
        )
        self.assertFalse(result)

    def test_rotation_for_matching_ratios_and_orientation_flip(self):
        frame = self._img(2000, 3000)  # portrait ≈ 0.66
        img = self._img(3000, 2000)    # landscape ≈ 1.5

        result = should_rotate_by_ratio(
            img, frame,
            frame_target_ratio=2/3,
            img_target_ratio=3/2
        )
        self.assertTrue(result)

    def test_no_rotation_if_ratios_do_not_match(self):
        frame = self._img(2000, 3000)  # ratio ≈ 0.66
        img = self._img(4000, 2000)    # ratio = 2.0 > mauvais ratio

        result = should_rotate_by_ratio(
            img, frame,
            frame_target_ratio=2/3,
            img_target_ratio=3/2
        )
        self.assertFalse(result)

    def test_no_rotation_if_orientation_not_flipped(self):
        frame = self._img(2000, 3000)  # portrait ratio 2/3
        img = self._img(2000, 3000)    # portrait ratio 2/3

        result = should_rotate_by_ratio(
            img, frame,
            frame_target_ratio=2/3,
            img_target_ratio=3/2
        )
        self.assertFalse(result)

    def test_rotation_without_orientation_requirement(self):
        frame = self._img(2000, 3000)
        img = self._img(3000, 2000)

        result = should_rotate_by_ratio(
            img, frame,
            frame_target_ratio=2/3,
            img_target_ratio=3/2,
            require_orientation_flip=False,
        )
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
