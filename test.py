import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QFrame, QGridLayout, 
                             QLineEdit, QStackedWidget)
from PyQt6.QtCore import Qt 
from PyQt6.QtGui import QIcon, QPixmap, QPalette, QBrush

# ==========================================
# VUES
# ==========================================

class Page_princ(QWidget):
    def __init__(self):
        super().__init__()
        
        # Indispensable pour que le fond s'applique bien dans un QStackedWidget
        self.setAutoFillBackground(True) 
        
        # Configuration de l'image de fond
        pixmap_fond = QPixmap("Images/Icone.png")
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap_fond.scaled(500, 500, 
                                                                               Qt.AspectRatioMode.IgnoreAspectRatio, 
                                                                               Qt.TransformationMode.SmoothTransformation)))
        self.setPalette(palette)

        self.Principale = QVBoxLayout()
        self.Principale.setAlignment(Qt.AlignmentFlag.AlignCenter) 

        # Le Conteneur semi-transparent
        self.conteneur = QFrame()
        self.conteneur.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 220);
                border-radius: 15px;
            }
        """)
        
        self.layout_conteneur = QVBoxLayout(self.conteneur)
        self.layout_conteneur.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_conteneur.setContentsMargins(40, 40, 40, 40)
        self.layout_conteneur.setSpacing(20)

        # Titre
        self.NomDuJeu = QLabel("Jeu du Néonaure")
        self.NomDuJeu.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.NomDuJeu.setStyleSheet("""
            font-size: 32px; 
            font-weight: bold; 
            color: #2A3E90;
            background-color: transparent;
        """)

        # Boutons
        self.b_jouer = QPushButton("JOUER")
        self.b_quitter = QPushButton("QUITTER")

        style_bouton = """
            QPushButton {
                font-size: 18px;
                padding: 15px;
                background-color: #3498DB;
                color: white;
                border-radius: 8px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """
        self.b_jouer.setStyleSheet(style_bouton)
        self.b_quitter.setStyleSheet(style_bouton)

        self.layout_conteneur.addWidget(self.NomDuJeu)
        self.layout_conteneur.addWidget(self.b_jouer)
        self.layout_conteneur.addWidget(self.b_quitter)
        
        self.Principale.addWidget(self.conteneur)
        self.setLayout(self.Principale)


class VueJeu(QWidget):
    def __init__(self):
        super().__init__()
        
        self.layout_principal = QVBoxLayout()
        self.layout_principal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.titre = QLabel("Grille de Néonaure")
        self.titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titre.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.layout_principal.addWidget(self.titre)

        # Le composant Grille (64 cases)
        self.layout_grille = QGridLayout()
        self.layout_grille.setSpacing(0)
        self.cases = {} 

        for ligne in range(8):
            for colonne in range(8):
                case = QLineEdit()
                case.setAlignment(Qt.AlignmentFlag.AlignCenter)
                case.setMaxLength(1) 
                case.setFixedSize(50, 50)
                case.setStyleSheet("""
                    QLineEdit {
                        border: 1px solid black;
                        font-size: 20px;
                        background-color: white;
                        color: black;
                    }
                """)
                self.layout_grille.addWidget(case, ligne, colonne)
                self.cases[(ligne, colonne)] = case
                
        self.layout_principal.addLayout(self.layout_grille)

        # Bouton Retour
        self.b_retour = QPushButton("Retour au menu")
        self.b_retour.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 10px;
                background-color: #E74C3C;
                color: white;
                border-radius: 5px;
                margin-top: 20px;
            }
        """)
        self.layout_principal.addWidget(self.b_retour)
        
        self.setLayout(self.layout_principal)

# ==========================================
# CONTRÔLEUR
# ==========================================

class Controleur(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuration de la fenêtre principale
        self.setWindowTitle("Projet SAE Néonaure")
        self.setWindowIcon(QIcon(sys.path[0] + '/Images/Icone.png'))
        self.resize(550, 650) # Taille légèrement augmentée pour s'adapter à la grille

        # 1. Création du QStackedWidget
        self.pile_vues = QStackedWidget()
        self.setCentralWidget(self.pile_vues)

        # 2. Instanciation des vues
        self.vue_menu = Page_princ()
        self.vue_jeu = VueJeu()

        # 3. Ajout des vues dans la pile
        self.pile_vues.addWidget(self.vue_menu) # Index 0
        self.pile_vues.addWidget(self.vue_jeu)  # Index 1

        # 4. Connexion des signaux (boutons) aux méthodes du contrôleur
        self.vue_menu.b_jouer.clicked.connect(self.afficher_jeu)
        self.vue_menu.b_quitter.clicked.connect(self.close)
        self.vue_jeu.b_retour.clicked.connect(self.afficher_menu)

    def afficher_jeu(self):
        # Bascule sur la vue de la grille
        self.pile_vues.setCurrentIndex(1)

    def afficher_menu(self):
        # Bascule sur le menu principal
        self.pile_vues.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # On lance uniquement le contrôleur, qui gère le reste
    controleur = Controleur()
    controleur.show()
    sys.exit(app.exec())