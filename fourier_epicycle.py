import numpy as np
from scipy.fft import ifft
from cmath import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import get_points
  
"""Initialize the data"""
# initialize the coordinates of point to fit to and the time step size
values = get_points.values
n_points = len(values)
dt = 0.01
t_steps = np.arange(0, n_points, dt)
n_t = len(t_steps)

# get the coefficients with inverse FFT
coes = ifft(values)
l_coes = abs(coes)

# Creat an array storing all the position: column is time, 
# and row is 2-D coor for each rotating sticks
atlas = np.zeros((n_t, n_points), dtype=complex)
for m in range(0, n_t):
    atlas[m,:] = np.full((1,n_points), exp(-pi*2j*t_steps[m]/n_points))
for n in range(0, n_points):
    atlas[:,n] = coes[n]*(atlas[:,n]**n)
atlas = np.add.accumulate(atlas,1)
real_atlas = atlas.real
imag_atlas = atlas.imag

def init_plt():
    """initialize the plot to click on"""
    # Set various dimension of the plot
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(5, 5))
    L = np.add.reduce(l_coes)
    ax = fig.add_subplot(autoscale_on=False, xlim=(-L, L), ylim=(-L, L), frameon=False)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])

    # Create the circles object to keep track of
    circle_color = (0.4,0.4,0.2)
    balls = [plt.Circle((real_atlas[0,i], imag_atlas[0,i]), radius = l_coes[i+1], 
            ec = circle_color, fill = False) for i in range(0,n_points-1)]
    for ball in balls:
        ax.add_patch(ball)

    # Create the sticks and trace object to keep track of
    trace_color = (1,1,0)
    line_color = (1,1,1)
    line, = ax.plot([], [], '.-', lw=1, c=line_color)
    trace, = ax.plot([], [], ',-', lw=1, c=trace_color)

    #Set the scatter plot for visual effect
    x = values.real
    y = values.imag
    ax.scatter(x,y, s=5)

    return fig, line, trace, balls

"""Animate the plot"""
fig, line, trace, balls = init_plt()
history_len = n_t+10  # how many trajectory points to display
history_x, history_y = deque(maxlen=history_len), deque(maxlen=history_len)

def animate(i):
    thisx = real_atlas[i,:]
    thisy = imag_atlas[i,:]

    history_x.appendleft(thisx[-1])
    history_y.appendleft(thisy[-1])

    line.set_data(thisx, thisy)
    trace.set_data(history_x, history_y)

    for idx, ball in enumerate(balls):
        ball.set_center((real_atlas[i,idx], imag_atlas[i,idx]))

ani = animation.FuncAnimation(fig, animate, n_t, interval=dt*500)
plt.show()
