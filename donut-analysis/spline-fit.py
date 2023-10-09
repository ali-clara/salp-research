from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import splrep, splev
# plt.style.use("seaborn")
import sys
sys.path.append("C:\\Users\\alicl\\Documents\\GitHub\\salp-research")
from create_paper_figure import MakePlot

# data = pd.read_csv("flow-modelling/vdot_model.csv")
# model_str = list(data.columns)
# model = [float(x) for x in model_str]
# t_model = np.arange(0, 30.1, 0.1)

area = np.load("donut-analysis/data/8-31-23/area_avg.npy") # mm^2
x = np.load("donut-analysis/data/8-31-23/t_avg.npy")
stdv = np.load("donut-analysis/data/8-31-23/area_stdv.npy")

fs = 60
initial_avg = np.mean(area[0:10*fs])
area[0:8*fs] = initial_avg # mm^2
area_m = area / 1e6 # m^2

h = 34 # mm
volume = area * h # mm^3

volume_spline = splrep(x, volume, s=len(x)*50*h)
vol_spline_fit = splev(x, volume_spline) # mm^3

vol_dot = splev(x, volume_spline, der=1) # mm^3/s
vol_dot_ml = vol_dot / 1e3 # ml/s
vol_dot_m = vol_dot / 1e9 # m^3/s

rho = 1000  # kg/m^3
c0 = 0.6    # dimensionless
thrust = rho*vol_dot_m**2 / (c0 * area_m) # N
thrust_mn = thrust * 1e3 # mN

fig, ax = plt.subplots(4,1)
ax[0].plot(x, area)
ax[1].plot(x, volume)
ax[1].plot(x, vol_spline_fit, label="volume spline fit")
ax[2].plot(x, vol_dot_ml)
ax[3].plot(x, thrust_mn)

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

# my_plot.set_savefig("donut-analysis/thrust-extrapolation.png")
# my_plot.label_and_save()