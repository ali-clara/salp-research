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

def trim_data(data_list):
    lengths = [len(data) for data in data_list]
    trim_to = min(lengths)

    for i, data in enumerate(data_list):
        data_list[i] = data[0:trim_to]

    return data_list

def average_data(data_list):
    mean = np.mean(data_list, axis=0)
    stdv = np.std(data_list, axis=0)
    return mean, stdv

def create_time_vector(data, recording_frequency=0.2):
    t_len = len(data)
    t = np.arange(0, t_len*recording_frequency, recording_frequency)
    return t

def load_and_compile(path):
    subfolder_names = ["1W", "2W", "3W"]
    data_means = []
    data_stdvs = []
    for folder in subfolder_names:
        subfolder_data = []
        for file in glob.glob(path+"\\"+str(folder)+"\\*.csv"):
            data = pd.read_csv(file)
            labels = data.keys()
            response = data[labels[0]].to_numpy()
            time = data[labels[1]]
            subfolder_data.append(response)

        trimmed_data = trim_data(subfolder_data)
        mean, stdv = average_data(trimmed_data)
        data_means.append(mean)
        data_stdvs.append(stdv)

    return data_means, data_stdvs

def disp_to_strain(mean_list, stdv_list, l_0):
    """should be eliminated after I redo data collection with the measured length included in each csv"""
    strain = []
    strain_stdv = []
    for i, mean in enumerate(mean_list):
        stdv = stdv_list[i]
        strain.append(mean / l_0)
        strain_stdv.append(stdv / l_0)

    return strain, strain_stdv

def g_to_mn(data):
    """ Convert data to milinewtons
    Args
        data - list of force values (g)"""
    mn = np.array(data) * 9.81
    return mn

if __name__ == "__main__":
    disp_folder_path = "26AWG\\strain"
    force_folder_path = "26AWG\\force"

    plot_strain = True
    plot_force = False
    
    if plot_strain:
        disp_mean, disp_stdv = load_and_compile(disp_folder_path)
        # strain_mean, strain_stdv = disp_to_strain(disp_mean, disp_stdv, l_0=53)
        strain_mean = disp_mean
        strain_stdv = disp_stdv
        for i, strain in enumerate(strain_mean):
            t = create_time_vector(strain)
            plt.plot(t, strain, label=str(i+1)+"W")
            plt.fill_between(t, strain+strain_stdv[i], strain-strain_stdv[i], alpha=0.5)

        plt.ylabel("Strain")
        plt.xlabel("Time (s)")
        plt.title("26AWG")
        plt.legend()
        # plt.savefig("26awg-strain.png")
        plt.show()

    if plot_force:
        force_means, force_stdvs = load_and_compile(force_folder_path)
        for i, force in enumerate(force_means):
            t = create_time_vector(force)
            force = g_to_mn(force)
            force_stdv = g_to_mn(force_stdvs[i])
            plt.plot(t, force, label=str(i+1)+"W")
            plt.fill_between(t, force+force_stdv, force-force_stdv, alpha=0.5)

        plt.ylabel("Force (mN)")
        plt.xlabel("Time (s)")
        plt.title("26AWG")
        plt.legend()
        plt.savefig("26awg-force.png")
        plt.show()

    t1 = np.load("donut-analysis/data/8-31-23/t_avg.npy")
    y1 = np.load("donut-analysis/data/8-31-23/area_avg.npy")
    y2 = np.load("donut-analysis/data/12-15-23/area_4W.npy") + 30
    t2 = np.load("donut-analysis/data/12-15-23/t_4W.npy") + 5

    plt.plot(t1, y1, '.', label="0.8mm, 5W")
    plt.plot(t2, y2, '.', label="0.4mm, 4W")
    plt.xlabel("Time (sec)")
    plt.ylabel("Area (mm^2)")
    plt.title("Embedded TCA Cross Section Comparison")
    plt.legend()
    plt.show()

        