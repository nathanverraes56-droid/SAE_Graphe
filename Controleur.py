import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QStackedWidget, QFileDialog)
from PyQt6.QtGui import QIcon
from Page_princ import Page_princ
from VueParam import VueParam
from VueJeu import VueJeu   # Import de ta vue de jeu
from Grille import Grille   # Import de ton modèle de données
import traceback

class Controleur(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuration de la fenêtre principale
        self.setWindowTitle("Projet SAE Néonaure")
        self.setWindowIcon(QIcon(os.path.join(sys.path[0], 'Images', 'Icone.png')))
        self.resize(550, 550)

        # Initialisation du modèle de jeu
        self.modele_jeu = Grille(8)

        # Configuration du QStackedWidget
        self.pile_vues = QStackedWidget()
        self.setCentralWidget(self.pile_vues)

        # Instanciation des vues 
        self.vue_menu = Page_princ()
        self.vue_param = VueParam()
        self.vue_jeu = VueJeu()      

        # Ajout des vues dans la pile
        self.pile_vues.addWidget(self.vue_menu)
        self.pile_vues.addWidget(self.vue_param)
        self.pile_vues.addWidget(self.vue_jeu)  

        # Connexions des signaux 
        self.vue_menu.b_para.clicked.connect(self.afficher_para)
        self.vue_menu.b_quitter.clicked.connect(self.close)
        self.vue_param.b_retour.clicked.connect(self.afficher_menu)
        self.vue_param.b_Theme1.clicked.connect(self.Theme1)
        self.vue_param.b_Theme2.clicked.connect(self.Theme2)
        
        # Connexion pour aller sur la page de jeu 
        self.vue_menu.b_jouer.clicked.connect(self.afficher_jeu)

        # Connexions des boutons de la page de Jeu
        self.vue_jeu.ouvrir.clicked.connect(self.action_ouvrir_grille)
        self.vue_jeu.verification.clicked.connect(self.action_verifier_grille)
        self.vue_jeu.quitter.clicked.connect(self.afficher_menu) 
        
        # Écoute active des cases de texte de la grille de jeu
        self.connecter_signaux_grille()
        
        # Application du thème par défaut au démarrage
        self.Theme1()

   # Fonction pour appliquer le QSS (Voir TP3)
    def appliquer_qss(self, nom_fichier: str) -> None:
        chemin_complet = os.path.join(sys.path[0], "fichier_qss", nom_fichier)
        if os.path.exists(chemin_complet):
            with open(chemin_complet, 'r', encoding='utf-8') as fichier_style:
                qss = fichier_style.read()
                QApplication.instance().setStyleSheet(qss)

    def afficher_para(self):
        self.pile_vues.setCurrentIndex(1)

    def afficher_menu(self):
        self.resize(550, 550) 
        self.pile_vues.setCurrentIndex(0)
        
    def afficher_jeu(self):
        self.resize(700, 700) 
        self.pile_vues.setCurrentIndex(2)
        
    def Theme1(self) -> None:
        self.appliquer_qss("Diffnes.qss")
        self.vue_param.b_Theme1.setEnabled(False)
        self.vue_param.b_Theme2.setEnabled(True)
    
    def Theme2(self) -> None:
        self.appliquer_qss("Adaptic.qss")
        self.vue_param.b_Theme1.setEnabled(True)
        self.vue_param.b_Theme2.setEnabled(False)



    #Début de la partie jeux
    def connecter_signaux_grille(self) -> None:
        """Détecte quand le joueur tape un chiffre dans l'une des cases."""
        for coords, qline_edit in self.vue_jeu.cases.items():
            ligne, colonne = coords
            qline_edit.textChanged.connect(
                lambda texte, l=ligne, c=colonne: self.gerer_saisie_joueur(l, c, texte)
            )

    def calculer_bordures_motifs(self) -> None:
        """
        Analyse la grille pour déterminer où tracer les traits gras des motifs.
        Génère un dictionnaire contenant le style CSS des bordures pour chaque case.
        """
        self.styles_bordures = {}
        
        # Création des motifs
        carte_motifs = {}
        for motif in self.modele_jeu.motifs:
            for case in motif.liste_cases:
                carte_motifs[(case.position_ligne, case.position_colonne)] = motif

        # On calcule les 4 bordures pour chaque case
        for l in range(self.modele_jeu.taille):
            for c in range(self.modele_jeu.taille):
                motif_actuel = carte_motifs.get((l, c))
                if not motif_actuel:
                    continue

                # On regarde à quel motif appartiennent les 4 voisins directs
                voisin_haut = carte_motifs.get((l - 1, c))
                voisin_bas = carte_motifs.get((l + 1, c))
                voisin_gauche = carte_motifs.get((l, c - 1))
                voisin_droite = carte_motifs.get((l, c + 1))

                # Si le voisin est d'un motif différent (ou qu'on touche le bord), on met 3px noir.
                # Sinon, on met 1px gris clair pour délimiter les cases du même motif.
                b_top = "3px solid black" if voisin_haut != motif_actuel else "1px solid #ccc"
                b_bottom = "3px solid black" if voisin_bas != motif_actuel else "1px solid #ccc"
                b_left = "3px solid black" if voisin_gauche != motif_actuel else "1px solid #ccc"
                b_right = "3px solid black" if voisin_droite != motif_actuel else "1px solid #ccc"

                # On sauvegarde la règle CSS de cette case
                self.styles_bordures[(l, c)] = f"border-top: {b_top}; border-bottom: {b_bottom}; border-left: {b_left}; border-right: {b_right};"


    def remplir_grille_graphique(self) -> None:
        """Prend les données du modèle Grille et les affiche dans la VueJeu."""
        self.vue_jeu.blockSignals(True) 
        self.calculer_bordures_motifs()

        for coords, case_modele in self.modele_jeu.dictionnaire_cases.items():
            qline_edit = self.vue_jeu.cases.get(coords)
            if qline_edit:
                qline_edit.setText(str(case_modele.valeur) if case_modele.valeur is not None else "")

                # On récupère les bordures générées pour cette case spécifique
                bordures_css = self.styles_bordures.get(coords, "border: 1px solid black;")

                if case_modele.est_fixe:
                    qline_edit.setReadOnly(True)
                    # On met les bordures + le fond gris + écriture noire
                    qline_edit.setStyleSheet(f"{bordures_css} font-size: 20px; background-color: #e0e0e0; font-weight: bold; color: black;")
                else:
                    qline_edit.setReadOnly(False)
                    # On met les bordures + le fond blanc + écriture bleue
                    qline_edit.setStyleSheet(f"{bordures_css} font-size: 20px; background-color: white; color: blue;")
                    
        self.vue_jeu.blockSignals(False)
        self.vue_jeu.etatresolution.setText("État de Résolution : En cours")


    def gerer_saisie_joueur(self, ligne: int, colonne: int, texte: str) -> None:
        """Met à jour le modèle et colore la case en rouge s'il y a un doublon adjacent."""
        case_modele = self.modele_jeu.dictionnaire_cases.get((ligne, colonne))
        qline_edit = self.vue_jeu.cases.get((ligne, colonne))
        
        if not case_modele or not qline_edit:
            return

        valeur = int(texte) if (texte.isdigit() and texte != "0") else None
        if texte == "0": 
            qline_edit.setText("")

        case_modele.set_valeur(valeur)

        # On a besoin de redonner ses bordures à la case quand on change sa couleur de fond
        bordures_css = self.styles_bordures.get((ligne, colonne), "border: 1px solid black;")

        if valeur is not None and not self.modele_jeu.verifier_voisins(ligne, colonne):
            qline_edit.setStyleSheet(f"{bordures_css} font-size: 20px; background-color: #ffcccc; color: red;")
            self.vue_jeu.etatresolution.setText("État de Résolution : Erreur d'adjacence !")
        else:
            qline_edit.setStyleSheet(f"{bordures_css} font-size: 20px; background-color: white; color: blue;")
            self.vue_jeu.etatresolution.setText("État de Résolution : En cours")

    def action_ouvrir_grille(self) -> None:
        """Bouton Ouvrir : Charge un fichier JSON."""
        chemin_fichier, _ = QFileDialog.getOpenFileName(self, "Ouvrir une grille Néonaure", "", "Fichiers JSON (*.json)")
        if chemin_fichier:
            self.modele_jeu.charger_grille_json(chemin_fichier)
            self.remplir_grille_graphique()
            

    def action_verifier_grille(self) -> None:
        """Bouton Vérification : Valide la grille entière (Voisins + Motifs)."""
        # Test des voisinages
        for coords in self.modele_jeu.dictionnaire_cases.keys():
            if not self.modele_jeu.verifier_voisins(coords[0], coords[1]):
                self.vue_jeu.etatresolution.setText("Vérification : Doublon détecté côte à côte !")
                return

        # Test des motifs
        for motif in self.modele_jeu.motifs:
            if not motif.verifier_contraintes():
                self.vue_jeu.etatresolution.setText("Vérification : Erreur dans la répartition d'un motif !")
                return

        # Validation de fin de partie
        if all(c.valeur is not None for c in self.modele_jeu.dictionnaire_cases.values()):
            self.vue_jeu.etatresolution.setText("Félicitations ! Grille résolue ! 🎈🎉🎈🎉🎈🎉🎈🎉🎈🎉🎉🎉🎈🎈")
        else:
            self.vue_jeu.etatresolution.setText("Vérification : Aucune erreur, continuez !")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controleur = Controleur()
    controleur.show()
    sys.exit(app.exec())