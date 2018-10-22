import numpy as np
import matplotlib.pyplot as plt
from math import exp, sqrt

# parameters
mass = 1
x_left_bound = -5
x_right_bound = 5
dx = 0.01
dt = 0.001
Um = 0
x1 = None
x2 = None
E_cf = np.arange(0.2, 1.6, 0.2)

# functions
def U(x):
    return x*x*exp(-x*x/2)

def F(x):
    return -(2*x*exp(-x*x/2) - x*x*x*exp(-x*x/2))

def V(x, E):
    global mass
    return sqrt(2*(E-U(x))/mass)

def init():
    global Um, x1, x2, x_left_bound, x_right_bound, dx
    for x in np.arange(0, x_right_bound, dx):
        if Um < U(x):
            x1, x2 = -x, x
            Um = U(x)

'''
Below are the functions of the subtasks of this homework.

'''
def plot_F():
    global x_left_bound, x_right_bound, dx

    fig, axF = plt.subplots()
    axU = axF.twinx()
    axF.get_shared_y_axes().join(axF, axU)
    axF.set_title("F(x)")
    axF.set_xlabel("x (m)")
    axF.set_ylabel("F (Nt)", color='tab:blue')
    axF.tick_params(axis='y', labelcolor='tab:blue')
    axU.set_ylabel("U (J)", color='tab:orange')
    axU.tick_params(axis='y', labelcolor='tab:orange')
    axF.axhline(y=0, color='k', linewidth=0.5)

    list_x = [x for x in np.arange(x_left_bound, x_right_bound, dx)]
    list_F = [F(x) for x in list_x]
    list_U = [U(x) for x in list_x]

    axF.plot(list_x, list_F, label='F(x)', color='tab:blue')
    axF.plot(list_x, list_U, label='U(x)', color='tab:orange')
    axF.text(x1-1.4, Um+0.04, 'x1=%.2f(m)'%(x1))
    axF.text(x2-0.7, Um+0.04, 'x2=%.2f(m)'%(x2))
    axU.axhline(y=Um, color='k', linewidth=0.5, linestyle='--')
    axU.text(-4.5, Um-0.07, 'Um=%.2f(J)'%(Um))

    axF.legend(loc='lower right')
    plt.subplots_adjust(top=0.88, bottom=0.11, left=0.12, right=0.885, hspace=0.2, wspace=0.2)



# phase-space trajectory
def plot_pst(x0, direction):
    global x_left_bound, x_right_bound, dx
    list_x = []
    list_v = []

    fig, ax = plt.subplots()
    ax.set_title("Phase-space Trajectory (x0=%.2fm)"%(x0))
    ax.set_xlabel("x (m)")
    ax.set_ylabel("v (m/s)")

    for i in [0, 1, 2, 3]:
        E = E_cf[i]*Um
        x = x0
        tmp_dir = direction

        # case 0: bounded motion
        if x1 < x < x2:
            for cnt in range(2*int((x2-x1)/dx)):
                if U(x) > E:
                    tmp_dir = -tmp_dir
                    x += dx*tmp_dir
                    continue

                list_x.append(x)
                list_v.append(V(x, E)*tmp_dir)
                x += dx*tmp_dir

        # case 1: else
        else:
            while x_left_bound < x < x_right_bound:
                if U(x) > E:
                    tmp_dir = -tmp_dir
                    x += dx*tmp_dir
                    continue

                list_x.append(x)
                list_v.append(V(x, E)*tmp_dir)
                x += dx*tmp_dir


        ax.plot(list_x, list_v, label='E=%.1fUm'%(E_cf[i]))
        list_x = []
        list_v = []

    for i in [4]:
        E = E_cf[i]*Um
        x = x0

        # if !(x==x1 || x==x2) && (xl<x<xr)
        while not(abs(x-x1)<dx or abs(x-x2)<dx) and (x_left_bound<x<x_right_bound):
            list_x.append(x)
            list_v.append(V(x, E)*direction)
            x += dx*direction

        ax.plot(list_x, list_v, label='E=%.1fUm'%(E_cf[i]))
        list_x = []
        list_v = []

    for i in [5, 6]:
        E = E_cf[i]*Um
        x = x0

        while x_left_bound <= x <= x_right_bound:
            list_x.append(x)
            list_v.append(V(x, E)*direction)
            x += dx*direction

        ax.plot(list_x, list_v, label='E=%.1fUm'%(E_cf[i]))
        list_x = []
        list_v = []


    ax.legend(loc='best')
    ax.axhline(y=0, color='k', linewidth=0.5)

def print_amplitude_and_period():
    global dt, x1, x2, mass

    E = 0.4*Um
    t = 0
    x = 0
    v = V(x, E)

    while v >= 0:
        dx, dv = v*dt, F(x)/mass*dt
        x += dx
        v += dv
        t += dt

    print('period: %.3f sec'%(4*t))
    print('amplitude: %.3f m'%(x))
