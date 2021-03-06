from vpython import *
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations
import matplotlib.animation as animation


# parameters
r = 0.02
L = 1.0
m = 4.0e-3/6.02e23
kB = 1.38e-23
v_init = 5.0
SHOW_ANIMATION = True
t = 0
dt = 0.01
N = 200
deltav = 1
T = 0.004
pressure_period = 1
u = 0.1

def disable_animation():
    global SHOW_ANIMATION
    SHOW_ANIMATION = False


def animation_init():
    global r, L, SHOW_ANIMATION
    if not SHOW_ANIMATION: return
    scene = canvas(width = 500, height = 450)
    scene.range = L
    d = L/2 + r
    borders_bot = curve(pos = [(d, -d, d), (-d, -d, d), (-d, -d, -d), (d, -d, -d), (d, -d, d)], radius = 0.005, color = color.white)
    borders_top = curve(pos = [(d, d, d), (-d, d, d), (-d, d, -d), (d, d, -d), (d, d, d)], radius = 0.005, color = color.white)
    borders_1 = curve(pos = [(d, -d, d), (d, d, d)], radius = 0.005, color = color.white)
    borders_2 = curve(pos = [(d, -d, -d), (d, d, -d)], radius = 0.005, color = color.white)
    borders_3 = curve(pos = [(-d, -d, d), (-d, d, d)], radius = 0.005, color = color.white)
    borders_4 = curve(pos = [(-d, -d, -d), (-d, d, -d)], radius = 0.005, color = color.white)



class Atom:
    def __init__(self, position = vec(0., 0., 0.), velocity = vec(0., 0., 0.)):
        self.pos = position
        self.vel = velocity

atoms = [Atom() for _ in range(N)]
atoms_ani = []
def particles_init():
    global r, L, v_init, SHOW_ANIMATION, N, atoms, atoms_ani
    for i in range(N):
        atoms[i].pos = vector(*[L*random() - L/2 for _ in range(3)])
        atoms[i].vel = v_init * vec.random().norm()
        if SHOW_ANIMATION:
            atoms_ani.append(sphere(pos = atoms[i].pos, radius = r, color = color.blue))



pressure = 0
right_wall_pos = L/2
def evolve(right_wall_fixed):
    global r, L, m, SHOW_ANIMATION, t, dt, N, atoms, atoms_ani, pressure_period, right_wall_pos
    # generate next position and velocity
    for i in range(N):
        atoms[i].pos += atoms[i].vel * dt

    # handle collision between two atoms
    for at1, at2 in combinations(atoms, 2):
        def distance(pos1, pos2):
            return sqrt(pos1.mag2 + pos2.mag2 - 2*dot(pos1, pos2))

        if distance(at1.pos, at2.pos) <= 2*r:
            x1, x2 = at1.pos, at2.pos
            v1, v2 = at1.vel, at2.vel
            at1.vel = v1 - dot(v1-v2, x1-x2)/mag2(x1-x2)*(x1-x2)
            at2.vel = v2 + dot(v1-v2, x1-x2)/mag2(x1-x2)*(x1-x2)

    # handle collision between atoms and wall
    # calculate pressure
    global pressure
    if abs(t - pressure_period) < 0.1*dt: pressure, t = 0, 0
    if (not right_wall_fixed) and (right_wall_pos < (3/2)*L):
        right_wall_pos += u * dt

    for at in atoms:
        if at.pos.x >= right_wall_pos-r: pressure += ((2 * m * at.vel.x) / (pressure_period)) / (L ** 2)
        
        if not right_wall_fixed:
            if at.pos.x >= right_wall_pos-r:
                if right_wall_pos < (3/2)*L: at.vel.x = 2*u - at.vel.x
                else:                        at.vel.x *= -1
                at.pos.x = right_wall_pos
            if at.pos.x <= -L/2+r:
                at.pos.x = -L/2
                at.vel.x *= -1
        elif not -L/2+r < at.pos.x < L/2-r:
            at.pos.x = L/2-r if at.pos.x > 0 else -L/2+r
            at.vel.x *= -1
        if not -L/2+r < at.pos.y < L/2-r:
            at.pos.y = L/2-r if at.pos.y > 0 else -L/2+r
            at.vel.y *= -1
        if not -L/2+r < at.pos.z < L/2-r:
            at.pos.z = L/2-r if at.pos.z > 0 else -L/2+r
            at.vel.z *= -1

    t += dt

    if SHOW_ANIMATION:
        # TODO: move right wall if not right_wall_fixed
        for i in range(N):
            atoms_ani[i].pos = atoms[i].pos




