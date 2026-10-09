# Task 1: Chest X-Ray Enhancement

**Input:** `data/chest_xray.png` (PNEUMONIA_10.png, the darkest of the samples we checked)

## Pipeline

1. **Load:** read the image as grayscale with `cv2.imread(..., cv2.IMREAD_GRAYSCALE)`.
2. **Histogram equalization:** `cv2.equalizeHist` spreads the pixel values over the full 0-255 range, which makes the lungs and ribs easier to see.
3. **Color mapping:** `cv2.applyColorMap(..., cv2.COLORMAP_JET)` turns small changes in brightness into changes in color.
4. **Color balance (gray world):** each B, G and R channel is scaled so all three have the same average. This evens out the channels so no single color dominates.
5. **Thresholding:** keep only pixels brighter than 200. These are the densest tissues, such as bone.
6. **Log transform:** `s = c * log(1 + r)` brightens the dark regions, so the faint outer edges of the ribcage show up.
7. **Gamma transform:** `s = 255 * (r / 255) ^ 0.5` lifts the midtones, which softens the bones and makes the lung tissue clearer.

Each step saves its result to `output/`. `output/summary.png` shows all the steps together.
