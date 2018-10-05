from vpython import *
from math import sqrt, sin, cos, radians
import matplotlib.pyplot as plt

# parameters
g = 9.8
m = 0.1
v0 = 100
theta = radians(75)
k = 0.001
vw = 20
dt = 0.001

# execution settings
# drag=T, wind=T : wind
# drag=F, wind=F : no wind 1.drag , 2.no drag
# drag=T, wind=F : no wind 1.drag
SHOW_ANIMATION = False
DRAG = True
WIND = True

def iteration(pos, velocity):
    global g, m, k, vw, WIND, DRAG, dt
    if WIND:
        v_rela = vec(velocity.x, velocity.y, velocity.z-vw)
    else:
        v_rela = vec(velocity.x, velocity.y, velocity.z)
    
    if DRAG:
        return (pos + dt*velocity,
                velocity + dt*vec(0,-g,0) + dt*(-k/m)*v_rela.mag*v_rela)
    else:
        return (pos + dt*velocity,
                velocity + dt*vec(0,-g,0))

# initial condition
scene = canvas(center=vec(50, 50, 50))
ground = box(pos=vec(50, -2, 50),
             length=100,
             width=100,
             height=1)
ball = sphere(pos=vec(0, 0, 0),
              velocity=vec(v0*cos(theta), v0*sin(theta), 0),
              radius=1,
              make_trail=True)

plot_x = []
plot_y = []
plot_z = []

max_height = 0
max_height_x = 0

# iteration
while ball.pos.y >= 0:
    if SHOW_ANIMATION:
        rate(1/dt)

    ball.pos, ball.velocity = iteration(ball.pos, ball.velocity)
    plot_x.append(ball.pos.x)
    plot_y.append(ball.pos.y)
    plot_z.append(ball.pos.z)

    if max_height < ball.pos.y:
        max_height = ball.pos.y
        max_height_x = ball.pos.x


# plot settings
plt.title('Trajectory of the Ball')
if WIND:
    plt.xlabel('x Distance (m)')
    plt.ylabel('z Distance(wind) (m)')
    plt.annotate('(%.2f, %.2f)'%(plot_x[-1], plot_z[-1]),
                 xy=(plot_x[-1], plot_z[-1]),
                 xytext=(plot_x[-1]-18, plot_z[-1]-2))
    plt.plot(plot_x, plot_z)
else:
    plt.xlabel('x Distance (m)')
    plt.ylabel('y Height (m)')
    plt.annotate('maximal height %.2f'%(max_height),
                 xy=(max_height_x, max_height),
                 xytext=(max_height_x, max_height))
    plt.annotate('maximal distance %.2f'%(plot_x[-1]),
                 xy=(plot_x[-1], plot_y[-1]),
                 xytext=(plot_x[-1]-145, plot_y[-1]))
    plt.plot(plot_x, plot_y)

# no wind
if not WIND:
    DRAG = True
    max_height = 0
    max_height_x = 0
    ball = sphere(pos=vec(0, 0, 0),
                  velocity=vec(v0*cos(theta), v0*sin(theta), 0),
                  radius=1,
                  make_trail=True)
    
    plot_x = []
    plot_y = []
    plot_z = []

    while ball.pos.y >= 0:
        if SHOW_ANIMATION:
            rate(1/dt)

        ball.pos, ball.velocity = iteration(ball.pos, ball.velocity)
        plot_x.append(ball.pos.x)
        plot_y.append(ball.pos.y)
        plot_z.append(ball.pos.z)

        if max_height < ball.pos.y:
            max_height = ball.pos.y
            max_height_x = ball.pos.x
    
    plt.xlabel('x Distance (m)')
    plt.ylabel('y Height (m)')
    plt.annotate('maximal height %.2f'%(max_height),
                 xy=(max_height_x, max_height),
                 xytext=(max_height_x, max_height))
    plt.annotate('maximal distance %.2f'%(plot_x[-1]),
                 xy=(plot_x[-1], plot_y[-1]),
                 xytext=(plot_x[-1], plot_y[-1]))
    plt.plot(plot_x, plot_y)

plt.show()
