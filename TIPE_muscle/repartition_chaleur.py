import numpy as np
import matplotlib.pyplot as plt


def chaleur(r, t):
	# Chaleur en fonction de la distance à la tige et du temps
	# Exponentielle décroissante avec décroissance en K/r pour la distance à l'axe
	# Réglage pour avoir une température max en environ 3 mn (Tmax = 100 pour R = 0 et Tmax = 70 pour R = Rmax = environ 1.5 cm)
	T_ini = 25
	A = 75
	B = 70
	K = (4 / 9) * 10 ** 2
	return T_ini + A*(1 - np.exp(-t/B)) / (K*r + 1)


t_lin = np.linspace(0, 500, 100000)

rayons = np.array([0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4])*10**(-2)

for rayon in rayons:
	plt.plot(t_lin, chaleur(rayon, t_lin), label='R = {} m'.format(rayon))

plt.xlabel('Temps t (en s)')
plt.ylabel('Chaleur (en °C)')
plt.legend()
plt.show()
