import numpy as np
import matplotlib.pyplot as plt

class SpriteCollection:

    def __init__(self, images: np.ndarray, bins: np.ndarray) -> None:
        """Build a sprite collection from the reference images
        """
        self._images = images
        self._bins = bins

    def get_images(self) -> np.ndarray:
        return self._images

    def get_image(self, index) -> np.ndarray:
        return self._images[index]

    def set_images(self, images: np.ndarray) -> None:
        self._images = images

    def get_bins(self) -> np.ndarray:
        return self._bins

    def set_bins(self, bins: np.ndarray) -> None:
        self._bins = bins

    def show_sprite_collection(self):
        fig, axs = plt.subplots(self._images.shape[0])
        for i, img in enumerate(self._images):
            axs[i].imshow(img)
            axs[i].axis('off')
        plt.show()