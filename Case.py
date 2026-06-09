class Case:

    """
    Création de la classe case
    """

    def __init__(self, position_ligne: int, position_colonne:int, valeur:int) -> None:
        self.position_ligne = position_ligne
        self.position_colonne = position_colonne
        self.valeur = valeur

    def getPositionCase(self) -> tuple:
        return (self.position_colonne, self.position_ligne)
    
    def setValeur(self, nouvelle_valeur) -> int:
        self.valeur = nouvelle_valeur

    def setPositionLigne(self, nouvelle_position_ligne) -> None:
        self.position_ligne = nouvelle_position_ligne

    def setPositionColonne(self, nouvelle_position_colonne) -> None:
        self.position_colonne = nouvelle_position_colonne
    