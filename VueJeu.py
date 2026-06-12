import sys
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QGridLayout, QLineEdit
from PyQt6.QtCore import Qt 
from PyQt6.QtGui import QFont, QIntValidator

class VueJeu(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Jeu du Néonaure')
        self.resize(700, 700)
        
        # Layout vertical principal
        layoutPrincipal = QVBoxLayout()
        self.setLayout(layoutPrincipal)

        # Grille de jeu
        self.layout_grille = QGridLayout()
        self.layout_grille.setSpacing(0) 
        self.layout_grille.setAlignment(Qt.AlignmentFlag.AlignCenter) # Centre la grille dans l'écran
        self.cases = {} 

        # Validateur pour n'accepter que des chiffres 
        validateur_chiffre = QIntValidator(1, 5)

        for ligne in range(8):
            for colonne in range(8):
                case = QLineEdit()
                case.setAlignment(Qt.AlignmentFlag.AlignCenter)
                case.setMaxLength(1) 
                case.setValidator(validateur_chiffre) # Empêche la saisie de lettres
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

        # Etat de la partie 
        self.etatresolution = QLabel("Etat de Résolution : En cours")
        self.etatresolution.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.etatresolution.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Barre d'outils / Boutons d'actions
        self.layoutBoutons = QHBoxLayout()
        
        self.quitter = QPushButton("Quitter")
        self.ouvrir = QPushButton("Ouvrir")
        self.enregistrer = QPushButton("Enregistrer")
        self.solveur = QPushButton("Solveur")
        
        self.layoutBoutons.addWidget(self.quitter)
        self.layoutBoutons.addWidget(self.ouvrir)
        self.layoutBoutons.addWidget(self.enregistrer)
        self.layoutBoutons.addWidget(self.solveur)
        
        # Assemblage dans le layout principal avec gestion des espaces
        layoutPrincipal.addSpacing(20)
        layoutPrincipal.addLayout(self.layout_grille)
        layoutPrincipal.addSpacing(20)
        layoutPrincipal.addWidget(self.etatresolution)
        layoutPrincipal.addStretch() # Pousse les boutons vers le bas proprement
        layoutPrincipal.addLayout(self.layoutBoutons)
        
        self.show()