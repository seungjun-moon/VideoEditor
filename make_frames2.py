import os
import cv2
import numpy as np
import logging
import argparse
from tqdm import tqdm

from utils.bdy_dict import boundary

def make_frames(video_file, save_path, name='', hdr=False, crop=False, hop=1, cut=0):
    actor = os.path.splitext(os.path.basename(video_file))[0]
    if actor in boundary.keys():
        cut = boundary[actor]['cut']
        hop = boundary[actor]['hop']
    vidcap = cv2.VideoCapture(video_file)
    success,image = vidcap.read()
    if hdr:
        unchanged_image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    count = 0
    success = True
    if name == '':
        name = 'frame'
    while success:
        print(count)
        success,image = vidcap.read()

        valid=[]

        if len(valid) > 1:
            
            offset = 0

            valid = [i+offset for i in valid]

            if count not in valid:
                count += 1
                continue

        if count % hop == 0 and count > cut:
            if crop:
                image = crop_image(image=image, actor=actor)
            cv2.imwrite(os.path.join(save_path, '{}_{}.png'.format(name, str(count).zfill(5))), image)
        else:
            count += 1
            continue
        if cv2.waitKey(10) == 27:
            break
        count += 1

def crop_image(image, scale=(550,802), actor=None):
    img = image

    s = scale[1]/scale[0]

    try:
        h,w,size = boundary[actor]['h'], boundary[actor]['w'], boundary[actor]['size']

    except:

        # h, w = 450, 1400   # view_009
        # size = 1150 # view_009 Not Working

        # h, w = 100, 1400   # view_010
        # size = 1150 # view_010

        # h, w = 100, 1150   # view_011
        # size = 1250 # view_011

        # h, w = 400, 1350   # view_012
        # size = 1200 # view_012

        # h, w = 400, 1100   # view_012
        # size = 1300 # view_012

        # h, w = 300, 1250   # view_013
        # size = 1300 # view_013

        # h, w = 100, 900   # view_014
        # size = 1200 # view_014

        # h, w = 0, 900   # view_015
        # size = 1200 # view_015

        # h, w= 750, 200 # 4K
        # size=1800 #4K

        # h, w= 1100, 500 # 4K
        # size=1200 #4K

        # h, w= 850, 300 # 4K
        # size=1500 #4K

        # h, w= 550, 100 # sjmoon_014
        # size=2000 # sjmoon_014

        # h,w = 600,50
        # size=2100

        # h,w = 200,0
        # size=1000

        # ratio = 0.75
        # margin = (1-ratio)/2
        # h,w = int((802 * margin)//1) ,int((550 * margin)//1)
        # size= int((550 * ratio)//1)

        # print(h, w, size)

        h,w = 35,110
        size= 2000


    s2 = int((size*s)//1)

    assert h+s2 < img.shape[0],   '{} {}'.format(h+s2, img.shape[0])
    assert w+size < img.shape[1], '{} {}'.format(w+size, img.shape[1])

    cropped_img = img[h:h+s2,w:w+size]
    img_ = np.zeros((s2,size,3))

    # print(s * size + h, img.shape)

    h = min(h, img.shape[0] - s * size - 1)
    w = min(w, img.shape[1] - size - 1)

    # img_[s2//2-cropped_img.shape[0]//2:s2//2+cropped_img.shape[0]//2,
    #      size//2-cropped_img.shape[1]//2:size//2+cropped_img.shape[1]//2] = cropped_img

    img_ = cropped_img

    img_ = cv2.resize(img_, scale)

    return img_

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a video')
    parser.add_argument('--video_file', default='deca.mp4')
    parser.add_argument('--save_path',  default='./frames')
    parser.add_argument('--hdr',   action='store_true')
    parser.add_argument('--crop',  action='store_true')
    parser.add_argument('--hop',   type=int, default=1)
    parser.add_argument('--cut',   type=int, default=-1)
    parser.add_argument('--actor', type=int, default=None)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    os.makedirs(args.save_path, exist_ok=True)

    make_frames(args.video_file, args.save_path, name='frame', hdr=args.hdr, crop=args.crop, hop=args.hop, cut=args.cut)