import numpy as np
from read_imgs import SplitArray, ReadImages
from multiprocessing import Pool

class InterVarianceOfMeans:
    def __init__(self, g, g1, g2, g3):
        if g is not None and len(g) > 0:
            self.global_mean = np.mean(g)
        else:
            self.global_mean = 0
        
        self.g1_mean = [np.mean(i) for i in g1 if i is not None and len(i) > 0]
        self.g2_mean = [np.mean(i) for i in g2 if i is not None and len(i) > 0]
        self.g3_mean = [np.mean(i) for i in g3 if i is not None and len(i) > 0]
        
        self.m = 0

    def calc(self):
        self.m += sum( (i - self.global_mean)**2 for i in self.g1_mean )
        self.m += sum( (i - self.global_mean)**2 for i in self.g2_mean )
        self.m += sum( (i - self.global_mean)**2 for i in self.g3_mean )
        return self.m

class IntraVariance:
    def __init__(self, g1, g2, g3):
        self.g1 = g1
        self.g2 = g2
        self.g3 = g3

    def calc_f(self):
        f = 0
        for i in range(len(self.g1)):
            n = len(self.g1[i]) + len(self.g2[i]) + len(self.g3[i])
            if n != 0:
                f += self.calc_var(self.g1[i], n)
                f += self.calc_var(self.g2[i], n)
                f += self.calc_var(self.g3[i], n)
        return f
    
    def calc_var(self, arr, n):
        if arr is not None and len(arr) > 0:
            return (len(arr)/n) * np.var(arr)
        else: return 0
    
# class FindThresh:
#     def __init__(self, g):
#         self.g = g
#         self.min_g = None
#         self.min_t = None

#     def find_thresh(self):
#         for t1 in range(0, 256):
#             print(f"t1: {t1}")
#             for t2 in range(t1, 256):
#                 split = SplitArray(self.g, [t1, t2])
#                 g1, g2, g3 = split.g1_arr, split.g2_arr, split.g3_arr
#                 g = 0
#                 inter_var = InterVarianceOfMeans(self.g, g1, g2, g3)
#                 g += inter_var.calc()
#                 intra_var = IntraVariance(g1, g2, g3)
#                 g += intra_var.calc_f()

#                 if self.min_g == None or self.min_g > g:
#                     self.min_g = g
#                     self.min_t = [t1, t2]
#         return self.min_t

folder_path = "imgs"
reader = ReadImages(folder_path)
images_array = reader.read_folder()
t = [50, 120]
split = SplitArray(images_array, t)
g1, g2, g3 = split.g1_arr, split.g2_arr, split.g3_arr

m = InterVarianceOfMeans(images_array, g1, g2, g3)
inter_var = m.calc()

f = IntraVariance(g1, g2, g3)
intra_var = f.calc_f()

x = FindThresh(images_array)
thresh = x.find_thresh()
print(thresh)
