from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import ipaddress


class Encodage(QWidget):
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
        self.lbl_SR_Reseau_IP = QLabel('Adresse sous-réseau:', self)
        self.lbl_SR_Broadcast_IP = QLabel('Adresse Broadcast (SR):', self)

        # Ajouter les labels dans le layout vertical des résultats
        self.result_layout.addWidget(self.lbl_AD_reseau)
        self.result_layout.addWidget(self.lbl_Broadcast_IP)
        self.result_layout.addWidget(self.lbl_SR_Reseau_IP)
        self.result_layout.addWidget(self.lbl_SR_Broadcast_IP)

        self.result_group.setLayout(self.result_layout)

        # Ajout du groupe de résultats au layout principal
        self.Master_Layout.addWidget(self.result_group)


        # Ajout de la 2ème partie du prog
        self.input_group_2 = QGroupBox("Appertenance Réseau")
        self.input_layout_2 = QHBoxLayout()

        #Adresse Ip
        self.AD_IP_2 = QLineEdit(self)
        self.AD_IP_2.setPlaceholderText('Adresse IP')
        self.AD_IP_2.setFixedWidth(150)

        # Masque de sous-réseau
        self.masque_2 = QComboBox(self)
        self.masque_2.addItems(['255.0.0.0', '255.255.0.0', '255.255.255.0'])
        self.masque_2.setFixedWidth(150)

        #Adresse réseau
        self.AD_RESEAU = QLineEdit(self)
        self.AD_RESEAU.setPlaceholderText('Adresse Réseau')
        self.AD_RESEAU.setFixedWidth(150)

        # Bouton de génération
        self.btn_generate_2 = QPushButton('Generate', self)
        self.btn_generate_2.setFixedWidth(100)

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
        self.btn_generate.clicked.connect(self.generator_Ip_ClassFull)
        self.btn_generate_2.clicked.connect(self.SameNetwork)

    def generator_Ip_ClassFull(self):
        ip = self.AD_IP.text()
        masque = self.masque.currentText()

        # Appel de la fonction de calcul
        adresse_reseau, broadcast = self.Calc_data(ip, masque)

        # Mise à jour des labels avec les valeurs calculées
        self.lbl_AD_reseau.setText(f"Adresse Réseau: {adresse_reseau}")
        self.lbl_Broadcast_IP.setText(f"Adresse Broadcast: {broadcast}")
        self.lbl_SR_Reseau_IP.setText(f"Adresse Sous-Réseau: {adresse_reseau}")
        self.lbl_SR_Broadcast_IP.setText(f"Adresse Broadcast (SR): {broadcast}")

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

    def SameNetwork(self):
        # Récupérer les valeurs des champs de saisie
        ip_str = self.AD_IP_2.text()
        masque_str = self.masque_2.currentText()
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