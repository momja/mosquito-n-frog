"""

"""
import os
import zipfile
import tempfile
from datetime import datetime
from pathlib import Path
import csv
import shutil

import cv2
import numpy as np
from numpy._typing import ArrayLike

import constants
from table_builder import TableBuilder
from image_builder import ImageBuilder
from sprite_utils.sprite_collection.sprite_collection import SpriteCollection


def export_png() -> bool:
    """
    Exports the final mosaic

    returns True on success

    """

    imageBuilder = ImageBuilder()

    return True


def export_csv(indices: ArrayLike, sprite_collection: SpriteCollection, h: int, w: int) -> bool:
    """
    Exports a zip file with the following structure:
    - A .csv file of the mosaic represented as a grid of indices corresponding to each tile
    - A .csv file mapping the index numbers to the tiles, and other useful metadata
    - A subirectory with the tiles from the sprite sheet parsed into their own images

    returns True on success

    """

    current_time = datetime.now().isoformat()
    filepaths = []

    # Create mosaic csv file
    temp_directory = Path(tempfile.gettempdir())
    mosaic_file = temp_directory.joinpath("mosaic.csv")
    np.savetxt(mosaic_file.as_posix(), indices, delimiter=',', fmt='%d')
    filepaths.append(mosaic_file.name)

    # Create png files for each image
    tile_directory = Path("tiles")
    tmp_tilepath = temp_directory.joinpath(tile_directory)
    try:
        shutil.rmtree(tmp_tilepath)
    except:
        pass
    os.mkdir(tmp_tilepath)
    print(sprite_collection.get_images().shape)
    images = sprite_collection.get_images()
    for i, sprite in enumerate(images):
        # images are normalized between 0 and 1. need to convert to 0-255
        # TODO: put this conversion logic somewhere else, maybe in image_helper.py
        name = _get_tile_filename(i)
        cv2.imwrite(tmp_tilepath.joinpath(name).as_posix(), sprite * 255)
        filepaths.append(tile_directory.joinpath(name))

    # Create csv key file
    tile_key_data = []
    for i, sprite in enumerate(sprite_collection.get_images()):
        tile_key_data.append([i, _get_tile_filename(i)])

    key_filename = f"key{constants.EXTENSIONS.CSV}"
    tile_key_file = temp_directory.joinpath(key_filename).as_posix()
    with open(tile_key_file, 'w', newline='') as csvfile:
        csv.writer(csvfile).writerows(tile_key_data)
    filepaths.append(key_filename)

    zipfile_name = f"result_{current_time}{constants.EXTENSIONS.ZIP}"
    create_zip(filepaths, temp_directory, zipfile_name)

    return True


def _get_tile_filename(index: int):
    return f"{index}_tile{constants.EXTENSIONS.PNG}"


def create_zip(file_paths, temp_directory, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file_path in file_paths:
            zipf.write(temp_directory.joinpath(file_path), arcname=file_path)
