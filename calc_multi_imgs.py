# calculate the threshold variance of multiple images

from read_imgs import ReadImages, Linearize
from calculate import MinVar

class Multi_MinVar:
    def __init__(self, lin_arr):
        self.thresholds = [] # [ [t11, t21], [t12, t22], [t13, t23], ...]
        self.lin_arr = lin_arr
    
    def multi_minvar(self):
        for arr in self.lin_arr:
            threshold = MinVar(arr).find_threshold()
            self.thresholds.append(threshold)
        print(self.thresholds)
        return self.thresholds
    
    def __str__(self):
        return f'Thresholds: {self.thresholds}'

folder_path = "imgs"
reader = ReadImages(folder_path)
images_array = reader.read_folder()

lin_arr = Linearize(images_array).linearize_multi()

multi = Multi_MinVar(lin_arr)
thresholds = multi.multi_minvar()

print(thresholds)
