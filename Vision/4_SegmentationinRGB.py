# %%
from tool import *

"""Segmenting red color in RGB space from image ‘peppers.jpg’.
Output segmented images in R,G,B, and final image, respectively
"""
# %%
red = (255, 0, 0)

img = imread("4_peppers.jpg")

img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

imshow(img_gray)

# ((img-red)^2).sum()

img[np.sqrt(np.sum((img - red) ^ 2, axis=2)) < 8] = (0, 0, 0)
imshow(img)
# imshow(img_gray)
# ((img - red) ^ 2).sum()
