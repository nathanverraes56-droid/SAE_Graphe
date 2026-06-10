import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt 
from PyQt6.QtGui import QIcon, QPixmap, QPalette, QBrush


class VueParam(QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialisation de la fenêtre
        self.setWindowTitle("Projet SAE Néonaure")
        self.setWindowIcon(QIcon(sys.path[0] + '/Images/Icone.png'))
        self.resize(500, 500)
        
        #  Création du layout principal
        self.Principale = QVBoxLayout()
        self.Principale.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Création et stylisation du label (Titre)
        self.NomParam = QLabel("Paramètres")
        self.NomParam.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.NomParam.setStyleSheet("""
            font-size: 32px; 
            font-weight: bold; 
            color: #2A3E90;
            background-color: transparent; 
        """)

        # Création des boutons
        self.b_Theme1 = QPushButton("Thème clair")
        self.b_Theme2 = QPushButton("Thème Sombre")
        self.b_retour = QPushButton("Menu")

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
        #self.b_Theme1.setStyleSheet(style_bouton)
        #self.b_Theme2.setStyleSheet(style_bouton)
        #self.b_retour.setStyleSheet(style_bouton)
       

        # Ajout des widgets au layout
        self.Principale.addWidget(self.NomParam)
        self.Principale.addWidget(self.b_Theme1)
        self.Principale.addWidget(self.b_Theme2)
        self.Principale.addWidget(self.b_retour)
        
        # Affichage
        self.setLayout(self.Principale)
        self.show()

