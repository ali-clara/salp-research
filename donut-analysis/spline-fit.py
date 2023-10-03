from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import splrep, splev
plt.style.use("seaborn")

data = pd.read_csv("flow-modelling/vdot_model.csv")
model_str = list(data.columns)
model = [float(x) for x in model_str]
t_model = np.arange(0, 30.1, 0.1)

area = np.load("donut-analysis/data/8-31-23/area_avg.npy") # mm^2
x = np.load("donut-analysis/data/8-31-23/t_avg.npy")

fs = 60
initial_avg = np.mean(area[0:10*fs])
area[0:8*fs] = initial_avg # mm^2
area_m = area / 1e6 # m^2

h = 3.3
volume = area * h # mm^3

volume_spline = splrep(x, volume, s=len(x)*18)
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


