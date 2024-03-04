import numpy as np
from scipy.signal import butter, lfilter, freqz
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use("seaborn")

def butter_lowpass(cutoff, fs, order=5):
    return butter(order, cutoff, fs=fs, btype='low', analog=False)

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def get_frequency_response(cutoff, fs, order):
    # Plot the frequency response.

    # Get the filter coefficients so we can check its frequency response.
    b, a = butter_lowpass(cutoff, fs, order)
    w, h = freqz(b, a, fs=fs, worN=8000)

    fig, ax = plt.subplots(1,1)
    ax.plot(w, np.abs(h), 'b')
    ax.plot(cutoff, 0.5*np.sqrt(2), 'ko')
    ax.axvline(cutoff, color='k')
    ax.set_xlim(0, 0.5*fs)
    ax.set_title("Lowpass Filter Frequency Response")
    ax.set_xlabel('Frequency [Hz]')
    ax.grid()

    plt.show()

def nan_interpolation(y):
    """Helper function to interpolate NAN values
    https://stackoverflow.com/questions/6518811/interpolate-nan-values-in-a-numpy-array"""
    nans = np.isnan(y)
    x = lambda z: z.nonzero()[0]
    y[nans]= np.interp(x(nans), x(~nans), y[~nans])

    return y

def center_data_about_zero(data):
    bias_term = np.mean(data[0:10])
    data = data - bias_term
    return data, bias_term

def return_data_to_offset(data, bias_term):
    data = data + bias_term
    return data

def do_filtering_process(data, cutoff, fs, order, plot_freq_response=False):
    data_interp = nan_interpolation(data)
    data_zeroed, data_bias = center_data_about_zero(data_interp)
    data_filtered = butter_lowpass_filter(data_zeroed, cutoff, fs, order)
    data_filtered = return_data_to_offset(data_filtered, data_bias)

    if plot_freq_response == True:
        get_frequency_response(cutoff, fs, order)

    return data_filtered
    
if __name__ == "__main__":

    fs = 30.0       # sample rate, Hz

    # load data
    file_name = "avg" 
    file_date = "8-31-23"
    # circ = np.load("data/"+file_date+"/circ_"+file_name+".npy")
    path = "origami/data/spring_tests/"
    y = np.load(path+"y_dist.npy")
    x = np.load(path+"t.npy")

    # area
    order = 2
    cutoff = 0.2
    filtered_y = do_filtering_process(y, cutoff, fs, order)

    fig, ax = plt.subplots()
    ax.plot(x, y, label='raw data')
    ax.plot(x-1, filtered_y, color="tab:red", linewidth=2, label='filtered data')
    ax.set_xlabel('Time [sec]')
    ax.legend()

    plt.tight_layout()
    plt.show()

    np.save(path+"y_filtered.npy", filtered_y)

    # np.save("data/"+file_date+"/circ_"+file_name+"_filtered.npy", filtered_circ)
    # np.save("data/"+file_date+"/area_"+file_name+"_filtered.npy", filtered_area)

    # data_to_export = list(zip(*[t, data, filtered_data, area]))
    # columns = ["time(sec)", "Raw circumference (mm)", "Filtered circumference (mm)", "Raw Area (mm^2)"]
    # df = pd.DataFrame(data_to_export, columns=columns)
    # df.to_csv("data/circumference_data_60fps.csv", index=False)




