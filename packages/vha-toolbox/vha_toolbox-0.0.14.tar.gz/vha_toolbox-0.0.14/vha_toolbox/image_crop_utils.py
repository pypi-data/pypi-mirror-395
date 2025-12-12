from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from PIL import Image


CropPosition = Literal[
    "center", "left", "right", "top", "bottom"
]


def crop_to_square(
    image: "Image.Image",
    position: CropPosition = "center"
) -> "Image.Image":
    """
    Crop an image to a square by trimming the longer dimension.

    Valid positions:
        - Landscape: "center", "left", "right"
        - Portrait : "center", "top", "bottom"

    Args:
        im (Image.Image): Input image.
        position (CropPosition): Crop alignment.

    Returns:
        Image.Image: Square-cropped image.

    Raises:
        ValueError: If image is None or position is invalid.
    """
    if image is None:
        raise ValueError("Image cannot be None")

    width, height = image.size

    # already square
    if width == height:
        return image.copy()

    # Landscape cropping
    if width > height:
        crop_size = height
        if position == "left":
            x0 = 0
        elif position == "right":
            x0 = width - crop_size
        elif position == "center":
            x0 = (width - crop_size) // 2
        else:
            raise ValueError(f"Invalid position '{position}' for landscape image")

        box = (x0, 0, x0 + crop_size, height)

    # Portrait cropping
    else:
        crop_size = width
        if position == "top":
            y0 = 0
        elif position == "bottom":
            y0 = height - crop_size
        elif position == "center":
            y0 = (height - crop_size) // 2
        else:
            raise ValueError(f"Invalid position '{position}' for portrait image")

        box = (0, y0, width, y0 + crop_size)

    return image.crop(box)
