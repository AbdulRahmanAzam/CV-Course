# Task 7: Coins Detection and Counting using Hough Circle Transform
# Idea: every edge pixel votes for circle centers (x, y) and radius r. Many votes = a circle = a coin.
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt

folder = "real_images"                                 # "images" = drawn samples, "real_images" = real photos

for file in glob.glob(f"{folder}/coins*"):
    img = cv2.imread(file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)                     # remove noise so no fake circles

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT,
                               dp=1.2,                 # vote grid size (1 = same as image)
                               minDist=50,             # 2 coin centers must be 50px apart
                               param1=100,             # Canny edge threshold (used inside)
                               param2=45,              # votes needed: lower = more circles (too low = fake circles on textures)
                               minRadius=20, maxRadius=70)   # coin sizes to look for
    circles = np.uint16(np.around(circles[0]))         # rows of (x, y, r)

    for x, y, r in circles:
        cv2.circle(img, (x, y), r, (0, 255, 0), 3)     # coin outline
        cv2.circle(img, (x, y), 2, (0, 0, 255), 3)     # center

    print(file, "coins:", len(circles))
    plt.figure()
    plt.imshow(img[:, :, ::-1])
    plt.title(f"Coins: {len(circles)}")
plt.show()
