class Case:

    """
    Création de la classe case composé de ses coordonéées ligne, colonne et de sa valeur
    """

    def __init__(self, position_ligne: int, position_colonne:int, valeur:int) -> None: # affectation des attributs de la classe Case
        self.position_ligne = position_ligne
        self.position_colonne = position_colonne
        self.valeur = valeur

    def getPositionCase(self) -> tuple: # renvoie un tuple composé de la position 
        return (self.position_colonne, self.position_ligne)
    
    def setValeur(self, nouvelle_valeur:int) -> None: # affectation d'une nouvelle valeur
        if self.valeur != None:
            print("vous ne pouvez pas modifier la valeur initiale") # vérification de l'existence d'une valeur sur une case
        else:
            self.valeur = nouvelle_valeur 

    def setPositionLigne(self, nouvelle_position_ligne: int) -> None: # modification de la position de la ligne de la case
        self.position_ligne = nouvelle_position_ligne

    def setPositionColonne(self, nouvelle_position_colonne:int) -> None: # modification de la position de la colonne de la case
        self.position_colonne = nouvelle_position_colonne
    
    #savoir quelles sont les cases qui sont autour 