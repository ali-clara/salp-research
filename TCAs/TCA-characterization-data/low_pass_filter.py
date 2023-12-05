from numpy.lib.stride_tricks import as_strided
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def moving_weighted_average(x, y, step_size=1, steps_per_bin=10,
                            weights=None):
    # This ensures that all samples are within a bin
    number_of_bins = int(np.ceil(np.ptp(x) / step_size))
    bins = np.linspace(np.min(x), np.min(x) + step_size*number_of_bins,
                       num=number_of_bins+1)
    bins -= (bins[-1] - np.max(x)) / 2
    bin_centers = bins[:-steps_per_bin] + step_size*steps_per_bin/2

    counts, _ = np.histogram(x, bins=bins)
    vals, _ = np.histogram(x, bins=bins, weights=y)

    bin_avgs = vals / counts
    n = len(bin_avgs)
    windowed_bin_avgs = as_strided(bin_avgs,
                                   (n-steps_per_bin+1, steps_per_bin),
                                   bin_avgs.strides*2)

    weighted_average = np.average(windowed_bin_avgs, axis=1, weights=weights)

    return bin_centers, weighted_average

def create_time_vector(trimmed_force_data):
    """
    Args
        trimmed_force_data - one list of trimmed force data"""
    recording_frequency = 0.2
    t_len = len(trimmed_force_data)
    t = np.arange(0, t_len*recording_frequency, recording_frequency)

    return t

def trim_data(data_list, input_signal):
    """Args
        force_data - list of force data to be trimmed
        input_signal - list of corresponding input data"""
    
    trim_index = 60
    # find the first location of a '1' - pulse turned on
    pulse_start_index = input_signal.index(1)
    # find the first location of a '0' ~after~ the first '1' - pulse turned off
    pulse_stop_index = input_signal.index(0, pulse_start_index)
    # trim the force data according to those indices
    trimmed_data = data_list[pulse_start_index-trim_index:pulse_stop_index+trim_index+1]
    trimmed_input = input_signal[pulse_start_index-trim_index:pulse_stop_index+trim_index+1]

    return trimmed_data, trimmed_input

if __name__ == "__main__":
    #plot the moving average with triangular weights
    weights = np.concatenate((np.arange(0, 5), np.arange(0, 5)[::-1]))

    disp_data_names = ["encoder-data_1.csv",
                         "encoder-data_2.csv",
                         "encoder-data_3.csv"]
    
    for name in disp_data_names:

        data = pd.read_csv("encoder_data/3W/"+name)
        
        raw_data = data["Linear displacement (mm)"].tolist()
        input_signal = data["Input Signal"].to_list()
        
        y, _ = trim_data(raw_data, input_signal)
        x = create_time_vector(y)

        bins, average = moving_weighted_average(x, y, steps_per_bin=len(weights),
                                                weights=weights)

        plt.plot(bins, average, label='moving average')
        plt.plot(x, y, '.')

    plt.show()