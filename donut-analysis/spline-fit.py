from matplotlib import pyplot as plt
import numpy as np
from scipy.interpolate import splrep, splev
plt.style.use("seaborn")


data = np.load("data/8-31-23/area_avg.npy") # mm^2
x = np.load("data/8-31-23/t_avg.npy")

fs = 60
initial_avg = np.mean(data[0:10*fs])
data[0:8*fs] = initial_avg

# data = data[20:]
# first = data[0]
# for i in range(500):
#     data = np.insert(data, 0, first)

# x = np.arange(0, 1/fs*len(data), 1/fs)

f = splrep(x, data, s=len(x)*1.5) # mm^2

area_spline_fit = splev(x,f) # mm^2
area_dot = splev(x,f,der=1) # mm^2/s

fig, ax = plt.subplots(2,1)
ax[0].plot(x, data, label="unfiltered average area data")
ax[0].plot(x, area_spline_fit, label="spline fit")
ax[0].set_ylabel("Area (mm^2)")
ax[0].set_xlabel("Time (sec)")
ax[0].set_title("Donut Area")
ax[0].legend(loc=0)

ax[1].plot(x, area_dot, label="splev 1st derivative")
ax[1].set_ylabel("dA/dt mm^2/s")
ax[1].set_xlabel("Time (sec)")
# ax[1].invert_yaxis()
ax[1].set_title("Donut Change in Area")
ax[1].legend(loc=0)
plt.tight_layout()

area_spline_fit = area_spline_fit / 1e6 # m^2
area_dot = area_dot / 1e6 # m^2/s

h = 3.3 # mm
h = h / 1000    # m 

v_dot = area_dot*h  # m^3/s

rho = 1000  # kg/m^3
c0 = 0.6    # dimensionless

thrust = rho*v_dot**2 / (c0 * area_spline_fit)

fig, ax = plt.subplots(2,1)
ax[0].plot(x, v_dot*1e6)
ax[0].set_title("Change in volume during contraction phase")
ax[0].set_ylabel("mL/s")
ax[0].set_xlabel("Time (sec)")
ax[0].set_xlim([0,30])

ax[1].plot(x, thrust*1000)
ax[1].set_title("Thrust during contraction phase")
ax[1].set_ylabel("thrust (mN)")
ax[1].set_xlabel("Time (sec)")
ax[1].set_xlim([0,30])
# ax[1].set_ylim([-0.001, 0.035])

plt.legend(loc=0)
plt.tight_layout()
plt.show()
