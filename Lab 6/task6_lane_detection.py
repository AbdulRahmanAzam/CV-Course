# Task 6: Lane Detection using Hough Line Transform
# Steps: gray -> edges -> keep only road area (ROI) -> Hough lines -> split left/right by slope -> draw
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt

folder = "real_images"                                 # "images" = drawn samples, "real_images" = real photos

for file in glob.glob(f"{folder}/road*"):
    img = cv2.imread(file)
    H, W = img.shape[:2]

    # 1) Edges
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    # 2) ROI: triangle in front of car. Everything outside it (sky, trees) is set to 0
    mask = np.zeros_like(edges)
    cv2.fillPoly(mask, [np.array([(0, H), (W, H), (W // 2, int(H * 0.58))])], 255)
    edges = cv2.bitwise_and(edges, mask)

    # 3) Hough line segments inside ROI
    lines = cv2.HoughLinesP(edges, 2, np.pi / 180, 50, minLineLength=40, maxLineGap=100)

    # 4) Slope tells side. Image y goes DOWN, so left lane has negative slope, right lane positive
    for x1, y1, x2, y2 in lines.reshape(-1, 4):
        slope = (y2 - y1) / (x2 - x1 + 1e-6)            # +1e-6 avoids divide by zero
        if abs(slope) > 0.4:                           # skip near-flat lines (not lanes)
            color = (0, 0, 255) if slope < 0 else (255, 0, 0)   # left = red, right = blue
            cv2.line(img, (x1, y1), (x2, y2), color, 8)

    plt.figure()
    plt.imshow(img[:, :, ::-1])
plt.show()
