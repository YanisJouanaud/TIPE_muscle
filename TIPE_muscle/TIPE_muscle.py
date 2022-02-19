import numpy as np
from  copy import deepcopy
from bulle_debug import f, df, newton
from repartition_3d import chaleur
from soft_body1D import long

def array_attrib(maille, nom_attrib) :
    attrib = np.zeros_like(maille)
    for i in range(np.size(attrib)) :
        attrib.flat[i] = getattr(maille.flat[i], nom_attrib)
    return attrib

class Fil :
    """ Fil traversant le miscle dans lequel il est créé """
    active = 0 #etat d'activation
    def __init__(self, forme, resistance):
        self.forme = forme
        self.res = resistance
    
    def diffusion(self, maille, t) :  #retourne
        pos = array_attrib(maille, "pos")
        return chaleur(pos, t)



class Bulle:
    """ bulle d'ethanol composant le muscle """
    active=0
    def __init__(self, pos, taille, mod_young):
        self.pos = pos
        self.rad = taille
        self.m_young = mod_young
        self.x = 1  #fraction molaire de liquide dans la bulle
        self.n0 = (10**5+2*self.m_young/self.rad)*4/3*np.pi*self.rad**3/(8.314*20)  #gaz parfaits sortof
    
    def fraction(self, temp) :  #retourne
        p_sat = (10**5)*10**(5.24677-1598.673/(temp-46.424)) #formule d'Antoine
        n_v = p_sat*(4/3)*np.pi*(self.rad**3)/(8.314*temp)
        return n_v/self.n0

    def taille(self, temp) :  #update
        self.rad = newton(f, df, 0.01, epsilon, temp, m_young)

class Muscle:
    """ muscle constitué de bulles et traversé par un fil """
    active = 0
    mod_young = 8 * 10**(-6)
    r_th = 3
    r_bulle = 0.0002

    def __init__(self, taille, densite):
        self.sizes = taille
        self.nb_bulles = densite * np.prod(taille)
        self.forme = []
        self.maille = None
        n = len(taille)
        for i in range(n) :
            self.forme.append(int((self.nb_bulles*(self.sizes[i]**2)/np.prod(np.delete(self.sizes, i)))**(1/n)))
        self.forme = tuple(self.forme)
        self.nb_bulles = np.prod(self.forme)
        self.fil=Fil("helicoidale", 5)
        
    def placement(self, l) :
        t = np.indices(self.maille.shape, sparse = True)
        I, J, K = tuple([t[i] if i<len(t) else [0] for i in range(3)])
        for i in I.flatten() :
            for j in J.flatten() :
                for k in np.array(K).flatten() :
                    if i != 0 :
                        Lx = l[0] + self.maille[i][j][k].rad + self.maille[i-1][j][k].rad
                        self.maille[i][j][k].pos = tuple(np.array(self.maille[i-1][j][k].pos) + np.array([Lx, 0, 0]))
                    if j != 0 :
                        Ly = l[1] + self.maille[i][j][k].rad + self.maille[i][j-1][k].rad
                        self.maille[i][j][k].pos = tuple(np.array(self.maille[i][j-1][k].pos) + np.array([0, Ly, 0]))
                    if k != 0 :
                        Lz = l[2] + self.maille[i][j][k].rad + self.maille[i][j][k-1].rad
                        self.maille[i][j][k].pos = tuple(np.array(self.maille[i][j][k-1].pos) + np.array([0, 0, Lz]))
                    


    def generate(self, pos):  #update et retourne
        maille = [Bulle(pos, self.r_bulle, self.mod_young)]
        for i in range(len(self.forme)) :
            for n in range(self.forme[i]) :
                maille += [deepcopy(maille[0])]
            maille = [maille]
        self.maille = np.array(maille[0])
        self.l0 = -2*self.r_bulle + np.array(self.sizes)/np.array(self.forme)
        self.placement(self.l0)
        return np.array(maille[0])

    
    def gonflement(self, t) :
        temps = self.fil.diffusion(self.maille, t)
        for i in range(self.nb_bulles) :
            self.maille.flat[i].taille(temps.flat[i])
        k, K = m_young*10, 1000*0.02*0.02*m_young/0.06  #random parce que j'ai la flemme
        l0 , L0 = 0.005*np.array(self.sizes), 0.02*self.sizes  #pareil
        l = long(array_attrib(self.maille, "rad"), k, K, l0, L0, np.array(self.forme))
        self.placemement(l)

muscle1 = Muscle((1,1,1), 30)
muscle1.generate((0,0,0))
print(muscle1.maille.shape, muscle1.forme, muscle1.sizes, "\n", array_attrib(muscle1.maille, "pos"))