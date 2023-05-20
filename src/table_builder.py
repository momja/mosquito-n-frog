"""
If you want to take the digital representation and render it physically by hand,
you are going to want a table. This is to aid with that.

If you are trying to generate the digital image, check out :mod:`image_builder`
"""

import numpy as np
from builder import Builder

class TableBuilder(Builder):
    """
    Table Builder is for building .csv files with the indexes of the classified mosaic tiles/sprites
    """

    def __init__(self, h: int, w: int) -> None:
        super().__init__()
        self._xy_arr = np.zeros((h, w)) # Assume it's always first two channels of the image


    def insert_subimage(self, x, y, index, img, scale):
        self._xy_arr[y, x] = index

    def build(self):
        filename = 'result.csv'
        np.savetxt(filename, self._xy_arr, delimiter=',', fmt='%d')
        return filename
