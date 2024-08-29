import random
import numpy as np
import matplotlib.pyplot as plt

class GenerateData:
    def __init__(self):
        self.generated_data = [0] * 256

    def insert_hill(self, h, w, x, randomness): # h = height of hill, w = width of hill, x = position of hill
        if 0 > x > 255 or 0 > w > 255:
            print("value out of range!")
            return ValueError
        
        # generate left side
        i = x - w/2
        j = x
        k = h
        
        while j >= 0 and j >= i:
            self.generated_data[j] = max(0, k + random.randint(-randomness, randomness))
            j -= 1
            k = max(0, int(k / 1.5))

        # generate right side
        i = x + w/2
        j = x + 1
        k = h//2

        while j < 256 and j < i:
            self.generated_data[j] = max(0, k + random.randint(-randomness, randomness))
            j += 1
            k = max(0, int(k / 1.5))

        pixel_array = np.array(self.generated_data, dtype=np.float32)
        pixel_array = pixel_array.astype(np.uint8)

        return pixel_array

    def insert_noise(self, h, lb, ub): # h = max height of noise
        if lb < 0 or ub > 255 or lb > ub:
            print("Value out of range!")
            return ValueError
        
        for i in range(lb, ub):
            self.generated_data[i] += random.randint(0, h)

class Hist:
    def __init__(self, global_img_arr):
        # Ensure global_img_arr is a list of histograms
        if isinstance(global_img_arr, np.ndarray):
            self.global_img_arr = [global_img_arr]
        else:
            self.global_img_arr = global_img_arr

    def histogram(self, threshold):
        if not isinstance(self.global_img_arr, list):
            print("global_img_arr should be a list of histograms")
            return None
        
        for idx, hist in enumerate(self.global_img_arr):
            # Check if histogram data is valid
            if hist is None or len(hist) != 256:
                print(f"Histogram {idx + 1} is empty or not valid.")
                continue
            
            # Print histogram stats
            print(f"Histogram for Image {idx + 1}:")
            print(f"Min: {np.min(hist)}, Max: {np.max(hist)}")
            
            # Plot histogram
            plt.figure()
            plt.bar(range(256), hist, width=1.0, edgecolor='black')
            plt.title(f"Histogram for Image {idx + 1}")
            plt.xlabel("Pixel Value")
            plt.ylabel("Frequency")

            # Draw threshold(s)
            if threshold:
                if isinstance(threshold, list):
                    for t in threshold:
                        plt.axvline(x=t, color='green', linewidth=1)
                else: 
                    plt.axvline(x=threshold, color='green', linewidth=1)

            plt.show()

arr = GenerateData()
generated_arr = arr.insert_hill(150, 50, 60, 5)
generated_arr = arr.insert_hill(100, 60, 150, 3)

histogram = Hist(generated_arr)
histogram.histogram(False)
