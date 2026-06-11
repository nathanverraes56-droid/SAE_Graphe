from Case import *

class Motif:
    """Un motif est une liste de cases ayant une taille (un nombre de cases)
    """
    
    def __init__(self, liste_cases : list[Case]) -> None:
        self.taille : int = len(liste_cases)
        self.liste_cases : list[Case] = liste_cases
        
    def getTaille(self) -> int:
        return self.taille
    
    def getListeCases(self) -> list[Case]:
        return self.liste_cases
    
    def valeurExiste(self, valeur: int) -> bool:
        """
        Vérifie si la valeur mise en paramètre existe déjà dans le motif
        """
        for i in range(self.getTaille()):
            if valeur in self.liste_cases[i][2]:
                return True
        return False
    
    def estValide(self) -> bool:
        """
        Vérifie si les valeurs des cases qui sont de 1 à N et si il existe deja une valeur identique dans le même motif
        """
        for i in range(self.getTaille()):
            if self.valeurExiste(self.liste_cases[i][2]):
                return False
        return True
    
        