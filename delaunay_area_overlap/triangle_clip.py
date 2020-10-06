"""
Use PyClipper on two triangles to find their intersection
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pyclipper

def clip(subjectPolygon, clipPolygon):
    def inside(p):
        return(cp2[0]-cp1[0])*(p[1]-cp1[1]) > (cp2[1]-cp1[1])*(p[0]-cp1[0])

    def computeIntersection():
        dc = [ cp1[0] - cp2[0], cp1[1] - cp2[1] ]
        dp = [ s[0] - e[0], s[1] - e[1] ]
        n1 = cp1[0] * cp2[1] - cp1[1] * cp2[0]
        n2 = s[0] * e[1] - s[1] * e[0]
        n3 = 1.0 / (dc[0] * dp[1] - dc[1] * dp[0])
        return [(n1*dp[0] - n2*dc[0]) * n3, (n1*dp[1] - n2*dc[1]) * n3]

    outputList = subjectPolygon
    cp1 = clipPolygon[-1]

    for clipVertex in clipPolygon:
        cp2 = clipVertex
        inputList = outputList
        outputList = []
        try:
            s = inputList[-1]
        except IndexError:
            return [[]], False

        for subjectVertex in inputList:
            e = subjectVertex
            if inside(e):
                if not inside(s):
                    outputList.append(computeIntersection())
                    outputList.append(e)
            elif inside(s):
                outputList.append(computeIntersection())
            s = e
        cp1 = cp2

 
    if outputList:
        return outputList, True
    else:
        return outputList, False

def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

np.random.seed(273875)

fig, ax = plt.subplots()

pts_1 = np.random.uniform(-1, 1, size=(3,2))
p = mpl.patches.Polygon(pts_1, color='C0', alpha=.3, lw=2)
ax.add_patch(p)
ax.plot(pts_1[:,0], pts_1[:,1], 'o', alpha=.5)

pts_2 = np.random.uniform(-1, 1, size=(3,2))
p = mpl.patches.Polygon(pts_2, color='C3', alpha=.3, lw=2)
ax.add_patch(p)
ax.plot(pts_2[:,0], pts_2[:,1], 'o', color='C3', alpha=.5)

ax.autoscale()
ax.set_aspect('equal')

pc = pyclipper.Pyclipper()
pts_1 = pyclipper.scale_to_clipper(pts_1)
pts_2 = pyclipper.scale_to_clipper(pts_2)
pc.AddPath(list(pts_1), pyclipper.PT_CLIP, True)
pc.AddPaths([list(pts_2)], pyclipper.PT_SUBJECT, True)

solution = pc.Execute(pyclipper.CT_INTERSECTION, pyclipper.PFT_EVENODD, pyclipper.PFT_EVENODD)
if solution:
    pts = np.asarray(pyclipper.scale_from_clipper(solution)[0])

    p = mpl.patches.Polygon(pts, color='green', alpha=.3, lw=4)
    ax.plot(pts[:,0], pts[:,1], 'o', color='green', alpha=.5)
    ax.add_patch(p)

    print(PolyArea(pts[:,0], pts[:,1]))

ax.axis('off')
plt.show()