import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.animation as animation


T_ini = 25
A = 75
B = 70
K = (4 / 9)

nb_points = 5000
temps_anim = 300


def chaleur(x, z, t):
    r = np.sqrt(x**2 + z**2)
    return T_ini + A*(1 - np.exp(-t/B)) / (K*r + 1)


def animate(i):
    fig.clear()
    ax = fig.add_subplot(111, projection='3d')

    C = chaleur(X, Z, i + 1)  # Chaleur après i secondes

    colmap = cm.ScalarMappable(cmap=cm.hsv_r)
    colmap.set_clim(C_min, C_max)

    c_map = cm.hsv_r((C - C_min)/(C_max - C_min))
    yg = ax.scatter(X, Y, Z, c=c_map, marker='o')
    cb = fig.colorbar(colmap)
    cb.ax.set_ylabel('Chaleur en °C')

    ax.set_xlabel('Largeur x')
    ax.set_ylabel('Longueur y')
    ax.set_zlabel('Hauteur z')

    ax.set_title('Temps: {} min {} s'.format(*divmod(i, 60)))


if __name__ == '__main__':
    fig = plt.figure(figsize=(10, 10))

    # Parallépipède de 6 cm de longueur, 3 de largeur, 3 de hauteur
    X = np.linspace(-1.5, 1.5, nb_points)
    Y = np.linspace(0, 6, nb_points)
    Z = np.linspace(-1.5, 1.5, nb_points)

    # On mélange pour avoir une répartition homogène des points sinon ils forment juste une droite
    np.random.shuffle(X)
    np.random.shuffle(Y)
    np.random.shuffle(Z)

    C_min = T_ini
    C_max = max(chaleur(X, Y, temps_anim + 1))

    anim = animation.FuncAnimation(fig, animate, frames=temps_anim, interval=10, blit=False)
    #anim.save('test_repartition.gif', writer='pillow')
    plt.show()
