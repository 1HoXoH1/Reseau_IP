from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import *
import ipaddress

from Projet_1.ReservedAdress.ReservedAdress import is_reserved


class CLMethod_Two(QWidget):
    def __init__(self):
        super().__init__()

        # Master Layout
        self.Master_Layout = QVBoxLayout()
        self.Master_Layout.setAlignment(Qt.AlignTop)  # Alignement en haut

        # Première section : "Entrée des données"
        self.input_group = QGroupBox("Entrée des données")
        self.input_layout = QHBoxLayout()
        self.input_layout.setAlignment(Qt.AlignCenter)

        # Expression régulière pour une adresse IP valide
        adress_regex = QRegExp(
            r'^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$')

        # Expression régulière pour un masque en CIDR (e.g., /24)
        cidr_regex = QRegExp(r'^\/(3[0-2]|[1-2]?[0-9])$')

        # Champ d'entrée pour l'adresse IP
        self.AD_IP = QLineEdit(self)
        self.AD_IP.setPlaceholderText('Adresse IP')
        self.AD_IP_validator = QRegExpValidator(adress_regex, self.AD_IP)
        self.AD_IP.setValidator(self.AD_IP_validator)

        # Champ d'entrée pour le masque
        self.masque = QLineEdit(self)
        self.masque.setPlaceholderText('Masque de l\'IP')
        self.masque_validator = QRegExpValidator(cidr_regex, self.masque)
        self.masque.setValidator(self.masque_validator)

        # Champ d'entrée pour l'adresse réseau
        self.AD_RS = QLineEdit(self)
        self.AD_RS.setPlaceholderText('Adresse réseau')
        self.AD_RS_validator = QRegExpValidator(adress_regex, self.AD_RS)
        self.AD_RS.setValidator(self.AD_RS_validator)

        # Bouton de vérification
        self.btn_generate = QPushButton('Vérification', self)

        # Ajout des widgets dans le layout horizontal (input_layout)
        self.input_layout.addWidget(self.AD_IP)
        self.input_layout.addWidget(self.masque)
        self.input_layout.addWidget(self.AD_RS)
        self.input_layout.addWidget(self.btn_generate)

        # Appliquer le layout à la section "Entrée des données"
        self.input_group.setLayout(self.input_layout)

        # Ajout de la section dans le Master Layout
        self.Master_Layout.addWidget(self.input_group)

        #Séparateur entre la section d'entrée et la section des résultats
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.Master_Layout.addWidget(self.separator)

        #Deuxième section : "Résultats"
        self.result_group = QGroupBox("Résultats")
        self.result_layout = QVBoxLayout()
        self.result_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Label pour afficher si l'IP appartient au réseau
        self.lbl_dansSR = QLabel('Appartient réseau : ', self)

        # Ajouter le label dans le layout vertical des résultats
        self.result_layout.addWidget(self.lbl_dansSR)

        # Appliquer le layout à la section "Résultats"
        self.result_group.setLayout(self.result_layout)

        # Ajout de la section dans le Master Layout
        self.Master_Layout.addWidget(self.result_group)

        # Appliquer le layout principal
        self.setLayout(self.Master_Layout)

        # Connecter le bouton à la fonction de vérification d'appartenance réseau
        self.btn_generate.clicked.connect(self.verifier_appartenance_reseau)

        #Style général de la fenêtre
        self.setStyleSheet(open("Style/styleLog.css").read())

    def verifier_appartenance_reseau(self):
        ip_text = self.AD_IP.text()
        masque_text = self.masque.text().lstrip('/')  # Retirer le "/" du masque
        reseau_text = self.AD_RS.text()

        if not self.AD_IP.text().strip() and not self.masque.text().strip() and not self.AD_RS.text().strip():
            self.lbl_dansSR.setText("Aucun champ remppli.")
            return
        if not self.AD_IP.text().strip() and not self.masque.text().strip():
            self.lbl_dansSR.setText("Aucune adresse IP et aucun masque.")
            return
        if not self.AD_IP.text().strip() and not self.AD_RS.text().strip():
            self.lbl_dansSR.setText("Aucune adresse IP et aucune adresse réseau.")
            return
        if not self.masque.text().strip() and not self.AD_RS.text().strip():
            self.lbl_dansSR.setText("Aucun masque et aucune adresse réseau.")
            return
        if not self.AD_IP.text().strip():
            self.lbl_dansSR.setText("Aucune adresse IP.")
            return
        if not self.masque.text().strip():
            self.lbl_dansSR.setText("Aucun masque.")
            return
        if not self.AD_RS.text().strip():
            self.lbl_dansSR.setText("Aucune adresse réseau.")
            return

        try:
            try:
                # Combiner l'adresse de réseau et le masque pour créer un objet réseau
                reseau = ipaddress.ip_network(f'{reseau_text}/{masque_text}', strict=False)
            except ValueError:
                self.lbl_dansSR.setText("L'adresse réseau n'est pas valide.")
                return

            # Créer un objet adresse IP
            ip = ipaddress.ip_address(ip_text)

            if is_reserved(ip):
                self.lbl_dansSR.setText("L'adresse IP est réservée.")
                return

            masque_int = int(masque_text)
            if masque_int > 30:
                self.lbl_dansSR.setText("Le masque doit être inférieur ou égal à /30")
                return

            try:
                # Vérifier si l'adresse réseau est valide
                ipaddress.ip_network(f'{reseau_text}/{masque_text}', strict=True)
            except ValueError:
                self.lbl_dansSR.setText("L'adresse réseau n'est pas valide pour ce masque.")
                return


            # Vérifier si l'adresse IP appartient au réseau
            if ip in reseau:
                self.lbl_dansSR.setText(f"Appartient au réseau : Oui, l'adresse renseignée appartient bien au réseau ({reseau})")
            else:
                self.lbl_dansSR.setText(f"Appartient au réseau : Non, l'adresse renseignée n'appartient pas au réseau ({reseau})")

        except ValueError as e:
            # Gestion des erreurs de format ou autres erreurs
            self.lbl_dansSR.setText("L'adresse IP n'est pas valide.")
            return
