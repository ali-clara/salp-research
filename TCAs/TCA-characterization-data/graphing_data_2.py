import numpy as np
import pandas as pd
import glob

import sys
sys.path.append("C:\\Users\\alicl\\Documents\\GitHub\\salp-research")
from create_paper_figure import MakePlot
import low_pass_filter
import first_order_fit_2

import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

def trim_data(data_array, trim_from=0, trim_to=None):
    """Trims a np.array or all nested elements of a np.array to be the same length"""
    # remember the original shape, in case that was important
    original_shape = data_array.shape
    flattened = data_array.flatten()

    if trim_to is None:
        lengths = [len(data) for data in flattened]
        trim_to = min(lengths)

    for i, data in enumerate(flattened):
        flattened[i] = data[trim_from:trim_to]

    reshaped = flattened.reshape(original_shape)
    return reshaped

def average_data(data_list):
    mean = np.mean(data_list)
    stdv = np.std(data_list)
    return mean, stdv

def create_time_vector(data, recording_frequency=0.2):
    t_len = len(data)
    t = np.arange(0, t_len*recording_frequency, recording_frequency)
    return t

def load_and_compile(path, subfolder_names, y_data_name, x_data_name, plot=True):
    data_means = []
    data_stdvs = []
    times = []
    for folder in subfolder_names:
        subfolder_data = []
        subfolder_times = []
        for file in glob.glob(path+"\\"+str(folder)+"\\*.csv"):
            data = pd.read_csv(file)
            response = data[y_data_name].to_numpy()
            subfolder_data.append(response)
            try:
                time = data[x_data_name].to_numpy()
                subfolder_times.append(time)
            except:
                time = create_time_vector(response)
                subfolder_times.append(time)

            if plot:
                plt.plot(time, response)
                plt.xlabel(x_data_name)
                plt.ylabel(y_data_name)
        
        # squish data and timestamp into a big np array
        # there's gotta be a way to do this that's not a for loop but I can't find it
        big_data = np.empty(shape=(2, len(subfolder_data)), dtype=object)
        for i, data in enumerate(subfolder_data):
            big_data[0,i] = subfolder_times[i]
            big_data[1,i] = data

        # trim it all the same length
        trimmed_big_data = trim_data(big_data)
        # take the mean and standard deviation
        mean, stdv = average_data(trimmed_big_data[1:])
        data_means.append(mean)
        data_stdvs.append(stdv)
        # is this kosher?
        time = np.mean(trimmed_big_data[0:][0])
        times.append(time)

    plt.show()
    return np.array(data_means, dtype=object), np.array(data_stdvs, dtype=object), np.array(times, dtype=object)

def disp_to_strain(mean_array, stdv_array, l_0):
    """Takes in np arrays of delX (mean + stdv) and original length and converts to strain"""
    strain = mean_array / l_0
    strain_stdv = stdv_array / l_0

    return strain, strain_stdv

def g_to_mn(data):
    """ Convert data to milinewtons
    Args
        data - list of force values (g)"""
    mn = np.array(data.tolist(), dtype=float) * 9.81
    return mn

if __name__ == "__main__":
    test_folder_path = "characterization-length\\force-length"
    disp_folder_path = "0.8mm\\strain"
    force_folder_path = "0.8mm\\force"
    cold_force_folder_path = "cold\\force"

    test = True
    plot_strain = False
    plot_force = False
    compare_temperature = False

    data_type = "Force (g)"
    x_axis = "Time (sec)"

    if test:
        means, stdvs, times =  load_and_compile(test_folder_path, subfolder_names=["0.5A"], y_data_name=data_type, x_data_name=x_axis)
        for i, data in enumerate(means):
            t = times[i]

            data = np.array(data.tolist(), dtype=float)
            stdv = np.array(stdvs[i].tolist(), dtype=float)
            
            if data_type == "Force (g)":
                data = g_to_mn(data)
                stdv = g_to_mn(stdvs[i])
            elif data_type == "Linear displacement (mm)":
                data, stdv = disp_to_strain(data, stdvs[i], l0=None) # <-- fill in l0, otherwise will throw error
            else:
                print("Plotting raw data")

            plt.plot(t, data)
            # plt.fill_between(t, data+stdv, data-stdv, alpha=0.5)

        plt.ylabel("Force (mN)")
        plt.xlabel("Time (sec)")
        # plt.legend(["4W", "6W", "8W"])
        # plt.title("Spring response, unpowered")
        plt.show()


    if plot_strain:
        disp_mean, disp_stdv, times = load_and_compile(disp_folder_path, subfolder_names=["1W", "2W", "3W", "4W"], data_name="Linear displacement (mm)")
        strain_mean, strain_stdv = disp_to_strain(disp_mean, disp_stdv, l_0=np.array([137.1, 135.8, 149.7, 134.6]))
        # strain_mean = disp_mean
        # np.save("4w-strain-avg.npy", strain_mean)
        # strain_stdv = disp_stdv
        my_plot = MakePlot()
        for i, strain in enumerate(strain_mean):
            t = times[i]
            my_plot.set_xy(t, strain)
            my_plot.set_stdev(strain_stdv[i])
            my_plot.set_data_labels(str(i+1)+"W")
            my_plot.set_axis_labels("Time (s)", "Strain")
            my_plot.set_xlim([0,60])
            my_plot.plot_xy()
        
        my_plot.set_savefig("paper-strain-data.pdf")
        my_plot.label_and_save()

    if plot_force:
        force_means, force_stdvs, times = load_and_compile(force_folder_path, subfolder_names=["1W", "2W", "3W", "4W"], data_name="Force (g)")
        my_plot = MakePlot()
        for i, force in enumerate(force_means):
            t = times[i]
            force = g_to_mn(force)
            force_stdv = g_to_mn(force_stdvs[i])
            my_plot.set_xy(t-15, force)
            my_plot.set_stdev(force_stdv)
            my_plot.set_data_labels(str(i+1)+"W")
            my_plot.set_axis_labels("Time (s)", "Force (mN)")
            my_plot.set_xlim([0,50])
            my_plot.plot_xy()

        my_plot.set_savefig("paper-force-data.png")
        my_plot.label_and_save()

    if compare_temperature:
        norm_means, norm_stdvs, times =  load_and_compile("26AWG\\force", subfolder_names=["3W"], data_name="Force (g)")
        oil_means, oil_stdvs, cold_times = load_and_compile("cold-oil\\force", subfolder_names=["6W"], data_name="Force (g)")
        water_means, water_stdvs, water_times = load_and_compile("cold-di-water\\force", subfolder_names=["8W"], data_name="Force (g)")
        for i, norm_force in enumerate(norm_means):
            t = times[i]
            ot = cold_times[i]
            wt = water_times[i]

            norm_force = g_to_mn(norm_force)
            norm_std = g_to_mn(norm_stdvs[i])

            cold_force = g_to_mn(oil_means[i])
            cold_std = g_to_mn(oil_stdvs[i])

            water_force = g_to_mn(water_means[i])
            water_std = g_to_mn(water_stdvs[i])

            plt.plot(t, norm_force, label="3W Room Temp")
            plt.plot(ot, cold_force, label="6W Cold Oil")
            plt.plot(wt, water_force, label="8W Cold DI Water")

        plt.ylabel("Force (mN)")
        plt.xlabel("Time (s)")
        plt.legend()
        plt.show()
        