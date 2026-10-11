# Task 2: Asset Tracking in a Computer Lab using SIFT
# Idea: SIFT finds "keypoints" (corners/blobs) + a 128-number description of each.
# If many keypoints of an asset photo also appear in the lab photo -> that asset is in the lab.
import glob
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

folder = "real_images"                                 # "images" = drawn samples, "real_images" = real photos

lab = cv2.imread(f"{folder}/lab.png")
sift = cv2.SIFT_create()
bf = cv2.BFMatcher()                                   # compares descriptors by distance

kp_lab, des_lab = sift.detectAndCompute(lab, None)     # keypoints + descriptors of lab photo

for file in glob.glob(f"{folder}/asset_*"):            # one photo per asset in our inventory
    name = os.path.basename(file)[6:-4]                # "asset_monitor.png" -> "monitor"
    asset = cv2.imread(file)
    kp, des = sift.detectAndCompute(asset, None) 

    # For each asset keypoint get the 2 closest lab keypoints.
    # Lowe's ratio test: keep it only if best match is clearly better than 2nd best.
    matches = bf.knnMatch(des, des_lab, k=2)
    good = [m for m, n in matches if m.distance < 0.75 * n.distance]

    if len(good) > 10:                                 # enough matches -> asset found
        # Homography = how asset photo is moved/rotated/scaled inside lab photo (RANSAC skips bad matches)
        src = np.float32([kp[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)      # points in asset
        dst = np.float32([kp_lab[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)  # same points in lab
        H, _ = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
        h, w = asset.shape[:2]
        corners = np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2)
        box = np.int32(cv2.perspectiveTransform(corners, H))   # asset corners -> lab position
        cv2.polylines(lab, [box], True, (0, 0, 255), 3)
        cv2.putText(lab, name, tuple(box[0][0]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        print(name, "PRESENT", len(good))
    else:
        print(name, "MISSING", len(good))

plt.imshow(lab[:, :, ::-1])
plt.show()
