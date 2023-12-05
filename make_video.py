import os
import cv2
import logging
import argparse
import numpy as np

from utils.common import frame_list, video_list

def make_mp4(load_path, save_path, name='video', fps=30):
    frame_array = []
    for i,file_name in enumerate(frame_list(load_path)):

        img = cv2.imread(os.path.join(load_path, file_name))
        height, width, layers = img.shape
        size = (width,height)
        frame_array.append(img)
    save_path = os.path.join(save_path, '{}.mp4'.format(name))
    logging.info('Save video in {}'.format(save_path))
    out = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, size)
    for i in range(len(frame_array)):
        out.write(frame_array[i])
    out.release()

def make_gif(load_path, save_path, name='video', fps=30):
    speed_sec = {'duration':1/fps}
    images=[]
    for i,file_name in enumerate(frame_list(load_path)):
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
    parser.add_argument('--load_path', default='./frames')
    parser.add_argument('--save_path', default='./results')
    parser.add_argument('--fps',       default=60, type=int)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    os.makedirs(args.save_path, exist_ok=True)

    if args.ext == 'mp4':
        make_mp4(args.load_path, args.save_path, 'video', args.fps)
    elif args.ext == 'gif':
        make_gif(args.load_path, args.save_path, 'video', args.fps)