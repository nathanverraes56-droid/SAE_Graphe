import json
from Case import Case
from Motif import Motif

class Grille:
    """
    Représente la grille globale du jeu Néonaure.
    Elle est composée d'une taille, d'une liste de Motifs et d'un dictionnaire
    permettant d'accéder instantanément à une case par ses coordonnées (ligne, colonne).
    """

    def __init__(self, taille: int = 8):
        self.taille: int = taille
        self.motifs: list[Motif] = []
        self.dictionnaire_cases: dict[tuple[int, int], Case] = {}

    def ajout_motif(self, motif: Motif) -> None: 
        """Ajoute un motif à la grille."""
        self.motifs.append(motif)

    def liste_valeurs_initiales(self) -> list[int]:
        """
        Retourne la liste de tous les chiffres fixes/indices de départ 
        présents sur la grille.
        """
        valeurs_initiales = []
        for case in self.dictionnaire_cases.values():
            if case.est_fixe and case.valeur is not None:
                valeurs_initiales.append(case.valeur)
        return valeurs_initiales

    def verifier_voisins(self, ligne: int, colonne: int) -> bool:
        """
        Vérifie si le chiffre de la case est bien entouré 
        de chiffres différents.
        """
        case_cible = self.dictionnaire_cases.get((ligne, colonne))
        if case_cible is None or case_cible.valeur is None:
            return True # Pas de chiffre, pas de conflit
        
        valeur_cible = case_cible.valeur

        # Les 8 positions autour de la case
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

        for dl, dc in directions:
            voisin = self.dictionnaire_cases.get((ligne + dl, colonne + dc))
            if voisin and voisin.valeur == valeur_cible:
                return False 

        return True

    def charger_grille_json(self, chemin_fichier: str) -> None:
        """
        Lit le fichier JSON pour créer les objets Case et Motif de la grille.
        """
        # On réinitialise les données pour éviter de cumuler les grilles
        self.motifs = []
        self.dictionnaire_cases = {}

        with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
            donnees = json.load(fichier)

        for nom_motif, liste_cases_json in donnees.items():
            cases_du_motif = []

            for donnee_case in liste_cases_json:
                ligne = donnee_case[0]
                colonne = donnee_case[1]
                valeur_brute = donnee_case[2]

                # Préparation pour la classe Case
                valeur = None if valeur_brute == 0 else valeur_brute
                est_fixe = valeur_brute > 0

                # Création de l'objet Case avec ses 4 paramètres requis
                nouvelle_case = Case(
                    position_ligne=ligne, 
                    position_colonne=colonne, 
                    valeur=valeur, 
                    est_fixe=est_fixe
                )
                
                cases_du_motif.append(nouvelle_case)
                self.dictionnaire_cases[(ligne, colonne)] = nouvelle_case

            nouveau_motif = Motif(cases_du_motif)
            self.ajout_motif(nouveau_motif)