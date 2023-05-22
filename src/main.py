#!/usr/bin/env python

"""
Main script for the Mosquito and Frog project

"""

__author__ = "Maxwell Omdal"

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

import image_helper
import logger
import parser_utils
from image_builder import ImageBuilder
from sprite_utils.sprite_collection.default_sprite_collection_builder import DefaultSpriteCollectionBuilder
from sprite_utils.sprite_collection.sprite_collection_builder import SpriteCollectionBuilder
from sprite_utils.sprite_selector.sprite_selector import SpriteSelector
import mosaic_exporter

if __name__ == '__main__':
    args = parser_utils.get_args()

    img = cv.imread(args.image)
    # Matplotlib displays images in BGR space for some reason
    img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
    img = image_helper.to_black_and_white(img)
    img = img/255

    sprite_collection_builder = DefaultSpriteCollectionBuilder()
    if args.spritesheet:
        sprite_collection_builder = SpriteCollectionBuilder()
        sprite_sheet = cv.imread(args.spritesheet)
        sprite_sheet = cv.cvtColor(sprite_sheet, cv.COLOR_RGB2BGR)/255
        sprite_collection_builder.add_sheet(sprite_sheet)

    sprite_collection_builder.set_sprite_height(args.height)
    sprite_collection_builder.set_sprite_width(args.width)
    sprite_collection = sprite_collection_builder.build()
    sprite_selector = SpriteSelector(sprite_collection)

    aspect_ratio = image_helper.aspect_ratio(img)
    y_count = args.y_count or int(args.x_count/aspect_ratio)

    img = image_helper.resize_image_for_sprites(img, args.x_count, y_count, sprite_collection)

    height, width, channels = img.shape

    indices, h, w = sprite_selector.classify(img, 1)

    binned_img = np.zeros((height, width, 3))

    logger.log_message("Teste")

    if args.is_export:
        mosaic_exporter.export_csv(indices, sprite_collection, h, w)
    else:
        imageBuilder = ImageBuilder()

        for y, row2 in enumerate(indices):
            for x, index in enumerate(row2):
                imageBuilder.insert_subimage(x, y, sprite_collection.get_image(index), binned_img, args.height)

        plt.imshow(binned_img)
        plt.show()
