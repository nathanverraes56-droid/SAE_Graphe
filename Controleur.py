import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QStackedWidget)
from PyQt6.QtGui import QIcon
from Page_princ import *
from VueParam import *
import os

class Controleur(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuration de la fenêtre principale
        self.setWindowTitle("Projet SAE Néonaure")
        self.setWindowIcon(QIcon(sys.path[0] + '/Images/Icone.png'))
        self.resize(550, 550)
        #  Configuration de l'image de fond
        pixmap_fond = QPixmap("Images/Icone.png")
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, 
                         QBrush(pixmap_fond.scaled(self.size(), 
                                Qt.AspectRatioMode.IgnoreAspectRatio, 
                                Qt.TransformationMode.SmoothTransformation)))
        self.setPalette(palette)

        #  Création du QStackedWidget
        self.pile_vues = QStackedWidget()
        self.setCentralWidget(self.pile_vues)

        #  Instanciation des vues
        self.vue_menu = Page_princ()
        self.vue_param = VueParam()

        # Ajout des vues dans la pile
        self.pile_vues.addWidget(self.vue_menu)
        self.pile_vues.addWidget(self.vue_param)

        #Connexion des signaux aux méthodes du contrôleur
        self.vue_menu.b_para.clicked.connect(self.afficher_para)
        self.vue_menu.b_quitter.clicked.connect(self.close)
        self.vue_param.b_retour.clicked.connect(self.afficher_menu)
        self.vue_param.b_Theme1.clicked.connect(self.Theme1)
        self.vue_param.b_Theme2.clicked.connect(self.Theme2)
        
        
    def appliquer_qss(self, nom_fichier: str) -> None:
        chemin_complet = os.path.join(sys.path[0], "fichiers_qss", nom_fichier)
        
        if os.path.exists(chemin_complet):
            with open(chemin_complet, 'r', encoding='utf-8') as fichier_style:
                qss = fichier_style.read()
                QApplication.instance().setStyleSheet(qss)
                
                
                
                
                

    def afficher_para(self):
        # Bascule sur la vue des paramètres
        self.pile_vues.setCurrentIndex(1)

    def afficher_menu(self):
        # Bascule sur le menu principal
        self.pile_vues.setCurrentIndex(0)
    
    # def afficher_jeu(self):
        #bascule sur le menu de jeu
        #self.pile_vues.setCurrentIndex(2)
        
    def Theme1(self) -> None:
        self.appliquer_qss("Diffnes.qss")
    
    def Theme2(self) -> None:
        self.appliquer_qss("Adaptic.qss")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controleur = Controleur()
    controleur.show()
    sys.exit(app.exec())