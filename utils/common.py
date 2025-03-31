import os
import cv2
import numpy as np

def list_with_exts(files, ext_list):
    files_with_exts = []
    for file in files:
        _, ext = os.path.splitext(file)
        if ext in ext_list:
            files_with_exts.append(file)

    return files_with_exts

def frame_list(path, sort=True, reverse=False):
    files  = os.listdir(path)
    frames = list_with_exts(files, ['.png','.jpg','.jpeg'])

    if sort:
        frames = sorted(frames)
    if reverse:
        frames.reverse()
    return frames

def video_list(path, sort=True):
    files  = os.listdir(path)
    videos = list_with_exts(files, ['.mp4'])

    if sort:
        videos = sorted(videos)
    return videos

def auto_cropping(image, w, h):
    h_orig, w_orig, _ = image.shape

    if w_orig/w <= h_orig/h:
        w_new = w_orig
        h_new = int((w_orig * h/w)//1)

    elif w_orig/w > h_orig/h:
        h_new = h_orig
        w_new = int((h_orig * w/h)//1)

    cropped_image = image[h_orig//2-h_new//2:h_orig//2+h_new//2, w_orig//2-w_new//2:w_orig//2+w_new//2]

    return cropped_image

def auto_padding(image, w, h):
    h_orig, w_orig, _ = image.shape

    if w_orig/w <= h_orig/h:
        h_new = h_orig
        w_new = int((h_orig * w/h)//1)

    elif w_orig/w > h_orig/h:
        w_new = w_orig
        h_new = int((w_orig * h/w)//1)

    new_image = np.zeros((h_new, w_new, 3))

    new_image[h_new//2-h_orig//2:h_new//2+h_orig//2, w_new//2-w_orig//2:w_new//2+w_orig//2] = cv2.resize(image, (w_orig, h_orig))

    return new_image


