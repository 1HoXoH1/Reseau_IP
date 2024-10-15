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

        # Première section : "Appertenance Réseau"
        self.input_group_2 = QGroupBox("Entrée des données")
        self.input_layout_2 = QHBoxLayout()

        # Adresse IP
        self.AD_IP_2 = QLineEdit(self)
        self.AD_IP_2.setPlaceholderText('Adresse IP')

        # Masque de sous-réseau
        self.masque_2 = QLineEdit(self)
        self.masque_2.setPlaceholderText('Masque IP')

        # Adresse réseau
        self.AD_RESEAU = QLineEdit(self)
        self.AD_RESEAU.setPlaceholderText('Adresse Réseau')

        # Expression régulière pour valider les adresses
        adress_regex = QRegExp(
            r'^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$')
        AD_IP_validator = QRegExpValidator(adress_regex, self.AD_IP_2)
        masque_2_validator = QRegExpValidator(adress_regex, self.masque_2)
        AD_RESEAU_validator = QRegExpValidator(adress_regex, self.AD_RESEAU)

        self.AD_IP_2.setValidator(AD_IP_validator)
        self.masque_2.setValidator(masque_2_validator)
        self.AD_RESEAU.setValidator(AD_RESEAU_validator)

        # Bouton de génération
        self.btn_generate_2 = QPushButton('Générer', self)

        # Ajout des widgets dans la ligne d'entrée
        self.input_layout_2.addWidget(self.AD_IP_2)
        self.input_layout_2.addWidget(self.masque_2)
        self.input_layout_2.addWidget(self.AD_RESEAU)
        self.input_layout_2.addWidget(self.btn_generate_2)

        self.input_group_2.setLayout(self.input_layout_2)
        self.Master_Layout.addWidget(self.input_group_2)

        # Séparateur entre la section d'entrée et la section des résultats
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.Master_Layout.addWidget(self.separator)

        # Deuxième section : "Résultats"
        self.result_group_2 = QGroupBox("Résultats")
        self.result_layout_2 = QVBoxLayout()

        # Label de réponse
        self.lbl_rep = QLabel('Réponse :', self)
        self.result_layout_2.addWidget(self.lbl_rep)

        self.result_group_2.setLayout(self.result_layout_2)

        # Ajout du groupe de résultats au layout principal
        self.Master_Layout.addWidget(self.result_group_2)

        # Appliquer le layout principal
        self.setLayout(self.Master_Layout)

        # Connecter le bouton au générateur d'adresse IP
        self.btn_generate_2.clicked.connect(self.SameNetwork)

        # Style général de la fenêtre
        self.setStyleSheet(open("Style/styleLog.css").read())

    def SameNetwork(self):
        # Récupérer les valeurs des champs de saisie
        ip_str = self.AD_IP_2.text()
        masque_str = self.masque_2.text()
        reseau_str = self.AD_RESEAU.text()


        # Vérifier que les champs ne sont pas vides
        if not ip_str.strip() and not masque_str.strip() and not reseau_str.strip():
            self.lbl_rep.setText("Aucun champs rempli.")
            return
        if not ip_str.strip() and not masque_str.strip():
            self.lbl_rep.setText("Aucune adresse IP et aucun masque.")
            return
        if not ip_str.strip() and not reseau_str.strip():
            self.lbl_rep.setText("Aucune adresse IP et aucune adresse réseau.")
            return
        if not masque_str.strip() and not reseau_str.strip():
            self.lbl_rep.setText("Aucun masque et aucune adresse réseau.")
            return
        if not ip_str.strip():
            self.lbl_rep.setText("Aucune adresse IP.")
            return
        if not masque_str.strip():
            self.lbl_rep.setText("Aucun masque.")
            return
        if not reseau_str.strip():
            self.lbl_rep.setText("Aucune adresse réseau.")
            return

        # Vérification de la classe de l'IP
        premier_octet = int(ip_str.split('.')[0])

        if 1 <= premier_octet <= 126:
            classe = 'A'
            masque_class = ipaddress.IPv4Network("0.0.0.0/8").netmask
        elif 128 <= premier_octet <= 191:
            classe = 'B'
            masque_class = ipaddress.IPv4Network("0.0.0.0/16").netmask
        elif 192 <= premier_octet <= 223:
            classe = 'C'
            masque_class = ipaddress.IPv4Network("0.0.0.0/24").netmask
        else:
            self.lbl_rep.setText("L'adresse renseignée est en dehors des classes A, B ou C.")
            return

        try:
            masque_sous_reseau = ipaddress.IPv4Network(f"0.0.0.0/{masque_str}", strict=False).netmask
        except ValueError:
            self.lbl_rep.setText("Le masque renseigné n'est pas valide.")
            return

        try:
            # Créer l'adresse IP
            ip = ipaddress.IPv4Address(ip_str)

            # Vérifier si l'adresse IP est réservée ou privée
            if ip.is_reserved:
                self.lbl_rep.setText("L'adresse renseignée est réservée.")
                return
            if ip.is_private:
                self.lbl_rep.setText("L'adresse renseignée est privée.")
                return

            # Créer le réseau à partir de l'adresse réseau et du masque
            try:
                reseau = ipaddress.IPv4Network(f"{reseau_str}/{masque_str}", strict=True)
            except ValueError:
                self.lbl_rep.setText("L'adresse réseau n'est pas valide pour ce masque.")
                return

            # Vérifier si l'adresse IP est dans le réseau
            if ip in reseau:
                self.lbl_rep.setText(f"L'adresse IP {ip} est dans le réseau {reseau_str} .")
            else:
                self.lbl_rep.setText(f"L'adresse IP {ip} n'est pas dans le réseau {reseau_str} .")
        except ValueError:
            # Gestion des erreurs de format incorrect
            self.lbl_rep.setText("Erreur dans l'IP, le masque ou l'adresse réseau.")

