import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
plt.style.use("seaborn")
import sys

sys.path.append("C:\\Users\\alicl\\Documents\\GitHub\\tvregdiff")
from tvregdiff import TVRegDiff

data = np.load("data/area_8-3-23.npy") # mm^2

# a little sneaky sneaky
data = data[20:]
first = data[0]
for i in range(300):
    data = np.insert(data, 0, first)

fs = 60
x = np.arange(0, 1/fs*len(data), 1/fs)
dx = 1/fs

dydx = TVRegDiff(data, 50, 1e3, plotflag=False, scale="small", dx=dx, diffkernel="sq", precondflag=True, cgmaxit=200) # mm^2/s

dydx_m = dydx / 1e6

h = 3.3 / 1000  # 3.3 mm thick in meters
dvdx = dydx_m * h

fig, ax = plt.subplots(2,1)
ax[0].scatter(x, data)
ax[0].set_xlabel("Time (sec)")
ax[0].set_ylabel("Area (mm^2)")

ax[1].plot(x, dydx)
ax[1].set_xlabel("Time (sec)")
ax[1].set_ylabel("Change in Area (mm^2/s)")

plt.tight_layout()

# fig, ax = plt.subplots(2,1)
# ax[0].plot(x, dvdx)
# ax[0].set_xlabel("Time (sec)")
# ax[0].set_ylabel("Change in Volume (m^3/s)")

# plt.tight_layout()
plt.show()