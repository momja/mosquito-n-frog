#!/usr/bin/env python

"""Main script for the Mosquito and Frog project"""

__author__ = "Maxwell Omdal"

import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import progressbar
import argparse
import imageBuilder
import imageHelper
from builtins import breakpoint
from sprite_utils.sprite_selector.gradient_based_sprite_selector import GradientBasedSpriteSelector
from sprite_utils.sprite_selector.sprite_selector import SpriteSelector
from sprite_utils.sprite_collection.sprite_collection_builder import SpriteCollectionBuilder

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tool for assisted mosaic generation')
    parser.add_argument('-i', '--image', help='sample image to use for mosaic generation')
    args = parser.parse_args()

    img = cv.imread(args.image)
    # Matplotlib displays images in BGR space for some reason
    img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
    img = imageHelper.to_black_and_white(img)
    img = img/255
    height, width, channels = img.shape

    sprite_sheet = cv.imread("example/corners.png")
    sprite_sheet = cv.cvtColor(sprite_sheet, cv.COLOR_RGB2BGR)/255

    sprite_collection_builder = SpriteCollectionBuilder()
    sprite_collection_builder.add_sheet(sprite_sheet)
    sprite_collection_builder.set_sprite_height(16)
    sprite_collection_builder.set_sprite_width(16)
    sprite_collection_no_gradient = sprite_collection_builder.build()
    sprite_collection_builder.set_include_rotations()
    sprite_collection_builder.set_include_gradient()
    sprite_collection = sprite_collection_builder.build()
    breakpoint()
    sprite_selector_no_gradient = SpriteSelector(sprite_collection_no_gradient)

    indices_2, h, w = sprite_selector_no_gradient.classify(img, 0.02)

    binned_img2 = np.zeros((h*16, w*16, 3))
    bins = sprite_collection.get_bins()
    
    for y, row2 in enumerate(indices_2):
        for x, index2 in enumerate(row2):
            imageBuilder.insert_subimage(x, y, sprite_collection_no_gradient.get_image(index2), binned_img2, 16)


    # sprite_collection.show_sprite_collection()
    # print(sprite_collection.get_bins())

    # print(binned_img.shape)
    # dx, dy = sprite_selector._build_normal_gradient(img, (img.shape[1], img.shape[0]))
    
    fig, axis = plt.subplots(2,2)
    axis[0,0].set_title("with gradient")
    axis[0,1].set_title("no gradient")
    axis[0,1].imshow(binned_img2)
    # axis[1,0].set_title("x gradient")
    # axis[1,0].imshow(dx)
    # axis[1,1].set_title("y gradient")
    # axis[1,1].imshow(dy)
    plt.show()
