import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import control

### ------ Data Parsing ------ ###

mandrel_data = pd.read_csv("data-collection_mandrel-coiled.csv")
nucleated_data = pd.read_csv("data-collection_self-coiled.csv")
step_data = pd.read_csv("data-collection_mandrel-step-response.csv")

t = np.array(mandrel_data["t"])
t_step = np.array(step_data["t"])

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
# 40g, mandrel-coiled, 3 watts, forced convection
m_w3_g40_fcd_1 = np.array(mandrel_data["40g_3w_forced"])
m_w3_g40_fcd_2 = np.array(mandrel_data["40g_3w_forced.1"])
# 20g, mandrel-coiled, 3 watts, free convection
m_w3_g20 = np.array(mandrel_data["20g_3w_free"])
# 0g, mandrel-coiled, 3 watts, free convection
m_w3_g0 = np.array(mandrel_data["0g_3w_free"])

w3_step_response = np.array(step_data["40g_3W_free_step"])

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
m_w3_g40_fcd_1 = adjust_start_pos(m_w3_g40_fcd_1)
m_w3_g40_fcd_2 = adjust_start_pos(m_w3_g40_fcd_2)
m_w3_g20 = adjust_start_pos(m_w3_g20)
m_w3_g0 = adjust_start_pos(m_w3_g0)

w3_step_response = adjust_start_pos(w3_step_response)

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
m_w3_g40_fcd_disp_avg, m_w3_g40_fcd_disp_stdv, m_w3_g40_fcd_strain_avg, m_w3_g40_fcd_strain_stdv = get_data_to_plot([m_w3_g40_fcd_1, m_w3_g40_fcd_2])

m_w3_g20_disp_avg, m_w3_g20_disp_stdv, m_w3_g20_strain_avg, m_w3_g20_strain_stdv = get_data_to_plot([m_w3_g20])
m_w3_g0_disp_avg, m_w3_g0_disp_stdv, m_w3_g0_strain_avg, m_w3_g0_strain_stdv = get_data_to_plot([m_w3_g0])

w3_step_disp_avg, w3_step_disp_stdv, w3_step_strain_avg, w3_step_strain_stdv = get_data_to_plot([w3_step_response])

plt.style.use("seaborn")

# plot 1: Mandrel coiled: 3W free, 1W free, 3W forced
def plot_varying_power():
    fig, ax = plt.subplots(2,1)
    # strain
    ax[0].errorbar(t, m_w3_g40_strain_avg, yerr=m_w3_g40_strain_stdv, capsize=3, capthick=1, label="3W, free")
    ax[0].errorbar(t, m_w3_g40_fcd_strain_avg, yerr=m_w3_g40_fcd_strain_stdv, capsize=3, capthick=1, label="3W, forced")
    ax[0].errorbar(t, m_w1_g40_strain_avg, yerr=m_w1_g40_strain_stdv, capsize=3, capthick=1, label="1W, free")
    ax[0].set_title("Strain vs Time")
    ax[0].set_xlabel("Time (sec)")
    ax[0].set_ylabel("Strain")
    ax[0].set_title("Mandrel Coiled TCA Strain Response to a 0.05Hz Square Wave with 40g load")
    ax[0].legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
    # displacement
    ax[1].errorbar(t, m_w3_g40_disp_avg, yerr=m_w3_g40_disp_stdv, capsize=3, capthick=1, label="3W, free")
    ax[1].errorbar(t, m_w3_g40_fcd_disp_avg, yerr=m_w3_g40_fcd_disp_stdv, capsize=3, capthick=1, label="3W, forced")
    ax[1].errorbar(t, m_w1_g40_disp_avg, yerr=m_w1_g40_disp_stdv, capsize=3, capthick=1, label="1W, free")
    ax[1].set_title("Mandrel Coiled TCA Position Response to a 0.05Hz Square Wave with 40g load")
    ax[1].set_xlabel("Time (sec)")
    ax[1].set_ylabel("Position (cm)")

    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("40g_varying_amp")
    plt.show()


# plot 2: Mandrel coiled: 40g, 20g, 0g
def plot_varying_load():
    fig, ax = plt.subplots(2,1)
    # strain
    ax[0].errorbar(t, m_w3_g40_strain_avg, yerr=m_w3_g40_strain_stdv, capsize=3, capthick=1, label="40 grams")
    ax[0].errorbar(t, m_w3_g20_strain_avg, yerr=m_w3_g20_strain_stdv, label="20 grams")
    ax[0].errorbar(t, m_w3_g0_strain_avg, yerr=m_w3_g0_strain_stdv, label="0 grams")
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
    # plt.savefig("3W_varying_load")
    plt.show()

def plot_step_reponse():
    fig, ax = plt.subplots(2,1)
    # strain
    ax[0].errorbar(t_step, w3_step_strain_avg, yerr=w3_step_strain_stdv, capsize=3, capthick=1)
    ax[0].set_xlabel("Time (sec)")
    ax[0].set_ylabel("Strain")
    ax[0].set_title("Mandrel Coiled TCA Strain Response to 3W Step Input")
    # displacement
    ax[1].errorbar(t_step, w3_step_disp_avg, yerr=w3_step_disp_stdv, capsize=3, capthick=1)
    ax[1].set_title("Mandrel Coiled TCA Position Response to 3W Step Input")
    ax[1].set_xlabel("Time (sec)")
    ax[1].set_ylabel("Position (cm)")

    k = 3
    tau = 5

    num = [k]
    den = [tau, 1]
    sys = control.TransferFunction(num, den)
    t_sim = np.linspace(0, 30, 1000)
    t_out, y_out = control.step_response(sys, t_sim)

    ax[1].plot(t_out, 24.9-y_out)

    num2 = [-k]
    sys = control.TransferFunction(num2, den)
    t_sim2 = np.linspace(30, 60, 1000)
    t_out2, y_out2 = control.step_response(sys, t_sim2)

    ax[1].plot(t_out2, 21.9-y_out2)
    
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("3W_step")
    plt.show()

plot_step_reponse()



