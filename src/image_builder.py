"""
Authored by: Maxwell Omdal

image_builder is used for constructing mosaics.
The module is not aware of where the image data comes from,
and does not choose which images to use,
it's just for inserting mosaic images into a larger image.
"""

from builder import Builder
import numpy as np

class ImageBuilder(Builder):
    def insert_subimage(self, x, y, subimg, img, scale) -> None:
        if scale == 1:
            # a lot quicker than sub-array insertion, so we can use this as a shortcut
            img[y,x] = subimg
        else:
            img[y*scale:y*scale+scale, x*scale:x*scale+scale] = subimg
