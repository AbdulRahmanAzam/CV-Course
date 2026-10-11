# Task 3: Anomaly Detection in Sensor Data using Wavelet Transformation
# Idea: wavelet splits signal into smooth part + detail (noise) parts.
# Remove small details -> clean "normal" signal. Points far from it = anomalies.
import numpy as np
import pywt
import matplotlib.pyplot as plt

folder = "real_images"                                 # "images" = drawn samples, "real_images" = real photos

data = np.loadtxt(f"{folder}/sensor.csv")              # sensor dataset: one reading per line

# 1) Decompose: [smooth, detail4, detail3, detail2, detail1] using "db4" wavelet, 4 levels
coeffs = pywt.wavedec(data, "db4", level=4)

# 2) Threshold: shrink small detail values to 0 (= remove noise). Keep coeffs[0] (smooth part).
threshold = np.std(coeffs[-1]) * np.sqrt(2 * np.log(len(data)))   # "universal threshold"
coeffs[1:] = [pywt.threshold(c, threshold, mode="soft") for c in coeffs[1:]]

# 3) Rebuild signal from cleaned coefficients
denoised = pywt.waverec(coeffs, "db4")[:len(data)]   # cut 1 extra point it may add

# 4) Residual = what normal pattern can't explain. Bigger than 2 std -> anomaly
residuals = data - denoised
anomalies = np.where(np.abs(residuals) > 2 * np.std(residuals))[0]   # indexes of anomalies
print("Anomalies:", len(anomalies))

plt.subplot(2, 1, 1)
plt.plot(data, label="Sensor Data")
plt.plot(denoised, "--", label="Denoised Signal")
plt.title("Sensor Data and Denoised Signal")
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(residuals, "r", label="Residuals")
plt.scatter(anomalies, residuals[anomalies], color="green", label="Anomalies")
plt.title("Residuals and Detected Anomalies")
plt.legend()
plt.show()
