# Lab 06 (minimal)

```bash
cd "Lab 6 Final"
python make_samples.py             # once: creates images/ (simple drawn test pictures)
python task1_screen_detection.py   # ... up to task8
```

Every task has one switch at the top:

```python
folder = "real_images"   # real photos/videos (default)
folder = "images"        # simple drawn samples from make_samples.py
```

Both folders use the same file names, so nothing else changes.
Video tasks (4, 8): press `q` to quit. Use `cv2.VideoCapture(0)` for webcam.

## real_images sources

| Task | Files | Source |
|---|---|---|
| 1, 2 | screens1/2, lab, asset_* (crops) | Wikimedia Commons: "Computer lab.jpg", "Computer lab showing desktop PCs warwick.jpg" |
| 3 | sensor.csv (1000 readings around a failure) | Numenta Anomaly Benchmark, machine_temperature_system_failure.csv |
| 4 | object.png, test_video.mp4 | OpenCV samples box.png + box_in_scene.png (video = that photo with camera motion + a block covering part) |
| 5 | pano1-3 | OpenCV test data stitching/boat1-3.jpg |
| 6 | road1-4 | Udacity CarND-LaneLines-P1 test_images |
| 7 | coins1 (Pakistani Rs 1 coins), coins2 (Czech coins on notes) | Wikimedia Commons: "1 rupe coins.JPG", "Czk- coins and banknotes.JPG" |
| 8 | security.mp4 | OpenCV samples vtest.avi |
