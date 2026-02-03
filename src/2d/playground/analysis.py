import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm as cm
from matplotlib import animation as animation
import numpy as np

from read_data import read_data, read_ddata

from sklearn.metrics import root_mean_squared_error

ntimes = 3000 #6000
nsteps = 1
dt = 0.02
nxy = 30

center = nxy // 2

height4, height8 = read_data("h", ntimes, nsteps=nsteps)
u4, u8 = read_data("u", ntimes, nsteps=nsteps)
v4, v8 = read_data("v", ntimes, nsteps=nsteps)

du_x4, du_x8 = read_data("du_x", ntimes, nsteps=nsteps)
du_y4, du_y8 = read_data("du_y", ntimes, nsteps=nsteps)

def plot_u():

    x = list(range(nxy))
    x, y = np.meshgrid(x,x)

    fig, ax = plt.subplots(figsize=(8,8))
    cont = ax.contourf(x, y, u4[0]-u8[0], cmap=cm.coolwarm)
    fig.colorbar(cont)
    def animate(frame):
        ax.set_title(f"time={frame}")
        ax.contourf(x, y, u4[frame]-u8[frame], cmap=cm.coolwarm)
    anim = animation.FuncAnimation(fig, func=animate, frames=ntimes)
    plt.show()

def plot_h_contour(save=False, interval=100):

    x = list(range(nxy))
    x, y = np.meshgrid(x,x)

    fig, (ax1,ax2) = plt.subplots(2, 1, figsize=(8,8))
    cont = ax1.contourf(x, y, height8[0], vmin=-0.5, vmax=1.1, cmap=cm.coolwarm)
    line1 = ax2.plot(height8[0][center,:])[0]
    ax2.set_ylim(-0.5,1)
    def animate(frame):
        ax1.set_title(f"time={interval * frame}")
        ax1.contourf(x, y, height8[frame], vmin=-0.5, vmax=1.1, cmap=cm.coolwarm)
        line1.set_ydata(height8[frame][center,:])
    def callback(current_frame: int, total_frames: int):
        print(f'Processing frame {current_frame} out of {total_frames}')

    anim = animation.FuncAnimation(fig, func=animate, frames=ntimes, interval=interval)
    if save:
        anim.save("wave2d.gif", writer="imagemagick", progress_callback=callback)
    else:
        plt.show()

def plot_hdiff_contour(save=False, interval=1):

    x = list(range(nxy))
    x, y = np.meshgrid(x,x)

    fig, (ax1,ax2) = plt.subplots(2, 2, figsize=(8,8))
    cont = ax1.contourf(x, y, height8[0]-height4[0], cmap=cm.coolwarm)
    line1 = ax2.plot(height8[0][center,:]-height4[0][center,:])[0]
    ax2.set_ylim(-0.5e-6,0.5e-6)
    def animate(frame):
        iframe = interval * frame
        ax1.set_title(f"time={iframe}")
        ax1.contourf(x, y, height8[iframe]-height4[iframe], cmap=cm.coolwarm)
        line1.set_ydata(height8[iframe][center,:]-height4[iframe][center,:])
    def callback(current_frame: int, total_frames: int):
        print(f'Processing frame {current_frame} out of {total_frames}')

    anim = animation.FuncAnimation(fig, func=animate, frames=ntimes)
    if save:
        anim.save("wave2d.gif", writer="imagemagick", progress_callback=callback)
    else:
        plt.show()

def plot_hdiff_slice(save=False, interval=1):

    x = list(range(nxy))
    x, y = np.meshgrid(x,x)

    fig, (ax1,ax2) = plt.subplots(2, 1, figsize=(8,8))

    diff = [height8[i][center,:] - height4[i][center,:] for i in range(ntimes)]
    height = [height8[i][center,:] for i in range(ntimes)]

    line1 = ax1.plot(height[0])[0]
    line2 = ax2.plot(diff[0])[0]
    ax1.set_ylim(-0.5, 1.0)
    ax2.set_ylim(-5e-7, 5e-7)
    def animate(frame):
        iframe = interval * frame
        ax1.set_title(f"time={iframe}")
        line1.set_ydata(height[iframe])
        line2.set_ydata(diff[iframe])
    def callback(current_frame: int, total_frames: int):
        print(f'Processing frame {current_frame} out of {total_frames}')

    anim = animation.FuncAnimation(fig, func=animate, frames=ntimes)
    if save:
        anim.save("wave2d.gif", writer="imagemagick", progress_callback=callback)
    else:
        plt.show()

