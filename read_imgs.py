import cv2
import os
from plantcv import plantcv as pcv
import numpy as np
import matplotlib as mpl
from PIL import Image

class ReadImages:
    def __init__(self, folderpath):
        self.folderpath = folderpath
        self.img_array = [] # array of single image
        self.img_array_array = [] # array of all images in folder

    def img_to_arr(self, filepath):
        try:
            img = Image.open(filepath).convert('RGB')
            rgb_img = np.array(img)
            gray_scale_img = pcv.rgb2gray_lab(rgb_img=rgb_img, channel='a')
            return gray_scale_img
        except (IOError) as e:
            print(f"Error opening image {filepath}: {e}")
            return None

    def read_folder(self):
        for filename in os.listdir(self.folderpath):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                filepath = os.path.join(self.folderpath, filename)
                arr = self.img_to_arr(filepath)
                if arr is not None:
                    self.img_array_array.append(arr)
        return self.img_array_array
    
class Hist(ReadImages):
    def histogram(self):
        img = self. 
folder_path = "imgs"
reader = ReadImages(folder_path)
images_array = reader.read_folder()

print(f"Number of images read: {len(images_array)}")
if images_array:
    print(f"Shape of the first image array: {images_array[0].shape}")
