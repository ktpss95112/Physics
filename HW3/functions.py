from vpython import *
import matplotlib.pyplot as plt

def Homework(position, velocity, figname, draw_q=False):
    class SimpleHarmonicOscillation():
        dt = 0.0001
        t = 0
        eps = 0.0005
        spring_length = 0.5
        k = 10
        ground = box(pos=vec(0, -0.6, 0), length=10, width=3, height=0.1)
        SHOW_ANIMATION = False

        def __init__(self, position, velocity):
            self.init_pos = position
            self.init_vel = velocity
            self.ball1 = sphere(dx=position[0], pos=vec(-self.spring_length+position[0],0,0), velocity=vec(velocity[0],0,0), radius=0.25)
            self.ball2 = sphere(dx=position[1], pos=vec(                    position[1],0,0), velocity=vec(velocity[1],0,0), radius=0.25)
            self.ball3 = sphere(dx=position[2], pos=vec( self.spring_length+position[2],0,0), velocity=vec(velocity[2],0,0), radius=0.25)
            self.list_x1 = [self.ball1.dx]
            self.list_x2 = [self.ball2.dx]
            self.list_x3 = [self.ball3.dx]
            self.list_t = [self.t]
            self.list_q1 = [self.ball1.dx + 2*self.ball2.dx + self.ball3.dx]
            self.list_q2 = [self.ball1.dx - self.ball3.dx]
            self.list_q3 = [self.ball1.dx - 2*self.ball2.dx + self.ball3.dx]

        def iterate(self):
            a1 = self.k*(self.ball2.dx - self.ball1.dx)
            a2 = 0.5*self.k*(self.ball1.dx + self.ball3.dx - 2*self.ball2.dx)
            a3 = self.k*(self.ball2.dx - self.ball3.dx)
            self.ball1.pos.x += self.ball1.velocity.x * self.dt
            self.ball2.pos.x += self.ball2.velocity.x * self.dt
            self.ball3.pos.x += self.ball3.velocity.x * self.dt
            self.ball1.dx = self.ball1.pos.x + self.spring_length
            self.ball2.dx = self.ball2.pos.x
            self.ball3.dx = self.ball3.pos.x - self.spring_length
            self.ball1.velocity.x += a1 * self.dt
            self.ball2.velocity.x += a2 * self.dt
            self.ball3.velocity.x += a3 * self.dt
            self.t += self.dt

        period = 1000000000
        def print_peroid(self):
            if self.period != 1000000000: return
            if abs(self.ball1.dx-self.init_pos[0])<self.eps\
                and abs(self.ball2.dx-self.init_pos[1])<self.eps\
                and abs(self.ball3.dx-self.init_pos[2])<self.eps\
                and abs(self.ball1.velocity.x-self.init_vel[0])<self.eps\
                and abs(self.ball2.velocity.x-self.init_vel[1])<self.eps\
                and abs(self.ball3.velocity.x-self.init_vel[2])<self.eps:
                print(f'Period: {self.t:.3f}')
                self.period = self.t

        def run(self):
            # debug
            #counter = 0
            while self.t <= 6:
                if self.SHOW_ANIMATION: rate(1/self.dt)
                self.iterate()

                self.list_x1.append(self.ball1.dx)
                self.list_x2.append(self.ball2.dx)
                self.list_x3.append(self.ball3.dx)
                self.list_t.append(self.t)
                self.list_q1.append(self.ball1.dx + 2*self.ball2.dx + self.ball3.dx)
                self.list_q2.append(self.ball1.dx - self.ball3.dx)
                self.list_q3.append(self.ball1.dx - 2*self.ball2.dx + self.ball3.dx)


                # debug
                '''if counter%10 == 0:
                    print('%.6f %.6f %.6f %.6f %.6f %.6f'%(
                        self.ball1.dx, self.ball2.dx, self.ball3.dx,
                        self.ball1.velocity.x,
                        self.ball2.velocity.x,
                        self.ball3.velocity.x,
                    ))
                counter += 1'''

                if self.t > 50*self.dt:
                    self.print_peroid()

        def draw(self):
            self.fig, self.ax = plt.subplots()

            if not draw_q:
                self.ax.set_title(f'x-t graph (x1,x2,x3)=(%.2f,%.2f,%.2f) (v1,v2,v3)=(%.2f,%.2f,%.2f)'%(*position, *velocity))
                self.ax.set_xlabel('t (sec)')
                self.ax.set_ylabel('x (m)')
                self.ax.plot(self.list_t, self.list_x1, label='x1')
                self.ax.plot(self.list_t, self.list_x2, label='x2')
                self.ax.plot(self.list_t, self.list_x3, label='x3')
                self.ax.legend(loc='upper right')
                self.ax.grid(b=True)
            else:
                self.ax.set_title(f'q-t graph')
                self.ax.set_xlabel('t (sec)')
                self.ax.set_ylabel('q (m)')
                self.ax.plot(self.list_t, self.list_q1, label='q1')
                self.ax.plot(self.list_t, self.list_q2, label='q2')
                self.ax.plot(self.list_t, self.list_q3, label='q3')
                self.ax.legend(loc='upper right')
                self.ax.grid(b=True)
            self.fig.savefig(figname)

        def __del__(self):
            self.ball1.visible = False
            self.ball2.visible = False
            self.ball3.visible = False
            del self.ball1, self.ball2, self.ball3
            self.draw()

    task = SimpleHarmonicOscillation(position, velocity) 
    task.run()
