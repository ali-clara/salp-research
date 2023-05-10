import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import control
plt.style.use('seaborn')

## -------------------- Preprocessing -------------------- ##
# grab data from csv
# data = pd.read_csv("force_data/load-cell-data_1683653160.csv") # 0.5 sec
# data = pd.read_csv("force_data/load-cell-data_1683654314.csv") # 0.5 sec
# data = pd.read_csv("force_data/load-cell-data_1683666918.csv") # 0.2 sec
# data = pd.read_csv("force_data/load-cell-data_1683672261.csv") # 0.2 sec
data = pd.read_csv("force_data/load-cell-data_1683672491.csv") # 0.2 sec, pulse length 30, approx 3W (actually measured not nominal)
recording_frequency = 0.2
pulse_length_sec = 30
pulse_length_index = int(pulse_length_sec / recording_frequency)

force_data_kgs = data["Force (kgs)"]
signal_data = data["Input Signal"]

# create time array 
t_len = len(signal_data)
t = np.arange(0, t_len*recording_frequency, recording_frequency)


# convert to milinewtons
def kgs_to_mn(data):
    mn = np.array(data) * 9.81 * 1000
    return mn

# adjust bias
def adjust_bias(data):
    abs_bias_term = 2
    for i, val in enumerate(data):
        if abs(val) <= abs_bias_term:
            data[i] = 0

    return data

force_data = kgs_to_mn(force_data_kgs)
# force_data = adjust_bias(force_data)
# print(force_data)

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
        index_at_t63 = np.where(np.isclose(data, val_at_t63, atol=0.3))[0][0]
    
    if type == 'decay':
        data = ss_val - data
        index_at_t63 = np.where(np.isclose(data, val_at_t63, atol=3))[0][0]
    
    tau = time[index_at_t63] - time[0]

    return tau

# first order model
pulse_start_index = np.where(signal_data==1)[0][0]
pulse_stop_index = np.where(signal_data==1)[0][-1]

# heating
k_h = find_k(force_data, pulse_start_index, pulse_stop_index)
tau_h = find_tau(force_data, t, pulse_start_index, pulse_stop_index, type='growth')
num_h = [k_h]
den_h = [tau_h, 1]
sys_h = control.TransferFunction(num_h, den_h)
t_sim_h = np.linspace(t[pulse_start_index], t[pulse_stop_index], 1000)
t_out_h, y_out_h = control.step_response(sys_h, t_sim_h)
# cooling
# k_c = find_k(force_data, pulse_stop_index, len(t))
tau_c = find_tau(force_data, t, pulse_stop_index, len(t), ss_val=k_h, type='decay')
k_c = -k_h
num2 = [k_c]
den2 = [tau_c, 1]
t_sim_c = np.linspace(t[pulse_stop_index], t[-1], 1000)
sys_c = control.TransferFunction(num2, den2)
t_out_c, y_out_c = control.step_response(sys_c, t_sim_c)

print(f"Heating: tau = {tau_h}, k = {k_h}")
print(f"Cooling: tau = {round(tau_c,4)}, k = {k_c}")

# plot
fig, ax = plt.subplots(1,1, figsize=(9,5))
ax.plot(t, force_data, label="Force response")
ax.plot(t_out_h, y_out_h, label=f"Heating: tau = {tau_h}, k = {k_h}")
ax.plot(t_out_c, -k_c+y_out_c, label=f"Cooling: tau = {round(tau_c,4)}, k = {k_c}")

ax2 = ax.twinx()
ax2.plot(t, 3*signal_data, 'k--', label="Input signal", alpha=0.4)

ax.set_xlabel("Time (sec)")
ax.set_ylabel("Force (mN)")
ax2.set_ylabel("Input signal (Watts)")
ax.set_title("Force response to step in power")

lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc=0)

plt.tight_layout()
# plt.savefig("force_data/figs/force-power-step.png")
plt.show()