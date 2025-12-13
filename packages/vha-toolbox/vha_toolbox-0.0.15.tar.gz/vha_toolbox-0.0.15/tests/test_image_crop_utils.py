import unittest
from PIL import Image
from vha_toolbox import crop_to_square


def make_img(w, h, color=(100, 0, 0)):
    """Helper: create a simple RGB image."""
    return Image.new("RGB", (w, h), color)


class CropToSquareTestCase(unittest.TestCase):

    def test_square_image_copy(self):
        img = make_img(500, 500)
        out = crop_to_square(img)

        self.assertEqual(out.size, (500, 500))
        self.assertIsNot(out, img)  # must be a copy
        self.assertEqual(list(out.getdata()), list(img.getdata()))

    def test_landscape_center(self):
        img = make_img(800, 600)
        out = crop_to_square(img, "center")
        self.assertEqual(out.size, (600, 600))

    def test_landscape_left(self):
        img = make_img(800, 600, (255, 0, 0))
        out = crop_to_square(img, "left")
        self.assertEqual(out.size, (600, 600))
        self.assertEqual(out.getpixel((0, 0)), (255, 0, 0))

    def test_landscape_right(self):
        img = make_img(800, 600, (123, 200, 50))
        out = crop_to_square(img, "right")
        self.assertEqual(out.size, (600, 600))
        self.assertEqual(out.getpixel((599, 0)), (123, 200, 50))

    def test_portrait_center(self):
        img = make_img(600, 900)
        out = crop_to_square(img, "center")
        self.assertEqual(out.size, (600, 600))

    def test_portrait_top(self):
        img = make_img(600, 900, (10, 100, 200))
        out = crop_to_square(img, "top")
        self.assertEqual(out.size, (600, 600))
        self.assertEqual(out.getpixel((0, 0)), (10, 100, 200))

    def test_portrait_bottom(self):
        img = make_img(600, 900, (20, 50, 90))
        out = crop_to_square(img, "bottom")
        self.assertEqual(out.size, (600, 600))
        self.assertEqual(out.getpixel((0, 599)), (20, 50, 90))

    def test_invalid_position_landscape(self):
        img = make_img(800, 600)
        with self.assertRaises(ValueError):
            crop_to_square(img, "top")  # invalid for landscape

    def test_invalid_position_portrait(self):
        img = make_img(600, 900)
        with self.assertRaises(ValueError):
            crop_to_square(img, "left")  # invalid for portrait

    def test_none_input(self):
        with self.assertRaises(ValueError):
            crop_to_square(None)


if __name__ == '__main__':
    unittest.main()
