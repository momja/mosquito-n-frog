"""Abstract class for sprite selection"""

from abc import abstractmethod
from typing import Tuple

import numpy

class AbstractSpriteSelector:
    """Abstraction of the sprite selector utility class
    """

    @abstractmethod
    def classify(self, img: numpy.ndarray, scale: float = 1) -> Tuple[numpy.ndarray, int, int]:
        """implemented by subclasses.
        classifies all the pixels in an image
        according to the implemented selector's logic

        Args:
            val (numpy.ndarray): the image of shape (m,n,3)
            scale (float): float value to scale original image by (if scale is 0.1 and img width is 100px, the final image will be 10 sprites wide)

        Returns:
            np.ndarray: an array of shape (m,n) where each index corresponds to a sprite in the sprite collection
        """