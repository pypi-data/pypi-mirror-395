import os
import sys
import shutil
import numpy as np
import matplotlib.pyplot as plt

path = sys.argv[1]

path = os.path.abspath(path)
FIELDS = os.path.join(path, "fields")
FRAMES = os.path.join(path, "frames")
MOVIE = os.path.join(path, "sim.mp4")
shutil.rmtree(FRAMES, ignore_errors=True)
os.makedirs(FRAMES, exist_ok=True)
shutil.rmtree(MOVIE, ignore_errors=True)

g = np.load(os.path.join(path, "temp", 'g.npy')).T
gmax = np.max(np.abs(g))

dir = os.path.join(path, "temp", 'fields')
umax = 0
fns = sorted(os.listdir(dir), key=lambda x: float(x[0:-4]))
for fn in fns:
    a = np.load(os.path.join(dir, fn))
    v = np.max(np.abs(a))
    if umax < v:
        umax = v

for fn in fns:
    name = fn[0:-4]
    a = np.load(os.path.join(FIELDS, fn)).T
    fig, axs = plt.subplots(1, 2)
    axs[1].imshow(a, cmap='seismic', origin='lower',
                  vmin=-umax, vmax=umax)
    axs[0].imshow(-g, cmap='gray',
                  origin='lower', vmin=-gmax, vmax=0)
    plt.savefig(os.path.join(FRAMES, f"{name}.png"))
    plt.close(fig)
