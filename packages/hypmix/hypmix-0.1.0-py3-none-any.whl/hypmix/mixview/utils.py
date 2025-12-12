# Standard Libraries
from typing import NamedTuple

# Dependencies
from matplotlib.axes import Axes
import numpy as np


class SquareOffset(NamedTuple):
    x_offset: int = 0
    y_offset: int = 0


def square_image(
    img: np.ndarray, rgb: bool = False
) -> tuple[SquareOffset, np.ndarray]:
    """
    Pads a rectangular image to make it square, for the purpose of reshaping
    an image axis to be better suited for GUI applications.

    Parameters
    ----------
    img: np.ndarray
        Image array.
    rgb: bool, optional
        Option to specify RGB image input.

    Returns
    -------
    offset: SquareOffset
        NamedTuple of offset values added due to padding. The 2 attributes are
        `x_offset` and `y_offset` representing the horizontal and vertical
        offsets respectively. One will always be zero.
    square_img: np.ndarray
        Image with np.nan values padding the sides to fit the square
    """
    long_axis = np.argmax(img.shape)
    if not rgb:
        short_axis = np.argmin(img.shape)
        padding_length = (img.shape[long_axis] - img.shape[short_axis]) // 2
        square_padding = np.full(
            (img.shape[long_axis], padding_length),
            np.nan,
        )
        square_img = np.concat(
            [square_padding, img, square_padding], axis=short_axis
        )

        if long_axis < short_axis:
            offset = SquareOffset(-padding_length, 0)
        else:
            offset = SquareOffset(0, -padding_length)

        return offset, square_img
    else:
        short_axis = np.argmin(img.shape[:-1])
        padding_length = (img.shape[long_axis] - img.shape[short_axis]) // 2
        square_padding = np.full(
            (img.shape[long_axis], padding_length, 3),
            np.nan,
        )
        square_img = np.concat(
            [square_padding, img, square_padding],
            axis=short_axis,
        )
        if long_axis < short_axis:
            offset = SquareOffset(-padding_length, 0)
        else:
            offset = SquareOffset(0, -padding_length)
        return offset, square_img


def set_image_axis(ax: Axes) -> None:
    """
    Sets a matplotlib axis up to display an image.
    """
    ax.set_xticks([])
    ax.set_yticks([])
    ax.tick_params(
        axis="both",
        which="both",
        bottom=False,
        top=False,
        left=False,
        right=False,
        labelbottom=False,
        labelleft=False,
    )
