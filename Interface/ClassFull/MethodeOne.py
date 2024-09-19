import ipaddress

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class Methode_One(QWidget):
    def __init__(self):
        super().__init__()

        # Master Layout
        self.Master_Layout = QVBoxLayout()
        self.Master_Layout.setAlignment(Qt.AlignTop)
        self.Master_Layout.setContentsMargins(20, 20, 20, 20)

        # GroupBox pour les champs d'entrée
        self.input_group = QGroupBox("Paramètres IP")
        self.input_layout = QHBoxLayout()

        # Adresse IP
        self.AD_IP = QLineEdit(self)
        self.AD_IP.setPlaceholderText('Adresse IP')
        self.AD_IP.setFixedWidth(150)

        # Masque de sous-réseau
        self.masque = QComboBox(self)
        self.masque.addItems(['255.0.0.0', '255.255.0.0', '255.255.255.0'])
        self.masque.setFixedWidth(150)

        # Bouton de génération
        self.btn_generate = QPushButton('Generate', self)
        self.btn_generate.setFixedWidth(100)

        # Ajout des widgets dans la ligne d'entrée
        self.input_layout.addWidget(self.AD_IP)
        self.input_layout.addWidget(self.masque)
        self.input_layout.addWidget(self.btn_generate)

        self.input_group.setLayout(self.input_layout)

        # Ajout de la GroupBox dans le layout principal
        self.Master_Layout.addWidget(self.input_group)

        # Séparateur (ligne horizontale)
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.Master_Layout.addWidget(self.separator)

        # Labels pour afficher les résultats
        self.result_group = QGroupBox("Résultats")
        self.result_layout = QVBoxLayout()

        self.lbl_AD_reseau = QLabel('Adresse Réseau:', self)
        self.lbl_Broadcast_IP = QLabel('Adresse Broadcast:', self)


        # Ajouter les labels dans le layout vertical des résultats
        self.result_layout.addWidget(self.lbl_AD_reseau)
        self.result_layout.addWidget(self.lbl_Broadcast_IP)


        self.result_group.setLayout(self.result_layout)

        # Ajout du groupe de résultats au layout principal
        self.Master_Layout.addWidget(self.result_group)

        # Appliquer le layout principal
        self.setLayout(self.Master_Layout)

        # Connecter le bouton au générateur d'adresse IP
        self.btn_generate.clicked.connect(self.generator_Ip_ClassFull)

    def generator_Ip_ClassFull(self):
        ip = self.AD_IP.text()
        masque = self.masque.currentText()

        # Appel de la fonction de calcul
        adresse_reseau, broadcast = self.Calc_data(ip, masque)

        # Mise à jour des labels avec les valeurs calculées
        self.lbl_AD_reseau.setText(f"Adresse Réseau: {adresse_reseau}")
        self.lbl_Broadcast_IP.setText(f"Adresse Broadcast: {broadcast}")


    def Calc_data(self, ip_str, masque_str):
        try:
            # Conversion des chaînes en objets IPv4
            ip = ipaddress.IPv4Address(ip_str)
            masque = ipaddress.IPv4Network(f"0.0.0.0/{masque_str}", strict=False).netmask

            # Calcul de l'adresse réseau
            adresse_reseau = ipaddress.IPv4Address(int(ip) & int(masque))

            # Calcul de l'adresse de broadcast
            broadcast = ipaddress.IPv4Address(int(adresse_reseau) | (int(masque) ^ 0xFFFFFFFF))

            return str(adresse_reseau), str(broadcast)
        except ValueError:
            # Gestion des erreurs de format incorrect
            return "Erreur dans l'IP ou le masque", "Erreur"
