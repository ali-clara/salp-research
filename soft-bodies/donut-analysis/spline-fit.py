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

def fit_spline(x, y, s, derivative=0):
    spline = splrep(x, y, s)
    spline_fit = splev(x, spline, der=derivative)
    return spline_fit

def thrust_from_dvdt(dvdt, a0, rho=1000, c0=0.6):
    """volume: m3. a0: m"""
    thrust = rho*dvdt**2 / (c0 * a0) # N
    return thrust

def volume_spline(cross_sec_area, h, t):
    """cross_sec_area: mm^2. h: mm
        volume out: m3, m3/s"""

    area_m2 = cross_sec_area / 1e6
    h_m = h / 1e3
    volume_m3 = area_m2*h_m

    volume_spline_m3 = fit_spline(t, volume_m3, s=len(t))
    vol_dot_spline_m3s = fit_spline(t, volume_m3, s=len(t), derivative=1)

    return volume_spline_m3, vol_dot_spline_m3s

### load the file of choice
# area = np.load("donut-analysis/data/12-15-23/area_4W.npy") # mm^2
# area = np.load("donut-analysis/data/8-31-23/area_avg.npy")
# area_interp = nan_interpolation(area)
# print(area_interp)
# x = np.load("donut-analysis/data/12-15-23/t_4W.npy")
# x = np.load("donut-analysis/data/8-31-23/t_avg.npy")
# stdv = np.load("donut-analysis/data/8-31-23/area_stdv.npy")

if __name__ == "__main__":

    path = "origami/data/spring_tests/"
    y = np.load(path+"y_filtered.npy")
    x = np.load(path+"t.npy")
    # x = np.arange(0, len(area)*0.2, 0.2)

    
vol_dot_ml = vol_dot / 1e3 # ml/s
vol_dot_m = vol_dot / 1e9 # m^3/s

thrust_n = thrust_from_dvdt(vol_dot_m, area_m) # N
thrust_mn = thrust_n * 1e3 # mN

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