if __name__ == '__main__':
    animation_init()
    particles_init()

    while True:
        evolve(right_wall_fixed=True)



def task_3():
    def draw_theory_line():
        global m, kB, N, deltav, T
        vx = np.arange(-10, 11, deltav)
        n = [N*deltav*sqrt(m/(2*pi*kB*T))*exp(-(m/(2*kB*T))*(_vx**2)) for _vx in vx]
        plt.plot(vx, n)

    fig, ax = plt.subplots()
    ax.set_title('Distribution of Velocity')
    ax.set_xlabel('velocity (m/s)')
    ax.set_ylabel('number of particles')

    def update_hist(frame):
        global m, kB, deltav, atoms, T
        ax.cla()
        ax.grid()
        ax.set_title('Distribution of Velocity')
        ax.set_xlabel('velocity (m/s)')
        ax.set_ylabel('number of particles')
        draw_theory_line()

        evolve(right_wall_fixed=True)
        vx_list = [at.vel.x for at in atoms]
        ax.hist(vx_list, np.arange(-10, 10+deltav, deltav))
        plt.xticks(np.arange(-10, 10+deltav, 1))
        ax.set_xlim(-10, 10)
        ymax = (N*deltav*sqrt(m/(2*pi*kB*T))) * 1.1
        plt.yticks(np.arange(0, ymax, 3))
        ax.set_ylim(top=ymax)
        # TODO: use blit and patch to boost performance

    draw_theory_line()
    global animation
    animation = animation.FuncAnimation(fig, update_hist)
    plt.show()



def task_4():
    global pressure
    while True:
        if abs(t - pressure_period) < 0.1*dt:
            print('Pressure:', pressure)
            global N, kB, T, L
            print('Ideal   :', (N * kB * T / (L ** 3)))
            print()
        evolve(right_wall_fixed=True)




def task_5():
    # let the particles run for a while in order to distribute the velocity
    for _ in range(50):
        evolve(right_wall_fixed=True) 

    fig, ax = plt.subplots()
    line, = ax.plot([], [])
    ax.grid()
    ax.set_title('Temperature of Expanding Box')
    ax.set_xlabel('time (sec)')
    ax.set_ylabel('temperature (K)')

    #t_list = [0]
    #T_list = [(m * np.mean(np.square([at.vel.mag for at in atoms]))) / (3 * kB)]

    def init():
        global atoms, m, kB
        global t_list, T_list
        global printed_expand_maximum
        printed_expand_maximum = False
        t_list = [0]
        T_list = [(m * np.mean(np.square([at.vel.mag for at in atoms]))) / (3 * kB)]
        ax.set_ylim(0.0015, T_list[-1]*1.1)
        line.set_data(t_list, T_list)
        return line,

    def update_graph(frame):
        global dt, atoms, m, kB
        global t_list, T_list
        evolve(right_wall_fixed=False)
        global printed_expand_maximum
        if (right_wall_pos >= (3/2)*L) and (not printed_expand_maximum):
            print('expand reach maximum')

        t_list.append(t_list[-1] + dt)
        rms2 = np.mean(np.square([at.vel.mag for at in atoms]))
        T_list.append((m * rms2) / (3 * kB))
        print('T =', T_list[-1])

        tmin, tmax = ax.get_xlim()
        if t_list[-1] >= tmax:
            ax.set_xlim(tmin, 2*tmax)
            ax.figure.canvas.draw()
        line.set_data(t_list, T_list)
        return line,

    global animation
    animation = animation.FuncAnimation(fig, update_graph, blit=True, init_func=init, interval=1)
    plt.show()




def task(num):
    eval(f'task_{num}()')



