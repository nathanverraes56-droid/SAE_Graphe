import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QStackedWidget, QFileDialog, QMessageBox)
from PyQt6.QtGui import QIcon
from Page_princ import Page_princ
from VueParam import VueParam
from VueJeu import VueJeu
from Grille import Grille
import json

class Controleur(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuration de la fenêtre principale
        self.setWindowTitle("Projet SAE Néonaure")
        self.setWindowIcon(QIcon(os.path.join(sys.path[0], 'Images', 'Icone.png')))
        self.resize(550, 550)

        # Initialisation du modèle de jeu
        self.modele_jeu = Grille(8)
        self.partie_modifiee = False

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
        self.vue_jeu.quitter.clicked.connect(self.afficher_menu)
        self.vue_jeu.enregistrer.clicked.connect(self.action_enregistrer_grille)
        
        self.connecter_signaux_grille()
        
        # Application du thème par défaut au démarrage
        self.setProperty("etat_fenetre", "menu")
        self.Theme1()

   # Fonction pour appliquer le QSS (Voir TP3)
    def appliquer_qss(self, nom_fichier: str) -> None:
        chemin_complet = os.path.join(sys.path[0], "fichier_qss", nom_fichier)
        if os.path.exists(chemin_complet):
            with open(chemin_complet, 'r', encoding='utf-8') as fichier_style:
                qss = fichier_style.read()
                QApplication.instance().setStyleSheet(qss)

    def afficher_jeu(self):
        self.resize(600, 600) 
        self.pile_vues.setCurrentIndex(2)
        
        # On passe en mode "jeu" et on met à jour le visuel
        self.setProperty("etat_fenetre", "jeu")
        self.style().unpolish(self)
        self.style().polish(self)

    def afficher_menu(self):
        self.resize(550, 550) 
        self.pile_vues.setCurrentIndex(0)
        
        # On passe en mode "menu" et on met à jour le visuel
        self.setProperty("etat_fenetre", "menu")
        self.style().unpolish(self)
        self.style().polish(self)
        
    def afficher_para(self):
        self.pile_vues.setCurrentIndex(1)
        
        # On repasse en mode "menu" et on met à jour le visuel
        self.setProperty("etat_fenetre", "menu")
        self.style().unpolish(self)
        self.style().polish(self)
        
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
        """
        Détecte quand le joueur tape un chiffre dans l'une des cases.
        """
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
        self.carte_motifs = {}
        for motif in self.modele_jeu.motifs:
            for case in motif.liste_cases:
                self.carte_motifs[(case.position_ligne, case.position_colonne)] = motif

        # On calcule les 4 bordures pour chaque case
        for l in range(self.modele_jeu.taille):
            for c in range(self.modele_jeu.taille):
                motif_actuel = self.carte_motifs.get((l, c))
                if not motif_actuel:
                    continue

                # On regarde à quel motif appartiennent les 4 voisins directs
                voisin_haut = self.carte_motifs.get((l - 1, c))
                voisin_bas = self.carte_motifs.get((l + 1, c))
                voisin_gauche = self.carte_motifs.get((l, c - 1))
                voisin_droite = self.carte_motifs.get((l, c + 1))

                # Si le voisin est d'un motif différent ou que l'on touche le bord, on met 3px noir.
                # Sinon, on met 1px gris clair pour délimiter les cases du même motif.
                b_top = "3px solid black" if voisin_haut != motif_actuel else "1px solid #ccc"
                b_bottom = "3px solid black" if voisin_bas != motif_actuel else "1px solid #ccc"
                b_left = "3px solid black" if voisin_gauche != motif_actuel else "1px solid #ccc"
                b_right = "3px solid black" if voisin_droite != motif_actuel else "1px solid #ccc"

                # On sauvegarde la règle CSS de cette case
                self.styles_bordures[(l, c)] = f"border-top: {b_top}; border-bottom: {b_bottom}; border-left: {b_left}; border-right: {b_right};"


    def remplir_grille_graphique(self) -> None:
        """
        Récupère les données du modèle Grille et les affiche dans la VueJeu.
        """
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
                    # On met les bordures avec le fond gris et l'écriture noire
                    qline_edit.setStyleSheet(f"{bordures_css} font-size: 20px; background-color: #e0e0e0; font-weight: bold; color: black;")
                else:
                    qline_edit.setReadOnly(False)
                    # On met les bordures avec le fond blanc et l'écriture bleue
                    qline_edit.setStyleSheet(f"{bordures_css} font-size: 20px; background-color: white; color: blue;")
                    
        self.vue_jeu.blockSignals(False)
        self.vue_jeu.etatresolution.setText("État de Résolution : En cours")


    def gerer_saisie_joueur(self, ligne: int, colonne: int, texte: str) -> None:
        """
        Enregistre le texte tapé et déclenche le contrôle de toute la grille.
        """
        case_modele = self.modele_jeu.dictionnaire_cases.get((ligne, colonne))
        qline_edit = self.vue_jeu.cases.get((ligne, colonne))
        
        if not case_modele or not qline_edit:
            return

        # On sauvegarde la valeur tapée dans le modèle
        valeur = int(texte) if (texte.isdigit() and texte != "0") else None
        if texte == "0": 
            qline_edit.setText("")

        case_modele.set_valeur(valeur)
        self.partie_modifiee = True

        # On lance l'analyse pour mettre à jour les couleurs
        self.mettre_a_jour_erreurs_visuelles()

    def mettre_a_jour_erreurs_visuelles(self) -> None:
        """Parcourt toute la grille et affiche en rouge les cases qui enfreignent une règle."""
        erreur_trouvee = False
        message = "État de Résolution : En cours"

        for coords, case_modele in self.modele_jeu.dictionnaire_cases.items():
            if case_modele.est_fixe:
                continue # On ne change jamais la couleur des indices fixes (ils restent gris)
            
            qline_edit = self.vue_jeu.cases.get(coords)
            bordures_css = self.styles_bordures.get(coords, "border: 1px solid black;")

            if case_modele.valeur is not None:
                #vérification des voisins
                voisins_ok = self.modele_jeu.verifier_voisins(coords[0], coords[1])
                
                #vérification du motif (Doublons ou chiffre > N)
                motif_actuel = self.carte_motifs.get(coords)
                motif_ok = motif_actuel.estValide() if motif_actuel else True

                # en cas d'erreur la case passe en rouge
                if not voisins_ok or not motif_ok:
                    qline_edit.setStyleSheet(f"{bordures_css} font-size: 20px; background-color: #ffcccc; color: red;")
                    erreur_trouvee = True
                    
                    if not voisins_ok:
                        message = "Erreur : Doublon avec un voisin adjacent !"
                    elif case_modele.valeur > motif_actuel.getTaille():
                        message = f"Erreur : Chiffre supérieur à {motif_actuel.getTaille()} !"
                    else:
                        message = "Erreur : Doublon détecté dans le motif !"
                else:
                    # case redevient blanche avec texte bleu
                    qline_edit.setStyleSheet(f"{bordures_css} font-size: 20px; background-color: white; color: blue;")
            else:
                # si la case est vide on s'assure qu'elle soit blanche
                qline_edit.setStyleSheet(f"{bordures_css} font-size: 20px; background-color: white; color: blue;")
                
        # all(...) renvoie True uniquement si toutes les cases ont une valeur
        grille_complete = all(case.valeur is not None for case in self.modele_jeu.dictionnaire_cases.values())

        #affichage du message final
        if erreur_trouvee:
            self.vue_jeu.etatresolution.setText(message)
        elif grille_complete:
            # s'il n'y a pas d'erreur (erreur_trouvee est False) ET que la grille est pleine
            self.vue_jeu.etatresolution.setText("Félicitations ! Grille résolue ! 🎉🎈🎉🎈🎉🎈🎉🎈🎈🎉🎉🎉🎉🎉🎈🎈🎈🎈🎉🎈🎉🎈🐅🐅")
            self.partie_modifiee = False # on considère la partie terminée, on peut quitter sans pop-up
        else:
            self.vue_jeu.etatresolution.setText("État de Résolution : En cours")
            
    def action_enregistrer_grille(self) -> None:
        """
        C'est le bouton "Enregistrer" il sauvegarde la partie en cours au format JSON.
        """
        chemin_fichier, _ = QFileDialog.getSaveFileName(self, "Enregistrer la grille", "", "Fichiers JSON (*.json)")
        
        # Si le joueur ne souhaite plus enregistrer
        if not chemin_fichier:
            return

        donnees_a_sauvegarder = {}
        
        # Reconstruction du dictionnaire sur chaque motif à l'aide d'une boucle
        for i, motif in enumerate(self.modele_jeu.motifs):
            nom_motif = f"motif{i+1}"
            cases_motif = []
            
            for case in motif.liste_cases:
                # On remplace None par 0 pour le fichier JSON
                valeur = case.valeur if case.valeur is not None else 0
                
                # On ajoute case.est_fixe à la fin
                cases_motif.append([case.position_colonne, case.position_ligne, valeur, case.est_fixe])
            
            donnees_a_sauvegarder[nom_motif] = cases_motif
            
        try:
            with open(chemin_fichier, 'w', encoding='utf-8') as fichier:
                # Permet de créer un fichier JSON lisible
                json.dump(donnees_a_sauvegarder, fichier, indent=4)
                
            self.vue_jeu.etatresolution.setText("Sauvegarde réussie !")
            self.partie_modifiee = False
        except Exception as e:
            self.vue_jeu.etatresolution.setText(f"Erreur de sauvegarde : {e}")

    def action_ouvrir_grille(self) -> None:
        """Bouton Ouvrir : Charge un fichier JSON uniquement en format 8x8."""
        chemin_fichier, _ = QFileDialog.getOpenFileName(self, "Ouvrir une grille Néonaure", "", "Fichiers JSON (*.json)")
        if not chemin_fichier:
            return # L'utilisateur a annulé la sélection

        try:
            # prelecture du fichier pour validation stricte du format 8x8
            with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
                donnees = json.load(fichier)

            compteur_cases = 0
            format_incorrect = False

            for nom_motif, liste_cases_json in donnees.items():
                for donnee_case in liste_cases_json:
                    colonne = donnee_case[0]
                    ligne = donnee_case[1]
                    compteur_cases += 1
                    
                    # si une coordonnée sort des index d'une grille 8x8 (0 à 7)
                    if ligne < 0 or ligne >= 8 or colonne < 0 or colonne >= 8:
                        format_incorrect = True

            # si le compte n'y est pas ou si ça déborde
            if compteur_cases != 64 or format_incorrect:
                QMessageBox.warning(
                    self,
                    "Format de grille non supporté",
                    f"Impossible d'importer cette grille.\n",
                    QMessageBox.StandardButton.Ok
                )
                return # on annule

            #si la validation est réussie, on procède au chargement normal
            self.modele_jeu.charger_grille_json(chemin_fichier)
            self.remplir_grille_graphique()
            self.partie_modifiee = False
            
        except Exception as e:
            # si le fichier JSON a un problème
            QMessageBox.critical(
                self,
                "Erreur de lecture",
                f"Le fichier JSON est corrompu ou illisible :\n{e}",
                QMessageBox.StandardButton.Ok
            )
            
    def peut_quitter_grille(self) -> bool:
        """
        Vérifie si la grille a été modifiée si oui affiche une boîte de dialogue de confirmation.
        """
        if self.partie_modifiee:
            # Création de la boîte de message de type Question
            reponse = QMessageBox.question(
                self,
                "Changements non sauvegardés",
                "Vous avez des modifications en cours. Voulez-vous vraiment quitter sans sauvegarder ?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No # Bouton sélectionné par défaut par sécurité
            )
            
            # Si le joueur répond "Oui", on l'autorise à quitter
            return reponse == QMessageBox.StandardButton.Yes
            
        return True # Si pas de modification, on peut quitter directement

    def afficher_menu(self):
        """Appelée lors du clic sur 'Quitter' dans le jeu"""
        # on bascule sur le menu que si le joueur a confirmé ou n'a rien modifié
        if self.peut_quitter_grille():
            self.resize(550, 550) 
            self.pile_vues.setCurrentIndex(0)
            
            self.setProperty("etat_fenetre", "menu")
            self.style().unpolish(self)
            self.style().polish(self)

    def closeEvent(self, event) -> None:
        """
        Méthode de PyQt quand on clique sur la croix.
        """
        # Si on est actuellement sur la page de jeu
        if self.pile_vues.currentIndex() == 2:
            if self.peut_quitter_grille():
                event.accept() # on accepte la fermeture de l'application
            else:
                event.ignore() # on annule la fermeture, l'application reste ouverte
        else:
            event.accept() # si on est dans les menus, on ferme directement


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controleur = Controleur()
    controleur.show()
    sys.exit(app.exec())