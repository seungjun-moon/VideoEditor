import os
from PIL import Image
import cv2

path1 = '/Users/moonseungjun/Downloads/epsilon/exps_snapshot/snapshot/male-3-casual/hybrid_pixie/visualization/animate+flame/'
path2 = '/Users/moonseungjun/Downloads/next3d/video5/frames'
save_path = 'video1_concat'

image_list1 = sorted(os.listdir(path1))
image_list2 = sorted(os.listdir(path2))

os.makedirs(save_path, exist_ok=True)

def make_mp4(path, fps=30):
    try:
        os.remove(os.path.join(path, '.DS_Store'))
    except:
        pass
    frame_array = []
    for i,file_name in enumerate(sorted(os.listdir(path))):
        img = cv2.imread(os.path.join(path, file_name))
        try:
            height, width, layers = img.shape
        except:
            print(file_name)
            exit()
        size = (width,height)
        frame_array.append(img)
    out = cv2.VideoWriter(path+'.mp4',cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, size)
    for i in range(len(frame_array)):
        out.write(frame_array[i])
    out.release()

for el in image_list1:
	if el[-4:] not in ['.png', '.jpg', 'jpeg']:
		image_list1.remove(el)
		print(el)
		print('remove')

for el in image_list2:
	if el[-4:] not in ['.png', '.jpg', 'jpeg']:
		image_list2.remove(el)
		print(el)
		print('remove')

# print(image_list1)

for i in range(min(len(image_list1), len(image_list2))):
	image= Image.new(mode="RGB", size=(512, 256), color=(255, 255, 255))
	# image1 = Image.open(os.path.join(path1,image_list1[i])).crop((512,0,1024,512)).resize((256,256))
	image1 = Image.open(os.path.join(path1,image_list1[i])).crop((0,0,512,512)).resize((256,256))
	image2 = Image.open(os.path.join(path2,image_list2[i])).resize((256,256))

	image.paste(image1, (0, 0))
	image.paste(image2, (256, 0))

	image.save(os.path.join(save_path, f'{i:05d}.png'))

make_mp4(save_path)