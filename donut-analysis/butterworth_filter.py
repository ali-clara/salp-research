import numpy as np
from scipy.signal import butter, lfilter, freqz
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use("seaborn")


def butter_lowpass(cutoff, fs, order=5):
    return butter(order, cutoff, fs=fs, btype='low', analog=False)

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Filter reqirements.
order = 2
fs = 60.0       # sample rate, Hz
cutoff = 0.07  # desired cutoff frequency of the filter, Hz

# order = 2
# fs = 30.0
# cutoff = 0.07

# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)

# Plot the frequency response.
w, h = freqz(b, a, fs=fs, worN=8000)

# fig, ax = plt.subplots(1,1)
# ax.plot(w, np.abs(h), 'b')
# ax.plot(cutoff, 0.5*np.sqrt(2), 'ko')
# ax.axvline(cutoff, color='k')
# ax.set_xlim(0, 0.5*fs)
# ax.set_title("Lowpass Filter Frequency Response")
# ax.set_xlabel('Frequency [Hz]')
# ax.grid()

data = np.load("data/circumference_8-3-23.npy")
t = np.arange(0, 1/fs*len(data), 1/fs)

bias_term = np.mean(data[0:50])
data = data - bias_term

# Filter the data, and plot both the original and filtered signals.
filtered_data = butter_lowpass_filter(data, cutoff, fs, order)

data = data + bias_term
filtered_data = filtered_data + bias_term

np.save("data/filtered-circumference_8-3-23.npy", filtered_data)

area = np.load("data/area_8-3-23.npy")

data_to_export = list(zip(*[t, data, filtered_data, area]))
columns = ["time(sec)", "Raw circumference (mm)", "Filtered circumference (mm)", "Raw Area (mm^2)"]
df = pd.DataFrame(data_to_export, columns=columns)
df.to_csv("data/circumference_data_60fps.csv", index=False)

fig, ax = plt.subplots(1,1)
ax.plot(t, data, '.', label='data')
ax.plot(t, filtered_data, '-', color="tab:red", linewidth=2, label='filtered data')
ax.set_xlabel('Time [sec]')
ax.grid()
ax.legend()

plt.show()

