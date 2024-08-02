import math
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

threshold_values = {}

def Hist(img, op_thres=None):
    row, col = img.shape 
    y = np.zeros(256)
    for i in range(0, row):
        for j in range(0, col):
            y[img[i, j]] += 1
    x = np.arange(0, 256)
    plt.bar(x, y, color='b', width=5, align='center', alpha=0.25)
    if op_thres is not None:
        plt.axvline(x=op_thres, color='r', linestyle='--', label=f'Threshold = {op_thres}')
        plt.legend()
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    plt.title('Histogram with Optimal Threshold')
    plt.show()
    return y

def regenerate_img(img, threshold):
    row, col = img.shape 
    y = np.zeros((row, col))
    for i in range(0, row):
        for j in range(0, col):
            y[i, j] = 255 if img[i, j] >= threshold else 0
    return y

def countPixel(h):
    return sum(h[i] for i in range(len(h)) if h[i] > 0)

def wieght(s, e):
    return sum(h[i] for i in range(s, e))

def mean(s, e):
    w = wieght(s, e)
    if w == 0:
        return 0
    return sum(h[i] * i for i in range(s, e)) / float(w)

def variance(s, e):
    m = mean(s, e)
    w = wieght(s, e)
    if w == 0:
        return 0
    return sum(((i - m) ** 2) * h[i] for i in range(s, e)) / w

def threshold(h):
    cnt = countPixel(h)
    for i in range(1, len(h)):
        vb = variance(0, i)
        wb = wieght(0, i) / float(cnt)
        mb = mean(0, i)
        
        vf = variance(i, len(h))
        wf = wieght(i, len(h)) / float(cnt)
        mf = mean(i, len(h))
        
        V2w = wb * vb + wf * vf
        V2b = wb * wf * (mb - mf) ** 2
        
        if not math.isnan(V2w):
            threshold_values[i] = V2w

def get_optimal_threshold():
    min_V2w = min(threshold_values.values())
    optimal_threshold = [k for k, v in threshold_values.items() if v == min_V2w]
    print('Optimal threshold:', optimal_threshold[0])
    return optimal_threshold[0]

image = Image.open('img2.jpg').convert("L")
img = np.asarray(image)

# Calculate histogram and threshold
h = Hist(img)
threshold(h)
op_thres = get_optimal_threshold()

# Plot histogram with the optimal threshold
Hist(img, op_thres)

# Generate and save the binary image
res = regenerate_img(img, op_thres)
plt.imshow(res, cmap='gray')
plt.title('Thresholded Image')
plt.savefig("otsu.jpg")
plt.show()
