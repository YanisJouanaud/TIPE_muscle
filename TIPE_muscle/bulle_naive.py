import numpy as np
import matplotlib.pyplot as plt


# ======= CONSTANTES ==========

n = 5*10**(-3)  # Quantité de matière en mol
rs = 1  # Résistance du fil en ohm
r_th = 90  # Résistance thermique
C = 2092*0.1  # Capacité thermique (en J/K)
R = 8.314  # constante des gazs parfaits
I = 1  # Intensité (en A)
T_ext = 293  # Température exterieure (en K)
r_ini = 0.001   # Rayon initiale de la bulle (en m)
P_ext = 10**5  # Pression extèrieure (en bar)
m_young = 0.5*10**6  # Module de Young (N/m)
M = 46.1  # Masse molaire de l'ethanol (g.mol-1)
L_v = 843 # Enthalpie de vaporisation (J.g-1)
T0 = 351.6 #température de vaporisation (K)
rho = 789*10**3 #masse volumique (g.mol-1)

def newton(f, df, ini, epsilon, T):
    x = ini
    while abs(f(x, T)) > epsilon:
        if df(x, T) != 0 :
            x -= f(x, T) / (df(x, T))

        else :
            x -= f(x, T) / (df(x, T) - epsilon)

    return x


def f(x, T):
    p_sat = 10**5*10**(M/R*L_v*(1/T0-1/T))  #formule de Dupré simplifié
    n_v = p_sat*4/3*np.pi*x**3/(R*T)
    if n_v<n :
        return n_v*R*T*x - 2* m_young*(4/3 * np.pi * x**3 - (n - n_v)*M / rho)  #chgmt d'etat
    else :
        return -P_ext*(x**3) - 2*m_young*(x**2) + 3*n*R*T/(4*np.pi)  #gaz parfait


def df(x, T):
    p_sat = 10**5*10**(M/R*L_v*(1/T0-1/T))  #formule de Dupré simplifié
    n_v = p_sat*4/3*np.pi*x**3/(R*T)
    if n_v<n :
        return p_sat*16/3*np.pi*x**3 - 2*m_young*(4*np.pi*x**2+p_sat*4*np.pi*M*x**2/(rho*R*T))
    else :
        return -3*P_ext*x**2 - 4*m_young*x


def temperature(t):
    ''' Retourne la température en fonction du temps'''
    return T_ext + rs * r_th * (I ** 2) * (1 - np.exp(-t*C / r_th))


def get_radius_list(t):
    ''' Retourne la liste des rayons de la bulle au cours du temps'''
    epsilon=10**(-6)
    r_list = [newton(f, df, 0, epsilon, T_ext)]

    for i in t[1:]:
        temp = temperature(i)
        r_list.append(newton(f, df, r_list[-1], epsilon, temp))

    return r_list


lin = np.linspace(0, 10, 1000)
radius_list = get_radius_list(lin)

plt.plot(lin, radius_list)
plt.show()
