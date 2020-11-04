from itertools import cycle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import h5py
from time import time
import matplotlib as mpl

T = 0
dt_log = []

def animate_matplotlib(traj, radii, colors=None, ax=None):
    if ax is None:
        ax = plt.gca()
    if colors is None:
        colors = ['C0']

    fig = ax.figure
    Nparticles = traj.shape[1]

    def update(frame):
        global T
        for i, circle in enumerate(circles):
            circle.center = traj[frame,i]

        if frame > 0:
            dt_log.append(time() - T)
            print(f"{np.average(dt_log)*1e3:.2f} ms")
        T = time()

        return circles

    color_wheel = cycle(colors)
    colors = [next(color_wheel) for i in range(Nparticles)]

    circles = []
    for i,pos in enumerate(traj[0]):
        circles.append(plt.Circle(pos, radii[i], color=colors[i]))
        ax.add_patch(circles[-1])

    ax.set_aspect('equal')
    anim = FuncAnimation(fig, update, len(traj), interval=15)

    xmax = np.max(traj[...,0]) + radii[0]
    xmin = np.min(traj[...,0]) - radii[0]
    ymax = np.max(traj[...,1]) + radii[0]
    ymin = np.min(traj[...,1]) - radii[0]
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])

    return anim

if __name__ == "__main__":
    with h5py.File('../data/small.h5', 'r') as f:
        traj = f['traj'][...]
        radii = f['radii'][...]

    anim = animate_matplotlib(traj, radii, colors=mpl.colors.TABLEAU_COLORS)
    plt.show()


