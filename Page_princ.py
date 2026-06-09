import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt 
from PyQt6.QtGui import QIcon, QPixmap, QPalette, QBrush

class Page_princ(QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialisation de la fenêtre
        self.setWindowTitle("Projet SAE Néonaure")
        self.setWindowIcon(QIcon(sys.path[0] + '/Images/Icone.png'))
        self.resize(500, 500)
        
        #  Configuration de l'image de fond
        pixmap_fond = QPixmap("Images/Icone.png")
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, 
                         QBrush(pixmap_fond.scaled(self.size(), 
                                Qt.AspectRatioMode.IgnoreAspectRatio, 
                                Qt.TransformationMode.SmoothTransformation)))
        self.setPalette(palette)

        #  Création du layout principal
        self.Principale = QVBoxLayout()
        self.Principale.setAlignment(Qt.AlignmentFlag.AlignCenter) 

        #Creation d'un cube avec une opacité plus faible pour meiux voir le titre
        self.conteneur = QFrame()
        self.conteneur.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 220); 
                border-radius: 15px; 
            }
        """)
        
        # Création d'un sous-layout pour organiser les éléments DANS le conteneur
        self.layout_conteneur = QVBoxLayout(self.conteneur)
        self.layout_conteneur.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_conteneur.setContentsMargins(40, 40, 40, 40) # Ajoute de l'espace à l'intérieur de la bulle
        self.layout_conteneur.setSpacing(20) # Ajoute de l'espace entre le titre et les boutons

        # ---------------------------------------------------------

        # Création et stylisation du label (Titre)
        self.NomDuJeu = QLabel("Jeu du Néonaure")
        self.NomDuJeu.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.NomDuJeu.setStyleSheet("""
            font-size: 32px; 
            font-weight: bold; 
            color: #2A3E90;
            background-color: transparent; 
        """)

        # Création des boutons
        self.b_jouer = QPushButton("JOUER")
        self.b_quitter = QPushButton("QUITTER")

        # Application d'un style CSS aux boutons
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

        # Rendre le bouton QUITTER fonctionnel
        self.b_quitter.clicked.connect(self.close)

        # Ajout des widgets au layout
        self.layout_conteneur.addWidget(self.NomDuJeu)
        self.layout_conteneur.addWidget(self.b_jouer)
        self.layout_conteneur.addWidget(self.b_quitter)
        
        # Ajout du conteneur au layout principal
        self.Principale.addWidget(self.conteneur)
        
        # Affichage
        self.setLayout(self.Principale)
        self.show()

if __name__ == "__main__":
    print('Lancement du menu principal...')
    app = QApplication(sys.argv)
    f = Page_princ()
    sys.exit(app.exec())