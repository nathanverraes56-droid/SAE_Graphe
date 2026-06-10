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

    def setPositionLigne(self, nouvelle_position_ligne: int) -> None: # modification de la position de la ligne de la case
        self.position_ligne = nouvelle_position_ligne

    def setPositionColonne(self, nouvelle_position_colonne:int) -> None: # modification de la position de la colonne de la case
        self.position_colonne = nouvelle_position_colonne
    
    def estVide(self) -> bool:
        return self.valeur == 0
    
    def estVoisin(self) -> list:
        """
        Met dans une liste les coordonées des voisins de la case :
        (ligne-1, colonne-1), (ligne-1, colonne), (ligne-1, colonne+1)
        (ligne, colonne-1), (ligne, colonne+1)
        (ligne+1, colonne-1), (ligne+1, colonne), (ligne+1, colonne+1)
        """
        liste_voisin: list[tuple] =[]
        liste_voisin = [(self.position[0]-1, self.position[1]-1), (self.position[0]-1, self.position[1]), (self.position[0]-1, self.position[1]+1),
         (self.position[0], self.position[1]-1), (self.position[0], self.position[1]+1), 
         (self.position[0]+1, self.position[1]-1), (self.position[0]+1, self.position[1]), (self.position[0]+1, self.position[1]+1)]
        for i in range(len(liste_voisin)):
            if liste_voisin[i][0] < 0:
                liste_voisin[i][0].pop() # retire si la position de la ligne est négative
            elif liste_voisin[i][1] < 0:
                liste_voisin[i][1].pop() # retire si la position de la colonne est négative
        return liste_voisin 
     