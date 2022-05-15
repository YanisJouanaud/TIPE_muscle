import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from bulle_debug import *

#Soft body dans le cas quasi-statique en 1 dimension. 
#On considère ici que les bulles sont equidistantes, on néglige toute force extérieur.

##Constantes :

m_young = (10**(-3))/(4*32)

k, K = m_young*10, 1000*0.02*0.02*m_young/0.06
l0 , L0 = 0.005, 0.02


##initialisation



def long(rayon, k, K, l0, L0, n, alpha) :
    return (k*l0 - 2*K*(alpha*np.sum(rayon) - L0))/(k + (2*n-1)*K)

def taille(rayon) :
    k, K = m_young*10, 1000*0.02*0.02*m_young/0.06  #random parce que j'ai la flemme
    l0 , L0 = 0.005, 0.02
    return n*long(rayon, k, K,l0, L0, n, 0.94) + np.sum(rayon) + 0.01


if __name__=='__main__' :
    T = np.linspace(0, 300, 1000)
    rayon = np.array([get_radius_list(T)])
    n = 100
    y=[]
    for i in range(len(T)) :
        rayons=[rayon[0][i]]*n
        y.append(taille(rayons))

    print(y)
    plt.plot(T, rayon[0])
    plt.grid()
    plt.xlabel("Temps (s)")
    plt.ylabel("Taille du muscle (m)")
    plt.show()
