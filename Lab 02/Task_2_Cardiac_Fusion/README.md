# Task 2: CT + MRI Fusion

**Input:** `data/ct_slice.png` and `data/mri_slice.png`. They are a matched pair, `Patient_001/CT/slice_001.png` and `Patient_001/MRI/slice_001.png`, from the `synthetic_slices` folder of the dataset.

## Pipeline

1. **Load:** read both slices as grayscale and resize the MRI to the CT's size.
2. **Equalize:** apply `cv2.equalizeHist` to each image separately.
3. **Color map + overlay:** color the CT with `COLORMAP_BONE` (structure) and the MRI with `COLORMAP_JET` (tissue), then blend them 50/50.
4. **Weighted fusion:** `cv2.addWeighted(ct_color, 0.7, mri_color, 0.3, 0)`.
5. **Log + gamma (0.8):** applied to the fused image so dark values are not crushed to black and bright values are not blown out to white.
6. **Comparison:** show CT, MRI and the fused image side by side with their histograms.

## Weighting logic

- **CT gets alpha = 0.7.** CT shows sharp structural edges, so it gets the bigger weight to keep those edges.
- **MRI gets beta = 0.3.** MRI shows soft-tissue variation. A smaller weight adds that detail without hiding the CT edges.
- `alpha + beta = 1`, so the overall brightness stays in range.

## Analysis

The notebook prints the mean (brightness) and standard deviation (contrast) of the CT, the MRI and the fused image. It also prints how strongly the fused image correlates with each input. A high correlation with both inputs means the fused image keeps information from each modality. The figures are saved to `output/`.
