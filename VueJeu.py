import sys
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QGridLayout, QLineEdit
from PyQt6.QtCore import Qt 
from PyQt6.QtGui import QFont

class VueJeu(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Jeu du Néonaure')
        self.resize(700, 700)
        
        #layout vertical principal 
        
        layoutPrincipal = QVBoxLayout() ; self.setLayout(layoutPrincipal)

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
                    }
                """)
                self.layout_grille.addWidget(case, ligne, colonne)
                self.cases[(ligne, colonne)] = case

        self.etatresolution = QLabel("Etat de Résolution : En cours")
        self.etatresolution.resize(50,50)
        self.etatresolution.setFont(QFont("Arial", pointSize=20))
        self.etatresolution.setAlignment(Qt.AlignmentFlag.AlignBottom)
        #EtatResolution.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.layoutBoutons = QHBoxLayout()
        
        self.quitter = QPushButton("Quitter")
        self.ouvrir = QPushButton("Ouvrir")
        self.enregistrer = QPushButton("Enregistrer")
        self.verification = QPushButton("Verification")
        self.solveur = QPushButton("Solveur")
        
        self.layoutBoutons.addWidget(self.quitter)
        self.layoutBoutons.addWidget(self.ouvrir)
        self.layoutBoutons.addWidget(self.enregistrer)
        self.layoutBoutons.addWidget(self.verification)
        self.layoutBoutons.addWidget(self.solveur)
        
        layoutPrincipal.addLayout(self.layout_grille)
        layoutPrincipal.addWidget(self.etatresolution)
        layoutPrincipal.addLayout(self.layoutBoutons)
        
        self.show()
        #commentaire
        
# --- main -----------------------------------------------------------------
if __name__ == "__main__":

    print(' --- main --- ')
    
    # création d'une QApplication
    app = QApplication(sys.argv)

    # creation d'un widget
    f = VueJeu()

    # lancement de l'application
    sys.exit(app.exec())