import numpy as np
import matplotlib.pyplot as plt
from math import exp, sqrt

# parameters
mass = 1
x_left_bound = -5
x_right_bound = 5
dx = 0.01
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

        # case 0: bounded motion
        if x1 < x < x2:
            for cnt in range(2*int((x2-x1)/dx)):
                list_x.append(x)
                list_v.append(V(x, E)*direction)
                x += dx*direction

                # update direction

        # case 1: right side
        elif x > x2:


        # case 2: left side
        else:


        ax.plot(list_x, list_v, label='E=%.1fUm'%(E_cf[i]))
        list_x = []
        list_v = []
        print('%d printed'%(i))

    for i in [4]:
        E = E_cf[i]*Um
        x = x0

        # if !(x==x1 || x==x2)
        while not(abs(x-x1)<dx or abs(x-x2)<dx):
            list_x.append(x)
            list_v.append(V(x, E)*direction)
            x += dx*direction

        ax.plot(list_x, list_v, label='E=%.1fUm'%(E_cf[i]))
        list_x = []
        list_v = []
        print('%d printed'%(i))

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
        print('%d printed'%(i))


    ax.legend(loc='best')

