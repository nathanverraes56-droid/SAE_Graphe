class Motif:
    """Un motif est une liste de cases ayant une taille (un nombre de cases)
    """
    
    def __init__(self, liste_cases) -> None:
        self.taille : int = len(liste_cases)
        self.liste_cases : list = liste_cases
        
    def getTaille(self) -> int:
        return(self.taille)
    
    def getListeCases(self):
        return(self.liste_cases)
            