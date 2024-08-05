# three groups g1, g2, g3
# two thresholds t1, t2
# find min var between groups
# search all possible configurations of the two thresholds
# W_i (i-th group weight) = n_i (i-th group pixel count) / N (total pixel count)
from plantcv import plantcv as pcv
import numpy as np
from PIL import Image

class MinVar:
    def __init__(self, px_count):
        self.px_count = px_count # array containing number of pixels of each value
        self.t1 = None
        self.t2 = None
        self.min_var = None

    def calc_var(self, m, arr):
        sq_diff = 0
        for x in range(len(arr)):
            sq_diff += ((x-m)**2) * arr[x]
        if sum(arr) != 0:
            var = sq_diff / sum(arr)
        else:
            var = 0
        return var
    
    def calc_intragroup_var(self, t1, t2):
        arr1 = self.px_count[0:t1+1]
        arr2 = self.px_count[t1:t2+1]
        arr3 = self.px_count[t2:256]
        n_total = sum(self.px_count)

        m1 = np.mean(arr1)
        v1 = self.calc_var(m1, arr1)
        w1 = sum(arr1) / n_total

        m2 = np.mean(arr2)
        v2 = self.calc_var(m2, arr2)
        w2 = sum(arr2) / n_total

        m3 = np.mean(arr3)
        v3 = self.calc_var(m3, arr3)
        w3 = sum(arr3) / n_total

        intra_g_var = (w1*(v1**2)) + (w2*(v2**2)) + (w3*(v3**2))
        return intra_g_var
        
    def find_min_var(self):
        for t1 in range(0, 255):
            for t2 in range(0, 255):
                v = self.calc_intragroup_var(t1, t2)
                if self.min_var == None or self.min_var > v :
                    self.min_var = v
        print(self.min_var)
        return self.min_var

px_count = [0, 0, 4, 5, 6, 8, 3, 0]
mv = MinVar(px_count)
mv_value = mv.find_min_var()
print(mv_value)

#img = cv2.imread('imgs/img.jpg')

# img = Image.open('imgs/img.jpg').convert('RGB')
# rgb_img = np.array(img)
# gray_scale_img = pcv.rgb2gray_lab(rgb_img=rgb_img, channel='a')
# img_array = gray_scale_img
# shape = img.shape[:2]
# print(img_array)
# for i in range(0, shape[0]):
#     for j in range(0, shape[1]):
