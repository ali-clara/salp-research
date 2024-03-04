from scipy.interpolate import splrep, splev
import numpy as np
import matplotlib.pyplot as plt
import copy
import sys
sys.path.append("C:\\Users\\alicl\\Documents\\GitHub\\salp-research")
from create_paper_figure import MakePlot

def mm2_to_m2(mm2):
    return mm2 / 1e6

def m2_to_mm2(m2):
    return m2 * 1e6

def mm3_to_m3(mm3):
    return mm3 / 1e9

def m3_to_mm3(m3):
    return m3 * 1e9

def n_to_mn(n):
    return n * 1e3

def level_start(y, cutoff):
    avg = np.mean(y[0:cutoff*fps])
    y[0:cutoff*fps] = avg
    return y

def level_end(y, cutoff):
    y[cutoff*fps:-1] = y[cutoff*fps]
    y[-1] = y[cutoff*fps]
    return y

def zero_start(y):
    above_zero = np.where(y[0:15*fps] > 0)[0]
    y[above_zero] = 0

def zero_end(y):
    last_zero = np.where(y>0)[0][0]
    y[last_zero:-1] = 0
    y[-1] = 0

def make_spline(x, y, scale_factor):
    spline = splrep(x, y, s=len(x)*scale_factor)
    # correction factor to level out the first few points of the spline 
        # (otherwise edge conditions are weird)
    spline[1][0:2] = y[0]
    spline_fit = splev(x, spline)
    spline_deriv = splev(x, spline, der=1)
    return spline_fit, spline_deriv

def calc_thrust(vol_dot, a0, rho=1000, c0=0.6):
    thrust = rho*vol_dot**2 / (c0 * a0)
    return thrust

def plot_volume_fit(volume, volume_fit, vol_dot, t, title):
    fig, ax = plt.subplots(2,1)
    ax[0].plot(t, volume)
    ax[0].plot(t, volume_fit)
    ax[0].set_xlabel("Time (sec)")
    ax[0].set_ylabel("Volume (mm3)")
    ax[0].set_title(title)

    ax[1].plot(t, vol_dot)
    ax[1].set_xlabel("Time (sec)")
    ax[1].set_ylabel("Volumetric Flow (mm3/s)")

    plt.tight_layout()
    plt.show()

def percent_decrease(val1, val2):
    delta = val1-val2
    return 100*delta / val1

l = 34.3 # mm
fps = 30

## tube
def tube_volume(front_area, t, pulse_type, plot=True):
    # front_area = np.load() # mm2
    # t = np.load()
    # std = np.load()
    # front_area = level_start(front_area, cutoff=8)
    r = front_area / (2*l)  # mm
    a0 = np.pi*r**2 # mm2
    volume_tube = np.pi*r**2*l # mm3

    volume_contraction = copy.copy(volume_tube)
    min_index = np.where(volume_contraction == min(volume_contraction))[0]
    volume_contraction = level_end(volume_contraction, cutoff=int(np.round(min_index/30)))

    print(f"{pulse_type} volume change: {volume_tube[0]} to {min(volume_tube)}, {percent_decrease(volume_tube[0], min(volume_tube))}%")

    vol_fit, vol_dot = make_spline(t, volume_contraction, scale_factor=600)
    zero_start(vol_dot)
    zero_end(vol_dot)

    if plot:
        plot_volume_fit(volume_tube, vol_fit, vol_dot, t, title=pulse_type)

    return vol_dot, a0

## shell
def shell_volume(front_area, t, dia_interp_list, t_interp_list, pulse_type, plot=True):
    
    # front_area = np.load() # mm2
    # t = np.load()
    # std = np.load()

    maj_diameter = front_area / l # mm
    print(f"major diameter {maj_diameter}")
    min_index = t_interp_list[-1]

    # interpolate to find the minor diameter across the contraction phase
    min_diameter = np.interp(t[0:min_index*fps], t_interp_list, dia_interp_list)
    # add dummy values to the end for plotting purposes
    min_diameter = np.append(min_diameter, [dia_interp_list[-1]]*(len(t[min_index*fps:-1])+1))
    
    a0 = np.pi*maj_diameter/2*min_diameter/2
    # volume_shell = np.pi * front_area * min_diameter / 4 # same as pi*maj/2*min/2*l
    volume_shell = a0*l

    print(f"{pulse_type} volume change: {volume_shell[0]} to {min(volume_shell)}, {percent_decrease(volume_shell[0], min(volume_shell))}%")

    volume_contraction = level_end(volume_shell, cutoff=min_index)

    vol_fit, vol_dot = make_spline(t, volume_contraction, scale_factor=500)
    zero_start(vol_dot)
    zero_end(vol_dot)

    if plot:
        plot_volume_fit(volume_shell, vol_fit, vol_dot, t, title=pulse_type)

    return vol_dot, a0

my_plot = MakePlot()
path_names = ["all-on", "pulse-hold", "pulse-release"]
body_type = "shell"

legend_names = ["Activated simultaneously", "Activated in sequence", "Activated and released"]

dia_interp_list = [[15.06, 15.06, 13.4, 12.6], [15.06, 15.06, 13.4, 12.6], [15.06, 15.06, 13.4]]
t_interp_list = [[0, 10, 20, 30], [0, 10, 40, 60], [0, 10, 35]]    # all-on, pulse-release, pulse-hold

for i, name in enumerate(path_names):
    front_area = np.load("data/averages/"+body_type+"_"+name+"_avg.npy") #mm2
    t = np.load("data/averages/"+body_type+"_"+name+"_t.npy")
    
    vol_dot, a0 = shell_volume(front_area, t, dia_interp_list[i], t_interp_list[i], pulse_type=body_type+"_"+name, plot=False) #mm3/s, mm2
    # vol_dot, a0 = tube_volume(front_area, t, pulse_type=body_type+"_"+name, plot=False) #mm3/s, mm2
     
    vol_dot_m3 = mm3_to_m3(vol_dot)
    a0_m2 = mm2_to_m2(a0)
    thrust = calc_thrust(vol_dot_m3, a0_m2) # N
    thrust_mn = n_to_mn(thrust)
    print(max(thrust_mn))

    my_plot.set_xy(t, thrust_mn*1e3)
    my_plot.set_data_labels(legend_names[i])
   
    my_plot.set_axis_labels(xlabel="Time (sec)", ylabel="Thrust (mN x 1e-3)")
    my_plot.plot_xy()

my_plot.set_savefig(body_type+"-thrust-plot.png")
my_plot.label_and_save()