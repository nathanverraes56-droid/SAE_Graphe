import sys
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt 
from PyQt6.QtGui import QFont

class VueJeu(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Jeu du Néonaure')
        self.resize(600, 600)
        
        #layout vertical principal 
        
        layoutPrincipal = QVBoxLayout() ; self.setLayout(layoutPrincipal)
        
        EtatResolution = QLabel("Etat de Résolution : En cours")
        EtatResolution.resize(50,50)
        EtatResolution.setFont(QFont("Arial", pointSize=20))
        EtatResolution.setAlignment(Qt.AlignmentFlag.AlignBottom)
        #EtatResolution.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layoutBoutons = QHBoxLayout()
        
        Quitter = QPushButton("Quitter")
        Ouvrir = QPushButton("Ouvrir")
        Enregistrer = QPushButton("Enregistrer")
        Verification = QPushButton("Verification")
        Solveur = QPushButton("Solveur")
        
        layoutBoutons.addWidget(Quitter)
        layoutBoutons.addWidget(Ouvrir)
        layoutBoutons.addWidget(Enregistrer)
        layoutBoutons.addWidget(Verification)
        layoutBoutons.addWidget(Solveur)
        
        layoutPrincipal.addWidget(EtatResolution)
        layoutPrincipal.addLayout(layoutBoutons)
        
        self.show()
        
# --- main -----------------------------------------------------------------
if __name__ == "__main__":

    print(' --- main --- ')
    
    # création d'une QApplication
    app = QApplication(sys.argv)

    # creation d'un widget
    f = VueJeu()

    # lancement de l'application
    sys.exit(app.exec())