# Task 4: Object Recognition in a Video using SIFT
# Idea: match SIFT keypoints of the reference image with each frame.
# Homography = how the reference got moved/rotated/scaled in the frame -> use it to draw the box.
# SIFT works under scale, rotation and partial occlusion (some keypoints still visible = enough).
import cv2
import numpy as np

folder = "real_images"                                 # "images" = drawn samples, "real_images" = real photos

ref = cv2.imread(f"{folder}/object.png")
sift = cv2.SIFT_create()
bf = cv2.BFMatcher()
kp_ref, des_ref = sift.detectAndCompute(ref, None)     # reference done once
h, w = ref.shape[:2]
corners = np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2)   # 4 corners of reference

video = cv2.VideoCapture(f"{folder}/test_video.mp4")      # 0 instead of path = webcam
while True:
    ok, frame = video.read()
    if not ok:                                         # video ended
        break
    kp, des = sift.detectAndCompute(frame, None)
    good = [m for m, n in bf.knnMatch(des_ref, des, k=2) if m.distance < 0.75 * n.distance]

    if len(good) > 10:
        src = np.float32([kp_ref[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)   # points in reference
        dst = np.float32([kp[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)       # same points in frame
        H, _ = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)    # RANSAC ignores wrong matches
        box = cv2.perspectiveTransform(corners, H)              # reference corners -> frame
        cv2.polylines(frame, [np.int32(box)], True, (0, 255, 0), 3)

    cv2.imshow("Object Recognition", frame)
    if cv2.waitKey(50) == ord("q"):                    # wait 50ms, q = quit
        break
