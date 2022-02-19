# 3d heatmap d'un parallélépipède

import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt


T_ini = 25
A = 75
B = 70
K = (4 / 9)

nb_points = 5000


def chaleur(pos, t):
	# Chaleur en fonction de la distance à la tige et du temps
	# Exponentielle décroissante avec décroissance en K/r pour la distance à l'axe
	# Réglage pour avoir une température max en environ 3 mn (Tmax = 100 pour R = 0 et Tmax = 70 pour R = Rmax = environ 1.5 cm)  (à ajuster avec les valeurs expérimentales)
	x,y,z = np.zeros_like(pos), np.zeros_like(pos), np.zeros_like(pos)
	for i in range(np.size(pos)) :
		x.flat[i], y.flat[i], z.flat[i] = pos.flat[i][0], pos.flat[i][1], pos.flat[i][2]
	result = np.zeros_like(x)
	r = np.sqrt(x**2 + z**2)
	
	for index, rayon in enumerate(r.flat):
		if rayon > R_ressort:
			result[index] = T_ini + A*(1 - np.exp(-t/B)) / (K*(rayon - R_ressort) + 1)
		
		else:
			result[index] = T_ini + Ap*(1 - np.exp(-t/Bp)) / (Kp*(R_ressort - rayon) + 1)
	
	return result

if __name__=='__main__' :
	# Parallépipède de 6 cm de longueur, 3 de largeur, 3 de hauteur
	X = np.linspace(-1.5, 1.5, nb_points)
	Y = np.linspace(0, 6, nb_points)
	Z = np.linspace(-1.5, 1.5, nb_points)

	# On mélange pour avoir une répartition homogène des points sinon ils forment juste une droite
	np.random.shuffle(X)
	np.random.shuffle(Y)
	np.random.shuffle(Z)

	C = chaleur(X, Z, 300)  # Chaleur après 300 s

	fig = plt.figure(figsize=(10, 10))
	ax = fig.add_subplot(111, projection='3d')

	colmap = cm.ScalarMappable(cmap=cm.hsv_r)
	colmap.set_array(C)

	c_map = cm.hsv_r((C - min(C))/(max(C) - min(C)))  # Les exemples de matplotlib mettent plutot cmap = hsv(C/max(C)) mais ducoup l'échelle ne match pas avec celle de la colorbar
	yg = ax.scatter(X, Y, Z, c=c_map, marker='o')
	cb = fig.colorbar(colmap)
	cb.ax.set_ylabel('Chaleur en °C')

	ax.set_xlabel('Largeur x')
	ax.set_ylabel('Longueur y')
	ax.set_zlabel('Hauteur z')

	plt.show()
