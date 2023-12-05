import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


force_old = pd.read_csv("main-TCA-batch-1/force_data/2W/load-cell-data_1.csv")["Force (g)"]
force_new = pd.read_csv("main-TCA-batch-2/force/2W.csv")["Force (g)"]

recording_frequency = 0.2

t_old = np.arange(0, len(force_old)*recording_frequency, recording_frequency)
t_new = np.arange(0, len(force_new)*recording_frequency, recording_frequency)

fig, ax = plt.subplots()
ax.plot(t_old, force_old*9.81, label="old")
ax.plot(t_new, force_new*9.81, label="new")
plt.title("TCA Comparison: 2W power input")
plt.ylabel("Force (mN)")
plt.xlabel("Time (sec)")
plt.legend(loc=0)
plt.show()

