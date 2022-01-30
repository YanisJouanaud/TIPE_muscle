import numpy as np

def translate(Vect, translation) :
    """ translate le Vect par translation """
    #Vect et translation doivent être des vecteurs (lignes) de même dimension que l'espace
    #non-broadcastable, faut itérer
    n = len(translation)
    m = np.eye(n+1)
    m[:, -1][:-1] = translation
    v = np.dot(Vect,np.concatenate(np.eye(n), np.zeros((3,1)), axis=1)) + np.array([0]*n+[1])
    return np.dot(m, v.T)[:-1]

def scaling(Vect, scale) :
    """ 'gonfle' le Vect d'une echelle scale """
    #Vect et scale doivent être des vecteurs (lignes) de même dimension que l'espace
    #non-broadcastable, faut itérer
    S = np.diag(scale)
    return np.dot(S, Vect)




class Fil :
    """ Fil traversant le miscle dans lequel il est créé """
    active = 0 #etat d'activation
    def __init__(self, forme, resistance):
        self.forme = forme
        self.res = resistance
    
    def diffusion(self, pos, t) :  #retourne
        pass


class Bulle:
    """ bulle d'ethanol composant le muscle """
    active=0
    def __init__(self, pos, taille, mod_young):
        self.pos = pos
        self.rad = taille
        self.m_young = mod_young
        self.x = 1  #fraction molaire de liquide dans la bulle
    
    def fraction(self, temp) :  #retourne
        pass

    def taille(self, temp) :  #update
        pass

class Muscle:
    """ muscle constitué de bulles et traversé par un fil """
    active = 0
    mod_young = 0.001
    r_th = 3
    r_bulle = 0.0002

    def __init__(self, taille, densite):
        self.sizes = taille
        self.nb_bulles = densite * np.prod(taille)
        self.forme = []
        self.maille = None
        n = len(taille)
        for i in range(n) :
            self.form.append(int((self.nb_bulles*(self.sizes[i]**2)/np.delete(self.sizes, i))**(1/n)))
        self.forme = tuple(self.forme)
        self.nb_bulles = np.prod(self.forme)
        self.fil=Fil("helicoidale", 5)
        

    def generate(self, pos):  #update et retourne
        maille = [Bulle(pos, self.r_bulle, self.mod_young)]
        I = np.identity(len(self.forme))
        for i in range(len(self.forme)) :
            for n in range(self.forme[i]) :
                maille += [Bulle(maille[0].pos + n*I[i]/self.sizes[i]*np.ones(len(maille[0])), self.r_bulle, self.mod_young)]
            maille = [maille]
        self.maille = np.array(maille[0])
        return np.array(maille[0])


    def gonflement(self, t) :
        temps = self.fil.diffusion(self.maille, t)
        for i in range(self.nb_bulles) :
            self.maille.flat[i].taille(temps.flat[i])
            #l = soft body sim



