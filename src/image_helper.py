import math
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from sprite_utils.sprite_collection.sprite_collection import SpriteCollection


def compare_images(*imgs: np.ndarray) -> None:
    fig, axis = plt.subplots(len(imgs))
    for i, (plot, img) in enumerate(zip(axis, imgs)):
        plot.plot(img)
        plot.set_title("Image ", i)

    plt.show()


def to_black_and_white(img: np.ndarray, preserve_channels: bool = True) -> np.ndarray:
    """
    Convert color image to black and white, optionally preserving the channels

    Args:
        img (np.ndarray): the original image
        preserve_channels (bool): whether the dimension of the image should be reduced to 2,
                                  or all channels will be kept, but as duplicates of each other

    Returns:
        np.ndarray: black and white image
    """
    m, n, c = img.shape

    if preserve_channels:
        return np.broadcast_to(cv.cvtColor(img, cv.COLOR_BGR2GRAY)[..., None], (m, n, c))
    else:
        return cv.cvtColor(img, cv.COLOR_BGR2GRAY)


def resize_image_for_sprites(img: np.ndarray, x_count: int, y_count: int, spritesheet: SpriteCollection) -> np.ndarray:
    """
    
    """
    up_points = (x_count*spritesheet.get_width(), y_count*spritesheet.get_height())
    return cv.resize(img, up_points, interpolation=cv.INTER_LINEAR)


def aspect_ratio(img: np.ndarray):
    """
    Width/Height
    """

    return img.shape[1]/img.shape[0]
