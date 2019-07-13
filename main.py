import tiny_face_eval
import read
import facenet_test
import video_shot
import split_blurry
import time


face_dest_path = '.\\face'
res_path = 'resource\\res.pkl'
recognized_dir = '.\\face_recognized'
model_path = '.\\resource\\20180408-102900\\20180408-102900.pb'
clear_dir = '.\\face_clear'
blurry_dir = '.\\face_blurry'
tiny_face_weight_file = '.\\resource\\hr_res101_pickle.pkl'
split_threshold = 30
read_threshold = 8
facenet_threshold = 1
detected_dir = face_dest_path
step = 10

if __name__ == '__main__':
    video_shot.extractFrame('list.txt', 'frame', 'config\\config.txt', step = step)
    print('抽帧已完成， 开始计时')
    start = time.time()
    tiny_face_eval.call(tiny_face_weight_file, 'frame\\video', 'face', 'resource', res_path)
    print('人脸检测已完成')
    read.read(face_dest_path, read_threshold, res_path)
    print('人脸区域分割已完成')
    # split_blurry.split(face_dest_path, clear_dir, blurry_dir, split_threshold)
    facenet_test.main(recognized_dir, detected_dir, model_path, facenet_threshold)
    end = time.time()
    print('人脸识别已完成，用时共%d秒', (end-start)/60)
