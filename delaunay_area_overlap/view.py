"""
Load the data and plot the particles at different frames
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import stoked
import h5py

mpl.rc('font', size=15)
nm = 1e-9 

with h5py.File('./trajectory_two_species.h5', 'r') as f:
    pos = f['pos'][...]
    idx = f['idx'][...]

colors = np.array(['C0']*pos.shape[1])
colors[idx] = 'C3'
# yield stoked.trajectory_animation(pos[::10]/nm, patches=stoked.circle_patches(75), trail=0, colors=colors)
N = pos.shape[0]
fig, axes = stoked.trajectory_snapshots(pos[:N//30:10]/nm, patches=stoked.circle_patches(75), colors=colors, N=4)
fig.patch.set_alpha(0.0)
for i in range(4):
    axes[i].tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
    axes[i].set_title('frame ' + str(int(np.linspace(0, N//30, 4)[i])))
    axes[i].patch.set_alpha(0.0)

plt.show()