# Task 3: Real-Time Echo Video

**Input:** `data/echo.mp4`, a short clip (`0X100009310A3BD7FC.mp4`) from EchoNet-Dynamic.

## How to run

1. Open `realtime_echo.ipynb` from inside this folder.
2. Run all cells.
3. A window opens with the raw video on the left and the enhanced video on the right.
4. Press **q** to stop early. Otherwise it closes when the video ends.
5. Frame 50 is saved as `output/side_by_side.png`.

## Steps applied to each frame

Histogram equalization, then JET heatmap, then color balance (gray world), then log transform, then gamma = 1.5. A gamma above 1 tones down the very bright white backscatter noise.
