import cv2
import glob
import matplotlib.pyplot as plt
import numpy as np

folder = "real_images"

for file in glob.glob(f"{folder}/screens*"):
    img = cv2.imread(file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)       # GRAY, not RGB: Canny works on 1 channel brightness

    # Canny = find edges (places where brightness changes fast)
    # gradient > 150 -> strong edge (kept)
    # gradient < 50  -> not edge (dropped)
    # in between     -> kept only if touching a strong edge
    edges = cv2.Canny(gray, 50, 150)                   # result: black image, white edge lines

    lines = cv2.HoughLinesP(edges, 1, np.pi /180, 50, minLineLength=40, maxLineGap=5)
    
    mask = np.zeros_like(gray)
    for x1,y1,x2,y2 in lines.reshape(-1, 4):
        cv2.line(mask, (x1,y1), (x2,y2), 255, 9)
        cv2.line(img, (x1,y1), (x2,y2), (255, 0, 255), 1)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    

    

    plt.figure()
    plt.subplot(1, 2, 1)
    plt.imshow(img[:, :, ::-1])                         # BGR -> RGB for matplotlib
    plt.title("Original")
    plt.subplot(1, 2, 2)
    plt.imshow(edges, cmap="gray")                      # cmap gray, else matplotlib shows it in colors
    plt.title("Canny edges")
plt.show()
