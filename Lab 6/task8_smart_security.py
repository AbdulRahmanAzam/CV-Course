# Task 8: Smart Security System (boundary detection + alarm)
# Idea: background subtractor learns what the empty scene looks like. Anything new/moving = foreground.
# Its contour = its boundary. If that boundary touches the security zone -> ALARM.
import cv2

folder = "real_images"                                 # "images" = drawn samples, "real_images" = real video
x1, y1, x2, y2 = 380, 200, 600, 440                    # security zone corners

video = cv2.VideoCapture(f"{folder}/security.mp4")     # 0 instead of path = webcam
bg = cv2.createBackgroundSubtractorMOG2()              # learns background from the frames it sees

while True:
    ok, frame = video.read()
    if not ok:
        break

    mask = bg.apply(frame)                             # white = foreground, gray(127) = shadow
    _, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)   # keep white only (drop shadows)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)   # boundaries

    alarm = False
    for c in contours:
        if cv2.contourArea(c) < 500:                   # tiny = noise, skip
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.drawContours(frame, [c], -1, (0, 255, 255), 2)
        if x < x2 and x + w > x1 and y < y2 and y + h > y1:     # object box overlaps zone box
            alarm = True

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255) if alarm else (255, 0, 0), 2)
    if alarm:
        cv2.putText(frame, "ALARM!", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    cv2.imshow("Security", frame)
    if cv2.waitKey(60) == ord("q"):
        break
