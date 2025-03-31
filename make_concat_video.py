import os
import cv2
import logging
import argparse
import numpy as np

from pathlib import Path
from utils.common import frame_list, auto_cropping, auto_padding

def make_mp4(load_paths, save_path, name='video', fps=30, reverse=False):
    frame_array = []
    frame_lists = []
    for load_path in load_paths:
        frame_lists.append(frame_list(load_path, reverse=reverse))

    lengths = [len(frames) for frames in frame_lists]
    num_frames = min(lengths)

    print(num_frames)

    num_paths = len(load_paths)
    w=550
    h=802

    for i in range(num_frames-1):
        for j in range(num_paths):
            image_ = cv2.imread(os.path.join(load_paths[j], frame_lists[j][i]))
            image_ = auto_cropping(image_, w, h)
            # image_ = auto_padding(image_, w, h)
            image_ = cv2.resize(image_, (w, h))

            image_ = np.uint8(image_)

            if j ==0:
                image = image_
            else:
                image = cv2.hconcat([image, image_])

        ### letter ###
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_thickness = 2
        text = f'Frame: {i + 1}'
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        text_x = image.shape[1] - text_size[0] - 10  # 오른쪽 끝에서 10px 떨어진 위치
        text_y = 30  # 상단에서 30px 아래 위치
        cv2.putText(image, text, (text_x, text_y), font, font_scale, (255, 0, 0), font_thickness, cv2.LINE_AA)
        ### ######

        cv2.imwrite('./outs/{}.png'.format(str(i).zfill(5)), image)
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
    parser.add_argument('--load_paths', nargs='+')
    parser.add_argument('--save_path', default='./results')
    parser.add_argument('--fps',       default=25, type=int)
    parser.add_argument('--reverse',    action='store_true')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    os.makedirs(args.save_path, exist_ok=True)

    name = Path(args.load_paths[0]).stem

    if args.ext == 'mp4':
        make_mp4(args.load_paths, args.save_path, name, args.fps, args.reverse)
    elif args.ext == 'gif':
        make_gif(args.load_paths, args.save_path, name, args.fps, args.reverse)