import numpy as np
import matplotlib.pyplot as plt


class CC:
    # global parameters
    V0 = 1
    Omega = 2 * np.pi * 3000
    R = 5
    C = 10e-6
    L = 200e-6
    dt = 1e-8
    Q_at_t0 = 0
    I_at_t0 = 0
    max_t = 1e-3


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


def get_t_PV_PR_PC_PL():
    ts, Qs, Is = np.array(tuple(gen_t_Q_I())).T
    PVs = np.multiply(Is, CC.V0 * np.sin(CC.Omega * ts))
    PRs = np.multiply(Is, Is * CC.R)
    PCs = np.multiply(Is, Qs / CC.C)
    PLs = np.multiply(Is[:-1], np.diff(Is) / CC.dt * CC.L)
    return ts, PVs, PRs, PCs, np.append(PLs, PLs[-1])


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


def task_3():
    ts, Qs, Is = np.array(tuple(gen_t_Q_I())).T
    Vs = np.array(CC.V0 * np.sin(CC.Omega * ts))

    # determine phase led or lagged
    for index in range(len(Is)):
        if ts[index] > 0.0006 and (Is[index] * Is[index+1] <= 0):
            tmpI = ts[index]
            break
    for index in range(len(Vs)):
        if ts[index] > 0.0006 and (Vs[index] * Vs[index+1] <= 0):
            tmpV = ts[index]
            break
    print(f'I leads V by {(tmpV-tmpI)*CC.Omega:.3f} = {(tmpV-tmpI)*CC.Omega/np.pi:.3f}*pi (unit: rad)')

    # plot
    fig = plt.figure(figsize=(7, 2.6), dpi=250)
    axQ = fig.add_subplot(1, 1, 1)
    axI = axQ.twinx()

    axQ.plot(ts, Vs, label='V(t)', color='tab:green')
    axI.plot(ts, Is, label='I(t)', color='tab:orange')

    axQ.set_title(f'V-t I-t Curve ( dt = {CC.dt} )')
    axQ.set_xlabel('t (sec)')
    axQ.set_ylabel('V (V)', rotation=0)
    axI.set_ylabel('I (A)', rotation=0)
    axQ.tick_params(axis='y', labelcolor='tab:green')
    axI.tick_params(axis='y', labelcolor='tab:orange')
    axQ.axhline(y=0, color='k', linewidth=0.5)
    axQ.set_xlim(left=ts[0], right=ts[-1])
    axQ.legend(loc='upper left')
    axI.legend(loc='upper right')
    plt.subplots_adjust(left=0.1, right=0.9, top=0.88, bottom=0.17)
    plt.show()


def task_4():
    ts, PVs, PRs, PCs, PLs = get_t_PV_PR_PC_PL()

    # fig = plt.figure(figsize=(4, 3), dpi=250)
    fig, (axup, axdown) = plt.subplots(2)

    axup.plot(ts, PRs, label='$P_{R}(t)$')
    axup.plot(ts, PCs, label='$P_{C}(t)$')
    axup.plot(ts, PLs, label='$P_{L}(t)$')

    axdown.plot(ts, PRs+PCs+PLs, label='$P_{RLC}(t)$')
    axdown.plot(ts, PVs, label='$P_{emf}(t)$')

    axup.set_title('$P_{R}(t)$ v.s. $P_{C}(t)$ v.s. $P_{L}(t)$ ' + f'( dt = {CC.dt} )')
    axup.set_xlabel('t (sec)')
    axup.set_ylabel('P (W)', rotation=0)
    axup.axhline(y=0, color='k', linewidth=0.5)
    axup.set_xlim(left=ts[0], right=ts[-1])
    axup.legend(loc='upper right')
    axdown.set_title('$( P_{R}(t) + P_{C}(t) + P_{L}(t) )$ v.s. $P_{emf}(t)$ ' + f'( dt = {CC.dt} )')
    axdown.set_xlabel('t (sec)')
    axdown.set_ylabel('P (W)', rotation=0, labelpad=15)
    axdown.axhline(y=0, color='k', linewidth=0.5)
    axdown.set_xlim(left=ts[0], right=ts[-1])
    axdown.legend(loc='upper right')
    plt.tight_layout()
    plt.show()


# task_2()
# task_3()
task_4()


