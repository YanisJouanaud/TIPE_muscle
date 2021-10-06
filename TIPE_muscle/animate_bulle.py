import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation


fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = plt.axes(xlim=(-7, 7), ylim=(-7, 7))

bulle = plt.Circle((0.0, 0.0),
                        radius=1.0,
                        color='b', alpha=0.5,
                        fill=True)


def get_radius_expansion(t):
    return 5 * (1 - np.exp(-t/100))


def init():
    bulle.center = (0, 0)
    ax.add_patch(bulle)
    return bulle,


def animate(i):
    bulle.radius = 1 + get_radius_expansion(i)
    return bulle,


anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=300, 
                               interval=20,
                               blit=True)

plt.show()
