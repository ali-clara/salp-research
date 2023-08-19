from matplotlib import pyplot as plt
import numpy as np
from scipy.interpolate import splrep, splev
plt.style.use("seaborn")


data = np.load("data/filtered-area_8-16-23.npy") # mm^2
# data = data[20:]
# first = data[0]
# for i in range(500):
#     data = np.insert(data, 0, first)
fs = 60
x = np.arange(0, 1/fs*len(data), 1/fs)

f = splrep(x, data, s=len(x)*2) # mm^2

area_spline_fit = splev(x,f) # mm^2
area_dot = splev(x,f,der=1) # mm^2/s

fig, ax = plt.subplots(2,1)
ax[0].plot(x, data, label="filtered area data")
ax[0].plot(x, area_spline_fit, label="spline")
ax[0].set_ylabel("Area (mm^2)")

ax[1].plot(x, area_dot, label="1st derivative")
ax[1].set_ylabel("dA/dt mm^2/s")
# ax[1].invert_yaxis()
plt.legend(loc=0)
plt.tight_layout()

area_spline_fit = area_spline_fit / 1e6 # m^2
area_dot = area_dot / 1e6 # m^2/s

h = 150 # mm
h = h / 1000    # m 

v_dot = area_dot*h  # m^3/s

rho = 1000  # kg/m^3
c0 = 0.6    # dimensionless

thrust = rho*v_dot**2 / (c0 * area_spline_fit)

fig, ax = plt.subplots(2,1)
ax[0].plot(x, v_dot*1e6)
ax[0].set_title("change in volume: contraction phase")
ax[0].set_ylabel("mL/s")
ax[0].set_xlim([0,37])

ax[1].plot(x, thrust*1000)
ax[1].set_title("thrust")
ax[1].set_ylabel("thrust (mN)")
ax[1].set_xlim([0,37])
ax[1].set_ylim([-0.001, 0.015])

plt.legend(loc=0)
plt.tight_layout()
plt.show()
