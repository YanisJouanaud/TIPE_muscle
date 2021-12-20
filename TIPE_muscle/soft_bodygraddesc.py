import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from bulle import *

m_young = (10**(-3))/(4*32)

k1, k2, K = m_young*10, m_young*10, 1000*0.02*0.02*m_young/0.06
l01, l02, L0 = 0.005, 0.005, 0.02
y=[]
def energie(rayons, distances) :
    Emilieu=0
    for i in range(len(distances)-2) :
        Emilieu+=1/2*k2*(distances[i+1]-l02)**2
    E=1/2*k1*((distances[0]-l01)**2+(distances[-1]-l01)**2)+Emilieu+1/2*K*(np.sum(distances)+2*np.sum(rayons)-L0)**2
    return E

def plotting(f, rayons) :
    ax = plt.axes(projection='3d')
    x = np.arange(-10,10,0.1)
    y = np.arange(-10,10,0.1)

    X, Y = np.meshgrid(x, y)
    Z = f(rayons, [X, Y])

    ax.plot_surface(X, Y, Z, cmap = plt.cm.cividis)

    ax.set_xlabel('x', labelpad=20)
    ax.set_ylabel('y', labelpad=20)
    ax.set_zlabel('z', labelpad=20)

    plt.show()

def deriv(f, i, r, x) :
    epsilon=1e-4
    xa=np.copy(x)
    x[i]+=epsilon
    return (f(r, x)-f(r, xa))/epsilon

def gradient_descent(f, r, n, ini) :
    pos = ini
    grad = np.array([deriv(f,i,r,pos) for i in range(n+1)])
    while abs(np.sum(grad))>1e-7:
        print(np.sum(grad))
        pos -= 1e4*grad
        grad = np.array([deriv(f,i,r,pos) for i in range(n+1)])
    return pos

def rayon(t):
    return 10-1000*np.exp(-1*t-5)

def taille(rayon, nb_bulles, ini) :
    rayons=rayon*np.ones((nb_bulles, 1))
    longueurs=gradient_descent(energie, rayons, nb_bulles, ini)
    return longueurs

y=[]
T = np.linspace(0, 300, 300)
z=[]
rayons = 0.008*np.ones((len(T),1))#get_radius_list(T)
pos = np.ones((7, 1))
for t in range(len(T)) :
    print(t)
    pos=taille(rayons[t], 6, 10*np.ones((7,1)))
    y.append(np.sum(pos)+2*np.sum(rayons))

#gradient_descent(energie, np.ones((2, 1)), 2)
plt.figure(1)
plt.plot(T, y)
plt.figure(2)
plt.plot(T, rayons)
#plotting(energie, np.ones((1,1)))
plt.legend()
plt.show()