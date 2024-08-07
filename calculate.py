# three groups g1, g2, g3
# two thresholds t1, t2
# find min var between groups
# search all possible configurations of the two thresholds
# W_i (i-th group weight) = n_i (i-th group pixel count) / N (total pixel count)
import cv2
from plantcv import plantcv as pcv
import numpy as np
from PIL import Image

class MinVar:
    def __init__(self, px_count):
        self.px_count = px_count # array containing number of pixels of each value
        self.t1 = None
        self.t2 = None
        self.min_var = None

    def calc_mean(self, arr):
        total = 0
        n = sum(arr)
        if n ==0:
            return 0
        else:
            for x in range(len(arr)):
                total += arr[x]*x
            m = total / n
            return m

    def calc_var(self, m, arr):
        sq_diff = 0
        for x in range(len(arr)):
            sq_diff += ((x-m)**2) * arr[x]
        if sum(arr)-1 != 0:
            var = sq_diff / (sum(arr)-1)
        else:
            return 0
        return var

    def calc_wv(self, arr, n_total): # weight multiplied by variance
        if len(arr) != 0:
            m = self.calc_mean(arr)
            v = self.calc_var(m, arr)
            w = sum(arr) / n_total
        else:
            return 0
        return w*v
    
    def calc_intragroup_var(self, t1, t2):
        arr1 = self.px_count[0:t1+1]
        arr2 = self.px_count[t1+1:t2+1]
        arr3 = self.px_count[t2+1:]
        n_total = sum(self.px_count)

        wv1 = self.calc_wv(arr1, n_total)
        wv2 = self.calc_wv(arr2, n_total)
        wv3 = self.calc_wv(arr3, n_total)

        intra_g_var = wv1 + wv2 + wv3
        return intra_g_var
    
    def calc_intragroup_var_single(self, t):
        arr1 = self.px_count[0:t+1]
        arr2 = self.px_count[t+1:]
        n_total = sum(self.px_count)

        wv1 = self.calc_wv(arr1, n_total)
        wv2 = self.calc_wv(arr2, n_total)

        intra_g_var = wv1 + wv2
        return intra_g_var
        
    def find_min_var(self):
        for t1 in range(0, 255):
            for t2 in range(1, 256):
                v = self.calc_intragroup_var(t1, t2)
                if self.min_var == None or self.min_var > v :
                    self.min_var = v
                    self.t1 = t1
                    self.t2 = t2
                    
        print("final")
        print("min var:" + str(self.min_var))
        print("t1: " + str(self.t1))
        print("t2: " + str(self.t2))
        return self.min_var
    
    def find_min_var_single(self):
        for t in range(0, 255):
            v = self.calc_intragroup_var_single(t)
            if self.min_var == None or self.min_var > v :
                self.min_var = v
                self.t1 = t
                    
        print("final")
        print("min var:" + str(self.min_var))
        print("t1: " + str(self.t1))
        return self.min_var



img = cv2.imread('imgs/img.jpg')
shape = img.shape[:2]

img = Image.open('imgs/img.jpg').convert('RGB')
rgb_img = np.array(img)
gray_scale_img = pcv.rgb2gray_lab(rgb_img=rgb_img, channel='a')
img_array = gray_scale_img
# print(img_array)

# initialize empty array for linearization of img_array 0 to 255
linear_arr = np.zeros(256, dtype=int) 
for i in range(0, shape[0]):
    for j in range(0, shape[1]):
        linear_arr[img_array[i][j]] += 1

# print(linear_arr)

mv = MinVar(linear_arr)
mv_value = mv.find_min_var()



# # test with small array
# # px_count = [0, 0, 4, 5, 3, 2, 1, 0]
# px_count = [0, 4, 3, 2, 1, 0,0,0,7,6,5]
# mv = MinVar(px_count)
# print( "individual variance test: " + str(mv.calc_var(3.4, px_count)) )
# mv_value = mv.find_min_var()
