import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# data 
t = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38]

# string goes from 2.375 (ish, t0) to 11 inches
g200_w1 = [[3/8, 1/2, 17/32, 9/16, 9/16, 10/16, 10/16, 11/16, 11/16, 3/4, 3/4, 3/4, 3/4, 11/16, 10/16, 10/16, 9/16, 9/16, 1/2, 1/2], 
            [3/8, 7/16, 7/16, 1/2, 9/16, 9/16, 10/16, 10/16, 10/16, 11/16, 11/16, 11/16, 11/16, 11/16, 10/16, 9/16, 9/16, 1/2, 1/2, 1/2], 
            [3/8, 7/16, 1/2, 1/2, 17/32, 9/16, 9/16, 9/16, 9/16, 10/16, 1/2, 1/2, 7/16, 7/16, 7/16, 3/8, 3/8, 3/8, 3/8, 3/8]] 
g200_w2 = [[], [], []]
g200_w3 = [[3/8, 1/2, 11/16, 12/16, 14/16, 1, 1, 17/16, 17/16, 18/16, 15/16, 3/4, 10/16, 9/16, 1/2, 1/2, 1/2, 1/2, 1/2, 1/2],
           [1/4, 3/8, 9/16, 11/16, 13/16, 14/16, 15/16, 15/16, 1, 1, 13/16, 10/16, 1/2, 1/2, 7/16, 7/16, 7/16, 7/16, 7/16, 7/16]]
        #    [14/16, 1, 17/16, 17/16, 18/16, 18/16, 19/16, 19/16, 19/16, 19/16, 19/16, 20/16, 20/16, 20/16, 20/16, 21/16, 21/16, 20/16, 19/16, 15/16]]
           
        #    []]

g100_w1 = [[], [], []]
g100_w2 = [[], [], []]
g100_w3 = [[], [], []]


def calc_mean_and_error(data):
    # normalize each bc I'm a goon 
    for i, _ in enumerate(data):
        data[i] = data[i] - data[i][0]
    mean = np.mean(data, axis=0)
    st_dev = np.std(data, axis=0)
    return mean, st_dev

def calc_strain(l, delta_l):
    return (l - np.array(delta_l)) / l

def calc_percent_contraction(l, delta_l):
    return (np.array(delta_l) / l) * 100

g200_w1_mean, g200_w1_st_dev = calc_mean_and_error(np.array(g200_w1))
g200_w3_mean, g200_w3_st_dev = calc_mean_and_error(np.array(g200_w3))

sns.set_theme()
fig, ax = plt.subplots(1,1)
ax.errorbar(t, calc_percent_contraction(8.5, g200_w1_mean), yerr=g200_w1_st_dev, capsize=2, label="1W")
ax.errorbar(t, calc_percent_contraction(8.5, g200_w3_mean), yerr=g200_w3_st_dev, capsize=2, label="3W")
ax.set_xlabel("Time (sec)")
ax.set_ylabel("Percent Compression (%)")
ax.set_title("TCA Behavior with 200g Weight")
plt.legend(loc=0)
plt.show()