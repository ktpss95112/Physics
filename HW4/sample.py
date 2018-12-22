from vpython import *
from random import random
import numpy as np

# physical parameter initialization
r = 0.05
L = 1.
N = 50
mHe = 4.E-3/6.02E23
kB = 1.38E-23
atoms = []
v_initial = 1.

# animation scene initialization
winsize = 500
scene = canvas(width = winsize, height = winsize)
scene.range = L
d = L/2 + r
borders_bot = curve(pos = [(d, -d, d), (-d, -d, d), (-d, -d, -d), (d, -d, -d), (d, -d, d)], radius = 0.005, color = color.white)
borders_top = curve(pos = [(d, d, d), (-d, d, d), (-d, d, -d), (d, d, -d), (d, d, d)], radius = 0.005, color = color.white)
borders_1 = curve(pos = [(d, -d, d), (d, d, d)], radius = 0.005, color = color.white)
borders_2 = curve(pos = [(d, -d, -d), (d, d, -d)], radius = 0.005, color = color.white)
borders_3 = curve(pos = [(-d, -d, d), (-d, d, d)], radius = 0.005, color = color.white)
borders_4 = curve(pos = [(-d, -d, -d), (-d, d, -d)], radius = 0.005, color = color.white)

# statistics graph initialization
deltav = 0.2    # bin size of the histogram
vbin = arange(-5, 5, deltav)    # stat range vx = -5 ~ 5
stat_graph = graph(width = winsize, height = 0.6 * winsize, xmin = -5, xmax = 5, ymax = 15, xtitle = 'vx (m/s)', ytitle = 'dN')
theory = gcurve(color = color.cyan)
observation = gvbars(color = color.red, delta = deltav)

# bookkeeping atom position and velocity
X = np.zeros(shape = (N, 3))
V = np.zeros(shape = (N, 3))

# object initialization
for i in range(N):
    xi = L*random() - L/2
    yi = L*random() - L/2
    zi = L*random() - L/2
    atoms.append(sphere(pos = vector(xi, yi, zi), radius = r, color = color.blue))
    X[i] = np.array([xi, yi, zi])
    V[i] = np.array([v_initial, 0., 0.]) 

### <TODO> ###
# compute the total kinetic energy (internal energy)
# compute the temperature
# plot the theoretical velocity distribution
du = 0.01
for u in arange(-5., 5., du):
    #theory.plot(pos=(u, dN(u)))
    continue


# time evolution
t = 0
dt = 0.01

while True:
    rate(1/dt)
    t += dt
    
    # plot and update the histogram of vx
    vx_hist = np.histogram(V[:, 0], bins = vbin)[0]
    observation.delete()
    for i in range(len(vx_hist)):
        observation.plot(vbin[i]+0.5*deltav, vx_hist[i])

    ### <TODO> ###
    # handle the collisions between an atom and walls 
    # handle the collisions between atoms    

    # step forward by dt by X=X+V*dt and update the new positions
    for i in range(N):
        X[i] = X[i] + V[i] * dt
        atoms[i].pos.x = X[i][0]
        atoms[i].pos.y = X[i][1]
        atoms[i].pos.z = X[i][2]
