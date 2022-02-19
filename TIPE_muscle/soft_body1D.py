import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
#from bulle import *

#Soft body dans le cas quasi-statique en 1 dimension. 
#On considère ici que les bulles sont equidistantes, on néglige toute force extérieur.

##Constantes :

m_young = (10**(-3))/(4*32)

k, K = m_young*10, 1000*0.02*0.02*m_young/0.06
l0 , L0 = 0.005, 0.02


##initialisation



def long(rayon, k, K, l0, L0, n) :
    return (k*l0 - 2*K*(np.sum(rayon) - L0))/(k + (2*n-1)*K)

def taille(rayon) :
    return n*long(rayon[-1]) + np.sum(rayon[-1])


if __name__=='__main__' :
    T = np.linspace(0, 100, 300)
    rayon = np.array([get_radius_list(T)])
    n = 100
    y=[]
    for i in range(len(T)) :
        rayons=[rayon[0][i] for m in range(n)]
        y.append(taille(rayons))

    plt.plot(rayon[0], y)
    plt.show()
