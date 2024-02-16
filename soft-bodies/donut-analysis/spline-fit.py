from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import splrep, splev
# plt.style.use("seaborn")
import sys
sys.path.append("C:\\Users\\alicl\\Documents\\GitHub\\salp-research")
from create_paper_figure import MakePlot

def nan_interpolation(y):
    """Helper function to interpolate NAN values
    https://stackoverflow.com/questions/6518811/interpolate-nan-values-in-a-numpy-array"""
    nans = np.isnan(y)
    x = lambda z: z.nonzero()[0]
    y[nans]= np.interp(x(nans), x(~nans), y[~nans])

    return y

### load the file of choice
# area = np.load("donut-analysis/data/12-15-23/area_4W.npy") # mm^2
# area = np.load("donut-analysis/data/8-31-23/area_avg.npy")
# area_interp = nan_interpolation(area)
# print(area_interp)
# x = np.load("donut-analysis/data/12-15-23/t_4W.npy")
# x = np.load("donut-analysis/data/8-31-23/t_avg.npy")
# stdv = np.load("donut-analysis/data/8-31-23/area_stdv.npy")

area = np.load("average-donut-circumference.npy")
x = np.arange(0, len(area)/60, 1/60)
# x = np.arange(0, len(area)*0.2, 0.2)

# fs = 30
# initial_avg = np.mean(area[0:5*fs])
# area[0:5*fs] = initial_avg # mm^2
area_m = area / 1e6 # m^2

h = 1 # mm
volume = area * h # mm^3

volume_spline = splrep(x, volume, s=len(x)/250)
vol_spline_fit = splev(x, volume_spline) # mm^3
# vol_spline_fit_ml = vol_spline_fit / 1e3

vol_dot = splev(x, volume_spline, der=1) # mm^3/s
print(min(vol_dot))
vol_dot_ml = vol_dot / 1e3 # ml/s
vol_dot_m = vol_dot / 1e9 # m^3/s

rho = 1000  # kg/m^3
c0 = 0.6    # dimensionless
thrust = rho*vol_dot_m**2 / (c0 * area_m) # N
thrust_mn = thrust * 1e3 # mN

fig, ax = plt.subplots(5,1)
ax[0].plot(x, area)
ax[1].plot(x, volume)
ax[1].plot(x, vol_spline_fit, label="volume spline fit")
# ax[2].plot(x, vol_spline_fit_ml)
ax[3].plot(x, vol_dot)
ax[4].plot(x, thrust_mn)

plt.tight_layout()
plt.show()

# my_plot = MakePlot(subplots=(2,1))

# my_plot.set_subplot(0)
# my_plot.set_xy(x, area)
# my_plot.set_stdev(stdv)
# my_plot.set_xlim([0, 62])
# my_plot.set_axis_labels("Time (sec)", "Area (mm^2)")
# my_plot.plot_xy()

# my_plot.set_subplot(1)
# cut = 2000
# my_plot.set_xy(x[0:cut], thrust_mn[0:cut])
# my_plot.set_xlim([0, 62])
# my_plot.set_axis_labels("Time (sec)", "Extrapolated Thrust (mN)")
# my_plot.plot_xy()

# my_plot.set_savefig("donut-analysis/thrust-extrapolation-single.png")
# my_plot.label_and_save()