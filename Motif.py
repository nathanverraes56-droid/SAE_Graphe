from Case import Case

class Motif:
    """Un motif est une liste de cases ayant une taille (un nombre de cases)"""
    
    def __init__(self, liste_cases: list[Case]) -> None:
        self.taille: int = len(liste_cases)
        self.liste_cases: list[Case] = liste_cases
        
    def getTaille(self) -> int:
        return self.taille
    
    def getListeCases(self) -> list[Case]:
        return self.liste_cases
    
    def estValide(self) -> bool:
        """
        Vérifie qu'il n'y a aucun doublon dans le motif et que 
        les valeurs saisies sont bien comprises entre 1 et N .
        """
        valeurs_trouvees = []
        
        for case in self.liste_cases:
            if not case.estVide():
                valeur = case.valeur
                
                # Verifie qu'il n'y a pas de doublon
                if valeur in valeurs_trouvees:
                    return False
                
                # Verifie que la valeur n'est pas superieure a la taille du motif
                if valeur > self.taille or valeur < 1:
                    return False
                    
                valeurs_trouvees.append(valeur)
                
        return True