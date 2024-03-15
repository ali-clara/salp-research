import numpy as np
import control
import matplotlib.pyplot as plt
# plt.style.use('seaborn-deep')

def normalize_and_trim(data, t, start, stop):
    data = data[start:stop]
    bias = data[0]
    data = data - bias
    t = t[start:stop]

    return data, bias, t

def find_ss(data, growth, ss_tol):
    if growth == False:
        peak = min(data)
    elif growth == True:
        peak = max(data)
    ss_list = []
    for val in data:
        if np.isclose(val, peak, atol=ss_tol):
            ss_list.append(val)

    ss_val = np.mean(ss_list)

    return ss_val

def find_index_at_t63(data, ss_val, tau_tol):
    val_at_t63 = ss_val*0.63
    # print(f"steady state value: {ss_val}. Value at 1 tau: {val_at_t63}")

    index_at_t63 = None
    tol = tau_tol
    step_size = tol / 2
    while index_at_t63 is None:
        try:
            tol = tol + step_size
            index_at_t63 = np.where(np.isclose(data, val_at_t63, atol=tol))[0][0]
        except IndexError:
            pass

    return index_at_t63

def find_tau(t, t63_index):
    tau_offset = t[t63_index]
    tau = tau_offset - t[0]
    return tau

def find_model(k, tau, t):
    num = [k]
    den = [tau, 1]
    sys = control.TransferFunction(num, den)
    t_sim = np.linspace(t[0], t[-1], 1000)
    t_out, y_out = control.step_response(sys, t_sim)

    return t_out, y_out

def fix_offset(list_to_offset, bias):
    offset_list = []
    for val in list_to_offset:
        val = val + bias
        offset_list.append(val)

    return offset_list

def find_first_order_fit(data, t, start, stop, growth=True, ss_tol=0.01, tau_tol=0.001):
    
    data, bias, t = normalize_and_trim(data, t, start, stop)
    ss_val = find_ss(data, growth, ss_tol)
    t63_index = find_index_at_t63(data, ss_val, tau_tol)
    tau = find_tau(t, t63_index)
    t_out, y_out = find_model(ss_val, tau, t)

    y_out, data = fix_offset([y_out, data], bias)

    # print(f"time constant: {tau}, k: {ss_val}")

    return t_out, y_out, ss_val, tau

if __name__ == "__main__":
    data = np.load("soft-bodies/origami/data/spring2/6W/average.npy")
    t = np.load("soft-bodies/origami/data/spring2/6W/t.npy")

    recording_frequency= 1 / 30
    pulse_start_index = int(14.25 / recording_frequency)
    # pulse_start_index = int(13.75 / recording_frequency)
    pulse_stop_index = int(20 / recording_frequency)

    t_contract, y_contract, ss_val_contract, tau_contract = find_first_order_fit(data, t, 0, pulse_start_index, growth=True)
    t_relax, y_relax, ss_val_relax, tau_relax = find_first_order_fit(data, t, pulse_start_index, pulse_stop_index, growth=False)
    
    print(f"Tau contraction: {np.round(tau_contract,3)}, steady state value: {np.round(ss_val_contract,3)}")
    print(f"Tau relaxation: {np.round(tau_relax,3)}, steady state value: {np.round(ss_val_relax,3)}")

    fig, ax = plt.subplots(2,1)
    fig.tight_layout(pad=2)
    
    ax[0].plot(t, data)
    ax[1].plot(t, data)
    ax[1].plot(t_relax, y_relax)
    ax[1].plot(t_contract, y_contract)
    # ax[1].hlines(ss_val + 1, 42, 52, color='red')
    # ax[1].vlines(t_data[t63_index], 0, 300, color='yellow')
    ax[0].set_title("6W first order fit")
    ax[1].set_xlabel("Time (sec)")
    ax[0].set_xlim([-1, 22])
    ax[1].set_xlim([-1, 22])
    plt.show()

