from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import ipaddress

class EncodageLess(QWidget):
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
        self.btn_generate = QPushButton('Generate', self)

        self.HLine.addWidget(self.AD_IP)
        self.HLine.addWidget(self.masque)
        self.HLine.addWidget(self.btn_generate)

        # Ajout des labels qui seront sous les QLineEdit
        self.lbl_AD_reseau = QLabel('Adresse Réseau:', self)
        self.lbl_Broadcast_IP = QLabel('Adresse Broadcast:', self)
        self.lbl_SR_Reseau_IP = QLabel('Adresse sous-réseau:', self)
        self.lbl_SR_Broadcast_IP = QLabel('Adresse Broadcast (SR):', self)

        # Ajout des labels à la VLine (sous les champs de saisie)
        self.VLine = QVBoxLayout()
        self.VLine.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        # Ajouter les labels dans le layout vertical
        self.VLine.addWidget(self.lbl_AD_reseau)
        self.VLine.addWidget(self.lbl_Broadcast_IP)
        self.VLine.addWidget(self.lbl_SR_Reseau_IP)
        self.VLine.addWidget(self.lbl_SR_Broadcast_IP)

        # Ajout du layout horizontal (pour les QLineEdit) et vertical (pour les labels) dans le layout principal
        self.Master_Layout.addLayout(self.HLine)  # Les QLineEdit en haut
        self.Master_Layout.addLayout(self.VLine)  # Les labels en dessous

        self.setLayout(self.Master_Layout)

        # Connecter le bouton au générateur d'adresse IP
        self.btn_generate.clicked.connect(self.generator_Ip_ClassFull)

    def generator_Ip_ClassFull(self):
        ip = self.AD_IP.text()
        masque = self.masque.text()

        #call function calc
        adresse_reseau, broadcast = self.Calc_data(ip, masque)

        # Mettre à jour les labels avec les valeurs calculées
        self.lbl_AD_reseau.setText(f"Adresse Réseau: {adresse_reseau}")
        self.lbl_Broadcast_IP.setText(f"Adresse Broadcast: {broadcast}")
        self.lbl_SR_Reseau_IP.setText(f"Adresse Sous-Réseau: {adresse_reseau}")
        self.lbl_SR_Broadcast_IP.setText(f"Adresse Broadcast (SR): {broadcast}")

    def Calc_data(self, ip_str, masque_str):
        try:
            # Convertir les chaînes en objets IPv4
            ip = ipaddress.IPv4Address(ip_str)
            masque = ipaddress.IPv4Network(f"0.0.0.0/{masque_str}", strict=False).netmask

            # Calcul de l'adresse réseau avec l'opération AND bit à bit
            adresse_reseau = ipaddress.IPv4Address(int(ip) & int(masque))

            # Calcul de l'adresse de broadcast
            broadcast = ipaddress.IPv4Address(int(adresse_reseau) | (int(masque) ^ 0xFFFFFFFF))

            return str(adresse_reseau), str(broadcast)
        except ValueError:
            # Gérer les erreurs de format incorrect
            return "Erreur dans l'IP ou le masque", "Erreur"
