import os
import cv2
import logging
import argparse
import numpy as np

from utils.common import frame_list, video_list

def crop_images(img_path, size=(1080,1080)):
    img = cv2.imread(img_path)
    h = 100
    w = 0
    cropped_img = img[h:h+size[0],w:w+size[1]]
    img_ = np.zeros((size[0],size[1],3))

    img_[size[0]//2-cropped_img.shape[0]//2:size[0]//2+cropped_img.shape[0]//2,
         size[1]//2-cropped_img.shape[1]//2:size[1]//2+cropped_img.shape[1]//2] = cropped_img

    return img_


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fit the frame size')
    parser.add_argument('--load_path', default='./seungeun')
    parser.add_argument('--save_path', default='./seungeun_cropped')
    parser.add_argument('--fps',       default=60, type=int)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    os.makedirs(args.save_path, exist_ok=True)

    frames = frame_list(args.load_path)

    for frame in frames:
        img = crop_images(os.path.join(args.load_path, frame))
        cv2.imwrite(os.path.join(args.save_path, frame),img)