def plot_udiff_slice(save=False):

    x = list(range(nxy))
    x, y = np.meshgrid(x,x)

    fig, (ax1,ax2) = plt.subplots(2, 1, figsize=(8,8))

    diff = [u8[i][center,:] - u4[i][center,:] for i in range(0, ntimes//nsteps)]
    u8slice = [u8[i][center,:] for i in range(0, ntimes//nsteps)]
    u4slice = [u4[i][center,:] for i in range(0, ntimes//nsteps)]

    line1 = ax1.plot(u8slice[0])[0]
    line2 = ax1.plot(u4slice[0])[0]
    line3 = ax2.plot(diff[0])[0]
    ax1.set_ylim(-0.5, 1.0)
    ax2.set_ylim(-1e-5, 1e-5)
    def animate(frame):
        ax1.set_title(f"time={frame*nsteps}")
        line1.set_ydata(u8slice[frame])
        line2.set_ydata(u4slice[frame])
        line3.set_ydata(diff[frame])
    def callback(current_frame: int, total_frames: int):
        print(f'Processing frame {current_frame} out of {total_frames}')

    anim = animation.FuncAnimation(fig, func=animate, frames=ntimes//nsteps)
    if save:
        anim.save("wave2d.gif", writer="imagemagick", progress_callback=callback)
    else:
        plt.show()


def plot_h8_h4_slice(save=False, interval=1):

    x = list(range(nxy))
    x, y = np.meshgrid(x,x)

    fig, ax1 = plt.subplots(1, figsize=(8,8))
    line1 = ax1.plot(height8[0][center,:], linewidth=5)[0]
    line2 = ax1.plot(height4[0][center,:])[0]
    ax1.set_ylim(-0.5,0.5)
    def animate(frame):
        ax1.set_title(f"time={interval * frame}")
        line1.set_ydata(height8[frame*interval][center,:])
        line2.set_ydata(height4[frame*interval][center,:])
    def callback(current_frame: int, total_frames: int):
        print(f'Processing frame {current_frame} out of {total_frames}')

    anim = animation.FuncAnimation(fig, func=animate, frames=int(ntimes/interval))
    if save:
        anim.save("wave2d.gif", writer="imagemagick", progress_callback=callback)
    else:
        plt.show()


def plot_total_volume():

    volume4 = [np.sum(height4[i]) for i in range(ntimes//nsteps)]
    volume8 = [np.sum(height8[i]) for i in range(ntimes//nsteps)] 
    diff = [volume8[i]-volume4[i] for i in range(ntimes//nsteps)]

    fig, (ax1, ax2) = plt.subplots(2,1)
    ax1.set_ylim(156.2048,156.205)
    ax1.plot(volume4, label="r32")
    ax1.plot(volume8, label="r64")
    ax2.plot(diff)
    ax1.legend()
    plt.show()

def plot_rmse():
    fig, ax = plt.subplots()
    time = [itime * nsteps for itime in range(ntimes//nsteps)]
    udiff = [root_mean_squared_error(u4[itime].flatten(), u8[itime].flatten()) for itime in range(ntimes//nsteps)]
    vdiff = [root_mean_squared_error(v4[itime].flatten(), v8[itime].flatten()) for itime in range(ntimes//nsteps)]
    hdiff = [root_mean_squared_error(height4[itime].flatten(), height8[itime].flatten()) for itime in range(ntimes//nsteps)]
    ax.plot(time, udiff, label="u")
    ax.plot(time, vdiff, label="v")
    ax.plot(time, hdiff, label="h")
    ax.legend()
    plt.show()

def plot_points():
    fig, (ax1, ax2) = plt.subplots(2,1)
    for ix, jx in [(center, center), (0,0), (center//2, center),]:
        u4_ij = [u4[i][ix,jx] for i in range(ntimes//nsteps)]
        u8_ij = [u8[i][ix,jx] for i in range(ntimes//nsteps)]
        udiff = [u4_ij[i] - u8_ij[i] for i in range(len(u4_ij))]
        #ax.plot(u4_ij, u8_ij, label=f"({ix},{jx})")
        ax1.plot(u4_ij, label=f"({ix},{jx})")
        ax2.plot(udiff, label=f"({ix},{jx})")
        ax1.set_xlim(0, 20)
        ax2.set_xlim(0, 20)
        ax1.legend()
        ax2.legend()
    plt.show()

def plot_lag():
        
  fig, ax = plt.subplots(3,5)
  for iax, ix in enumerate([0, center//4, center//2, 3*center//4, center]):
    indices = [(ix, jx) for jx in range(center+1)]
    for ix, jx in indices: 
      for iay, lag in enumerate([1, 2, 3]):
        u4_ij = [u4[i][ix,jx] for i in range(ntimes//nsteps)]
        u8_ij = [u8[i][ix,jx] for i in range(ntimes//nsteps)]
        udiff = [u4_ij[i] - u8_ij[i] for i in range(len(u4_ij))]
        x = [udiff[i] for i in range(ntimes//nsteps - lag)]
        y = [udiff[i+lag] for i in range(ntimes//nsteps - lag)]
        ax[iay, iax].scatter(x, y, label=f"({ix},{jx})", alpha=0.5)
        ax[iay, iax].set_box_aspect(1)
        ax[iay, iax].set_title(f"x={ix}, lag={lag}")
          #ax[iax].legend()
  plt.show()

def plot_lag2():        
  fig, ax = plt.subplots(1,2)
  for iax, ix in enumerate([0, center]):
    indices = [(0,0), (center,center)]#[(ix, jx) for jx in range(center+1)]
    for ix, jx in indices: 
      for iay, lag in enumerate([2]):
        u4_ij = [du_x[i][ix,jx] for i in range(ntimes//nsteps)]
        x = [u4_ij[i] for i in range(ntimes//nsteps - lag)]
        y = [u4_ij[i+lag] for i in range(ntimes//nsteps - lag)]
        ax[iax].scatter(x, y, label=f"({ix},{jx})", alpha=0.5)
        ax[iax].set_box_aspect(1)
        ax[iax].set_title(f"x={ix}, lag={lag}")
        ax[iax].legend()
  plt.show()

fig, ax = plt.subplots()
ax.plot([v8[itme][center,center] for itme in range(ntimes//nsteps)])
ax.plot([u8[itme][center,center] for itme in range(ntimes//nsteps)])
plt.show()

#plot_lag()
#plot_points()
#plot_lag()
#plot_udiff_slice()
#plot_h8_h4_slice()
#plot_h_contour()
#plot_total_volume()
