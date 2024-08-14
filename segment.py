import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

class Segment:
    def __init__(self, t, img_arr, group):
        self.g = group  # set group 0, 1, 2 as foreground
        self.t = t
        self.arr = img_arr
        self.img = []
        self.set_foreground()
        self.convert_to_img_and_show()

    def set_foreground(self):
        # Initialize a list to store segmented images
        self.img = []
        
        # Apply thresholding based on the group
        for idx, img in enumerate(self.arr):
            if self.g == 0:
                # Set pixels less than t[0] to 255 (white), otherwise 0 (black)
                segmented_img = np.where(img < self.t[0], 255, 0).astype(np.uint8)
            elif self.g == 1:
                # Set pixels between t[0] and t[1] to 255 (white), otherwise 0 (black)
                segmented_img = np.where((img > self.t[0]) & (img < self.t[1]), 255, 0).astype(np.uint8)
            elif self.g == 2:
                # Set pixels greater than t[1] to 255 (white), otherwise 0 (black)
                segmented_img = np.where(img > self.t[1], 255, 0).astype(np.uint8)
            else:
                # Default case (if g is not 0, 1, or 2)
                segmented_img = np.zeros_like(img, dtype=np.uint8)
            
            # Append the segmented image to the list
            self.img.append(segmented_img)

    def convert_to_img_and_show(self):
        for image_array in self.img:
            image = Image.fromarray(image_array)
            plt.imshow(image, cmap='gray')  # Use 'gray' colormap for black and white images
            plt.axis('off')  # Hide axis
            plt.show()
