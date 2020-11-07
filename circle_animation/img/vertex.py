import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(figsize=(12,6), ncols=2, sharex=True, sharey=True, constrained_layout=True)

ax = axes[0]

kwargs = dict(radius=.03, color='k')
ax.add_patch(plt.Circle((0,0), **kwargs))

theta = np.linspace(0,2*np.pi, 11)
for i,th in enumerate(theta[:-1]):
    x = np.cos(th)
    y = np.sin(th)
    ax.add_patch(plt.Circle((x,y), **kwargs))

    x1 = np.cos(theta[i])
    y1 = np.sin(theta[i])
    x2 = np.cos(theta[i+1])
    y2 = np.sin(theta[i+1])
    xy = [[0,0],[x1,y1],[x2,y2]]
    t = mpl.patches.Polygon(xy, edgecolor='k', facecolor=(0,0,0,.3), lw=1.5)
    ax.add_patch(t)

ax.set_title('Vertex Shader', weight='bold', fontsize=24)

ax = axes[1]

triangles = []
for i,th in enumerate(theta[:-1]):
    x = np.cos(th)
    y = np.sin(th)
    ax.add_patch(plt.Circle((x,y), **kwargs))

    x1 = np.cos(theta[i])
    y1 = np.sin(theta[i])
    x2 = np.cos(theta[i+1])
    y2 = np.sin(theta[i+1])

    xy = [[0,0],[x1,y1],[x2,y2]]
    triangles.append(xy)

    t = mpl.patches.Polygon(xy, edgecolor='k', facecolor=(0,0,0,0), lw=1.5)
    ax.add_patch(t)

x = np.linspace(-1,1, 50)
dx = x[1] - x[0]
X, Y = np.meshgrid(x, x)

triangles = np.array(triangles)
t = triangles[0]
area = 0.5 *(-t[1,1]*t[2,0] + t[0,1]*(-t[1,0] + t[2,0]) + t[0,0]*(t[1,1] - t[2,1]) + t[1,0]*t[2,1]);

for i in range(len(x)-1):
    for j in range(len(x)-1):
        pos = np.array((X[i,j], Y[i,j])) + dx/2

        for tri in triangles:
            s = 1/(2*area)*(tri[0,1]*tri[2,0] - tri[0,0]*tri[2,1] + (tri[2,1] - tri[0,1])*pos[0] + (tri[0,0] - tri[2,0])*pos[1]);
            t = 1/(2*area)*(tri[0,0]*tri[1,1] - tri[0,1]*tri[1,0] + (tri[0,1] - tri[1,1])*pos[0] + (tri[1,0] - tri[0,0])*pos[1]);

            if s >= 0 and t >= 0 and 1 - s - t >= 0:
                r = plt.Rectangle(pos - dx/2, dx, dx, facecolor='C0', edgecolor='k', alpha=1)
                ax.add_patch(r)

ax.set_title('Fragment Shader', weight='bold', fontsize=24)

for ax in axes:
    ax.axis('off')
    ax.set_aspect('equal')

    xmax = 1.1
    ax.set_xlim([-xmax,xmax])
    ax.set_ylim([-xmax,xmax])

plt.savefig('circle_vertex.svg', transparent=True)
plt.show()
