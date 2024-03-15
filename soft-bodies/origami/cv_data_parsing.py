import numpy as np
import matplotlib.pyplot as plt

folder_path = "origami\\data\\spring2\\"

y_6w_avg = np.load(folder_path+"6W\\average.npy")
y_6w_std = np.load(folder_path+"6W\\stdv.npy")
t_6w = np.load(folder_path+"6W\\t.npy")

y_8w_avg = np.load(folder_path+"8W\\average.npy")+0.32
y_8w_std = np.load(folder_path+"8W\\stdv.npy")
t_8w = np.load(folder_path+"8W\\t.npy")

plt.plot(t_6w, y_6w_avg, label="6W")
plt.plot(t_8w, y_8w_avg, label="8W")
plt.xlabel("Time (sec)")
plt.ylabel("Length between reference points (mm)")
plt.legend()
plt.title("Cold Water")
plt.show()