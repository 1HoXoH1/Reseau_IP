from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import *
import ipaddress

class CLMethod_Two(QWidget):
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
        self.AD_RS = QLineEdit(self)
        self.AD_RS.setPlaceholderText('Adresse réseau')

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

        #ajout du validateur pour l'adresse réseau
        self.AD_RS_validator = QRegExpValidator(adress_regex, self.AD_RS)
        self.AD_RS.setValidator(self.AD_RS_validator)

        self.btn_generate = QPushButton('Vérification', self)

        self.HLine.addWidget(self.AD_IP)
        self.HLine.addWidget(self.masque)
        self.HLine.addWidget(self.AD_RS)
        self.HLine.addWidget(self.btn_generate)

        # Ajout des labels qui seront sous les QLineEdit
        self.lbl_dansSR = QLabel('Appartient au réseau : ', self)

        # Ajout des labels à la VLine (sous les champs de saisie)
        self.VLine = QVBoxLayout()
        self.VLine.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        # Ajouter les labels dans le layout vertical
        self.VLine.addWidget(self.lbl_dansSR)


        # Ajout du layout horizontal (pour les QLineEdit) et vertical (pour les labels) dans le layout principal
        self.Master_Layout.addLayout(self.HLine)  # Les QLineEdit en haut
        self.Master_Layout.addLayout(self.VLine)  # Les labels en dessous

        self.setLayout(self.Master_Layout)

        # Connecter le bouton au générateur d'adresse IP
        self.btn_generate.clicked.connect(self.verifier_appartenance_reseau)

    def verifier_appartenance_reseau(self):
        ip_text = self.AD_IP.text()
        masque_text = self.masque.text().lstrip('/')  # Retirer le "/" du masque
        reseau_text = self.AD_RS.text()

        try:
            # Combiner l'adresse de réseau et le masque pour créer un objet réseau
            reseau = ipaddress.ip_network(f'{reseau_text}/{masque_text}', strict=False)

            # Créer un objet adresse IP
            ip = ipaddress.ip_address(ip_text)

            # Vérifier si l'adresse IP appartient au réseau
            if ip in reseau:
                self.lbl_dansSR.setText(f"Appartient au réseau : Oui ({reseau})")
            else:
                self.lbl_dansSR.setText(f"Appartient au réseau : Non ({reseau})")

        except ValueError as e:
            # Gestion des erreurs de format ou autres erreurs
            self.lbl_dansSR.setText(f"Erreur : {str(e)}")

