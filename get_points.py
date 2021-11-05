# Implementation of matplotlib function
import matplotlib.pyplot as plt
import numpy as np
import sys

plt.style.use('dark_background')
fig = plt.figure(figsize=(5, 5))
L = 10
ax = fig.add_subplot(autoscale_on=False, xlim=(-L, L), ylim=(-L, L))
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])

values = plt.ginput(100)
values = np.array([complex(x,y) for (x,y) in values])

plt.close()