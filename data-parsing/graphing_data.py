import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import pandas as pd

from create_paper_figure import MakePlot
import low_pass_filter
import first_order_fit


## -------------------- Global parameters -------------------- ##

# how much data to save on either side of the pulse
trim_index = 55
# rate at which data was taken (sec)
recording_frequency = 0.2
# length of input singnal pulse (sec)
pulse_length = 30

## -------------------- Preprocessing -------------------- ##

def g_to_mn(data):
    """ Convert data to milinewtons
    Args
        data - list of force values (g)"""
    mn = np.array(data) * 9.81
    return mn

def disp_to_strain(data, lg):
    """Args
        data - list of displacement values (mm)"""
    
    strain = (lg - np.array(data)) / lg
    return strain

def trim_data(data_list, input_signal):
    """Args
        force_data - list of force data to be trimmed
        input_signal - list of corresponding input data"""
    
    # find the first location of a '1' - pulse turned on
    pulse_start_index = input_signal.index(1)
    # find the first location of a '0' ~after~ the first '1' - pulse turned off
    pulse_stop_index = input_signal.index(0, pulse_start_index)
    # trim the force data according to those indices
    trimmed_data = data_list[pulse_start_index-trim_index:pulse_stop_index+trim_index+1]
    trimmed_input = input_signal[pulse_start_index-trim_index:pulse_stop_index+trim_index+1]

    return trimmed_data, trimmed_input

def create_time_vector(trimmed_force_data):
    """
    Args
        trimmed_force_data - one list of trimmed force data"""
    t_len = len(trimmed_force_data)
    t = np.arange(0, t_len*recording_frequency, recording_frequency)

    return t

def force_preprocessing(data_names, path):
    """
    Args 
        data_names - array of strings, names of the data to be preprocessed
        path - string, where the data lives
    Returns 
        big_data_array - array of raw force data (g)
        t - time (sec)"""
    big_data_array = []
    for name in data_names:
        data = pd.read_csv(path+name)
        force_data = data["Force (g)"].to_list()
        input_data = data["Input Signal"].to_list()

        force_data, input_data = trim_data(force_data, input_data)
        force_data = g_to_mn(force_data)
        big_data_array.append(force_data)

    t = create_time_vector(big_data_array[0])
    
    return big_data_array, t, np.array(input_data)


def strain_preprocessing(data_names, path, og_lengths):
    """
    Args 
        data_names - array of strings, names of the data to be preprocessed
        path - string, where the data lives
        og_lengths - resting length of TCA corresponding to each data collection
    Returns 
        big_data_array - array of raw strain data (mm)
        t - time (sec)"""
    big_data_array = []
    for i, name in enumerate(data_names):
        try:
            data = pd.read_csv(path+name)
            disp_data = data["Linear displacement (mm)"].to_list()
            input_data = data["Input Signal"].to_list()

            disp_data, input_data = trim_data(disp_data, input_data)
            strain_data = disp_to_strain(disp_data, og_lengths[i])

            big_data_array.append(strain_data)
        except FileNotFoundError:
            pass

    t = create_time_vector(big_data_array[0])
    
    return big_data_array, t, np.array(input_data)

## -------------------- Helper Functions -------------------- ##

def find_data_avg(big_data_array):
    """Args
        big_data_array - all the force data"""
    mean = np.mean(big_data_array, axis=0)
    st_dev = np.std(big_data_array, axis=0)

    return mean, st_dev

def filter_data(raw_data, t):
    filtered_data = []
    for data in raw_data:
        weights = np.concatenate((np.arange(0, 5), np.arange(0, 5)[::-1]))
        t_filtered, filtered = low_pass_filter.moving_weighted_average(t, 
                                                                data, 
                                                                steps_per_bin=len(weights),
                                                                weights=weights)
        filtered_data.append(filtered)

    return filtered_data, t_filtered

def align_yaxis(ax1, ax2):
    """Thanks Tim from stack overflow"""
    y_lims = np.array([ax.get_ylim() for ax in [ax1, ax2]])

    # force 0 to appear on both axes, comment if don't need
    y_lims[:, 0] = y_lims[:, 0].clip(None, 0)
    y_lims[:, 1] = y_lims[:, 1].clip(0, None)

    # normalize both axes
    y_mags = (y_lims[:,1] - y_lims[:,0]).reshape(len(y_lims),1)
    y_lims_normalized = y_lims / y_mags

    # find combined range
    y_new_lims_normalized = np.array([np.min(y_lims_normalized), np.max(y_lims_normalized)])

    # denormalize combined range to get new axes
    new_lim1, new_lim2 = y_new_lims_normalized * y_mags
    ax1.set_ylim(new_lim1)
    ax2.set_ylim(new_lim2)

