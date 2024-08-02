import cv2
import os
from plantcv import plantcv as pcv
import numpy as np
import matplotlib as mpl
from PIL import Image

class read_images:
    def __init__(self, folderpath):
        self.folderpath = folderpath
        self.img_array = [] # array of image
        self.img_array_array = [] # array of all images in folder

    def img_to_arr(self, filepath):
        img = Image.open(filepath)
        gray_scale_img = pcv.rgb2gray_lab(rgb_img=img, channel ='a')
        self.img_array.append(np.array(gray_scale_img))
        gray_scale_img_conc = np.concatenate(gray_scale_img)
        self.img_array = np.array(gray_scale_img_conc, dtype='int64')

    def read_folder(self):
        for filename in os.listdir(self.folderpath):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                filepath = os.path.join(self.folderpath, filename)
                arr = self.img_to_arr(filepath)
                self.img.array_array.append(arr)
