import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

#Data:
x = np.linspace(0,2*np.pi,100)
f = np.sin(x) + .02*(np.random.rand(100)-.5)

#Normalization:
dx = x[1] - x[0] # use np.diff(x) if x is not uniform

#First derivatives:
df = np.diff(f) / dx
cf = np.convolve(f, [1,-1]) / dx
gf = ndimage.gaussian_filter1d(f, sigma=1, order=1, mode='wrap') / dx

#Plotting:
plt.figure()
plt.plot(x, f, 'k', lw=2, label='original')
plt.plot(x[:-1], df, 'r.', label='np.diff, 1')
plt.plot(x, cf[:-1], 'r--', label='np.convolve, [1,-1]')
plt.plot(x, gf, 'r', label='gaussian, 1')

plt.show()