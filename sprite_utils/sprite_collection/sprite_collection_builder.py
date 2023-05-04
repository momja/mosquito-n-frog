"""Sprite Collection Builder standard implementation
"""
import numpy as np
import cv2 as cv
from sprite_utils import constants
from sprite_utils.sprite_collection.sprite_collection import SpriteCollection

class SpriteCollectionBuilder:
    """Builds sprite collections
    """

    def __init__(self) -> None:
        self._sheets = []
        self._width = 0
        self._height = 0
        self._horizontal_spacing = 0
        self._vertical_spacing = 0
        self._include_rotations = False
        self._include_gradient = False

    def add_sheet(self, image: np.ndarray) -> None:
        """add a sheet of sprites to the current collection given the sheet array

        Args:
            image (np.ndarray): the sprite sheet to be split and added to the collection
        """
        self._sheets.append(image)

    def set_sprite_width(self, width: int) -> None:
        self._width = width

    def set_sprite_height(self, height: int) -> None:
        self._height = height

    def set_sprite_horizontal_spacing(self, horizontal_spacing: int) -> None:
        """Some spritesheets have spacing between each sprite for visibility
        """
        self._horizontal_spacing = horizontal_spacing

    def set_sprite_vertical_spacing(self, vertical_spacing: int) -> None:
        """Some spritesheets have spacing between each sprite for visibility
        """
        self._vertical_spacing = vertical_spacing

    def set_include_rotations(self):
        self._include_rotations = True

    def set_include_gradient(self):
        self._include_gradient = True

    def _create_bins(self, images:np.ndarray) -> np.ndarray:
        """Create the bins which are used to fit the classifier model.

        Args:
            images (np.ndarray): the set of images of shape (x,m,n,3) for the sprite collector

        Returns:
            np.ndarray: numpy array of shape (x,y),
            where x is the number of images provided,
            and y is the channels.

            This may include extra channels, such as x and y gradient,
            so it is not guaranteed to always be the standard 3
        """

        x, m, n, _ = images.shape

        if not self._include_gradient:
            return np.mean(images, axis=(1,2)) 
        else:
            gradients = self._compute_gradients(images)
            mean_gradients = np.mean(gradients, axis=(1,2)) # compute the mean x, y gradients
            flat_mean_gradients = mean_gradients.reshape(x,-1) # join last two axes
            final_bins = np.concatenate((np.mean(images, axis=(1,2)), flat_mean_gradients), axis=1)
            return final_bins # should be of shape (x, 9) assuming channels==3
    
    def _compute_gradients(self, images: np.ndarray) -> np.ndarray:
        """Computes x and y gradients for the provided images.

        Args:
            images (np.ndarray): set of images to compute gradients for
            (x,m,n,3) where x is the number of 3-channel images 
        Returns:
            np.ndarray: (x,m,n,2,3) array
        """
        x,m,n,c = images.shape
        gradients = np.empty((x,m,n,2,c))
        for i, image in enumerate(images):
            dx_64f = cv.Sobel(image, cv.CV_64F, 1, 0, ksize=11)
            dy_64f = cv.Sobel(image, cv.CV_64F, 0, 1, ksize=11)
            x_max = np.max(np.abs(dx_64f))
            y_max = np.max(np.abs(dy_64f))
            if x_max != 0:
                dx_64f = dx_64f/x_max
            if y_max != 0:
                dy_64f = dy_64f/y_max
            gradients[i] = np.stack((dx_64f, dy_64f), axis=2)

        return gradients

    def build(self) -> SpriteCollection:
        total_images = sum([
                sheet.shape[0]//(self._vertical_spacing + self._height)*\
                sheet.shape[1]//(self._horizontal_spacing + self._width)\
            for sheet in self._sheets])

        all_images = np.empty((total_images, self._width, self._height, constants.CHANNELS))
        # TODO: I don't think a for loop is needed, it should all be doable with dsplit
        images_added = 0
        for sheet in self._sheets:
            sheet_height, sheet_width, _ = sheet.shape
            
            # subdivide sprite sheet
            images = sheet.reshape(sheet_height // self._height,
                                   self._height,
                                   sheet_width // self._width,
                                   self._width,
                                   constants.CHANNELS)
            images = images.swapaxes(1,2)
            images = images.reshape(-1, self._height, self._width, constants.CHANNELS)

            # TODO: will fail with non-zero spacing
            all_images[images_added:images_added+images.shape[0]] = images
            images_added += images.shape[0]

        if self._include_rotations:
            r90 = np.rot90(all_images, 1, (1,2))
            r180 = np.rot90(all_images, 2, (1,2))
            r270 = np.rot90(all_images, 3, (1,2))
            all_images = np.vstack((all_images, r90, r180, r270))

        bins = self._create_bins(all_images)
        sprite_collector = SpriteCollection(all_images, bins)
        return sprite_collector
