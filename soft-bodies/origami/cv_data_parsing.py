import numpy as np
import matplotlib.pyplot as plt


def trim_data(data_array, trim_from=0, trim_to=None):
    """Trims a np.array or all nested elements of a np.array to be the same length"""
    # remember the original shape, in case that was important
    original_shape = data_array.shape
    flattened = data_array.flatten()

    if trim_to is None:
        lengths = [len(data) for data in flattened]
        trim_to = min(lengths)+trim_from

    for i, data in enumerate(flattened):
        flattened[i] = data[trim_from:trim_to]

    reshaped = flattened.reshape(original_shape)
    return reshaped

folder_path = "origami\\data\\spring2\\8W\\"
y_8w_1 = np.load(folder_path+"ydist_1.npy")
y_8w_2 = np.load(folder_path+"ydist_2.npy")-0.15
# y_6w_3 = np.load(folder_path+"ydist_3.npy")

y_8w_1 = np.insert(y_8w_1, -1, np.array([np.nan]*150))
# y_6w_2 = np.insert(y_6w_2, -1, np.array([np.nan]*150))

t1 = np.load(folder_path+"t_1.npy")
t2 = np.load(folder_path+"t_2.npy")+0.25
# t3 = np.load(folder_path+"t_3.npy")

t1 = np.insert(t1, -1, np.array([np.nan]*150))
# t2 = np.insert(t2, -1, np.array([np.nan]*150))

plt.plot(t1, y_8w_1)
plt.plot(t2, y_8w_2)
# plt.plot(t3, y_6w_3)
plt.show()


trimmed = trim_data(np.array([y_8w_1, y_8w_2], dtype=object))

data_reshape = np.array([trimmed[0],
                         trimmed[1]])

average = np.nanmean(data_reshape, axis=0)
stdv = np.nanstd(data_reshape, axis=0)

t = np.arange(0, len(average)/30, 1/30)

plt.plot(t, average)
plt.fill_between(t, average+stdv, average-stdv, alpha=0.5)
plt.show()

np.save(folder_path+"average.npy", average)
np.save(folder_path+"stdv.npy", stdv)
np.save(folder_path+"t.npy", t)