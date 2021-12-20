import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# ======= CONSTANTES ==========

n = 10*10**(-3)  # Quantité de matière en mol
rs = 1.5/2.5  # Résistance du fil en ohm
r_th = 16 # Résistance thermique
C = 0.8  # Capacité thermique (en J/K)
R = 8.314  # constante des gazs parfaits
I = 2.5  # Intensité (en A)
T_ext = 293  # Température exterieure (en K)
r_ini = 0.001   # Rayon initiale de la bulle (en m)
P_ext = 10**5  # Pression extérieure (en Pa)
m_young = (10**-3)/(4*32)  # Module de Young (N/m) https://www.editions-ellipses.fr/PDF/9782340005549_extrait.pdf http://fltsi.fr/tsi/tsi2/Cours%20et%20TD%20par%20Domaines%20de%20Competence_TSI2/DC25_Solides%20deformables_RDM/PARTIE%201%20Introduction%20RdM/Valeurs%20num%C3%A9riques%20de%20modules%20de%20Young.pdf
M = 46.1  # Masse molaire de l'ethanol (g.mol-1)
L_v = 843 # Enthalpie de vaporisation (J.g-1)
T0 = 351.6 #température de vaporisation (K)
rho = 789*10**3 #masse volumique (g.mol-1)
R0 = 0.5 * (10**-3) #taille initiale de la bulle (m)
G = 10**-3  #module de cisaillement



def newton(f, df, ini, epsilon, T):
    x = ini
    while abs(f(x, T)) > epsilon:
        if df(x, T) != 0 :
            x -= f(x, T) / (df(x, T))

        else :
            x -= f(x, T) / (df(x, T) - epsilon)
    if x>0.0001 :
        return x
    else : 
        return newton(f, df, ini+0.1, epsilon, T)

p_liste=[]
def f(x, T):
    #p_sat = (10**5)*np.exp(M*L_v*((1/T0)-(1/T))/R)  #formule de Dupré simplifié
    p_sat = (10**5)*10**(5.24677-1598.673/(T-46.424))  #formule d'Antoine
    p_liste.append(p_sat)
    n_v = p_sat*(4/3)*np.pi*(x**3)/(R*T)
    V = 4/3*np.pi*x**3
    if n_v<n :
        return x*n_v*R*T - (V - (n-n_v)*M/rho)*(x*P_ext - 4/3*G*x + 2*m_young)  #chgmt d'etat
    else :
        return -P_ext*(x**3) - 2*m_young*(x**2) + 3*n*R*T/(4*np.pi)  #gaz parfait




def df(x, T):
    h=10**-9
    return (f(x+h, T)-f(x, T))/h


def temperature(t):
    ''' Retourne la température en fonction du temps'''
    return T_ext + rs * r_th * (I ** 2) * (1 - np.exp(-t*C / r_th))


def get_radius_list(t):
    ''' Retourne la liste des rayons de la bulle au cours du temps'''
    epsilon=10**(-9)
    r_list = [newton(f, df, 0.1, epsilon, T_ext)]
    temp=293
    for i in t[1:]:
        p_sat = (10**5)*10**(5.24677-1598.673/(temp-46.424)) #formule d'Antoine
        n_v = p_sat*(4/3)*np.pi*(r_list[-1]**3)/(R*temp)
        temp = temperature(i)
        r_list.append(newton(f, df, r_list[-1], epsilon, temp))

    return r_list

if __name__=="__main__" :
    lin = np.linspace(0, 300, 10000)
    radius_list=[]
    plt.figure(1)
    for i in range(1) :
        
        plt.plot(lin, get_radius_list(lin), label=str(I)+"A")

    plt.legend()
    plt.figure(2)
    for i in range(1) :
        
        plt.plot(lin, temperature(lin), label=str(I)+"A")
    plt.legend()

    plt.grid()
    plt.show()