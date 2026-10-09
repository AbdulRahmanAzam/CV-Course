# Medical Imaging Portfolio (Lab 02)

Computer Vision Lab 02: basic image enhancement on medical images with OpenCV and NumPy.

| Folder | Task | Notebook |
|---|---|---|
| `Task_1_Chest_XRay/` | Enhancing a chest X-ray | `xray_enhancement.ipynb` |
| `Task_2_Cardiac_Fusion/` | Fusing a CT slice and an MRI slice | `modal_fusion.ipynb` |
| `Task_3_Echo_Analysis/` | Enhancing an echo video in real time | `realtime_echo.ipynb` |

## Setup

```bash
pip install -r requirements.txt
```

Open a notebook from inside its own task folder and run all cells. The notebooks use relative paths such as `data/...` and `output/...`, so they need to run from that folder.

## Datasets

Only the sample files each notebook uses are included, not the full datasets:

- Chest X-ray: [COVID19+PNEUMONIA+NORMAL Chest X-Ray](https://www.kaggle.com/datasets/sachinkumar413/covid-pneumonia-normal-chest-xray-images)
- CT and MRI: [Heart CT & MRI Dataset](https://www.kaggle.com/datasets/ziya07/heart-ct-and-mri-dataset)
- Echo video: [Stanford EchoNet-Dynamic](https://www.kaggle.com/datasets/manojkumarcs28/echonet-dynamic-by-stanford-university)
