"""
Find the area of overlap of two delaunay tessellations
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.spatial import Delaunay, distance_matrix
import h5py

mpl.rc('font', size=15)
nm = 1e-9 

def area_overlap(p1, p2, thresh=1800*nm):
    D1 = Delaunay(p1).simplices
    D2 = Delaunay(p2).simplices
    area = 0

    for i in range(len(D1)):
        for j in range(len(D2)):
            pts_1 = p1[D1[i]]
            pts_2 = p2[D2[j]]

            d1 = distance_matrix(pts_1, pts_1)
            if (d1 > thresh).any():
                continue

            d2 = distance_matrix(pts_2, pts_2)
            if (d2 > thresh).any():
                continue

            pc = pyclipper.Pyclipper()
            pts_1 = pyclipper.scale_to_clipper(pts_1)
            pts_2 = pyclipper.scale_to_clipper(pts_2)
            pc.AddPath(list(pts_1), pyclipper.PT_CLIP, True)
            pc.AddPaths([list(pts_2)], pyclipper.PT_SUBJECT, True)

            solution = pc.Execute(pyclipper.CT_INTERSECTION, pyclipper.PFT_EVENODD, pyclipper.PFT_EVENODD)
            if solution:
                pts = np.asarray(pyclipper.scale_from_clipper(solution)[0])
                A = PolyArea(pts[:,0], pts[:,1])
                area += A

    return area
  
fig, ax = plt.subplots()
A = []
for i in pbar(range(0, len(pos)//10, 20)):
    p1 = pos[i,idx]
    p2 = np.delete(pos[i], idx, axis=0)
    A.append(area_overlap(p1, p2))
ax.plot(A)
ax.set(xlabel='frame', ylabel='area overlap')
plt.show()