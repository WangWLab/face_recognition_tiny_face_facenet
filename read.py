import pickle
import os
import cv2
from concurrent.futures import ThreadPoolExecutor

def read(dest_path, read_threshold, res_path):
    def crop(key, value):
        img = cv2.imread(key)
        for index, item in enumerate(value):
            if item[4] > read_threshold:
                x_start = int(item[1])
                x_end = int(item[3])
                y_start = int(item[0])
                y_end = int(item[2])
                crop_img = cv2.resize(img[x_start:x_end, y_start:y_end], (160, 160))
                cv2.imwrite(os.path.join(dest_path, os.path.splitext(os.path.split(key)[1])[0] + '_' + str(index) + '.jpg'), crop_img)
        print(key + '          done')
    with open(res_path, 'rb') as f:
        res = pickle.load(f)
    with ThreadPoolExecutor(10) as executor:
        for key, value in res.items():
            executor.submit(crop, key, value)