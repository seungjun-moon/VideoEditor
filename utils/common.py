import os

def list_with_exts(files, ext_list):
    files_with_exts = []
    for file in files:
        _, ext = os.path.splitext(file)
        if ext in ext_list:
            files_with_exts.append(file)

    return files_with_exts

def frame_list(path, sort=True):
    files  = os.listdir(path)
    frames = list_with_exts(files, ['.png','.jpg','.jpeg'])

    if sort:
        frames = sorted(frames)
    return frames

def video_list(path, sort=True):
    files  = os.listdir(path)
    videos = list_with_exts(files, ['.mp4'])

    if sort:
        videos = sorted(videos)
    return videos