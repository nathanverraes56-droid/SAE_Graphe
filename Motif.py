from Case import *

class Motif:
    """Un motif est une liste de cases ayant une taille (un nombre de cases)
    """
    
    def __init__(self, liste_cases : list[Case]) -> None:
        self.taille : int = len(liste_cases)
        self.liste_cases : list[Case] = liste_cases
        
    def getTaille(self) -> int:
        return(self.taille)
    
    def getListeCases(self) -> list[Case]:
        return(self.liste_cases)
    
    
            