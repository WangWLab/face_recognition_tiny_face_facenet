from imutils import paths
import argparse
import cv2
import sys
import os
import shutil

def split(image_dir, clear_dir, blurry_dir, threshold):
    for image_path in paths.list_images(image_dir):
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fm = cv2.Laplacian(gray, cv2.CV_64F).var()
        if fm > threshold:
            shutil.copy(image_path, os.path.join(clear_dir, os.path.split(image_path)[1]))
        else:
            shutil.copy(image_path, os.path.join(blurry_dir, os.path.split(image_path)[1]))