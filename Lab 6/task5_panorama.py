# Task 5: Panoramic Image using SIFT
# Idea: find same keypoints in two overlapping photos -> homography tells how to place
# right photo next to left one -> warp right photo, paste left photo on top.
import cv2
import numpy as np
import matplotlib.pyplot as plt

folder = "real_images"                                 # "images" = drawn samples, "real_images" = real photos

sift = cv2.SIFT_create()
bf = cv2.BFMatcher()

def stitch(left, right):
    kp1, des1 = sift.detectAndCompute(left, None)
    kp2, des2 = sift.detectAndCompute(right, None)
    good = [m for m, n in bf.knnMatch(des2, des1, k=2) if m.distance < 0.75 * n.distance]

    src = np.float32([kp2[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)   # points in right photo
    dst = np.float32([kp1[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)   # same points in left photo
    H, _ = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)                     # right -> left coordinates

    # Canvas wide enough for both. Warp right photo into it, then paste left photo at the start.
    pano = cv2.warpPerspective(right, H, (left.shape[1] + right.shape[1], left.shape[0]))
    pano[:, :left.shape[1]] = left

    # Cut off empty black part on the right
    x, y, w, h = cv2.boundingRect(cv2.findNonZero(cv2.cvtColor(pano, cv2.COLOR_BGR2GRAY)))
    return pano[:, :x + w]

images = [cv2.imread(f"{folder}/pano{i}.png") for i in [1, 2, 3]]
panorama = stitch(stitch(images[0], images[1]), images[2])   # (1 + 2) + 3

plt.imshow(panorama[:, :, ::-1])
plt.show()
