import numpy as np
import matplotlib.pyplot as plt


class CC:
    # global parameters
    V0 = 1
    Omega = 2 * np.pi * 3000
    R = 5
    C = 10e-6
    L = 200e-6
    dt = 1e-7
    Q_at_t0 = 0
    I_at_t0 = 0
    max_t = dt * 10000


def gen_t_Q_I():
    curly_E = lambda t: np.matrix([ [0.] , [CC.V0 * np.sin(CC.Omega * t) / CC.L]])
    QI = np.matrix([ [CC.Q_at_t0] , [CC.I_at_t0] ])
    M = np.matrix([ [0., 1.] , [-1/(CC.L * CC.C), -CC.R/CC.L] ])
    t = 0.
    yield t, QI[0,0], QI[1,0]

    while t < CC.max_t:
        t += CC.dt
        QI = QI + CC.dt * ( M * QI + curly_E(t) )
        yield t, QI[0,0], QI[1,0]


def task_2():
    ts, Qs, Is = np.array(tuple(gen_t_Q_I())).T

    fig = plt.figure(figsize=(7, 2.6), dpi=250)
    axQ = fig.add_subplot(1, 1, 1)
    axI = axQ.twinx()

    axQ.plot(ts, Qs*1e6, label='Q(t)', color='tab:blue')
    axI.plot(ts, Is, label='I(t)', color='tab:orange')

    axQ.set_title(f'Q-t I-t Curve ( dt = {CC.dt} )')
    axQ.set_xlabel('t (sec)')
    axQ.set_ylabel(r'Q ($\mu$C)', rotation=0)
    axI.set_ylabel('I (A)', rotation=0)
    axQ.tick_params(axis='y', labelcolor='tab:blue')
    axI.tick_params(axis='y', labelcolor='tab:orange')
    axQ.axhline(y=0, color='k', linewidth=0.5)
    axQ.set_xlim(left=ts[0], right=ts[-1])
    axQ.legend(loc='upper left')
    axI.legend(loc='upper right')
    plt.subplots_adjust(left=0.1, right=0.9, top=0.88, bottom=0.17)
    plt.show()





task_2()



