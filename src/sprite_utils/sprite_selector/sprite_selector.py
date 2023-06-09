"""
The standard sprite selector implementation uses the pixel color
at each point in the image solely as it's classifier technique
"""

import numpy as np
import cv2 as cv
from sklearn.neighbors import NearestNeighbors

from sprite_utils.sprite_collection.sprite_collection import SpriteCollection
from sprite_utils.sprite_selector.abstract_sprite_selector import AbstractSpriteSelector

class SpriteSelector(AbstractSpriteSelector):
    """
    Used for controlling the KNN model of sprite selection.
    Relies on the SpriteCollection class

    """

    def __init__(self, sprite_collection: SpriteCollection) -> None:
        nbrs_learner = NearestNeighbors(n_neighbors=1, algorithm='ball_tree')
        print("classifying")
        self._nbrs_classifier = nbrs_learner.fit(sprite_collection.get_bins())
        print("done classifying")
        self._sprite_collection = sprite_collection

    def classify(self, image: np.ndarray, scale: float = 1):
        """Accepts ndarray of shape (n, m, 3) and returns classified values

        Args:
            img (np.ndarray): image to run classifier on

        Returns:
            _type_: _description_
        """

        assert(len(image.shape) == 3)

        h, w = self._sprite_collection.get_height(), self._sprite_collection.get_width()

        scale_width = image.shape[1] // w
        scale_height = image.shape[0] // h
        dim = (scale_width, scale_height)

        scaled_image = cv.resize(image, dim, interpolation=cv.INTER_LINEAR)
        _, indices = self._nbrs_classifier.kneighbors(scaled_image.reshape(-1, 3))
        indices = indices.reshape(scale_height, scale_width)
        return indices, scale_height, scale_width
