import h5py
import matplotlib as mpl
import numpy as np
import circle_vis

def animate_2d(position, radius, colors, xlim=None, ylim=None, background_color='k', time_it=False):
    """
    Create a 2D animation of a trajectory of circles

    Arguments:
        position[T,N,2]       position array of T frames, N particles in 2D
        radius[N]             radius of N particles
        colors                colors of the particles
        xlim[2]               view limits of x-axis (default: auto-compute)
        xlim[2]               view limits of y-axis (default: auto-compute)
        background_color      color of the background (default: black)
    """
    vshader = f'../shaders/circle_instanced.vs'
    fshader = f'../shaders/circle_simple.fs'
    rgba = mpl.colors.to_rgba_array(colors)
    background_color = mpl.colors.to_rgb(background_color)

    rmax = np.max(radius)
    if xlim is not None:
        xmin, xmax = xlim
    else:
        xmin = np.min(position[...,0]) - rmax
        xmax = np.max(position[...,0]) + rmax
    if ylim is not None:
        ymin, ymax = ylim
    else:
        ymin = np.min(position[...,1]) - rmax
        ymax = np.max(position[...,1]) + rmax
    dims = np.array([[xmin, xmax], [ymin, ymax]], dtype=float)

    circle_vis.circle_vertex_instanced(position=position,
                         radii=radius,
                         dims=dims,
                         colors=rgba,
                         background_color=background_color,
                         vshader=vshader,
                         fshader=fshader,
                         time_it=time_it)

with h5py.File('../data/medium.h5', 'r') as f:
    traj = f['traj'][...]
    radii = f['radii'][...]

colors = mpl.colors.TABLEAU_COLORS
animate_2d(traj, radii, colors, background_color='white', time_it=True)
