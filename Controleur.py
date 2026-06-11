import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QStackedWidget)
from PyQt6.QtGui import QIcon
from Page_princ import Page_princ
from VueParam import VueParam

class Controleur(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuration de la fenêtre principale
        self.setWindowTitle("Projet SAE Néonaure")
        self.setWindowIcon(QIcon(os.path.join(sys.path[0], 'Images', 'Icone.png')))
        self.resize(550, 550)
        
        # ✨ STYLE PAR DÉFAUT AU DÉMARRAGE ✨
        # On applique directement les règles QSS pour afficher l'image de fond
        # et rendre les conteneurs transparents dès l'ouverture.
        QApplication.instance().setStyleSheet("""
            QMainWindow {
                background-image: url("Images/Icone.png");
                background-position: center;
                background-repeat: no-repeat;
            }
            QStackedWidget, QStackedWidget > QWidget {
                background-color: transparent;
            }
        """)

        # Configuration du QStackedWidget
        self.pile_vues = QStackedWidget()
        self.setCentralWidget(self.pile_vues)

        # Instanciation des vues
        self.vue_menu = Page_princ()
        self.vue_param = VueParam()

        # Ajout des vues dans la pile
        self.pile_vues.addWidget(self.vue_menu)
        self.pile_vues.addWidget(self.vue_param)

        # Connexion des signaux aux méthodes du contrôleur
        self.vue_menu.b_para.clicked.connect(self.afficher_para)
        self.vue_menu.b_quitter.clicked.connect(self.close)
        self.vue_param.b_retour.clicked.connect(self.afficher_menu)
        self.vue_param.b_Theme1.clicked.connect(self.Theme1)
        self.vue_param.b_Theme2.clicked.connect(self.Theme2)
        
    def appliquer_qss(self, nom_fichier: str) -> None:
        """Loads and applies a QSS stylesheet, with console feedback if it fails."""
        chemin_complet = os.path.join(sys.path[0], "fichier_qss", nom_fichier)
        print(f"🔍 Tentative de chargement du QSS : {chemin_complet}")
        
        if os.path.exists(chemin_complet):
            try:
                with open(chemin_complet, 'r', encoding='utf-8') as fichier_style:
                    qss = fichier_style.read()
                    QApplication.instance().setStyleSheet(qss)
                    print(f"🎨 Style '{nom_fichier}' appliqué avec succès !")
            except Exception as e:
                print(f"❌ Erreur lors de la lecture du fichier QSS : {e}")
        else:
            print(f"❌ ERREUR : Le fichier '{nom_fichier}' est introuvable à l'adresse indiquée.")

    def afficher_para(self):
        self.pile_vues.setCurrentIndex(1)

    def afficher_menu(self):
        self.pile_vues.setCurrentIndex(0)
    
    def Theme1(self) -> None:
        self.appliquer_qss("Diffnes.qss")
    
    def Theme2(self) -> None:
        self.appliquer_qss("Adaptic.qss")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controleur = Controleur()
    controleur.show()
    sys.exit(app.exec())