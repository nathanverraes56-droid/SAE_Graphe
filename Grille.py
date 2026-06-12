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

    def verifier_voisins(self, ligne: int, colonne: int) -> bool:
        """
        Vérifie si le chiffre de la case (ligne, colonne) est bien entouré 
        de chiffres différents (y compris en diagonale).
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
                return False # Doublon détecté chez un voisin !

        return True

    def charger_grille_json(self, chemin_fichier: str) -> None:
        """
        Lit le fichier JSON pour créer les objets Case et Motif de la grille.
        Accepte le format classique (3 valeurs) et le format de sauvegarde (4 valeurs).
        """
        # On vide la grille actuelle avant d'en charger une nouvelle
        self.motifs = []
        self.dictionnaire_cases = {}

        with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
            donnees = json.load(fichier)

        for nom_motif, liste_cases_json in donnees.items():
            cases_du_motif = []

            for donnee_case in liste_cases_json:
                colonne = donnee_case[0]
                ligne = donnee_case[1]
                valeur_brute = donnee_case[2]

                # Si la valeur est 0, c'est une case vide (None dans notre modèle)
                valeur = None if valeur_brute == 0 else valeur_brute
                
                # 💡 L'astuce de compatibilité :
                # Si la liste contient 4 éléments, c'est une sauvegarde, on lit l'état "est_fixe".
                # Sinon, c'est un fichier d'origine, on déduit que c'est fixe si la valeur > 0.
                if len(donnee_case) >= 4:
                    est_fixe = donnee_case[3]
                else:
                    est_fixe = valeur_brute > 0

                nouvelle_case = Case(
                    position_ligne=ligne, 
                    position_colonne=colonne, 
                    valeur=valeur, 
                    est_fixe=est_fixe
                )
                
                cases_du_motif.append(nouvelle_case)
                self.dictionnaire_cases[(ligne, colonne)] = nouvelle_case

            # On crée le motif avec ses cases et on l'ajoute à la grille
            nouveau_motif = Motif(cases_du_motif)
            self.ajout_motif(nouveau_motif)