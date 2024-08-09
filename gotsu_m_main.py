from read_imgs import ReadImages, Linearize
from gotsu_m import M_Gotsu


folder_path = "imgs"
reader = ReadImages(folder_path)
images_array = reader.read_folder()

lin_arr = Linearize(images_array).linearize_multi()

multi = M_Gotsu(lin_arr)
thresholds = multi.find_thresh()

print(thresholds)
