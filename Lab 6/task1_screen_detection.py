# Task 1: Computer Screen Detection using Hough Line Transform
# Idea: screen border = 4 straight lines. Find lines -> lines make rectangles -> rectangles = screens.
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt

folder = "real_images"                                # "images" = drawn samples, "real_images" = real photos
 
for file in glob.glob(f"{folder}/screens*"):          # every screens image in the folder
    img = cv2.imread(file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)      # Hough works on 1 channel

    # 1) Edges: Canny keeps pixels where brightness changes sharply (borders)
    edges = cv2.Canny(gray, 50, 150)                  # 50/150 = low/high edge thresholds

    # 2) Hough lines: every edge pixel "votes" for lines through it; lines with many votes are real
    #    args: rho step 1px, angle step 1 degree, min 50 votes, min length 40px, join gaps < 5px
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, minLineLength=40, maxLineGap=5)

    # 3) Draw the found lines on a black image -> each screen becomes a white rectangle outline
    mask = np.zeros_like(gray)
    for x1, y1, x2, y2 in lines.reshape(-1, 4):       # each line = (x1, y1, x2, y2)
        cv2.line(mask, (x1, y1), (x2, y2), 255, 9)    # thick (9px) so corners join up
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 1)   # also show Hough lines (pink) on photo

    # 4) Closed outlines = screens. boundingRect gives (x, y, width, height) of each one
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    screens = [cv2.boundingRect(c) for c in contours]
    screens = [s for s in screens if s[2] > 60 and s[3] > 45 and 1 < s[2] / s[3] < 2]   # screen-sized, wider than tall
    screens = sorted(screens, key=lambda s: (s[1], s[0]))   # sort: top row first, then left -> right

    # 5) ON / OFF: a screen that is ON is bright inside
    for x, y, w, h in screens:
        status = "ON" if gray[y + h // 2, x + w // 2] > 100 else "OFF"   # brightness of center pixel
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(img, status, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # 6) MISSING: in the same row, empty space wider than a screen = a screen should be there
    for a, b in zip(screens, screens[1:]):            # each screen and the next one
        x, y, w, h = a
        if abs(b[1] - y) < h / 2 and b[0] - (x + w) > w:     # same row, big empty gap
            x = (x + w + b[0]) // 2 - w // 2          # middle of the gap
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
            cv2.putText(img, "MISSING", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    print(file, "screens found:", len(screens))
    plt.figure()
    plt.imshow(img[:, :, ::-1])      
                     # [:, :, ::-1] = BGR -> RGB for matplotlib
plt.show()
