import os
import cv2
import shutil
import numpy as np

from glob import glob
from pathlib import Path
from argparse import ArgumentParser

def convert_image_name_in_loop(image_path, start_idx):
    os.makedirs(os.path.join(image_path, 'source'), exist_ok=True)
    path = Path(image_path)
    image_list = sorted(glob(f'{path}/*.jpg') + glob(f'{path}/*.png'))

    for idx,image in enumerate(image_list):

        save_idx = idx + start_idx

        shutil.copy(image, os.path.join(os.path.join(image_path, 'source'),f"{save_idx:05d}.png"))
        os.remove(image)

def pad_image_name_in_loop(image_path, start_idx):
    os.makedirs(os.path.join(image_path, 'source'), exist_ok=True)
    path = Path(image_path)
    image_list = sorted(glob(f'{path}/*.jpg') + glob(f'{path}/*.png'))

    for idx,image in enumerate(image_list):

        image_idx = int(Path(image).stem)

        save_idx = image_idx + start_idx

        shutil.copy(image, os.path.join(os.path.join(image_path, 'source'),f"{save_idx:05d}.png"))
        os.remove(image)

if __name__ == '__main__':
    # Set up command line argument parser
    parser = ArgumentParser(description="Fit formatting before preprocess")
    parser.add_argument('--image_path', type=str, default="../data/obama")
    parser.add_argument('--start_idx', type=int, default=0)
    parser.add_argument('--can_sort', action='store_true')

    args = parser.parse_args()

    if args.can_sort:
        convert_image_name_in_loop(args.image_path, args.start_idx)
    else:
        pad_image_name_in_loop(args.image_path, args.start_idx)