###### ------------------ Flight Code ------------------ #########

if __name__ == "__main__":

    force_data_names = ["load-cell-data_1.csv", 
                        "load-cell-data_2.csv", 
                        "load-cell-data_3.csv"]

    strain_data_names = ["encoder-data_1.csv",
                        "encoder-data_1-1.csv",
                        "encoder-data_2.csv",
                        "encoder-data_3.csv"]

    encoder_tca_lengths_10g = [129.4, 129.4, 125.6, 106.2]

    assert len(strain_data_names) == len(encoder_tca_lengths_10g), "strain data and TCA lengths should match"

    def get_and_plot_force():
        power_input = ["1W", "2W", "3W", "4W"]

        my_plot = MakePlot()

        for power in power_input:
            data_path = "force_data/"+power+"/"
            raw_force_data, t, input_data = force_preprocessing(force_data_names, data_path)
            data_avg, data_stdv = find_data_avg(raw_force_data)

            ss_val = first_order_fit.find_ss(data_avg, tol=40)

            heating_params, cooling_params = first_order_fit.first_order_model(data_avg,
                                                                        t,
                                                                        ss_tolerance=15,
                                                                        trim_index=trim_index)
    
            k_h, tau_h, t_out_h, y_out_h = heating_params
            k_c, tau_c, t_out_c, y_out_c = cooling_params

            k_h = k_h/int(power[0])
            k_c = k_c/int(power[0])

            print(power)
            print(f"Heating: tau = {round(tau_h,3)}, k = {round(k_h,3)}")
            print(f"Cooling: tau = {round(tau_c,3)}, k = {round(k_c,3)}")

            my_plot.set_xy(t, data_avg)
            my_plot.set_stdev(data_stdv)
            my_plot.set_axis_labels("Time (sec)", "Force (mN)")
            my_plot.set_data_labels(power)
            my_plot.set_savefig("figs/force-figs/force-first-order-model.png")
            my_plot.plot_xy()

            # heating first order model
            my_plot.use_same_color()
            my_plot.set_xy(t_out_h, y_out_h, '--')
            my_plot.plot_xy()

            # cooling first order model
            my_plot.use_same_color()
            my_plot.set_xy(t_out_c, y_out_c, '--')
            my_plot.plot_xy()

        my_plot.label_and_save()


    def get_and_plot_strain():
        power_input = ["1W", "2W", "3W"]

        my_plot = MakePlot()

        for power in power_input:
            data_path = "encoder_data/"+power+"/"
            raw_strain_data, t, input_data = strain_preprocessing(strain_data_names, data_path, encoder_tca_lengths_10g)
            raw_data_avg, raw_data_stdv = find_data_avg(raw_strain_data)
            
            filtered_strain_data, filtered_t = filter_data(raw_strain_data, t)
            filtered_data_avg, filtered_data_stdv = find_data_avg(filtered_strain_data)

            k_h, tau_h, t_out_h, y_out_h = first_order_fit.find_first_order_sys(raw_data_avg, t, 
                                                                        start=55, stop=int(40/0.2), 
                                                                        type='decay', ss_tolerance=0.001,
                                                                        offset = 1.0)
            
            y_out_h = 1 - y_out_h

            k_h = k_h/int(power[0])
            # k_c = k_c/int(power[0])

            print(power)
            print(f"Heating: tau = {round(tau_h,3)}, k = {round(k_h,3)}")

            my_plot.set_axis_labels("Time (sec)", "Strain")
            my_plot.set_data_labels(power)
            
            # filtered data average
            # my_plot.set_xy(filtered_t, [filtered_data_avg])
            # my_plot.set_stdev([filtered_data_stdv])
            # my_plot.set_savefig("figs/encoder-figs/encoder-filtered-data.png")
            # my_plot.plot_xy()

            # raw data average
            my_plot.set_xy(t, raw_data_avg)
            my_plot.set_stdev(raw_data_stdv)
            my_plot.set_savefig("figs/encoder-figs/encoder-raw-data-model.pdf")
            my_plot.plot_xy()

            # heating first order model
            my_plot.use_same_color()
            my_plot.set_xy(t_out_h, y_out_h, '--')
            my_plot.plot_xy()

            # cooling first order model
            # my_plot.use_same_color()
            # my_plot.set_xy(t_out_c, y_out_c, '--')
            # my_plot.plot_xy()

            # raw data individuals
            # fig, ax = plt.subplots(1,1)
            # for data in raw_strain_data:
            #     ax.plot(t, data)
            
            # plt.show()

        my_plot.label_and_save()

    get_and_plot_strain()

