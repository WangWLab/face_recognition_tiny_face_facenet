# -*- coding:UTF-8 -*-
import os
import cv2
import sys

resize_width=500

def CreateDirIfNotExist(path):
    if not os.path.exists(path):
        os.mkdir(path)
        return True
    return False

def extractFrame(videoFile, frameDir, configFilePath, step):
    videoFile = open(videoFile, 'r')
    configFile = open(configFilePath, 'a')
    lines = []
    for line in videoFile.readlines():
        lines.append(line.replace('\n', ''))

    if not os.path.exists(frameDir):
        os.mkdir(frameDir)

    for line in lines:
        if not os.path.exists(line):
            print(line + " not exists")
            exit(-1)

        capture = cv2.VideoCapture(line)
        resize_width = int(capture.get(3)*1.7)
        resize_height = int(capture.get(4)*1.7)

        if not capture.isOpened():
            print("fail to open" + line)
            exit(-1)

        totalFrameNumber = capture.get(7) - 1 
        mediaName = os.path.basename(line)
        framePath = os.path.join(frameDir, os.path.splitext(mediaName)[0])
        if not CreateDirIfNotExist(framePath):
            print("创建视频帧目录[" + mediaName + "]失败，目录已存在")
            exit(-1)

        fps = capture.get(5)  # CV_CAP_PROP_FPS
        if fps is None:
            continue

        configFile.write(mediaName + '\n' + str(fps) + '\n')

        success = True
        idx = 0
        frameCount = 0
        while success:
            success, frame = capture.read()
            if idx % step == 0:
                path = os.path.join(framePath, str(frameCount) + '.jpg')
                size = (resize_width, resize_height)
                dst = cv2.resize(frame, size)
                cv2.imwrite(path, dst)
                frameCount += 1
            idx += 1
        capture.release()
    videoFile.close()
    configFile.close()