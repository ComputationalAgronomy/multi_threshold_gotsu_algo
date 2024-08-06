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

    def calc_var(self, m, arr):
        sq_diff = 0
        for x in range(len(arr)):
            sq_diff += ((x-m)**2) * arr[x]
        if sum(arr)-1 != 0:
            var = sq_diff / (sum(arr)-1)
        else:
            var = 0
        return var
    
    def calc_intragroup_var(self, t1, t2):
        arr1 = self.px_count[0:t1+1]
        arr2 = self.px_count[t1+1:t2+1]
        arr3 = self.px_count[t2+1:]
        n_total = sum(self.px_count)

        print(f"t1 = {t1}, t2 = {t2}")
        print(f"arr1: {arr1}")
        print(f"arr2: {arr2}")
        print(f"arr3: {arr3}")

        if len(arr1) != 0:
            m1 = np.mean(arr1)
            v1 = self.calc_var(m1, arr1)
            w1 = sum(arr1) / n_total
        else:
            v1 = 0
            w1 = 0

        if len(arr2) != 0:
            m2 = np.mean(arr2)
            v2 = self.calc_var(m2, arr2)
            w2 = sum(arr2) / n_total
        else:
            v2 = 0
            w2 = 0

        if len(arr3) != 0:
            m3 = np.mean(arr3)
            v3 = self.calc_var(m3, arr3)
            w3 = sum(arr3) / n_total
        else:
            v3 = 0
            w3 = 0

        intra_g_var = (w1*v1) + (w2*v2) + (w3*v3)
        return intra_g_var
        
    def find_min_var(self):
        for t1 in range(0, 10):
            for t2 in range(1, 11):
                v = self.calc_intragroup_var(t1, t2)
                print(f"Evaluating t1 = {t1}, t2 = {t2}, var = {v}")  # Debugging print statement
                if self.min_var == None or self.min_var > v :
                    self.min_var = v
                    self.t1 = t1
                    self.t2 = t2
                    print("min var:" + str(self.min_var))
                    print("t1: " + str(self.t1))
                    print("t2: " + str(self.t2))
                    print("------")
        print("final")
        print("min var:" + str(self.min_var))
        print("t1: " + str(self.t1))
        print("t2: " + str(self.t2))
        return self.min_var



# img = cv2.imread('imgs/3.jpg')
# shape = img.shape[:2]

# img = Image.open('imgs/3.jpg').convert('RGB')
# rgb_img = np.array(img)
# gray_scale_img = pcv.rgb2gray_lab(rgb_img=rgb_img, channel='a')
# img_array = gray_scale_img
# # print(img_array)

# # initialize empty array for linearization of img_array 0 to 255
# linear_arr = np.zeros(256, dtype=int) 
# for i in range(0, shape[0]):
#     for j in range(0, shape[1]):
#         linear_arr[img_array[i][j]] += 1

# # print(linear_arr)

# mv = MinVar(linear_arr)
# mv_value = mv.find_min_var()




# test with small array
# px_count = [0, 0, 4, 5, 3, 2, 1, 0]
px_count = [0, 4, 3, 2, 1, 0]
mv = MinVar(px_count)
print( "individual variance test: " + str(mv.calc_var(3.4, px_count)) )
mv_value = mv.find_min_var()
