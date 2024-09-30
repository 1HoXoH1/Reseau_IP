from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import *
import ipaddress

class CLMethod_One(QWidget):
    def __init__(self):
        super().__init__()

        #Master Layout
        self.Master_Layout = QVBoxLayout()
        self.Master_Layout.setAlignment(Qt.AlignTop)  # Alignement en haut
        self.Master_Layout.setContentsMargins(30, 30, 30, 30)

        #Première section : "Entrée des données"
        self.input_group = QGroupBox("Entrée des données")
        self.input_layout = QHBoxLayout()
        self.input_layout.setAlignment(Qt.AlignCenter)
        self.input_layout.setSpacing(20)

        # Expression régulière pour une adresse IP valide
        adress_regex = QRegExp(
            r'^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$')

        # Expression régulière pour un masque en CIDR
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

        # Bouton de génération
        self.btn_generate = QPushButton('Generate', self)
        self.btn_generate.setFixedWidth(120)

        # Ajout des widgets dans le layout horizontal (input_layout)
        self.input_layout.addWidget(self.AD_IP)
        self.input_layout.addWidget(self.masque)
        self.input_layout.addWidget(self.btn_generate)

        # Appliquer le layout à la section "Entrée des données"
        self.input_group.setLayout(self.input_layout)

        # Ajout de la section dans le Master Layout
        self.Master_Layout.addWidget(self.input_group)

        # Séparateur entre la section d'entrée et la section des résultats
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.Master_Layout.addWidget(self.separator)

        # Deuxième section : "Résultats"
        self.result_group = QGroupBox("Résultats")
        self.result_layout = QVBoxLayout()
        self.result_layout.setAlignment(Qt.AlignLeft)
        self.result_layout.setSpacing(10)

        # Labels pour afficher les résultats
        self.lbl_SR_Reseau_IP = QLabel('Adresse sous-réseau:', self)
        self.lbl_SR_Broadcast_IP = QLabel('Adresse Broadcast (SR):', self)

        # Ajouter les labels dans le layout vertical des résultats
        self.result_layout.addWidget(self.lbl_SR_Reseau_IP)
        self.result_layout.addWidget(self.lbl_SR_Broadcast_IP)

        # Appliquer le layout à la section "Résultats"
        self.result_group.setLayout(self.result_layout)

        # Ajout de la section dans le Master Layout
        self.Master_Layout.addWidget(self.result_group)

        # Appliquer le layout principal
        self.setLayout(self.Master_Layout)

        # Connecter le bouton au générateur d'adresse IP
        self.btn_generate.clicked.connect(self.generator_Ip_ClassFull)

        #Style général de la fenêtre
        self.setStyleSheet(open("Style/styleLog.css").read())

    def generator_Ip_ClassFull(self):
        # Vérification de l'adresse IP
        if not self.AD_IP.text().strip():
            self.lbl_SR_Reseau_IP.setText("Aucune adresse IP")
            self.lbl_SR_Broadcast_IP.hide()
            return

        # Vérification du masque
        if not self.masque.text().strip():
            self.lbl_SR_Reseau_IP.setText("Aucun masque")
            self.lbl_SR_Broadcast_IP.hide()
            return

        self.lbl_SR_Broadcast_IP.show()

        ip_str = self.AD_IP.text().strip()  # Récupération de l'adresse IP et suppression des espaces
        masque_str = self.masque.text().strip()  # Récupération du masque au format /XX

        try:
            # Convertir l'adresse IP en objet IPv4
            ip = ipaddress.IPv4Address(ip_str)
            # Créer l'objet réseau avec le masque en format CIDR
            network = ipaddress.IPv4Network(f"{ip}/{masque_str[1:]}", strict=False)

            # Vérification du masque
            if network.prefixlen > 30:
                self.lbl_SR_Reseau_IP.setText("Le masque doit être inférieur ou égal à /30")
                self.lbl_SR_Broadcast_IP.hide()
                return

            # Vérification si l'adresse est réservée ou privée
            if ip.is_reserved:
                self.lbl_SR_Reseau_IP.setText("L'adresse renseignée est réservée.")
                self.lbl_SR_Broadcast_IP.hide()
                return

            if ip.is_private:
                self.lbl_SR_Reseau_IP.setText("L'adresse renseignée est privée.")
                self.lbl_SR_Broadcast_IP.hide()
                return

            # Calculer l'adresse de sous-réseau et l'adresse de broadcast
            adresse_reseau = network.network_address
            broadcast = network.broadcast_address

            # Mettre à jour les labels avec les valeurs calculées
            self.lbl_SR_Reseau_IP.setText(f"Adresse Sous-Réseau: {adresse_reseau}")
            self.lbl_SR_Broadcast_IP.setText(f"Adresse Broadcast (SR): {broadcast}")

        except ValueError as e:
            # Gérer les erreurs de format incorrect
            QMessageBox.critical(self, "Erreur", f"Entrée invalide : {e}")