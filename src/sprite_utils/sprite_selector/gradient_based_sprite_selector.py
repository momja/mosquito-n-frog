"""The gradient-based sprite selector utilizes both
a pixel color based KNN approach, and a gradient based matching approach
"""
from typing import Tuple
from matplotlib import pyplot as plt
import numpy as np
import cv2 as cv
from sprite_utils.sprite_collection.sprite_collection import SpriteCollection
from sprite_utils.sprite_selector.sprite_selector import SpriteSelector
from sklearn.neighbors import NearestNeighbors

class GradientBasedSpriteSelector(SpriteSelector):
    """The gradient-based sprite selector utilizes both
    a pixel color based KNN approach, and a gradient based matching approach
    """
    
    def __init__(self, sprite_collection: SpriteCollection) -> None:
        # check required shape for gradient baseed sprite selector
        assert(sprite_collection.get_bins().shape[-1] == 9)
        nbrs_learner = NearestNeighbors(n_neighbors=1, algorithm='kd_tree')
        self.nbrs_classifier = nbrs_learner.fit(sprite_collection.get_bins())

    def classify(self, image: np.ndarray, sprite_collection: SpriteCollection, scale: float = 1):
        assert(len(image.shape) == 3)

        scale_width = int(image.shape[1] * scale)
        scale_height = int(image.shape[0] * scale)
        dim = (scale_width, scale_height)

        scaled_image = cv.resize(image, dim, interpolation=cv.INTER_LINEAR)
        
        dx, dy = self._build_normal_gradient(image, dim)

        sample = np.concatenate((scaled_image, dx, dy), axis=2)

        # TODO: This is really, really slow
        _, indices = self.nbrs_classifier.kneighbors(sample.reshape(-1, 9))
        indices = indices.reshape(scale_height, scale_width)

        return indices, scale_height, scale_width

    def _build_normal_gradient(self, img: np.ndarray, dim: Tuple[int, int]) -> np.ndarray:
        dx_64f = cv.Sobel(img, cv.CV_64F, 1, 0, ksize=11)
        dy_64f = cv.Sobel(img, cv.CV_64F, 0, 1, ksize=11)
        dx_64f = cv.resize(dx_64f, dim, interpolation=cv.INTER_CUBIC)
        dy_64f = cv.resize(dy_64f, dim, interpolation=cv.INTER_CUBIC)

        x_max = np.max(np.abs(dx_64f))
        y_max = np.max(np.abs(dy_64f))
        if x_max != 0:
            dx_64f = dx_64f/x_max
        if y_max != 0:
            dy_64f = dy_64f/y_max
        return dx_64f, dy_64f
