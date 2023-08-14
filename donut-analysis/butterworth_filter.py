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

def center_data_about_zero(data):
    bias_term = np.mean(data[0:40])
    data = data - bias_term
    return data, bias_term

def return_data_to_offset(data, bias_term):
    data = data + bias_term
    return data

def do_filtering_process(data, cutoff, fs, order, plot_freq_response=False):
    data_zeroed, data_bias = center_data_about_zero(data)
    data_filtered = butter_lowpass_filter(data_zeroed, cutoff, fs, order)
    data_filtered = return_data_to_offset(data_filtered, data_bias)

    if plot_freq_response == True:
        get_frequency_response(cutoff, fs, order)

    return data_filtered
    
if __name__ == "__main__":

    fs = 60.0       # sample rate, Hz

    # load data
    circ = np.load("data/circumference_8-3-23.npy")
    area = np.load("data/area_8-3-23.npy")
    t = np.arange(0, 1/fs*len(circ), 1/fs)

    # order = 2
    # fs = 30.0
    # cutoff = 0.07

    order = 2
    cutoff = 0.07  # desired cutoff frequency of the filter, Hz
    filtered_circ = do_filtering_process(circ, cutoff, fs, order)

    order = 1
    cutoff = 0.06
    filtered_area = do_filtering_process(area, cutoff, fs, order)

    fig, ax = plt.subplots(2,1)
    ax[0].plot(t, circ, '.', label='raw data')
    ax[0].plot(t, filtered_circ, '-', color="tab:red", linewidth=2, label='filtered data')
    ax[0].set_xlabel('Time [sec]')
    ax[0].legend()

    ax[1].plot(t, area, '.', label='raw data')
    ax[1].plot(t, filtered_area, '-', color="tab:red", linewidth=2, label='filtered data')
    ax[1].set_xlabel('Time [sec]')
    ax[1].legend()

    plt.show()

    np.save("data/filtered-circumference_8-11-23.npy", filtered_circ)
    np.save("data/filtered-area-data_8-11-23.npy", filtered_area)

    # data_to_export = list(zip(*[t, data, filtered_data, area]))
    # columns = ["time(sec)", "Raw circumference (mm)", "Filtered circumference (mm)", "Raw Area (mm^2)"]
    # df = pd.DataFrame(data_to_export, columns=columns)
    # df.to_csv("data/circumference_data_60fps.csv", index=False)




