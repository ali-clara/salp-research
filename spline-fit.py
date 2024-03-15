from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import splrep, splev
from create_paper_figure import MakePlot

def nan_interpolation(y):
    """Helper function to interpolate NAN values
    https://stackoverflow.com/questions/6518811/interpolate-nan-values-in-a-numpy-array"""
    nans = np.isnan(y)
    x = lambda z: z.nonzero()[0]
    y[nans]= np.interp(x(nans), x(~nans), y[~nans])

    return y

def fit_spline(x, y, s, derivative=0):
    """Uses splrep and splev to fit a spline to the data. Differentiates based on the given
        derivative term.
        s- constant int or float, smoothing. Larger s = more smoothing
        returns - array of same length as x and y
    """
    spline = splrep(x, y, s=s)
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

if __name__ == "__main__":

    path = "soft-bodies/origami/data/spring2/6W/"
    y = np.load(path+"average.npy")
    x = np.load(path+"t.npy")
    # x = np.arange(0, len(area)*0.2, 0.2)

    smoothing = 0.15
    y_fit = fit_spline(x, y, s=smoothing)
    y_dot_fit = fit_spline(x, y, s=smoothing, derivative=1)

    fig, ax = plt.subplots(2,1)
    ax[0].plot(x, y)
    ax[0].plot(x, y_fit)
    ax[0].set_ylabel("Y")
    ax[1].plot(x, y_dot_fit)
    ax[1].set_ylabel("dY/dt")
    plt.show()

    