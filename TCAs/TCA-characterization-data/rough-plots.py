import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
import os

# force_old = pd.read_csv("main-TCA-batch-1/force_data/2W/load-cell-data_1.csv")["Force (g)"]
# force_new = pd.read_csv("main-TCA-batch-2/force/2W/2W.csv")["Force (g)"]
# force_3w = pd.read_csv("main-TCA-batch-2/force/3W/3W.csv")["Force (g)"]

recording_frequency = 0.2

# t_old = np.arange(0, len(force_old)*recording_frequency, recording_frequency)
# t_new = np.arange(0, len(force_new)*recording_frequency, recording_frequency)
# t_3w = np.arange(0, len(force_3w)*recording_frequency, recording_frequency)

# fig, ax = plt.subplots()
# ax.plot(t_old, force_old*9.81, label="old")
# ax.plot(t_new, force_new*9.81, label="new")
# ax.plot(t_3w, force_3w*9.81)
# plt.title("TCA Comparison: 2W power input")
# plt.ylabel("Force (mN)")
# plt.xlabel("Time (sec)")
# plt.legend(loc=0)
# plt.show()

path = "26AWG/force/3W/"
fig, ax = plt.subplots()
data_max = 0
for file_name in glob.glob(path+"*.csv"):
    print(file_name)
    data = pd.read_csv(file_name)
    labels = data.keys()
    response = data[labels[0]].to_numpy()
    time = data[labels[1]].to_numpy()

    # force = data["Linear displacement (mm)"]
    # time = data["Time (s)"]
    # x = np.arange(0, len(force)*recording_frequency, recording_frequency)
    # print(data)
    ax.plot(time, response)
    data_max = max(max(response), data_max)

ax.set_title("2W")
# ax.set_title("~1W, 0.7")
# ax.set_ylabel("displacement (mm)")
ax.set_ylabel("force (g)")
ax.set_ylim([-10, data_max+3])

plt.show()