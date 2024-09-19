from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import *
import ipaddress


class Methode_Three(QWidget):
    def __init__(self):
        super().__init__()
        # master VBOX
        self.Master_Layout = QVBoxLayout()
        self.Master_Layout.setAlignment(Qt.AlignTop)  # Alignement en haut

        # Création du layout pour les champs de saisie
        self.HLine = QHBoxLayout()
        self.HLine.setAlignment(Qt.AlignCenter)

        self.nbSR = QLineEdit(self)
        self.nbSR.setPlaceholderText('Nombre de sous réseau')
        self.nbHote = QLineEdit(self)
        self.nbHote.setPlaceholderText('Nombre d\'hôtes')
        self.AD_RS = QLineEdit(self)
        self.AD_RS.setPlaceholderText('Adresse réseau')

        # Expression régulière pour un masque CIDR valide
        adress_regex = QRegExp(
            r'^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\/(3[0-2]|[1-2]?[0-9])$')


        # ajout du validateur pour l'adresse réseau
        self.AD_RS_validator = QRegExpValidator(adress_regex, self.AD_RS)
        self.AD_RS.setValidator(self.AD_RS_validator)

        self.btn_generate = QPushButton('Vérification', self)

        self.HLine.addWidget(self.nbSR)
        self.HLine.addWidget(self.nbHote)
        self.HLine.addWidget(self.AD_RS)
        self.HLine.addWidget(self.btn_generate)

        # Ajout des labels qui seront sous les QLineEdit
        self.lbl_nbTotHotes = QLabel('Nomber total d\'hotes : ', self)
        self.lbl_decoupeSR = QLabel('Possibilité de découpe en fonction des sous réseaux ? : ', self)
        self.lbl_decoupeIP = QLabel('Possibilité de découpe en fonction des IPs ? : ', self)



        # Ajout des labels à la VLine (sous les champs de saisie)
        self.VLine = QVBoxLayout()
        self.VLine.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Ajouter les labels dans le layout vertical
        self.VLine.addWidget(self.lbl_nbTotHotes)
        self.VLine.addWidget(self.lbl_decoupeSR)
        self.VLine.addWidget(self.lbl_decoupeIP)


        # Ajout du layout horizontal (pour les QLineEdit) et vertical (pour les labels) dans le layout principal
        self.Master_Layout.addLayout(self.HLine)  # Les QLineEdit en haut
        self.Master_Layout.addLayout(self.VLine)  # Les labels en dessous

        self.setLayout(self.Master_Layout)

        # Connecter le bouton au générateur d'adresse IP
        #self.btn_generate.clicked.connect(self.calc_nb_total_hotes)







