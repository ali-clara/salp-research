import numpy as np
import control

## -------------------- First Order Modeling -------------------- ##
def find_ss(data, tol, offset=None):
    if offset is not None:
        data = offset - data

    peak = max(data)

    ss_list = []
    for val in data:
        if np.isclose(val, peak, atol=tol):
            ss_list.append(val)

    ss_val = np.mean(ss_list)

    return ss_val

def find_k(data, start, stop, ss_tolerance, offset):
    data = data[start:stop]
    k = find_ss(data, ss_tolerance, offset)
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

def find_tau(data, time, start, stop, ss_tolerance, ss_val=None, type='growth'):
    """Returns - time constant, 
                steady state value"""
    
    # slice arrays to area of interest
    data = data[start:stop]
    time = time[start:stop]

    if ss_val == None:
        ss_val = find_ss(data, ss_tolerance)
    
    val_at_t63 = ss_val*0.63

    if type == 'growth':
        index_at_t63 = find_index_at_t63(data, val_at_t63)
    
    if type == 'decay':
        data = growth_to_decay(data, ss_val)
        index_at_t63 = find_index_at_t63(data, val_at_t63)
    
    tau = time[index_at_t63] - time[0]

    return tau

def find_first_order_sys(data, t, start, stop, type, ss_tolerance, offset, ss_val=None):
    k = ss_val
    if ss_val is None:
        k = find_k(data, start, stop, ss_tolerance, offset)
    tau = find_tau(data, t, start, stop, ss_tolerance, type=type, ss_val=ss_val)
    num = [k]
    den = [tau, 1]
    sys = control.TransferFunction(num, den)
    t_sim = np.linspace(t[start], t[stop], 1000)
    t_out, y_out = control.step_response(sys, t_sim)

    return k, tau, t_out, y_out

def first_order_model(force_data, t, ss_tolerance=40, trim_index=55, recording_frequency=0.2, pulse_length=30, offset=None):
    pulse_start_index = trim_index
    pulse_length_index = int(pulse_length / recording_frequency)
    pulse_stop_index = pulse_start_index+pulse_length_index

    # heating
    k_h, tau_h, t_out_h, y_out_h = find_first_order_sys(data=force_data, 
                                                        t=t, 
                                                        start=pulse_start_index, 
                                                        stop=pulse_stop_index, 
                                                        type="growth", 
                                                        ss_tolerance=ss_tolerance,
                                                        offset=offset)
    # cooling
    k_c, tau_c, t_out_c, y_out_c = find_first_order_sys(data=force_data, 
                                                        t=t, 
                                                        start=pulse_stop_index, 
                                                        stop=-1, 
                                                        type="decay",
                                                        ss_tolerance=ss_tolerance,
                                                        ss_val=k_h,
                                                        offset=offset)

    y_out_c = growth_to_decay(y_out_c, k_c)

    return [k_h, tau_h, t_out_h, y_out_h], [k_c, tau_c, t_out_c, y_out_c]