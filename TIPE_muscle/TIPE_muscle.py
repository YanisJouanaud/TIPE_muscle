import numpy as np
from  copy import deepcopy
import matplotlib.pyplot as plt
from bulle_debug import f, df, newton
from repartition_3d import chaleur
from soft_body1D import long
from tqdm import tqdm
from memory_profiler import profile

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
        #pos = array_attrib(maille, "pos")
        return chaleur(maille, t)



class Bulle:
    """ bulle d'ethanol composant le muscle """
    active = 0
    epsilon = 10**(-12)
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
        self.rad = newton(f, df, 0.1, self.epsilon, temp, self.m_young)

class Muscle:
    """ muscle constitué de bulles et traversé par un fil """
    active = 0
    mod_young = (10**-3)/(4*32)
    r_th = 70
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
        self.fil = Fil("helicoidale", 5)
    
    @property
    def vol(self) :
        return np.prod(self.sizes)

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
        self.sizes = (abs(self.maille[0][0][-1].pos[2] - self.maille[0][0][0].pos[2]),
                    abs(self.maille[0][-1][0].pos[1] - self.maille[0][0][0].pos[1]),
                    abs(self.maille[-1][0][0].pos[0] - self.maille[0][0][0].pos[0]))
 
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
        maille_pos = array_attrib(self.maille, "pos")
        tempers = self.fil.diffusion(maille_pos, t)
        for i in range(self.nb_bulles) :
            self.maille.flat[i].taille(tempers.flat[i])
        k, K = self.mod_young*10, 1000*0.02*0.02*self.mod_young/0.06  #random parce que j'ai la flemme
        l0 , L0 = 0.005*np.array(self.sizes), 0.02*np.sum(np.array(self.sizes)[0])  #pareil
        l = long(array_attrib(self.maille, "rad"), k, K, l0, L0, np.array(self.forme), 0.95)
        self.placement(l)


def main() :
    muscle1 = Muscle((1,1,1), 30)
    muscle1.generate((0,0,0))
    print(muscle1.vol)
    y = []
    t = np.linspace(0,500,5000)
    for i in tqdm(t) :
        muscle1.gonflement(i)
        a = np.empty(1, dtype=object)
        a[0] = tuple(muscle1.maille[0][0][0].pos)
        y.append(muscle1.vol)
    return t,y

if __name__=='__main__' :
    t,y=main()
    plt.plot(t,y)
    plt.show()