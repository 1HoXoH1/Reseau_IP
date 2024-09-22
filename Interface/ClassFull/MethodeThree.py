import math

from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import *
import ipaddress
import math


class Methode_Three(QWidget):
    def __init__(self):
        super().__init__()
        # master VBOX
        self.Master_Layout = QVBoxLayout()
        self.Master_Layout.setAlignment(Qt.AlignTop)  # Alignement en haut

        # Création du layout pour les champs de saisie
        self.HLine = QHBoxLayout()
        self.HLine.setAlignment(Qt.AlignCenter)

        self.nbSR = QLineEdit(self)
        self.nbSR.setPlaceholderText('Nombre de sous réseau')
        self.nbHote = QLineEdit(self)
        self.nbHote.setPlaceholderText('Nombre d\'hôtes')
        self.AD_RS = QLineEdit(self)
        self.AD_RS.setPlaceholderText('Adresse réseau')

        # Expression régulière pour un masque CIDR valide
        adress_regex = QRegExp(
            r'^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\/(3[0-2]|[1-2]?[0-9])$')


        # ajout du validateur pour l'adresse réseau
        self.AD_RS_validator = QRegExpValidator(adress_regex, self.AD_RS)
        self.AD_RS.setValidator(self.AD_RS_validator)

        self.btn_generate = QPushButton('Vérification', self)

        self.HLine.addWidget(self.nbSR)
        self.HLine.addWidget(self.nbHote)
        self.HLine.addWidget(self.AD_RS)
        self.HLine.addWidget(self.btn_generate)

        # Ajout des labels qui seront sous les QLineEdit
        self.lbl_nbTotHotes = QLabel('Nomber total d\'hotes : ', self)
        self.lbl_decoupeSR = QLabel('Possibilité de découpe en fonction des sous réseaux ? : ', self)

        # Table pour afficher les sous-réseaux (cachée au début)
        self.tableauSR = QTableWidget(self)
        self.tableauSR.setColumnCount(5)
        self.tableauSR.setMaximumHeight(250)
        self.tableauSR.setMaximumWidth(1100)
        self.tableauSR.setHorizontalHeaderLabels(
            ['Adresse réseau', 'Première IP', 'Dernière IP', 'Broadcast', "Nombre d'hôtes"])
        header = self.tableauSR.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.tableauSR.hide()  # Cacher le tableau au début

        # Appliquer le style CSS au tableau
        self.tableauSR.setStyleSheet("""
                   QTableWidget {
                       background-color: #f0f0f0;  /* Couleur de fond du tableau */
                       border: 2px solid #333;     /* Bordure autour du tableau */
                       gridline-color: #888;       /* Couleur des lignes de séparation */
                   }
                   QHeaderView::section {
                       background-color: #5f5f5f;  /* Couleur de fond des en-têtes */
                       color: white;               /* Couleur du texte des en-têtes */
                       font-weight: bold;          /* Texte en gras dans les en-têtes */
                       border: 1px solid #333;
                       padding: 4px;
                   }
                   QTableWidget::item {
                       border: 1px solid #ccc;     /* Bordure des cellules */
                       padding: 4px;
                   }
                   QTableWidget::item:selected {
                       background-color: #87CEFA;  /* Couleur de la ligne sélectionnée */
                       color: black;               /* Couleur du texte de la ligne sélectionnée */
                   }
               """)


        self.lbl_decoupeIP = QLabel('Possibilité de découpe en fonction des IPs ? : ', self)

        # Ajout des labels à la VLine (sous les champs de saisie)
        self.VLine = QVBoxLayout()
        self.VLine.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Ajouter les labels dans le layout vertical
        self.VLine.addWidget(self.lbl_nbTotHotes)
        self.VLine.addWidget(self.lbl_decoupeSR)
        self.VLine.addWidget(self.tableauSR)
        self.VLine.addWidget(self.lbl_decoupeIP)


        # Ajout du layout horizontal (pour les QLineEdit) et vertical (pour les labels) dans le layout principal
        self.Master_Layout.addLayout(self.HLine)  # Les QLineEdit en haut
        self.Master_Layout.addLayout(self.VLine)  # Les labels en dessous

        self.setLayout(self.Master_Layout)

        # Connecter le bouton au générateur d'adresse IP
        self.btn_generate.clicked.connect(self.lancer_prog)

    def lancer_prog(self):
        self.calc_nb_total_hotes()
        self.verifier_decoupe_sr()



    def calculer_masque_initial(self):
        # Récupérer l'adresse IP
        adresse_reseau = self.AD_RS.text()
        octets = list(map(int, adresse_reseau.split('.')))

        # Vérifier la validité de l'adresse IP
        if len(octets) != 4 or any(o < 0 or o > 255 for o in octets):
            raise ValueError("Adresse IP non valide.")

        # Déterminer le masque en fonction de la tranche d'adresse IP
        if 0 <= octets[0] < 128:
            masque = 8  # Classe A
        elif 128 <= octets[0] < 192:
            masque = 16  # Classe B
        elif 192 <= octets[0] < 224:
            masque = 24  # Classe C
        else:
            raise ValueError("Adresse IP non valide pour les classes A, B ou C.")

        return masque



    def calc_nb_total_hotes(self):
        try:
            masque = self.calculer_masque_initial()

            # Calculer le nombre total d'hôtes
            total_hotes = 2 ** (32 - masque) - 2  # -2 pour les adresses réservées (réseau et broadcast)

            # Afficher le nombre total d'hôtes
            self.lbl_nbTotHotes.setText(f"Nombre total d'hôtes : {total_hotes}")

        except ValueError as e:
            self.lbl_nbTotHotes.setText(f"Erreur : {str(e)}")


    def verifier_decoupe_sr(self):
        try:
            # Récupérer les valeurs saisies
            nombre_sr = int(self.nbSR.text())
            masque_initial = self.calculer_masque_initial()

            # Calculer le nombre de bits disponibles
            bits_disponibles = 32 - masque_initial

            # Calculer le nombre de bits nécessaires pour le nombre de sous-réseaux demandé
            if nombre_sr <= 0:
                raise ValueError("Le nombre de sous-réseaux doit être supérieur à 0.")

            bits_nécessaires = math.ceil(math.log2(nombre_sr))

            # Vérifier si la découpe est possible
            if bits_nécessaires > bits_disponibles:
                self.lbl_decoupeSR.setText(
                    f"Impossible de réaliser la découpe. Bits nécessaires : {bits_nécessaires}, Bits disponibles : {bits_disponibles}")
                self.tableauSR.hide()
                return

            # Calculer le nombre de sous-réseaux possibles
            max_sous_reseaux_possibles = 2 ** bits_nécessaires

            # Vérifier si le nombre de sous-réseaux demandés dépasse le maximum possible
            if nombre_sr > max_sous_reseaux_possibles:
                self.lbl_decoupeSR.setText(
                    f"Impossible de réaliser la découpe. Nombre de sous-réseaux demandés : {nombre_sr}, Max possibles : {max_sous_reseaux_possibles}")
                self.tableauSR.hide()
                return

            # Calculer le nouveau masque
            nouveau_masque = masque_initial + bits_nécessaires

            # Calculer la taille de chaque sous-réseau
            taille_sous_reseau = 2 ** (32 - nouveau_masque)  # Nombre d'adresses dans chaque sous-réseau

            # Convertir l'adresse réseau de départ en entier
            adresse_reseau = self.AD_RS.text()
            reseau = ipaddress.IPv4Network(adresse_reseau, strict=False)
            adresse_entier = int(reseau.network_address)

            # Liste pour stocker les adresses des sous-réseaux
            #plan_adressage = []

            # Réinitialiser et montrer le tableau
            self.tableauSR.setRowCount(nombre_sr)
            self.tableauSR.show()

            # Boucle pour générer chaque sous-réseau
            for i in range(nombre_sr):
                # Créer un sous-réseau à chaque itération
                sous_reseau = ipaddress.IPv4Network((adresse_entier, nouveau_masque), strict=False)
                adresse_reseau = sous_reseau.network_address
                adresse_broadcast = sous_reseau.broadcast_address
                premiere_ip = sous_reseau.network_address + 1
                derniere_ip = sous_reseau.broadcast_address - 1
                nombre_hotes = taille_sous_reseau - 2  # Retirer réseau et broadcast

                # Remplir le tableau avec les informations de chaque sous-réseau
                self.tableauSR.setItem(i, 0, QTableWidgetItem(str(sous_reseau.network_address)))
                self.tableauSR.setItem(i, 1, QTableWidgetItem(str(premiere_ip)))
                self.tableauSR.setItem(i, 2, QTableWidgetItem(str(derniere_ip)))
                self.tableauSR.setItem(i, 3, QTableWidgetItem(str(adresse_broadcast)))
                self.tableauSR.setItem(i, 4, QTableWidgetItem(str(nombre_hotes)))

                # Incrémenter l'adresse réseau de la taille d'un sous-réseau
                adresse_entier += taille_sous_reseau


        except ValueError as e:
            self.lbl_decoupeSR.setText(f"Erreur : {str(e)}")
        except Exception as e:
            self.lbl_decoupeSR.setText(f"Erreur inattendue : {str(e)}")  # Capture toutes les autres erreurs


    #def verifier_decoupe_ip(self):


