from matplotlib import pyplot as plt
import numpy as np
from scipy.interpolate import splrep, splev


data = np.load("data/filtered-area-data_8-11-23.npy") # mm^2
fs = 60
x = np.arange(0, 1/fs*len(data), 1/fs)

f = splrep(x, data, s=len(x)*2) # mm^2

area_spline_fit = splev(x,f) # mm^2
area_dot = splev(x,f,der=1) # mm^2/s

fig, ax = plt.subplots(1,1)
ax.plot(x, data, label="noisy data")
ax.plot(x, area_spline_fit, label="fitted")
ax.set_title("donut area")
ax.set_ylabel("mm^2")
ax.legend(loc=0)

area_spline_fit = area_spline_fit / 1e6 # m^2
area_dot = area_dot / 1e6 # m^2/s

h = 0.01 # mm
h = h / 1000 # m

v_dot = area_dot*h # m^3/s

rho = 1000 # kg/m^3
c0 = 0.6 

thrust = rho*v_dot**2 / (c0 * area_spline_fit[0])

fig, ax = plt.subplots(3,1)
ax[0].plot(x, area_dot, label="1st derivative")
ax[0].set_title("change in area")
ax[0].set_ylabel("m^2/s")

ax[1].plot(x, v_dot)
ax[1].set_title("change in volume")
ax[1].set_ylabel("m^3/s")

ax[2].plot(x, thrust)
ax[2].set_title("thrust")

plt.legend(loc=0)
plt.tight_layout()
plt.show()
