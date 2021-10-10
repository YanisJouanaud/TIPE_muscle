class fil :
    #fil traversant le muscle
    active = 0 #etat d'activation
    def __init__(self, longueur, resistance):
        self.L=longueur
        self.res=resistance

class muscle:
    #muscle consitué de bulles et traversé par un fil
    active = 0
    def __init__(self, taille, bulles, tension, resthermique):
        self.size = taille
        self.bubbles = bulles
        self.exp = tension
        self.rth = resthermique

    def generate(self, distribution):
        pass


class bulle:
    active=0
    def __init__(self, taille, gaz):
        self.rad = taille
        self.gaz = gaz