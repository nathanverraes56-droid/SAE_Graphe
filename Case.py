class Case:
    """
    Création de la classe case composée de ses coordonnées
    de sa valeur et de son statut (fixe ou jouable)
    """

    def __init__(self, position_ligne: int, position_colonne: int, valeur: int | None = None, est_fixe: bool = False) -> None: 
        self.position_ligne = position_ligne
        self.position_colonne = position_colonne
        self.valeur = valeur
        # permet de Savoir si un nombre etait deja la a la base
        self.est_fixe = est_fixe 

    def getPositionCase(self) -> tuple[int, int]: 
        """Renvoie un tuple composé de la position"""
        return (self.position_colonne, self.position_ligne) 

    def setPositionLigne(self, nouvelle_position_ligne: int) -> None: 
        self.position_ligne = nouvelle_position_ligne

    def setPositionColonne(self, nouvelle_position_colonne: int) -> None:
        self.position_colonne = nouvelle_position_colonne
    
    def set_valeur(self, nouvelle_valeur: int | None) -> None:
        if not self.est_fixe:
            self.valeur = nouvelle_valeur

    def estVide(self) -> bool:
        return self.valeur is None or self.valeur == 0
    
    def estVoisin(self) -> list[tuple[int, int]]:
        """Génère et renvoie les coordonnées valides des 8 voisins autour de la case."""
        voisins_valides = []
        l = self.position_ligne
        c = self.position_colonne
        
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for decalage_l, decalage_c in directions:
            nouvelle_ligne = l + decalage_l
            nouvelle_colonne = c + decalage_c
            
            # On vérifie que la coordonnée ne sort pas de la grille par le haut ou la gauche
            if nouvelle_ligne >= 0 and nouvelle_colonne >= 0:
                voisins_valides.append((nouvelle_ligne, nouvelle_colonne))
                
        return voisins_valides