import json
from Motif import *
class Grille:

    """
    Création de la classe Grille composé de sa taille un d'un 
    dictionnaire pour lequel sa clé est le nom du motif et sa valeur 
    est de la classe motif
    """

    def __init__(self, taille: int):
        self.taille = taille
        self.liste = []
    

    def ajoutMotif(self, motif: Motif) -> None: 
        """
        Ajoute un motif à la grille précisé en parametre
        """
        self.liste.append(motif)


    def listeCaseNonVide(self) -> list[Motif]:
        """
        Fait une liste à partir des cases non vide
        """
        liste_composant_grille = []
        for i in range(self.taille):
            if self.liste[i][2] > 0:
                liste_composant_grille.append(self.liste[i][2])
        return liste_composant_grille


    def setValeurCase(self, nouv_valeur: int) -> None:
        """
        Modifie la valeur de la case si elle ne fait pas partie des valeurs d'origine
        """
        if self.valeur in self.liste_case_non_vide():
            print("vous ne pouvez pas modifier la valeur initiale") # vérification de l'existence d'une valeur sur une case
        else:
            self.valeur = nouv_valeur 

    def charger_grille_json(self, chemin_fichier: str) -> None:
        """
        Lit le fichier JSON pour créer une grille.
        """
        with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
            donnees = json.load(fichier)

        for nom_motif, liste_cases_json in donnees.items():
            cases_du_motif = []

            for donnee_case in liste_cases_json:
                ligne = donnee_case[0]
                colonne = donnee_case[1]
                valeur_brute = donnee_case[2]

                valeur = None if valeur_brute == 0 else valeur_brute
                est_fixe = valeur_brute > 0

                nouvelle_case = Case(ligne, colonne, valeur)
                
                cases_du_motif.append(nouvelle_case)
                
                self.dictionnaire_cases[(ligne, colonne)] = nouvelle_case

            nouveau_motif = Motif(cases_du_motif)
            self.motifs.append(nouveau_motif)
