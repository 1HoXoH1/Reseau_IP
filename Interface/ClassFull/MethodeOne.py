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
        self.masque = QLineEdit(self)
        self.masque.setPlaceholderText('Masque')
        self.masque.editingFinished.connect(self.isCutoutSR)
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
        #réponse pas toujours présente
        self.lbl_Adress_SR = QLabel('Adresse sous_réseau:', self)
        self.lbl_Adress_SR.setHidden(True)
        self.lbl_Broadcast_SR = QLabel('Adresse Broadcast SR:', self)
        self.lbl_Broadcast_SR.setHidden(True)

        # Ajouter les labels dans le layout vertical des résultats
        self.result_layout.addWidget(self.lbl_AD_reseau)
        self.result_layout.addWidget(self.lbl_Broadcast_IP)
        self.result_layout.addWidget(self.lbl_Adress_SR)
        self.result_layout.addWidget(self.lbl_Broadcast_SR)

        self.result_group.setLayout(self.result_layout)

        # Ajout du groupe de résultats au layout principal
        self.Master_Layout.addWidget(self.result_group)

        # Appliquer le layout principal
        self.setLayout(self.Master_Layout)

        # Connecter le bouton au générateur d'adresse IP
        self.btn_generate.clicked.connect(self.onGenerateClicked)


    def Calc_data(self):
        ip_str = self.AD_IP.text()
        masque_str = self.masque.text()

        try:
            # Conversion des chaînes en objets IPv4
            ip = ipaddress.IPv4Address(ip_str)
            masque = ipaddress.IPv4Network(f"0.0.0.0/{masque_str}", strict=False).netmask

            # Calcul de l'adresse réseau
            adresse_reseau = ipaddress.IPv4Address(int(ip) & int(masque))

            # Calcul de l'adresse de broadcast
            broadcast = ipaddress.IPv4Address(int(adresse_reseau) | (int(masque) ^ 0xFFFFFFFF))

            # Mise à jour des labels avec les valeurs calculées
            self.lbl_AD_reseau.setText(f"Adresse Réseau: {adresse_reseau}")
            self.lbl_Broadcast_IP.setText(f"Adresse Broadcast: {broadcast}")
        except ValueError:
            # Gestion des erreurs de format incorrect
            return "Erreur dans l'IP ou le masque", "Erreur"


    def Calc_data_sr(self, ip_str, masque_str):
        try:
            # Conversion de la chaîne en objet IPv4
            ip = ipaddress.IPv4Address(ip_str)
            # Détermination du masque de classe
            # if ip.is_private or ip.is_loopback or ip.is_reserved:
            #     masque = ipaddress.IPv4Network('10.0.0.0/8', strict=False).netmask  # Classe A
            # elif ip in ipaddress.IPv4Network('172.16.0.0/12'):
            #     masque = ipaddress.IPv4Network('172.16.0.0/12', strict=False).netmask  # Classe B
            # elif ip in ipaddress.IPv4Network('192.168.0.0/16'):
            #     masque = ipaddress.IPv4Network('192.168.0.0/16', strict=False).netmask  # Classe C
            # else:
            #     # Détermination du masque de classe basé sur l'adresse IP
            #     if ip.is_global:
            #         if ip < ipaddress.IPv4Address('128.0.0.0'):
            #             masque = ipaddress.IPv4Network('255.0.0.0', strict=False).netmask  # Classe A
            #         elif ip < ipaddress.IPv4Address('192.0.0.0'):
            #             masque = ipaddress.IPv4Network('255.255.0.0', strict=False).netmask  # Classe B
            #         else:
            #             masque = ipaddress.IPv4Network('255.255.255.0', strict=False).netmask  # Classe C
            #     else:
            masque = ipaddress.IPv4Network(f"0.0.0.0/{masque_str}", strict=False).netmask

            print(masque)
            # Calcul de l'adresse réseau
            adresse_reseau_sr = ipaddress.IPv4Address(int(ip) & int(masque))

            # Calcul de l'adresse de broadcast
            broadcast_sr = ipaddress.IPv4Address(int(adresse_reseau_sr) | (int(masque) ^ 0xFFFFFFFF))
            print(broadcast_sr)
            return str(adresse_reseau_sr), str(broadcast_sr)
        except ValueError:
            # Gestion des erreurs de format incorrect
            return "Erreur dans l'IP", "Erreur"

    def onGenerateClicked(self):
        # Cette méthode est toujours appelée lorsque le bouton est cliqué
        self.isCutoutSR()

    def isCutoutSR(self):
        ip_text = self.AD_IP.text()
        masque_text = self.masque.text()

        try:
            # Convertir l'adresse IP et le masque en objets ip_address et ip_network
            adresse_ip = ipaddress.ip_address(ip_text)
            masque_sous_reseau = ipaddress.ip_network(f"0.0.0.0/{masque_text}", strict=False).netmask

            # Vérification de la classe de l'IP
            premier_octet = int(ip_text.split('.')[0])

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
                raise ValueError("Adresse IP en dehors des classes A, B ou C.")

            # Valider si le masque correspond à la classe
            if masque_sous_reseau > masque_class:
                # Si l'IP est subdivisée en sous-réseaux
                QMessageBox.information(self, "Sous-réseaux",
                                        f"L'adresse IP {ip_text} est subdivisée en sous-réseaux avec le masque {masque_text}.")
                # Appel de la fonction qui traite les sous-réseaux
                adresse_reseau_sr, broadcast_sr = self.Calc_data_sr(ip_text, masque_text)
                self.lbl_Adress_SR.setText(f"Adresse Réseau SR: {adresse_reseau_sr}")
                self.lbl_Broadcast_SR.setText(f"Adresse Broadcast SR: {broadcast_sr}")
                self.lbl_Broadcast_SR.setHidden(False)
                self.lbl_Adress_SR.setHidden(False)

                self.Calc_data()

            else:
                # Si l'IP n'est pas subdivisée
                QMessageBox.warning(self, "Pas de sous-réseaux",
                                    f"L'adresse IP {ip_text} n'est pas subdivisée avec le masque {masque_text}.")
                # Calcul des adresses réseau et broadcast en fonction de la classe
                self.Calc_data()

        except ValueError as e:
            QMessageBox.critical(self, "Erreur", f"Entrée invalide : {e}")


