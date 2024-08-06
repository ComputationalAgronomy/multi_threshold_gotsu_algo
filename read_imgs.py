import cv2
import os
from plantcv import plantcv as pcv
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

class ReadImages:
    def __init__(self, folderpath):
        self.folderpath = folderpath
        self.img_array = []  # array of single image
        self.img_array_array = []  # array of all images in folder

    def img_to_arr(self, filepath):
        try:
            img = Image.open(filepath).convert('RGB')
            rgb_img = np.array(img)
            gray_scale_img = pcv.rgb2gray_lab(rgb_img=rgb_img, channel='a')
            self.img_array = gray_scale_img
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

class Hist:
    def __init__(self, img_array_array):
        self.img_array_array = img_array_array

    def histogram(self):
        if not self.img_array_array:
            print("No images to compute histogram.")
            return None
        
        for idx, img in enumerate(self.img_array_array):
            # Ensure image data is valid
            if img is None or img.size == 0:
                print(f"Image {idx + 1} is empty or not valid.")
                continue
            
            print(f"Processing Image {idx + 1} with shape {img.shape}")
            
            # Compute histogram
            hist = cv2.calcHist([img], [0], None, [256], [0, 256])
            hist_flat = hist.flatten()
            
            # Print histogram stats
            print(f"Histogram for Image {idx + 1}:")
            print(f"Min: {np.min(hist_flat)}, Max: {np.max(hist_flat)}")
            
            # Plot histogram
            plt.figure()
            plt.bar(range(256), hist_flat, width=1.0, edgecolor='black')
            plt.title(f"Histogram for Image {idx + 1}")
            plt.xlabel("Pixel Value")
            plt.ylabel("Frequency")
            plt.show()
        
        print("Histograms plotted")
        return

folder_path = "imgs"
reader = ReadImages(folder_path)
images_array = reader.read_folder()

print(f"Number of images read: {len(images_array)}")
if images_array:
    print(f"Shape of the first image array: {images_array[0].shape}")

histogram = Hist(images_array)
histogram.histogram()
