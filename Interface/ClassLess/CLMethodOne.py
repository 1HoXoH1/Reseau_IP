from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import *
import ipaddress

class CLMethod_One(QWidget):
    def __init__(self):
        super().__init__()
        # master VBOX
        self.Master_Layout = QVBoxLayout()
        self.Master_Layout.setAlignment(Qt.AlignTop)  # Alignement en haut

        # Création du layout pour les champs de saisie
        self.HLine = QHBoxLayout()
        self.HLine.setAlignment(Qt.AlignCenter)

        self.AD_IP = QLineEdit(self)
        self.AD_IP.setPlaceholderText('Adresse IP')
        self.masque = QLineEdit(self)
        self.masque.setPlaceholderText('Masque de l\'IP')

        # Expression régulière pour un masque CIDR valide
        adress_regex = QRegExp(
            r'^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\/(3[0-2]|[1-2]?[0-9])$')

        # Créer un validateur pour forcer l'entrée correcte
        self.AD_IP_validator = QRegExpValidator(adress_regex, self.AD_IP)
        self.AD_IP.setValidator(self.AD_IP_validator)


        # Ajout du validateur pour le champ "masque" en bloquant les caractères qui ne sont pas
        #conforme à un maque
        cidr_regex = QRegExp(r'^\/(3[0-2]|[1-2]?[0-9])$')
        self.masque_validator = QRegExpValidator(cidr_regex, self.masque)
        self.masque.setValidator(self.masque_validator)

        self.btn_generate = QPushButton('Generate', self)

        self.HLine.addWidget(self.AD_IP)
        self.HLine.addWidget(self.masque)
        self.HLine.addWidget(self.btn_generate)

        # Ajout des labels qui seront sous les QLineEdit
        self.lbl_SR_Reseau_IP = QLabel('Adresse sous-réseau:', self)
        self.lbl_SR_Broadcast_IP = QLabel('Adresse Broadcast (SR):', self)

        # Ajout des labels à la VLine (sous les champs de saisie)
        self.VLine = QVBoxLayout()
        self.VLine.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        # Ajouter les labels dans le layout vertical
        self.VLine.addWidget(self.lbl_SR_Reseau_IP)
        self.VLine.addWidget(self.lbl_SR_Broadcast_IP)

        # Ajout du layout horizontal (pour les QLineEdit) et vertical (pour les labels) dans le layout principal
        self.Master_Layout.addLayout(self.HLine)  # Les QLineEdit en haut
        self.Master_Layout.addLayout(self.VLine)  # Les labels en dessous

        self.setLayout(self.Master_Layout)

        # Connecter le bouton au générateur d'adresse IP
        self.btn_generate.clicked.connect(self.generator_Ip_ClassFull)

    def generator_Ip_ClassFull(self):
        ip = self.AD_IP.text().strip()  # Récupération de l'adresse IP et suppression des espaces
        masque = self.masque.text().strip()  # Récupération du masque au format /XX

        # Appeler la fonction calc pour obtenir l'adresse réseau et l'adresse de broadcast
        adresse_reseau, broadcast = self.Calc_data(ip, masque)

        # Mettre à jour les labels avec les valeurs calculées
        self.lbl_SR_Reseau_IP.setText(f"Adresse Sous-Réseau: {adresse_reseau}")
        self.lbl_SR_Broadcast_IP.setText(f"Adresse Broadcast (SR): {broadcast}")

    def Calc_data(self, ip_str, masque_str):
        try:
            # Convertir l'adresse IP en objet IPv4
            ip = ipaddress.IPv4Address(ip_str)

            # Créer l'objet réseau avec le masque en format CIDR
            network = ipaddress.IPv4Network(f"{ip}/{masque_str[1:]}", strict=False)

            # Calculer l'adresse de sous-réseau et l'adresse de broadcast
            adresse_reseau = network.network_address
            broadcast = network.broadcast_address

            return str(adresse_reseau), str(broadcast)
        except ValueError as e:
            # Gérer les erreurs de format incorrect
            return "Erreur dans l'IP ou le masque", "Erreur"

