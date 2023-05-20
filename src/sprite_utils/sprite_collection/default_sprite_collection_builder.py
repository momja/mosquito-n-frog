"""
A default Sprite Collection Builder used when no spritesheet is provided
"""
import numpy as np
from sprite_utils import constants
from sprite_utils.sprite_collection.sprite_collection import SpriteCollection

class DefaultSpriteCollectionBuilder:
    def __init__(self) -> None:
        self._width = 0
        self._height = 0


    def set_sprite_width(self, width: int) -> None:
        self._width = width


    def set_sprite_height(self, height: int) -> None:
        self._height = height


    def _create_bins(self, images:np.ndarray) -> np.ndarray:
        return np.mean(images, axis=(1,2))


    def build(self) -> SpriteCollection:
        total_images = 8
        all_images = np.ones((total_images, self._width, self._height, constants.CHANNELS))
        for i, image in enumerate(all_images):
            image*=i/(8-1)

        return SpriteCollection(all_images, self._create_bins(all_images))
