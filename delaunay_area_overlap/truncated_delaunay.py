"""
Plot a truncated Delaunay tessellation
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.spatial import Delaunay, distance_matrix
import h5py

mpl.rc('font', size=15)
nm = 1e-9

def t_delaunay_plot(points, color, ax):
    D1 = Delaunay(points)
    mask = np.zeros(len(D1.simplices), dtype=bool)
    mask[...] = False
    for i in range(len(mask)):
        p = points[D1.simplices[i]]
        D = distance_matrix(p, p)
        if (D > 1800*nm).any():
            mask[i] = True
        else: 
            patch = mpl.patches.Polygon(p, color=color, alpha=.2)
            ax.add_patch(patch)

    ax.plot(points[:,0], points[:,1], 'o', color=color)
    ax.triplot(points[:,0], points[:,1], D1.simplices, color=color, mask=mask)
    
with h5py.File('./trajectory_two_species.h5', 'r') as f:
    pos = f['pos'][...]
    idx = f['idx'][...]

fig, ax = plt.subplots()
frame = pos[200]
p1 = frame[idx]
t_delaunay_plot(p1, 1800*nm, 'C3', ax)

p2 = np.delete(frame, idx, axis=0)
t_delaunay_plot(p2, 1800*nm, 'C0', ax)
ax.autoscale()
ax.set_aspect('equal')
ax.axis('off')
plt.tight_layout()
plt.show()