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
        self.global_img_arr = []  # array of all images in folder

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
                    self.global_img_arr.append(arr)
        return self.global_img_arr
    
class SplitArray:
    def __init__(self, global_img_arr, t):
        self.glob_arr = global_img_arr
        self.t = t
        self.g1_arr = []
        self.g2_arr = []
        self.g3_arr = []
        self.split()
    
    def split(self):
        for array in self.glob_arr:
            g1 = []
            g2 = []
            g3 = []

            for i in range(array.shape[0]):  # Loop through rows
                for j in range(array.shape[1]):  # Loop through columns
                    value = array[i, j]
                    if value != 0:
                        if value < self.t[0]:
                            g1.append(value)
                        elif self.t[0] <= value < self.t[1]:
                            g2.append(value)
                        else:
                            g3.append(value)

            self.g1_arr.append(g1)
            self.g2_arr.append(g2)
            self.g3_arr.append(g3)
        return self.g1_arr, self.g2_arr, self.g3_arr
                    
class Linearize:
    def __init__(self, img_arr_arr):
        self.linearized_arr = []
        self.img_arr_arr = img_arr_arr
        
    def linearize_single(self, arr):
        # initialize empty array for linearization of img_array 0 to 255
        linear_arr = np.zeros(256, dtype=int) 
        for i in range(0, len(arr)):
            for j in range(0, len(arr[i])):
                linear_arr[arr[i][j]] += 1
        return linear_arr
    
    def linearize_multi(self):
        for x in self.img_arr_arr:
            linear_arr = self.linearize_single(x)
            self.linearized_arr.append(linear_arr)
        return self.linearized_arr

class Hist:
    def __init__(self, global_img_arr):
        self.global_img_arr = global_img_arr

    def histogram(self, threshold):
        if not self.global_img_arr:
            print("No images to compute histogram.")
            return None
        
        for idx, img in enumerate(self.global_img_arr):
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

            if threshold:
                for t in threshold:
                    plt.axvline(x=t, color='green', linewidth=1)

            plt.show()
        
        print("Histograms plotted")
