# NOT part of the lab. Run once: it draws simple fake test images/videos into images/.
# Real photos with the same file names are in real_images/.
import os
import cv2
import numpy as np

os.makedirs("images", exist_ok=True)
rng = np.random.default_rng(7)

# Task 3: 1000 normal sensor readings (mean 0, std 1)
np.random.seed(42)
np.savetxt("images/sensor.csv", np.random.normal(0, 1, 1000), fmt="%.4f")

def rand_color():
    return [int(v) for v in rng.integers(0, 256, 3)]

def textured(h, w, color, label):
    img = np.full((h, w, 3), color, np.uint8)
    for _ in range(60):
        cv2.circle(img, (int(rng.integers(0, w)), int(rng.integers(0, h))), int(rng.integers(3, 10)), rand_color(), -1)
    cv2.putText(img, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    return img

def paste(scene, obj, cx, cy, angle, scale):
    h, w = obj.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, scale)
    M[0, 2] += cx - w / 2
    M[1, 2] += cy - h / 2
    size = (scene.shape[1], scene.shape[0])
    m = cv2.warpAffine(np.full((h, w), 255, np.uint8), M, size)
    scene[m > 0] = cv2.warpAffine(obj, M, size)[m > 0]

# Task 1: 2 rows x 6 screens (on / off / one missing)
img = np.full((500, 900, 3), 180, np.uint8)
layout = ["on off on on off on", "off on on missing on off"]
for top, row in zip([80, 260], layout):
    for c, status in enumerate(row.split()):
        x = 40 + c * 140
        if status != "missing":
            cv2.rectangle(img, (x, top), (x + 110, top + 90), (25, 25, 25), -1)
            cv2.rectangle(img, (x + 8, top + 8), (x + 102, top + 82), (235, 200, 120) if status == "on" else (45, 45, 45), -1)
cv2.imwrite("images/screens.png", img)

# Task 2: asset photos + lab scene (UPS not in the scene)
assets = {"monitor": textured(170, 230, (150, 90, 30), "LAB-PC-07"),
          "keyboard": textured(110, 320, (60, 60, 60), "KEYBOARD"),
          "cpu": textured(220, 120, (40, 40, 40), "A-1023"),
          "ups": textured(140, 200, (30, 30, 120), "UPS")}
for name, a in assets.items():
    cv2.imwrite(f"images/asset_{name}.png", a)
lab = np.full((600, 900, 3), (170, 200, 215), np.uint8)
paste(lab, assets["monitor"], 250, 170, 8, 0.9)
paste(lab, assets["keyboard"], 300, 450, -12, 1.1)
paste(lab, assets["cpu"], 700, 300, 0, 0.8)
cv2.imwrite("images/lab.png", lab)

# Task 4: reference object + video where it moves/rotates/scales and gets partly covered
book = textured(260, 190, (40, 60, 160), "BOOK")
cv2.imwrite("images/object.png", book)
out = cv2.VideoWriter("images/test_video.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 20, (640, 480))
for i in range(90):
    t = i / 89
    frame = np.full((480, 640, 3), (200, 210, 200), np.uint8)
    paste(frame, book, 150 + 340 * t, 240, -30 + 60 * t, 0.6 + 0.6 * t)
    if 35 <= i <= 60:
        x = int(150 + 340 * t)
        cv2.rectangle(frame, (x - 20, 120), (x + 120, 300), (150, 150, 150), -1)
    out.write(frame)
out.release()

# Task 5: one wide scene cut into 3 overlapping photos
scene = np.full((450, 1400, 3), (230, 190, 140), np.uint8)
scene[250:] = (80, 140, 90)
for x in range(20, 1380, 110):
    top = 300 - int(rng.integers(100, 220))
    cv2.rectangle(scene, (x, top), (x + 80, 300), rand_color(), -1)
    for wy in range(top + 10, 290, 22):
        for wx in range(x + 8, x + 72, 18):
            if rng.random() < 0.7:
                cv2.rectangle(scene, (wx, wy), (wx + 10, wy + 12), (40, 220, 250), -1)
for _ in range(120):
    cv2.circle(scene, (int(rng.integers(0, 1400)), int(rng.integers(310, 445))), int(rng.integers(4, 14)), rand_color(), -1)
for k, x in enumerate([0, 400, 800]):
    cv2.imwrite(f"images/pano{k + 1}.png", scene[:, x:x + 600])

# Task 6: road images from the car camera
for k, shift in enumerate([0, 60]):
    road = np.full((540, 960, 3), (235, 200, 150), np.uint8)
    road[310:] = (70, 130, 80)
    cv2.fillPoly(road, [np.array([[0, 540], [960, 540], [560, 310], [400, 310]])], (100, 100, 100))
    cv2.line(road, (220 + shift, 540), (455, 325), (0, 200, 255), 8)
    for d in range(0, 10, 2):
        p = lambda t: (int(740 + shift + (505 - 740 - shift) * t), int(540 - 215 * t))
        cv2.line(road, p(d / 10), p((d + 1) / 10), (255, 255, 255), 8)
    cv2.imwrite(f"images/road{k + 1}.png", road)

# Task 7: coins of 3 sizes on a table
coins = np.full((500, 700, 3), (60, 100, 140), np.uint8)
for x, y, r in [(100, 100, 30), (250, 90, 40), (420, 110, 50), (590, 120, 30), (120, 300, 50),
                (300, 280, 30), (470, 300, 40), (620, 330, 40), (300, 430, 30)]:
    cv2.circle(coins, (x, y), r, (190, 190, 190), -1)
    cv2.circle(coins, (x, y), r, (110, 110, 110), 3)                # darker rim
    cv2.circle(coins, (x, y), r * 2 // 3, (150, 150, 150), 2)       # inner ring
cv2.imwrite("images/coins.png", coins)

# Task 8: room camera, a bag walks into the zone and back out
room = np.full((480, 640, 3), (200, 210, 215), np.uint8)
room[330:] = (120, 140, 150)
cv2.rectangle(room, (430, 230), (560, 330), (90, 90, 90), -1)
out = cv2.VideoWriter("images/security.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 15, (640, 480))
out.write(room)                                   # first frame = empty room (background)
for i in range(100):
    frame = room.copy()
    x = 20 + i * 7 if i < 60 else 440 - (i - 60) * 10
    cv2.rectangle(frame, (x, 300), (x + 70, 390), (30, 30, 160), -1)
    out.write(frame)
out.release()
print("Sample data saved in images/")
