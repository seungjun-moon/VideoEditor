import os
import cv2
import logging
import argparse

def make_frames(video_file, save_path, name=''):
    vidcap = cv2.VideoCapture(video_file)
    success,image = vidcap.read()
    count = 0
    success = True
    if name == '':
        name = 'frame'
    while success:
      success,image = vidcap.read()
      cv2.imwrite(os.path.join(save_path, '{}_{}.png'.format(name, str(count).zfill(4))), image)
      if cv2.waitKey(10) == 27:
          break
      count += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a video')
    parser.add_argument('--video_file', default='deca.mp4')
    parser.add_argument('--save_path',  default='./frames')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    os.makedirs(args.save_path, exist_ok=True)

    make_frames(args.video_file, args.save_path, name='frame')