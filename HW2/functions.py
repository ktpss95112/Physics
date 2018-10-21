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

    fig, ax = plt.subplots()
    ax.set_title("F(x)")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("F (Nt)")
    ax.axhline(y=0, color='k', linewidth=0.5)

    list_x = [x for x in np.arange(x_left_bound, x_right_bound, dx)]
    list_F = [F(x) for x in list_x]
    list_U = [U(x) for x in list_x]

    ax.plot(list_x, list_F, label='F(x)')
    ax.plot(list_x, list_U, label='U(x)')
    ax.text(x1-1.3, Um+0.04, 'x1=%.2f'%(x1))
    #ax.plot(x1, Um, color='k')
    ax.text(x2-0.7, Um+0.04, 'x2=%.2f'%(x2))
    #ax.plot(x2, Um, color='k')
    ax.legend(loc='best')

# phase-space trajectory
def plot_pst(x0, direction):
    global x_left_bound, x_right_bound, dx
    list_x = []
    list_v = []

    fig, ax = plt.subplots()
    ax.set_title("Phase-space Trajectory (x0=%.2f , v0=%.2f)"%(x0, V(x0, Um)*direction))
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
    #print('%.2f %.2f'%(v, F(x)))

    while U(x) < E:
        dx, dv = v*dt, F(x)/mass*dt
        x += dx
        v += dv
        t += dt
        #print('%.2f %.2f'%(x, v))

    print('period: %.2f sec'%(4*t))
    print('amplitude: %.2f m'%(x))
