import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-deep')
import pandas as pd
import sys
sys.path.append("C:\\Users\\alicl\\Documents\\GitHub\\salp-research")
from create_paper_figure import MakePlot

def trim(array):
    return array[0:3500]

def load_and_compile(path, num_trials):
    big_area_list = []
    big_time_list = []

    for i in range(num_trials):
        area_a = np.load(path+"/area_"+str(i+1)+"a.npy")
        area_b = np.load(path+"/area_"+str(i+1)+"b.npy")
        big_area_list.append(trim(area_a))
        big_area_list.append(trim(area_b))

        time_a = np.load(path+"/t_"+str(i+1)+"a.npy")
        time_b = np.load(path+"/t_"+str(i+1)+"b.npy")
        big_time_list.append(trim(time_a))
        big_time_list.append(trim(time_b))

    return big_area_list, big_time_list 

def nan_interpolation(y):
    """Helper function to interpolate NAN values
    https://stackoverflow.com/questions/6518811/interpolate-nan-values-in-a-numpy-array"""
    nans = np.isnan(y)
    x = lambda z: z.nonzero()[0]
    y[nans]= np.interp(x(nans), x(~nans), y[~nans])

    return y

def graph_values(values, times, avg, avg_time, stdv):
    fig, ax = plt.subplots(2,1)
    my_plot = MakePlot()

    for i, val in enumerate(values):
        
        ax[0].plot(times[i], val)

        # ax[1].plot(t_a, circ_a, '.')
        # ax[1].plot(t_b, circ_b, '.')

    my_plot.set_xy(avg_time, avg)
    my_plot.set_stdev(stdv)
    my_plot.set_axis_labels("Time (sec)", "Contour Area (mm^2)")
    my_plot.plot_xy()
    my_plot.set_savefig("avg_donut_response.pdf")
    my_plot.label_and_save()

    
    ax[1].plot(avg_time, avg)
    ax[1].fill_between(avg_time, avg+stdv, avg-stdv, alpha=0.5)
    ax[1].set_ylabel("Contour Area (mm^2)")
    ax[1].set_xlabel("Time (s)")
    ax[1].set_xlim([-2,60])
    
    ax[0].set_xlim([-2,60])
    ax[0].set_xlabel("Time (s)")
    ax[0].set_ylabel("Contour Area (mm^2)")
    ax[0].set_title("Soft Module Area, 5W Power")

    plt.tight_layout()
    plt.savefig("total_donut_response.png")
    plt.show()

areas, times = load_and_compile("data/8-31-23", num_trials=3)
average = np.mean(areas, axis=0)
stdv = np.std(areas, axis=0)

average_interp = nan_interpolation(average)
stdv_interp = nan_interpolation(stdv)

t = np.arange(0, len(average)/60, 1/60)

graph_values(areas, times, average_interp, t, stdv_interp)

np.save("data/8-31-23/area_avg.npy", average_interp)
np.save("data/8-31-23/area_stdv.npy", stdv_interp)
np.save("data/8-31-23/t_avg.npy", t)

# area_a = np.load(file_path+"/area_"+str(i+1)+"a.npy")
# circ_a = np.load(file_path+"/circ_"+str(i+1)+"a.npy")
# t_a = np.load(file_path+"/t_"+str(i+1)+"a.npy")

# area_b = np.load(file_path+"/area_"+str(i+1)+"b.npy")
# circ_b = np.load(file_path+"/circ_"+str(i+1)+"b.npy")
# t_b = np.load(file_path+"/t_"+str(i+1)+"b.npy")