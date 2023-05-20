"""
Parent builder class for constructing a representation of the mosaic. There are different ways a user might want to generate the final result of the program, so they can continue the process manually. You can check out :mod:`image_builder` and :mod:`table_builder` for some examples
"""

from abc import ABC, abstractmethod
import numpy as np

class Builder(ABC):
    @abstractmethod
    def insert_subimage(self, x:int, y:int, subimg, img, scale: int) -> None:
        """Inserts a subimage into a larger image canvas
    
        Args:
            x (int): x coord
            y (int): y coord
            subimg (np.ndarray): smaller image
            img (np.ndarray): image to add subimage to
            scale (int): the multiplier for the (x,y) coordinates
        """
        pass
