import numpy as np
import control

## -------------------- First Order Modeling -------------------- ##
def find_ss(data, tol, bias):

    data = bias - data
    peak = max(data)

    ss_list = []
    for val in data:
        if np.isclose(val, peak, atol=tol):
            ss_list.append(val)

    ss_val = np.mean(ss_list)

    return ss_val

def find_k(data, start, stop, ss_tolerance, bias):
    data = data[start:stop]
    k = find_ss(data, ss_tolerance, bias)
    return k

def growth_to_decay(growth_data, ss_val):
    decay = ss_val - growth_data
    return decay

def find_index_at_t63(data, val_at_t63):
    index_at_t63 = None
    tol = 0.2
    while index_at_t63 is None:
        try:
            tol = tol + 0.1
            index_at_t63 = np.where(np.isclose(data, val_at_t63, atol=tol))[0][0]
        except IndexError:
            pass

    return index_at_t63

def find_tau(data, time, start, stop, ss_tolerance, bias, ss_val=None, type='growth'):
    """Returns - time constant, 
                steady state value"""
    
    # slice arrays to area of interest
    data = data[start:stop]
    time = time[start:stop]

    if ss_val == None:
        ss_val = find_ss(data, ss_tolerance, bias)
    
    val_at_t63 = ss_val*0.63

    if type == 'growth':
        index_at_t63 = find_index_at_t63(data, val_at_t63)
    
    if type == 'decay':
        data = growth_to_decay(data, ss_val)
        index_at_t63 = find_index_at_t63(data, val_at_t63)
    
    tau = time[index_at_t63] - time[0]

    return tau

def normalize(data):
    bias_term = data[0]
    data = bias_term - np.array(data)
    return data, bias_term

def find_first_order_sys(data, t, start, stop, type, ss_tolerance, ss_val=None):
    bias = data[0]

    k = ss_val
    if ss_val is None:
        k = find_k(data, start, stop, ss_tolerance, bias)
    tau = find_tau(data, t, start, stop, ss_tolerance, type=type, ss_val=ss_val, bias=bias)
    num = [k]
    den = [tau, 1]
    sys = control.TransferFunction(num, den)
    t_sim = np.linspace(t[start], t[stop], 1000)
    t_out, y_out = control.step_response(sys, t_sim)

    if type == "decay":
        y_out = -y_out + bias

    elif type == "growth":
        y_out = y_out + bias

    # print(bias)
    # y_out = y_out + bias

    return k, tau, t_out, y_out

def first_order_model(data, t, ss_tolerance=40, trim_index=55, recording_frequency=0.2, pulse_length=30):
    pulse_start_index = trim_index
    pulse_length_index = int(pulse_length / recording_frequency)
    pulse_stop_index = pulse_start_index+pulse_length_index

    # normalize
    data, bias_term = normalize(data)

    # heating
    k_h, tau_h, t_out_h, y_out_h = find_first_order_sys(data=data, 
                                                        t=t, 
                                                        start=pulse_start_index, 
                                                        stop=pulse_stop_index, 
                                                        type="growth", 
                                                        ss_tolerance=ss_tolerance)
    # cooling
    k_c, tau_c, t_out_c, y_out_c = find_first_order_sys(data=data, 
                                                        t=t, 
                                                        start=pulse_stop_index, 
                                                        stop=-1, 
                                                        type="decay",
                                                        ss_tolerance=ss_tolerance,
                                                        ss_val=k_h)

    # un-normalize
    # y_out_h = bias_term + y_out_h
    # y_out_c = bias_term + y_out_c
    
    y_out_c = growth_to_decay(y_out_c, k_c)

    return [k_h, tau_h, t_out_h, y_out_h], [k_c, tau_c, t_out_c, y_out_c]