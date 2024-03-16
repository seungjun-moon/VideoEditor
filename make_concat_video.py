import os
import cv2
import logging
import argparse
import numpy as np

from pathlib import Path
from utils.common import frame_list, video_list

def make_mp4(load_paths, save_path, name='video', fps=30, reverse=False):
    frame_array = []
    frame_lists = []
    for load_path in load_paths:
        frame_lists.append(frame_list(load_path, reverse=reverse))

    num_paths = len(load_paths)
    size=512

    for i in range(len(frame_lists[0])):
        for j in range(num_paths):
            image_ = cv2.imread(os.path.join(load_paths[j], frame_lists[j][i]))
            image_ = cv2.resize(image_, (size, size))
            if j ==0:
                image = image_
            else:
                image = cv2.hconcat([image, image_])
        frame_array.append(image)
        height, width, layers = image.shape
        shape = (width,height)
    save_path = os.path.join(save_path, '{}.mp4'.format(name))
    logging.info('Save video in {}'.format(save_path))
    out = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, shape)
    for i in range(len(frame_array)):
        out.write(frame_array[i])
    out.release()

def make_gif(load_path, save_path, name='video', fps=30, reverse=False):
    speed_sec = {'duration':1/fps}
    images=[]
    for i,file_name in enumerate(frame_list(load_path, reverse=reverse)):
        file_path = os.path.join(load_path, file_name)
        images.append(imageio.imread(file_path))
        if i > 500:
            break

    save_path = os.path.join(save_path, '{}.gif'.format(name))
    logging.info('Save video in {}'.format(save_path))
    imageio.mimsave(save_path, images, **speed_sec)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a video')
    parser.add_argument('--ext',       default='mp4')
    parser.add_argument('--load_paths', default='./frames,./frames')
    parser.add_argument('--save_path', default='./results')
    parser.add_argument('--fps',       default=60, type=int)
    parser.add_argument('--reverse',    action='store_true')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    os.makedirs(args.save_path, exist_ok=True)

    load_paths = args.load_paths.split(',')
    name = Path(load_paths[0]).stem

    if args.ext == 'mp4':
        make_mp4(load_paths, args.save_path, name, args.fps, args.reverse)
    elif args.ext == 'gif':
        make_gif(load_paths, args.save_path, name, args.fps, args.reverse)