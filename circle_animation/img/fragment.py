import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(figsize=(12,6), ncols=2, sharex=True, sharey=True, constrained_layout=True)

ax = axes[0]
kwargs = dict(radius=.03, color='k')
ax.add_patch(plt.Circle((1,1), **kwargs))
ax.add_patch(plt.Circle((-1,1), **kwargs))
ax.add_patch(plt.Circle((-1,-1), **kwargs))
ax.add_patch(plt.Circle((1,-1), **kwargs))

xy = [[1,1],[-1,1],[-1,-1]]
t = mpl.patches.Polygon(xy, edgecolor='k', facecolor=(0,0,0,.3), lw=1.5)
ax.add_patch(t)

xy = [[1,1],[1,-1],[-1,-1]]
t = mpl.patches.Polygon(xy, edgecolor='k', facecolor=(0,0,0,.3), lw=1.5)
ax.add_patch(t)
ax.set_title('Vertex Shader', weight='bold', fontsize=24)

ax = axes[1]
kwargs = dict(radius=.03, color='k')
ax.add_patch(plt.Circle((1,1), **kwargs))
ax.add_patch(plt.Circle((-1,1), **kwargs))
ax.add_patch(plt.Circle((-1,-1), **kwargs))
ax.add_patch(plt.Circle((1,-1), **kwargs))

xy = [[1,1],[-1,1],[-1,-1]]
t = mpl.patches.Polygon(xy, edgecolor='k', facecolor=(0,0,0,.0), lw=1.5)
ax.add_patch(t)

xy = [[1,1],[1,-1],[-1,-1]]
t = mpl.patches.Polygon(xy, edgecolor='k', facecolor=(0,0,0,.0), lw=1.5)
ax.add_patch(t)

x = np.linspace(-1,1, 50)
dx = x[1] - x[0]
X, Y = np.meshgrid(x, x)
for i in range(len(x)-1):
    for j in range(len(x)-1):
        pos = np.array((X[i,j], Y[i,j])) + dx/2
        if np.linalg.norm(pos) <= 1:
            r = plt.Rectangle(pos - dx/2, dx, dx, facecolor='C0', edgecolor='k', alpha=1)
            ax.add_patch(r)
        else:
            r = plt.Rectangle(pos - dx/2, dx, dx, facecolor=(0,0,0,0), edgecolor='k')
            ax.add_patch(r)

ax.set_title('Fragment Shader', weight='bold', fontsize=24)

for ax in axes:
    ax.axis('off')
    ax.set_aspect('equal')

    xmax = 1.1
    ax.set_xlim([-xmax,xmax])
    ax.set_ylim([-xmax,xmax])

plt.savefig('circle_fragment.svg', transparent=True)
plt.show()
