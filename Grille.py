import json
from Case import Case
from Motif import Motif

class Grille:
    """
    Une grille composée d'une taille, d'une liste de Motifs et d'un dictionnaire
    permettant d'accéder instantanément à une case par ses coordonnées.
    """

    def __init__(self, taille: int = 8):
        self.taille: int = taille
        self.motifs: list[Motif] = []
        self.dictionnaire_cases: dict[tuple[int, int], Case] = {}

    def ajout_motif(self, motif: Motif) -> None: 
        """Ajout d'un motif à la grille."""
        self.motifs.append(motif)

    def verifier_voisins(self, ligne: int, colonne: int) -> bool:
        """
        Vérifie si le chiffre de la case (ligne, colonne) est entouré 
        de chiffres différents.
        """
        case_cible = self.dictionnaire_cases.get((ligne, colonne))
        if case_cible is None or case_cible.valeur is None:
            return True # Pas de chiffre, pas de conflit
        
        valeur_cible = case_cible.valeur

        # 8 positions autour de la case
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
        Lecture du fichier JSON pour créer les objets Case et Motif de la grille.
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

                # si valeur_brute est égale 0 c'est une case vide (None)
                if valeur_brute == 0:
                    valeur = None
                else:
                    valeur = valeur_brute
                
                # si la liste contient 4 éléments c'est une sauvegarde on lit l'état est_fixe sinon c'est un fichier d'origine on déduit que c'est fixe si la valeur > 0
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

            # on crée le motif avec ses cases et on l'ajoute à la grille
            nouveau_motif = Motif(cases_du_motif)
            self.ajout_motif(nouveau_motif)

    def resoudre_backtracking(self) -> bool:
        """
        Résout la grille automatiquement.
        Retourne True si une solution a été trouvée, False sinon.
        """
        # On cherche la première case vide 
        case_vide = None
        for case in self.dictionnaire_cases.values():
            if case.valeur is None:
                case_vide = case
                break

        # S'il n'y a plus de case vide, la grille est résolue 
        if case_vide is None:
            return True

        l = case_vide.position_ligne
        c = case_vide.position_colonne

        # On trouve le motif de cette case pour connaître sa taille maximum N
        motif_associe = None
        for m in self.motifs:
            if case_vide in m.liste_cases:
                motif_associe = m
                break

        taille_max = motif_associe.getTaille()

        # On teste toutes les valeurs possibles de 1 à N
        for v in range(1, taille_max + 1):
            case_vide.valeur = v  # On tente de poser le chiffre

            # On vérifie si ce chiffre respecte les voisins et les contraintes du motif
            if self.verifier_voisins(l, c) and motif_associe.estValide():
                # Si c'est bon, on demande de résoudre la case vide suivante
                if self.resoudre_backtracking():
                    return True  # La solution s'est propagée jusqu'au bout !

            # Si pas de solution possible pour l'instant on passe au chiffre suivant
            case_vide.valeur = None

        # Si aucun chiffre de 1 à N ne fonctionne, cette branche est une impasse
        return False