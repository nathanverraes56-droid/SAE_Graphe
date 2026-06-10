from Motif import *
class Grille:

    """
    Création de la classe Grille composé de sa taille un d'un 
    dictionnaire pour lequel sa clé est le nom du motif et sa valeur 
    est de la classe motif
    """

    def __init__(self, taille: int, liste:list):
        self.taille = taille
        self.liste = []
    

    def ajoutMotif(self, motif: Motif) -> None: # implémentation des motifs à la grille
        self.liste.append(motif)


    def listeCaseNonVide(self) -> list[Motif]:
        liste_composant_grille = []
        for i in range(self.taille):
            if self.liste[i][2] > 0:
                liste_composant_grille.append(self.liste[i][2])
        return liste_composant_grille


    def setValeurCase(self, nouv_valeur: int) -> None:
        if self.valeur in self.liste_case_non_vide():
            print("vous ne pouvez pas modifier la valeur initiale") # vérification de l'existence d'une valeur sur une case
        else:
            self.valeur = nouv_valeur 