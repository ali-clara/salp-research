import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import pandas as pd
import control

from create_paper_figure import MakePlot


## -------------------- Global parameters -------------------- ##

# how much data to save on either side of the pulse
trim_index = 75
# rate at which data was taken (sec)
recording_frequency = 0.2
# length of input singnal pulse (sec)
pulse_length = 30

## -------------------- Preprocessing -------------------- ##

# convert to milinewtons
def g_to_mn(data):
    """Args
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
        big_data_array - array of raw force data (mN)
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
        big_data_array - array of raw force data (mN)
        t - time (sec)"""
    big_data_array = []
    for i, name in enumerate(data_names):
        data = pd.read_csv(path+name)
        disp_data = data["Linear displacement (mm)"].to_list()
        input_data = data["Input Signal"].to_list()

        disp_data, input_data = trim_data(disp_data, input_data)
        strain_data = disp_to_strain(disp_data, og_lengths[i])
        big_data_array.append(strain_data)

    t = create_time_vector(big_data_array[0])
    
    return big_data_array, t, np.array(input_data)
## -------------------- Helper Functions -------------------- ##

def find_data_avg(big_data_array):
    """Args
        big_data_array - all the force data"""
    mean = np.mean(big_data_array, axis=0)
    st_dev = np.std(big_data_array, axis=0)

    return mean, st_dev

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


## -------------------- First Order Modeling -------------------- ##
def find_k(data, start, stop):
    data = data[start:stop]
    k = max(data)
    return k

def find_tau(data, time, start, stop, ss_val=None, type='growth'):
    """Returns - time constant, 
                steady state value"""
    # slice arrays to area of interest
    data = data[start:stop]
    time = time[start:stop]

    if ss_val == None:
        ss_val = max(data)
    
    val_at_t63 = ss_val*0.63

    if type == 'growth':
        index_at_t63 = np.where(np.isclose(data, val_at_t63, atol=2.6))[0][0]
    
    if type == 'decay':
        data = ss_val - data
        index_at_t63 = np.where(np.isclose(data, val_at_t63, atol=3.1))[0][0]
    
    tau = time[index_at_t63] - time[0]

    return tau

def find_first_order_sys(force_data, t, start, stop, type):
    k = find_k(force_data, start, stop)
    tau = find_tau(force_data, t, start, stop, type=type)
    num = [k]
    den = [tau, 1]
    sys = control.TransferFunction(num, den)
    t_sim = np.linspace(t[start], t[stop], 1000)
    t_out, y_out = control.step_response(sys, t_sim)

    return k, tau, t_out, y_out

def first_order_model(force_data, t):
    pulse_start_index = trim_index
    pulse_length_index = int(pulse_length / recording_frequency)
    pulse_stop_index = pulse_start_index+pulse_length_index

    # heating
    k_h, tau_h, t_out_h, y_out_h = find_first_order_sys(force_data, t, pulse_start_index, pulse_stop_index, type="growth")
    # cooling
    k_c, tau_c, t_out_c, y_out_c = find_first_order_sys(force_data, t, pulse_stop_index, -1, type="decay")

    print(f"Heating: tau = {tau_h}, k = {k_h}")
    print(f"Cooling: tau = {round(tau_c,4)}, k = {k_c}")

    return [k_h, tau_h, t_out_h, y_out_h], [k_c, tau_c, t_out_c, y_out_c]

def growth_to_decay(growth_data):
    ss = max(growth_data)
    decay = ss - growth_data
    return decay


###### ------------------ Flight Code ------------------ #########

power_input = ["1W", "2W", "3W"]
# power_input = ["4W"]

force_data_names = ["load-cell-data_1.csv", 
                    "load-cell-data_2.csv", 
                    "load-cell-data_3.csv"]

strain_data_names = ["encoder-data_1.csv",
                     "encoder-data_2.csv",
                     "encoder-data_3.csv"]

encoder_tca_lengths_10g = [129.4, 125.6, 106.2]

def get_and_plot_force():
    my_plot = MakePlot()

    for power in power_input:
        data_path = "force_data/"+power+"/"
        raw_force_data, t, input_data = force_preprocessing(force_data_names, data_path)
        data_avg, data_stdv = find_data_avg(raw_force_data)

        # heating_params, cooling_params = first_order_model(data_avg, t)

        my_plot.set_xy(t, [data_avg])
        my_plot.set_stdev([data_stdv])
        my_plot.set_axis_labels("Time (sec)", "Force (mN)")
        my_plot.set_data_labels([power])
        my_plot.set_savefig("testfig.png")

        my_plot.plot_xy()

    my_plot.label_and_save()


def get_and_plot_strain():
    my_plot = MakePlot()

    for power in power_input:
        data_path = "encoder_data/"+power+"/"
        raw_strain_data, t, input_data = strain_preprocessing(strain_data_names, data_path, encoder_tca_lengths_10g)
        data_avg, data_stdv = find_data_avg(raw_strain_data)

        my_plot.set_xy(t, [data_avg])
        my_plot.set_stdev([data_stdv])
        my_plot.set_axis_labels("Time (sec)", "Strain")
        my_plot.set_data_labels([power])
        my_plot.set_savefig("testfig.png")

        my_plot.plot_xy()

    my_plot.label_and_save()


get_and_plot_strain()

