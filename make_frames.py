import os
import cv2
import numpy as np
import logging
import argparse

def make_frames(video_file, save_path, name='', hdr=False, crop=False, hop=1):
    vidcap = cv2.VideoCapture(video_file)
    success,image = vidcap.read()
    if hdr:
        unchanged_image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    count = 0
    success = True
    if name == '':
        name = 'frame'
    while success:
        success,image = vidcap.read()

        if count % hop == 0:
            if not crop:
                cv2.imwrite(os.path.join(save_path, '{}_{}.png'.format(name, str(count).zfill(4))), image)
            if crop:
                image = crop_image(image)
                cv2.imwrite(os.path.join(save_path, '{}_{}.png'.format(name, str(count).zfill(4))), image)
        else:
            count += 1
            continue
        if cv2.waitKey(10) == 27:
            break
        count += 1

def crop_image(image, scale=(512,512)):
    img = image
    # h, w = 350, 700   # view_000
    # size = (1200,1200) # view_000

    # h, w = 400, 800   # view_001
    # size = (1200,1200) # view_001

    # h, w = 450, 1200   # view_002
    # size = (1200,1200) # view_002

    # h, w = 500, 900   # view_003
    # size = (1200,1200) # view_003

    # h, w = 400, 1200   # view_004
    # size = (1200,1200) # view_004

    # h, w = 400, 1250   # view_005
    # size = (1200,1200) # view_005

    # h, w = 300, 1000   # view_006
    # size = (1250,1250) # view_006

    # h, w = 400, 1500   # view_007
    # size = (1050,1050) # view_007

    # h, w = 700, 1100   # view_008
    # size = (1200,1200) # view_008

    # h, w = 700, 950   # view_009
    # size = (1200,1200) # view_009 Not Working

    # h, w = 200, 1200   # view_010
    # size = (1250,1250) # view_010

    # h, w = 200, 1000   # view_011
    # size = (1250,1250) # view_011

    # h, w = 350, 1250   # view_012
    # size = (1250,1250) # view_012

    # h, w = 250, 1100   # view_013
    # size = (1250,1250) # view_013

    # h, w = 250, 1100   # view_014
    # size = (1150,1150) # view_014

    h, w = 700, 150   # view_015
    size = (800,800) # view_015

    # h,w=300,700      # mesh
    # size = (500,500) # mesh

    cropped_img = img[h:h+size[0],w:w+size[1]]
    img_ = np.zeros((size[0],size[1],3))

    img_[size[0]//2-cropped_img.shape[0]//2:size[0]//2+cropped_img.shape[0]//2,
         size[1]//2-cropped_img.shape[1]//2:size[1]//2+cropped_img.shape[1]//2] = cropped_img

    img_ = cv2.resize(img_, scale)

    return img_

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a video')
    parser.add_argument('--video_file', default='deca.mp4')
    parser.add_argument('--save_path',  default='./frames')
    parser.add_argument('--hdr',  action='store_true')
    parser.add_argument('--crop',  action='store_true')
    parser.add_argument('--hop', type=int, default=1)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    os.makedirs(args.save_path, exist_ok=True)

    make_frames(args.video_file, args.save_path, name='frame', hdr=args.hdr, crop=args.crop, hop=args.hop)