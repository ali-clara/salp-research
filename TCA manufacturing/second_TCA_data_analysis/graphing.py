import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

### ------ Data Parsing ------ ###

mandrel_data = pd.read_csv("data-collection_mandrel-coiled.csv")
nucleated_data = pd.read_csv("data-collection_self-coiled.csv")

t = np.array(mandrel_data["t"])

# 400g, self-coiled, 1 watt, free convection
s_w1_g400_1 = np.array(nucleated_data["400g_1w_free"])
s_w1_g400_2 = np.array(nucleated_data["400g_1w_free.1"])
# 400g, self-coiled, 3 watts, free convection
s_w3_g400_1 = np.array(nucleated_data["400g_3w_free"])
s_w3_g400_2 = np.array(nucleated_data["400g_3w_free.1"])

# 40g, mandrel-coiled, 1 watt, free convection
m_w1_g40_1 = np.array(mandrel_data["40g_1w_free"])
m_w1_g40_2 = np.array(mandrel_data["40g_1w_free.1"])
# 40g, mandrel-coiled, 3 watts, free convection
m_w3_g40_1 = np.array(mandrel_data["40g_3w_free"])
m_w3_g40_2 = np.array(mandrel_data["40g_3w_free.1"])
# 20g, mandrel-coiled, 3 watts, free convection
m_w3_g20 = np.array(mandrel_data["20g_3w_free"])
# 0g, mandrel-coiled, 3 watts, free convection
m_w3_g0 = np.array(mandrel_data["0g_3w_free"])

self_coiled_arrays = [s_w1_g400_1, s_w1_g400_2, s_w3_g400_1, s_w3_g400_2]
mandrel_coiled_arrays = [m_w1_g40_1, m_w1_g40_2, m_w3_g40_1, m_w3_g40_2]

# adjust for initial length
# start_pos = 2.5 # cm
def adjust_start_pos(array, start_pos=2.5):
    array = array - start_pos
    return array

s_w1_g400_1 = adjust_start_pos(s_w1_g400_1)
s_w1_g400_2 = adjust_start_pos(s_w1_g400_2)
s_w3_g400_1 = adjust_start_pos(s_w3_g400_1)
s_w3_g400_2 = adjust_start_pos(s_w3_g400_2)

m_w1_g40_1 = adjust_start_pos(m_w1_g40_1)
m_w1_g40_2 = adjust_start_pos(m_w1_g40_2)
m_w3_g40_1 = adjust_start_pos(m_w3_g40_1)
m_w3_g40_2 = adjust_start_pos(m_w3_g40_2)
m_w3_g20 = adjust_start_pos(m_w3_g20)
m_w3_g0 = adjust_start_pos(m_w3_g0)

### ------ Helper Functions ------ ###

def calc_mean_and_error(data):
    """data: array of arrays"""
    mean = np.mean(data, axis=0)
    st_dev = np.std(data, axis=0)
    return mean, st_dev

def calc_strain(l_0, l):
    """l_0 - initial length, l - current length"""
    return (l_0 - l) / l

def calc_displacement(l_0, l):
    return l_0, l

def get_strain(data_list):
    """data_list: list of arrays"""
    strains = []
    for data in data_list:
        strain = []
        l_0 = data[0]
        for length in data:
            strain.append(calc_strain(l_0, length))
        strains.append(strain)
    
    return strains

def get_data_to_plot(data_list):
    disp_avg, disp_stdv = calc_mean_and_error(data_list)
    strain_list = get_strain(data_list)
    strain_avg, strain_stdv = calc_mean_and_error(strain_list)

    return disp_avg, disp_stdv, strain_avg, strain_stdv


### ------ Flight Code ------ ###
s_w1_g400_disp_avg, s_w1_g400_disp_stdv, s_w1_g400_strain_avg, s_w1_g400_strain_stdv = get_data_to_plot([s_w1_g400_1, s_w1_g400_2])
s_w3_g400_disp_avg, s_w3_g400_disp_stdv, s_w3_g400_strain_avg, s_w3_g400_strain_stdv = get_data_to_plot([s_w3_g400_1, s_w3_g400_2])

m_w1_g40_disp_avg, m_w1_g40_disp_stdv, m_w1_g40_strain_avg, m_w1_g40_strain_stdv = get_data_to_plot([m_w1_g40_1, m_w1_g40_2])
m_w3_g40_disp_avg, m_w3_g40_disp_stdv, m_w3_g40_strain_avg, m_w3_g40_strain_stdv = get_data_to_plot([m_w3_g40_1, m_w3_g40_2])

m_w3_g20_disp_avg, m_w3_g20_disp_stdv, m_w3_g20_strain_avg, m_w3_g20_strain_stdv = get_data_to_plot([m_w3_g20])
m_w3_g0_disp_avg, m_w3_g0_disp_stdv, m_w3_g0_strain_avg, m_w3_g0_strain_stdv = get_data_to_plot([m_w3_g0])

m_strain_avg = m_w1_g40_strain_avg
m_strain_stdv = m_w1_g40_strain_stdv
m_disp_avg = m_w1_g40_disp_avg
m_disp_stdv = m_w1_g40_disp_stdv

s_strain_avg = s_w1_g400_strain_avg
s_strain_stdv = s_w1_g400_strain_stdv
s_disp_avg = s_w1_g400_disp_avg
s_disp_stdv = s_w1_g400_disp_stdv


# plot 1: Mandrel coiled: 3W free, 1W free, 3W forced

# plot 2: Mandrel coiled: 40g, 20g, 0g
def do_plot_2():

    plt.style.use("seaborn")
    fig, ax = plt.subplots(2,1)
    # strain
    ax[0].errorbar(t, m_w3_g40_strain_avg, yerr=m_w3_g40_strain_stdv, capsize=3, capthick=1, label="40 grams")
    ax[0].errorbar(t, m_w3_g20_strain_avg, yerr=m_w3_g20_strain_stdv, label="20 grams")
    ax[0].errorbar(t, m_w3_g0_strain_avg, yerr=m_w3_g0_strain_stdv, label="0 grams")
    ax[0].set_title("Strain vs Time")
    ax[0].set_xlabel("Time (sec)")
    ax[0].set_ylabel("Strain")
    ax[0].set_title("Mandrel Coiled TCA Strain Response to 3W, 0.05Hz Square Wave")
    ax[0].legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
    # displacement
    ax[1].errorbar(t, m_w3_g40_disp_avg, yerr=m_w3_g40_disp_stdv, capsize=3, capthick=1, label="40 grams")
    ax[1].errorbar(t, m_w3_g20_disp_avg, yerr=m_w3_g20_disp_stdv, label="20 grams")
    ax[1].errorbar(t, m_w3_g0_disp_avg, yerr=m_w3_g0_disp_stdv, label="0 grams")
    ax[1].set_title("Mandrel Coiled TCA Position Response to 3W, 0.05Hz Square Wave")
    ax[1].set_xlabel("Time (sec)")
    ax[1].set_ylabel("Position (cm)")

    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("3W_varying_load")
    plt.show()

do_plot_2()



