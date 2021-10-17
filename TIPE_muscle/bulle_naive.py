import numpy as np
#import matplotlib.pyplot as plt
from animate_bulle import anim_expansion
#On considère ici une bulle constituée d'un gaz parfait dans un solide elastique
#  chauffée à même la résistance et dont la perte calorifique suit la loi de
#  refroidissement de Newton.



def rtoV(r):
    return 4/3*np.pi*r**3

def init():
    return {"n":5*(10**-3),"Rs":1,"Rth":90,"I":1,"C":2092*0.1,"Text":293,"r_ini":0.001,"P_ext":10**5,"Mod_Young":0.5*10**6}

def f(x,T):
    dic=init()
    return -dic["P_ext"]*x**3-2*dic["Mod_Young"]*x**2+3*dic["n"]*8.314*T/(4*np.pi)

def Df(x) :
    dic=init()
    return -3*dic["P_ext"]*x**2-4*dic["Mod_Young"]*x

def temperature(t) :
    dic=init()
    Rs,Rth,I,C,Text = dic["Rs"],dic["Rth"],dic["I"],dic["C"],dic["Text"]
    return (Rs * Rth * (I ** 2) * (1 - np.exp(-(1 / Rth * C) * t)) + Text)
    
def radius(P, r):
    dic=init()
    n,Pext, Mod_Young = dic["n"], dic["P_ext"], dic["Mod_Young"]
    T=P*(4/3)*np.pi*r**3/(8.314*n)
    while abs(P-Pext)>2*Mod_Young/r :
        r+=0.00001
        P=n*R*T/((4/3)*np.pi*r**3)
    return r

def newton(f, df, T, ini, epsilon) : #prend un parametre T en plus des parametres usuels
    x=ini
    while abs(f(x, T))>epsilon :
        if df(x)!=0 :
            x=x-f(x,T)/(df(x))
        else :
            x=x-f(x,T)/(df(x)-10**(-6))
    return x

def expansion(t): #t doit ici être un linspace
    dic=init()
    epsilon=10**(-6)
    r=[newton(f, Df, dic["Text"], 0, epsilon)]
    for i in t:
        temp=temperature(i)
        r.append(newton(f, Df, temp, r[-1], epsilon))
        print(temp)
    return r

def get_radius_expansion(t):
    if type(t) == int or type(t) == float :
        T=np.linspace(0,t,100000)
        return expansion(T)[-1]
    else :
        return expansion(t)

print(expansion(np.linspace(0,10,1000)))
anim_expansion(get_radius_expansion)
