from Motif import *
class Grille:

    def __init__(self, taille, dictionnaire: dict):
        self.taille = taille
        self.dictionnaire = {}
    

    def ajout_motif(self, motif: Motif, nom_motif: str):
        self.dictionnaire[nom_motif] = motif