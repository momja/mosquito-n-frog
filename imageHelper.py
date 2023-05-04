import math
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

def compare_images(*imgs: np.ndarray) -> None:
    fig, axis = plt.subplots(len(imgs))
    for i, (plot, img) in enumerate(zip(axis, imgs)):
        plot.plot(img)
        plot.set_title("Image ", i)

    plt.show()

def to_black_and_white(img: np.ndarray, preserve_channels: bool = True) -> np.ndarray:
    """Convert color image to black and white, optionally preserving the channels

    Args:
        img (np.ndarray): _description_

    Returns:
        np.ndarray: _description_
    """
    m,n,c = img.shape

    if preserve_channels:
        return np.broadcast_to(cv.cvtColor(img, cv.COLOR_BGR2GRAY)[..., None],(m,n,c))
    else:
        return cv.cvtColor(img, cv.COLOR_BGR2GRAY) 

# def resize_max(img: np.ndarray, scale: float) -> np.ndarray:
#     # subdivide sprite sheet
#     h,w,c = img.shape
#     h_o,w_o= (math.ceil(h*scale), math.ceil(w*scale))
#     diff_x, diff_y = h - h_o/scale
#     cv.copyMakeBorder(img, )
#     bin_size = input_size // output_size
#     small_image = img.reshape((output_size, bin_size, 
#                                     output_size, bin_size, 3)).max(3).max(1)
#     Vreturn small_image