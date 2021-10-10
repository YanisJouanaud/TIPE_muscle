import numpy as np
import matplotlib.pyplot as plt
from animate_bulle import anim_expansion
#On considère ici une bulle constituée d'un gaz parfait dans un solide elastique
#  chauffée à même la résistance et dont la perte calorifique suit la loi de
#  refroidissement de Newton.


def rtoV(r):
    return 4/3*np.pi*r**3

def init():
    return {"n":1.6*(10**-7),"Rs":0.5,"Rth":6.25,"I":1,"C":2092*0.04,"Text":300,"r_ini":0.001,"P_ext":10**5,"Mod_Young":0.5*10**6}

def pression(t, V) :
    dic=init()
    n,Rs,Rth,I,C,Text = dic["n"], dic["Rs"],dic["Rth"],dic["I"],dic["C"],dic["Text"]
    return n * 8.314 * (Rs * Rth * (I ** 2) * (1 - np.exp(-(1 / Rth * C) * t)) + Text) / V

def radius(P, r):
    dic=init()
    n,Pext, Mod_Young = dic["n"], dic["P_ext"], dic["Mod_Young"]
    T=P*(4/3)*np.pi*r**3/(8.314*n)
    while abs(P-Pext)>2*Mod_Young/r :
        r+=0.00001
        P=n*R*T/((4/3)*np.pi*r**3)
    return r

def expansion(t): #t doit ici être un linspace
    r=[init()["r_ini"]]
    for i in t:
        r.append(radius(pression(i, rtoV(r[-1])), r[-1]))
        print(pression(i, rtoV(r[-1])), "Pascals")
    return r

def get_radius_expansion(t):
    if type(t) == int or type(t) == float :
        T=np.linspace(0,t,100000)
        return expansion(T)[-1]
    else :
        return expansion(t)

print(expansion(np.linspace(0,100,100000)))
#anim_expansion(get_radius_expansion)