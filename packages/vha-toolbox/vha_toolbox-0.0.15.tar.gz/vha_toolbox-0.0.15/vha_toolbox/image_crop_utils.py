from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from PIL import Image


CropPosition = Literal[
    "center", "left", "right", "top", "bottom"
]


def crop_to_square(
    image: "Image.Image",
    position: CropPosition = "center",
    offset: int = 0
) -> "Image.Image":
    """
    Crop an image to a square, with optional offset allowing to shift
    the crop start point (e.g. 10 px from top or bottom).

    Args:
        image (Image.Image): Input image.
        position (CropPosition): Crop alignment.
        offset (int): Shift from the chosen side.

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

    # Landscape mode
    if width > height:
        crop_size = height

        if position == "left":
            x0 = max(0, offset)
        elif position == "right":
            x0 = min(width - crop_size, width - crop_size - offset)
        elif position == "center":
            x0 = (width - crop_size) // 2
        else:
            raise ValueError(f"Invalid position '{position}' for landscape")

        box = (x0, 0, x0 + crop_size, height)

    # Portrait mode
    else:
        crop_size = width

        if position == "top":
            y0 = max(0, offset)
        elif position == "bottom":
            y0 = min(height - crop_size, height - crop_size - offset)
        elif position == "center":
            y0 = (height - crop_size) // 2
        else:
            raise ValueError(f"Invalid position '{position}' for portrait")

        box = (0, y0, width, y0 + crop_size)

    return image.crop(box)
