import numpy as np
import matplotlib.pyplot as plt
plt.style.use("seaborn")
from scipy import ndimage
import scipy.optimize
from sympy import Symbol
import sympy

fs = 60.0   # sample frequency Hz
circumference = np.load("data/filtered-circumference_8-11-23.npy")   # mm
area = np.load("data/filtered-area-data_8-11-23.npy") # mm^

area = area[20:]
first = area[0]
for i in range(300):
    area = np.insert(area, 0, first)

t = np.arange(0, 1/fs*len(area), 1/fs) # sec

def radius_from_circumference(circumference):
    return circumference / (2*np.pi)

def trim(data, t_start, t_stop):
    return data[t_start*int(fs):t_stop*int(fs)]

def mm_to_m(data):
    return data / 1000

def mm2_to_m2(data):
    return data / 1e6

def mm3_to_ml(data):
    return data / 1000

def finite_difference(f, x):
    # normalization
    dx = x[1] - x[0] # use np.diff(x) if x is not uniform
    # first derivatives
    df = np.diff(f) / dx
    last = df[-1]
    df = np.append(df, last)
    return df

def model_f(x,a,b):
    return a*np.exp(b*x) 

def do_curve_fit(x, y, p0=[14.5, -0.1]):
    p_opt, p_cov = scipy.optimize.curve_fit(model_f, x, y, p0)
    a_opt, b_opt = p_opt
    print(f"Optimal fit: y = {a_opt}*e^({b_opt}*t)")

    y_model = model_f(x, a_opt, b_opt)

    return a_opt, b_opt, y_model

def find_symbolic_f(a, b):
    x = Symbol('x')
    f_sym = a*sympy.E**(b*x)
    print(f_sym)
    f = sympy.lambdify(x, f_sym)

    return f_sym, f

def find_symbolic_fdot(f_sym):
    x = Symbol('x')
    f_dot_sym = sympy.diff(f_sym, x)
    print(f_dot_sym)
    f_dot = sympy.lambdify(x, f_dot_sym)

    return f_dot_sym, f_dot

def find_volume_flux(r, r_dot):
    h = 0.01 # 1 cm
    v_dot = np.pi*h*2*r*r_dot
    return v_dot


# circumference = trim(circumference, 0, 25) # mm
# t = trim(t, 0, 25)
# r = radius_from_circumference(circumference)   # mm
# r = mm_to_m(r) # m
# r_dot = finite_difference(r, t)

# v_dot = find_volume_flux(r, -r_dot)
# v_dot = mm3_to_ml(v_dot)

a_dot = finite_difference(area, t) # mm^2/s
v_from_a = mm3_to_ml(a_dot*0.01)

fig, ax = plt.subplots(2,1)
ax[0].plot(t, area, label="filtered area, mm^2")
ax[0].legend(loc=0)
ax[0].set_ylabel("Area (mm^s)")

ax[1].plot(t, a_dot, label="Finite difference, mm^2/s")
ax[1].legend(loc=0)
ax[1].set_ylabel("dA/dt (mm^2/s)")

# ax[2].plot(t, v_from_a, label="v dot, ml/s")
# ax[2].legend(loc=0)

plt.tight_layout()
plt.show()




"""
a, b, y = do_curve_fit(t, radius)

r_sym, r_func = find_symbolic_f(a, b)
r_dot_sym, r_dot_func = find_symbolic_fdot(r_sym)

r = r_func(t)
r_dot = r_dot_func(t)

v_dot = find_volume_flux(r, -r_dot)

fig, ax = plt.subplots(2,1)
ax[0].scatter(t, radius, label='Measured data')
ax[0].plot(t, y, color='tab:red', label="Exponential fit")
ax[0].set_ylabel("radius (m)")
ax[0].set_xlabel("time (s)")
ax[0].legend(loc=0)
ax[1].plot(t, v_dot, color='tab:pink')
ax[1].set_xlabel("time (s)")
ax[1].set_ylabel("change in volume (m^3/s)")
plt.tight_layout()

model_t = np.linspace(0, 200, 750)
model_r = model_f(model_t, a, b)

r = r_func(model_t)
r_dot = r_dot_func(model_t)

v_dot = find_volume_flux(r, -r_dot)

fig, ax = plt.subplots(3,1)
ax[0].plot(model_t, r, color='tab:red', label="Radius fit")
ax[0].set_ylabel("radius (m)")

ax[1].plot(model_t, -r_dot, color='tab:orange', label="Change in radius")
ax[1].set_ylabel("change in radius (m/s)")

ax[2].plot(model_t, v_dot, color='tab:pink')
ax[2].set_ylabel("change in volume (m^3/s)")

plt.tight_layout()
plt.show()

# fig, ax = plt.subplots(1,1)
# ax.plot(t, circumference)
# plt.show()

# plt.scatter(t, v_dot)
# plt.show()
"""