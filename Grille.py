from Motif import *
class Grille:

    """
    Création de la classe Grille composé de sa taille un d'un 
    dictionnaire pour lequel sa clé est le nom du motif et sa valeur 
    est de la classe motif
    """

    def __init__(self, taille, dico: dict):
        self.taille = taille
        self.dico = {}
    

    def ajout_motif(self, motif: Motif, nom_motif: str) -> None: # implémentation des motifs à la grille
        self.dictionnaire[nom_motif] = motif