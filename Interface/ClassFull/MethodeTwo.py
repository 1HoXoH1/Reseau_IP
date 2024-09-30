import ipaddress

from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import *


class Methode_Two(QWidget):
    def __init__(self):
        super().__init__()

        # Master Layout
        self.Master_Layout = QVBoxLayout()
        self.Master_Layout.setAlignment(Qt.AlignTop)
        self.Master_Layout.setContentsMargins(20, 20, 20, 20)

        # Ajout de la 2ème partie du prog
        self.input_group_2 = QGroupBox("Appertenance Réseau")
        self.input_layout_2 = QHBoxLayout()

        #Adresse Ip
        self.AD_IP_2 = QLineEdit(self)
        self.AD_IP_2.setPlaceholderText('Adresse IP')
        #self.AD_IP_2.setFixedWidth(180)

        # Masque de sous-réseau
        self.masque_2 = QLineEdit(self)
        self.masque_2.setPlaceholderText('Masque IP')
        #self.masque_2.setFixedWidth(180)

        #Adresse réseau
        self.AD_RESEAU = QLineEdit(self)
        self.AD_RESEAU.setPlaceholderText('Adresse Réseau')
        #self.AD_RESEAU.setFixedWidth(180)

        # Expression régulière pour une adresse  valide
        adress_regex = QRegExp(
            r'^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$')


        AD_IP_validateur = QRegExpValidator(adress_regex, self.AD_IP_2)
        masque_2_validateur = QRegExpValidator(adress_regex, self.masque_2)
        AD_RS_validateur = QRegExpValidator(adress_regex, self.AD_RESEAU)

        self.AD_IP_2.setValidator(AD_IP_validateur)
        self.masque_2.setValidator(masque_2_validateur)
        self.AD_RESEAU.setValidator(AD_RS_validateur)

        # Bouton de génération
        self.btn_generate_2 = QPushButton('Générer', self)
        self.btn_generate_2.setFixedWidth(150)

        # Ajout des widgets dans la ligne d'entrée
        self.input_layout_2.addWidget(self.AD_IP_2)
        self.input_layout_2.addWidget(self.masque_2)
        self.input_layout_2.addWidget(self.AD_RESEAU)
        self.input_layout_2.addWidget(self.btn_generate_2)

        self.input_group_2.setLayout(self.input_layout_2)

        self.Master_Layout.addWidget(self.input_group_2)


        # Labels pour afficher les résultats
        self.result_group_2 = QGroupBox("Résultats")
        self.result_layout_2 = QVBoxLayout()

        self.lbl_rep = QLabel('Réponse :', self)

        # Ajouter les labels dans le layout vertical des résultats
        self.result_layout_2.addWidget(self.lbl_rep)

        self.result_group_2.setLayout(self.result_layout_2)

        # Ajout du groupe de résultats au layout principal
        self.Master_Layout.addWidget(self.result_group_2)

        # Appliquer le layout principal
        self.setLayout(self.Master_Layout)

        # Connecter le bouton au générateur d'adresse IP
        self.btn_generate_2.clicked.connect(self.SameNetwork)
        # # Style général de la fenêtre
        self.setStyleSheet(open("Style/styleLog.css").read())

    def SameNetwork(self):
        # Récupérer les valeurs des champs de saisie
        ip_str = self.AD_IP_2.text()
        masque_str = self.masque_2.text()
        reseau_str = self.AD_RESEAU.text()

        try:
            # Créer le réseau à partir de l'adresse réseau et du masque
            reseau = ipaddress.IPv4Network(f"{reseau_str}/{masque_str}", strict=False)

            # Créer l'adresse IP
            ip = ipaddress.IPv4Address(ip_str)

            # Vérifier si l'adresse IP est dans le réseau
            if ip in reseau:
                self.lbl_rep.setText(f"L'adresse IP {ip} est dans le réseau {reseau}.")
            else:
                self.lbl_rep.setText(f"L'adresse IP {ip} n'est pas dans le réseau {reseau}.")
        except ValueError:
            # Gestion des erreurs de format incorrect
            self.lbl_rep.setText("Erreur dans l'IP, le masque ou l'adresse réseau.")