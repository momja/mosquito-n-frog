"""
Helper for dealing with command line arguments
"""

import argparse

def make_parser():
    parser = argparse.ArgumentParser(description='tool for assisted mosaic generation')
    parser.add_argument('-i', '--image', help='sample image to use for mosaic generation')
    parser.add_argument('-s', '--spritesheet', help='file path to the sprite sheet to use')
    parser.add_argument('-x', dest='x_count', type=int, help='count of tiles in X direction of result')
    parser.add_argument('-y', dest='y_count', type=int, help='count of tiles in Y direction of result')
    parser.add_argument('--height', type=int, default=16, help='pixel height of each sprite in the spritesheet')
    parser.add_argument('--width', type=int, default=16, help='pixel width of each sprite in the spritesheet')
    parser.add_argument('-e', '--export', dest='is_export', type=bool, help='if export flag is provided, the result will be exported instead of displayed')
    return parser

def get_args():
    parser = make_parser()
    return parser.parse_args()
