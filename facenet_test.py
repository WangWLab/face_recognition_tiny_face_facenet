import cv2
import facenet
import numpy as np
import tensorflow as tf
import os
import shutil
from scipy import misc

recognized_dir = 'D:\\Programs\\face_datection\\dataset\\result_1.7_10_recognized'
detected_dir = 'D:\\Programs\\face_datection\\dataset\\result_1.7_10_face_clear'
model_path = '.\\resource\\200408-102900\\2018180408-102900.pb'
def load_and_prepro_data(paths):
    img_list = list()
    for item in paths:
        img = misc.imread(item, mode='RGB')
        img_list.append(facenet.prewhiten(img))
    images = np.stack(img_list)
    return images


def main(recognized_dir, detected_dir, model_path, threshold):
    detected_path = [os.path.join(detected_dir, item) for item in os.listdir(detected_dir)]
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    with tf.Graph().as_default():
        with tf.Session(config=config) as sess:
            facenet.load_model(model_path)
            images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
            for item in detected_path:
                counter = 0
                flag = True
                if len(os.listdir(recognized_dir)) == 0:
                    shutil.copy(item, os.path.join(recognized_dir, os.path.split(item)[1]))
                    continue
                for face in [os.path.join(recognized_dir, item) for item in os.listdir(recognized_dir)]:
                    images = load_and_prepro_data([item, face])
                    feed_dict = {images_placeholder: images, phase_train_placeholder: False}
                    emb = sess.run(embeddings, feed_dict=feed_dict)
                    dist = np.sqrt(np.sum(np.square(np.subtract(emb[0, :], emb[1, :]))))
                    if dist <= threshold:
                        # counter += 1
                        flag = False
                if flag:
                    shutil.copy(item, os.path.join(recognized_dir, os.path.split(item)[1]))
                #     if dist < 1:
                #         flag = False
                # if counter < 1 and flag:
                #     shutil.copy(item, os.path.join(recognized_dir, os.path.split(item)[1]))
                print(item+'             done')


if __name__ == '__main__':
    # main(recognized_dir, detected_dir, model_path, threshold)
    detected_dir = ['D:\\Programs\\face_datection\\dataset\\result_1.7_10_face_clear', 'D:\\Programs\\face_datection\\dataset\\result_1.7_10_face_blurry']
    cata = ['clear', 'blurry']
    threshold = [1, 1.1]
    for index, dir in enumerate(detected_dir):
        for thre in threshold:
            recognized_dir = 'D:\\Programs\\face_datection\\dataset\\result_1.7_10_recognition_' + cata[index] + '_' + str(thre)
            if not os.path.exists(recognized_dir):
                os.mkdir(recognized_dir)
            main(recognized_dir, dir, model_path, thre)
