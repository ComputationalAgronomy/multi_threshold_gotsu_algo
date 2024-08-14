from read_imgs import ReadImages, Linearize, Hist
from gotsu_m import M_Gotsu
from segment import Segment


folder_path = "imgs"
reader = ReadImages(folder_path)
images_array = reader.read_folder()

lin_arr = Linearize(images_array).linearize_multi()

multi = M_Gotsu(lin_arr)
thresholds = multi.find_thresh()

print(thresholds)

Segment(thresholds, images_array, 1)

histogram = Hist(images_array)
histogram.histogram(thresholds)
