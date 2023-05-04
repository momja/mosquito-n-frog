"""
Authored by: Maxwell Omdal

image_builder is used for constructing mosaics.
The module is not aware of where the image data comes from,
and does not choose which images to use,
it's just for inserting mosaic images into a larger image.
"""

import numpy as np

def insert_subimage(x: int, y: int, subimg: np.ndarray, img: np.ndarray, scale: int) -> None:
    """Inserts a subimage into a larger image canvas

    Args:
        x (int): x coord
        y (int): y coord
        subimg (np.ndarray): smaller image
        img (np.ndarray): image to add subimage to
        scale (int): the multiplier for the (x,y) coordinates
    """

    if scale == 1:
        # a lot quicker than sub-array insertion, so we can use this as a shortcut
        img[y,x] = subimg
    else:
        img[y*scale:y*scale+scale, x*scale:x*scale+scale] = subimg
